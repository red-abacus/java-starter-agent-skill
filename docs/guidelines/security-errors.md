# Security and Error Contracts

Read when: Changing authentication, authorization, resource scope, error handling, or localization.

Use only the sections relevant to the task. [Handbook index](../java-spring-guidelines.md).

## Sections

- [Authentication approach](#authentication-approach)
- [JWT implementation](#jwt-implementation)
- [JWT signing keys](#jwt-signing-keys)
- [Token lifetimes and renewal](#token-lifetimes-and-renewal)
- [CORS](#cors)
- [CSRF](#csrf)
- [Password storage](#password-storage)
- [Deferred abuse controls](#deferred-abuse-controls)
- [Security](#security)
- [Java exception conventions](#java-exception-conventions)
- [Errors and localization](#errors-and-localization)

## Authentication approach

When an API needs authentication, the owner's usual starting point is application-issued JWT bearer tokens, with the application responsible for both issuance and validation. Confirm the authentication flow during project discovery, using existing explicit decisions. Project functionality and client requirements may justify a different mechanism or explicitly separated mechanisms.

Start with stateless request authentication: validate the JWT without retaining server-side authentication sessions. Add session tracking and invalidation only when the project's functionality requires them. Define the storage, lifetime, and effect of invalidation on subsequent authentication for the affected workflow.

Establish caller types, how credentials reach the API, deliberately public endpoints, and the issuance/validation contract. Alternative token formats and identity providers remain project-specific exceptions to the usual setup. Authentication is implemented when required by the application; these defaults do not add login or token endpoints to unrelated workflows.

Login throttling and API rate limiting remain [deferred opt-ins](#deferred-abuse-controls).

## JWT implementation

Use Spring Security's JWT components by default for application-issued tokens. A focused authentication service owns the authentication flow and issuance. Use `JwtEncoder`, typically `NimbusJwtEncoder`, to create/sign tokens, and Resource Server support with a configured `JwtDecoder` to validate incoming tokens through the security filter chain. Configure `SessionCreationPolicy.STATELESS` for the default stateless flow.

Define signing keys, token claims, validation rules, and lifetimes for the target project. When session tracking is introduced, establish whether invalidation rejects already-issued JWTs, prevents renewal, or both; implement the checks required by that agreed behavior.

## JWT signing keys

Use asymmetric RS256 signing by default: a private key signs tokens, and trusted public keys verify them. Store private keys in Google Secret Manager under the existing [secret delivery policy](delivery-gke.md#secret-storage-and-delivery), using WIF/ADC and startup loading. Keep keys separate across environments and stable across application replicas and restarts; do not generate a new production signing key on each Pod startup.

Configure trusted verification keys and accepted signing algorithms explicitly. Include a key identifier (`kid`) and plan rotation so overlapping deployments can validate tokens signed by current and retiring keys. Define key strength, rotation timing, and rollout coordination during implementation, accounting for outstanding unexpired tokens.

Choose Cloud KMS signing when project requirements justify managed signing. Integrate the signing operation explicitly and account for its network dependency; the default local `NimbusJwtEncoder` configuration does not automatically delegate signing to KMS.

## Token lifetimes and renewal

Every access JWT has an explicit expiry. Configure lifetimes per project according to the affected workflow's security and usability requirements. Start with JWT-only authentication when it meets those requirements; refresh tokens are opt-in.

When persistent login requires refresh tokens, use rotating, revocable refresh tokens with stored lifecycle state. Access JWT validation for ordinary API requests can remain stateless while renewal and refresh-token revocation use that retained state. Define expiry, renewal, logout, and invalidation behavior with the user during workflow implementation, using existing explicit decisions.

## CORS

Configure CORS when cross-origin browser access is required. Centralize configuration through `CorsConfigurationSource` integrated with `SecurityFilterChain`, using explicit origin allowlists defined per project and environment.

Allow the methods and headers the clients need, including exposed response headers where the public contract requires browser access. Enable credentialed browser requests only when the authentication flow requires them. Test allowed/rejected origins and preflight requests through the actual security configuration so authentication does not incorrectly block permitted preflights.

## CSRF

Determine CSRF handling during implementation from the actual credential transport. For endpoints protected exclusively by explicitly supplied `Authorization` bearer tokens, use a scoped CSRF exemption only after confirming they accept no automatically supplied browser credentials.

Protect affected state-changing requests in cookie/session flows, including JWT or refresh-token cookies. In mixed applications, scope protection and exceptions to the relevant endpoints or security filter chains. Stateless authentication alone does not establish that CSRF protection can be disabled.

Revisit the configuration when authentication or credential transport changes. Verify protected requests with missing, invalid, and valid CSRF tokens through the actual security configuration.

## Password storage

When the project manages user passwords, use Spring Security's `PasswordEncoder` abstraction and explicitly select Argon2id for new hashes. Use `DelegatingPasswordEncoder` to identify stored formats and support gradual upgrades from existing encodings; do not assume its factory default selects Argon2id.

Store salted, adaptive password hashes and keep hashes out of response DTOs and credentials out of logs. Tune hashing parameters against the actual deployment's CPU, memory, and acceptable login latency. Hashing runs inside the application; select compatible implementation dependencies when implementing the password flow.

Preserve an existing project's established encoding until a migration is deliberately included in scope.

## Deferred abuse controls

Treat login throttling and API rate limiting as later-stage considerations. They are not default application or starter features. Implement them only when explicitly included in the requested or agreed project scope, defining the concrete requirements and mechanism with the user during that work.

## Security

Roles are bundles of capabilities. Define capability identifiers centrally and enforce them on public service entry methods, for example `@PreAuthorize("hasAuthority('customer:update')")`. Use `SecurityFilterChain` for authentication requirements, deliberately public endpoints, and general request restrictions. Avoid repeating the full business permission policy across controllers and services.

An operation capability is not unrestricted access to every matching resource. Where required, call a dedicated access policy for ownership, organization/tenant membership, or resource-specific restrictions before exposing or changing data. Apply required scope predicates to queries too.

Enable method security when used, normally with `@EnableMethodSecurity`. Spring Boot's security dependency alone does not establish that these checks are active. Security annotations rely on invocation through the configured Spring interception mechanism; a direct constructor call or self-invocation is not proof of enforcement. For jobs and service-to-service entry points, establish the intended execution identity and boundary rather than bypassing checks accidentally.

Security-filter failures can happen before MVC handling. Configure the corresponding authentication/access-denied handlers to return the same error format and localization as controller advice. Preserve the API's intended distinction between authentication and authorization failures.

## Java exception conventions

Use specific unchecked exceptions (`RuntimeException` subclasses) by default for failed operations, such as `CustomerNotFoundException` or `OrderAlreadyClosedException`. Keep HTTP status selection and response construction in the centralized advice, rather than coupling service exceptions to HTTP.

Retain `Optional<T>` for expected single-result absence. Introduce explicit result models when callers routinely branch on several meaningful workflow outcomes; do not add a universal result wrapper. Preserve checked exceptions where an established contract or justified use case requires them.

Catch exceptions to recover, translate at a boundary, or add useful context. Preserve the original cause when wrapping; follow the logging policy rather than logging merely to rethrow.

Account for the actual [transaction configuration](entities-persistence.md#transactions): Spring's ordinary default rolls back on unchecked exceptions and errors, not checked exceptions. When a checked exception crosses a transaction boundary, deliberately configure and test the required rollback behavior, using type-based rules where needed.

## Errors and localization

Use a centralized `@RestControllerAdvice` with `ProblemDetail`, normally supported by `ResponseEntityExceptionHandler` for built-in MVC errors. Services throw meaningful custom exceptions; the HTTP boundary selects status and response details.

Default mappings: invalid input 400, missing required resource 404, known conflict 409, and unexpected failure 500. Preserve more specific established contracts where applicable. Handle validation failures from bodies, query/path parameters, nested DTOs, and object-level rules. Avoid converting every exception into a generic 500.

Use RFC 9457 fields and extensions:

```json
{
  "type": "https://api.example.com/problems/validation-error",
  "title": "Request validation failed",
  "status": 400,
  "detail": "One or more request fields are invalid.",
  "instance": "/api/v1/customers",
  "code": "VALIDATION_ERROR",
  "traceId": "9e6f42d8c1054c42ad03af1164fc2348",
  "errors": [
    {"field": "email", "code": "INVALID_EMAIL", "message": "Must be a valid email address."}
  ]
}
```

This is an illustrative problem-type URI and trace identifier. A project supplies its actual stable type URIs and tracing/correlation context. Include validation errors for validation failures, not as fabricated field errors on unrelated problems. Object-level failures may have no field path. Clients should branch on stable codes rather than human messages. Return safe details, not stack traces, database diagnostics, or arbitrary exception messages.

Use the combined localization approach: the server returns localized defaults and clients may provide their own text using stable codes. Resolve the supported language through `Accept-Language` and fall back to English. Use message bundles and `MessageSource` for titles, details, and validation messages. Keep identifiers, field paths, and problem-type identities stable across languages. Configure supported locales and message fallbacks explicitly; do not depend on the host machine's locale or expose raw message keys on missing translations.

## Primary references

Consult documentation matching the target project's versions when verifying framework behavior.

- [Spring method security](https://docs.spring.io/spring-security/reference/servlet/authorization/method-security.html)
- [Spring Security application-issued JWT support](https://docs.spring.io/spring-security/reference/servlet/oauth2/)
- [Spring Security JWT validation](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html)
- [Spring Security stateless authentication and sessions](https://docs.spring.io/spring-security/reference/servlet/authentication/session-management.html)
- [Spring Security CORS integration](https://docs.spring.io/spring-security/reference/servlet/integrations/cors.html)
- [Spring Security CSRF considerations](https://docs.spring.io/spring-security/reference/features/exploits/csrf.html)
- [Spring Security CSRF configuration and testing](https://docs.spring.io/spring-security/reference/servlet/exploits/csrf.html)
- [Spring Security password encoders](https://docs.spring.io/spring-security/reference/features/authentication/password-storage.html)
- [OWASP password storage guidance](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [JWT security best practices](https://www.rfc-editor.org/rfc/rfc8725.html)
- [Refresh token security and rotation](https://www.rfc-editor.org/rfc/rfc9700.html#section-4.14)
- [Google Cloud digital signatures](https://docs.cloud.google.com/kms/docs/digital-signatures)
- [Spring error responses](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-rest-exceptions.html)
- [Spring transaction rollback rules](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/rolling-back.html)
- [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html)
