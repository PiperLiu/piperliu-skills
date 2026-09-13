# Repository Instructions

This repository contains reusable Agent Skills.

## Principles

- Do not add a skill only because an idea sounds useful.
- Prefer skills backed by repeated real-world use.
- Keep each skill narrowly scoped.
- Avoid project-specific secrets, credentials, hostnames, account IDs, private URLs, or personal data.
- Prefer portable instructions over agent-specific syntax.
- Keep examples generic unless the example itself is the subject of the skill.

## Editing Skills

When modifying a skill:

1. Preserve the front matter.
2. Keep the skill name stable unless there is a strong reason to rename it.
3. Make the trigger condition explicit in the `description`.
4. Separate required behavior from optional guidance.
5. Include validation criteria for operational skills.
6. Avoid unnecessarily long background explanations.

## Adding Scripts

Scripts should be:

- deterministic where practical;
- safe by default;
- explicit about destructive operations;
- easy to run locally;
- documented from `SKILL.md`.

Do not commit generated caches, secrets, large binaries, or local environment files.

## Pull Request Standard

A skill change should explain:

- why the skill exists;
- what recurring problem it solves;
- what changed;
- how the skill was validated.
