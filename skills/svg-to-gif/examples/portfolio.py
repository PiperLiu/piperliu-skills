"""Deterministic portfolio-projection scene adapted from MathAnimKit.

See references/scenes.md for the distinction between projection and return.
"""
import math
import random

VW, VH = 600, 420
CX, CY = 300, 195
SX, SY = 100, 90
RANDOM = random.Random(2026)
LATENT = [(RANDOM.gauss(0, 1), RANDOM.gauss(0, 1)) for _ in range(40)]


def smooth(t):
    t = max(0., min(1., t))
    return t * t * (3. - 2. * t)


def state(t):
    """Cycle: change weight, correlation, weight, correlation in four smooth phases."""
    k = (t % 1) * 4
    phase, local = min(3, int(k)), smooth(k - int(k))
    if phase == 0:
        return 0.85 - 0.45 * local, 0.7
    if phase == 1:
        return 0.4, 0.7 - 1.4 * local
    if phase == 2:
        return 0.4 + 0.45 * local, -0.7
    return 0.85, -0.7 + 1.4 * local


def fmt(n):
    return f'{n:.2f}'


def svg_frame(t):
    weight, corr = state(t)
    ux, uy = weight, 1 - weight
    norm = math.hypot(ux, uy)
    ux, uy = ux/norm, uy/norm

    def pos(x, y):
        return fmt(CX + x*SX), fmt(CY - y*SY)

    def line(x1, y1, x2, y2, color, width=1, opacity=1):
        return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                f'stroke="{color}" stroke-width="{width}" stroke-opacity="{opacity}"/>')

    connectors, dots, projections = [], [], []
    for a, b in LATENT:
        # Same underlying observations across every frame. Only correlation changes.
        x = a * 1.15
        y = (corr*a + math.sqrt(max(0, 1-corr*corr))*b) * 1.15
        p = x*ux + y*uy
        qx, qy = p*ux, p*uy
        x1, y1 = pos(x, y)
        x2, y2 = pos(qx, qy)
        connectors.append(line(x1, y1, x2, y2, '#0c665f', 1.4, 0.35))
        dots.append(f'<circle cx="{x1}" cy="{y1}" r="4.1" fill="#159c89"/>')
        projections.append(f'<circle cx="{x2}" cy="{y2}" r="3.3" fill="#e49b30"/>')

    x1,y1=pos(-4*ux,-4*uy)
    x2,y2=pos(4*ux,4*uy)
    axis = line(x1,y1,x2,y2,'#e49b30',4,1)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{VW}" height="{VH}" viewBox="0 0 {VW} {VH}">
  <defs><clipPath id="plot"><rect x="32" y="43" width="536" height="303" rx="14"/></clipPath></defs>
  <rect width="600" height="420" fill="#101112"/>
  <rect x="32" y="43" width="536" height="303" rx="14" fill="#141718"/>
  <g clip-path="url(#plot)">
    <path d="M32 195H568 M300 43V346" stroke="#666b6f" stroke-width="1.4"/>
    {''.join(connectors)}
    {axis}
    {''.join(dots)}
    {''.join(projections)}
    <circle cx="300" cy="195" r="4.4" fill="#f4f4f4"/>
  </g>
  <g font-family="Arial, Helvetica, sans-serif">
    <text x="560" y="183" font-size="18" fill="#f0f0f0" text-anchor="end">A</text>
    <text x="312" y="62" font-size="18" fill="#f0f0f0">B</text>
    <text x="45" y="29" font-size="16" font-weight="600" fill="#f0f0f0">Portfolio projection</text>
    <circle cx="47" cy="368" r="5" fill="#159c89"/>
    <text x="59" y="373" font-size="14" fill="#dedede">returns</text>
    <circle cx="163" cy="368" r="5" fill="#e49b30"/>
    <text x="175" y="373" font-size="14" fill="#dedede">projections</text>
    <text x="554" y="373" text-anchor="end" font-size="14" fill="#e49b30">w direction</text>
    <text x="45" y="403" font-size="14" fill="#e5e5e5">A: {weight*100:3.0f}%    B: {(1-weight)*100:3.0f}%</text>
    <text x="555" y="403" font-size="14" text-anchor="end" fill="#e5e5e5">correlation: {corr:+.2f}</text>
  </g>
</svg>'''

