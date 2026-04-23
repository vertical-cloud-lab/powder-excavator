"""
Generate the four design subpanels and the mechanism animation for the
powder-excavator, in the **corrected longitudinal-pivot / sideways-tilt**
geometry that incorporates the Edison Scientific design-review feedback
(see ``docs/edison/analysis-v2-corrected-gondola.md``).

Outputs (all under ``docs/figures/``):

* ``panel-A-orthographic.svg``  -- end / side / top views, dimensions
* ``panel-B-pivot-detail.svg``  -- close-up of one end-cap pivot boss + pin
* ``panel-C-isometric.svg``     -- 3D / isometric of the assembly on a gantry
* ``panel-D-mechanism.svg``     -- 4-step mechanism (J-plunge -> strike-off
                                   -> transport -> sideways tilt against cam)
* ``mechanism.gif``             -- animation of the cam-engagement + sideways
                                   tilt step

The script is intentionally a single, self-contained file so the figure set
can be regenerated with one command after geometry tweaks::

    python scripts/generate_figures.py

It depends only on the Python standard library, ``cairosvg``, and ``Pillow``;
``cairosvg`` is used purely to rasterise the per-frame SVGs of the animation
into PNG bytes that ``Pillow`` then concatenates into an animated GIF.
"""

from __future__ import annotations

import io
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = REPO_ROOT / "docs" / "figures"

# ---------------------------------------------------------------------------
# Shared SVG building blocks
# ---------------------------------------------------------------------------

SVG_DEFS = """\
  <defs>
    <linearGradient id="metal" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"   stop-color="#dfe4ea"/>
      <stop offset="0.5" stop-color="#aab2bd"/>
      <stop offset="1"   stop-color="#7e8794"/>
    </linearGradient>
    <linearGradient id="metalH" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0"   stop-color="#dfe4ea"/>
      <stop offset="0.5" stop-color="#aab2bd"/>
      <stop offset="1"   stop-color="#7e8794"/>
    </linearGradient>
    <pattern id="powder" width="6" height="6" patternUnits="userSpaceOnUse">
      <rect width="6" height="6" fill="#e8d9a8"/>
      <circle cx="1.5" cy="1.5" r="0.6" fill="#b89a55"/>
      <circle cx="4"   cy="3.5" r="0.6" fill="#b89a55"/>
      <circle cx="2"   cy="5"   r="0.5" fill="#b89a55"/>
    </pattern>
    <marker id="arrowK" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#222"/>
    </marker>
    <marker id="arrowB" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#1f5fbf"/>
    </marker>
    <marker id="arrowR" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#c0392b"/>
    </marker>
  </defs>
"""


def _svg_open(width: int, height: int, font_size: int = 13) -> str:
    return (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="Helvetica, Arial, sans-serif" font-size="{font_size}">\n'
        f"{SVG_DEFS}"
    )


def _svg_close() -> str:
    return "</svg>\n"


# ---------------------------------------------------------------------------
# Trough cross-section primitive
# ---------------------------------------------------------------------------
#
# The trough cross-section (looking along its long axis L) is a half-cylinder
# with a smooth chamfered bumper on the outside of the rim.  When the trough
# rolls about its longitudinal pivot pin (the corrected v2 geometry), this is
# the cross-section that visually rotates in the side / end view.

