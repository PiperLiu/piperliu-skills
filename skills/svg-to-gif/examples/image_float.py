"""Float an optional sibling asset.png/asset.jpg; fallback is vector artwork.

Copy this scene into a project and place one licensed/generated image beside it.
Embedding bytes makes frames independent of the renderer's temporary directory.
"""
import base64
import math
from pathlib import Path


def artwork():
    for name, mime in (("asset.png", "image/png"), ("asset.jpg", "image/jpeg")):
        path = Path(__file__).with_name(name)
        if path.is_file():
            encoded = base64.b64encode(path.read_bytes()).decode("ascii")
            return (f'<image x="-110" y="-110" width="220" height="220" '
                    f'preserveAspectRatio="xMidYMid meet" '
                    f'xlink:href="data:{mime};base64,{encoded}"/>')
    return ('<rect x="-90" y="-90" width="180" height="180" rx="48" fill="#a6dcd4"/>'
            '<circle cx="-28" cy="-8" r="9" fill="#132c33"/>'
            '<circle cx="28" cy="-8" r="9" fill="#132c33"/>'
            '<path d="M-28 28q28 30 56 0" fill="none" stroke="#132c33" stroke-width="7" '
            'stroke-linecap="round"/>')


ARTWORK = artwork()


def svg_frame(t):
    phase = math.tau * t
    y = 186 + 12 * math.sin(phase)
    rotation = 4 * math.cos(phase)
    shadow = 82 + 5 * math.sin(phase)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
      width="600" height="400" viewBox="0 0 600 400">
      <rect width="600" height="400" fill="#f5ecdb"/>
      <ellipse cx="300" cy="324" rx="{shadow:.3f}" ry="10" fill="#d5c9b3"/>
      <g transform="translate(300 {y:.3f}) rotate({rotation:.3f})">{ARTWORK}</g>
    </svg>'''
