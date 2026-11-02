# Execution ledger — plan: 2026-10-30-java-spring-portable-kit.md

## Decisions and preflight

- The user approved the design and said to proceed. Execute inline without another approval round.
- The workspace is not a Git repository. Keep the ledger here instead of Git-dependent execution scripts; leave all work local as requested.
- This is a documentation/configuration kit, not a Java application. Validate configurations with real tools and contract probes; avoid tests that merely assert documentation wording.
- Java 25 and Maven 3.9.12 are available. Python 3.12 and PyYAML are available.
- Existing IntelliJ settings use Checkstyle 12.1.0 with no active custom profile. Preserve them and explain how to select the kit profile.
- Shared interfaces: skill links, README copying instructions, and the validator must agree on the same repository-relative layout. Maven templates and verification must agree on `kit.root` and the Checkstyle profile.

## Baseline observations

- Bootstrap baseline selected feature packages, unrelated record DTOs, handwritten mapping, Flyway, and a fixed Java 21 baseline. Quote: “Organize by feature: customer.api, customer.application, customer.domain, and customer.persistence”. It also chose a JWT boundary without a selected authentication mechanism. This is a reference/default gap, not a lack of general engineering ability.
- Change baseline correctly preserved Gradle, distinguished field presence, isolated mapper behavior, and required Spring-proxy security tests. It solved inheritance conflicts by saying “Make UpdateCustomerDto independent of BaseCustomerDto”, which differs from the user's chosen DTO convention.
- Review baseline identified the major security, PATCH, and error-handling bugs without the kit. It treated the unnecessary interface and simple @Query as cleanup opportunities. The kit should add grounded convention checks, not claim credit for already-correct generic review behavior.

## Progress

- Task 1: complete. Entry points, engineering/workflow guides, and partial-update explanation written; owned links resolve.
- Task 2: complete. Eight Java probes and both quality checks pass. A failed explicit-null probe exposed engine-wide ModelMapper null-skipping despite a copied TypeMap configuration; the dedicated PATCH engine fixes the reproduced case without mutating the injected ordinary mapper. Negative quality probes reject wildcard imports, wrong order, and missing braces. Maven recipe and fixture plugin definitions match structurally.
- Task 3: complete. All three skills authored, quick-validated, and independently exercised. Bootstrap chose responsibility packages, inherited DTOs, ModelMapper, Liquibase, compatible versions verified at creation, and deferred unknown product choices. Change preserved inheritance and existing Gradle/Java/error contracts. Review separated defects from convention preferences. Routing checks excluded unrelated implementation/review tasks.
- Task 4: complete. Validator tests observed failing because the implementation was absent; all 13 now pass. Validator checks only owned artifacts and supports optional fixture omission.
- Task 5: complete. Runtime and full copies validate from another working directory. Full relocated Maven verification passes. Fresh final review found no critical/important issues and independently repeated Python/Maven checks in another fresh copy. Its minor README-copy link issue was reproduced and fixed by documenting the companion verification file; the corrected optional copy validates.

## Execution notes

- The sandbox protected `.agents/` and blocked Maven cache/network access. Narrow escalated writes to the approved skill paths and Maven downloads into `/tmp/deconstruct-java-m2` were automatically approved. No global skills were installed.
- Maven fixture pins Java 25, Boot 4.1.2, ModelMapper 3.2.8, Spotless 3.10.4, Checkstyle plugin 3.6.0, and Checkstyle 12.1.2. Boot manages the remaining dependency/plugin versions.
- Final delivery remains local. All five tasks are complete; no application, Git metadata, commit, push, PR, global skill installation, or `.idea/` changes were introduced.
