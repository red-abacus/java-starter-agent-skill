# Build, Configuration, and Logging

Read when: Changing Java/Boot versions, Maven setup, dependency-update automation, security scanning, configuration binding, or logging.

Use only the sections relevant to the task. [Handbook index](../java-spring-guidelines.md).

## Sections

- [Build and version policy](#build-and-version-policy)
- [Dependency-update automation](#dependency-update-automation)
- [Portable security scanning](#portable-security-scanning)
- [Configuration and logging](#configuration-and-logging)

## Build and version policy

For new projects, choose Maven, a currently supported Java LTS compatible with the latest stable supported Spring Boot release, and required dependencies/infrastructure. Verify current primary documentation at creation time. Pin the chosen Java baseline, Boot patch release, additional dependencies, and build plugins. Align Java across IDE, Maven, CI, and runtime, and create Maven Wrapper.

Use Boot's starter parent by default and its managed dependency versions; use its BOM when another parent is required. Deliberately review overrides rather than independently upgrading every Spring/Hibernate dependency. Preview Java features and pre-release dependencies require a deliberate project decision.

For AI capabilities, follow the [Spring AI framework preference](spring-ai.md#framework-preference) and [dependency-alignment policy](spring-ai-implementation.md#dependency-and-version-alignment).

The verification fixture records a dated compatible stack. It is not a business application or a reason to upgrade an existing repository. A new project should document its actual build/test/run commands, configuration, integrations, and selected versions.

Dependency-update automation remains [opt-in](#dependency-update-automation).

## Dependency-update automation

Tools such as Dependabot and Renovate are optional, not the default approach. Do not configure a bot or a routine update-PR schedule in starter applications without an explicit project decision to adopt it. Select the tool, cadence, grouping, and review policy during that work, respecting existing project requirements and Spring Boot dependency management.

## Portable security scanning

Use portable security scanning as the default approach, with repository-owned configuration and commands that run locally and in CI. Prefer OWASP Dependency-Check's Maven plugin for Java dependency vulnerabilities and Trivy CLI for secrets in source/configuration files and vulnerabilities in built container images. Pin compatible scanner versions per project. GitHub Actions can execute these commands; GitHub's built-in security products and paid security features are not prerequisites.

Agree scan scope, execution points, blocking thresholds, and documented exceptions with the user during project implementation. Distinguish repository-file secret scans from Git-history coverage, and scan the actual image intended for release when image scanning applies. Do not silently select a universal severity gate or treat an unavailable scan as a clean result.

Plan advisory-data updates, caching, credentials, and failure handling for the selected tools; Dependency-Check uses NVD data. Security scanning does not enable the optional dependency-update bots.

## Configuration and logging

Use YAML for application configuration: non-sensitive shared defaults, small profile overrides, and external runtime configuration. Use environment variables or mounted files for non-sensitive settings; follow the [secret delivery policy](delivery-gke.md#secret-storage-and-delivery) for credentials. Create only profiles with meaningful differences. Select active profiles externally and document required settings. Avoid copying the entire base file into each profile or committing credentials.

Bind related settings to typed `@ConfigurationProperties` classes under `config`, register them through scanning or explicit configuration, and validate required settings at startup with `@Validated`. Prefer types such as Duration/URI and constructor-injected properties objects. Reserve `@Value` for isolated settings and `Environment` for genuinely dynamic property lookup. Message translation bundles remain `.properties` resources; the YAML preference concerns application configuration.

Services log meaningful business activity and problems they recover from. Use DEBUG for useful diagnostics, INFO for significant business events, and WARN for meaningful degradation/recovery. Logging is not proof that a transaction committed; describe outcomes accurately.

The centralized HTTP handler logs unexpected propagated failures once at ERROR with the exception, stable code, and useful context. Expected validation/missing-resource/conflict cases normally have no stack trace and may need no extra application log. Other entry points, including scheduled jobs and consumers, own their logging boundary. Preserve causes when wrapping errors; avoid logging merely to rethrow.

Use parameterized SLF4J messages and a trailing exception argument when a stack trace is needed. Keep logs in English and include the same trace/correlation identifier as the error response. Select useful metadata instead of dumping entire DTOs, entities, credentials, or tokens. Avoid automatic entry/exit logging on every method. Tracing/context propagation and production log transport are configured for the target project, not silently assumed by adding `@Slf4j`.

## Primary references

Consult documentation matching the target project's versions when verifying framework behavior.

- [Spring Boot configuration](https://docs.spring.io/spring-boot/reference/features/external-config.html)
- [IntelliJ EditorConfig](https://www.jetbrains.com/help/idea/editorconfig.html)
- [Spotless Maven](https://github.com/diffplug/spotless/blob/main/plugin-maven/README.md)
- [Checkstyle ImportOrder](https://checkstyle.org/checks/imports/importorder.html)
- [SLF4J logging](https://www.slf4j.org/faq.html)
- [Spring Boot requirements](https://docs.spring.io/spring-boot/system-requirements.html)
- [OWASP Dependency-Check Maven usage and advisory data](https://dependency-check.github.io/DependencyCheck/dependency-check-maven/)
- [Trivy secret scanning](https://trivy.dev/docs/latest/scanner/secret/)
- [Trivy container-image scanning](https://trivy.dev/docs/latest/target/container_image/)
- [Trivy Java coverage](https://trivy.dev/docs/latest/coverage/language/java/)
