# Spring AI Guidelines

Read when: Implementing or reviewing AI integrations, agents, evaluations, or AI-powered pipelines in Java/Spring Boot applications.

Use only the references and sections needed for the task. [Handbook index](../java-spring-guidelines.md).

## Framework preference

Prefer Spring AI as the integration framework for AI capabilities in Java/Spring Boot projects. Introduce AI dependencies and integrations when the application requires those capabilities, following the [gradual-adoption policy](../agent-workflow.md#existing-projects) for existing projects.

These guidelines provide general conventions to adapt to each workflow. Establish concrete AI requirements during project and workflow discovery, reusing explicit decisions already supplied. The framework preference does not select a provider, model, agent architecture, evaluation strategy, or pipeline execution mechanism.

Follow the existing [build and version policy](build-configuration.md#build-and-version-policy) when selecting compatible project versions.

## Sections

This file routes accepted policies to focused references. Follow cross-links when the affected behavior crosses a boundary; the table is not required reading in full.

| Task touches | Read |
| --- | --- |
| AI dependencies or compatible version selection | [Dependency and version alignment](spring-ai-implementation.md#dependency-and-version-alignment) |
| Class responsibilities or package organization | [Component boundaries](spring-ai-implementation.md#component-boundaries) |
| Provider/model selection or generation settings | [Provider and model selection](spring-ai-implementation.md#provider-and-model-selection) |
| Prompt resources or template changes | [Prompt storage and management](spring-ai-implementation.md#prompt-storage-and-management) |
| Typed outputs, conversion, or validation | [Response formats and validation](spring-ai-implementation.md#response-formats-and-validation) |
| Completed responses, SSE, or background results | [API delivery and streaming](spring-ai-implementation.md#api-delivery-and-streaming) |
| Code-defined workflows or model-directed agents | [Workflow and agent orchestration](spring-ai-implementation.md#workflow-and-agent-orchestration) |
| Remote agents, MCP, or A2A | [Remote agents and protocol integration](spring-ai-implementation.md#remote-agents-and-protocol-integration) |
| Conversation continuity or history | [Conversation memory](spring-ai-implementation.md#conversation-memory) |
| Retrieval, embeddings, or RAG | [Retrieval and RAG](spring-ai-implementation.md#retrieval-and-rag) |
| Timeouts, retries, output repair, or execution budgets | [Runtime timeouts, retries, and budgets](spring-ai-runtime.md#runtime-timeouts-retries-and-budgets) |
| AI logs, metrics, tracing, or content capture | [Logging, metrics, and tracing](spring-ai-runtime.md#logging-metrics-and-tracing) |
| Tool availability, caller context, or execution permissions | [Tool access and execution permissions](spring-ai-runtime.md#tool-access-and-execution-permissions) |
| Permitted data, prompt injection, or output trust | [Untrusted content and permitted data](spring-ai-runtime.md#untrusted-content-and-permitted-data) |
| Application tests, datasets, or evaluation criteria | [Testing and evaluations](spring-ai-evaluations.md#testing-and-evaluations) |
| Live-evaluation triggers or deployment gating | [Evaluation execution and deployment gates](spring-ai-evaluations.md#evaluation-execution-and-deployment-gates) |

## Primary references

- [Spring AI capabilities](https://docs.spring.io/spring-ai/reference/index.html)
