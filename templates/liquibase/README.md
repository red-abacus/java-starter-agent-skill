# Liquibase Adoption Recipe

Read only the recipe sections needed for the configuration being adopted. [Template index](../README.md).

## Liquibase

Adapt [the master changelog](db.changelog-master.xml) and its illustrative change before copying them to `src/main/resources/db/changelog/`. Configure `spring.liquibase.change-log: classpath:db/changelog/db.changelog-master.xml`. Replace the example table with a real requirement; do not ship unused schema.

Run migrations at application startup by default. The application YAML fragment explicitly enables Liquibase and selects the XML master; merge these settings when adopting the database migration recipe. Keep the application unready until migration and initialization succeed, and account for migration time and Liquibase lock waiting in deployment startup/probe settings.

Follow the [schema evolution policy](../../docs/guidelines/entities-persistence.md#schema-evolution-and-rollout-compatibility): favor compatible additions and phase breaking transitions across releases where needed. Coordinate code/data migration before removing old structures, test intermediate states, and plan application rollback and database recovery separately.

Use explicit `include` elements for deterministic ordering, relative paths, and focused XML changesets. Use `sqlFile` or SQL blocks for justified database-specific operations, with reviewed rollback where feasible. Once applied, retain changeset identities, paths, and content; add a new changeset for corrections. Test against the selected production engine with Testcontainers and actual migrations. XML parsing in this kit does not prove SQL or rollback behavior.
