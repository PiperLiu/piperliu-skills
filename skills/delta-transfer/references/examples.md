# Examples

## Example 1 — Anime / Cinematic Interpretation

### Inputs

- **A**: a weaker adaptation of the same manga moment.
- **B**: the preferred adaptation.
- **C**: a different scene the user wants to improve.

### Bad transfer

```text
B uses a low camera angle, blue-gray palette, and empty street.
Therefore C should use a low camera angle, blue-gray palette, and empty street.
```

This copies B.

### Better delta extraction

Suppose inspection suggests:

```text
A:
- presents all narrative information immediately
- centers the character
- keeps foreground/background equally readable
- emotional cue is explicit

B:
- withholds part of the information
- isolates the character with negative space
- uses depth and occlusion to create a reveal
- lets posture and staging carry emotion
```

Possible transferable delta:

```text
Increase:
- visual hierarchy
- information withholding
- environmental participation in emotion

Reduce:
- centered explanatory staging
- simultaneous readability of every element
- explicit emotional signaling

Adapt:
- use C's own environment to create isolation/tension
- choose framing appropriate to C's action, not B's literal camera angle
```

---

## Example 2 — Writing

### A

> The launch went badly because several systems failed at the same time. The team was stressed and had to work quickly to fix the issues.

### B

> At 09:02 the checkout queue stopped draining. Three minutes later, support tickets doubled. By 09:11, the team had disabled the new payment path.

Possible delta:

```text
abstract → concrete
conclusion-first → evidence-first
generic emotional labeling → observable consequences
weak temporal structure → explicit sequence
```

### C

> The migration was difficult and caused many problems, but the engineers eventually resolved them.

A delta-transferred version could become:

> The first batch stalled after 18,000 objects. Retry traffic then saturated the source connection, and the second worker began timing out. The team cut concurrency, resumed from the last checkpoint, and completed the remaining objects without restarting the migration.

---

## Example 3 — UI

### A

A settings screen exposes 24 controls with equal weight.

### B

The preferred redesign:

- shows three common controls;
- groups advanced controls behind disclosure;
- makes destructive actions visually separate;
- provides immediate preview.

### Delta

```text
increase:
- hierarchy
- progressive disclosure
- consequence visibility

reduce:
- simultaneous choice load
- destructive-action adjacency
```

### C

C is a photo export dialog.

Do not copy B's exact layout.

Apply the mechanism:

- keep destination, format, and export as primary;
- collapse metadata and naming rules under Advanced;
- isolate destructive overwrite behavior;
- show a small output preview or summary.

---

## Example 4 — Code / Architecture

### A

A feature requires callers to coordinate cache lookup, parsing, validation, fallback, and error mapping.

### B

A preferred implementation moves those mechanics behind one domain-shaped interface.

### Delta

```text
increase:
- locality
- interface depth
- ownership of failure handling

reduce:
- caller orchestration
- duplicated policy
- leaked implementation detail
```

### C

C is a thumbnail subsystem with a different domain model.

Do not copy B's class hierarchy. Apply the architectural direction through C's own natural interface.

---

## Example 5 — Weak Pair

A and B are two posters for different products, audiences, and campaign goals.

B looks better to the user.

The skill should not pretend this is a controlled comparison:

```text
The pair changes too many variables to infer one reliable improvement direction.
I can extract a few low-confidence hypotheses, or we can use a more comparable A/B pair.
```
