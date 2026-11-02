# Agent Working Agreement

This agreement governs collaboration and delivery. The [engineering handbook](java-spring-guidelines.md) owns implementation conventions. The current user request and the project's applicable instructions determine the task.

## Understand the change

Read relevant project instructions, code, tests, build configuration, and public contracts before deciding what to change. Reuse what the repository already answers. Ask focused questions when a missing business requirement materially changes the outcome; settle routine choices using the project and the kit.

Respect new-project defaults and existing-project constraints. Resolve missing product requirements that materially affect the task; do not infer a database, authentication provider, or example Customer domain from this kit.

Use the [handbook index](java-spring-guidelines.md) to select topic sections. During affected workflow implementation, establish requirements for deletion, caching, external-effect ordering/delivery, and deployment availability controls using the corresponding guide. Reuse explicit answers already supplied for that task or project. Continue independent work while material questions remain pending.

Establish [reliability goals and alerting](guidelines/operations.md#reliability-goals-and-alerting) per project during discovery, agreeing concrete targets and configuration during the affected operational implementation.

## Scale planning

| Task | Expected collaboration |
| --- | --- |
| Small, clear change | Inspect, implement, and verify without a separate planning approval. |
| Standard feature following established conventions | Outline a short plan and proceed when requirements are clear. |
| Substantial or uncertain change | Investigate, explain meaningful approaches/trade-offs, and align on the design before implementation. |

A useful plan states intended behavior, scope/non-goals, affected layers/configuration/migrations, acceptance criteria, verification commands, and unresolved decisions. Use a durable plan for longer work. Do not add formal documents or approval gates to every small edit. Once an approach is settled, continue through implementation and verification rather than returning only a plan or repeatedly asking whether to proceed.

Give concise progress updates at meaningful discoveries, decisions, or limitations. Bring the user back in when a material assumption fails or the agreed scope needs to change. Established conventions, including mapping library and DTO shape, are already decisions rather than questions to reopen on every feature.

## Existing projects

Respect documented and enforced requirements. Apply personal defaults where the project leaves room and make relevant, bounded improvements that support the task. Preserve unrelated user work.

For an existing Gradle project, keep Gradle. For an existing Java/Boot baseline, do not upgrade it during an unrelated change. Preserve enforced formatting and public error/DTO contracts unless migration is requested. A local mapper extraction can support a feature when compatible; converting every service or reorganizing all packages is a broader migration.

When an adopted default conflicts with an existing requirement, preserve that requirement and report material deviations. Involve the user when the decision changes architecture, public behavior, or scope; do not ask about every routine difference. Explicit instructions to migrate override the ordinary gradual-adoption default within the requested scope.

## Implement and verify

Keep changes focused on the requested behavior. Add meaningful regression/behavior tests where appropriate. Use the smallest useful check while developing, then complete the project's required checks for the final change. Pure documentation/formatting edits do not need artificial application tests.

Update affected documentation with the change, following the [documentation conventions](guidelines/architecture-java-style.md#documentation-and-comments), including the preference to avoid adding Javadoc by default.

Use the actual build/wrapper and supported runtime. Confirm mapping, validation, persistence, authorization, and transaction claims at the layer where the behavior exists. A plain mock-based unit test does not prove a Spring interceptor or database constraint works.

Run the checks before claiming success. Fix failures within scope. Identify pre-existing failures, unavailable dependencies/container runtimes, and skipped checks by name. Do not describe intended tests or an unexecuted CI pipeline as passing evidence. If verification cannot run, explain exactly what was checked and what remains unverified.

## Git delivery

Default delivery is verified local changes plus a concise handoff. It does not include automatic commits or pushes.

- A request to commit includes the necessary local commit, without implying a push.
- A request to open a PR includes its branch, commits, push, and PR creation. Complete authorized intermediate steps without repeated questions. Use draft/ready status as requested; when unspecified, prefer a draft and state its status.
- Merging needs its own instruction.

Keep commits focused and include only the task's changes. Follow existing commit conventions; otherwise use concise imperative messages such as `Handle explicit nulls in customer updates`. PRs explain the problem and resulting behavior, verification evidence, and material migration/configuration changes. Link relevant provided issues and report actual CI state.

## Handoff

Lead with the result. Include the changed behavior, relevant files, executed verification and outcomes, and material limitations or project decisions. Keep routine implementation detail brief. A blocked check or pending CI result remains visible; do not conceal it behind a broad “all verified” statement.
