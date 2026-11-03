# DTO Validation and Mapping

Read when: Changing DTO inheritance, validation, JSON presence, or ModelMapper behavior.

Use only the sections relevant to the task. [Handbook index](../java-spring-guidelines.md).

## Sections

- [DTOs and validation](#dtos-and-validation)
- [Mapping and entities](#mapping-and-entities)

## DTOs and validation

For each domain, share genuinely common fields through a base DTO; extend it for create, update, and response particularities. Keep server-owned identifiers/audit information in appropriate response DTOs rather than making them client-writable merely to reuse a base.

Express as much request-body validation as possible on DTOs. Reject forbidden nulls for client-supplied fields there, using `@NotNull` or `@NotBlank` when a string must also contain non-whitespace characters. Trigger DTO validation at the HTTP boundary before delegating to the business operation, avoiding unnecessary persistence calls. Apply operation-specific requiredness and the PATCH presence rules below.

Services perform checks that need business context or cannot reasonably be represented on DTOs. Validate state that service transformations can invalidate; successful input validation is not proof of valid final state.

For AI-generated DTOs, follow the [AI response validation convention](spring-ai-implementation.md#response-formats-and-validation): validate explicitly at the AI boundary and apply contextual business rules in services.

For monetary and exact decimal fields, align validation with the workflow's agreed [precision, scale, and rounding rules](architecture-java-style.md#money-and-decimal-values) and database columns.

Inherited Bean Validation constraints accumulate. An overridden getter can add a constraint, but cannot remove or relax one from its parent. Put only universally applicable constraints in the base; put creation-only requiredness on the create child's getter. Prefer child-specific rules over operation validation groups. When changing a base constraint, inspect every affected child to preserve its contract.

Partial updates have three states:

| Request | Result |
| --- | --- |
| Field omitted | Keep the stored value. |
| Explicit `null` | Clear if nullable; reject if clearing is forbidden. |
| Supplied value | Validate and apply it. |

An ordinary nullable field or `Optional<T>` alone loses the first/second distinction. Preserve JSON field presence in the update DTO. Requiredness for a supplied PATCH field must allow omission while rejecting a forbidden explicit null; an unconditional inherited `@NotBlank` is unsuitable. Child-specific, presence-aware DTO validation can express that rule without validation groups or abandoning the DTO hierarchy. See the [worked PATCH example](../examples/partial-updates.md).

## Mapping and entities

Use ModelMapper in dedicated mapper classes, such as `CustomerMapper`, called by services. Keep pure property conversion separate from business decisions. Use Jackson for JSON binding rather than replacing DTO/entity mapping with `ObjectMapper.convertValue` by default.

Configure mappings predictably at initialization. Avoid changing a shared mapper's configuration during requests. Use explicit mappings/converters for exceptions, skip server-owned properties on input, and avoid silently ignoring ambiguous matches. For PATCH, map only explicitly supplied, allowed fields and permit a present nullable field to clear. Blanket null-skipping is not the PATCH contract. Existing mapper settings must be inspected before reuse.

## Primary references

Consult documentation matching the target project's versions when verifying framework behavior.

- [Jakarta Validation inheritance and groups](https://jakarta.ee/specifications/bean-validation/3.0/jakarta-bean-validation-spec-3.0.html)
- [ModelMapper property mapping](https://modelmapper.org/user-manual/property-mapping/)
