"""
Pure Python preview renderer for the Archimedes auger.
No dependencies — uses only stdlib math to generate an SVG.
Run: python3 cad/auger/render_preview.py
Output: cad/auger/preview.svg
"""
import math

# ── Design parameters (must match archimedes-auger.scad) ─────────
OUTER_R      = 10.0   # mm
INNER_R      = 8.0    # mm
HEIGHT       = 100.0  # mm
PITCH        = 10.0   # mm
TURNS        = 9.2
FIN_INNER_R  = 1.5    # mm
FIN_THICK    = 2.0    # mm
BOTTOM_CAP   = 4.0    # mm
TOP_CAP      = 4.0    # mm
EXIT_D       = 2.5    # mm
M3_D         = 2.5    # mm
HELIX_START  = BOTTOM_CAP
HELIX_END    = HEIGHT - TOP_CAP

# ── SVG layout ────────────────────────────────────────────────────
SCALE        = 5.0    # px per mm
PAD          = 60     # px padding

# Cross-section panel (left)
CS_X0        = PAD
CS_W         = int(2 * OUTER_R * SCALE)
CS_H         = int(HEIGHT * SCALE)
CS_CX        = CS_X0 + CS_W // 2

# Front isometric panel (right) — flattened helix projection
ISO_X0       = CS_X0 + CS_W + PAD * 2
ISO_W        = 160
ISO_CX       = ISO_X0 + ISO_W // 2

TOTAL_W      = ISO_X0 + ISO_W + PAD
TOTAL_H      = CS_H + PAD * 3 + 40

def mm_to_px(mm):
    return mm * SCALE

def y(z_mm):
    """Convert Z coordinate (mm, 0=bottom) to SVG y (top of diagram = top of auger)."""
    return PAD + 40 + (HEIGHT - z_mm) * SCALE

lines = []

def svg_open():
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" '
                 f'width="{TOTAL_W}" height="{TOTAL_H}" style="background:white; font-family:Arial,sans-serif;">')

def svg_close():
    lines.append('</svg>')

def rect(x, y_pos, w, h, fill, stroke='#333', sw=1.5, opacity=1.0, rx=0):
    lines.append(f'<rect x="{x:.1f}" y="{y_pos:.1f}" width="{w:.1f}" height="{h:.1f}" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
                 f'opacity="{opacity}" rx="{rx}"/>')

def line(x1, y1, x2, y2, color='#333', sw=1.5, dash=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    lines.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                 f'stroke="{color}" stroke-width="{sw}"{d}/>')

def text(x, y_pos, content, size=11, anchor='middle', color='#222', bold=False, italic=False):
    style = f'font-size:{size}px; text-anchor:{anchor}; fill:{color};'
    if bold:   style += ' font-weight:bold;'
    if italic: style += ' font-style:italic;'
    lines.append(f'<text x="{x:.1f}" y="{y_pos:.1f}" style="{style}">{content}</text>')

def arrow(x1, y1, x2, y2, color='#333', sw=1.2):
    line(x1, y1, x2, y2, color=color, sw=sw)
    # arrowhead at (x2, y2)
    dx, dy = x2-x1, y2-y1
    L = math.hypot(dx, dy)
    if L < 1: return
    ux, uy = dx/L, dy/L
    px, py = -uy, ux
    size = 5
    pts = f'{x2:.1f},{y2:.1f} {x2-ux*size+px*3:.1f},{y2-uy*size+py*3:.1f} {x2-ux*size-px*3:.1f},{y2-uy*size-py*3:.1f}'
    lines.append(f'<polygon points="{pts}" fill="{color}"/>')

def dim_arrow_v(x, y1, y2, label, side='right'):
    arrow(x, y1, x, y1+5, color='#888', sw=1)
    arrow(x, y2, x, y2-5, color='#888', sw=1)
    line(x, y1, x, y2, color='#888', sw=1, dash='4,3')
    lx = x + 8 if side == 'right' else x - 8
    anchor = 'start' if side == 'right' else 'end'
    text(lx, (y1+y2)/2 + 4, label, size=9, anchor=anchor, color='#666')

def dim_arrow_h(x1, x2, y_pos, label):
    arrow(x1, y_pos, x1+5, y_pos, color='#888', sw=1)
    arrow(x2, y_pos, x2-5, y_pos, color='#888', sw=1)
    line(x1, y_pos, x2, y_pos, color='#888', sw=1, dash='4,3')
    text((x1+x2)/2, y_pos - 4, label, size=9, color='#666')

# ── BUILD SVG ─────────────────────────────────────────────────────
svg_open()

