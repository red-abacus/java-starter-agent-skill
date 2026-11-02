# Portable Java and Spring Boot Kit Design

Status: approved on 2026-10-30. The user authorized implementation with “proceed”.

## Intent and selected approach

Turn the interview's accepted preferences into a portable, application-independent repository kit. The user can copy it into a new starter project or selectively adopt it in an existing project. Future agents must have actionable conventions, examples, and verification guidance without needing this conversation.

The distribution approaches discussed were a repository kit, personally installed skills, or both. The user selected the repository kit. Keep all deliverables here; personal/global installation and plugin publication are outside this scope. The repository currently contains a provisional AGENTS.md and local IntelliJ settings, with no application, build, or Git metadata.

Use a layered kit: concise repository instructions, detailed references, three focused skills, and reusable configuration templates. A single large AGENTS.md would repeat workflow instructions on every task; an application scaffold would require product and infrastructure decisions the user has not made.

## Proposed deliverables

| Path | Purpose |
| --- | --- |
| `AGENTS.md` | Replace the provisional guide with a concise, approximately 200–400 word entry point titled Repository Guidelines. Link to the detailed guides and state core conventions and adoption rules. |
| `README.md` | Explain the kit, its contents, copying into new projects, selective adoption in existing projects, prerequisites, verification, and example skill invocations. |
| `docs/java-spring-guidelines.md` | Authoritative engineering handbook with rationale, practical examples, framework caveats, and links to primary documentation. |
| `docs/agent-workflow.md` | Scaled planning, verification, gradual adoption, and delivery rules. |
| `.agents/skills/java-spring-bootstrap/SKILL.md` | Prepare a new project using this kit; establish project choices, verify compatible versions, and wire selected templates. |
| `.agents/skills/java-spring-change/SKILL.md` | Implement or fix a Java/Spring feature using the accepted conventions and task-appropriate checks. |
| `.agents/skills/java-spring-review/SKILL.md` | Review a change against the handbook and project requirements, reporting evidence and actionable findings. |
| `.editorconfig` | Active IntelliJ-compatible formatting and import settings, plus basic text-file settings. |
| `config/checkstyle.xml` | Enforce the agreed subset of Java style that is suitable for build checks. |
| `templates/` | Clearly labeled Maven quality-plugin integration fragments, application/profile YAML examples, and Liquibase XML organization examples with justified SQL usage. |
| `scripts/validate-kit.py` | Lightweight local validation of artifact structure, references, metadata, and parseable configuration. |

The implementation may split long references or add necessary skill UI metadata and validation fixtures. Keep the three workflow roles distinct. Shared project guides remain the source of truth; skill links must resolve after copying the entire documented kit layout into a different project. Avoid absolute local paths, symlinks, and dependencies on the source repository's location. Package implementation defaults separately from user-confirmed rules.

## Accepted engineering rules

