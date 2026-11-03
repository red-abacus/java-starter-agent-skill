# Kit Verification

Initial evidence was recorded on 2026-10-30. Separate records below cover the 2026-11-02 progressive-disclosure refactor and 2026-11-03 Spring AI routing checks. These checks validate the kit and its small contract fixture; application integration still belongs in each adopting project.

## Repeatable checks

```sh
python3 scripts/validate-kit.py
python3 -m unittest discover -s tests -v
mvn -f verification/pom.xml verify
```

Prerequisites and dependency setup are described in the source repository README. The Maven fixture uses Java 25, Spring Boot 4.1.2, and ModelMapper 3.2.8. Boot manages JUnit, Jackson, Hibernate Validator, Lombok, and core Maven plugins; the POM pins additional dependencies and quality plugins.

In the restricted authoring environment, Maven used the equivalent command with `-Dmaven.repo.local=/tmp/deconstruct-java-m2`. Dependencies were downloaded into that temporary cache. Offline follow-up checks used `-o` after provisioning.

## Initial executed evidence (2026-10-30)

| Check | Observed result |
| --- | --- |
| Python validator tests | 13 passed, including relocated paths, read-only CLI behavior, missing files, broken/escaping references, invalid skill metadata, and malformed XML/YAML. |
| Java contract fixture | 8 passed, zero failures/errors/skips. Real Jackson, Bean Validation, and ModelMapper exercised. |
| Spotless and Checkstyle | Conforming fixture accepted; Checkstyle reported zero violations. |
| Quality negative probe | A temporary class with wrong import order, a wildcard import, and a braceless `if` was rejected. Checkstyle reported all three; Spotless rejected the wildcard. Source files were unaffected. |
| Skill frontmatter validation | All three skills passed the skill-creator quick validator. |
| Relocated copies | Runtime and full layouts validated outside their directories; the full copy also passed Maven verification. |
| Recipe consistency | Maven quality plugin definitions in the integration recipe and executable fixture matched structurally. |
| Independent final review | No critical/important issues. A minor optional README-copy link gap was reproduced, documented, and rechecked successfully. |

The Java probes cover omission, nullable clearing under an existing null-skipping shared mapper, supplied values, forbidden null/blank names, inherited length constraints, create requiredness, internal presence metadata, and ordinary create conversion. The initial null-clearing probe failed with a copied per-TypeMap configuration; isolating the PATCH engine fixed that reproduced behavior without changing ordinary mapping configuration.

The fixture is test-only; Maven's empty-JAR warning is expected. Java 25 also reports deprecated Unsafe calls from the tested Lombok/ModelMapper dependencies. No full Java layout engine is installed by Spotless.

## Skill behavior checks

Each skill was evaluated independently against a small dry-run scenario, with a no-skill baseline recorded before authoring. These are decision checks, not generated-application integration tests.

- Bootstrap baseline chose feature packages, record DTOs, handwritten mapping, Flyway, and an assumed JWT boundary. With guidance, it chose responsibility packages, inherited DTOs, dedicated ModelMapper classes, Liquibase, and deferred unspecified product/provider choices. It excluded existing-project changes and React-only work from bootstrap routing.
- Change baseline preserved Gradle and handled presence but abandoned DTO inheritance. With guidance, it retained inheritance, moved create-only constraints into the appropriate child, used presence-aware update validation and isolated PATCH mapping, and preserved the existing error contract and Java baseline. It required real proxy tests rather than claiming plain unit tests proved interception. It excluded read-only review and Python-only implementation from this skill's trigger.
- Review identified controller/repository bypass, missing method security, ineffective transaction boundaries, misleading direct-construction tests, PATCH presence loss, and raw exception responses. It separated these defects from capability naming, dedicated mappers, unnecessary interfaces, inherited DTOs, and a derived-query preference. It excluded Python-only review and routed implementation to the change workflow. The no-skill baseline already found the main correctness bugs; the kit adds grounded convention checks rather than demonstrating new generic defect-detection ability.

## Portability and limits

Copy tests cover the documented runtime layout, including hidden skills, and the full maintenance layout under a differently named directory. Validation runs from outside the copy. Relative references resolve without the original checkout; optional Java fixture links are checked when that fixture is included.

The Python validator checks local inline Markdown link targets, heading destinations, and XML/YAML syntax. Heading checks support the kit's ATX headings and duplicate suffixes, ignoring fenced examples; arbitrary HTML anchors and other Markdown extensions are not covered. It does not check web-link availability, XSD validity, database execution, dependency security, or application semantics. It deliberately avoids unrelated target-project documentation and historical planning records.

No production database, container-backed migration/rollback, running server, actual service-security/transaction proxy, tracing transport, locale resolver, or live IntelliJ formatting was tested here. Those are documented conventions and integration responsibilities, not working features supplied by these fragments. The Java fixture cannot substitute for target-project MVC, persistence, security, or transaction tests. Use the target project's supported versions and real contracts when adapting it.

## Progressive disclosure refactor (2026-11-02)

The 10,698-word handbook was split into ten authoritative [topic guides](java-spring-guidelines.md), with a 365-word routing index. AGENTS.md remains 399 words. Skills retain their discovery metadata and contain 241–262 words; template adoption is routed through a 166-word index to focused recipes. The common working agreement dropped conditional infrastructure detail, which remains in the corresponding guides.

