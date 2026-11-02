# External Integrations and Background Work

Read when: Changing provider clients, external-effect ordering, scheduling, or asynchronous work.

Use only the sections relevant to the task. [Handbook index](../java-spring-guidelines.md).

## Sections

- [External integrations](#external-integrations)
- [HTTP clients and organization](#http-clients-and-organization)
- [Timeouts and retries](#timeouts-and-retries)
- [Provider failures](#provider-failures)
- [Workflow ordering and database coordination](#workflow-ordering-and-database-coordination)
- [Background work](#background-work)
- [Scheduled tasks](#scheduled-tasks)
- [Request- and event-triggered execution](#request--and-event-triggered-execution)

## External integrations

### HTTP clients and organization

Use `RestClient` by default for external HTTP calls in imperative MVC/JPA applications. Put communication in dedicated, provider-focused classes under `clients`, such as `PaymentProviderClient`. Services call these clients and retain business decisions and workflow coordination.

Keep provider request/response DTO types separate from public API DTOs. Build clients using Spring Boot's injected `RestClient.Builder` to retain its configured defaults, with provider-specific configuration applied during initialization.

Introduce declarative Spring HTTP Service interfaces when they make an integration clearer; generated proxies can use RestClient as their synchronous transport. These interfaces express a justified remote boundary and do not require handwritten service interface/implementation pairs. Choose WebClient when reactive processing or streaming requirements justify it.

Use APIs compatible with the target project's versions and preserve existing integration conventions during gradual adoption.

### Timeouts and retries

Configure explicit connection and read/response timeouts per provider through typed configuration. Define and enforce an overall operation budget covering attempts and waits. Choose limits for the integration's requirements, and verify the effective HTTP transport settings; individual timeout settings do not automatically establish a total deadline.

Start with one attempt. Enable retries deliberately per operation, only for explicitly classified transient failures when repeating the operation is safe. A timeout does not prove that the remote operation was never applied. Preserve the existing idempotency policy.

For retry-enabled operations, configure a small total attempt limit, including the initial call, with exponential backoff and jitter. Respect applicable Retry-After instructions within the remaining operation budget; stop when the required delay or another attempt cannot fit. Unchanged requests rejected for validation, permissions, or permanent business reasons are not transient failures.

Configure retries at one owning layer, accounting for HTTP transport and provider SDK retries so attempts do not multiply unexpectedly. Test failure classification, attempt counts, delays, budget exhaustion, and uncertain remote outcomes at the appropriate integration boundary. Timeout and retry mechanisms must be compatible with the target project's versions; no specific resilience library is mandated by this policy.

### Provider failures

Use layered error translation. Clients normalize transport failures and provider responses into focused integration exceptions, preserving causes and useful internal metadata. Services interpret documented business outcomes and translate them to the application's business meaning. Centralized advice constructs the established ProblemDetail response with a stable code, traceId, and safe localized text.

Choose status codes according to the application's meaning and role, using these defaults where applicable:

| Meaning | Response |
| --- | --- |
| Recognized business rejection | Appropriate established 400/404/409 contract |
| Temporary dependency unavailability prevents completion | 503 |
| Required upstream response times out while acting as a gateway | 504 |
| Invalid upstream response while acting as a gateway | 502 |
| Unexpected application or integration configuration failure | 500 |

Classify failures rather than copying provider status codes automatically. Rejection of the application's own provider credentials is a server-side integration problem, not evidence that the API caller must authenticate again. Likewise, a provider's 404 becomes an application missing-resource result only when the use case gives it that meaning.

Keep raw provider payloads, credentials, and internal diagnostics out of public errors. Follow the existing logging ownership policy so an unexpected propagated failure is logged once at its handling boundary. Verify provider-to-integration translation and public error contracts with focused tests.

### Workflow ordering and database coordination

Discover ordering and delivery requirements with the user for each affected workflow before selecting its coordination mechanism, unless that workflow's behavior is already explained. Establish which steps depend on committed database changes, which are independent, whether the response needs an external result, and how failures, uncertain outcomes, and interrupted delivery should be handled.

A notification announcing a database change waits for successful commit. Saving or flushing an entity alone is not a successful commit. Independent external operations may run before database work when the agreed flow permits it. Choose ordering according to these dependencies rather than applying one sequence to every workflow.

Keep database transactions short and place external HTTP calls outside them by default. A normal database rollback does not undo an external HTTP operation. Use synchronous service/workflow coordination when the external result is needed immediately, with explicit partial-failure recovery where required.

For follow-up work that must survive interruption, persist delivery intent alongside the business change in the same database transaction and process it after commit, using an appropriate outbox or persisted-job mechanism. Account for possible repeated delivery. Use an ordinary in-memory after-commit listener only when the agreed workflow accepts best-effort delivery. Define pending, completed, and failed states where needed; select infrastructure according to the workflow rather than requiring it in every project.

Verify the agreed sequencing, commit/rollback behavior, and recovery guarantees at their actual boundaries.

## Background work

### Scheduled tasks

Use Spring `@Scheduled` for simple periodic tasks, enabling scheduling when used. Keep scheduling components thin under `schedulers` and delegate business operations to services.

Externalize schedules and enable/disable settings. Set cron time zones explicitly: UTC by default, or the agreed business zone. During workflow discovery, establish whether overlapping runs are allowed, missed runs need recovery, and execution should happen once across all application instances.

An in-process schedule alone does not provide durable delivery or coordination across instances. Add coordination where instances must share one logical schedule, and account for repeated execution according to the workflow. Choose Quartz with JDBC storage when persistent schedules and configurable handling of missed runs are required, or platform scheduling when execution belongs to deployment infrastructure. Select these mechanisms from the workflow's requirements; durable work delivery remains an explicit requirement in its own right.

### Request- and event-triggered execution

Use synchronous execution by default. Select background execution during workflow discovery according to ordering, completion, and delivery requirements. Use `@Async` with a managed executor for in-process work whose pending tasks may be lost during restart; use durable jobs or queues when persistence, recovery, and tracked completion are required, following the existing database-coordination policy.

Enable async support explicitly when used and invoke through a separate Spring-managed bean so proxy-based interception applies. Configure bounded concurrency and queue capacity, with explicit task rejection, shutdown, and failure-reporting behavior. Observe failures through returned futures or an explicit asynchronous exception handler.

Pass identifiers or immutable task data and load required persistence state inside the worker's own transaction. Ordinary thread-bound transactions do not propagate to newly started threads. Establish the required execution identity, tenant context, and trace context explicitly, preserving authorization requirements and clearing propagated context after execution.

Verify actual asynchronous invocation, failure handling, context isolation, and transaction behavior where the workflow depends on them; a direct method call alone does not prove interception.

## Primary references

Consult documentation matching the target project's versions when verifying framework behavior.

- [HTTP retry safety](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)
- [HTTP Retry-After guidance](https://www.rfc-editor.org/rfc/rfc9110.html#section-10.2.3)
- [HTTP server error semantics](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.6)
- [Spring transaction-bound events](https://docs.spring.io/spring-framework/reference/data-access/transaction/event.html)
- [Transactional outbox pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html)
- [Spring Security concurrency support](https://docs.spring.io/spring-security/reference/servlet/integrations/concurrency.html)
- [Spring REST clients and HTTP Service interfaces](https://docs.spring.io/spring-framework/reference/integration/rest-clients.html)
- [Spring Boot HTTP client configuration](https://docs.spring.io/spring-boot/reference/io/rest-client.html)
- [Spring task execution and scheduling](https://docs.spring.io/spring-framework/reference/integration/scheduling.html)
- [Spring Boot Quartz support](https://docs.spring.io/spring-boot/reference/io/quartz.html)
