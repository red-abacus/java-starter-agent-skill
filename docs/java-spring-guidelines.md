# Java and Spring Boot Guidelines

These are the owner's accepted defaults. In existing projects, apply the [gradual-adoption policy](agent-workflow.md#existing-projects). Explicit project requirements and the current task determine what changes. Examples use `Customer` and `com.example`; these are illustrative names, not mandatory domain or package choices.

## Select guidance by task

This file is a routing index. Read the applicable project instructions and [working agreement](agent-workflow.md), then select the references below. Read only relevant sections; follow additional links when the behavior crosses a boundary. The references are not a checklist to load in full.

| Task touches | Read |
| --- | --- |
| Packages, class responsibilities, service contracts, Java style, collections, decimal values, or opt-in caching | [Architecture and Java style](guidelines/architecture-java-style.md) |
| Comments, Javadoc, README content, or architectural decision records | [Documentation conventions](guidelines/architecture-java-style.md#documentation-and-comments) |
| HTTP paths, updates, responses, pagination, binding, versioning, ETags, or OpenAPI | Relevant [REST contract sections](guidelines/rest-api.md#sections) |
| DTO inheritance, request validation, or structural mapping | [DTO validation and mapping](guidelines/dto-validation-mapping.md); for PATCH, the [worked example](examples/partial-updates.md) |
| Entities, repositories, transactions, deletion, constraints, or migrations | Relevant [persistence sections](guidelines/entities-persistence.md#sections) |
| Authentication, CORS/CSRF, capability/resource checks, exceptions, errors, or localization | Applicable [security/error sections](guidelines/security-errors.md#sections) |
| Provider HTTP calls, commit-dependent effects, scheduling, or asynchronous work | Relevant [integration/background sections](guidelines/integrations-background.md#sections) |
| AI framework selection | [Spring AI preference](guidelines/spring-ai.md#framework-preference) |
| AI dependencies, clients, prompts, outputs, agents, memory, or retrieval | Relevant [AI implementation sections](guidelines/spring-ai-implementation.md#sections) |
| AI execution limits, telemetry, tools, or data trust boundaries | Relevant [AI runtime/security sections](guidelines/spring-ai-runtime.md#sections) |
| AI workflow tests, model evaluations, or evaluation deployment gates | Relevant [AI evaluation sections](guidelines/spring-ai-evaluations.md#sections) |
| Tests or verification of changed behavior | [Testing surfaces](guidelines/testing.md#testing), then the applicable subsection |
| Maven/JDK/Boot setup, dependency updates, security scanning, configuration binding, or logging | Relevant [build/configuration sections](guidelines/build-configuration.md#sections) |
| Reliability goals, alerts, probes, shutdown, resources, scaling, placement, metrics, or tracing | Relevant [operations sections](guidelines/operations.md#sections) |
| GKE identities/secrets, image packaging, Helm, environments, or CI/CD | Relevant [delivery sections](guidelines/delivery-gke.md#sections) |

## Scope examples

- A DTO PATCH fix starts with DTO/mapping guidance and its example; add HTTP, persistence, security, and test sections only as affected.
- A migration starts with persistence/migrations and database testing; consult API contracts only if behavior changes.
- A Helm-only change starts with [chart organization](guidelines/delivery-gke.md#helm-chart-organization) and [rollout verification](guidelines/delivery-gke.md#deployment-strategy-and-release-verification); add [availability controls](guidelines/operations.md#availability-during-maintenance-and-failures) when budgets or placement change.
- A minimal bootstrap reads architecture and build/configuration first, adding references for the capabilities actually requested.

## Adoption and primary references

Use the [template index](../templates/README.md) only when adopting or changing configuration recipes. Each topic lists its primary sources. Consult the documentation matching the target project's versions, rather than relying on a newer API from a tutorial.
