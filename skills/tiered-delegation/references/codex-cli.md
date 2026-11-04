# Codex CLI as a worker (macOS)

## Command

```bash
RUN=~/path/to/session-folder      # outside the repo
codex exec \
  -m gpt-6.1-sol \
  -c model_reasoning_effort='"xhigh"' \
  -c approval_policy='"never"' \
  -s danger-full-access \
  -C /absolute/repo \
  -o "$RUN/result-<task>.md" \
  - < "$RUN/brief-<task>.md" > "$RUN/log-<task>.txt" 2>&1
```

- `-` reads the prompt from stdin, so the brief can be long markdown without quoting problems.
- `-o` writes only the final message. Read it first; open the log only if something failed.
- `-c` values are TOML: strings need inner quotes (`'"xhigh"'`).
- Run it in the background (async shell, or `&` with the PID noted) so the director can keep working. A typical bounded job takes 5–20 minutes.
- Check `codex --version` and `codex exec --help` if flags fail; the CLI changes often.

## Model and effort

- Engineering with tests: a strong coding model at `high`, or `xhigh` for design-heavy tooling.
- Narrow fix rounds: `high` is enough.
- Use whatever models the account lists. Prefer the strongest available for anything with judgment; cheaper or "lite" models produce visibly worse work on open-ended tasks.

## Sandbox

- `workspace-write` blocks writes to `.git` (no commit/push) and to some dot-directories such as `.agents/`. Use it only for jobs that don't commit and don't touch those paths.
- `danger-full-access` is needed to commit, push, or write dot-directories. Use it only with a bounded brief in a repo you own.
- Network may be needed for `git push` and package installs; `danger-full-access` allows it.

## Monitoring

- Don't tail the log in a loop. Wait for completion, then read the `-o` file.
- Check that it started: after about a minute the log should show it reading files. An empty log usually means a CLI error, such as a bad flag or auth.
- To stop a runaway job, `kill <pid>` it and its children. Kill by PID, not by name.

## Reading past Codex sessions

- Sessions are stored at `~/.codex/sessions/YYYY/MM/DD/rollout-*-<thread-id>.jsonl`. A `codex://threads/<id>` link maps to the file ending in that id.
- The files are large. Extract with a script instead of reading them directly:
  - user prompts: `type=="response_item"`, `payload.type=="message"`, `payload.role=="user"`;
  - tool calls: `payload.type` in `custom_tool_call` / `function_call`, with code in `payload.input` / `arguments`.
- Use these to diagnose why a worker or a user session went wrong: which docs it read, which tools it skipped, and what it improvised.

## Pitfalls seen in practice

- **Autonomous "director" runs** (improve → verify → commit → probe → review, unbounded) produce some good commits, then loop on verification. Give them a fixed number of rounds and a stop condition, or split them into separate briefs.
- **Clean-context probe agents** are expensive and slow to evaluate. Prefer one real run checked by the director.
- **Tools that pass tests but fail on real data**: false positives, output that is far too large. Always run the new tool once on a real case before accepting.
- **Machine paths leaking into repos**: forbid absolute local paths in committed files if the repo must be portable, and run its portability check if one exists.
