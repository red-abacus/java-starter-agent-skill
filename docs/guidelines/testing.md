# Testing Guidelines

Read when: Selecting checks for the affected behavior; read the surface table and applicable subsections.

Use only the sections relevant to the task. [Handbook index](../java-spring-guidelines.md).

## Sections

- [Testing](#testing)
- [Naming, structure, and fixtures](#naming-structure-and-fixtures)
- [Time and asynchronous determinism](#time-and-asynchronous-determinism)
- [External HTTP integration tests](#external-http-integration-tests)
- [Database test isolation](#database-test-isolation)

## Testing

| Surface | Default approach |
| --- | --- |
| Business rules | JUnit Jupiter, Mockito, AssertJ; focused unit tests with substituted collaborators. |
| Controllers | MVC slices with MockMvc and mocked services; verify binding, DTO validation, HTTP status/headers, error shape, and relevant locale behavior. |
| Mappers | Real configured ModelMapper, including custom conversions and PATCH presence/null cases. |
| External HTTP clients | Local WireMock servers with the real client/transport; mock provider clients in service unit tests. |
| AI workflows | Layered application tests and live-model evaluations under the [Spring AI evaluation convention](spring-ai-evaluations.md#testing-and-evaluations), with versioned workflow datasets and workflow-specific acceptance criteria. |
| Persistence | Repository tests with Testcontainers using the production database engine and real migrations. |
| Method security | Actual Spring-managed service proxy with method security enabled; allowed/denied capabilities and resource restrictions. |
| Complete flow | Selected SpringBootTest scenarios for wiring, transactions, and important cross-layer behavior. |

Load the intended web security configuration in relevant MVC tests. A mocked service cannot prove its actual authorization annotations work. Test role-to-capability expansion separately from supplying authorities directly with `@WithMockUser`. For a live server, authenticate the HTTP request itself; test-thread security context does not automatically cross to the server thread.

Plain unit tests do not exercise Spring transactions. For transaction-dependent behavior, verify database outcomes and rollback through the real boundary. Account for test-managed rollback masking commit/flush behavior, and flush/reload when testing persistence effects. Container-backed tests need a compatible container runtime. Report unavailable checks rather than treating skipped tests as passing.

Prefer behavioral coverage, boundaries, failures, and regression cases to generated-accessor tests or arbitrary coverage targets. No numeric coverage threshold is prescribed.

### Naming, structure, and fixtures

Mirror production packages under `src/test/java`. Use `*Test` for unit/slice tests and `*IT` for integration tests, wiring the actual Maven runners accordingly. Name test methods with `should<Outcome>When<Condition>`, such as `shouldRejectCreationWhenCustomerCodeAlreadyExists`.

Structure tests as Arrange, Act, Assert, separated by blank lines. Add comments when they clarify the scenario. Focus each test on one behavior; multiple related assertions are appropriate. Keep tests independent of execution order and shared mutable state.

Keep setup close to the test. Use `@BeforeEach` for genuinely shared preparation and small fixture builders/factories for repeated domain setup. Group related scenarios with `@Nested` when it improves navigation, and use `@ParameterizedTest` when the same behavior should hold across several inputs.

Verify meaningful outcomes with AssertJ and important collaboration contracts with Mockito. Preserve existing project conventions during gradual adoption.

### Time and asynchronous determinism

Inject Java's `Clock` into services whose business behavior needs the current time, such as token expiration, cancellation cutoffs, or temporary access checks. Use `Clock.systemUTC()` in production and a fixed or otherwise controlled clock in tests, applying the agreed business zone where calendar rules require it. Test relevant before/at/after boundaries explicitly.

Ordinary CRUD and comparisons between supplied dates do not require a Clock merely for consistency. Framework-managed audit timestamps may retain their configured auditing mechanism. A fixed business clock does not advance executors, network timeouts, or database clocks; control each relevant time source explicitly when its behavior is under test.

For asynchronous tests, use bounded futures/latches when completion can be signalled directly, or Awaitility for eventually observable results with an explicit maximum wait and meaningful assertions. Keep polling assertions free of side effects and use completion-based waits rather than arbitrary sleeps for synchronization.

Separate fast business-rule tests from tests exercising real asynchronous execution. Test retry calculations with controlled delays and randomness where practical, retaining integration tests for actual timing and transport behavior where required.

### External HTTP integration tests

Mock provider clients in service unit tests. For client integration tests, use local WireMock servers with the real RestClient and the HTTP transport implementation used in production. Assign ports dynamically, configure the client's test base URL, and reset expectations and recorded requests between tests. WireMock's JUnit Jupiter extension can manage the server lifecycle.

Verify methods, paths, query parameters, headers, JSON payloads, and response handling. Cover successful responses, documented business rejections, malformed responses, timeouts, and relevant retry behavior. Keep routine tests independent of live provider availability.

Use MockRestServiceServer as a focused isolated alternative where appropriate. Its replacement request factory does not exercise real network traffic, so use a local HTTP server for transport-dependent claims.

Stubs verify the client against configured examples. Maintain contract examples or use selected sandbox checks when actual provider compatibility needs verification; local stubs alone do not prove that the provider still implements those examples.

### Database test isolation

Choose isolation according to the behavior under test. Reuse containers within a properly managed lifecycle to reduce startup cost while isolating each test's data. Align container lifetime with the Spring contexts that access it.

Use rollback for ordinary repository tests whose changes remain in the test transaction. For tests that commit, use real HTTP requests, or execute background work, provide explicit cleanup/reset or separate databases/schemas as appropriate. A test transaction does not roll back independent server or worker transactions. Finish background work before cleanup so later writes cannot contaminate subsequent tests.

Create small, scenario-owned fixtures. Read generated IDs from saved entities instead of assuming particular sequence values. Flush and reload where assertions depend on actual database persistence or constraints, and exercise real transaction boundaries when verifying commit/rollback behavior.

Start shared-database integration tests sequentially. Introduce parallel execution only with verified data isolation and supported container lifecycle management, using separate databases/schemas where needed. Keep the selected production database engine and actual Liquibase migrations under the existing persistence testing policy.

## Primary references

Consult documentation matching the target project's versions when verifying framework behavior.

- [Java Clock](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/time/Clock.html)
- [Spring Boot testing](https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html)
- [Spring test-managed transactions](https://docs.spring.io/spring-framework/reference/testing/testcontext-framework/tx.html)
- [Testcontainers JUnit lifecycle](https://java.testcontainers.org/test_framework_integration/junit_5/)
- [Spring HTTP client testing](https://docs.spring.io/spring-framework/reference/testing/spring-mvc-test-client.html)
- [WireMock JUnit Jupiter integration](https://wiremock.org/docs/junit-jupiter/)
- [JUnit nested tests](https://docs.junit.org/6.0.3/writing-tests/nested-tests.html)
- [JUnit parameterized tests](https://docs.junit.org/6.0.3/writing-tests/parameterized-classes-and-tests.html)
- [Awaitility usage](https://github.com/awaitility/awaitility/wiki/Usage)
