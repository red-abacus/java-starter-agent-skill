# GKE Delivery

Read when: Preparing or changing cloud identity, secrets, images, Helm releases, environments, or CI/CD.

Use only the sections relevant to the task. [Handbook index](../java-spring-guidelines.md).

## Sections

- [Delivery infrastructure](#delivery-infrastructure)
- [Application identity and Google Cloud clients](#application-identity-and-google-cloud-clients)
- [Secret storage and delivery](#secret-storage-and-delivery)
- [Environments and promotion](#environments-and-promotion)
- [Application packaging](#application-packaging)
- [Helm chart organization](#helm-chart-organization)
- [Deployment strategy and release verification](#deployment-strategy-and-release-verification)
- [GitHub Actions workflows and cloud authentication](#github-actions-workflows-and-cloud-authentication)

## Delivery infrastructure

Default to Google Kubernetes Engine (GKE) for application deployment, Google Artifact Registry for container images, Helm for releases, and GitHub Actions for CI/CD. Apply these as new-project defaults while preserving explicit project requirements and existing infrastructure during gradual adoption.

Establish concrete Google Cloud projects, locations, registry repositories, clusters, namespaces, Helm chart sources, release configuration, and CI runner/tool configuration for the target project. Scope infrastructure changes, publishing, and deployment actions to the requested work.

### Application identity and Google Cloud clients

Use Workload Identity Federation for GKE when applications access Google Cloud APIs. Assign an appropriate Kubernetes ServiceAccount to each application or distinct workload and grant narrowly scoped permissions on the resources it needs. Prefer direct IAM grants to the workload principal where supported; use IAM service-account impersonation when API limitations or established identity requirements justify it. Reuse existing cluster identity infrastructure after checking its configuration.

Use Application Default Credentials (ADC) with Google Cloud Java clients and compatible Spring integrations so runtime credentials come from the workload identity. Avoid distributing service-account private-key files. Keep application runtime permissions separate from CI publishing/deployment permissions; end-user API authentication remains a project-specific concern.

Select Spring Framework on Google Cloud (commonly called Spring Cloud GCP) starters per integration when their auto-configuration or Spring abstractions are useful. Plain Google Cloud Java clients are also appropriate; WIF and ADC do not require Spring Cloud. When adopting these modules, select a compatible, pinned Google Cloud Spring BOM for the project's Spring Boot/Spring Cloud versions. Keep provider adapters in responsibility-based packages such as `clients`, with business rules in services.

### Secret storage and delivery

Store application secrets in Google Secret Manager by default, restricting access to the required application and environment. Load configuration secrets at startup through the compatible Secret Manager Spring starter, authenticated through WIF and ADC. Bind settings through the existing typed configuration approach and fail startup if a required secret cannot be loaded.

Keep secret references and version selections in external application/deployment configuration. Keep secret values outside Git, container images, and Helm values. Pin secret versions and update them through controlled releases; configuration-secret rotation uses a rolling restart by default. Coordinate rotation with the system that accepts the credential and the release's recovery requirements.

Use live refresh only when the affected configuration, clients, and connection pools explicitly support it and the behavior is tested. Updating a remote secret or mounted file alone does not establish that existing application objects reload it. GKE-mounted secrets or synchronization to Kubernetes Secrets are justified alternatives where the platform requires them; establish access controls and rotation/reload behavior for the selected delivery mechanism.

### Environments and promotion

The usual environment setup is development, staging, and production. A POC/MVP may start with a single environment. Decide the actual environment set during development of the target project, adapting it to the project's needs and maturity.

Establish deployment triggers and promotion rules during that work, including which environments deploy automatically. Publishing an image after a merge to main defines publication timing; environment deployment is a separate decision. Create profiles, Helm overrides, and delivery configuration only for the environments the project actually uses.

### Application packaging

Use a container image as the primary delivery artifact for the default GKE target. Package the application through Spring Boot's Maven plugin, with an executable JAR as input to image construction. Use Cloud Native Buildpacks by default, adapting execution to the project's CI environment. Spring Boot's `build-image` goal requires access to a Docker daemon. Choose a Dockerfile when custom operating-system packages, organizational base-image requirements, or other image requirements are better expressed that way, and preserve established project packaging during gradual adoption.

Run Maven verification before image creation so the full configured checks run:

```sh
./mvnw verify
./mvnw spring-boot:build-image
```

Align the image's Java runtime with the project's selected baseline and pin image inputs per project. Publish images to Artifact Registry with release or commit-based tags, capture their digests, and reference the digest in Helm releases. Promote the same image across environments, supplying environment-specific runtime configuration through deployment configuration. Select concrete image references and publishing behavior within the target project's authorized delivery workflow.

### Helm chart organization

Default to an application-owned chart alongside the application code under `helm/<application>/`. Keep shared, non-sensitive defaults in `values.yaml` and small overrides for the environments the project actually has, such as `values-dev.yaml` and `values-prod.yaml`.

Include Chart.yaml, templates, and a values.schema.json that validates important configurable values. Pass the image repository and digest explicitly and reference externally managed secrets. Version the chart independently from the application image; appVersion is descriptive application metadata rather than the chart version or an implicit image selector.

Run `helm lint` and render supported environment configurations with `helm template` using their intended values and image inputs. These checks validate values and rendered output locally; verify deployment-specific behavior against the target environment as required by the change.

When repeated deployment patterns emerge, extract shared helpers into a versioned library chart. Preserve established shared-chart or separate-deployment-repository workflows during gradual adoption.

### Deployment strategy and release verification

Use rolling updates by default for APIs. Choose Recreate when overlapping versions are incompatible and downtime is acceptable, or canary/blue-green delivery when release risk justifies the additional infrastructure. For availability-sensitive APIs, start with `maxUnavailable: 0` and `maxSurge: 1` when capacity permits overlap, then adjust for application size and requirements.

Use readiness checks to establish when replacements can serve traffic and apply the graceful shutdown policy to terminating instances. Preserve compatibility between overlapping application versions, including the adopted phased schema-evolution policy. Deployment rollout settings control availability during application updates; PodDisruptionBudgets constrain supported voluntary evictions and do not govern a Deployment's rolling updates.

Give deployment verification a bounded timeout and run focused smoke checks against the deployed application. Treat a stalled rollout or failed smoke check as a failed release. Capture diagnostics and follow the project's recovery policy, considering application rollback and database recovery separately. Select concrete rollout settings, checks, timeouts, and recovery behavior for the target project and verify the actual release path before reporting success.

### GitHub Actions workflows and cloud authentication

Separate verification, image publishing, and deployment into focused workflows under `.github/workflows/`:

| Workflow | Responsibility |
| --- | --- |
| `ci.yml` | Pull-request Maven verification, OpenAPI validation/compatibility checks, and Helm lint/render checks. |
| `ai-evals.yml` (AI applications) | Model-backed evaluations on pushes to `main`, with results tied to the evaluated revision and configuration. |
| `publish.yml` | Verify the selected trusted revision, build and publish its image to Artifact Registry, and record the digest. |
| `deploy.yml` | Deploy an existing image digest and selected chart version through Helm, then verify rollout and focused smoke checks. |

Apply the [portable security-scanning policy](build-configuration.md#portable-security-scanning) at the agreed workflow points. Keep scanner configuration and commands in the repository so the checks can also run locally or on another CI provider; define blocking rules during project implementation.

For AI applications, enforce the [evaluation deployment gate](spring-ai-evaluations.md#evaluation-execution-and-deployment-gates): require passing model-backed evaluations for the revision being deployed. Keep live-model evaluations out of PR and scheduled CI runs; their CI trigger is a push to `main`. Ensure separate deployment workflows cannot bypass this gate.

The current image-publication trigger is a merge into `main`. Verify the resulting main-branch revision before building and publishing, and associate the image tag and digest with that exact revision. Configure event wiring consistently with the project's main-branch policy.

Promote the same image across environments. Choose deployment triggers and environment-promotion rules per project. Give verification jobs only the permissions they need and pin action dependencies to reviewed immutable revisions.

Authenticate to Google Cloud using GitHub OIDC with Workload Identity Federation and short-lived credentials, with narrowly scoped publishing/deployment permissions and trust restricted to intended repository and release contexts. Reuse the owner's existing GitHub-to-GCP WIF integration where applicable. Establish the target project's provider references, trust conditions, and required identities/permissions rather than recreating federation infrastructure automatically.

Serialize deployments targeting the same Helm release. Cancel superseded verification runs where useful and define deployment cancellation behavior deliberately. Verify workflow checks and the configured authentication and release paths at the appropriate boundaries before claiming they work.

## Primary references

Consult documentation matching the target project's versions when verifying framework behavior.

- [Spring Boot OCI image packaging](https://docs.spring.io/spring-boot/maven-plugin/build-image.html)
- [Artifact Registry image storage and publishing](https://docs.cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling)
- [GKE image digests](https://docs.cloud.google.com/kubernetes-engine/docs/concepts/about-container-images)
- [Workload Identity Federation for GKE](https://docs.cloud.google.com/kubernetes-engine/docs/concepts/workload-identity)
- [GKE workload permissions and service-account impersonation](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/workload-identity)
- [Application Default Credentials](https://docs.cloud.google.com/docs/authentication/application-default-credentials)
- [Spring Framework on Google Cloud credentials](https://googlecloudplatform.github.io/spring-cloud-gcp/reference/html/core.html)
- [Google Cloud Spring modules and compatibility](https://github.com/GoogleCloudPlatform/spring-cloud-gcp)
- [Google Cloud Spring Secret Manager integration](https://googlecloudplatform.github.io/spring-cloud-gcp/reference/html/index.html)
- [Secret Manager best practices](https://docs.cloud.google.com/secret-manager/docs/best-practices)
- [GKE Secret Manager mounted-secret integration](https://docs.cloud.google.com/secret-manager/docs/secret-manager-managed-csi-component)
- [Helm charts and values schemas](https://helm.sh/docs/topics/charts/)
- [Helm values overrides](https://helm.sh/docs/chart_template_guide/values_files/)
- [Helm library charts](https://helm.sh/docs/topics/library_charts/)
- [Kubernetes Deployment strategy and rollout status](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [GitHub OIDC authentication to Google Cloud](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-google-cloud-platform)
- [Google Cloud authentication action](https://github.com/google-github-actions/auth)
- [GitHub workflow concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency)
- [GitHub workflow trigger events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)
- [GitHub Actions dependency security](https://docs.github.com/en/actions/reference/security/secure-use)
