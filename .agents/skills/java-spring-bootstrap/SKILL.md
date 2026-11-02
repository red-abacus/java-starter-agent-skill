---
name: java-spring-bootstrap
description: Use when starting a new Java or Spring Boot application in an empty or newly scaffolded repository using the owner's working conventions.
---

# Bootstrap a Java/Spring Boot Project

## Establish scope and select guidance

Inspect the repository and known product decisions. Read the [working agreement](../../../docs/agent-workflow.md) and use the [handbook index](../../../docs/java-spring-guidelines.md) to select only the sections needed for requested capabilities. Begin with [project structure and responsibilities](../../../docs/guidelines/architecture-java-style.md#project-structure) and [build/version policy](../../../docs/guidelines/build-configuration.md#build-and-version-policy). The topic list is a router, not required reading in full.

Establish Maven coordinates, base package, application scope, and required integrations. Resolve database and [authentication requirements](../../../docs/guidelines/security-errors.md#authentication-approach) when needed; do not infer a database, microservices, or the example Customer domain. Proceed with independent setup while material requirements remain pending.

## Build the requested capabilities

Verify compatible supported Java LTS/Spring Boot versions through current primary documentation, pin them, and create Maven Wrapper. Record actual build/run commands and adapt the application's AGENTS.md.

For an HTTP API, select affected REST, DTO/mapping, and error-contract sections. Add persistence, external-client, background-work, or cloud guidance only when implementing those capabilities. Follow cross-links when behavior spans layers.

Use the [template index](../../../templates/README.md) to select quality/build and relevant application configuration recipes. Adopt only applicable settings; infrastructure, migrations, profiles, and cache facilities are not automatically part of scaffolding.

## Verify and hand off

Select [tests for implemented surfaces](../../../docs/guidelines/testing.md#testing), then relevant subsections. Verify actual framework/database behavior where applicable, report commands and limitations, and deliver within the working agreement's authorized scope.
