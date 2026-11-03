# Java and Spring Boot Working Kit

A portable set of conventions and agent workflows based on the owner's preferred way of building Java/Spring Boot applications. Use it as a starting point for a new project or adopt the parts that fit an existing application.

## Start here

- [AGENTS.md](AGENTS.md): concise repository instructions.
- [Engineering handbook](docs/java-spring-guidelines.md): task routing to focused architecture, API, persistence, security, testing, and delivery references.
- [Agent workflow](docs/agent-workflow.md): planning, adoption, verification, and Git delivery.
- [Partial-update example](docs/examples/partial-updates.md): inheritance, validation, field presence, and ModelMapper.
- [Template guide](templates/README.md): configuration files and Maven integration.
- [Verification record](docs/verification.md): checks actually exercised and their limits.

The kit contains guidelines and integration examples. It has no business application, chosen database, authentication provider, or deployed infrastructure. New-project delivery defaults are GKE, Artifact Registry container images, Helm releases, and GitHub Actions CI/CD; configure concrete environments per project. Files under `verification/` are small executable contract probes for the kit's examples.

The handbook is a task index, not required background reading in full. Skills load its selected topic sections and examples as needed. Template adoption is also routed by configuration task, so an application change need not read delivery recipes. A reference link makes guidance discoverable; it does not enforce a model's reading behavior.

## Skills

| Skill | Use it for |
| --- | --- |
| [java-spring-bootstrap](.agents/skills/java-spring-bootstrap/SKILL.md) | Starting a new Java/Spring Boot project from these conventions. |
| [java-spring-change](.agents/skills/java-spring-change/SKILL.md) | Implementing a feature or fixing an existing Java/Spring Boot application. |
| [java-spring-review](.agents/skills/java-spring-review/SKILL.md) | Reviewing a change against project requirements and applicable kit conventions. |

Example prompts:

```text
Use $java-spring-bootstrap to prepare this empty repository for a Spring Boot API.
Use $java-spring-change to add customer status updates using this project's contracts.
Use $java-spring-review to review the customer PATCH changes without editing files.
```

Codex discovers repository skills in `.agents/skills/`. Other agents can read `AGENTS.md`, the guides, and skill files directly; automatic discovery depends on their support. See the [official skill documentation](https://learn.chatgpt.com/docs/build-skills).

## Reuse in a new project

Copy the following together, preserving their relative locations and hidden directories:

```text
AGENTS.md
.editorconfig
.agents/skills/
docs/java-spring-guidelines.md
docs/agent-workflow.md
docs/guidelines/
docs/examples/
config/checkstyle.xml
templates/
```

If retaining this README as a kit reference, also copy `docs/verification.md` so its source-kit verification links remain valid. Otherwise, merge relevant instructions into the application's README and omit the source-kit verification sections. A new application's AGENTS.md should retain the core rules and add its actual packages, commands, required environment variables, and project-specific decisions. Its command section must describe the application rather than this kit's verification harness.

The skill and example links above assume the complete documented layout. Do not copy a skill alone without its linked project guides. Keep development records under `docs/superpowers/` in this source repository; future applications do not need them.

Before generating the application, establish its Maven coordinates, base package, required integrations, database when persistence is needed, and authentication requirements when security is needed. Then select compatible versions from current primary documentation. The pinned verification versions here are a dated example, not a permanent definition of “latest”.

Follow [the template guide](templates/README.md) to merge Maven plugins, replace the illustrative `com.example` import prefix, and adopt only the profile/migration examples the project needs. Create Maven Wrapper for the new application. Keep its Java major version aligned across IntelliJ, Maven, CI, and production.

## Adopt in an existing project

Inspect its instructions, formatter, build, versions, public contracts, security model, and migrations first. Merge guidance into existing files; review differences before replacing anything. Preserve an existing Gradle build or established API envelope during an unrelated feature. Use the kit where compatible and plan broader migrations separately.

Add the skills and shared guides together. Adapt their root-relative guide locations if the project uses another documentation layout. Update package-specific import configuration in all three places: `.editorconfig`, Checkstyle, and the Maven Spotless recipe.

IntelliJ picks up `.editorconfig` when its bundled EditorConfig support is enabled. If using CheckStyle-IDEA, select `config/checkstyle.xml` as a project configuration. The kit does not overwrite local `.idea/` settings. CI checks the selected rules; it does not reproduce every IntelliJ line-wrap decision.

## Verify this kit

Prerequisites: Python 3.10+, PyYAML, Maven 3.9+, and Java 25 for the dated Java verification fixture. The fixture may download Maven dependencies. Use an isolated virtual environment for Python dependencies if desired.

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate-kit.py
python3 -m unittest discover -s tests -v
mvn -f verification/pom.xml verify
```

The Python command is read-only. It checks kit-owned paths, skill frontmatter, local references and Markdown heading destinations, and XML/YAML syntax. Its tests exercise missing and malformed artifacts, topic references, and relocation. Maven runs real mapping/validation contract probes, Checkstyle, and the cleanup checks. See [verification details](docs/verification.md) for negative checks and unexecuted integration surfaces.

For skill-routing changes, run the separate [read-only agent scenarios](verification/skill-scenarios/README.md). They cover prompt changes, evaluation deployment gates, and unrelated Java work; the Python suite does not execute them.

To validate a relocated copy that includes the optional maintenance files, run:

```sh
python3 /path/to/copied-kit/scripts/validate-kit.py --root /path/to/copied-kit
```

For maintaining the kit itself, also copy `scripts/`, `tests/`, `requirements-dev.txt`, `verification/`, and this README. Application adopters need only the runtime guidance/configuration layout above. Keep short instructions and skills focused. Update the authoritative topic reference when a convention changes, and update the handbook routing only when its read conditions change.