def trough_cross_section(
    cx: float,
    cy: float,
    radius: float,
    rotate_deg: float = 0.0,
    powder_fill_frac: float = 1.0,
    *,
    bumper: bool = True,
) -> str:
    """Return SVG for the trough cross-section, rolled by ``rotate_deg`` about
    its central pivot axis.

    The semicircle's flat (open) edge runs across the top when ``rotate_deg=0``;
    positive ``rotate_deg`` rolls the trough so its right rim drops (pouring
    direction).
    """
    r = radius
    shell = (
        f'M {-r} 0 L {r} 0 '
        f'A {r} {r} 0 0 1 {-r} 0 Z'
    )
    fill_h = r * powder_fill_frac
    powder_path = (
        f'M {-r * 0.985} {r - fill_h} L {r * 0.985} {r - fill_h} '
        f'A {r * 0.985} {r * 0.985} 0 0 1 {-r * 0.985} {r - fill_h} Z'
    )
    parts = [
        f'<g transform="translate({cx},{cy}) rotate({rotate_deg})">',
        f'  <path d="{shell}" fill="url(#metal)" stroke="#222" stroke-width="2"/>',
        f'  <path d="{powder_path}" fill="url(#powder)" opacity="0.95"/>',
    ]
    if bumper:
        # Smooth chamfered "bumper" / rounded lip on the right rim — the
        # surface that slides up the cam track.
        parts.append(
            f'  <path d="M {r} 0 L {r + 6} -2 L {r + 6} 4 L {r} 6 Z" '
            f'fill="#7e8794" stroke="#222" stroke-width="1.2"/>'
        )
    parts.append("</g>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Panel A — Orthographic
# ---------------------------------------------------------------------------

def panel_A() -> str:
    W, H = 1200, 720
    s = [_svg_open(W, H)]
    s.append(
        f'<text x="{W//2}" y="34" text-anchor="middle" font-size="22" font-weight="700">'
        "Subpanel A — Orthographic views (end, side, top)</text>"
    )
    s.append(
        f'<text x="{W//2}" y="56" text-anchor="middle" font-size="13" fill="#555" font-style="italic">'
        "longitudinal pivot axis along L; arms grip the two short end caps; trough rolls SIDEWAYS to pour</text>"
    )

    # End view (looking down the long axis L) — leftmost
    g_end_x, g_end_y = 60, 110
    s.append(f'<g transform="translate({g_end_x},{g_end_y})">')
    s.append('<text x="160" y="0" text-anchor="middle" font-size="16" font-weight="600">End view (along L)</text>')
    s.append('<rect x="155" y="20" width="10" height="160" fill="url(#metal)" stroke="#333"/>')
    s.append('<text x="170" y="35" font-size="11" fill="#444">arm (one of two,</text>')
    s.append('<text x="170" y="49" font-size="11" fill="#444">on the end cap)</text>')
    R = 60
    cx, cy = 160, 180
    s.append(trough_cross_section(cx, cy, R, rotate_deg=0, powder_fill_frac=0.85))
    s.append(f'<circle cx="{cx}" cy="{cy}" r="6" fill="#c0392b" stroke="#7a1f15" stroke-width="1.5"/>')
    s.append(f'<text x="{cx + 12}" y="{cy + 4}" font-size="11" fill="#c0392b">pivot pin (end-on)</text>')
    s.append(f'<line x1="{cx - R}" y1="{cy + R + 30}" x2="{cx + R}" y2="{cy + R + 30}" '
             'stroke="#222" stroke-width="1.2" marker-start="url(#arrowK)" marker-end="url(#arrowK)"/>')
    s.append(f'<text x="{cx}" y="{cy + R + 50}" text-anchor="middle" font-size="13">D ≈ 27 mm</text>')
    s.append('</g>')

    # Side view (looking perpendicular to L, from the long side) — middle
    g_side_x, g_side_y = 430, 110
    s.append(f'<g transform="translate({g_side_x},{g_side_y})">')
    s.append('<text x="200" y="0" text-anchor="middle" font-size="16" font-weight="600">Side view (looking at long side)</text>')
    L_px = 320
    arm_h = 140
    arm_top = 20
    for ax in (40, 40 + L_px):
        s.append(f'<rect x="{ax - 6}" y="{arm_top}" width="12" height="{arm_h}" fill="url(#metal)" stroke="#333"/>')
    body_top = arm_top + arm_h - 20
    body_h = 60
    s.append(
        f'<path d="M 40 {body_top} '
        f'L {40 + L_px} {body_top} '
        f'L {40 + L_px} {body_top + 10} '
        f'Q {40 + L_px / 2} {body_top + body_h} '
        f'40 {body_top + 10} Z" '
        f'fill="url(#metalH)" stroke="#222" stroke-width="2"/>'
    )
    s.append(
        f'<path d="M 50 {body_top + 4} L {30 + L_px} {body_top + 4} '
        f'L {30 + L_px} {body_top + 12} Q {40 + L_px / 2} {body_top + body_h - 6} '
        f'50 {body_top + 12} Z" fill="url(#powder)" opacity="0.95"/>'
    )
    pin_y = body_top + 8
    s.append(f'<line x1="28" y1="{pin_y}" x2="{40 + L_px + 12}" y2="{pin_y}" '
             'stroke="#c0392b" stroke-width="3"/>')
    s.append(f'<text x="{40 + L_px / 2}" y="{pin_y - 6}" text-anchor="middle" font-size="11" fill="#c0392b">'
             'longitudinal pivot pin (axis ∥ L, runs through both end caps)</text>')
    s.append(f'<line x1="40" y1="{body_top + body_h + 30}" x2="{40 + L_px}" y2="{body_top + body_h + 30}" '
             'stroke="#222" stroke-width="1.2" marker-start="url(#arrowK)" marker-end="url(#arrowK)"/>')
    s.append(f'<text x="{40 + L_px / 2}" y="{body_top + body_h + 50}" text-anchor="middle" font-size="13">L ≈ 3 D ≈ 80 mm</text>')
    for bx in (52, 28 + L_px):
        s.append(f'<path d="M {bx} {body_top} L {bx + 16} {body_top - 5} L {bx + 16} {body_top + 4} L {bx} {body_top + 4} Z" '
                 'fill="#7e8794" stroke="#222" stroke-width="1.2"/>')
    s.append(f'<text x="{40 + L_px / 2}" y="{body_top - 12}" text-anchor="middle" font-size="11" fill="#444">'
             'chamfered bumper (one per end) — slides up the cam track</text>')
    s.append('</g>')

    # Top view — rightmost
    g_top_x, g_top_y = 880, 110
    s.append(f'<g transform="translate({g_top_x},{g_top_y})">')
    s.append('<text x="130" y="0" text-anchor="middle" font-size="16" font-weight="600">Top view</text>')
    L_top = 220
    W_top = 50
    s.append(f'<rect x="20" y="40" width="{L_top}" height="{W_top}" fill="url(#metalH)" stroke="#222" stroke-width="2"/>')
    s.append(f'<rect x="26" y="46" width="{L_top - 12}" height="{W_top - 12}" fill="url(#powder)" opacity="0.95"/>')
    s.append(f'<line x1="8" y1="{40 + W_top / 2}" x2="{20 + L_top + 12}" y2="{40 + W_top / 2}" '
             'stroke="#c0392b" stroke-width="2.5" stroke-dasharray="6 4"/>')
    s.append(f'<text x="{20 + L_top / 2}" y="{40 + W_top + 18}" text-anchor="middle" font-size="11" fill="#c0392b">'
             'pivot pin axis (along centre line of trough length)</text>')
    for ax in (8, 20 + L_top):
        s.append(f'<rect x="{ax - 6}" y="{40 - 6}" width="12" height="{W_top + 12}" fill="url(#metal)" stroke="#333"/>')
    s.append(f'<text x="-4" y="32" font-size="11" fill="#444">arms grip the two end caps</text>')
    s.append(f'<line x1="{20 + L_top / 2 - 50}" y1="{40 + W_top + 50}" '
             f'x2="{20 + L_top / 2 + 50}" y2="{40 + W_top + 50}" stroke="#5a4a30" stroke-width="6"/>')
    s.append(f'<text x="{20 + L_top / 2}" y="{40 + W_top + 70}" text-anchor="middle" font-size="11" fill="#5a4a30">'
             'fixed strike-off bar (bed-edge mounted)</text>')
    s.append('</g>')

    s.append(
        f'<text x="{W//2}" y="{H - 60}" text-anchor="middle" font-size="13" fill="#444" font-style="italic">'
        "The pivot pin runs along the trough's LONG axis L (not across its width).  Arms grip the two end caps,"
        "</text>"
    )
    s.append(
        f'<text x="{W//2}" y="{H - 40}" text-anchor="middle" font-size="13" fill="#444" font-style="italic">'
        "so when the trough rolls about the pin it pours over the FULL 80 mm long edge — eliminating the narrow-bottleneck"
        "</text>"
    )
    s.append(
        f'<text x="{W//2}" y="{H - 20}" text-anchor="middle" font-size="13" fill="#444" font-style="italic">'
        "and trapped-volume problems of an end-over-end tilt of a half-cylinder (Edison analysis-v2 §3)."
        "</text>"
    )
    s.append(_svg_close())
    return "".join(s)


# ---------------------------------------------------------------------------
# Panel B — Pivot detail
# ---------------------------------------------------------------------------

def panel_B() -> str:
    W, H = 900, 600
    s = [_svg_open(W, H)]
    s.append(
        f'<text x="{W//2}" y="34" text-anchor="middle" font-size="22" font-weight="700">'
        "Subpanel B — Pivot pin / end-cap detail (longitudinal axis)</text>"
    )
    s.append(
        f'<text x="{W//2}" y="56" text-anchor="middle" font-size="13" fill="#555" font-style="italic">'
        "single horizontal pin runs ALONG L, through both end caps and both arms; quick-release to swap troughs"
        "</text>"
    )
    cx, cy, R = 350, 320, 130
    s.append(f'<path d="M {cx - R} {cy} L {cx + R} {cy} A {R} {R} 0 0 1 {cx - R} {cy} Z" '
             'fill="url(#metal)" stroke="#222" stroke-width="2.5"/>')
    s.append(f'<text x="{cx}" y="{cy + R + 30}" text-anchor="middle" font-size="12" fill="#444">'
             'trough end cap (cross-section, looking down L)</text>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="20" fill="#7e8794" stroke="#222" stroke-width="2"/>')
    s.append(f'<text x="{cx + 28}" y="{cy - 24}" font-size="11" fill="#444">pivot boss (printed</text>')
    s.append(f'<text x="{cx + 28}" y="{cy - 12}" font-size="11" fill="#444">into end cap)</text>')
    s.append(f'<rect x="{cx - 8}" y="{cy - 200}" width="16" height="180" fill="url(#metal)" stroke="#333"/>')
    s.append(f'<text x="{cx + 18}" y="{cy - 160}" font-size="12" fill="#444">arm (one of two; bolted to gantry carriage)</text>')
    s.append(f'<line x1="{cx - 80}" y1="{cy}" x2="{cx + 90}" y2="{cy}" stroke="#c0392b" stroke-width="6"/>')
    s.append(f'<circle cx="{cx + 95}" cy="{cy}" r="6" fill="#c0392b" stroke="#7a1f15" stroke-width="1.5"/>')
    s.append(f'<text x="{cx + 105}" y="{cy + 5}" font-size="12" fill="#c0392b">pin (along L)</text>')
    s.append(f'<path d="M {cx + 100} {cy - 18} q 14 18 0 36" fill="none" stroke="#c0392b" stroke-width="2"/>')
    s.append(f'<text x="{cx + 110}" y="{cy + 30}" font-size="11" fill="#c0392b">e-clip / retaining ring</text>')
    com_y = cy + 38
    s.append(f'<line x1="{cx - 7}" y1="{com_y}" x2="{cx + 7}" y2="{com_y}" stroke="#222" stroke-width="1.6"/>')
    s.append(f'<line x1="{cx}" y1="{com_y - 7}" x2="{cx}" y2="{com_y + 7}" stroke="#222" stroke-width="1.6"/>')
    s.append(f'<circle cx="{cx}" cy="{com_y}" r="9" fill="none" stroke="#222" stroke-width="1.2"/>')
    s.append(f'<text x="{cx + 16}" y="{com_y + 5}" font-size="11" fill="#222">centre of mass (loaded)</text>')
    s.append(f'<text x="{cx - 240}" y="{cy + 100}" font-size="12" fill="#222">'
             'pivot pin sits ~3 mm above loaded COM</text>')
    s.append(f'<text x="{cx - 240}" y="{cy + 116}" font-size="12" fill="#222">'
             '→ gravity returns trough to "open-up" (stable pendulum)</text>')
    s.append(f'<text x="{cx - 240}" y="{cy + 152}" font-size="11" fill="#5a3a8a">'
             'metal pivot pin doubles as ground path for an</text>')
    s.append(f'<text x="{cx - 240}" y="{cy + 168}" font-size="11" fill="#5a3a8a">'
             'optional conductive (e.g. copper-tape) trough lining,</text>')
    s.append(f'<text x="{cx - 240}" y="{cy + 184}" font-size="11" fill="#5a3a8a">'
             'mitigating triboelectric charging on fine inorganic powders.</text>')
    s.append(_svg_close())
    return "".join(s)


# ---------------------------------------------------------------------------
# Panel C — Isometric
# ---------------------------------------------------------------------------

def panel_C() -> str:
    W, H = 1000, 640
    s = [_svg_open(W, H)]
    s.append(
        f'<text x="{W//2}" y="34" text-anchor="middle" font-size="22" font-weight="700">'
        "Subpanel C — 3D / isometric view of the assembly on a gantry"
        "</text>"
    )
    s.append(
        f'<text x="{W//2}" y="56" text-anchor="middle" font-size="13" fill="#555" font-style="italic">'
        "two arms grip the two end caps; longitudinal pin (red) along L; cam track on a fixed post for sideways tilt"
        "</text>"
    )
    s.append('<rect x="180" y="80" width="640" height="22" fill="url(#metalH)" stroke="#222" stroke-width="1.5"/>')
    s.append('<text x="500" y="76" text-anchor="middle" font-size="12" fill="#444">gantry carriage (X / Z stage)</text>')
    s.append('<polygon points="270,102 290,102 290,300 270,300" fill="url(#metal)" stroke="#333"/>')
    s.append('<polygon points="640,102 660,102 670,290 650,290" fill="url(#metal)" stroke="#333"/>')
    s.append(
        '<polygon points="290,300 660,290 660,260 290,270" '
        'fill="#dfe4ea" stroke="#222" stroke-width="2"/>'
    )
    s.append(
        '<path d="M 290,270 '
        'C 360,420 590,410 660,260 '
        'L 660,290 '
        'C 590,440 360,450 290,300 Z" '
        'fill="url(#metalH)" stroke="#222" stroke-width="2"/>'
    )
    s.append(
        '<polygon points="296,295 654,287 654,265 296,275" '
        'fill="url(#powder)" opacity="0.95"/>'
    )
    s.append('<line x1="266" y1="285" x2="676" y2="275" stroke="#c0392b" stroke-width="4"/>')
    s.append('<circle cx="266" cy="285" r="6" fill="#c0392b" stroke="#7a1f15" stroke-width="1.5"/>')
    s.append('<circle cx="676" cy="275" r="6" fill="#c0392b" stroke="#7a1f15" stroke-width="1.5"/>')
    s.append('<text x="200" y="298" font-size="12" fill="#c0392b">pivot pin (along L)</text>')
    s.append('<polygon points="320,272 340,266 340,258 320,264" fill="#7e8794" stroke="#222" stroke-width="1.2"/>')
    s.append('<polygon points="610,266 630,260 630,252 610,258" fill="#7e8794" stroke="#222" stroke-width="1.2"/>')
    s.append('<text x="475" y="248" text-anchor="middle" font-size="11" fill="#444">'
             'chamfered bumpers (rim of long side) — slide up the cam track</text>')
    s.append('<rect x="850" y="180" width="18" height="320" fill="#8a7a5e" stroke="#444"/>')
    s.append('<text x="858" y="510" text-anchor="middle" font-size="11" fill="#5a4a30">fixed post</text>')
    s.append('<polygon points="730,300 850,300 850,250 730,300" fill="#8a7a5e" stroke="#444" stroke-width="1.5"/>')
    s.append('<text x="780" y="320" text-anchor="middle" font-size="12" fill="#5a4a30">smooth inclined cam track</text>')
    s.append('<text x="780" y="336" text-anchor="middle" font-size="11" fill="#7a6a4a">'
             '(replaces sawtooth; bumper slides up its hypotenuse)</text>')
    s.append('<rect x="220" y="510" width="350" height="10" fill="#5a4a30" stroke="#222"/>')
    s.append('<text x="395" y="535" text-anchor="middle" font-size="11" fill="#5a4a30">'
             'fixed strike-off bar (bed-edge mounted; trough wipes under during the lift-out)</text>')
    s.append('<rect x="180" y="555" width="430" height="55" fill="url(#powder)" stroke="#7a5a1a"/>')
    s.append('<text x="395" y="595" text-anchor="middle" font-size="12" fill="#7a5a1a">powder bed</text>')
    s.append(_svg_close())
    return "".join(s)


# ---------------------------------------------------------------------------
# Panel D — Mechanism (4 steps now: J-plunge, strike-off, transport, tilt)
# ---------------------------------------------------------------------------

def _draw_step_frame(
    title: str,
    *,
    show_bed: bool,
    arm_xy,
    arm_h,
    pivot_xy,
    trough_rotate: float,
    trough_radius: float,
    show_cam: bool,
    powder_pour: bool,
    show_strike_off: bool,
    extra: str = "",
) -> str:
    parts = []
    parts.append(f'<text x="200" y="0" text-anchor="middle" font-size="17" font-weight="600">{title}</text>')
    if show_bed:
        parts.append('<rect x="0" y="380" width="400" height="60" fill="url(#powder)" stroke="#7a5a1a"/>')
        parts.append('<text x="200" y="430" text-anchor="middle" font-size="11" fill="#7a5a1a">powder bed</text>')
    if show_strike_off:
        parts.append('<rect x="240" y="332" width="120" height="6" fill="#5a4a30" stroke="#222"/>')
        parts.append('<text x="300" y="328" text-anchor="middle" font-size="10" fill="#5a4a30">strike-off bar</text>')
    if show_cam:
        parts.append('<rect x="370" y="160" width="14" height="260" fill="#8a7a5e" stroke="#444"/>')
        parts.append('<polygon points="270,300 370,300 370,230 270,300" fill="#8a7a5e" stroke="#444"/>')
        parts.append('<text x="320" y="320" text-anchor="middle" font-size="10" fill="#5a4a30">smooth cam ramp</text>')
    ax, ay = arm_xy
    parts.append(f'<rect x="{ax - 8}" y="{ay}" width="16" height="{arm_h}" fill="url(#metal)" stroke="#333"/>')
    px, py = pivot_xy
    parts.append(f'<circle cx="{px}" cy="{py}" r="7" fill="#c0392b" stroke="#7a1f15" stroke-width="1.5"/>')
    parts.append(trough_cross_section(px, py, trough_radius, rotate_deg=trough_rotate))
    if powder_pour:
        parts.append(
            '<g fill="url(#powder)" opacity="0.95">'
            '<path d="M 305,255 Q 310,310 320,375 L 360,375 Q 370,310 345,255 Z"/>'
            '</g>'
        )
        parts.append('<text x="335" y="395" text-anchor="middle" font-size="11" fill="#7a5a1a">'
                     'powder pours over the FULL long edge</text>')
    parts.append(extra)
    return "\n".join(parts)


def panel_D() -> str:
    W, H = 1760, 600
    s = [_svg_open(W, H)]
    s.append(
        f'<text x="{W//2}" y="34" text-anchor="middle" font-size="22" font-weight="700">'
        "Subpanel D — Mechanism of action (side view, 4 steps)"
        "</text>"
    )
    s.append(
        f'<text x="{W//2}" y="56" text-anchor="middle" font-size="13" fill="#555" font-style="italic">'
        "arms always vertical; trough rolls SIDEWAYS about its longitudinal pin; smooth cam ramp (no sawtooth)"
        "</text>"
    )
    R = 38
    # Step 1 — J-curve plunge
    s.append('<g transform="translate(20,80)">')
    s.append(_draw_step_frame(
        "1. J-curve plunge",
        show_bed=True,
        arm_xy=(200, 30),
        arm_h=240,
        pivot_xy=(200, 290),
        trough_rotate=0,
        trough_radius=R,
        show_cam=False,
        powder_pour=False,
        show_strike_off=False,
        extra=(
            '<path d="M 60 60 L 60 200 Q 60 260 130 280" fill="none" stroke="#1f5fbf" '
            'stroke-width="3" marker-end="url(#arrowB)"/>'
            '<text x="48" y="120" font-size="11" fill="#1f5fbf" transform="rotate(-90 48 120)" text-anchor="middle">Z ↓</text>'
            '<text x="100" y="294" font-size="11" fill="#1f5fbf">then X →</text>'
            '<text x="36" y="22" font-size="10" fill="#1f5fbf">J-curve avoids flat-blunt compaction</text>'
        ),
    ))
    s.append('</g>')
    s.append('<line x1="430" y1="280" x2="465" y2="280" stroke="#222" stroke-width="2.5" marker-end="url(#arrowK)"/>')
    # Step 2 — strike-off
    s.append('<g transform="translate(480,80)">')
    s.append(_draw_step_frame(
        "2. Lift past strike-off bar",
        show_bed=True,
        arm_xy=(160, 30),
        arm_h=200,
        pivot_xy=(160, 250),
        trough_rotate=0,
        trough_radius=R,
        show_cam=False,
        powder_pour=False,
        show_strike_off=True,
        extra=(
            '<line x1="40" y1="280" x2="40" y2="120" stroke="#1f5fbf" stroke-width="3" marker-end="url(#arrowB)"/>'
            '<text x="26" y="200" font-size="11" fill="#1f5fbf" transform="rotate(-90 26 200)" text-anchor="middle">Z ↑</text>'
            '<text x="290" y="290" font-size="10" fill="#5a4a30">trough wipes under bar →</text>'
            '<text x="290" y="304" font-size="10" fill="#5a4a30">defines fill volume</text>'
        ),
    ))
    s.append('</g>')
    s.append('<line x1="890" y1="280" x2="925" y2="280" stroke="#222" stroke-width="2.5" marker-end="url(#arrowK)"/>')
    # Step 3 — transport
    s.append('<g transform="translate(940,80)">')
    s.append(_draw_step_frame(
        "3. Transport (X →)",
        show_bed=False,
        arm_xy=(120, 30),
        arm_h=200,
        pivot_xy=(120, 250),
        trough_rotate=0,
        trough_radius=R,
        show_cam=False,
        powder_pour=False,
        show_strike_off=False,
        extra=(
            '<line x1="220" y1="180" x2="320" y2="180" stroke="#1f5fbf" stroke-width="3" marker-end="url(#arrowB)"/>'
            '<text x="270" y="170" font-size="12" fill="#1f5fbf" text-anchor="middle">X →</text>'
            '<text x="200" y="320" font-size="10" fill="#444" text-anchor="middle">'
            'trough hangs level under gravity</text>'
        ),
    ))
    s.append('</g>')
    s.append('<line x1="1300" y1="280" x2="1335" y2="280" stroke="#222" stroke-width="2.5" marker-end="url(#arrowK)"/>')
    # Step 4 — sideways tilt against cam
    s.append('<g transform="translate(1340,80)">')
    s.append(_draw_step_frame(
        "4. Sideways tilt → deposit",
        show_bed=False,
        arm_xy=(120, 30),
        arm_h=200,
        pivot_xy=(120, 250),
        trough_rotate=55,
        trough_radius=R,
        show_cam=True,
        powder_pour=True,
        show_strike_off=False,
        extra=(
            '<line x1="20" y1="100" x2="80" y2="100" stroke="#1f5fbf" stroke-width="3" marker-end="url(#arrowB)"/>'
            '<text x="50" y="92" text-anchor="middle" font-size="11" fill="#1f5fbf">gantry pushes X →</text>'
            '<path d="M 90 220 a 36 36 0 0 1 38 -42" fill="none" stroke="#1f5fbf" stroke-width="2.5" '
            'marker-end="url(#arrowB)"/>'
            '<text x="50" y="248" font-size="10" fill="#1f5fbf">trough rolls sideways</text>'
            '<text x="50" y="262" font-size="10" fill="#1f5fbf">about its long axis</text>'
            '<text x="160" y="190" font-size="10" fill="#c0392b">bumper rides up cam</text>'
        ),
    ))
    s.append('</g>')
    s.append(
        f'<text x="{W//2}" y="{H - 50}" text-anchor="middle" font-size="13" fill="#444" font-style="italic">'
        "Pure-X gantry travel works because the smooth cam ramp gives a continuously varying engagement point"
        "</text>"
    )
    s.append(
        f'<text x="{W//2}" y="{H - 30}" text-anchor="middle" font-size="13" fill="#444" font-style="italic">'
        "(unlike a fixed sawtooth tooth, which is kinematically incompatible with a horizontally-translating pivot — Edison v2 §1)."
        "</text>"
    )
    s.append(_svg_close())
    return "".join(s)


# ---------------------------------------------------------------------------
# Animation: cam-engagement + sideways tilt
# ---------------------------------------------------------------------------

def _frame_svg(t: float) -> str:
    W, H = 700, 460
    R = 50
    pivot_y = 240
    if t < 0.35:
        pivot_x = 100 + (t / 0.35) * 130
        roll = 0.0
    elif t < 0.75:
        pivot_x = 230 + ((t - 0.35) / 0.4) * 30
        roll = ((t - 0.35) / 0.4) * 60.0
    else:
        pivot_x = 260
        roll = 60.0

    s = [_svg_open(W, H, font_size=12)]
    s.append('<rect x="40" y="20" width="620" height="14" fill="url(#metalH)" stroke="#222"/>')
    s.append(f'<rect x="{pivot_x - 8}" y="34" width="16" height="{pivot_y - 34}" fill="url(#metal)" stroke="#333"/>')
    s.append('<rect x="40" y="400" width="380" height="40" fill="url(#powder)" stroke="#7a5a1a"/>')
    s.append('<rect x="370" y="386" width="60" height="6" fill="#5a4a30" stroke="#222"/>')
    s.append('<rect x="500" y="180" width="14" height="240" fill="#8a7a5e" stroke="#444"/>')
    s.append('<polygon points="380,300 500,300 500,220 380,300" fill="#8a7a5e" stroke="#444"/>')
    s.append(f'<circle cx="{pivot_x}" cy="{pivot_y}" r="7" fill="#c0392b" stroke="#7a1f15" stroke-width="1.5"/>')
    s.append(trough_cross_section(pivot_x, pivot_y, R, rotate_deg=roll, powder_fill_frac=0.85))
    if t > 0.75:
        a = (t - 0.75) / 0.25
        s.append(
            f'<g fill="url(#powder)" opacity="{0.6 + 0.35 * a:.2f}">'
            f'<path d="M {pivot_x + 30} {pivot_y + 18} '
            f'Q {pivot_x + 50} {pivot_y + 80} {pivot_x + 70} {pivot_y + 160} '
            f'L {pivot_x + 110} {pivot_y + 160} '
            f'Q {pivot_x + 130} {pivot_y + 80} {pivot_x + 95} {pivot_y + 18} Z"/>'
            f'</g>'
        )
    s.append(
        '<text x="350" y="50" text-anchor="middle" font-size="13" font-weight="600">'
        'Sideways tilt against a smooth cam (corrected geometry)</text>'
    )
    s.append(
        '<text x="350" y="68" text-anchor="middle" font-size="11" fill="#555" font-style="italic">'
        'pivot axis runs ALONG the trough length L; trough rolls sideways and pours over the full long edge</text>'
    )
    s.append(_svg_close())
    return "".join(s)


def render_gif() -> None:
    try:
        import cairosvg  # type: ignore
        from PIL import Image  # type: ignore
    except ImportError as e:  # pragma: no cover
        raise SystemExit(
            "cairosvg and Pillow are required to render the animation: "
            f"pip install cairosvg Pillow ({e})"
        )

    n_frames = 24
    images = []
    for i in range(n_frames):
        t = i / (n_frames - 1)
        png_bytes = cairosvg.svg2png(bytestring=_frame_svg(t).encode("utf-8"))
        images.append(Image.open(io.BytesIO(png_bytes)).convert("P", palette=Image.ADAPTIVE))
    out = FIG_DIR / "mechanism.gif"
    images[0].save(
        out,
        save_all=True,
        append_images=images[1:] + list(reversed(images[1:-1])),
        duration=110,
        loop=0,
        optimize=True,
        disposal=2,
    )
    print(f"wrote {out}")


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    panels = {
        "panel-A-orthographic.svg": panel_A,
        "panel-B-pivot-detail.svg": panel_B,
        "panel-C-isometric.svg": panel_C,
        "panel-D-mechanism.svg": panel_D,
    }
    for name, fn in panels.items():
        path = FIG_DIR / name
        path.write_text(fn())
        print(f"wrote {path}")
    render_gif()


if __name__ == "__main__":
    main()
