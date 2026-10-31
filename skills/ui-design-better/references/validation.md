# Review and validation

Read for significant implementation, redesign, or a requested review. Scale evidence to the claim and the risk; avoid ritual screenshots and endless polish loops.

## Establish the relevant baseline

For existing products, distinguish visual cleanup, page restructuring/state repair, and workflow change. Preserve business contracts, data semantics, validation, permissions, route parameters, and existing useful actions outside the requested change. A new feature or flow fix ordinarily inherits the visual language; a visual redesign may revisit accidental defaults while retaining locked brand assets.

Capture or inspect the current representative screen and operate the affected path. Inspect shared tokens/components before patching instances. Prove one representative slice, then propagate the resolved language. Update the existing design document when durable conventions emerge; distinguish inferred conventions from user-approved rules. Do not create a duplicate system or rewrite unrelated code.

For screenshot recreation, match logical viewport, content, crop, and state before comparing. Prioritize large regional differences and alignment before small effects. Clearly distinguish reproduced areas from extrapolated ones.

## Gather enough actual evidence

- At 100% reading size, inspect the main view and relevant text with the actual fonts loaded. Use thumbnails for visual mass, not legibility.
- For a long page, inspect the whole sequence and ending. A polished hero does not establish a polished page.
- Enlarge or crop a dense region around 200% when needed to expose alignment, doubled borders, icon weight, and inconsistent padding. Return to actual size to judge reading.
- Blur or mask text, or view a small thumbnail, to check focal weight, distribution, and repetitive blocks. Do not mask away the imagery being evaluated.
- Include the main state and the highest-risk affected state: perhaps long content, empty results, error/recovery, an open overlay, or completion. If one state covers both, reuse it.
- If the product supports another class of device, inspect a representative state there. Walk the full flow on both only when the input or task behavior differs materially.
- Use observable readiness rather than an arbitrary wait for async behavior. Check that canvas/WebGL output is nonempty and assets actually loaded.

Re-capture changed evidence, reuse unaffected evidence, and avoid expanding into every language × page × state × viewport unless specific risks justify it. Shared styles may broaden the affected area. Repeating captures without changing or learning anything is not validation.

Dynamic behavior needs operation, sequence frames, or a playable recording appropriate to the claim. A sequence reveals states and ordering; judging real-time feel requires real-time observation. A saved screenshot is not an inspected screenshot. Source code, build output, and a reviewer's report cannot replace the observations they do not contain.

## Verify the task separately

Start at a real entry, make inputs, trigger the action, and observe its result. A URL that directly displays a success state is useful for visual inspection but does not test submission.

For affected persistence, save and read back after refresh/re-entry. For failure, confirm retained input, useful feedback, and recovery. For balances, limited attempts, charging, or rewards, check exhaustion and duplicate activation when relevant. For navigation, check return context; for dragging, check threshold, cancellation, and scroll coexistence. Test overlay focus and primary-action visibility with a mobile keyboard when that is a real risk.

Run relevant existing verification and appropriate type/lint/build/tests according to project requirements and the change. Do not prescribe a universal build ban or demand a whole suite for a cosmetic edit. Repeat tests when a change or observed intermittent failure justifies it, not merely because a feature is asynchronous or random. Report environmental blockers; investigate only as needed to complete the authorized deliverable, without silently changing unrelated authentication or configuration.

## Review criteria

| Question | Evidence and desired outcome |
| --- | --- |
| Is the task truthful and operable? | Real action reaches a real result; no false success, input loss, duplicate commitment, or unrecoverable failure |
| Can people read and act? | Actual-size text, visible primary action, reachable controls, sensible focus and state cues |
| Is the center apparent? | The important object and next action are identifiable without reading every label |
| Does the expression belong here? | Product-specific composition/media or legible domain relationships, with coherent identity |
| Is it resolved throughout? | Detail, spacing, type, surfaces, secondary states, and ending meet the same quality level |
| Does movement clarify? | Feedback, direction, continuity, interruptibility, reading rests, and appropriate fallback |
| What can be removed? | Redundant copy, decorative data, duplicate containers, and explanation that adds no understanding |

