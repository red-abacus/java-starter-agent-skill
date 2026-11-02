# Integration Templates

These are adoption recipes, not a starter application. Read the recipe for the configuration being added or changed; copy only the files it requires. The [handbook index](../docs/java-spring-guidelines.md) routes engineering policies.

| Configuration task | Recipe and artifacts |
| --- | --- |
| IntelliJ formatting, imports, Spotless, or Checkstyle | [Maven/quality recipe](maven/README.md), [plugin fragment](maven/quality-plugins.xml), root `.editorconfig`, and `config/checkstyle.xml` |
| YAML profiles, typed configuration, localization, OSIV, Actuator, or shutdown | Relevant [application configuration recipe](application/README.md) sections and selected YAML fragments in that directory |
| Liquibase XML master/includes and startup migration adoption | [Liquibase recipe](liquibase/README.md), [master](liquibase/db.changelog-master.xml), and the adapted example change |
| Image packaging, Helm chart layout, or GitHub Actions | Relevant [delivery recipe](delivery.md) section; concrete charts/workflows are generated for the target project |

Preserve the relative kit layout when copying shared guides and skills. Select actual products, integrations, environments, and resource values during target-project development, using decisions already supplied. Do not adopt unused schema or configuration merely because an example exists.
