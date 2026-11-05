---
name: svg-to-gif
description: Render scripted 2D SVG frames into size-controlled looping GIFs using Python, resvg, and FFmpeg. Use when the user requests SVG-to-GIF or this SVG frame pipeline has already been selected for the task. Generic animation, GIF compression, image generation, 3D rendering, and video generation/editing requests alone do not trigger this skill.
---

# SVG to GIF

Render procedural SVG scenes through Python → static SVG frames → resvg → PNG → FFmpeg → GIF. Adapted from MathAnimKit; the scene is independent of the renderer. This pipeline requires no Manim, Node.js, browser, or Python packages. The scripts target macOS, Linux, and Windows with Python 3.9+ and compatible native executables.

## Scope and routing

Select the production approach from the user's intended visual result before using this skill. Its availability is not a reason to choose SVG. Activate it for an explicitly requested SVG-to-GIF workflow, or after independently selecting procedural 2D SVG frames as an appropriate way to produce the requested GIF.

- Use it for editable diagrams, icons, or image-asset compositions whose animation is authored as SVG frames and whose delivery format is GIF.
- A request for a small animation or a size-limited GIF alone is insufficient. Existing video or raster frame sequences can use their native conversion workflow without an SVG intermediate.
- Keep 3D modeling/rendering, generated images or video, camera/lighting work, and existing animation projects in the tools appropriate to those tasks. Do not flatten or simplify the requested result to fit this renderer.
- In mixed workflows, apply these instructions only to the selected SVG-to-GIF stage. Generated or 3D-rendered imagery can be an asset in that stage if useful; this does not constrain how the asset itself is created. Reconsider the approach if the desired motion exceeds what the SVG stage expresses well.

## Required workflow

1. Confirm that the selected stage fits the scope above. Infer its output location, duration, dimensions, loop behavior, and any hard size limit from the request. Resolve only consequential omissions.
2. Inspect the environment before rendering. Run `scripts/animation_tools.py` with an available Python 3.9+ interpreter. It reports executable paths, versions, hashes, and actual rendering/encoding capability. Use explicit `--resvg`, `--ffmpeg`, and optional `--gifsicle` paths when the project has selected tools. Do not treat an old version number alone as incompatibility.
3. If required tools are absent or fail the probe, follow [dependency setup](references/dependencies.md). **Ask before installing or downloading missing tools, including isolated copies, unless that specific change is already authorized.** State the proposed version, source, destination, and environmental effects. Never silently upgrade, uninstall, replace an executable, alter global PATH/shell profiles, or invoke a package manager to repair the environment. Optional gifsicle is not a blocker.
4. Create a project-owned scene using [the scene contract](references/scenes.md). Copy an example as a starting point; do not edit installed skill files for each animation. Review Python scenes before executing them: a scene is trusted executable code, not sandboxed data. Use deterministic motion and seeds. For image assets inside the SVG scene, follow the asset tool's native workflow and reuse stable artwork across frames when appropriate. Asset generation remains outside this skill's scope; do not assume a particular harness.
5. Render using [the CLI guide](references/rendering.md). Preserve source and inputs. With a target size, inspect the chosen attempt and quality at its actual dimensions. If a hard limit is unmet, report it and revise meaningful visual choices; do not claim success merely because a GIF exists.
6. Preview representative frames and the loop seam. Verify legibility, intended motion, duration, background/transparency, actual bytes, and any factual relationships. Deliver the GIF, editable scene/assets, and render report. Report which settings changed to meet the budget. Do not claim cross-platform execution was tested on platforms you have not run.

## Quick start

Commands below run from the skill directory; use absolute script/scene paths when working elsewhere. On Windows select an installed Python 3 interpreter (for example `py -3`) instead of assuming `python3` exists.

```sh
python3 scripts/animation_tools.py
python3 scripts/render_animation.py --scene examples/orbit.py --output /path/to/project/orbit.gif --width 480 --fps 10 --seconds 4 --colors 32 --target-kib 400 --keep-keyframes
```

The scripts never install dependencies. A missing tool stops the render. Existing outputs require explicit `--overwrite`. The JSON sidecar records the selected toolchain and encoding result. For later renders, `--require-toolchain /path/to/previous.gif.json` checks for dependency drift before running the scene; a mismatch requires a decision, not an automatic upgrade.

## Resources and validation

- [Dependency setup](references/dependencies.md): read for missing/incompatible tools, side-by-side versions, or reproducibility.
- [Scenes and image assets](references/scenes.md): read when authoring scenes or incorporating generated imagery.
- [Rendering and size control](references/rendering.md): CLI, output contracts, quality tradeoffs, and failure handling.
- `examples/orbit.py`: minimal non-mathematical loop with no font or image dependency.
- `examples/portfolio.py`: original mathematical scene extracted from MathAnimKit; interpret its projection correctly as described in the scene guide.
- `examples/image_float.py`: optional local PNG/JPEG asset embedded in SVG; contains a vector fallback so it also runs without an image.
- Run `python3 -m unittest discover -s tests -v` for deterministic regression tests. With dependencies available, render the examples into a temporary directory and inspect the GIF and report. Tests with simulated tools do not replace a real encode.
