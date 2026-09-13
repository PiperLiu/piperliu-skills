# Delta Transfer Method Notes

## 1. The Analogy

The motivating analogy is:

```text
Δ = B - A
D = C + Δ
```

In a real vector space, this can sometimes correspond to a direction in an embedding or latent representation. In ordinary agent work, the artifacts may be images, paragraphs, interfaces, codebases, or plans with no shared numerical feature space.

Therefore this skill uses **semantic delta decomposition** rather than pretending that all artifacts have literal subtractable vectors.

```text
raw difference(A, B)
        ↓
remove non-causal / incidental differences
        ↓
portable improvement mechanisms
        ↓
adapt mechanisms to C's context
        ↓
D
```

## 2. Raw Difference vs Improvement Delta

A and B can differ in three broad ways:

### Invariants represented differently
The underlying subject, requirement, or event is the same but represented differently.

### Incidental differences
Changes that happen to differ between the pair but do not explain the preference.

### Explanatory differences
Changes that plausibly create the improvement and can survive outside the original pair.

The agent should infer the third class conservatively.

## 3. Delta Representation

Prefer directional mechanisms:

```text
increase focal isolation
reduce explanatory redundancy
increase contrast between setup and reveal
move state ownership closer to the behavior it controls
delay secondary information until after the primary action
```

Avoid pair-bound copying:

```text
use the same red background
put the character in the lower-left
use the same class names
copy B's sentence opener
```

unless the literal feature is itself what the user wants to transfer.

## 4. Transferability Heuristic

A candidate delta is stronger when it has:

- explanatory power;
- portability;
- independence from B-specific content;
- compatibility with C;
- observable effects after transfer.

Use qualitative confidence (`high`, `medium`, `low`) instead of invented numeric scores.

## 5. Direction vs Destination

Delta transfer specifies a **direction**, not a destination.

If:

```text
A: weak hierarchy
B: stronger hierarchy
C: already extremely hierarchical
```

the lesson is not “make C even more hierarchical.” The lesson is that insufficient hierarchy was one weakness in A.

Always inspect C before applying the direction.

## 6. C Is an Active Context

C is not an empty carrier. Its content determines how the principle should be expressed.

The same transferable direction may require different concrete actions in different targets.

## 7. One Pair Is Limited Evidence

A single contrast pair may change many variables simultaneously.

When causality is ambiguous:

- keep low-confidence claims explicit;
- prefer mechanisms supported by multiple observations;
- transfer conservatively;
- use additional A/B pairs when available.

If multiple comparable A/B pairs point in the same direction, shared deltas become stronger evidence.
