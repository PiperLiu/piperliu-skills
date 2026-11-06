---
name: idea-storm
description: Use when the user invokes idea-storm or wants divergent brainstorming, unconventional ideas, or free creative exploration across multiple perspectives. Not for converging on requirements or implementation plans.
---

# Idea Storm

Maximize the diversity, novelty, and surprise of ideas. Keep this a lightweight, single round of exploration.

## Workflow

1. Use the user's original topic and stated constraints. Ask questions only if the topic is impossible to understand.
2. Launch four independent subagents in parallel, configuring low reasoning effort through the actual agent interface whenever supported. Give each the same original topic and constraints, plus one perspective:
   - **Wild Thinker:** Challenge assumptions and propose outrageous, unconventional possibilities.
   - **User Observer:** Find overlooked needs, frustrations, desires, and counterintuitive pain points.
   - **Cross-Domain Thinker:** Borrow concepts from unrelated industries, science, and nature.
   - **Minimalist Inventor:** Find surprisingly simple, clever, low-resource solutions.
3. Ask each subagent for 5–8 distinct ideas, each with a short name and a concrete explanation. Keep their contexts independent; do not share other agents' answers before generation is complete.
4. Collect the results, remove near-duplicates, and combine complementary ideas without flattening unusual differences.
5. Present 10–15 interesting ideas grouped by theme, concisely and in the user's language. Highlight 2–3 especially surprising or promising directions and briefly explain their creative potential.
6. Invite the user to choose directions for further discussion; stop before planning implementation.

## Rules

- Prioritize divergence over feasibility. Do not reject an idea merely because it seems impractical, or turn the highlights into a feasibility ranking.
- Avoid generic suggestions; make the distinctive mechanism or twist clear.
- Do not start coding, writing specifications, scoring ideas, or automatically researching them.
- The four perspectives are defaults. Adapt them when doing so increases diversity for the topic, while retaining four distinct perspectives.

## Runtime Limits

- Request low reasoning effort for every subagent through supported parameters; prose instructions alone do not configure it. If effort overrides are unavailable, use a suitable lightweight model when available, and describe the limitation honestly.
- If fewer than four worker slots are available, run the four independent assignments in batches without sharing their answers. If subagents are unavailable, disclose this and use four separate perspective passes in the main agent; do not claim independent agents ran.

## Validation

Before presenting, check that all four perspectives contributed, near-duplicates were removed, and unconventional ideas survived synthesis. Report actual runtime limitations without claiming parallel execution or low effort that was not configured.
