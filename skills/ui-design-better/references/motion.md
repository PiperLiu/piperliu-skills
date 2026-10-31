# Interface motion

Read for feedback, transitions, entrances, scrolling, and gesture feel. Use [generated motion](generated-motion.md) only when the media itself must undergo semantic change.

## Purpose and allocation

Useful motion directs attention, explains a relationship, exposes progress, confirms an action, rewards exploration, or establishes mood. Choose the leading purpose. Decoration can exist when inexpensive, pausable where needed, and subordinate to use.

For a new interface, consider three opportunities: immediate feedback for the leading action, continuity for an important state change, and a coordinated first entrance. These are opportunities to cover meaning, not a quota of animations. A fast cut, static response, or an already mature component may satisfy the need. Do not add an entrance to a task where it delays work.

Concentrate invention in a few product-specific moments. Describe the idea as “this object changes this way because the user did this.” The affected object should deliver the result; avoid unrelated celebration on every click.

## Coherence and feel

Take weight, friction, elasticity, and rhythm from the chosen direction. A snap can evoke a magnetic catch, a damped slide a drawer, a flow honey, an impact a heavy object settling, a bounce a rubber ball, or a drift something suspended. Mechanical precision can use a hard cut or an intentionally stepped rhythm. These are analogies to tune, not physics requirements.

For a spring system with comparable units, exploratory stiffness/damping pairs might be snap 350–400/10–15, damped slide 250–300/20–25, flow 150–200/30–40, impact 400–500/5–10, bounce 300/8, drift 100/25. Parameters depend on mass, integration, library, and displacement; inspect the result rather than transplanting numbers. Low damping suits small accents more than large panels. Large-area overshoot around 1–2% can already be enough; a small confirmation mark may tolerate 10–20%.

Cause should propagate visibly: the initiating object moves first, dependent elements follow with smaller amplitude or short offsets, and the destination acknowledges arrival. Keep a coherent direction across image, label, indicator, and background. Shape continuity can turn the previous object into the next state instead of replacing everything at once.

## Transition vocabulary

- **Same object, new place:** use continuous geometry or a shared element. Return it to a sensible origin and restore navigation/scroll context. If the old origin is offscreen, choose a coherent return rather than flying to an invisible location.
- **Same content, different size/layout:** move or reshape it; crossfading scaled duplicates often creates ghosting. Crossfade when content actually changes.
- **Lists:** distinguish removed, added, and retained items. Move retained objects into new positions rather than fading the whole list.
- **Selection:** a shared moving indicator can connect old and new selection. Measure varying option widths; initialize and remeasure directly after font load or resize rather than animating from zero.
- **Enter/exit:** opening and closing should have intelligible inverse directions. A drawer enters from its own edge. Exit is often faster than entrance, around 60–70%, when that feels natural.
- **Boundaries:** make an unavailable next step understandable through disabled affordance, a short boundary response, or explicit status. Do not require a bounce everywhere.
- **Destination readiness:** prepare media and required content before revealing a destination. Do not end an elegant transition on a white unloaded rectangle. Retain frequently switched views when justified, with a memory budget.

For whole-page transitions, a covering wipe is often robust because DOM replacement occurs under cover; overlapping pages need simultaneous DOM and layer/memory management; shared elements require careful handling of interruption, back navigation, double clicks, and resizing. Select for continuity and reliability, not a hierarchy of fanciness. Always have a direct-to-final-state fallback. An initial loading narrative should explain a real wait, not create one.

## Timing starting points

| Change | Initial tuning range |
| --- | --- |
| Immediate press response | Begin on input; a short response around 80ms can feel direct |
| Press/selection settlement | 150–300ms; a subtle 0.96–0.98 press scale may suffice |
| Small popover or menu | 180–250ms; expand from the trigger, often from near-full scale |
| Drawer or panel | 250–400ms depending on distance |
| View/page transition | 350–500ms; long blocking transitions impose a cost |
| Stagger | 40–80ms between related elements; keep the overall entrance brief |
| Hover lift | Often 2–4px; large travel can detach the object from its target |

A first entrance around 600ms total, or a richer section reveal under about 900ms, is a useful starting budget. Play, teaching, storytelling, and a deliberately slow ritual may need other timing. Tune to the actual distance, scale, frequency, input, and meaning.

For invisible effects such as copying or saving, communicate the actual result near the action, including what was copied/saved when useful. A generic “Success” is weaker than a specific result. Play confirmation once per meaningful change rather than replaying it on redundant clicks.

## Scroll as narrative, when useful

Persuasive or exhibition pages can benefit from content-aware reveals and a continuous transformation that demonstrates the product. Neither is an obligation for every marketing page. Workspaces, forms, and reading usually benefit from immediate native scrolling.

Distinguish **scroll-triggered** animation (crossing a threshold starts a timed event) from **scroll-driven** animation (position determines progress). Triggered reveals normally play once and remain visible; resetting at a viewport boundary makes reading unstable. A deliberately theatrical reset should happen only after the content fully leaves view.

For driven sequences, stop when the input stops, reverse coherently, and render the correct state after a mid-page refresh or jump. Use local section progress when the story is local; do not automatically map an entire website to one timeline. Preserve native navigation and a skip route for long sequences.

