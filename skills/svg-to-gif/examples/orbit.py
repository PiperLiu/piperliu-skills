"""A small orbiting icon: no fonts, external assets, or randomness."""
import math


def svg_frame(t):
    angle = math.tau * t
    x, y = 300 + 176 * math.cos(angle), 190 + 92 * math.sin(angle)
    pulse = 1 + .06 * math.sin(angle)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="380" viewBox="0 0 600 380">
      <rect width="600" height="380" rx="32" fill="#132c33"/>
      <ellipse cx="300" cy="190" rx="176" ry="92" fill="none" stroke="#57767b" stroke-width="2"/>
      <g transform="translate(300 190) scale({pulse:.5f})">
        <rect x="-46" y="-46" width="92" height="92" rx="28" fill="#f7c877"/>
        <path d="M-20 0h40M0-20v40" stroke="#132c33" stroke-width="8" stroke-linecap="round"/>
      </g>
      <circle cx="{x:.4f}" cy="{y:.4f}" r="17" fill="#a6dcd4"/>
      <circle cx="{x:.4f}" cy="{y:.4f}" r="7" fill="#132c33"/>
    </svg>'''