- Organize Java packages by responsibility: controllers, services, entities, repositories, DTOs, utilities, configuration, mappers, and other relevant concerns. Keep them flat by default; use functional subpackages inside responsibility packages only in substantially larger projects.
- Controllers own HTTP endpoints, OpenAPI, query/path validation, request-body validation triggering, delegation, and response construction. Services own business logic, validation requiring context, orchestration, processing, and repository interactions. Split services around domain models.
- Use concrete services. Introduce interfaces for multiple implementations or a clear abstraction, rather than automatically producing Service/ServiceImpl pairs.
- Use base DTOs for common domain fields and specialized child DTOs. Put universally applicable constraints in the base and operation-specific constraints in children. Inherited constraints accumulate; they cannot be relaxed by overriding. Prefer child-specific constraints over validation groups.
- Validate request bodies at DTO level where possible. Services handle remaining business validation and validate state that service processing can invalidate.
- PATCH semantics distinguish omitted (unchanged), explicit null (clear if allowed), and supplied values (validate and apply). Explain presence tracking and its interaction with inherited DTO constraints. Ordinary nullable fields, Optional, or blanket null-skipping alone cannot implement these semantics.
- Use ModelMapper through dedicated mapper classes called by services. Structural conversion belongs there; business decisions remain in services. Jackson handles JSON.
- Entities contain fields, persistence annotations, and relationship helpers. Follow the configured JPA provider's ownership, synchronization, cascade, and lifecycle guidance; do not universalize example cascade settings.
- Use Lombok Getter/Setter for entities and DTOs, RequiredArgsConstructor with final dependencies, Slf4j for logging, selective builders, and DTO constructors where needed.
- Annotate service transaction methods individually: read-only transactions for database reads and Transactional for writes. Account for transaction propagation and proxy invocation when documenting examples.
- Centralize HTTP exception translation with RestControllerAdvice and ProblemDetail, with stable code, traceId, and validation errors. Keep security-filter responses consistent through their own handlers.
- Localize API messages using a combined server/client approach with English fallback, message bundles, and stable machine identifiers. Keep logging messages in English.
- Roles bundle capabilities. Check granular operation capabilities on service methods, and general request permissions in SecurityFilterChain. Use dedicated policies for resource-specific access. Enable method security when used; ordinary self-invocation does not reapply proxy-based annotations.
- Prefer derived repository methods, then Specifications. Custom repository fragments and handwritten queries are justified exceptions. Persistence filtering and pagination should execute in the database where appropriate.
- Use Liquibase XML by default, explicit includes for ordering, focused migration files, and SQL when justified. Preserve applied migration identity/content and exercise real migrations with Testcontainers.
- Use YAML shared defaults, small profile overrides, externalized secrets, and typed, validated ConfigurationProperties injected through constructors.
- Services log business activity and recoveries. The centralized handler logs unexpected propagated HTTP failures once; other entry points own their boundaries. Expected failures normally have no stack trace. Use parameterized messages and meaningful context; correlate logs and response traceId and avoid logging full sensitive objects.
- Use explicit local variable types. Prefer streams for straightforward transformations and loops for multi-step work or state changes. Prefer guard clauses and early returns; retain meaningful if/else alternatives.
- Use four spaces, a 120-column wrapping target, same-line opening braces, braces on single-statement control blocks, UTF-8, LF, final newlines, and no trailing whitespace. Prefer explicit imports, including static imports, alphabetically grouped as JDK, Jakarta, third-party, project, and static. Project-specific package prefixes are configured during adoption.
- IntelliJ's built-in formatter and EditorConfig own detailed formatting. Spotless performs cleanup and selected checks; Checkstyle enforces selected structural rules. Do not configure a competing full Java formatter or claim exact line-wrap parity in CI.
- Use Maven for new projects, with the latest compatible Java LTS and stable supported Spring Boot version verified at project creation and pinned per project. Use the Maven Wrapper and Boot dependency management. Preserve existing build/version choices during unrelated work.
- Default testing uses JUnit Jupiter, Mockito, AssertJ, MVC slices with MockMvc, real mapper tests, repository tests with Testcontainers, method-security tests through actual Spring proxies, and selected full application tests. Test relevant outcomes, failure paths, partial updates, access restrictions, and transaction behavior.

## Accepted agent workflow

Use direct implementation for small clear tasks, a short plan for standard features, and design review for substantial or uncertain decisions. Ask about missing business decisions; resolve routine choices using established conventions. Verify before claiming completion and report actual results and limitations.

Deliver verified local changes by default. Commit or open a PR when requested, including the necessary intermediate steps without repeated approval requests. Merging requires its own instruction. Follow existing commit conventions or use concise imperative messages. Preserve unrelated user changes.

For existing applications, respect project requirements, apply personal defaults where compatible, and make relevant bounded improvements. Plan broader migrations separately. Never turn ordinary adoption into an unrequested framework upgrade, package reorganization, or public-contract change.

## Builder decisions and project-specific choices

The builder may choose concise filenames, illustrative names, skill descriptions, documentation splits, and fixture design. Preserve the accepted semantics above. Exact package singular/plural spelling, test naming, and example class names are implementation defaults rather than newly inferred personal requirements.

Future target projects choose their database, authentication mechanism, artifact/package identifiers, supported locales, deployment environment, and business capabilities. Bootstrap must obtain these when necessary rather than infer them from the Nexcall examples. Avoid copying proprietary code, organization-specific infrastructure, or local IntelliJ state into the kit. Preserve the existing `.idea/` directory.

Provide reusable configuration examples and integration instructions rather than creating a runnable business application. Any versions embedded in examples are a dated, verified snapshot; the bootstrap workflow must recheck compatibility before initializing a future project. Keep schema migration examples illustrative and inactive until adopted.

## Verification and acceptance

- Check every accepted rule is represented and that skill instructions agree with the guides.
- Validate skill metadata and positive/negative trigger examples, including preserving an existing Gradle project and not expanding a review into implementation.
- Resolve local Markdown links and skill reference paths, including from a temporary copy in a differently named directory.
- Parse XML/YAML configuration and verify the EditorConfig/import settings against official tool documentation.
- Exercise Checkstyle and Spotless configuration with small valid and invalid Java fixtures if compatible runtimes and dependencies are available. Report any unavailable execution instead of claiming success.
- Verify the kit validation command, document prerequisites, and separate static checks from Java/database behavior that has not been executed.
- Review the resulting files for contradictions, stale version claims, accidental broad approval gates, and invented preferences.
- Leave all work local. Do not initialize Git, commit, push, publish, or change global agent settings.

Successful delivery is a readable, portable, internally consistent kit with actionable skills and reusable configuration, accompanied by concrete verification evidence and clearly stated project-specific decisions.