| Check | Observed result |
| --- | --- |
| Policy preservation | All 225 original policy blocks and 100 primary-source URLs were accounted for. Of those blocks, 223 retain their wording after whitespace/link normalization; two replace stale "below" pointers with direct cross-topic links while preserving the policy. This checks content preservation, not application behavior. |
| Validator regressions | Four new negative cases failed before implementation: missing topic guide, broken link inside a topic, missing target heading, and missing same-file heading. All 18 unit tests passed after the validator change, including duplicate-heading links. |
| Kit and relocation validation | Source, full relocated copy, and runtime-only relocated copy passed. Actual CLI checks ran from outside the copies; the runtime copy excludes maintenance files and the Java fixture. |
| Skill metadata | All three skills passed the skill-creator quick validator. |
| Maven verification | Offline verification using the provisioned temporary cache passed: 8 contract tests, zero failures/errors/skips, Spotless clean, and zero Checkstyle violations. |

Independent, read-only planning scenarios recorded actual content exposure before and after the initial split:

| Scenario | Before body reads | After body reads | Outcome |
| --- | --- | --- | --- |
| Inherited DTO PATCH | 5,497 words / 47,091 bytes | 3,739 words / 29,125 bytes | Preserved presence-aware validation, inherited constraints, dedicated PATCH mapping, and relevant verification without reading delivery guidance. |
| Minimal webhook bootstrap | 10,045 words / 81,198 bytes | 6,659 words / 51,063 bytes | Selected only requested capabilities; did not read persistence, operations, delivery, scheduling, or caching policy sections. |

Heading-only navigation is excluded from these body counts and was recorded separately. The original bootstrap attempted a whole-handbook read that was truncated; its before count includes only confirmed exposed content. The after runs completed without truncation. Paths chosen by independent agents differed, including whether optional probe source was inspected; these single samples demonstrate useful routing, not a controlled token benchmark or a guarantee about future models.

A separate Helm-only review correctly identified that availability settings require discussion with the owner before finalization, and did not read DTO/mapping or persistence guidance. Its initial run read the full application-testing guide; that observation led to conditional verification routing in the review skill and direct Helm/rollout/availability links in the index.

A fresh review of the same Helm proposal after that refinement read the four entry documents plus selected chart, rollout, health, shutdown, sizing, replica, and availability sections: 2,939 words / 23,396 bytes, with heading navigation counted separately. It did not read application-testing, mapping, or persistence guides, and retained the owner-discussion requirement and deployment-specific verification obligations.

Independent final review found no critical/important issues and identified a stale PATCH prose pointer left by the split. It was replaced with a direct DTO-validation link; a similar deployment pointer was corrected during the same navigation check. Both destinations pass heading validation. The reviewer independently confirmed policy/source preservation, required discussions, unchanged executable artifacts, unit checks, and runtime-copy portability.

## Spring AI disclosure and routing (2026-11-03)

The 2,524-word AI guide became a 365-word [router](guidelines/spring-ai.md), with focused [implementation](guidelines/spring-ai-implementation.md), [runtime/security](guidelines/spring-ai-runtime.md), and [evaluation](guidelines/spring-ai-evaluations.md) references of 1,421, 698, and 394 words. The handbook routes common AI tasks directly to those references. Root instructions and the three skill files were unchanged.

All 17 policy sections and 18 primary-source URLs were preserved. Policy comparison normalizes whitespace and Markdown link destinations; accepted policy prose was unchanged. Cross-topic links now target the owning guide, and the validator requires all four AI files.

Three [versioned scenarios and scoring criteria](../verification/skill-scenarios/README.md) were run before and after the split, each in an independent fresh context. Agents received skill discovery metadata and their task without the rubric or interview history. A temporary reader captured exact exposed guidance; [dated results](../verification/skill-scenarios/2026-11-03-results.json) retain read content, hashes, measurements, answer excerpts, and human scoring. The [complete answers](../verification/skill-scenarios/2026-11-03-answers.md) support independent re-scoring.

| Scenario | Before body reads | After body reads | Observed result |
| --- | --- | --- | --- |
| Prompt-only change | 2,960 words / 23,584 bytes | 2,836 words / 22,887 bytes | Kept resource-based prompts, existing contracts/model, and appropriate verification; read selected prompt/evaluation/permitted-data sections. |
| Evaluation/deployment gate | 3,715 words / 29,608 bytes | 3,494 words / 27,876 bytes | Kept local on-demand and main-push-only live evaluations; required matching revision/configuration evidence and blocked every nonpassing state across deployment workflows. |
| Unrelated Java fix | 2,817 words / 22,266 bytes | 2,860 words / 22,732 bytes | Selected the change workflow and focused Java tests; opened no AI guide in either layout. The larger handbook added 43 words. |

All three post-split runs met the scenario criteria. The prompt case also read permitted-data guidance for evaluation inputs; it did not load unrelated runtime topics. Heading-only navigation is counted separately in the result artifact. The general Testing section exposed its subsections in these runs. Counts exclude host/system context, automatically supplied root instructions, discovery metadata, tool formatting, and final answers. One sample per case/layout is a routing observation; optional reads differed, so these numbers are not a controlled token benchmark or a guarantee about future agents.

Kit validation and all 18 Python validator tests passed. Actual full and runtime-only copies validated from outside their relocated directories. Removing each AI guide in a temporary copy was rejected as a missing required artifact. No application model evaluation, deployment, or Java fixture behavior was exercised by this documentation/routing change.

Fresh independent review confirmed policy/source preservation, working links, routing scores against complete answers, captured-content hashes/counts, and passing validation/tests/relocation checks. Two evidence details were corrected: full answer transcripts were retained for re-scoring, and the prompt baseline's extra evaluation-gate read was made explicit. No findings remained. Source URL preservation does not establish current framework API correctness; bootstrap/review skill files had no independent before snapshots, while root instructions and the change skill were compared against captured content.

These behavioral checks did not generate an application, invoke a cloud service, or test a deployed workload. File organization and instructions guide selective reading; they cannot enforce a hard context budget.
