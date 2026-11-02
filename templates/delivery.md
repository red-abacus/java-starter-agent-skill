# Delivery Recipes

Read only the recipe sections needed for the configuration being adopted. [Template index](README.md).

## Container images

For target applications, follow the [packaging policy](../docs/guidelines/delivery-gke.md#application-packaging): run `./mvnw verify`, then use `./mvnw spring-boot:build-image` with Spring Boot's Maven plugin and a compatible Docker daemon. Configure the Artifact Registry image name, selected Java runtime, and pinned builder/runtime inputs for the project. Use a Dockerfile when justified by its image requirements.

Publish through the project's authorized delivery workflow, capture the image digest, and supply that digest to Helm releases. Promote the same image across environments with external runtime configuration. Registry authentication, CI configuration, and actual deployment environments are established per project.

## Helm charts

Decide the [actual environment set and promotion rules](../docs/guidelines/delivery-gke.md#environments-and-promotion) during project development. Development, staging, and production are usual; a POC/MVP may use a single environment. Generate only the required overrides and delivery configuration.

For target applications, keep an application-owned chart under `helm/<application>/` with Chart.yaml, templates, values.yaml, and values.schema.json. Use small environment override files only for actual environments. Supply the Artifact Registry image repository and digest explicitly and reference externally managed secrets. Chart versions evolve independently from application image versions.

Apply the [resource sizing policy](../docs/guidelines/operations.md#resource-budgets-and-jvm-sizing): configure CPU/memory requests and a memory limit, choosing CPU limits per platform/workload. Start with Paketo's memory calculator when using its buildpacks, retain room for non-heap/native memory, and avoid competing heap flags. Select actual allocations per project, document provisional POC values, and validate startup and representative load before tuning resources or JVM behavior.

Follow the [replica and autoscaling policy](../docs/guidelines/operations.md#replicas-and-autoscaling): fixed replicas suit simple workloads; add HPA when justified. Select actual replica counts, availability-related placement, metrics, bounds, and scaling behavior per application/environment. Budget database and downstream capacity for maximum replicas plus rollout overlap, and verify multi-replica behavior. The kit does not prescribe universal replica counts or generate an HPA resource.

For deployments with availability requirements, apply the [maintenance and failure policy](../docs/guidelines/operations.md#availability-during-maintenance-and-failures). Discuss availability needs, PDB settings, placement strictness, and cluster capacity with the user during implementation before finalizing those settings, using existing explicit project answers. Keep controls optional for single-replica POCs accepting interruption, and verify node drains, replacement scheduling, and reduced-replica capacity where required.

Use the [release strategy policy](../docs/guidelines/delivery-gke.md#deployment-strategy-and-release-verification): rolling updates by default, with availability settings and capacity selected for the application. Coordinate readiness, graceful shutdown, and compatibility between overlapping versions. Verify rollout within a bounded timeout and run focused deployed smoke checks; failed checks fail the release and invoke the project's recovery policy. Application rollback and database recovery require separate consideration.

Run `helm lint` and `helm template` with the intended environment values and image inputs before delivery. Follow the [chart organization policy](../docs/guidelines/delivery-gke.md#helm-chart-organization) and adopt a versioned library chart when repeated patterns justify shared helpers. The kit documents this layout; generate concrete charts from the target application's requirements.

## GitHub Actions

Use the handbook's [verification/publish/deploy workflow boundaries](../docs/guidelines/delivery-gke.md#github-actions-workflows-and-cloud-authentication). Generate concrete workflows for the target application's Maven, OpenAPI, and Helm checks, Artifact Registry image publication, and Helm deployment by digest.

Publish images after merges into `main`, verifying and recording the exact resulting revision. Use GitHub OIDC with the existing Google Cloud Workload Identity Federation integration where applicable. Configure the actual provider references, repository/release trust conditions, and narrowly scoped identities/permissions for the project. Pin action dependencies to reviewed immutable revisions and serialize deployments to the same Helm release. Choose deployment triggers, promotion rules, and cancellation behavior for the project.
