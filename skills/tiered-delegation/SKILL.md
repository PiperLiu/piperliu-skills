---
name: tiered-delegation
description: Split work between a scarce, high-judgment agent (director) and abundant worker agents on a different quota, such as Codex CLI. Use when the current model or account has limited credits, a task needs heavy implementation, testing or repetitive verification, or the user asks to "let Codex do it", delegate, or save premium credits.
---

# Tiered delegation

Spend the scarce model on judgment and the abundant model on labor. The director decides **what** and **whether it is good**; workers do **how**, repeatedly and cheaply.

## Who does what

| Director (scarce: premium model / limited account) | Worker (abundant: e.g. Codex on a Pro account) |
|---|---|
| Diagnose the real problem; read the evidence that matters | Bulk reading, searching, extracting from logs |
| Architecture, interfaces, acceptance criteria | Implementation, refactors, tests, fixtures |
| Taste-critical text: guidance, prompts, names, user-facing copy | Docs that follow a given spec; registration, wiring |
| Accept or reject: run the result on real data, look at it | Build, lint, test, fix-until-green loops |
| Report to the user | Commit and push when the brief allows |

Do the work yourself only if it is taste- or judgment-critical, or if writing the brief would cost more than doing it (roughly five tool calls or fewer).

## The loop

1. **Diagnose first.** Find the root cause before delegating. A worker given a symptom will polish the symptom.
2. **Write the critical part yourself** if quality depends on judgment (principles, guidance, the one tricky algorithm). Tell the worker those files are fixed except for mechanical edits.
3. **Write a bounded brief** (template below). The brief is the whole context; the worker has not seen your conversation.
4. **Launch the worker in the background**, then do independent work or wait. Don't poll in a tight loop.
5. **Accept on real data.** Read the worker's summary, check `git log`/diff stats, then run the new thing once on a real case. Tests passing is not acceptance. Unit tests miss false positives, output bloat and wrong defaults.
6. **Send a narrow fix brief** for what acceptance found: specific cases, expected behaviour, and the same bounds. One or two of these rounds is normal.
7. **Report** what changed, what was verified and what was not.

## Brief template

```markdown
# Brief: <task> (bounded)
Repo: <absolute path>, branch <b>, push to <remote>? yes/no

## Context
<the root cause in 3–6 lines; concrete failing examples>

## Fixed files (do not rewrite content)
<paths the director wrote>

## Build
<numbered deliverables with concrete behaviour, names, thresholds, input/output shapes>

## Rules
- Tests for each piece; <verify command> must pass.
- Bounded: one implementation pass, then at most N fix rounds for failing tests.
- Do NOT: launch sub-agents, run long renders/probes, iterate on aesthetics, refactor unrelated code.
- Commit with message + required trailer, push, STOP.
- Final message: files changed, commands as implemented, test counts, what was skipped.
```

## Hard-won rules

- **Bound every run.** Use explicit round limits and a stop condition. An open-ended "improve, verify, repeat" loop burns the worker's quota on re-verification without converging.
- **No self-review loops of aesthetics by the worker.** Judgment stays with the director; the worker gets concrete criteria.
- **Concrete over abstract.** Give thresholds, examples and a reference implementation if one exists, copied to a stable path rather than `/tmp`.
- **Small outputs.** Ask tools to print compact summaries by default (full detail behind `--full`). Large outputs waste the director's context when it accepts the work.
- **One worker per independent job.** Parallelize only if the jobs touch different files.
- **Keep artifacts outside the repo**: briefs, logs and results go in a session folder. Only the deliverable gets committed.
- **Verify persistence**: confirm the commit is pushed (`git status -sb` shows no ahead/behind).

## Worker harnesses

- Codex CLI on macOS: see [references/codex-cli.md](references/codex-cli.md).
- Other harnesses follow the same pattern: non-interactive mode, explicit model and effort, sandbox that permits the needed writes, brief from a file, last message to a file, log to a file.
