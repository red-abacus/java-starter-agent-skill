# Entities and Persistence

Read when: Changing entities, queries, database transactions, constraints, deletion, or Liquibase migrations.

Use only the sections relevant to the task. [Handbook index](../java-spring-guidelines.md).

## Sections

- [Entities](#entities)
- [Entity identifiers](#entity-identifiers)
- [Shared entity metadata and auditing](#shared-entity-metadata-and-auditing)
- [Entity equality and hashing](#entity-equality-and-hashing)
- [Relationship fetching](#relationship-fetching)
- [Open Session in View](#open-session-in-view)
- [Deletion policy](#deletion-policy)
- [Transactions](#transactions)
- [Persistence and migrations](#persistence-and-migrations)
- [Database naming](#database-naming)
- [Validation and database constraints](#validation-and-database-constraints)
- [Enum persistence](#enum-persistence)
- [Liquibase migrations](#liquibase-migrations)
- [Startup migration execution](#startup-migration-execution)
- [Schema evolution and rollout compatibility](#schema-evolution-and-rollout-compatibility)

## Entities

Entities contain fields, persistence annotations, and relationship helpers such as `addChild`/`removeChild`. Helpers maintain the owning/inverse sides consistently. Keep business operations in services. Choose cascade, orphan removal, fetching, and equality behavior using the configured JPA provider's guidance and the association's lifecycle; `CascadeType.ALL` and `orphanRemoval = true` are not universal defaults.

Keep relationship collections mutable under the [collection conventions](architecture-java-style.md#collections-mutability-and-ordering), managing changes through the relationship helpers.

### Entity identifiers

Use generated Long surrogate IDs by default. Prefer Long over primitive long for new entity ID fields so an unassigned ID can be null. Choose sequence versus identity generation after selecting the database.

Keep business identifiers, such as customer codes, separate and enforce their required uniqueness in the database. Use UUIDs or separate public identifiers when concrete requirements justify them. Preserve existing projects' identifier schemes during gradual adoption.

### Shared entity metadata and auditing

Use a small abstract BaseEntity annotated with MappedSuperclass for genuinely common persistence metadata: Long id, Instant createdAt, and Instant updatedAt. Its mappings apply to concrete entity tables; the base has no separate table. Keep it focused on fields and persistence/auditing metadata, with business rules in services.

Use Spring Data timestamp auditing with CreatedDate and LastModifiedDate. Enable and configure the auditing infrastructure and entity listener for the target project, and keep these timestamps server-managed.

Add Version metadata where optimistic locking is needed, at the appropriate entity root or mapped superclass. Add actor fields such as createdBy/updatedBy when required, and choose deletion metadata according to lifecycle needs. Allow exceptions for entities with different identifiers or metadata requirements.

### Entity equality and hashing

Use generated-ID equality where logical entity comparison is needed, retaining reference identity otherwise. Immutable business-key equality can be an explicit exception when the key is genuinely stable and unique.

The same instance is always equal to itself; different new instances with null IDs are unequal. Compare equal non-null IDs only for the appropriate persistent entity type, accounting for proxies. Keep hashCode stable across ID assignment and persistence. Exclude relationships, mutable business fields, and audit timestamps from equality and hashing.

Keep the implementation explicit and tested. Centralize it in BaseEntity only when valid for the relevant entity hierarchies; avoid blanket all-field Lombok equality on entities. Verify transient instances, ID assignment, detached/proxy comparisons, and set membership across persistence against the configured provider.

### Relationship fetching

Use LAZY relationship mappings by default, configuring to-one associations explicitly and verifying the provider's behavior for the mapping. Fetch the relationships required by each use case deliberately before mapping results to DTOs.

Prefer EntityGraph alongside derived repository methods where it fits. Use justified fetch joins or DTO projections for specialized reads. Complete persistence-dependent DTO mapping inside the service transaction.

Verify query behavior and pagination with real persistence tests. Accessing unfetched relationships while processing a list can cause an extra query per row. Collection fetch joins require particular care with pagination because limits may be applied in memory instead of in the database; choose a fetch/query plan that preserves the intended database pagination.

### Open Session in View

Disable Open Session in View (OSIV), called Open EntityManager in View in Spring's JPA support, by default for new JPA REST APIs: set `spring.jpa.open-in-view: false` in shared configuration.

Return fully constructed response DTOs from services. Fetch required state and complete persistence-dependent mapping inside the service transaction; controllers and JSON serialization must not depend on lazy loading afterward.

Verify HTTP response construction with OSIV disabled and without a test-managed transaction masking missing fetches. For existing applications, inspect dependencies on request-scoped lazy loading and migrate affected fetch plans and mapping before changing the setting, following gradual adoption.

### Deletion policy

Prefer physical deletion where business rules allow it. Introduce soft deletion explicitly for domain models whose requirements justify retaining removed records.

Whenever deletion is discussed for a task, ask the user which deletion type is needed before implementing deletion behavior. An explicit choice already supplied for that task answers this question; the general physical-deletion preference does not replace this clarification.

Services enforce deletion permissions, business rules, and dependency checks. Choose cascades and relationship handling according to the agreed lifecycle. For soft deletion, define ordinary and privileged visibility, filtering and totals, uniqueness, restoration if supported, and relationship behavior. Add deletion metadata only to entities that need it, keeping the shared BaseEntity focused on common metadata.

## Transactions

Declare transactions on individual service methods: `@Transactional(readOnly = true)` for database reads and `@Transactional` for writes. Place the boundary around database work that must succeed or fail together. Pure computations and external-only operations do not automatically need a transaction.

Account for propagation: under ordinary REQUIRED propagation, an inner method joins the existing transaction rather than establishing its own read-only/write settings. A read-only flag is an optimization hint, not an authorization rule or universal write guard. Calls within the same object do not reapply proxy-based transaction annotations. Keep transaction boundaries clear and test rollback where behavior depends on it.

Apply the [exception and rollback conventions](security-errors.md#java-exception-conventions), deliberately defining rollback behavior for checked exceptions that cross a transaction boundary.

## Persistence and migrations

Repositories extend suitable Spring Data interfaces. Prefer readable derived methods, then Specifications for dynamic/composable filtering. Keep predicate construction in dedicated specification classes. The service chooses criteria for the use case, and the repository executes them. Use custom repository fragments or handwritten JPQL/native SQL as justified exceptions based on clarity, required capabilities, or demonstrated performance needs. Do not move persistence into services merely to avoid `@Query`.

Apply data filtering and pagination in the database where appropriate, rather than fetching large sets and reproducing the query in Java. Test meaningful filter combinations, ordering, pagination, and applicable scope restrictions. Custom queries need the same verification as derived ones.

### Database naming

Use plural table names and lowercase snake_case database identifiers. Keep Java class names singular and Java fields camelCase.

| Object | Convention | Example |
| --- | --- | --- |
| Table | Plural noun | `customers`, `customer_addresses` |
| Column | Lowercase snake_case | `first_name`, `created_at` |
| Primary-key column | `id` | `id` |
| Foreign-key column | Referenced model/relationship plus `_id` | `customer_id` |
| Primary-key constraint | `pk_<table>` | `pk_customers` |
| Unique constraint | `uk_<table>_<columns_or_purpose>` | `uk_customers_code` |
| Foreign-key constraint | `fk_<table>_<relationship>` | `fk_orders_customer` |
| Check constraint | `ck_<table>_<rule>` | `ck_orders_quantity` |
| Index | `idx_<table>_<columns_or_purpose>` | `idx_customers_created_at` |

Name constraints and indexes explicitly in Liquibase. Use meaningful qualifiers to distinguish multiple relationships, composite keys, or indexes on the same table, and respect the selected database's identifier limits with consistent, unambiguous shortening when needed.

Align the configured ORM naming strategy with Liquibase. Let it handle ordinary camelCase-to-snake_case column mappings; declare explicit table names, join-column names, and exceptions. Preserve existing schema conventions during gradual adoption, and keep applied migration identities and content stable.

### Validation and database constraints

Use layered validation: DTOs reject invalid input early, services enforce business and contextual rules, and the database protects persisted integrity. Enforce required persisted values with Liquibase-managed NOT NULL constraints as well as the appropriate request DTO null checks. Server-managed fields remain the server's responsibility rather than becoming required request fields.

Define unique, foreign-key, and appropriate check constraints through Liquibase where required by the model. Keep entity metadata aligned with the migrated schema. DTO validation and entity mapping annotations do not replace database constraints.

Align decimal column precision/scale with the agreed [money and decimal conventions](architecture-java-style.md#money-and-decimal-values), request validation, and service calculations.

Service pre-checks may provide helpful feedback, but uniqueness must also be enforced in the database because concurrent requests can pass the same pre-check. Explicitly translate recognized business conflicts to stable domain codes and 409 ProblemDetail responses, including failures surfaced at flush or transaction commit. Use reliable constraint/provider metadata; return safe details and reserve conflict mappings for known conditions rather than every integrity failure.

Verify early rejection with controller tests asserting validation responses and no service invocation. Verify actual constraints through persistence tests that bypass request DTO validation, using the selected database and real Liquibase migrations.

### Enum persistence

Use string-based enum persistence by default, declaring `@Enumerated(EnumType.STRING)` explicitly for ordinary fixed enums. Treat stored names as stable values. Reordering constants preserves their meaning; renaming or removing a persisted value requires a deliberate migration or an explicit mapping that preserves compatibility.

Use a dedicated `AttributeConverter` when independent persistence codes or legacy compatibility justify it. Configure conversion on the attribute instead of combining it with `@Enumerated`, and test the supported codes and unknown-value behavior.

Define column types, lengths, and applicable constraints through Liquibase, and verify that the ORM mapping matches the selected database and dialect. Exercise persistence round trips and relevant migrations against the actual database engine. Govern stored values and public JSON values through their respective contracts; a persistence annotation does not define JSON serialization.

### Liquibase migrations

Use Liquibase XML by default, a root changelog with explicit includes, and focused migration files. Several related small changesets may share a file. Execution follows declared include order, not changeset IDs. Use SQL files for specialized operations where justified. Keep applied migration identity and content stable; add corrective migrations instead of editing history. Renaming/moving files can change identity unless deliberately managed. Supply rollback where practical and document irreversible effects.

Use actual Liquibase migrations in Testcontainers integration tests. Reconcile entities with the migrated schema; Hibernate's schema auto-update must not become a second independent production migration mechanism. Use startup migrations by default and select database credentials and privileges for the target project.

### Startup migration execution

Run Liquibase during Spring Boot application startup, using the XML master changelog shipped with the selected application release. Keep Liquibase enabled in the application configuration. Treat migration failure as startup failure and keep the application unready for business traffic until migration and initialization complete successfully.

Use Liquibase's changelog locking to coordinate concurrent startup against the same database. Account for migration execution and lock waiting when configuring startup/probe timing, and verify effective startup and failure behavior with the selected database and deployment configuration. Preserve an existing project's required migration execution strategy during gradual adoption.

### Schema evolution and rollout compatibility

Prefer additive schema changes compatible with the application versions present during a normal rolling release. Plan renames, removals, type changes, and tighter constraints around existing data and running consumers.

Use phased migrations when existing structures must be replaced:

| Phase | Responsibility |
| --- | --- |
| Expand | Add the new structure while preserving what existing consumers need. |
| Migrate | Transition code and existing data, explicitly coordinating reads, writes, and backfill ordering. |
| Contract | Remove the old structure after consumers have migrated and rollback requirements permit removal. |

Each schema phase can still run through startup Liquibase migrations across the appropriate application releases. Keep routine compatible additions proportionate; use the phased approach where needed for a breaking transition.

Verify intermediate schema/data states against the selected database, including relevant migration and rollout behavior. Use an explicitly planned maintenance window when a breaking change cannot reasonably be phased. Treat application rollback and database recovery as separate concerns, documenting the recovery approach and irreversible effects where relevant.

## Primary references

Consult documentation matching the target project's versions when verifying framework behavior.

- [Jakarta Persistence optimistic locking](https://jakarta.ee/specifications/persistence/3.2/jakarta-persistence-spec-3.2.html#_entity_versions_and_optimistic_locking)
- [Spring Data pagination and query methods](https://docs.spring.io/spring-data/jpa/reference/repositories/query-methods-details.html)
- [Spring Data web pagination and sorting](https://docs.spring.io/spring-data/commons/reference/repositories/core-extensions.html)
- [Hibernate associations](https://docs.hibernate.org/orm/7.0/userguide/html_single/)
- [Hibernate entity equality](https://docs.hibernate.org/orm/7.0/userguide/html_single/#mapping-model-pojo-equalshashcode)
- [Hibernate equality and proxies](https://docs.hibernate.org/orm/7.0/introduction/html_single/#equals-and-hash)
- [Hibernate association fetching](https://docs.hibernate.org/orm/7.0/introduction/html_single/#proxies-and-lazy-fetching)
- [Hibernate enum mapping](https://docs.hibernate.org/orm/7.1/userguide/html_single/#basic-enums)
- [Spring Data entity graphs](https://docs.spring.io/spring-data/jpa/reference/jpa/query-methods.html#jpa.entity-graph)
- [Spring Boot Open EntityManager in View](https://docs.spring.io/spring-boot/reference/data/sql.html#data.sql.jpa-and-spring-data.open-entitymanager-in-view)
- [Spring Data entity-state detection](https://docs.spring.io/spring-data/jpa/reference/jpa/entity-persistence.html)
- [Jakarta Persistence mapped superclasses](https://jakarta.ee/specifications/persistence/3.2/jakarta-persistence-spec-3.2.html#_mapped_superclasses)
- [Spring Data auditing](https://docs.spring.io/spring-data/jpa/reference/auditing.html)
- [Spring transaction annotations](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html)
- [Spring transaction propagation](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/tx-propagation.html)
- [Spring Data Specifications](https://docs.spring.io/spring-data/jpa/reference/jpa/specifications.html)
- [SQL constraints (PostgreSQL example)](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [Concurrent uniqueness enforcement (PostgreSQL example)](https://www.postgresql.org/docs/current/index-unique-checks.html)
- [Liquibase include ordering](https://docs.liquibase.com/community/reference-guide-5-0-4/changelog-attributes/include)
- [Spring Boot database initialization](https://docs.spring.io/spring-boot/how-to/data-initialization.html)
- [Liquibase changelog locking](https://docs.liquibase.com/concepts/tracking-tables/databasechangeloglock-table.html)
- [Liquibase expand-contract schema evolution](https://www.liquibase.com/technical-glossary/expand-contract-pattern)
