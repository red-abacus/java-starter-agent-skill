# Spring AI Runtime and Security

Read when: Changing AI execution limits, telemetry, tool permissions, or untrusted-data boundaries.

Use only relevant sections. [Spring AI index](spring-ai.md#sections); [handbook index](../java-spring-guidelines.md).

## Sections

- [Runtime timeouts, retries, and budgets](#runtime-timeouts-retries-and-budgets)
- [Logging, metrics, and tracing](#logging-metrics-and-tracing)
- [Tool access and execution permissions](#tool-access-and-execution-permissions)
- [Untrusted content and permitted data](#untrusted-content-and-permitted-data)

## Runtime timeouts, retries, and budgets

Extend the existing [integration timeout and retry policy](integrations-background.md#timeouts-and-retries) to AI execution. Start with one attempt, explicit connection/response timeouts, and an overall workflow deadline. Enable bounded transport retries only for classified transient failures where repeating the operation is safe.

Enable output repair only when justified by the workflow, with an explicit attempt limit. Distinguish transport retries, output-repair calls, and planned agent iterations, counting all of them and tool calls within the workflow's time, token, and cost budgets. Select concrete limits during workflow implementation.

Account for Spring AI, transport, and provider SDK retries so attempts do not multiply. Define the outcome when execution limits are exhausted, including how already-completed actions are reported. Verify effective timeout settings, attempt counts, budget exhaustion, and partial execution behavior at the relevant boundaries.

## Logging, metrics, and tracing

Use operational metadata and AI metrics by default, extending the existing [logging conventions](build-configuration.md#configuration-and-logging) and [Micrometer policy](operations.md#metrics-and-tracing). Record workflow, provider/model, duration, outcome, retry counts, tool-call counts, and execution-budget exhaustion at the appropriate boundaries. Track token usage where available and estimated cost when usage and pricing information support it; identify estimates as such.

Keep metric labels bounded. Put request and conversation identifiers in appropriate logs or traces rather than metric labels. Exclude raw prompts, completions, and tool arguments/results from routine telemetry. Enable content capture only for an agreed purpose, with permitted data, redaction, access, and retention defined per project or workflow.

Add tracing when justified per project or workflow, reusing the existing tracing setup. Verify instrumentation and propagation for the actual integration and execution paths, including streaming or asynchronous boundaries where used. Log unexpected propagated failures once at the established boundary, following the existing logging responsibilities.

## Tool access and execution permissions

Use explicit tool allowlists per workflow. Shared default tools are appropriate when every request through that AI client needs those capabilities. Introduce dynamic discovery from an approved catalog when justified by the workflow.

Expose focused operations with typed, validated arguments. Tool classes delegate to existing services through their secured entry points. Resolve caller and tenant context from trusted application context, and enforce capabilities and resource access on each execution under the existing [service-security policy](security-errors.md#security). Filtering tool visibility does not replace execution-time authorization.

During workflow implementation, define which actions may run automatically and which require the application user's confirmation, reusing explicit decisions already supplied. Implement that agreed action policy in application execution logic.

Verify the effective tool allowlist, including tools inherited from client defaults. In the applicable Spring AI APIs, per-call tools append to client defaults; supplying a smaller per-call list alone does not restrict the complete set.

## Untrusted content and permitted data

Treat user input, retrieved documents, conversation history, and tool results as untrusted content. Keep them separate from application-owned instructions. Prompt separation and screening support the controls; application code enforces access and execution boundaries.

Send only data needed for the task and permitted for the caller and selected provider. Define sensitive-data handling during workflow implementation, using existing explicit project decisions. Keep credentials and secrets outside prompts.

Enforce authorization and validate proposed actions in application execution code under the [tool-access policy](#tool-access-and-execution-permissions). Validate model output for its downstream destination, such as safe rendering for HTML and parameterized database queries, in addition to the [typed-response validation](spring-ai-implementation.md#response-formats-and-validation).

Use these application controls by default. Select additional specialized filters or guardrail models per workflow when justified, establishing the permitted data and additional controls during implementation.

Test relevant boundaries with direct and indirect prompt-injection scenarios using harmless fixtures and substitute tools. Evaluate actual authorization, data access, and execution behavior rather than treating prompt wording or screening alone as proof of enforcement.

## Primary references

Consult documentation matching the target project's versions when verifying framework behavior.

- [Spring AI structured-output validation and self-correction calls](https://docs.spring.io/spring-ai/reference/api/structured-output/validation.html)
- [Spring AI observability and content-capture defaults](https://docs.spring.io/spring-ai/reference/observability/)
- [Spring AI tool definition, availability, and execution](https://docs.spring.io/spring-ai/reference/api/tools.html)
- [OWASP prompt-injection controls and verification](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
