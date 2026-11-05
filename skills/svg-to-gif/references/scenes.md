# Authoring SVG scenes

This reference applies after selecting the SVG-to-GIF pipeline. It describes that stage's scene format and asset handling; choose other tools for 3D rendering, image/video generation, or other production stages according to their own requirements.

## Contract

A scene is a trusted Python `.py` file exporting `svg_frame(t) -> str`. The renderer samples `t = frame_index / frame_count`, covering `[0, 1)` without duplicating the endpoint. Return a complete static SVG with explicit width, height, and viewBox. For a seamless loop, values and preferably velocities should agree at 0 and 1. Use time-derived motion; do not accumulate state each time the function is called because size search renders the scene multiple times.

```python
import math

def svg_frame(t):
    x = 160 + 90 * math.cos(math.tau * t)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="320" height="200" viewBox="0 0 320 200">
      <rect width="320" height="200" fill="#132c33"/>
      <circle cx="{x:.3f}" cy="100" r="18" fill="#f7c877"/>
    </svg>'''
```

Copy an example to the output project before editing. Keep scene geometry, assets, and animation parameters there; the renderer belongs to the skill. For randomized layouts, generate a fixed seeded sample once and animate its parameters. Avoid importing packages unless they materially help the scene and their installation has been authorized.

resvg renders static SVG: CSS/SMIL animation, JavaScript, browser layout, and `foreignObject` are not this pipeline. Compute the animated state in Python. Escape user-supplied labels with `html.escape`. Use a background rectangle for predictable opaque GIFs. GIF has limited color and binary transparency; gradients, soft transparent edges, photographic backgrounds, and camera movement often increase size substantially.

Font fallback varies across systems. Inspect the actual render, especially CJK labels and mathematical notation. Use fonts already available or request an authorized font asset; for strict portability use paths for critical lettering. This pipeline does not typeset LaTeX by itself. Do not install a TeX distribution merely to render a small label without discussing that footprint.

## Local or generated images

If the harness provides image generation and the task benefits from illustrated assets, use its documented generation/editing workflow. Save the returned asset to the project, retain its provenance, and animate stable transforms such as translation, rotation, scale, clipping, or reveals. The image tool is optional; the skill also works entirely with local SVG geometry. A request to create an animation does not automatically choose a paid external image service.

`examples/image_float.py` looks for `asset.png` or `asset.jpg` next to its own source and embeds it as a data URI, otherwise displaying a vector fallback. This example demonstrates the full connection without a network dependency. Transparent PNG is useful for cutout characters; match the canvas background to avoid edge halos in GIF.

Do not reference local images relative to temporary frame paths: the SVG frames are written in a temporary directory. Resolve sources relative to `Path(__file__).parent`, load them once, and embed their bytes. Keep the original files for future edits and record their hashes in the project's asset record; the render sidecar hashes the scene, not every file arbitrary Python code could read. Base64 increases intermediate SVG size, so resize very large assets beforehand using an existing approved tool when useful.

## MathAnimKit example

`examples/portfolio.py` preserves the source toolkit's deterministic correlated point cloud and four-phase weight/correlation loop. The encoder is now separate. The depicted orange points are orthogonal projections onto `u = w / ||w||`. Portfolio return is `w · r = ||w|| (r · u)`; it is not simply the projection length. The fixed random sample illustrates the correlation construction and does not have an exactly prescribed sample correlation.

## Preview criteria

Inspect the start, middle, turning points, and transition back to the start. Saved quarter-cycle SVG keyframes aid editing; for real raster quality, extract frames from the final GIF with the selected FFmpeg into a temporary preview directory and view them. Check moving parts for collisions/clipping, labels at the selected output size, and the intended relationship between motion and meaning. Preview the GIF itself where the harness supports playback; still frames cannot prove timing quality.