A three-second look is a useful diagnostic for first impression and focal hierarchy, not a timed usability study. Replacing the name with an unrelated product is a useful test of generic marketing, but efficient category conventions in a tool are not a defect. Look for meaningful business relationships and exception priority rather than demanding an ornamental hero in every application.

Do not treat quiet taste as a universal standard. Distinguish observable defects from preferences. A review should improve the chosen direction, preserve its strongest decisions, and say when no meaningful defect was found. Do not add features or invented data merely to make a design feel more real. When proposing another element, consider what must yield space or attention.

## Fresh perspective, when available

Independent review can counter attachment to the implementation. Use it only when available and authorized; self-review is a valid fallback and should be labeled accurately.

A visual reviewer needs current screenshots or an operable page, original task, viewport, hard constraints, and the design intent in one sentence. Existing-product polish also needs the existing design rules. Do not provide the source code, a defense of the design, or prior scores as substitutes for evidence. The reviewer should not modify files during a review-only pass.

A fresh UX walkthrough can instead start from the entry page, necessary test materials, device context, and side-effect boundaries, without a supplied expected path. Ask the reviewer to infer the likely task and trace one important path. Record “what was visible → why that action seemed appropriate → what happened,” distinguishing blocked, mistaken, and uncertain steps. Separate observations, suspected causes, and desired outcomes. Reproduce suspected defects and exclude tool/test-data failures before changing the product.

These are different review questions. An inferred walkthrough does not replace a specified functional check. An agent is not a representative user sample and cannot establish human success rate, satisfaction, or time savings. Only claim an independent review when an actual independent execution occurred.

## Repair and stop

Prioritize task/data failures, unreadable content, and misleading states before aesthetic refinements. Then address hierarchy/identity, detail, motion, and subtraction. Write findings with a location, observation, consequence, desired result, and verification method. A short list of the highest-impact issues is more useful than an unranked inventory. Preserve one or two defining strengths explicitly.

If the central composition or key media is fundamentally inappropriate, return to that premise. Small border and spacing improvements cannot rescue the wrong structure. Otherwise make targeted changes rather than replacing a coherent direction with the reviewer's preferred style.

Treat automated contrast, small-text, long-line, heading-spacing, hidden-content, and template-pattern flags as evidence to inspect. Measured accessibility failures need correction; heuristic eyebrow/icon/rail warnings may be justified. Correct the defect or state the concrete product reason, without turning a tool's heuristic into an extra aesthetic law.

Scores are optional communication aids for broad design reviews. If used, anchor them to observable gaps: broken/unreadable, functional but generic, coherent with material defects, well-resolved with minor gaps, or exceptional category-level work. Do not compare arbitrary model decimals or call a page accepted because it crossed a number. Serious task/readability failures cannot be averaged away by beautiful imagery. Existing-system polish often benefits more from compliance findings than a taste score.

Recheck affected results after fixes. Stop when required behavior works, significant visual defects are resolved, the chosen expression is coherent, and further changes do not produce a meaningful gain. Do not run an endless score chase or enlarge verification merely to generate more evidence. Explain unresolved blockers or tradeoffs honestly.

## Files and delivery

Respect project output conventions. Keep drafts, intermediate media, temporary captures, and logs in a task-specific working area; keep formal code, final media, and maintained design documentation in production locations. Do not overwrite another task, clean unrelated history, move existing files, or modify ignore rules merely to hide evidence. Production references must not point into temporary research directories.

Keep only needed tools/resources. Existing screenshot and project tools are preferable to inventing a new framework. For custom browser automation, use an isolated temporary profile and appropriate platform settings rather than interacting with personal browser credentials.

Inspect the final diff and references: only requested work and necessary supporting changes, no caches/secrets/large accidental binaries, all production assets present, no stale working-directory links. Describe the result, meaningful design choices, actual checks, important omissions, and evidence location. A concept-only result is not a rendered interface; an unexecuted flow is not tested; a static image is not a functional demo. Lack of tools should narrow the claim, not manufacture a pass.
