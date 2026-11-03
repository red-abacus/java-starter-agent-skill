# Spring AI Testing and Evaluations

Read when: Changing AI workflow tests, evaluation datasets, execution triggers, or deployment gates.

Use only relevant sections. [Spring AI index](spring-ai.md#sections); [handbook index](../java-spring-guidelines.md).

## Sections

- [Testing and evaluations](#testing-and-evaluations)
- [Evaluation execution and deployment gates](#evaluation-execution-and-deployment-gates)

## Testing and evaluations

Use a layered strategy. Keep ordinary application tests independent of live model calls under the existing [Java testing conventions](testing.md#testing). Verify prompt rendering, DTO validation, authorization, tool execution, and error handling with appropriate substituted collaborators and boundary tests.

Maintain a small, versioned evaluation dataset per AI workflow, including inputs, context, expected outcomes, edge cases, and discovered regressions. Run evaluations against the actual selected model and prompts to assess workflow behavior. Apply the [permitted-data controls](spring-ai-runtime.md#untrusted-content-and-permitted-data) to evaluation data and grader calls too.

Prefer programmatic checks for measurable outcomes, such as extracted fields, valid references, and correct tool arguments. Use model-based graders for semantic quality where useful, with explicit rubrics calibrated against human-reviewed examples. Define acceptance criteria per workflow, and avoid requiring exact wording for free-form answers.

Record the model, prompt revision, dataset, generation settings, and grader configuration with results. Spring AI evaluators can support relevance or contextual factual-support checks alongside application-specific checks; a grader result does not establish correctness beyond the criteria and cases actually evaluated.

## Evaluation execution and deployment gates

Use tiered execution: run ordinary application tests in regular CI and keep evaluation commands and configuration in the repository so they can also run locally. Model-backed evaluations run locally on demand and in CI only on pushes to `main`. Do not add live-model evaluations to pull-request checks, scheduled runs, or other CI triggers by default.

Require passing model-backed evaluations before deploying an application revision with AI capabilities. Evaluation failure blocks deployment. Associate the evidence with the exact revision being released and its recorded model, prompt, dataset, and grader configuration; success for an unrelated revision does not satisfy the gate. A failed, skipped, canceled, or unavailable evaluation is not a passing result.

Define evaluation scope, acceptance criteria, execution budgets, and the concrete job dependencies per project, reusing the settled trigger and deployment-blocking rules. Keep quality failures distinguishable from provider or infrastructure errors in the reported results. Verify the gate in the actual release path, including when evaluation and deployment use separate workflows.

## Primary references

Consult documentation matching the target project's versions when verifying framework behavior.

- [Spring AI evaluation testing](https://docs.spring.io/spring-ai/reference/api/testing.html)
