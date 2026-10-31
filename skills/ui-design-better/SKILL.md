---
name: ui-design-better
description: Design, implement, improve, or review websites, apps, workspaces, and UI components with a coherent visual identity, purposeful motion, and clear product language. Use when visual hierarchy, interaction design, design direction, or UI quality requires judgment, including screenshot recreation and UI redesign. Do not expand a fully specified text or style edit into a redesign, or use for backend-only work, standalone video editing, or unrelated prose writing.
license: MIT; see THIRD_PARTY_NOTICES.md.
---

# UI Design Better

Make interfaces whose structure, imagery, language, and behavior belong to their product. Aim for the completion and character of excellent work in that category. A functioning template is a starting point; an unusual surface is not sufficient either.

**Be ambitious about expression and precise about consequences.** Quiet, exuberant, spare, dense, raw, and meticulous work can all succeed. Choose deliberately, then carry that choice through the whole experience. Preserve the surprising part when refining it.

## How to apply the guidance

There are three levels of instruction:

- **Requirements:** preserve the user's scope and locked choices; communicate facts honestly; keep essential content readable and actions usable; verify claims with appropriate evidence. Aesthetic ambition does not excuse misleading states, lost input, or inaccessible essential controls.
- **Defaults:** useful starting points for hierarchy, candidate exploration, timing, typography, and implementation. Change them when the product, existing system, or observed result gives a better reason.
- **Creative prompts:** ways to discover possibilities, not a catalog of permitted styles. Combine, replace, or go beyond them.

Numbers in the references are tuning ranges, not universal laws. No font, color, layout, medium, or motion technique is banned merely because it is common. No project owes this skill a hero animation, exactly three concepts, a single CTA across an entire dashboard, a new design system, or a particular library. Judge the relationship between the choice and its purpose.

Follow the user's language in conversation and the audience's language in the interface. The skill's English instructions do not prescribe English UI text.

## Match the work to the request

| Request | Appropriate response |
| --- | --- |
| Exact local edit | Make it directly. Check the changed region and neighbors when appearance can change. Skip concept documents and broad audits. |
| New interface or substantial redesign | Establish the task, explore internally, choose a direction, build a representative slice, then refine with real evidence. |
| Compare directions or layouts | Produce a few genuinely different, equally viable previews with comparable content; include the existing version when relevant. |
| Extend or polish an existing product | Inspect its tokens, shared components, navigation, and behavior. Repair at the source and preserve its identity unless redesign is requested. |
| Recreate a screenshot | Match its viewport, proportions, typography, and crop. Do not reinterpret it as a new art direction. |
| Review only | Deliver located observations, consequences, and actionable recommendations. Do not change product files or implement the recommendations. |
| Design brief or static mockup only | Deliver that artifact. Distinguish proposed behavior from behavior that has actually been implemented and tested. |

Do not introduce a mandatory approval pause. Ask when a material decision is unresolved; otherwise execute within the authority already given. A chosen direction is a constraint to deepen, not an invitation to reopen exploration.

## 1. Find the product's center

Inspect the request, relevant code and screens, brand assets, and project design conventions. Establish:

- who uses it, in what situation, to accomplish what;
- the actual objects, content, prices, data, and rules the UI must carry;
- the main device, input methods, supported viewport range, and environment;
- existing assets, technical constraints, accessibility requirements, and delivery format;
- what is fixed, what can change, and what remains unknown.

Do not borrow facts from reference products. Ask a focused batch of questions only when missing information changes the core solution and cannot be inferred. Make reversible local decisions yourself.

For the current screen or task, identify the leading object or information and the leading action. Map **action → object change → visible feedback → next state**. Prioritization is contextual: several legitimate workflows can coexist, but users should understand which one matters now.

Remove, merge, or demote competing decoration, repeated explanation, and equal-weight secondary actions. Preserve object names, decision evidence, current state, and the information needed to act. Subtraction should strengthen the useful content, not merely empty the page.

## 2. Choose an expressive direction

For substantial new work, read [Direction and composition](references/direction.md). Separate references for product identity from references for interaction behavior. Inspect actual examples where possible, extract why they work, and adapt the relationships to this product.

Explore alternative mechanisms internally before settling on the first plausible layout. One candidate should grow directly from a distinctive object, process, or user action in the product. Alternatives can be sketches or short descriptions; do not build several entire products to think clearly.

