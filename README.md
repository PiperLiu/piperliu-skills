# PiperLiu Skills

A curated collection of Agent Skills I actually use for software engineering, research, automation, and personal workflows.

This repository favors **small, practical, reusable skills** over large prompt collections.

## Goals

- Keep useful workflows reusable across projects.
- Prefer skills that have been tested in real work.
- Keep skills readable by both humans and coding agents.
- Avoid coupling skills to one specific agent whenever possible.
- Store durable instructions here instead of copying large prompts across repositories.

## Repository Structure

```text
README.md
AGENTS.md
LICENSE
.gitignore
templates/
└── skill-template/
    └── SKILL.md
skills/
├── be-zym/
│   └── SKILL.md
├── delta-transfer/
│   ├── SKILL.md
│   └── references/
│       ├── examples.md
│       └── method.md
├── explore-exploit/
│   └── SKILL.md
└── grill-me-batch/
    ├── SKILL.md
    └── assets/
        └── review.html
```

Each skill lives in its own directory and should contain a `SKILL.md`.

A skill may optionally include:

```text
scripts/
references/
assets/
examples/
```

## Skill Philosophy

A good skill should answer four questions:

1. **When should an agent use this skill?**
2. **What outcome should it produce?**
3. **What constraints must it respect?**
4. **How can the result be validated?**

Prefer concrete operating instructions over vague advice.

## Creating a New Skill

Copy the template:

```bash
cp -R templates/skill-template skills/my-new-skill
```

Then edit:

```text
skills/my-new-skill/SKILL.md
```

Keep the `name` short and stable. Make the `description` explain when the skill should be used.

## Available Skills

- [be-zym](skills/be-zym/SKILL.md): Apply Zhang Yiming-inspired habits of low ego, independent judgment, empathy, imagination, practical execution, and patient iteration when requested.
- [delta-transfer](skills/delta-transfer/SKILL.md): Infer the transferable improvement delta from a baseline A to a preferred counterpart B, then apply that direction to a new target C without copying B or erasing C's identity.
- [explore-exploit](skills/explore-exploit/SKILL.md): Balance exploitation and exploration when proposing design alternatives, combining evidence-backed approaches with informative experiments and bold creative directions.
- [grill-me-batch](skills/grill-me-batch/SKILL.md): Batch high-leverage design decisions into a self-contained local HTML review form, collect one copyable feedback payload, iterate only on unresolved dependencies, and require explicit approval before implementation.

## Example

```yaml
---
name: explore-exploit
description: Balance exploitation and exploration when proposing candidate solutions during collaborative planning, design, or creative ideation.
---
```

## Naming

Recommended:

```text
lowercase-kebab-case
```

Examples:

```text
explore-exploit
release-checklist
research-benchmark
aws-bounded-run
github-issue-handoff
```

## Compatibility

The repository intentionally uses a simple `SKILL.md` layout so skills can be adapted for multiple agent environments instead of being tightly coupled to one product.

## Install

Clone the repository:

```bash
git clone https://github.com/PiperLiu/piperliu-skills.git
```

Or use individual skill directories in whichever agent/tool supports local or repository-based skills.

## Contributing

This is primarily a personal curated repository, but issues and pull requests are welcome when they improve clarity, portability, or correctness.

## License

MIT.
