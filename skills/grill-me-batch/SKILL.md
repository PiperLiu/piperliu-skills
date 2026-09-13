---
name: grill-me-batch
description: Use before implementing a non-trivial feature, refactor, architecture change, or project when the user wants the design challenged and clarified without serial one-question-at-a-time chat. Inspect the available artifacts first, batch the material decisions into a self-contained local HTML review form with recommended options, collect one copyable feedback payload, iterate only on unresolved dependencies, and do not modify project code until the user explicitly approves the final design.
---

# Grill Me Batch

Turn a vague or partially specified implementation request into a decision-complete design without forcing the user through a long serial interview.

The core contract is **design first, implementation later**. During the grilling phase, inspect and reason freely, but keep the target project read-only. Generate local review artifacts outside the project. Implementation starts only after the design is settled and the user gives an explicit final approval in a later turn.

## Use When

Use this skill when:

- the user asks to “grill” or stress-test a design before coding;
- a feature or refactor has several product or engineering decisions that require user judgment;
- the user wants questions collected into a form instead of being asked one at a time;
- a plan needs explicit agreement before implementation begins.

Do not use it when:

- the task is trivial and has no material design choices;
- the user has already supplied a decision-complete specification and explicitly wants immediate implementation;
- the remaining uncertainty is purely factual and can be resolved by inspecting files, documentation, tools, or tests.

## Non-Negotiable Implementation Gate

Until the gate opens:

- Do not edit implementation files in the target project.
- Do not create migrations, production configuration, generated code, or commits for the target change.
- Do not interpret “implement it after we agree” as present approval.
- It is fine to read the codebase, run read-only inspection, search documentation, and create temporary HTML review files outside the project.

The gate opens only after:

1. the material design decisions are settled;
2. you present a final design / implementation plan;
3. the user explicitly approves implementation after seeing that final plan.

Do not present the final plan and implement it in the same assistant turn.

## 1. Inspect Before Asking

Read the conversation and inspect the in-scope project before generating questions.

Separate unknowns into:

- **Facts** — discoverable from code, files, docs, tools, history, or external references. Resolve these yourself when access is available.
- **Decisions** — choices that depend on the user's desired behavior, priorities, risk tolerance, scope, or product intent. Ask the user.
- **Assumptions** — material beliefs that are neither verified facts nor explicit decisions. Convert them into research or decisions.

Never ask the user for a repository fact you can safely discover yourself.

## 2. Build a Decision Map

Identify the smallest set of material decisions required to make the design implementation-ready.

Useful dimensions include, when relevant:

- goal and success criteria;
- scope and explicit exclusions;
- user-visible behavior and UX;
- data ownership, persistence, and state transitions;
- interfaces and integration boundaries;
- compatibility and migration behavior;
- failure modes and recovery;
- performance, privacy, and security constraints;
- test and acceptance behavior;
- rollout, observability, and operational ownership.

Skip dimensions that do not matter for the task.

For each decision, assign a stable short ID such as `scope-1`, `ux-2`, or `migration-1`. Track which decisions depend on earlier choices.

## 3. Batch by Decision Frontier

Do not ask questions serially when they can be answered independently.

A review round should contain the complete set of **currently answerable material decisions**: questions whose answers do not depend on another unanswered question in the same round.

Before adding two questions to the same round, ask:

> Could a plausible answer to question A remove question B, materially change B's wording or options, or change which answer I recommend for B?

If yes, B is downstream and belongs in a later round.

Do not artificially limit the number of independent questions. Also do not pad the form with low-value stylistic choices that can be decided during implementation.

## 4. Write Good Questions

Each question must contain:

- `id` — stable across rounds;
- `category` — short grouping label;
- `question` — one decision in plain language;
- `context` — why the decision matters and the consequence of choosing differently;
- `type` — `single` or `multi`;
- `options` — concrete choices with concise trade-offs;
- at least one recommended option.

For a `single` question, recommend exactly one option. For `multi`, recommend the combination you believe best fits the evidence.

Do not hide behind “it depends.” Give the strongest current recommendation and explain the trade-off briefly. The user can reject it.

Every question must still allow:

- **Other** — a custom answer outside the proposed options;
- **Additional comments** — free-form nuance that overrides an option when they conflict.

Prefer concrete options over free-form-only questions. If the option space seems too broad, research it first and present the best useful choices you can identify.

## 5. Generate the HTML Review

Use `assets/review.html` from this skill directory as the template.

