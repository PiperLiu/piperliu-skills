# Visual and interaction language

Read for composition, typography, surfaces, controls, density, and responsive design. Review large relationships before small styling.

## Hierarchy and space

Describe a defect relationally: what is competing with what, what is too far from its action, or which grouping is unclear. A class-name change proves implementation changed; rendered evidence establishes whether it improved.

- Give each region a legible hierarchy. Contrast, area, weight, placement, and movement should not all emphasize different things.
- Use closer spacing within groups and more separation between groups. Keep the same spatial relationship consistent.
- Let parent layouts own spacing between regions; components own internal spacing. Avoid several wrappers each contributing to the same gap.
- Use negative space to group and pace. Preserve useful density in work tools; do not remove necessary information to manufacture luxury.
- Intentional asymmetry, overlaps, large type, and broken grids can work with local alignment and a clear reading order. Do not repair an intentional imbalance into bland symmetry.
- Start with an open canvas, rows, or a table. Add a surface when it encloses a meaningful object or operation, not simply because another wrapper exists.
- Avoid redundant boundaries: a divider plus adjoining borders, repeated nested shadows, or a frame around a frame serving the same grouping. Keep useful table rules, clear object edges, and modal boundaries.
- Give a long page variation in scale, density, composition, and pauses. Repeated cards or full-width rules in every section can flatten the rhythm. Finish with the same care as the opening.

Common failure signals include ornamental eyebrow pills everywhere, decorative single-side color rails, three equal feature cards saying little, unrelated glow, giant generic slogans, repeated all-caps labels, and a dashboard's obligatory four KPI cards. Investigate their purpose. A real status badge, quotation rule, category convention, or chosen maximalist vocabulary can justify the same form.

## Typography and real content

Choose type for character, reading task, language coverage, and context. A distinctive display face can pair with a quieter body face; one well-handled family or a system face may be more appropriate. Do not rotate the same fashionable font through unrelated projects, or mistake letter-spaced system text for a complete brand identity.

Use a small set of roles: display, section title, body, supporting text, labels, and data. Make differences perceptible instead of accumulating almost-identical sizes. Test the actual language and fallback fonts, mixed-script baseline and apparent weight, and long names.

Starting ranges, subject to real-size reading:

| Content | Useful initial range |
| --- | --- |
| Chinese reading text | 16–18 CSS px |
| Product body and controls | 14–16 CSS px |
| Sustained dense desktop work | 13–14 CSS px if comfortably readable |
| Reading prose leading | About 1.6–1.75 |
| Multiline Chinese heading leading | About 1.2–1.35, checked with actual glyphs |
| Latin prose measure | Roughly 55–75 characters; adapt for script and task |

Do not use tiny low-contrast text or compressed leading as a substitute for resolving density. Enlarging text and narrow viewports should preserve reading and operation. Condensed faces suit display or short identifiers more than long reading.

Chinese headings need their own leading and line-break decisions; Latin poster settings often collide. Avoid fixed one-line heights for multiline content. Balance short blocks by meaning; keep a number with its unit and avoid awkward isolated characters or broken short words. Wrapping helpers are aids, not proof. Remove negative-margin fixes that merely move the collision elsewhere.

Use content-driven height and flexible containers before reducing text size. Truncate deliberately only when the full value is reachable and similar objects remain distinguishable. Use tabular numerals for comparing changing or aligned numeric columns; choose optical form for a standalone display number. Align quantities and decimals for comparison and retain units, currency, sign, precision, and time context consistently.

Real product content comes first. For prototypes, use one coherent fictional setting and plausible variation in names, lengths, values, and timestamps. Do not make fabricated adoption, growth, customer endorsements, uptime, or outcomes appear to be product facts. Irregular numbers do not become true just because they look realistic. Explain simulated data and unconnected actions in the handoff; place disclosures in the UI when needed to prevent a consequential misunderstanding.

## Color, surfaces, and detail

Assign stable roles to text, background, action, selection, disabled, and status colors. Distinguish important states with text, shape, or icon as well as hue. Keep normal states quiet enough for actual exceptions to stand out; a sea of green success chips can hide the one urgent failure.

