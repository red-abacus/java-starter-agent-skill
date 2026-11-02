# Repository Guidelines

## Purpose & Organization

This repository is a portable Java/Spring Boot conventions kit. Use the [handbook index](docs/java-spring-guidelines.md) to select task-relevant references and the [working agreement](docs/agent-workflow.md) for collaboration. Read only affected topic sections; configuration adoption uses the [template index](templates/README.md).

Use standard Maven source/test/resource directories in new applications. Group packages by responsibility, adding functional subpackages when size warrants them. Three workflows live in `.agents/skills/`; authoritative topic policies are in `docs/guidelines/`, examples in `docs/examples/`, quality configuration in `config/`, and adoption recipes in `templates/`. `verification/` contains contract probes, not a starter application.

## Architecture & Style

Controllers own HTTP, OpenAPI, input validation, delegation, and response construction. Concrete, domain-focused services own business logic and individual transaction boundaries. Enable method security when used; enforce capabilities on services and resource access through policies. Repositories own persistence: derived methods first, then Specifications, with justified custom queries.

Use base/child DTOs, child-specific validation, and dedicated ModelMapper classes. Preserve omitted/null/value distinctions for PATCH. Entities contain persistence state and relationship helpers. Use Lombok, explicit local types, guard clauses, streams for straightforward transformations, and loops for mutations or multi-step work.

IntelliJ plus `.editorconfig` controls formatting: four spaces, 120-column target, braces, and explicit grouped imports. Spotless cleans up; Checkstyle checks selected rules. Detailed conventions belong in the selected topic reference.

## Build & Verification

Install `requirements-dev.txt`, then run:

- `python3 scripts/validate-kit.py`: validate portable references and configuration.
- `python3 -m unittest discover -s tests -v`: exercise validator failure cases.
- `mvn -f verification/pom.xml verify`: run Java contract probes and quality checks.

For new applications, use Maven Wrapper and verified compatible Java LTS/Spring Boot releases pinned per project. Use JUnit Jupiter, Mockito, AssertJ, MVC slices, Testcontainers, Spring-proxy security tests, and selected integration flows. Report actual results and unavailable checks.

## Collaboration & Delivery

For deletion tasks, ask the user whether physical or soft deletion is needed unless already explicit for that task.

During workflow discovery, establish external-effect ordering, commit dependencies, and delivery requirements with the user.

Keep caching opt-in and define its requirements during affected workflow implementation. Discuss deployment availability budgets and placement with the user during implementation before finalizing them, reusing explicit project answers.

Scale planning to complexity. Respect project requirements and preserve unrelated changes; plan broader migrations separately. Deliver verified local changes by default. Commit or open PRs when requested; merging needs its own instruction. Follow existing commit conventions, otherwise use concise imperative summaries. Explain behavior, verification, and material limitations.
