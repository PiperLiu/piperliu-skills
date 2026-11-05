# Rendering and size control

Use a Python 3.9+ interpreter and absolute paths when not in the skill directory. Paths with spaces must be quoted. Windows PowerShell can use `py -3` or `& "C:\path\python.exe"` with the same script arguments. No shell-specific tools are invoked by the Python pipeline.

```sh
python3 scripts/animation_tools.py --output /path/to/project/toolchain.json
python3 scripts/render_animation.py --scene /path/to/project/scene.py --output /path/to/project/loop.gif --width 480 --fps 10 --seconds 6 --colors 32 --target-kib 400 --strict-target --keep-keyframes
```

Select side-by-side binaries with `--resvg /path/to/resvg --ffmpeg /path/to/ffmpeg`. Optional optimization uses the selected/PATH gifsicle; `--no-gifsicle` gives an explicitly unoptimized run. The probe and render accept the same executable-selection flags. A provided path always identifies the intended tool; it must not trigger an installation or fallback replacement.

To check for drift before rendering:

```sh
python3 scripts/render_animation.py --scene /path/to/project/scene.py --output /path/to/project/revision.gif --require-toolchain /path/to/project/loop.gif.json
```

Use the same selection flags as the baseline, including `--no-gifsicle` when applicable. `animation_tools.py --compare` compares two standalone probe reports; it exits 2 on drift. Reports record identities, not a request to restore them by modifying the machine.

## Parameters

| Option | Meaning |
| --- | --- |
| `--scene` | Required trusted Python scene exporting `svg_frame(t)`. |
| `--output` | Required `.gif` destination. |
| `--width` | 100–2000 pixels, default 560; SVG aspect ratio sets height. |
| `--fps` | Integer 3–50, default 10. GIF delays use centiseconds; rates such as 10, 20, 25, or 50 divide that timebase evenly. |
| `--seconds` | 1–60, default 6; frame count is rounded from seconds × fps. Actual encoded timing is in the report. |
| `--colors` | 4–256, default 48; palette generation budget, including any reserved transparency entry. |
| `--target-kib` | Positive size goal; 1 KiB = 1024 bytes. Up to five distinct attempts, progressively reducing dimensions, fps, and palette. |
| `--strict-target` | Requires a size goal; exit 2 when unmet, preserving the smallest candidate and report. |
| `--keep-keyframes` | Save four editable SVGs in `<output>.keyframes/`. |
| `--overwrite` | Explicitly allow replacing the GIF, JSON sidecar, and named SVG keyframes. Default refuses collisions. |
| `--require-toolchain` | Refuse dependency identity drift relative to a probe report or render sidecar before loading the scene. |

## Output and failure semantics

A successful render writes `loop.gif`, `loop.gif.json`, and optional `loop.gif.keyframes/keyframe_1.svg` through `keyframe_4.svg`. Temporary PNG frames are removed. The JSON includes requested and selected parameters, each attempt's byte size, actual encoded dimensions/frame delays/duration/loop count, target status, scene/renderer hashes, and toolchain identities. It is provenance for local reproduction; preserve scene assets separately.

The search retains the smallest completed candidate, which need not be the last attempt. It stops as soon as an attempt reaches the budget. This is a bounded heuristic, not a guarantee of optimal compression. It does not shorten the requested story or remove visual content automatically. Reducing frame rate changes sampling and may slightly change rounded duration; inspect the reported encoded timing.

Exit codes: render `0` means encoded successfully (in best-effort mode a budget can still be unmet); `2` means strict budget unmet or command-line usage error; `1` means dependency, scene, toolchain, or render failure. Read the report's `target_met` and stderr to distinguish outcomes. Probe `0` means required capabilities pass, `1` means a required dependency fails, and `2` means comparison drift or command-line usage error.

Existing outputs are checked before executing the scene and again before publication. Candidate files remain temporary until encoding is complete. Publication is per file; an I/O failure during final writes can leave a partial set, so confirm that the GIF and sidecar both exist and match before delivery. `--overwrite` replaces only named output files; it does not delete unrelated files in a keyframe directory.

## Choosing a useful budget

Prefer flat backgrounds, limited moving regions, short loops, and a small intentional palette. Width, fps, and duration are the main tradeoffs. This implementation uses a global palette and no dithering, a good starting point for clean diagrams and icons; inspect photographic or gradient-heavy scenes for banding. An optional gifsicle pass is retained only if smaller and canvas/timing/loop metadata is preserved.

If a hard platform limit uses decimal bytes, convert explicitly (for example 400,000 bytes ÷ 1024 = 390.625 KiB). Use `--strict-target`. When the smallest result still misses, report its actual size, revise the scene or settings, and rerender to a new file. If the delivery platform supports video, a separate MP4/WebM workflow may suit continuous imagery better; this renderer currently exports GIF only, so agree on that format change instead of silently substituting it.