# Title
text(TOTAL_W//2, 28, 'Archimedes Auger Attachment — Design Preview', size=15, bold=True)
text(TOTAL_W//2, 45, '20mm OD × 100mm height | M3 spindle mount | 2.5mm exit hole | PLA/PETG FDM',
     size=10, color='#555', italic=True)

# ══════════════════════════════════════════════════════
# PANEL 1: CROSS-SECTION
# ══════════════════════════════════════════════════════
text(CS_CX, y(HEIGHT) - 14, 'Cross-Section View', size=12, bold=True)

left_wall_x  = CS_X0
right_wall_x = CS_X0 + int((OUTER_R + INNER_R) * SCALE)
wall_w       = int((OUTER_R - INNER_R) * SCALE)
inner_left   = CS_X0 + wall_w
inner_right  = CS_X0 + int(2 * OUTER_R * SCALE) - wall_w

# Left tube wall
rect(left_wall_x, y(HEIGHT), wall_w, int(HEIGHT * SCALE),
     fill='#a8c8e8', stroke='#1a5276', sw=2)
# Right tube wall
rect(inner_right, y(HEIGHT), wall_w, int(HEIGHT * SCALE),
     fill='#a8c8e8', stroke='#1a5276', sw=2)

# Bottom cap
rect(left_wall_x, y(BOTTOM_CAP), int(2*OUTER_R*SCALE), int(BOTTOM_CAP*SCALE),
     fill='#2e86c1', stroke='#1a5276', sw=2)
# Exit hole (white gap in bottom cap)
ex = CS_CX - mm_to_px(EXIT_D/2)
ew = mm_to_px(EXIT_D)
rect(ex, y(0)+1, ew, int(BOTTOM_CAP*SCALE)-1, fill='white', stroke='none')

# Top cap
rect(left_wall_x, y(HEIGHT), int(2*OUTER_R*SCALE), int(TOP_CAP*SCALE),
     fill='#2e86c1', stroke='#1a5276', sw=2)
# M3 hole (white gap in top cap)
m3x = CS_CX - mm_to_px(M3_D/2)
m3w = mm_to_px(M3_D)
rect(m3x, y(HEIGHT)-1, m3w, int(10*SCALE)+1, fill='white', stroke='none')

# Loading slots (shown as lighter areas in top cap)
for sx_offset in [-5.5, 2.5]:
    sx = CS_CX + mm_to_px(sx_offset)
    rect(sx, y(HEIGHT)-1, mm_to_px(3), int(TOP_CAP*SCALE)+1, fill='white', stroke='none')

# Helical fin cross-sections (horizontal lines at each half-pitch)
n_fins = int((HELIX_END - HELIX_START) / (PITCH/2)) + 1
for i in range(n_fins):
    z_fin = HELIX_START + i * (PITCH/2)
    if z_fin > HELIX_END: break
    fy = y(z_fin)
    # Left fin segment
    line(inner_left, fy,
         inner_left + mm_to_px(INNER_R - FIN_INNER_R), fy,
         color='#c0392b', sw=2)
    # Right fin segment
    line(inner_right - mm_to_px(INNER_R - FIN_INNER_R), fy,
         inner_right, fy,
         color='#c0392b', sw=2)

# Dimension: total height
dim_arrow_v(CS_X0 + int(2*OUTER_R*SCALE) + 25, y(HEIGHT), y(0), '100mm', side='right')

# Dimension: OD
dim_arrow_h(CS_X0, CS_X0 + int(2*OUTER_R*SCALE), y(0) + 22, '20mm OD')

# Dimension: wall thickness
dim_arrow_h(CS_X0, inner_left, y(HEIGHT/3), '2mm wall')

# Dimension: pitch
p1 = HELIX_START + PITCH * 2
p2 = p1 + PITCH
dim_arrow_v(inner_left - 18, y(p1), y(p2), f'{int(PITCH)}mm pitch', side='left')

# Labels
text(CS_CX, y(0) + 35, f'Exit hole ⌀{EXIT_D}mm', size=9, color='#27ae60', bold=True)
text(CS_CX, y(HEIGHT) - 6,  f'M3 pilot ⌀{M3_D}mm + 4 loading slots', size=9, color='#7d3c98', bold=True)
text(inner_left - 5, y(HELIX_START + 8), f'Helical fin', size=9, color='#c0392b', anchor='end')
text(inner_left - 5, y(HELIX_START + 8) + 12, f'(1.5mm inner radius,', size=8, color='#888', anchor='end')
text(inner_left - 5, y(HELIX_START + 8) + 22, f'2mm thick)', size=8, color='#888', anchor='end')

# ══════════════════════════════════════════════════════
# PANEL 2: ISOMETRIC HELIX PROJECTION
# ══════════════════════════════════════════════════════
text(ISO_CX, y(HEIGHT) - 14, 'Helix Path (Front Projection)', size=12, bold=True)

# Draw the helical fin projected onto a 2D front view
# In front projection: x = r*cos(angle), z = z → projected x = x, projected y = z
n_pts = 400
pts_outer = []
pts_inner = []

for i in range(n_pts + 1):
    t = i / n_pts
    z_val = HELIX_START + t * (HELIX_END - HELIX_START)
    angle = t * TURNS * 2 * math.pi
    xo = (INNER_R - 0.5) * math.cos(angle)   # outer fin edge
    xi = FIN_INNER_R * math.cos(angle)         # inner fin edge
    svgx_o = ISO_CX + mm_to_px(xo)
    svgx_i = ISO_CX + mm_to_px(xi)
    svgy   = y(z_val)
    pts_outer.append((svgx_o, svgy))
    pts_inner.append((svgx_i, svgy))

# Draw the helix as a polyline
def polyline(pts, color, sw=1.5, opacity=1.0):
    pts_str = ' '.join(f'{px:.1f},{py:.1f}' for px, py in pts)
    lines.append(f'<polyline points="{pts_str}" fill="none" stroke="{color}" '
                 f'stroke-width="{sw}" opacity="{opacity}"/>')

# Outer tube outline
rect(ISO_CX - mm_to_px(OUTER_R), y(HEIGHT),
     mm_to_px(2*OUTER_R), mm_to_px(HEIGHT),
     fill='#ddeeff', stroke='#1a5276', sw=2, opacity=0.3)

# Tube walls (solid)
rect(ISO_CX - mm_to_px(OUTER_R), y(HEIGHT),
     mm_to_px(OUTER_R - INNER_R), mm_to_px(HEIGHT),
     fill='#a8c8e8', stroke='none', opacity=0.7)
rect(ISO_CX + mm_to_px(INNER_R), y(HEIGHT),
     mm_to_px(OUTER_R - INNER_R), mm_to_px(HEIGHT),
     fill='#a8c8e8', stroke='none', opacity=0.7)
# Outlines
line(ISO_CX - mm_to_px(OUTER_R), y(0), ISO_CX - mm_to_px(OUTER_R), y(HEIGHT), '#1a5276', 2)
line(ISO_CX + mm_to_px(OUTER_R), y(0), ISO_CX + mm_to_px(OUTER_R), y(HEIGHT), '#1a5276', 2)

# Top and bottom caps
rect(ISO_CX - mm_to_px(OUTER_R), y(BOTTOM_CAP), mm_to_px(2*OUTER_R), mm_to_px(BOTTOM_CAP),
     fill='#2e86c1', stroke='none', opacity=0.6)
rect(ISO_CX - mm_to_px(OUTER_R), y(HEIGHT), mm_to_px(2*OUTER_R), mm_to_px(TOP_CAP),
     fill='#2e86c1', stroke='none', opacity=0.6)

# Helical fin paths
polyline(pts_outer, '#c0392b', sw=2.0)
polyline(pts_inner, '#e74c3c', sw=1.2)

# Exit and M3 hole markers
circle_r = 4
lines.append(f'<circle cx="{ISO_CX:.1f}" cy="{y(0):.1f}" r="{circle_r}" '
             f'fill="#27ae60" stroke="white" stroke-width="1.5"/>')
lines.append(f'<circle cx="{ISO_CX:.1f}" cy="{y(HEIGHT):.1f}" r="{circle_r}" '
             f'fill="#7d3c98" stroke="white" stroke-width="1.5"/>')

text(ISO_CX + mm_to_px(OUTER_R) + 8, y(0),       '← Exit ⌀2.5mm', size=9, color='#27ae60', anchor='start')
text(ISO_CX + mm_to_px(OUTER_R) + 8, y(HEIGHT)+4, '← M3 mount',     size=9, color='#7d3c98', anchor='start')

# ══════════════════════════════════════════════════════
# SPEC TABLE at bottom
# ══════════════════════════════════════════════════════
ty = TOTAL_H - PAD + 5
specs = [
    ('Outer diameter', '20 mm'),
    ('Total height',   '100 mm'),
    ('Wall thickness', '2 mm'),
    ('Inner diameter', '16 mm'),
    ('Helix pitch',    '10 mm / turn'),
    ('Turns',          '9.2'),
    ('Exit hole',      '⌀2.5 mm'),
    ('M3 pilot',       '⌀2.5 mm × 10 mm deep'),
    ('Print',          'PLA/PETG, 0.2mm layers, vertical'),
]
col_w = (TOTAL_W - 2*PAD) / len(specs)
for i, (k, v) in enumerate(specs):
    sx = PAD + i * col_w + col_w/2
    text(sx, ty,      k, size=8, color='#555')
    text(sx, ty + 13, v, size=9, color='#111', bold=True)

line(PAD, ty - 8, TOTAL_W - PAD, ty - 8, color='#ccc', sw=1)

svg_close()

output_path = '/Users/devoranajjar/Github/powder-excavator/cad/auger/preview.svg'
with open(output_path, 'w') as f:
    f.write('\n'.join(lines))

print(f'Saved: {output_path}')
