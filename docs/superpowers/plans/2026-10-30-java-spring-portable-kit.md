# Portable Java and Spring Boot Kit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. The approved design and the user's instruction to proceed authorize inline implementation and verification.

**Goal:** Produce a portable repository kit expressing the user's accepted Java/Spring conventions, actionable skills, and usable configuration examples.

**Architecture:** Keep concise entry points and focused workflows, with detailed guidance in shared project references. Put integration recipes in templates and executable verification in a separate fixture, without building a business application.

**Tech Stack:** Markdown skills, EditorConfig, Checkstyle, Spotless/Maven, YAML, Liquibase XML, Python 3 validation, and selected Java contract probes.

**Spec:** [Approved design](../specs/2026-10-30-java-spring-portable-kit-design.md).

## Global Constraints

- Remain repository-local and portable; preserve `.idea/` and unrelated files.
- Keep `AGENTS.md` titled Repository Guidelines, approximately 200–400 words.
- Preserve the accepted engineering, adoption, planning, and Git-delivery semantics in the design.
- Use explicit imports and types, four spaces, a 120-column wrapping target, and IntelliJ-owned wrapping.
- Keep dependencies and plugin versions pinned in runnable verification; future bootstrap rechecks compatibility.
- No application scaffolding, global installation, Git initialization, commits, pushes, or publication.
- Use native implementation, with independent behavioral skill checks and a final independent review. No additional planning gate is needed after the user's explicit instruction to proceed.

## Review Focus

1. A copy in a differently named directory must resolve skill and documentation links without the source checkout.
2. A PATCH DTO must preserve inheritance and distinguish omitted, explicit null, and supplied values without weakening create validation.
3. Plain service tests must not be described as evidence that Spring method security or transaction interception works.
4. Existing Gradle/older Java projects must retain their requirements during ordinary adoption.
5. Cleanup tools must not introduce a competing Java formatter or a new project-specific package/database assumption.

## Task 1: Authoritative references and entry points

**Files:** `AGENTS.md`, `README.md`, `docs/java-spring-guidelines.md`, `docs/agent-workflow.md`, `docs/examples/partial-updates.md`.

**Interfaces:** Shared guide links are repository-relative; the engineering guide owns code conventions and the workflow guide owns collaboration/delivery policy. The partial-update example specifies an executable contract for the verification fixture.

- [x] Write a concise entry point, the accepted conventions and rationale, and practical examples.
- [x] Document usage in new projects and selective merging into existing projects, including hidden skill directories.
- [x] Check coverage against the design and resolve internal links once the complete tree exists.

## Task 2: Configuration and integration templates

**Files:** `.editorconfig`, `config/checkstyle.xml`, `templates/README.md`, `templates/maven/quality-plugins.xml`, `templates/application/*.yml`, `templates/liquibase/**`, `verification/pom.xml`, `verification/src/test/**`.

**Interfaces:** Maven configuration uses `${kit.root}/config/checkstyle.xml` and consistent import groups; adoption replaces the project-package prefix. Templates clearly distinguish illustrative fragments from runnable files. Verification depends only on explicit pinned library/plugin versions.

- [x] Check primary documentation for actual IntelliJ import properties, Checkstyle modules, ModelMapper configuration, and compatible pinned versions.
- [x] Create the agreed configurations and optional starter examples, without deployment credentials or a selected database engine.
- [x] Run Maven Checkstyle/Spotless on conforming fixtures; inject wildcard imports or missing braces into temporary copies and confirm rejection.
- [x] Exercise inherited DTO validation and PATCH mapping with real Jackson, Bean Validation, and ModelMapper. Include omitted/non-null/null cases and enforce required-name clearing rules.

## Task 3: Focused skills with behavioral checks

**Files:** `.agents/skills/java-spring-{bootstrap,change,review}/SKILL.md`, `docs/verification.md`.

**Interfaces:** Each skill links to the guides through `../../../docs/`; copying the whole documented kit layout preserves these links. Descriptions distinguish bootstrap, implementation, and review.

- [x] Run no-skill baseline scenarios before authoring skills. Record concrete mismatches, not assumed failures.
- [x] Author bootstrap, validate it, and run the scenario with that skill before moving to change.
- [x] Author change, validate it, and rerun its inheritance/PATCH scenario before moving to review.
- [x] Author review, validate it, and rerun the review scenario. Preserve read-only scope and distinguish correctness findings from convention mismatches.
- [x] Record positive and negative discovery cases and observed limitations. Keep automatic discovery enabled.

## Task 4: Portable validation command

**Files:** `scripts/validate-kit.py`, `tests/test_validate_kit.py`, `requirements-dev.txt`.

**Interface:** `python3 scripts/validate-kit.py [--root PATH]` reports artifact errors and returns nonzero on invalid input; it performs no mutations. Use PyYAML for actual YAML parsing and standard-library XML/path handling.

- [x] Before implementation, write behavioral tests for a relocated kit, a broken local link, malformed XML/YAML, invalid skill metadata, and an escaping reference. Observe failures caused by the missing validator.
- [x] Implement validation limited to kit-owned paths, rather than policing unrelated target-project documentation.
- [x] Run `python3 -m unittest discover -s tests -v` and `python3 scripts/validate-kit.py`; require passing results.

## Task 5: Integration and final review

- [x] Run the validator and its tests, skill-creator quick validation, and Maven verification on the final files.
- [x] Copy the deliverable layout to a temporary directory and validate from another working directory.
- [x] Dispatch one fresh reviewer against the approved design, final files, and Review Focus above. Resolve material issues and rerun affected checks.
- [x] Update `docs/verification.md` with actual commands/results and separate scenario/static/Java checks from unexecuted database or production behavior.
- [x] Update the progress record and leave verified local changes with an entry-point link.