Possible constructions:

- a layered hero whose foreground and background respond at different rates;
- a large wordmark moving into its actual navigation position, measured from the layout, without an unnecessary duplicate;
- an uninterrupted object journey through overview, detail, interior, and result;
- a chapter handoff through an expanding mask, a matching shape, a view into an image, a background change, or a progressively revealed declaration.

Use parallax where real depth exists. Keep readable text, buttons, and forms stable; graphic display type can be a layer when legibility is protected. Give reading a resting phase. A sequence should hand its focal object or attention to the next section, not pin a stage and abruptly discard it. Wordmark handoff, depth, and other patterns need not all appear together.

For a large-screen theatrical hero, roughly 100–200vh of progress may be a useful experiment, shortened on mobile; changes around 15% scale or 15vh translation can be perceptible. These are examples of sufficient visible change, not minimum motion requirements. Smaller motion can be correct when the purpose is subtler. Do not force long pinning on short content.

Reveals can follow content: a path draws along its direction; connected steps unfold in reading order; a photo reveals from its subject; rigid machinery settles sharply; paper can have slight rotational drag; meaningful numbers can roll from their previous values. Use a coordinated vocabulary for ordinary sections and distinct emphasis where content warrants it, rather than adding a different trick everywhere.

Smooth scrolling is input treatment, not a story by itself. Add it only if it improves the experience and preserves expected navigation. Full-screen snapping suits particular exhibitions more than long text or normal business tasks. Prefer mature native capabilities or the project's existing library for complex choreography; do not mandate a new dependency when native tools suffice. If coordinating multiple animation systems, use one timing source and verify compatibility. Package pinned local dependencies when offline delivery requires them.

## Optional composition prompts

Borrow the relationship between input, visual response, and information, not a reference's theme or assumed technology. These prompts span media, orchestration, and UI state; only semantic media needs a generated-motion pipeline.

| Pattern | Purpose and acceptance question |
| --- | --- |
| One product, changing materials/scenes | Explain capabilities while retaining silhouette and identity; do parameters match the visible state? |
| Surface to interior to whole | Reveal a meaningful scale/structural relationship; can the reader return to the original context? |
| Small window becomes a stage | Move attention from object recognition to detail; are crop, reading space, and the return to normal flow resolved? |
| Multiple images converge | Explain inputs becoming one focus; are identities and reverse paths preserved? |
| Scatter becomes order | Make organization visible; does the final reading order actually help, and can an automatic introduction be skipped? |
| Perspective display becomes frontal UI | Move from product impression to readable content; does it settle long enough to read and interact? |
| Draggable sticker stage | Reward exploration with brand objects; do reset/cancel, link access, and touch scrolling still work? |
| In-place hover/focus preview | Reveal relevant media without overwhelming a compact list; is the same information reachable by touch and keyboard, without edge overflow? |
| Relationship constellation | Reveal links through selection; does detail remain stable and is a sequential/list equivalent available? |
| Expanded choice with compressed neighbors | Focus one choice while retaining alternatives; are small options identifiable, focus stable, and auto-advance absent during reading? |
| Audio-responsive state form | Distinguish idle/listening/processing/output/error; does real input drive it, with permission, silence, interruption, and stop handled? |
| Content collection as space | Express a collection then return to search/organization; are actual capabilities and sources clear without invented results? |
| Accumulated use becomes material | Encode meaningful history or growth reproducibly; does the visual avoid suggesting a broken/disabled control? |
| Shared icon geometry | Connect related states through anchors; are final semantics, accessible names, small-size clarity, and reversal correct? |

A recording demonstrates an appearance, not an operable interaction or its implementation. Verify current source, dependency, and license before reuse. Do not infer a physics engine, generation model, microphone chain, performance, or mobile quality from an attractive preview.

## Runtime discipline

Business state should update independently of decorative completion. High-frequency interactions must be interruptible: retarget from the current pose rather than restarting at the beginning. Avoid long periods where transitions block input.

Animate transforms and opacity where possible; explicitly list animated properties. Small indicators can reasonably animate dimensions. Expensive filters, large repaint areas, and layout animation need measurement. Separate layout reads and writes, record input in handlers, and render in a shared animation loop. Stop work when settled, hidden, or offscreen; clean up listeners and observers.

Native view transitions can preserve object identity with unique transition names. Watch for duplicate names, stale snapshots, unsupported pseudo-element selectors, and blank destinations. Inspect current browser behavior and documentation when implementation depends on such details; the design intent is more durable than a particular selector workaround.

Respect reduced motion: present equivalent information and final states without large movement, automatic scrub, or camera shake. Do not remove results, hide content at zero opacity, require sound, or wait for an animation before allowing the main action. Autoplay and looping need appropriate pause/start behavior and browser-policy fallbacks.

## Verify motion as motion

Operate once at normal speed, reverse, interrupt, repeat quickly, and reach the boundary. Look for wrong directions, flashes, ghosting, resets, lag, and stuck intermediate states. Test reduced motion. Sequence images establish state and ordering; direct operation or playable recording is needed to judge real-time feel. Report frame rate or performance improvement only when measured.