Check text, boundaries, focus, and selection against their actual backdrop, including image, transparency, and animation. Meet the project's accessibility target; do not trade essential legibility for atmosphere. A secondary color may be quieter without becoming unreadable.

Hue and temperature shifts can create surface hierarchy as well as lightness. Monochrome, duotone, or alternating light and dark chapters can be expressive. Gradients, noise, heavy borders, and shadows are available when they reinforce depth, character, or meaning. Apply finish coherently: precise treatments and raw marks can coexist if their contrast is deliberate.

Reserve exceptional emphasis for meaningful priority. Equal-level components should have comparable visual weight unless a difference communicates importance. Do not give every ordinary card its own bright palette and heavy shadow.

## Controls and icons

Carry a shared grammar through buttons, inputs, switches, tags, overlays, and empty states: shape, edge, weight, selection, feedback, and movement. A component library supplies useful semantics and behavior; theme its typography, spacing, density, and states rather than changing only the primary color.

- Make interactive affordances discoverable. Separate default, pressed, focused, selected, disabled, and busy meanings.
- Preserve hit area and nearby layout during state changes. Provide touch and keyboard access to hover-revealed actions.
- Use semantic elements, accessible names, visible focus, and a logical focus order. Unfamiliar icons benefit from visible labels. Static decoration should not look clickable.
- Use a consistent icon family, optical size, stroke, endpoints, and alignment. Fill gaps with compatible shapes rather than mixing unrelated emoji, glyphs, and libraries.
- Choose the family for the product: thin editorial marks, sharp instrument-like symbols, friendly filled forms, variable-weight symbols, pixel grids, or no icons. Existing installed icons usually take precedence over replacing a library.
- Match apparent stroke weight to text and align optically, not only by bounding boxes. Around 1–1.25 times the text size is a starting point, not a sizing contract.
- A few custom brand illustrations can enrich key moments. Do not draw a complex natural hero as a thin placeholder icon merely because SVG is convenient.
- Give arrows a consistent meaning. An external-destination arrow should not misleadingly label an in-place submit action. Prevent nested row/card actions from firing each other.
- Check asset and icon licenses for the actual platform and use. Public availability alone does not grant web or commercial reuse.

## Interaction and state completeness

Model the states the actual task can reach: initial, loading, empty, partial, editing, invalid, submitting, complete, failed, and recovering as applicable. Do not create a ceremonial state matrix for states the product does not have.

Place feedback near its cause. Keep useful input and context after failure, show a recovery action, prevent unintended duplicate submission, and make destructive scope clear. Forms need understandable labels, requirements, validation, and errors tied to fields. Dialogs and popovers need reachable close behavior, focus handling appropriate to their role, and an unobscured primary action. Do not confuse cosmetic success feedback with confirmed persistence.

In linked workspaces, selecting a time range, object, or exception should update related views consistently. Put judgment fields in the list and secondary detail in an inspector or contextual surface. Prefer a domain's useful work surface over ornamental analytics. Count avoidable clicks, modal interruptions, cross-page trips, and repeated data entry when evaluating a workflow change; do not turn those observations into unsupported claims about real users.

## Devices and recreation

Choose the target from use context; 1440×900 and 390×844 are convenient examples, not universal specifications. A screenshot's physical pixels may be multiplied by DPR. For recreation, establish logical viewport and crop, measure area proportions and alignment lines, then match typography and media before shadows and small decoration. Compare aligned renders or overlays; document extrapolated states and responsive behavior.

For mobile, rethink sequence and reach. Use comfortably sized targets (often around 44 CSS px or larger, adjusted to platform requirements), safe-area spacing, and controls that survive the virtual keyboard. Check dynamic height, orientation when relevant, internal scrolling, and fixed bottom bars. Multi-screen flows should retain selection, scroll position, and sensible back behavior; a side-by-side screen overview can reveal inconsistency but does not replace operating the flow.

For canvas and gestures, check real drawing, coordinate mapping, touch cancellation, and that page scrolling remains available. For nested workspaces, verify which area scrolls and avoid accidental double scrolling. Wearables, kiosks, and in-vehicle displays require their actual physical and input constraints rather than a scaled phone layout. Do not claim hardware, haptic, or safety validation from a desktop screenshot.
