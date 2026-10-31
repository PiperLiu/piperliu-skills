# Generated motion and runtime

Read when existing/generated video or frame sequences will carry semantic motion inside an interface. This is a portable planning and acceptance guide, not an installed media pipeline. Use the project's actual tools and document reproducible commands. Simple geometry, UI state, live data, and freely interactive 3D usually belong in code.

## 1. Separate independent decisions

Record these once in a compact motion specification. Existing project files can serve this purpose; exact filenames and serialization are optional.

| Decision | What to establish |
| --- | --- |
| User intent | Subject count, identity, relationships, style, intended action, and non-negotiable continuity |
| Background ownership | Complete scene belongs in the media, or an isolated subject must composite into the page |
| Input | Scroll, pointer, drag, touch, orientation, audio, data, state, or time |
| Input semantics | Continuous value, discrete step, or event |
| Time control | Scrub, play a transition segment, or autonomous playback |
| Navigation | Continuous page, paged sections, or no page movement; independent of playback |
| Parameter space | Linear range, circular loop, two-dimensional sampling, or independent discrete states |
| Production continuity | A continuous chain or independent clips |
| Display | Actual container ratio, largest CSS dimensions, crop/safe area, target DPR, supported devices |
| Fallback | Initial/rest pose, loading/failure state, reduced-motion equivalent, unavailable-input substitute |

Do not reinterpret explicit user choices as merely stylistic suggestions. Clarify a missing choice if it changes feasibility or the expected result. Do not default every asset to square: derive its ratio from the destination and verify actual output dimensions. If the service needs another ratio, define the crop or padding.

Keep derived production plans separate from those facts: storyboard, keyframes and clip chain, identity reference, anchor, loop policy, expected frame count, frame strategy, budget, and gesture behavior. A final timeline and a delivery-budget record each have their own authoritative values. Do not copy durations and state indexes into several independent places.

## 2. Discover the meaningful change

Inspect the object's structure, function, material, space, states, and information. Useful verbs include assemble, unfold, peel, grow, crystallize, reveal, scan, orbit, enter, trace, converge, compare, charge, and complete. Choose the action that explains something; do not pack the whole vocabulary into one shot.

Separate three layers:

- **Semantic media:** joints, connection, deformation, material, hair, cloth, contact, occlusion, and a predetermined scene transformation.
- **Geometric orchestration:** position, scale, crop, path, perspective, mask, inertia, and time mapping.
- **UI state:** selected item, actual data, focus, cancellation, completion, text, and error.

Generate the first layer when needed; implement the latter two precisely in code. If moving a flat image breaks contact or occlusion, more CSS patches will not produce the missing semantic action. Conversely, do not generate a large raster movie to perform a rectangle's expansion.

### Rotation is not one parameter model

| Requested effect | Correct interpretation |
| --- | --- |
| Face follows a circular pointer direction | Front-facing gaze travels around a direction ring; angle alone can suffice |
| Face responds to horizontal and vertical distance | Two-dimensional poses, including a neutral center; not one ring or left-to-right movie |
| Head scans left to right | Bounded yaw range with a center, not a closed rotation |
| Product spins on a turntable | Circular orientation exposing front, sides, and back |

Real product backs and side details need reference evidence. For a complete turn, approved quarter views can constrain separate arcs; do not let a front image silently authorize an invented back. Ring mapping uses the shortest circular distance; 2D input requires a real 2D representation or another explicit solution. A radial node layout is not a circular media timeline.

### Continuous scene handoffs

Choose a visual anchor before generating segments:

| Mechanism | Anchor and risk |
| --- | --- |
| Scale penetration | A centered landmark becomes the next scale; avoid jumping too many scales in one clip |
| Occlusion | A foreground object fully covers the view at handoff; incomplete coverage exposes the replacement |
| Shape match | Preserve screen position and contour while meaning/material changes |
| Time passage | Lock framing and geometry while time, light, or material changes |
| Reflection entry | Establish a clear reflection that grows into the next scene |
| Cutaway entry | Reveal an interior through a surface while preserving spatial relationships and camera continuity |

These are prompts, not exclusive transition types. Large geometry-changing scenes are higher risk; prove them in a pilot. Every scrub frame must work as a still. Check whether reverse playback is physically and narratively coherent; splashes and irreversible events may need a separate reverse transition or different control model. Keep explanatory text in stable reading phases and in the page layer.

## 3. Budget before expensive production

Choose **background ownership**, **media representation**, and **time controller** separately. A paged layout does not imply segmented sources; a video does not imply autoplay; scrolling does not imply scrub.

