# REST API Conventions

Read when: Changing an HTTP endpoint or its public contract; select the affected contract sections.

Use only the sections relevant to the task. [Handbook index](../java-spring-guidelines.md).

## Sections

- [REST API conventions](#rest-api-conventions)
- [Resource design](#resource-design)
- [Update methods](#update-methods)
- [Successful responses](#successful-responses)
- [Success body structure](#success-body-structure)
- [Pagination model](#pagination-model)
- [Pagination responses](#pagination-responses)
- [Sorting](#sorting)
- [Filtering](#filtering)
- [JSON names and enums](#json-names-and-enums)
- [Dates, times, and zones](#dates-times-and-zones)
- [Nulls and empty response values](#nulls-and-empty-response-values)
- [JSON request binding](#json-request-binding)
- [API versioning](#api-versioning)
- [Retries and idempotency](#retries-and-idempotency)
- [Concurrent edits](#concurrent-edits)
- [OpenAPI and contract checks](#openapi-and-contract-checks)

## REST API conventions

Resource-path examples below omit the `/api/v1` base prefix unless shown explicitly.

### Resource design

Use a resource-first API with focused domain actions when ordinary resource operations do not express the business workflow clearly. Design public resources around business concepts; internal Java packages remain organized by responsibility.

Use plural nouns for collections, lowercase paths, and hyphens between words, such as `/customers` and `/customer-notes`. Put resource identifiers in paths, such as `/customers/{customerId}`, and filtering criteria in query parameters. Keep relationship paths shallow and meaningful, such as `/customers/{customerId}/orders`, rather than exposing a chain of database associations.

For a business action, a path such as `POST /orders/{orderId}/cancel` is appropriate when a focused command expresses the workflow. Model cancellations as resources, such as `POST /orders/{orderId}/cancellations`, when they need their own identity, information, or lifecycle. Prefer ordinary resource operations where they fit; avoid creating a separate action endpoint for every CRUD operation. GET retrieves data and must not request a state change.

### Update methods

Use PATCH for routine partial updates, preserving the omitted/null/value contract described in the [DTO validation guide](dto-validation-mapping.md#dtos-and-validation). Expose PUT only for explicit full-replacement use cases; do not generate a PUT endpoint automatically for every editable resource.

A PUT contract defines the complete client-editable representation and the meaning of omitted fields, while preserving server-owned identifiers and audit information. Do not implement PUT and PATCH as interchangeable partial updates. Existing application contracts remain subject to the gradual-adoption policy.

### Successful responses

Return created/updated resource DTOs by default, so clients receive the resulting server state. Use these success responses:

| Operation | Default response |
| --- | --- |
| Retrieve a resource or collection | 200 with data; an empty collection remains 200. |
| Create a resource | 201 with a Location header and the created resource DTO. |
| PATCH or PUT an existing resource | 200 with the updated resource DTO. |
| Complete a deletion | 204 with no body. |
| Complete a domain action | 200 with a meaningful result, or 204 when no useful result needs returning. |
| Accept asynchronous work | 202 with operation/status information and a way to track progress. |

A 204 response has no body. A 202 response indicates accepted work that has not finished, rather than completed success. When a PUT endpoint explicitly supports creation, successful creation returns 201; this does not make creation through PUT a default capability. Preserve existing application contracts during gradual adoption.

### Success body structure

Return response DTOs directly for individual resources, including creation and updates. Use an array of response DTOs for small, intentionally unpaginated collections. When pagination or other collection metadata is needed, return a dedicated collection response DTO containing the items and relevant metadata. Keep that public contract explicit rather than exposing a framework pagination implementation's JSON shape.

Do not add a universal success envelope by default. Errors retain the adopted ProblemDetail structure, and 204 responses remain empty. Preserve existing response contracts during gradual adoption.

### Pagination model

Use page-number pagination with `page` and `size` query parameters by default. Use cursor/keyset pagination for explicitly justified use cases, such as large collections consumed sequentially or feeds. Treat cursor pagination as an explicit endpoint contract rather than silently changing an established page-based API. Choose ordering and indexes deliberately for the selected approach.

Use zero-based page numbers. Omitted parameters default to `page=0` and `size=20`; the default maximum size is 100. Default and maximum sizes are configurable project defaults, with documented endpoint exceptions justified by payload size and query cost. Require `page >= 0` and `1 <= size <= configured maximum`.

Reject explicitly supplied blank, nonnumeric, negative, or oversized parameters with 400 and the established validation ProblemDetail. Validate the original request values before framework normalization can mask invalid input; merely setting a Pageable resolver maximum does not implement strict rejection. A valid page beyond the available results returns 200 with an empty collection. Apply defaults only to omitted parameters.

### Pagination responses

For ordinary page-based collections, return a dedicated DTO with top-level `items` and a nested `page` object containing `number`, `size`, `totalElements`, and `totalPages`. Include totals by default. For example, a matching result set containing one customer is represented as:

```json
{
  "items": [
    {"id": 123, "name": "Alice"}
  ],
  "page": {
    "number": 0,
    "size": 20,
    "totalElements": 1,
    "totalPages": 1
  }
}
```

`number` is zero-based; `size` is the effective requested page capacity, including the default when omitted, rather than the number of returned items. Totals describe the same filtered, authorized result set as the items. Account for count-query cost when implementing the endpoint.

Use explicitly documented slice/cursor response contracts when totals are unnecessary or counting is too expensive. Define their navigation metadata and omit unavailable totals rather than fabricating values or silently dropping fields from an established page response. Map repository pagination results into the public response DTO.

### Sorting

Support allowlisted multi-field sorting using repeated `sort` query parameters, such as `sort=name,asc&sort=createdAt,desc`. Preserve the supplied field order as sorting priority. Accept `asc` and `desc`, defaulting to `asc` when direction is omitted.

Each endpoint documents its supported public sort fields, their mapping to persistence properties, and a meaningful default order when sorting is omitted. Reject unsupported fields, invalid directions, and malformed expressions with 400 and the established validation ProblemDetail. Validate requested properties explicitly; framework binding alone does not establish the allowlist.

Ensure a unique final order, adding an identifier or other unique tie-breaker where needed. For example, `name,asc` can become `name,asc` followed by `id,asc` unless the requested ordering is already unique. Apply sorting in the database before pagination. Unique ordering resolves ties for unchanged data; it does not freeze results across concurrent changes.

### Filtering

Use explicit, typed query parameters as the filtering default, such as `status=ACTIVE&country=RO&nameContains=Ann`. Each endpoint documents its supported filters and matching rules. Use exact matching by default and explicit parameter names for other operations, such as `nameContains`. Combine different filters with AND; where a filter supports multiple values, document OR semantics within that filter.

Group related criteria in a typed filter DTO. Validate input at the HTTP boundary and contextual rules in services. Reject unsupported filters and invalid values with 400 and the established validation ProblemDetail. Apply filtering and authorization scope in the database before sorting/pagination, using the same criteria for totals.

Keep derived repository methods for simple, fixed criteria and use dedicated Specifications for dynamic combinations. Introduce a filter language or structured search endpoint only when requirements justify a richer search contract, with explicit syntax, validation, and semantics.

### JSON names and enums

Use camelCase JSON property names, matching Java DTO naming. Use the same published field names in requests and responses where they represent the same concept.

Represent enums as stable UPPER_SNAKE_CASE strings, initially matching Java enum constant names. Treat these strings as public API values and preserve them when internal Java names are refactored, using explicit serialization mappings where needed. Accept the documented enum spelling exactly and reject unknown values and numeric ordinals with 400. Keep human-readable or localized labels separate from enum codes.

### Dates, times, and zones

Represent points in time as RFC 3339 timestamp strings and use Java Instant by default. Normalize timestamp responses to UTC with a `Z` suffix, such as `2026-10-31T12:30:00Z`. Timestamp inputs must provide UTC or an explicit offset so they resolve to an instant.

Use LocalDate for calendar dates, such as birth dates represented as `1990-05-20`. Keep these as dates without time-zone conversion. Where the business requires local schedules or regional time rules, define explicit zone handling rather than inferring a zone from server settings. A numeric UTC offset alone does not capture regional daylight-saving rules.

Return the established validation ProblemDetail for invalid or ambiguous temporal input. Preserve an existing application's published formats during gradual adoption.

### Nulls and empty response values

Include declared nullable response fields as explicit nulls by default. Return empty arrays for known-empty collections and empty objects for known-empty maps. Keep null, empty strings, and empty collections distinct.

Make omission an explicit contract choice for projections or conditional fields. Separate slice/cursor DTOs can omit totals because those fields are outside their contract. Configure and verify serialization inclusion rules deliberately; empty containers must remain present where the response contract requires them.

These rules concern response serialization. Preserve the existing omitted/null/value distinction and presence tracking for PATCH requests.

### JSON request binding

Use strict JSON request binding by default, with explicit, documented compatibility exceptions. Reject unknown JSON properties with 400 and the established ProblemDetail format. Require the declared JSON value type: numeric fields receive JSON numbers and boolean fields receive true/false. Reject stringified numbers, string/numeric boolean substitutes, and fractional values for integer fields rather than silently coercing or truncating them.

Missing required fields and forbidden nulls follow the DTO's validation rules. Preserve the adopted enum spelling and PATCH presence contracts. Query/path parameters arrive as text and are parsed into their declared types; JSON token-type rules do not prohibit that normal parameter conversion.

Configure and test the effective HTTP binding rules explicitly; unknown-property rejection alone does not disable type coercion. Scope API request binding and compatibility exceptions deliberately, preserving established application contracts during gradual adoption.

### API versioning

Use `/api/v1`-style path versioning for new APIs. Introduce a new major version for breaking contract changes, such as renaming/removing fields, changing field types, or introducing required inputs. Keep compatible changes within the existing version after assessing their effect on supported clients.

Assess compatibility across validation rules, pagination behavior, status codes, and business semantics as well as JSON shape. An optional response field can be compatible when clients tolerate additional fields; assess that tolerance rather than assuming it. Plan migration and deprecation before removing an older version, with the transition period chosen per project. Preserve an existing project's versioning strategy during ordinary adoption.

### Retries and idempotency

Idempotency keys are not required in the current defaults. Honor HTTP method semantics and domain uniqueness rules. Revisit an idempotency-key requirement only as a separate decision for a concrete use case; ordinary API generation must not introduce that requirement automatically.

### Concurrent edits

Use ETag/If-Match optimistic concurrency for selected resources whose edit workflows need stale-revision detection. Return a strong ETag identifying the selected resource representation. Protected modifications require the client's earlier revision through If-Match; document missing-precondition behavior explicitly. Return 412 Precondition Failed with the established ProblemDetail when that revision is stale.

Keep the comparison and database write atomic. JPA Version metadata can support the database check where applicable, but loading the latest entity alone does not reveal that the client edited an older representation. Derive a strong ETag from an entity version only when that version captures all relevant representation changes; account for related data and representation variants. Verify stale-client handling and write races at the actual persistence boundary.

### OpenAPI and contract checks

Use code-first OpenAPI with springdoc-openapi, selecting a version compatible with the target project. Generate the specification from controllers, DTOs, and annotations. Let DTO metadata provide basic schemas and add annotations where descriptions or generated schemas need clarification.

Define stable operationIds that are unique within each API description, and organize documentation by API major version. Document actual validation, null/PATCH behavior, pagination, filtering, security requirements, response codes, and relevant headers such as ETag/If-Match.

In target-application CI, generate and validate the specification and run compatibility checks against the appropriate supported-contract baseline. Flag potentially breaking changes for review. Keep HTTP behavior tests alongside specification checks, especially for binding, serialization, and error responses; schema checks alone do not verify those behaviors.

## Primary references

Consult documentation matching the target project's versions when verifying framework behavior.

- [Resource-oriented API design](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design)
- [API versioning strategies](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design#implement-versioning)
- [springdoc-openapi](https://springdoc.org/)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [Custom domain methods](https://google.aip.dev/136)
- [HTTP method semantics](https://www.rfc-editor.org/rfc/rfc9110.html#name-method-definitions)
- [PATCH semantics](https://www.rfc-editor.org/rfc/rfc5789.html)
- [HTTP If-Match preconditions](https://www.rfc-editor.org/rfc/rfc9110.html#name-if-match)
- [Jackson external property names](https://github.com/FasterXML/jackson-annotations/wiki/Jackson-Annotations)
- [Jackson enum serialization](https://github.com/FasterXML/jackson-databind/wiki/Serialization-features#datatype-specific-serialization)
- [Jackson deserialization controls](https://github.com/FasterXML/jackson-databind/wiki/Deserialization-Features)
- [Jackson mapper and coercion controls](https://github.com/FasterXML/jackson-databind/wiki/Mapper-Features)
- [RFC 3339 timestamps](https://www.rfc-editor.org/rfc/rfc3339.html)
- [Java Instant](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/time/Instant.html)
- [Java LocalDate](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/time/LocalDate.html)
- [Java offset and zone distinctions](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/time/OffsetDateTime.html)
