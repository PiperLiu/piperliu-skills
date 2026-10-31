# Media and rendering

Read when imagery, a material, an illustrated object, or a rendered scene carries product meaning. Choose the medium for the visual problem.

## Give the asset a job

Ask what would deserve the image position if only one image, one heading, and one action remained. Does it identify an object, explain a relationship, show evidence, establish an atmosphere, or enable manipulation? A purely atmospheric image can be valuable; its relationship to the intended feeling should be deliberate.

Missing hierarchy is not missing imagery. Repair a weak concept or composition upstream before generating more pictures. Conversely, do not replace a necessary natural subject with generic geometry solely because code is easier.

Tools also benefit from object thumbnails, maps, covers, diagrams, and spatial context. Pure data tasks may need none. Media should change a decision or the experience rather than occupy an empty rectangle.

## Choose the production method

| Need | Suitable medium |
| --- | --- |
| Existing accurate product, place, person, or brand | Inspected, authorized original asset |
| Natural form, illustration, atmosphere, complex light or texture | Photography, licensed artwork, or generated bitmap |
| Exact diagram, data, labels, simple geometry | SVG, HTML/CSS, or canvas with appropriate semantics |
| Real-time configuration or adjustable proportions | Layered vectors or real-time rendering, often supported by static texture/detail images |
| Free viewpoint, physical interaction, changing reflection | Real-time 3D and physics when needed |
| Predetermined semantic transformation or camera journey | Generated or existing video/frames; see [generated motion](generated-motion.md) |

Reuse good material rather than generating to demonstrate tool use. Preserve editability and the project's established asset system. Natural heroes deserve enough detail and craft; vectors are legitimate finished art when their style and complexity fit the intended result.

Text, controls, live data, and accessible state remain in real UI. A screenshot can be a product illustration but cannot substitute for an operating product. A configuration change should visibly affect the configured object; a static photograph with a changing label does not fulfill that interaction.

Use existing authorized tools and services. Account login does not imply permission for unbounded paid generation. Do not silently switch paid providers, install a production pipeline, or ask for secrets in chat. If media cannot be produced, make a usable provisional version with an asset brief; identify the limitation in the handoff.

Offline delivery restricts runtime dependencies, not an already authorized asset-production method. Package approved outputs locally. Keep runtime links and licenses intact.

## Asset brief and prompting

Specify the subject and medium, composition and occupancy, text-safe area, background, material/light, permitted variation, and exclusions. Derive these from the page rather than a generic “hyper-detailed” prompt.

- Leave the intended text region free of highlights and busy detail. Around 10% separation between subject/shadow and text is a useful initial safety margin, adjusted for responsive crops.
- For background integration, request the actual page color or true transparency. Verify the output; a requested hex value is not proof of a match.
- Establish a common light direction, viewpoint, scale, edge treatment, and material logic across a set. More detail everywhere reduces focus.
- Keep generated words, logos, fake UI, watermarks, and unrelated floating props out when those are not the intended content. Use original brand assets for exact marks.
- Decide who owns cast shadows. Keeping an isolated asset's shadow separate often makes reuse easier; a scene's meaningful contact shadows may belong in the scene.

Generate a small set of purposeful variations and select against the brief. Use the version that composes best, not automatically the busiest one. Place it in the actual layout before extending the series. Fix a mismatch at its cause, whether composition, asset, or crop; do not distort the whole design to defend an unsuitable picture.

For A/B comparisons, hold original media and export quality equal unless the asset itself is the variable being tested.

## Integrate image and page

- Sample actual edges to match a background, or deliberately fade/mask an edge. A frameless visual may cross a color or section boundary and participate in the composition.
- Inspect alpha pixels and edges on the final background plus light and dark test backgrounds. File extension and a checkerboard-looking preview do not prove transparency.
- Let bitmap material and light connect with precise code-drawn paths, lines, and editable labels. Image annotations must point to real coordinates after cropping and scaling.
- On narrow screens, crop to the information-bearing region or provide a dedicated crop. Do not shrink an entire wide scene until its subject is unreadable. Move annotations below the image when anchored labels no longer fit.
- Reuse a detail crop later in the page when it reinforces continuity. Avoid generating a mismatched new scene for every section.
- An expressive painting can be a recurring stage behind a precise, quiet interface. Crop boldly, keep foreground UI legible, and use the artwork sparingly. Monochrome mapping, duotone, or halftone can unify heterogeneous sources when compatible with their meaning and license.

For abstract technology, derive a tangible representation from its data, tools, process, or output. Let accurate diagrams or typography carry the composition if no useful object exists. A luminous sphere is a choice, not a default explanation.

## Series, sprites, and interactive scenes

Create a concise style specification for a family: medium, view, light, proportions, palette, and baseline. Different objects should remain distinguishable by silhouette and structure at their final size, not only by hue. Derive states from approved references to preserve identity rather than generating every state independently.

Cut sprite sheets around actual extents with transparent gutters; do not assume a uniform cell crop cannot cut off a branch or include a neighbor. Align contact points across states. Objects that flip, rotate, or fall need credible sides, backs, closed edges, and lighting that remains compatible with the scene.

For play and tactile interfaces, inventory objects, how users recognize them, input effects, required states, feedback, and asset cost. Trace the loop from action to changed object to result or next turn. Do not use one static picture with different captions for genuinely distinct visible states.

The performance itself may reasonably last longer than a normal UI transition. Settle charges and rewards exactly once at the appropriate point, retain committed results across refresh, lock only necessary actions during a performance, and define when a gesture crosses its activation threshold. Reduced motion changes the performance, not the game's result or operation.

## Textures, external material, and 3D

Use actual color/diffuse maps for surfaces rather than a library's rendered preview sphere. Check tiling seams and repetition at final size; a model's UV texture is not necessarily seamless. Color maps generally need color-space treatment distinct from numerical normal/roughness data. Verify normal orientation and UVs with real light.

For maps, scans, scientific imagery, and engineering drawings, distinguish a photograph, interpretation, measurement, simulation, and original diagram. Preserve provenance and scale/context when they carry meaning. Inspect actual downloaded dimensions rather than trusting a catalog thumbnail or label. Scientific or archival credibility must come from the source, not an aged-paper effect.

Check each item's permitted use and attribution. A public API, museum download, or institutional name does not establish commercial reuse rights. Keep source, license, required credit, modifications, and any share-alike obligations with the asset. A reference-only image is not automatically licensed for publication or unrestricted derivative use.

Choose real-time 3D for genuine viewpoint, material, or spatial interaction. A mature renderer and, when needed, physics system can handle geometry and forces; images can supply textures, sprites, or environment. Judge perspective, volume, contact shadow, material distinction, and transmitted force in the running scene, not whether a library was imported.

Pause hidden/offscreen work, choose a device-appropriate DPR budget (a cap near 2 is often useful), provide a no-WebGL static fallback, and keep reduced-motion results functional. Confirm the canvas has actually rendered before capturing evidence. Prerendered glass/refraction only represents its source environment; it does not physically refract arbitrary page content.

## Export and handoff

Size outputs for maximum CSS display dimensions and a justified target DPR; around 2× is a useful still-image starting point, not permission to upscale a low-resolution source. Use responsive crops/srcset where useful. JPEG/WebP suit opaque images; PNG/WebP can carry alpha. Balance visual quality against transfer and decoded memory. Data URLs add roughly one third to encoded binary size.

Keep editable/source originals apart from delivery exports. Record origin, use, processing, and generation prompts; record model and actual cost only when the tool supplies them. Never invent those metadata. Avoid presenting generated places, people, product imagery, or mock results as documentary evidence.