- A coherent environment, contact shadow, depth of field, or camera journey often favors a complete scene video. Do not key it merely to make every asset transparent.
- A small transparent sequence needing frequent random access may suit an alpha atlas. True 2D sampling often needs a grid of poses or another multidimensional representation.
- A long or large transparent one-dimensional sequence may favor video with an appropriate alpha/compositing strategy. Chroma video with runtime keying is one option, not the only portable format.
- Independent states should be budgeted separately; do not pretend arbitrary transitions exist between them.

Estimate minimum frame pixels from **maximum CSS dimensions × target DPR**, accounting for crop and aspect ratio. Probe the actual source; a “768P” label, requested frame count, or upscaled export is not evidence of native detail.

For an atlas, estimate both sheet capacity and decoded memory:

```text
columns = floor(texture_limit / cell_width)
rows = floor(texture_limit / cell_height)
capacity = columns * rows
RGBA frame memory ≈ width * height * frame_count * 4 bytes
```

Include gutters, padded sheet area, decoder/GPU copies, and device headroom in the real budget. A 4096px texture side can be a conservative planning limit, not a universal hardware guarantee. Forty-eight 640px cells do not fit a single 4096px square (only 36 do). Small compressed transfer size can still decode into excessive memory.

If over budget, change sampling density, segment scope, representation, or an explicitly revised display target. Do not silently sacrifice confirmed clarity to fit one sheet, or invent untested multi-atlas switching. Rebudget after actual frame counts and dimensions are known. A lower target DPR is an acknowledged sharpness compromise, not a change to the device's DPR. Deliver one justified main representation plus useful fallback, rather than maintaining competing pipelines unnecessarily.

## 4. Keyframes, pilot, and continuity

With existing media, preserve originals and start with analysis. Do not regenerate assets merely to follow this sequence.

For new semantic motion, approve keyframes before asking video generation to invent their connection. Lock character/product identity with actual reference inputs: silhouette, proportions, face, clothing, materials, marks, logos, part counts, and major geometry. Keep a reusable identity specification for a stable subject.

Each adjacent pair should describe one primary semantic change. Short clips, often about 3–6 seconds, reduce drift; actual duration follows the action and service. A prompt specifies path, allowed motion, fixed anchors, camera, scene/light, start/end, loop/reversal needs, and exclusions. Fixed-camera language is inappropriate when the camera journey is the intended change. Avoid gratuitous blinking, idle sway, scale breathing, extra parts, cuts, flicker, and unrelated detail.

Use the generation tool's supported reference and start/end modes. If a service rejects a required constraint, surface that limitation and select an authorized alternative; do not silently drop the constraint. Reproducible seeds help when supported but do not replace reference images. Model capabilities, prices, and parameter constraints must be checked against the chosen service rather than hardcoded into this skill.

For a new isolated asset, true alpha keyframes preserve a clean reusable source. If a video tool needs chroma input, composite a deterministic keyed copy and retain the alpha original. Check actual transparency rather than a painted checkerboard. Existing keyed media can still be processed. Pick a key absent from the subject and inspect time-uniform background, fine edges, internal colors, and spill.

Build a **pilot**: first approved keyframe pair, one short clip, chosen media representation, and actual placement in the page. Verify content, sharpness, interaction, and cost before multiplying production. Record what was accepted and which artifacts/settings it covers; hashes can make that record robust. Changes to the defining artifacts invalidate the old conclusion. This is a production checkpoint, not an invented requirement for user approval when the work is already authorized.

For continuous chains, use the previous accepted **actual output tail** as the next generation input, retaining the planned destination frame. Verify two different things: the exact handoff input was used, and the decoded output tail/head actually match. A hash proves the former, not the latter. Inspect identity, framing, light, scene, and cumulative drift. Fix the current segment upstream before producing more from a bad seam. Independent clips need not pretend to share a seamless chain.

Watch the complete master. First/last screenshots cannot reveal an internal hard cut, delayed action, flicker, wrong direction, duplicated part, or premature finish. A loop must preserve the motion and image across its seam, not merely request identical endpoints.

## 5. Frame preparation and compilation

Keep native frames when they already meet the intended playback, or when held/stepped timing is part of the art. Interpolate only to solve observed sampling or playback gaps, then compare original and interpolated contact sheets and motion. Reject added ghosting, double contours, tears, interpenetration, structural change, or brightness jumps. Interpolation is not automatically an upgrade.

Trim actual redundant holds without deleting meaningful slow change. Recheck every new adjacency after trimming or joining; do not jump from an early frame directly to a distant endpoint. Stabilize only unintended drift of an anchored subject, not intentional camera travel, free movement, or perspective change. Preserve accepted endpoints.

