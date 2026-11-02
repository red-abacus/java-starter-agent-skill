# Application Configuration Recipes

Read only the recipe sections needed for the configuration being adopted. [Template index](../README.md).

## Application configuration

### YAML and profiles

Merge [the YAML fragments](application.yml) into `src/main/resources/`. Keep shared defaults in `application.yml`; profile files contain small differences. Select profiles externally. Add database/provider settings only when selected, with secrets supplied outside source control.

### Caching

Follow the [caching policy](../../docs/guidelines/architecture-java-style.md#caching): starter applications have no application caching by default. Add it only when specifically required by the user or an agreed workflow, defining all applicable requirements during implementation of that workflow. Do not add cache dependencies, annotations, settings, or infrastructure as starter defaults.

### Google Cloud access

For Google Cloud access on GKE, follow the [application identity policy](../../docs/guidelines/delivery-gke.md#application-identity-and-google-cloud-clients): configure the workload's Kubernetes ServiceAccount and resource permissions, and let ADC obtain runtime credentials through WIF. Select Google Cloud Spring starters only for integrations that benefit from them, with a compatible pinned BOM; plain Google clients are also supported. The fragments do not configure cluster identities, IAM grants, or private-key credentials.

### Secrets

Follow the [secret delivery policy](../../docs/guidelines/delivery-gke.md#secret-storage-and-delivery): use Google Secret Manager and startup loading through its Spring starter by default. Configure secret references with explicit versions for the target environment, grant only required access, and fail startup for unavailable required secrets. Keep values outside Git, images, and Helm values. Rotate through a controlled release and rolling restart unless tested refresh or an established platform delivery mechanism justifies an alternative. The fragments do not select secrets or add the starter/import configuration.

### Persistence

For new JPA REST APIs, the fragment disables OSIV with `spring.jpa.open-in-view: false`. Fetch required relationships and construct response DTOs inside service transactions. Review existing applications' lazy-loading dependencies before adopting this setting.

### Health and availability

For new deployed applications, add `spring-boot-starter-actuator` and adopt the fragment's minimal health exposure and availability probes. It hides health details/components; configure any authorized diagnostic detail deliberately. Define endpoint access in SecurityFilterChain. When using a separate management port, also configure main-port probe paths, for example with `management.endpoint.health.probes.add-additional-paths: true`, and their access rules. Choose readiness dependencies and deployment probe timing for the application; the fragment does not configure security or deployment infrastructure.

### Graceful shutdown

The fragment explicitly enables [graceful shutdown](../../docs/guidelines/operations.md#graceful-shutdown). Select `spring.lifecycle.timeout-per-shutdown-phase` per application and coordinate all applicable shutdown phases, load-balancer draining, and any `preStop` hook with the Pod's `terminationGracePeriodSeconds`. Configure background-work shutdown/recovery according to its delivery requirements, confirm signal delivery, and verify termination under active traffic and relevant processing. Concrete timeouts and deployment hooks belong to the target project.

### Metrics and tracing

Use Actuator's Micrometer metrics and add the registry/export configuration selected for the project's monitoring platform. When tracing is justified, select compatible Micrometer Tracing/OpenTelemetry dependencies and OTLP export settings. Configure any additional management endpoint exposure and access explicitly, and verify trace/correlation propagation through HTTP clients and asynchronous work.

### Typed settings

Bind grouped settings to a validated `@ConfigurationProperties` class, register it with scanning or `@EnableConfigurationProperties`, and inject it through constructors. The example timeout should bind to `Duration`, with an appropriate positivity/range constraint.

### Localization

For localization, `messages.properties` contains English fallback text; locale-specific bundles override supported translations. Set an explicit supported locale list, default English, and an Accept-Language resolver. Disabling system-locale fallback alone does not set the request locale. Use stable message keys/error codes and preserve placeholders. The fragments do not implement the resolver or error handler.
