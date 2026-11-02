---
name: java-spring-review
description: Use when reviewing Java or Spring Boot changes for correctness and consistency with the owner's conventions, including pull requests and pre-delivery reviews.
---

# Review Java/Spring Boot Changes

## Establish scope and select guidance

Stay read-only unless fixes are requested. Obtain the actual diff or review target, surrounding context, contracts, and evidence. Read the [working agreement](../../../docs/agent-workflow.md) and use the [handbook index](../../../docs/java-spring-guidelines.md) to select only sections relevant to the affected behavior. For Helm-only reviews, use the index's chart/rollout links and affected operations sections.

Respect established project requirements. An existing build tool, framework baseline, formatter, or public response contract is not a defect merely because a new-project default differs.

## Follow affected behavior

Use [architecture/service guidance](../../../docs/guidelines/architecture-java-style.md#responsibilities) for layer boundaries. Select REST, DTO/mapping, persistence, security/errors, integrations, or operational guidance as touched; follow cross-links for actual dependencies.

For PATCH, consult [DTO validation/mapping](../../../docs/guidelines/dto-validation-mapping.md) and the [worked example](../../../docs/examples/partial-updates.md). For authorization or transactions, inspect actual intercepted calls and corresponding tests. For workflow-specific choices, verify the required user decisions were established. Load template recipes only when reviewing their adoption.

## Assess evidence and report

For application behavior, consult the [testing surface table](../../../docs/guidelines/testing.md#testing) and applicable subsections. For chart/workflow-only changes, use the verification requirements in the affected delivery/operations sections. Distinguish demonstrated defects, missing verification, and convention suggestions. Do not infer framework behavior from plain mocks or report unexecuted checks as passing.

Report substantive findings with location, concrete trigger, impact, and focused remedy, followed by material test limits. If no actionable issues were found, say so. Do not manufacture findings or edit, commit, publish, or merge during read-only review.
