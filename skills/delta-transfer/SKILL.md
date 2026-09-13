---
name: delta-transfer
description: Infer the transferable improvement delta from a paired contrast A→B, then apply that delta to a new target C while preserving C's identity, content, constraints, and context. Use when the user provides an inferior/baseline example A, a preferred counterpart B, and a target C, and wants C improved specifically in the ways B improves on A. Works across images, writing, UI, code, architecture, presentations, prompts, and other comparable artifacts; treat vector arithmetic as a reasoning metaphor unless a real embedding/vector tool is explicitly available.
---

# Delta Transfer

Use a contrast pair to learn an improvement direction, then transfer that direction to a new target.

Conceptually:

```text
A = baseline / less preferred example
B = preferred counterpart
C = new target
Δ = transferable improvement from A → B
D = C improved by Δ
```

The goal is **not** to make C resemble B in general.

The goal is to identify what makes B better *relative to A*, isolate the parts of that difference that are portable, and express those same improvement mechanisms in C without erasing what makes C itself.

## Core Rule

Treat:

```text
D ≈ C ⊕ transferable(B − A)
```

as a reasoning model.

Do **not** claim literal vector arithmetic unless an actual embedding space, feature representation, or transformation tool is available and appropriate.

For normal agent work, `B − A` means a structured latent difference: changes in emphasis, composition, abstraction, timing, hierarchy, restraint, clarity, architecture, tone, behavior, or other qualities that plausibly explain why B is preferred.

## Inputs

The workflow expects three comparable artifacts:

- **A — Baseline**: the weaker, less preferred, or earlier interpretation.
- **B — Better counterpart**: comparable to A and preferred by the user.
- **C — Target**: the new artifact to improve.

Optional but useful:

- explicit invariants that must not change;
- user hints about why B feels better;
- strength of transfer: `subtle`, `moderate`, or `strong`;
- output mode: analysis only, transformation instructions, or direct transformation when suitable tools are available.

A and B should ideally represent the same task, scene, requirement, or intent. If they do not, first identify a shared comparison basis.

## Do Not Ask the User to Verbalize the Delta First

A major purpose of this skill is to help when the user can recognize that B is better but cannot easily explain why.

Inspect A and B first. Infer candidate improvement mechanisms yourself.

Ask the user only when:

- several materially different explanations remain plausible;
- a difference could be either intentional improvement or incidental variation;
- applying the inferred direction to C would risk changing a protected property.

## Workflow

### 1. Establish the Comparison Basis

Before extracting the delta, identify what A and B are trying to accomplish in common.

Examples:

- the same manga panel interpreted by two directors;
- the same product screen redesigned twice;
- the same paragraph before and after a strong edit;
- two implementations of the same requirement;
- two slides communicating the same point;
- two prompts intended to generate the same class of result.

Write a one-sentence **shared intent**.

If A and B do not share enough intent to support a meaningful comparison, stop and explain why the pair is weak evidence.

### 2. Identify Invariants

Separate properties that should remain stable from properties that may explain the improvement.

Typical invariants include:

- subject identity;
- factual content;
- user requirement;
- narrative event;
- data semantics;
- public API behavior;
- brand identity;
- target audience;
- C's unique content;
- explicit user constraints.

Do not infer an improvement from a difference that merely changes an invariant.

### 3. Extract Candidate Deltas

Compare A and B at multiple abstraction levels.

Do not begin with surface adjectives such as “more cinematic,” “cleaner,” or “better designed.” Decompose them into observable mechanisms.

Useful levels:

#### Intent / emphasis
What does B direct attention toward that A does not?

#### Structure / composition
How are parts arranged, sequenced, grouped, paced, framed, or prioritized differently?

#### Information / abstraction
What does B remove, compress, reveal, defer, simplify, or make explicit?

#### Dynamics / rhythm
Does B change timing, transition, escalation, spacing, cadence, or interaction?

#### Sensory / stylistic treatment
When relevant: lighting, color, camera distance, line weight, prose rhythm, density, typography, animation, sound implication, etc.

#### Engineering / behavioral mechanism
For code and systems: ownership, interface depth, locality, failure handling, state flow, coupling, observability, performance, or testability.

For each candidate difference, state:

1. **Observed change** — what changed from A to B.
2. **Hypothesized benefit** — why that may make B better.
3. **Mechanism** — the more general principle underneath the surface change.

### 4. Filter for Transferability

Do not transfer the raw difference set.

Classify every candidate delta as one of:

- **Transfer** — portable improvement mechanism.
- **Adapt** — useful principle, but must be re-expressed for C.
- **Do not transfer** — pair-specific, incidental, or incompatible with C.
- **Uncertain** — plausible but weakly supported.

Use these tests:

#### Portability test
Would this principle still make sense on another artifact with the same broad goal?

#### Counterfactual test
If B kept this mechanism but changed its specific characters, wording, colors, modules, or scene details, would the improvement likely remain?

#### Identity test
Can this improvement be applied without turning C into B?

#### Causal-plausibility test
Could this difference reasonably explain the user's preference, rather than merely correlate with it?

#### Constraint test
Does the change respect C's requirements and invariants?

A difference that fails these tests is not part of the transferable delta.

### 5. Build the Delta Card

Summarize the transferable direction before touching C.

Use this compact representation:

```text
DELTA CARD

Shared intent:
- ...

Preserve:
- ...
- ...

Increase / emphasize:
- ...

Reduce / avoid:
- ...

Reorganize:
- ...

Introduce:
- ...

Remove:
- ...

Adapt rather than copy:
- ...

Do not transfer:
- ...

Confidence:
- High / Medium / Low
```

