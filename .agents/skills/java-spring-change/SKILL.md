---
name: java-spring-change
description: Use when implementing a feature, fixing a bug, or changing Java or Spring Boot application code under the owner's working conventions.
---

# Change a Java/Spring Boot Application

## Scope and select guidance

Inspect applicable instructions, nearby code, contracts, tests, build, and user changes. Read the [working agreement](../../../docs/agent-workflow.md) and use the [handbook index](../../../docs/java-spring-guidelines.md) to select affected topic sections. Keep existing requirements and unrelated work intact. Read additional references when the behavior crosses a boundary, rather than loading the whole library.

For a clear change, state the approach briefly and proceed. Align substantial architectural or uncertain product decisions before implementation; continue through authorized implementation and verification.

## Implement at the owning layer

Use the [architecture/service sections](../../../docs/guidelines/architecture-java-style.md#responsibilities) when changing responsibilities and the Java/Lombok sections when style choices arise. Select API, persistence, security/error, integration, configuration, or delivery sections according to what the change touches.

For PATCH, read [DTO validation/mapping](../../../docs/guidelines/dto-validation-mapping.md) and the [worked example](../../../docs/examples/partial-updates.md). Preserve inheritance and omitted/null/value semantics. Add relevant HTTP, transaction, authorization, and persistence guidance when affected; do not infer those behaviors from mapping alone.

For deletion, caching, external effects, or availability configuration, resolve the guide's workflow-specific requirements using explicit answers already supplied. Read [configuration recipes](../../../templates/README.md) only when adopting or changing that configuration.

## Verify and deliver

Use the [testing surface table](../../../docs/guidelines/testing.md#testing), then applicable subsections. Run meaningful checks and the project's required verification, reporting actual results and unavailable checks. Deliver verified local changes by default; Git actions follow the working agreement and the user's request.
