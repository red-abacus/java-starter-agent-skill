# Spring AI Implementation

Read when: Changing AI dependencies, clients, prompts, outputs, orchestration, remote integrations, memory, or retrieval.

Use only relevant sections. [Spring AI index](spring-ai.md#sections); [handbook index](../java-spring-guidelines.md).

## Sections

- [Dependency and version alignment](#dependency-and-version-alignment)
- [Component boundaries](#component-boundaries)
- [Provider and model selection](#provider-and-model-selection)
- [Prompt storage and management](#prompt-storage-and-management)
- [Response formats and validation](#response-formats-and-validation)
- [API delivery and streaming](#api-delivery-and-streaming)
- [Workflow and agent orchestration](#workflow-and-agent-orchestration)
- [Remote agents and protocol integration](#remote-agents-and-protocol-integration)
- [Conversation memory](#conversation-memory)
- [Retrieval and RAG](#retrieval-and-rag)

## Dependency and version alignment

Import a pinned, stable `org.springframework.ai:spring-ai-bom` alongside Spring Boot's dependency management. Add only the starters and modules required by the application. Let dependency management supply module versions and document justified overrides.

Verify Java, Spring Boot, Spring AI, and provider SDK compatibility together, using documentation matching the selected versions. Preserve existing project baselines and handle broader upgrades separately under the [gradual-adoption policy](../agent-workflow.md#existing-projects).

## Component boundaries

Use dedicated AI client classes called by domain or workflow services by default. For example, an HTTP flow can delegate from `DocumentController` to `DocumentService`, then `DocumentAiClient`, with the AI client using Spring AI's `ChatClient` for chat-model interaction.

Domain services own business rules, authorization, contextual validation, and decisions about using AI results. AI clients own prompt construction, model calls, and response conversion. Keep business decisions in services.

When tool classes are needed, expose focused operations that delegate to existing services, preserving their authorization and business rules. Introduce workflow services for multi-step coordination according to the existing [service-collaboration convention](architecture-java-style.md#service-collaboration).

Keep the [responsibility-based package organization](architecture-java-style.md#project-structure), using packages such as `services`, `clients`, `tools`, `dto`, and `config` only when they contain relevant code. Separate deployment of AI capabilities remains a justified project-specific architecture choice.

## Provider and model selection

Select providers and models explicitly per workflow, starting with one provider/model wherever it meets the requirements. Decide during workflow implementation according to quality, required capabilities, latency, cost, and data-handling requirements. Different purposes, such as generation and evaluation, may use different models when justified.

Keep model identifiers and generation settings in externalized configuration, following the existing [YAML and typed-properties conventions](build-configuration.md#configuration-and-logging). Use Spring AI's common abstractions where suitable and keep provider-specific details inside AI clients.

Verify required capabilities for the selected Spring AI integration and actual model, including tool calling, structured output, streaming, and relevant modalities. A common API does not establish equivalent behavior across models.

Introduce dynamic routing or fallback only when the workflow requires it, with explicitly defined and verified behavior.

## Prompt storage and management

Keep application-authored prompts in classpath resource files by default, under `src/main/resources/prompts/<workflow>/`, with purpose-specific names such as `system.st` and `user.st`. Avoid inline prompts as much as possible, including short prompts; use them only as a clearly justified exception.

Version prompt resources with application code through Git and review changes alongside the code that consumes them. Dedicated AI clients load the templates through Spring's Resource abstraction and supply their variables. Keep application instructions separate from user-supplied text and retrieved context.

Use external prompt management as a justified exception when a workflow needs independently managed updates. Establish concrete versioning, availability, and rollout behavior for that mechanism during implementation.

## Response formats and validation

Use typed DTOs for AI results consumed by application code, following the existing DTO conventions. Free-form text remains appropriate for answers intended primarily for people to read.

Prefer provider-native schema constraints where the selected integration, actual model, and required schema support them. Verify effective support rather than treating a configuration flag as proof of enforcement. Prompt-based structured conversion remains an alternative where needed; its output is best effort.

Apply explicit layered validation. AI clients parse responses, check their structure, and run applicable DTO validation explicitly. Services validate business meaning, permissions, references, and contextual rules before using the result, following the existing [validation responsibilities](dto-validation-mapping.md#dtos-and-validation). Type conversion alone does not establish that DTO validation ran, and schema conformance does not establish factual or business correctness.

Report unusable output through meaningful exceptions under the existing [exception conventions](security-errors.md#java-exception-conventions). Do not silently substitute empty or fabricated values.

## API delivery and streaming

Use a single completed response by default, especially for typed DTOs requiring validation before application use. Enable streaming when incremental delivery benefits the workflow, preferring Server-Sent Events (SSE) for server-to-client updates.

For streaming, define completion, safe error events, timeouts, disconnect handling, and cancellation during workflow implementation. Treat partial output as provisional and validate completed structured results before business use under the [response-validation policy](#response-formats-and-validation).

Keep controllers responsible for HTTP delivery, services for orchestration, and AI clients for model interaction. Spring MVC can adapt reactive streams for SSE; verify compatible dependencies and behavior for the project's selected Spring AI and Spring versions.

Use the existing [background-execution conventions](integrations-background.md#request--and-event-triggered-execution) when work needs to continue independently of the HTTP connection. Select durable jobs with tracking when the workflow requires persistence, recovery, and later result retrieval.

## Workflow and agent orchestration

Choose the simplest approach that meets the workflow's requirements. Use a single model call for a focused task when sufficient. Prefer code-defined workflows when the sequence and branches are known, using AI in selected steps. Introduce model-directed agents when dynamic planning or tool selection provides a clear benefit.

For agent execution, define termination conditions and limits on steps, elapsed time, and cost during workflow implementation. Concrete limits belong to the affected workflow rather than universal kit values.

Keep orchestration in domain or workflow services, with AI clients handling model interaction and existing services enforcing business rules. Choose synchronous, asynchronous, or durable background execution separately under the existing [execution and coordination conventions](integrations-background.md#request--and-event-triggered-execution), including the affected workflow's ordering and recovery requirements.

## Remote agents and protocol integration

Choose the integration per workflow and boundary. Keep application-owned capabilities as focused local Java tools delegating to services. Use dedicated clients for remote agents or services with established application APIs, following the existing [HTTP integration conventions](integrations-background.md#http-clients-and-organization).

Adopt Spring AI's Model Context Protocol (MCP) integration when standardized access to tools, resources, or prompts benefits the workflow. Consider Agent2Agent (A2A) when independent agents need interoperable task delegation and collaboration. MCP and agent-to-agent protocol libraries remain opt-in; verify compatibility with the selected project versions and remote implementations when adopting them.

Isolate protocol and integration details in dedicated clients or adapters. Reuse the existing authorization, [tool-access rules](spring-ai-runtime.md#tool-access-and-execution-permissions), [timeouts, retry limits, and execution budgets](spring-ai-runtime.md#runtime-timeouts-retries-and-budgets) across these boundaries.

## Conversation memory

Use stateless AI calls by default, supplying the necessary context in each request. Enable conversation memory when the workflow requires continuity. Persistent conversation state can coexist with stateless JWT authentication; it does not require retaining authentication sessions.

When memory is needed, define ownership and authorize access to each conversation. Set context limits, such as message or token budgets, and decide how older context is removed or summarized. Agree storage, retention, and deletion behavior during workflow implementation, reusing explicit project decisions.

Use process-local memory only when losing state on restart is acceptable. Choose persistent/shared storage when conversations must survive restarts or continue across application replicas. Verify that the selected Spring AI version and storage implementation preserve the message types required by the workflow, including tool messages where needed. Follow the existing [migration policy](entities-persistence.md#liquibase-migrations) when the selected storage requires database schema.

Treat model-context memory and complete chat history as separate requirements; selecting a memory window does not establish a full-history storage policy.

## Retrieval and RAG

Introduce retrieval and Retrieval Augmented Generation (RAG) when the workflow needs application data or documents as model context. Choose the simplest retrieval approach that meets the requirements: direct service/database lookup for precise current business data, keyword/full-text search for terminology or exact phrases, or vector/hybrid retrieval when meaning-based search is justified. Vector stores and embeddings are opt-in capabilities.

During workflow implementation, select sources, retrieval limits, relevance criteria, and grounding rules. Enforce caller and tenant access before retrieved material reaches the model, applying the [permitted-data controls](spring-ai-runtime.md#untrusted-content-and-permitted-data).

Define indexing and document-update/deletion behavior where applicable. Preserve source identifiers so generated answers can be traced to retrieved material, and define the outcome when relevant evidence is missing or insufficient.

Evaluate retrieval quality and generated-answer quality separately against the affected workflow's requirements.

## Primary references

Consult documentation matching the target project's versions when verifying framework behavior.

- [Spring AI setup and version compatibility](https://docs.spring.io/spring-ai/reference/getting-started.html)
- [Spring AI ChatClient](https://docs.spring.io/spring-ai/reference/api/chatclient.html)
- [Spring MVC asynchronous responses and streaming](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-async.html)
- [Spring AI model capability comparison](https://docs.spring.io/spring-ai/reference/api/chat/comparison.html)
- [Spring AI prompts, templates, and resources](https://docs.spring.io/spring-ai/reference/api/prompt.html)
- [Spring AI provider-native structured output](https://docs.spring.io/spring-ai/reference/api/structured-output/native.html)
- [Spring AI output converters and limitations](https://docs.spring.io/spring-ai/reference/api/structured-output/converters.html)
- [Spring AI effective workflows and agents](https://docs.spring.io/spring-ai/reference/api/effective-agents.html)
- [Spring AI MCP client and server integration](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-overview.html)
- [A2A agent interoperability and its relationship to MCP](https://a2a-protocol.org/latest/)
- [Spring AI conversation memory and storage](https://docs.spring.io/spring-ai/reference/api/chat-memory.html)
- [Spring AI modular retrieval and RAG](https://docs.spring.io/spring-ai/reference/api/retrieval-augmented-generation.html)
