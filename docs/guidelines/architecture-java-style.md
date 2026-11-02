# Architecture and Java Style

Read when: Changing packages, layer responsibilities, service contracts, Java style, collections, monetary/decimal values, documentation, or caching requirements.

Use only the sections relevant to the task. [Handbook index](../java-spring-guidelines.md).

## Sections

- [Project structure](#project-structure)
- [Responsibilities](#responsibilities)
- [Services](#services)
- [Controller-facing contracts](#controller-facing-contracts)
- [Service collaboration](#service-collaboration)
- [Caching](#caching)
- [Java style](#java-style)
- [Collections, mutability, and ordering](#collections-mutability-and-ordering)
- [Money and decimal values](#money-and-decimal-values)
- [Lombok](#lombok)
- [Documentation and comments](#documentation-and-comments)

## Project structure

Use standard Maven directories: `src/main/java`, `src/main/resources`, `src/test/java`, and `src/test/resources`. Keep documentation under `docs/` and generated artifacts outside source control.

Organize packages by technical responsibility. A new project's example layout is:

```text
com.example.application
├── controllers
├── services
├── clients
├── schedulers
├── entities
├── repositories
├── dto
├── mappers
├── specifications
├── exceptions
├── handlers
├── config
├── security
├── validation
└── utils
```

Create a package when there is code for it. Keep ordinary packages flat. When a responsibility package becomes substantially larger, introduce functional subpackages within it, such as `services.notifications` or `controllers.customers`. Exact singular/plural spelling above is the kit's default; preserve established spelling when adopting an existing project. Java package segments are lowercase identifiers, so a conceptual “user-management” group might become `usermanagement`.

## Responsibilities

| Component | Owns |
| --- | --- |
| Controller | Endpoint definitions, OpenAPI, query/path validation, triggering DTO validation, direct service delegation, and HTTP response construction. |
| Service | Business logic, contextual validation, orchestration, data preparation, business transformations, and repository interactions. |
| Client | Provider-focused HTTP communication and provider request/response handling, called by services. |
| Scheduler | Scheduling triggers and delegation to service-owned business operations. |
| Mapper | Structural DTO/entity conversion and mapping configuration. |
| Repository | Database access and query execution. |
| Entity | Persisted state, mapping metadata, and relationship helpers. |
| Access policy | Resource-specific authorization checks invoked by services. |
| Exception handler | HTTP exception translation and unexpected propagated failure logging. |

Keep business logic out of controllers, mappers, and repositories. Services are organized around domain models and may collaborate with other services. Respect existing module boundaries; this kit does not impose an unagreed rule that every service may touch only one repository.

Use concrete `@Service` classes. Add an interface for multiple implementations or a clear abstraction, such as a boundary around an external provider. Do not generate a matching interface/implementation pair for every service.

## Services

### Controller-facing contracts

Use DTO-based controller-facing service contracts by default. Group related request data in request DTOs, pass identifiers as explicit arguments, and return response DTOs representing the resulting server state. Apply the existing required/optional result and missing-resource conventions.

Services call dedicated mappers; controllers construct HTTP responses and headers. Pass the expected revision explicitly to services for protected updates so the check and write can remain atomic. Internal service work may use entities or domain values as appropriate.

Introduce separate command/result models or an API-facing service facade only when reuse or complexity justifies them. Focused internal results may carry necessary metadata while preserving the public resource DTO response shape.

Apply the [collection conventions](#collections-mutability-and-ordering) to service results, including their mutability and required ordering.

### Service collaboration

Use direct, synchronous service calls for simple flows. Extract a dedicated workflow service when coordination becomes complex, reusable, or has a distinct business purpose. Domain services retain their business rules; workflow services coordinate the steps.

Reuse another domain's business operations through its service and keep dependencies acyclic, extracting shared coordination when needed. Preserve capability and resource-access checks during collaboration. Retain justified repository access for query composition under the existing repository policy.

Define the transaction on the coordinating entry method when database operations must succeed together. Participating service calls can join the existing transaction through REQUIRED propagation, subject to the configured transaction manager and existing transaction rules.

### Caching

Do not implement application caching by default. Introduce it only when specifically required by the user or by an agreed workflow.

Define all caching requirements with the user during implementation of the affected workflow. Establish the purpose, cached data, provider, key scope, acceptable staleness, expiration, size limits, invalidation, consistency, failure behavior, authorization, and verification requirements as applicable. Reuse explicit workflow decisions already supplied. This kit does not select a default cache provider or add caching dependencies, annotations, configuration, or infrastructure to starter applications.

## Java style

- Declare explicit local types instead of `var`. Use standard class, method, field, constant, and package naming conventions.
- Prefer guard clauses and early returns for rejection and no-op cases. Keep `if/else` where both branches represent meaningful alternatives; extract named helpers when nesting obscures the flow.
- Use streams for straightforward transformations, filtering, grouping, and reductions. Use loops for multi-step work, mutations, complex branching, or recovery. Keep lambdas short, avoid side effects inside `map`/`filter`/`peek`, and use sequential streams by default.
- Return `Optional<T>` for expected single-result absence, return `T` or throw a meaningful exception for required results, and return empty collections for no matches. An Optional-returning method must never return null. Keep Optional primarily in return contracts, rather than automatically using it for DTO/entity fields.
- Follow the [exception conventions](security-errors.md#java-exception-conventions): specific unchecked exceptions for failed operations, with explicit result models only when workflow outcomes justify them.
- Use four spaces, same-line opening braces, braces even for one-statement control blocks, and a 120-column wrapping target. Use UTF-8, LF, final newlines, and no trailing whitespace.
- Use explicit imports, including in tests. Allow explicit static imports that aid readability. Group JDK imports (`java`/`javax`), Jakarta, third-party, project imports, then static imports; sort within groups.

IntelliJ's built-in formatter reads `.editorconfig`. Spotless performs import/whitespace cleanup; Checkstyle enforces the agreed subset of structural rules. The build deliberately does not install a competing full Java formatter or promise exact IntelliJ wrapping. Update the project import prefix consistently in all quality configurations. A wrapping target is not a blanket ban on an unbreakable URL or string literal.

## Collections, mutability, and ordering

Declare variables and contracts using collection interfaces such as `List`, `Set`, and `Map`. Use `List` for sequences, `Set` when uniqueness matters, and `Map` for keyed lookup. Choose implementations according to the required behavior.

Use mutable collections when assembling or changing data. Prefer unmodifiable service-result collections when callers do not need to modify their contents, using methods such as `List.copyOf`. Unmodifiable collections protect their structure; mutable DTOs or other elements can still change. Factory null restrictions remain part of the contract: `List.copyOf` rejects null elements.

Keep JPA relationship collections mutable and manage them through the established relationship helpers, following the configured provider's guidance.

Define ordering explicitly when it affects behavior or API responses. Select ordered implementations where needed, such as `LinkedHashMap` or `LinkedHashSet` for insertion order, and apply the established database sorting rules for query results. Do not infer a stable order from an unordered collection.

## Money and decimal values

Use `BigDecimal` by default for monetary amounts, prices, rates, and other exact decimal values. Integer minor units are appropriate when a workflow or provider contract requires them. Use `double`/`float` for measurements and calculations where approximation is acceptable.

Construct decimal constants from strings, such as `new BigDecimal("19.95")`, avoiding binary floating-point construction for exact values. Define currency, precision, scale, and rounding rules during implementation of the affected workflow. Do not assume every amount has two decimal places or select a universal rounding mode. Make rounding explicit where calculations require it.

Align request DTO validation, service calculations, entity mappings, and Liquibase-managed column precision/scale with the agreed rules. Use `compareTo` for numeric comparisons when scale is irrelevant; `equals` distinguishes values such as `2.0` and `2.00`.

## Lombok

Use Lombok `@Getter` and `@Setter` for DTO/entity boilerplate, `@RequiredArgsConstructor` with final collaborators for injection, and `@Slf4j` when logging is needed. Use builders selectively and add DTO constructors when useful. Check inheritance support before choosing `@Builder`; inherited state must not disappear. Do not substitute `@Data` for the selected annotations automatically.

## Documentation and comments

Do not add Javadoc by default. Use it only when explicitly requested or required by an existing project's conventions or tooling. Respect required existing documentation when changing the affected code.

Write comments and technical documentation in English. Use inline comments to explain business rationale, unusual constraints, and justified workarounds; avoid comments that merely restate obvious code.

Keep setup, configuration, and build/test/run commands in the README. Maintain HTTP contracts through the agreed [code-first OpenAPI approach](rest-api.md#openapi-and-contract-checks). Update affected documentation alongside code changes.

Record consequential architectural choices in short files under `docs/decisions/`, explaining context, the decision, and consequences. Routine implementation choices do not require decision records.

## Primary references

Consult documentation matching the target project's versions when verifying framework behavior.

- [Java BigDecimal arithmetic, construction, and equality](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/math/BigDecimal.html)
- [Java List contracts and unmodifiable collections](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/List.html)
- [Java Map contracts and ordering](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Map.html)