Write a compact design intent, in an existing project document or working notes:

> Audience and task; desired first impression; leading object and action; composition; typography and color roles; key media; interaction/result; memorable moment; constraints and things deliberately omitted.

Translate words such as “premium,” “simple,” or “playful” into visible and behavioral decisions. Make the essential grouping and operation work without relying on decoration; a quick grayscale sketch is useful when structure is uncertain. Color can still carry legitimate semantic information, with another cue for essential states.

Recommend and deepen one direction unless comparison is requested or would resolve a meaningful uncertainty. When comparing, vary structure, visual center, typography, media, or interaction rather than generating color skins. Keep all candidates appropriate and feasible. Let user feedback guide selection; avoid averaging away their strongest qualities.

## 3. Compose the real interface

Read [Visual and interaction language](references/visual.md) for substantial visual work. Use real content early and choose a structure suited to the task:

- **Persuasion:** make the product, its concrete value, and the next action understandable. Show what the product actually delivers. Design the composition before defaulting to a headline–paragraph–button template.
- **Work and browsing:** put the objects, first useful content, or work surface in view. Let secondary details appear in context. A large slogan should not displace the work.
- **Mobile:** compose for reach, reading order, safe areas, and the current step. Reconsider the task hierarchy rather than squeezing desktop columns together.
- **Play and tactile tools:** identify the distinctive objects, input thresholds, visible states, and core loop. The process itself may be the experience.

Create only the tokens and component rules needed now. Carry the chosen language through tables, forms, overlays, loading, empty, error, and completion states, and through the end of a long page. Build one representative page or end-to-end slice before spreading the system.

Read [Media and rendering](references/media.md) when assets carry meaning or character. Choose or create pivotal imagery early enough to compose around it. Keep text, data, focus, and interactive controls in semantic UI rather than baking them into images or video.

## 4. Give behavior a legible form

Read [Interface motion](references/motion.md) when designing transitions, gestures, entrances, or scroll narratives. Cover immediate action feedback and understandable state changes; consider a coordinated first entrance when it helps. Static feedback or a deliberate cut can be the right solution.

Choose one or two moments where the product's own action becomes unusually satisfying or explanatory. Show the affected object changing, not just a button performing. Motion should connect cause and result, preserve identity and orientation, and yield to new input.

Use CSS, SVG, native APIs, the project's animation system, or real-time rendering for precise geometric changes. Read [Generated motion and runtime](references/generated-motion.md) only when video or frame sequences must carry changing anatomy, structure, material, occlusion, or a predetermined camera journey. This skill supplies design and acceptance criteria, not bundled generation services or media-processing scripts.

Read [Product language](references/tone.md) when writing or revising headings, explanations, onboarding, errors, and product narrative. Copy and layout should clarify the same task; do not fix weak meaning by making the words smaller.

## 5. Verify, refine, and deliver

Read [Review and validation](references/validation.md) for substantial new work, redesign, or a requested audit. Treat visual quality and task completion as separate questions.

Look at the running result at its intended reading size. Inspect the main state, the highest-risk relevant state, and another representative viewport when supported. Check a long page's full rhythm. Screenshots must actually be viewed; successful capture and valid source code do not establish visual quality.

Operate the main path from entry to observable result. For affected persistence, test save and read-back; for failure, test recovery and retained context. Test relevant fast reversal and reduced-motion behavior. Match verification depth to the change and run appropriate project checks.

Review in this order: task blockers and false states; readability; hierarchy and identity; spacing and detail; motion quality; redundant content. If the composition or media premise is wrong, revisit it instead of decorating around it. Keep the distinctive choices that still serve the goal.

Independent review is useful when available and authorized, especially for substantial work; it is not a prerequisite for making progress. Give a fresh reviewer current evidence, the task and constraints, without your defense or past scores. Label self-review accurately. Stop when meaningful defects are resolved or further changes are only preference churn; do not chase a numeric score indefinitely.

Keep drafts and evidence in the project's working area, final assets in production locations, and references valid. Do not store task output inside the skill. Finish with the result, consequential choices, what was verified, remaining limitations, and relevant artifact or evidence links. Do not claim visual, interaction, performance, or independent-review validation that did not occur.