When useful, add a table:

| Dimension | A | B | Transfer direction | Confidence |
|---|---|---|---|---|
| attention | diffuse | focused | concentrate hierarchy | high |
| pacing | uniform | staged | create contrast in rhythm | medium |

The Delta Card is the semantic equivalent of the conceptual vector `B − A`.

### 6. Map the Delta onto C

Inspect C independently before changing it.

For each transferable dimension:

1. Determine C's current state.
2. Ask whether C already expresses the desired property.
3. Determine how the improvement mechanism should manifest *in C's own language*.
4. Avoid pushing a dimension past the point where it stops helping.
5. Preserve all C-specific invariants.

Do not mechanically reproduce B's literal solution.

Examples:

- If B improves A through tighter framing, C may need stronger visual focus, not the exact same crop.
- If B improves A by deleting exposition, C may need to remove a redundant explanation, not copy B's sentence structure.
- If B improves A through a deeper module boundary, C may need a different interface because its domain model differs.
- If B improves A through stronger contrast, C may need typographic hierarchy rather than B's colors.

### 7. Produce D

Choose the output according to the task and available tools.

#### Analysis-only
Return the Delta Card plus a concrete C→D transformation plan.

#### Editable artifact
Apply the delta directly when the requested artifact type and tools support safe editing.

#### Prompt / handoff
Produce a transformation brief that another model, designer, developer, or tool can execute.

When performing a direct transformation, keep the user's original C available conceptually as the baseline for validation.

### 8. Validate D Against the Direction

Do not validate D by asking “does it look like B?”

Validate these two claims separately:

#### Directional success
Did D move from C in the improvement directions inferred from A→B?

#### Identity preservation
Did D remain recognizably C, preserving C's content, function, identity, and constraints?

Also check:

- No pair-specific detail from B leaked into D without reason.
- No improvement dimension was over-applied.
- No protected invariant was changed.
- New changes not justified by the delta are minimized.

If D is worse on an important C-specific property, reduce or adapt the transfer instead of defending the analogy.

## Strength of Transfer

Interpret requested strength qualitatively.

### Subtle
Apply only the highest-confidence transferable mechanisms. Preserve almost everything else.

### Moderate
Apply all high-confidence mechanisms and selected medium-confidence ones.

### Strong
Push the inferred direction clearly, but still preserve invariants. Strong transfer does not authorize copying B-specific content.

Default to **moderate** when the user does not specify.

## Multiple Plausible Deltas

Sometimes A→B is underdetermined: several changes happen at once and the user has not said which one caused the preference.

Do not collapse uncertainty into one confident story.

Instead:

1. identify 2–4 plausible delta hypotheses;
2. rank them by evidence and transferability;
3. apply shared high-confidence directions first;
4. either keep disputed directions conservative or ask the user to choose.

If the transformation is cheap and reversible, producing a few C variants along different delta hypotheses can be more informative than asking abstract questions.

## Domain Guidance

### Images / Film / Visual Design

Look beyond object identity.

Possible transferable axes:

- focal hierarchy;
- framing and camera distance;
- pose and gesture readability;
- negative space;
- foreground/midground/background separation;
- lighting motivation;
- value grouping;
- color restraint;
- depth cues;
- timing implied by composition;
- emotional specificity;
- visual information density;
- shot-to-shot continuity.

Do not transfer literal characters, costumes, background objects, or palette unless those are themselves the identified mechanism.

### Writing

Possible axes:

- specificity;
- sentence rhythm;
- information ordering;
- compression;
- implication versus exposition;
- voice distance;
- argument structure;
- transition strength;
- concrete versus abstract language.

Preserve C's facts and intended meaning unless the user authorizes substantive changes.

### UI / Product Design

Possible axes:

- visual hierarchy;
- interaction cost;
- progressive disclosure;
- grouping;
- primary action clarity;
- error prevention;
- feedback timing;
- density;
- discoverability.

Do not copy B's branding or layout when the transferable mechanism can be expressed more naturally in C.

### Code / Architecture

Possible axes:

- locality;
- ownership;
- interface depth;
- coupling;
- state flow;
- naming;
- failure boundaries;
- test surface;
- observability;
- data movement.

Preserve C's functional requirements and public compatibility constraints unless the user explicitly allows breaking changes.

## Failure Modes

### “Make C like B”
Wrong. This is reference imitation, not delta transfer.

### Transfer every A/B difference
Wrong. Many differences are incidental or context-specific.

### Invent a literal vector
Wrong unless a real embedding representation exists.

### Use vague style labels as the delta
“More cinematic” is not enough. Explain what changed to create that effect.

### Erase C
The transfer fails if D is merely B with C's content pasted in.

### Assume B is universally better
B is evidence for the user's preference in this comparison, not a universal quality standard.

### Overfit one pair
One A/B pair is weak evidence for subtle causal claims. Mark confidence accordingly.

## Output Format

Unless direct transformation is the obvious requested result, report:

```text
## Shared intent

## A → B: observed improvements

## Transferable delta
- Transfer:
- Adapt:
- Do not transfer:
- Uncertain:

## C-specific invariants

## Applying the delta to C

## Result / transformation brief

## Validation
- Directional success:
- Identity preservation:
- Risks / uncertainty:
```

Keep the analysis concrete enough that a user can disagree with a specific inferred delta instead of having to argue with vague taste.