For transparency, inspect white, black, saturated, and final-page backgrounds. Test the **encoded delivery video**, not only pristine source frames: compression can introduce spill and blocks. Do not hide a broken source with aggressive threshold expansion, eroded silhouettes, or blurred edges. Fine hair, glass, translucency, and motion blur may call for a different representation. Prebaked reflection cannot respond physically to arbitrary future backgrounds.

Compile dimensions and quality within source and device budgets. For fast random video seeking, dense keyframes or all-intra encoding may help but increase transfer cost; choose and measure against the actual controller. Do not force all-keyframe video on ordinary sequential playback. Remove unintended audio when the experience does not use it.

For an atlas, retain frame count, rows/columns, cell dimensions, and parameter mapping in its manifest, and verify them against the actual file. Select a cell in a stable decoded texture or renderer rather than constructing new image layers on every input. Do not blend two large decoded frames simply to disguise insufficient sampling; that can add ghosting and memory cost without adding the missing motion.

Generate the timeline from **final retained/encoded frames**, including actual fps, state IDs, segment boundaries, rest frames, and rate curves. A useful segment model has:

```text
start <= hold < endExclusive
```

The stop pose is the last valid visible frame (`hold`), not the exclusive encoding boundary. IDs and order must agree with page states. Re-trimming or re-encoding requires regeneration; do not maintain handwritten seconds separately in UI code.

## 6. Controller and lifecycle

**Scrub:** input continuously determines progress. Clamp bounded ranges; wrap rings using shortest distance; sample 2D input as 2D. Input handlers update targets, a shared frame loop renders. For video, prefer the newest target frame and discard obsolete seeks. Smoothing and speed limits should not create persistent lag; avoid smoothing twice.

**Segment playback:** an event chooses a state, then time advances through its transition. Begin promptly and allow other UI movement in parallel. For a continuous chain, retain one media instance/source instead of replacing clips per page. Reverse from the currently visible time, cancel obsolete work, and honor the latest target. Do not rely on negative browser playback rate. Use frame callbacks or a suitable render loop rather than coarse `timeupdate` events for exact stopping; pause and settle before overshooting `hold`. Forward and reverse share authoritative rate curves.

**Autonomous:** time drives the media. Respect autoplay policy and sound requirements, expose a user start where needed, and loop only qualified loops. Muted inline video can help but does not guarantee autoplay.

For stepped navigation, define one gesture versus one raw wheel event, inertia coalescing, active-playback retarget/queue/ignore policy, and clamp/loop boundaries. Programmatic scroll must not accidentally trigger another step. Centralize thresholds and navigation locks. Ordinary resize should not repeatedly swap media sources; a necessary device-version reload should restore the current semantic state.

Preload the static fallback, metadata, and required media; wait for image decode or video readiness before switching. Do not seek before metadata exists. Choose compatible desktop/mobile assets at initialization when possible. Keep a readable fallback visible before readiness and preserve the visual state at handoff. Never reveal a raw green-screen source when rendering fails.

Recalculate input geometry after layout changes. Pause hidden/offscreen work, stop settled loops, release event handlers/renderers, and resume from current state. Request orientation or microphone access through an appropriate user action; denial, silence, or interruption needs a fallback. Audio amplitude shows activity, not task completion. Reduced motion presents equivalent stable content, without automatically scrubbing through the movie.

Coalesce rendering around the latest input, update only changed frames/properties, and keep layout reads separate from writes. Share compositing parameters between offline checks and the runtime; do not create a second set of keying thresholds in page code. A renderer failure must release any navigation lock and preserve usable static content.

## 7. Acceptance and diagnosis

Test contract fidelity, identity, master continuity, prepared frames, delivery media, timeline, and real runtime in that order. An upstream failure should not be disguised downstream.

Use the target CSS size and DPR at 100% browser zoom. Inspect cold cache, slow load, failure, low-capability mobile conditions, viewport change, background/resume, quick input, reversal, endpoints, and reduced motion as relevant. Scrub must stop at the corresponding state; segments must stop cleanly without hopping back; one inertial gesture should not skip unintended states; autonomous media needs working start/fallback behavior.

For flashes, check source, joins, encoded seams, exclusive boundaries, stale layers, and decode readiness. For sticky motion, check smoothing and seek backlog. For a blurry revision, check native source size, interpolation, repeated resize, cell size, and compression. For key residue, inspect the actual decoded delivery before changing renderer thresholds.

Retain source/reference inputs, prompts and tool metadata, the accepted pilot record, budget, final timeline, processing commands, and QA evidence in the task's working area. Production includes the chosen media, static fallback, and runtime integration. If an explanatory preview is requested, expose current progress/frame and its mapping, verify beginning/middle/end and reverse, and pause inactive media. Do not add a technical explainer to the product's normal user flow.
