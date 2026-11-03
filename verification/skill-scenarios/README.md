# Skill Routing Scenarios

Use [the scenario dataset](spring-ai-routing.json) to check task-specific guidance selection after changing skills or handbook routing. These are read-only agent planning exercises; no application or live provider calls are required.

For each case, start a fresh agent context with the target repository location, the case's `prompt`, and only the three repository skills' discovery metadata. Let the agent select the applicable skill and references. Keep `criteria` hidden until scoring. Do not preload the handbook, topic bodies, other cases, or interview history.

Ask the agent to report its selected skill, planned change, verification, and all files/sections read. Capture actual read content or tool transcripts; distinguish heading navigation from policy-body reads. Check each criterion against both the answer and the reads. Record failures and unavailable evidence explicitly. A focused cross-link read, such as permitted-data handling for evaluation inputs, is relevant when the plan actually uses that boundary.

For layout comparisons, run the same cases before and after the change in independent contexts. Preserve prompts, observed answers, read records, and scoring with a dated result. Report exact exposed word/byte counts only when captured; do not describe a single run as a token benchmark or reliability guarantee. See the [2026-11-03 captured results](2026-11-03-results.json) and [complete answers](2026-11-03-answers.md).

The Python validator suite checks artifacts, references, and relocation. It does not execute these agent scenarios. Application tests and model-backed workflow evaluations remain separate under the [AI evaluation policies](../../docs/guidelines/spring-ai-evaluations.md#testing-and-evaluations).