Replace the single placeholder `__MODEL_JSON__` with JSON shaped like:

```json
{
  "id": "stable-topic-id-round-1",
  "title": "Short design review title",
  "topic": "One sentence describing what this round settles.",
  "round": 1,
  "lang": "en",
  "settled": ["Concise decision already settled"],
  "questions": [
    {
      "id": "scope-1",
      "category": "Scope",
      "question": "Which behavior belongs in the first release?",
      "context": "This changes the implementation boundary and acceptance tests.",
      "type": "single",
      "options": [
        {
          "label": "Core path only",
          "detail": "Smaller first release; defer advanced cases.",
          "recommended": true
        },
        {
          "label": "Core + advanced cases",
          "detail": "Broader first release; more implementation and testing cost.",
          "recommended": false
        }
      ]
    }
  ]
}
```

Set `lang` to `zh-CN` for a Chinese conversation; otherwise use `en` unless another language is clearly appropriate.

### Artifact rules

- Write the generated form to the OS temporary directory, never into the target project by default.
- Suggested filename: `grill-me-batch-<topic>-round-<n>.html`.
- Keep it fully self-contained and offline: no CDN, remote fonts, analytics, network requests, or build step.
- JSON-encode the model safely. When inserting it into the inline script, escape `<`, `>`, and `&` as Unicode escapes so user/project text cannot terminate the script tag.
- Open the file with the platform's normal local-file opener when available (`open`, `xdg-open`, or `start`). Otherwise give the absolute path.

The bundled template provides:

- recommended answers pre-selected;
- radio / checkbox choices;
- an `Other` answer per question;
- an additional-comments box per question;
- a global-notes box;
- local browser persistence for unfinished review state;
- a live feedback preview;
- **Copy feedback** with a clipboard fallback;
- a reset-to-recommendations action.

Tell the user that recommendations are pre-selected: they should change anything they disagree with, add nuance where useful, then click **Copy feedback** and paste the result back into the chat.

Do not ask additional design questions in chat while a review form is pending.

## 6. Process the Returned Feedback

The copied payload is deliberately plain text and includes stable question IDs.

When it returns:

1. Apply every selected answer to the decision map.
2. Treat an additional comment as authoritative when it conflicts with a selected option.
3. Treat an unanswered material decision as still open; do not silently decide it unless the user explicitly delegated that choice.
4. Add new decisions exposed by the answers.
5. Prune branches made irrelevant by settled choices.
6. Resolve any new factual prerequisites yourself.
7. Compute the next decision frontier.

If material decisions remain, generate another HTML round containing only the newly answerable unresolved decisions. Do not restart the entire interview.

Use a normal chat follow-up only for malformed feedback or a tiny ambiguity that cannot reasonably justify another review round.

## 7. Close the Design

The design phase is complete when:

- every reachable material decision is settled or explicitly deferred;
- no material assumption remains hidden;
- remaining facts are known or clearly identified as implementation-time verification;
- the implementation boundary and acceptance behavior are clear enough that another competent agent could implement without inventing product decisions.

Then present a concise final design containing:

1. goal and success criteria;
2. agreed scope and exclusions;
3. key behavior and architecture decisions;
4. important failure / migration / compatibility behavior;
5. acceptance and validation plan;
6. explicitly deferred work and remaining risks.

End by asking for explicit implementation approval.

Do **not** implement in that turn.

## Quality Check

Before each HTML round, verify:

- [ ] Facts were researched instead of delegated back to the user.
- [ ] Every question represents a material decision.
- [ ] No question in the round depends on another unanswered question in that same round.
- [ ] Every question has concrete options, useful trade-offs, and a recommendation.
- [ ] The generated HTML is outside the target project and requires no network.
- [ ] The feedback payload tells the receiving agent to continue design only, not implementation.

Before opening the implementation gate, verify:

- [ ] The final plan reflects the returned feedback rather than the original assumptions.
- [ ] Deferred decisions are explicit.
- [ ] The user has seen the final plan.
- [ ] The user gave a fresh, explicit approval to implement.

## Prior Art

This workflow is conceptually related to Matt Pocock's `grill-me` / `grilling` approach and to public HTML questionnaire / batch-grilling experiments in the Agent Skills ecosystem. This implementation intentionally keeps the interaction portable: a local offline HTML file plus a copy-and-paste handoff, with no dependency on a particular browser multiplexing environment or agent-specific UI.
