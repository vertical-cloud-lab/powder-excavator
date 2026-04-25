#!/usr/bin/env python3
"""
animate_dispensing.py — generate per-concept 2D schematic GIFs that show
each of the eight alternative powder-dosing mechanisms (A–H) actually
loading and dispensing powder.

The static OpenSCAD renders + half-cutaway sections + annotated panels
(see ``scripts/annotate_alternatives.py``) describe geometry but not
*motion*. This script fills that gap with an intentionally schematic
2-D side-view animation per concept (480×360 px, transparent background,
~3 s loop at 12 fps) plus a 4×2 composite ``composite-animation.gif``.

Pure Pillow — no OpenSCAD / Blender / browser required.

Run:

    python scripts/animate_dispensing.py
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Tuple

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parent.parent
OUT_DIR = REPO / "cad" / "alternatives"

W, H = 480, 360
FPS = 12
DURATION_S = 4.0
N_FRAMES = int(FPS * DURATION_S)

BG = (255, 255, 255, 0)        # transparent
TITLE_BG = (32, 56, 92, 255)
TITLE_FG = (255, 255, 255, 255)
PART = (90, 100, 120, 255)      # mechanism body
PART_FILL = (220, 225, 235, 255)
ACCENT = (0, 110, 200, 255)
POWDER = (160, 100, 40, 255)    # cohesive powder = brownish
VIAL = (130, 165, 210, 255)
ANVIL = (60, 70, 90, 255)
LABEL = (24, 24, 28, 255)
MUTED = (90, 95, 110, 255)


def _font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


F_TITLE = _font(16, bold=True)
F_PHASE = _font(13, bold=True)
F_LABEL = _font(11)


def _new_frame() -> Tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGBA", (W, H), BG)
    draw = ImageDraw.Draw(img)
    return img, draw


def _draw_title(draw: ImageDraw.ImageDraw, title: str, phase: str) -> None:
    draw.rectangle([(0, 0), (W, 30)], fill=TITLE_BG)
    draw.text((10, 7), title, fill=TITLE_FG, font=F_TITLE)
    draw.text((10, H - 22), f"phase: {phase}", fill=MUTED, font=F_PHASE)


def _draw_vial(
    draw: ImageDraw.ImageDraw,
    cx: int,
    top: int,
    fill_frac: float = 0.0,
) -> None:
    """Draw a simple side-view vial centred at cx with mouth at y=top."""
    w, h = 50, 70
    x0, x1 = cx - w // 2, cx + w // 2
    y0, y1 = top, top + h
    # body
    draw.rounded_rectangle([(x0, y0), (x1, y1)], radius=6, outline=PART,
                           width=2, fill=(245, 248, 252, 255))
    # collected powder
    if fill_frac > 0:
        fh = int((h - 6) * min(1.0, fill_frac))
        draw.rectangle([(x0 + 3, y1 - fh - 3), (x1 - 3, y1 - 3)],
                       fill=POWDER)
    # neck
    draw.line([(x0, y0), (x1, y0)], fill=PART, width=2)


def _powder_grains(
    draw: ImageDraw.ImageDraw,
    bbox: Tuple[int, int, int, int],
    n: int,
    seed: int = 0,
    radius: int = 2,
) -> None:
    """Scatter small POWDER dots inside bbox to suggest a powder pile/cloud."""
    rng = random.Random(seed)
    x0, y0, x1, y1 = bbox
    for _ in range(n):
        x = rng.uniform(x0, x1)
        y = rng.uniform(y0, y1)
        draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)],
                     fill=POWDER)


def _falling_grains(
    draw: ImageDraw.ImageDraw,
    cx_range: Tuple[int, int],
    y0: int,
    y1: int,
    n: int,
    t: float,
    seed: int = 0,
) -> None:
    """Animate n grains falling from y0 to y1 in column cx_range (looped t∈[0,1))."""
    rng = random.Random(seed)
    for i in range(n):
        cx = rng.uniform(*cx_range)
        phase = (t + i / max(n, 1)) % 1.0
        y = y0 + phase * (y1 - y0)
        draw.ellipse([(cx - 2, y - 2), (cx + 2, y + 2)], fill=POWDER)


# ---------------------------------------------------------------------------
# Phase helper
# ---------------------------------------------------------------------------

@dataclass
class Phase:
    name: str
    duration: float  # seconds


def _phase_at(phases: List[Phase], t_s: float) -> Tuple[str, float]:
    """Return (phase_name, progress_in_phase∈[0,1]) for absolute time t_s."""
    total = sum(p.duration for p in phases)
    t_s = t_s % total
    acc = 0.0
    for p in phases:
        if t_s < acc + p.duration:
            return p.name, (t_s - acc) / p.duration
        acc += p.duration
    return phases[-1].name, 1.0


# ---------------------------------------------------------------------------
# Per-concept frame renderers — each returns a PIL Image for absolute time t
# ---------------------------------------------------------------------------

def render_A(t: float) -> Image.Image:
    """Tap-driven sieve cup: gantry pecks cup down on a fixed anvil."""
    phases = [
        Phase("descend", 0.7),
        Phase("strike (powder kicks through mesh)", 1.0),
        Phase("retract", 0.7),
        Phase("repeat", 1.6),
    ]
    name, p = _phase_at(phases, t)
    img, draw = _new_frame()
    _draw_title(draw, "A — Tap-driven sieve cup", name)

    # gantry travel: y_cup_top: 50 (high) → 150 (struck)
    if name == "descend":
        y_top = 50 + int(100 * p)
    elif name == "strike (powder kicks through mesh)":
        # bounce: down at peak then up slightly
        bounce = math.sin(p * math.pi) * 6
        y_top = 150 - int(bounce)
    elif name == "retract":
        y_top = 150 - int(100 * p)
    else:
        y_top = 50

    cx = 140
    # cup
    cup_w, cup_h = 80, 90
    cup_x0 = cx - cup_w // 2
    cup_x1 = cx + cup_w // 2
    draw.rectangle([(cup_x0, y_top), (cup_x1, y_top + cup_h)],
                   outline=PART, width=2, fill=PART_FILL)
    # powder pile inside
    _powder_grains(draw, (cup_x0 + 6, y_top + 20, cup_x1 - 6, y_top + 70),
                   n=35, seed=1)
    # mesh line at cup bottom
    draw.line([(cup_x0 + 4, y_top + cup_h - 4),
               (cup_x1 - 4, y_top + cup_h - 4)],
              fill=ANVIL, width=2)
    for i in range(cup_x0 + 8, cup_x1 - 4, 5):
        draw.line([(i, y_top + cup_h - 6), (i, y_top + cup_h - 2)],
                  fill=PART, width=1)

    # strike pad (annular bottom rim of cup) → highlighted on impact
    pad_color = ACCENT if name == "strike (powder kicks through mesh)" else PART
    draw.rectangle([(cup_x0 - 3, y_top + cup_h - 4),
                    (cup_x0 + 4, y_top + cup_h + 2)],
                   fill=pad_color)
    draw.rectangle([(cup_x1 - 4, y_top + cup_h - 4),
                    (cup_x1 + 3, y_top + cup_h + 2)],
                   fill=pad_color)

    # bed anvil
    anvil_y = 250
    draw.rectangle([(60, anvil_y), (220, anvil_y + 8)], fill=ANVIL)
    draw.polygon([(125, anvil_y), (140, anvil_y - 12), (155, anvil_y)],
                 fill=ANVIL)  # central pillar
    draw.rectangle([(132, anvil_y - 12), (148, anvil_y)], fill=ANVIL)
    # impact arrows
    if name == "strike (powder kicks through mesh)":
        for dx in (-30, 30):
            draw.polygon([
                (cx + dx, y_top + cup_h + 6),
                (cx + dx - 4, y_top + cup_h + 12),
                (cx + dx + 4, y_top + cup_h + 12),
            ], fill=ACCENT)

    # falling grains during strike phase
    if name == "strike (powder kicks through mesh)":
        # central bore of anvil drops grains into vial
        _falling_grains(draw, (135, 145), y_top + cup_h, anvil_y - 4,
                        n=8, t=p, seed=42)
    # vial right of anvil
    fill_frac = {"descend": 0.05, "strike (powder kicks through mesh)": 0.18,
                 "retract": 0.18, "repeat": 0.22}[name]
    _draw_vial(draw, cx=350, top=anvil_y - 70, fill_frac=fill_frac)

    # arrows + labels
    draw.line([(cx, 35), (cx, y_top - 4)], fill=ACCENT, width=1)
    draw.polygon([(cx - 4, y_top - 4), (cx + 4, y_top - 4),
                  (cx, y_top + 2)], fill=ACCENT)
    draw.text((cx + 8, 35), "gantry", fill=MUTED, font=F_LABEL)
    draw.text((230, anvil_y - 5), "fixed bed-anvil", fill=MUTED, font=F_LABEL)
    draw.text((325, anvil_y - 85), "receiving vial", fill=MUTED, font=F_LABEL)
    return img


def render_B(t: float) -> Image.Image:
    """Pez-style chamber strip: chambers fill, indexed, then knocked through."""
    phases = [
        Phase("strike-off fill", 1.0),
        Phase("step strip", 0.8),
        Phase("pawl punches dose", 1.0),
        Phase("repeat", 1.2),
    ]
    name, p = _phase_at(phases, t)
    img, draw = _new_frame()
    _draw_title(draw, "B — Pez-style chamber strip", name)

    # hopper above
    hopper_pts = [(100, 50), (160, 50), (140, 110), (120, 110)]
    draw.polygon(hopper_pts, outline=PART, width=2, fill=PART_FILL)
    _powder_grains(draw, (104, 54, 156, 100), n=25, seed=7)

    # strip with chambers — slides right over time
    n_ch, ch_w, ch_h = 6, 38, 36
    strip_y = 130
    base_x = 80
    if name == "strike-off fill":
        offset = 0
    elif name == "step strip":
        offset = int(38 * p)
    elif name == "pawl punches dose":
        offset = 38
    else:  # repeat
        offset = 38 + int(38 * p)
    strip_x0 = base_x + offset

    # strip body
    draw.rectangle([(strip_x0 - 10, strip_y),
                    (strip_x0 + n_ch * ch_w + 10, strip_y + ch_h)],
                   outline=PART, width=2, fill=PART_FILL)
    # chambers
    for i in range(n_ch):
        cx0 = strip_x0 + i * ch_w + 4
        cx1 = cx0 + ch_w - 8
        draw.rectangle([(cx0, strip_y + 4), (cx1, strip_y + ch_h - 4)],
                       outline=PART, width=1)
        # filled if chamber has been under hopper already
        chamber_world_x = cx0 + (cx1 - cx0) // 2
        # filled if currently passed the hopper (hopper centered ~130)
        if chamber_world_x < 145 - 6:
            _powder_grains(draw, (cx0 + 2, strip_y + 6, cx1 - 2,
                                  strip_y + ch_h - 6),
                           n=8, seed=i)

    # strike-off knife (fixed) just right of hopper
    knife_x = 165
    draw.line([(knife_x, strip_y - 6), (knife_x, strip_y + 4)],
              fill=ANVIL, width=3)
    draw.text((knife_x + 4, strip_y - 14), "strike-off",
              fill=MUTED, font=F_LABEL)

    # bed-mounted advance pawl above strip at outlet position (right end)
    pawl_x = 360
    pawl_y_base = strip_y - 14
    if name == "pawl punches dose":
        pawl_dy = int(20 * math.sin(p * math.pi))
    else:
        pawl_dy = 0
    pawl_y = pawl_y_base + pawl_dy
    draw.polygon([(pawl_x - 8, pawl_y), (pawl_x + 8, pawl_y),
                  (pawl_x, pawl_y + 14)], fill=ACCENT)
    draw.line([(pawl_x, pawl_y - 14), (pawl_x, pawl_y)], fill=ACCENT, width=2)
    draw.text((pawl_x + 12, pawl_y - 4), "bed pawl", fill=MUTED, font=F_LABEL)

    # outlet hole in strip floor under pawl
    draw.line([(pawl_x - 12, strip_y + ch_h),
               (pawl_x + 12, strip_y + ch_h)], fill=BG, width=2)

    # falling grains during punch
    if name == "pawl punches dose":
        _falling_grains(draw, (pawl_x - 6, pawl_x + 6),
                        strip_y + ch_h, 290, n=6, t=p, seed=11)

    fill_frac = {"strike-off fill": 0.05, "step strip": 0.05,
                 "pawl punches dose": 0.18, "repeat": 0.18}[name]
    _draw_vial(draw, cx=pawl_x, top=290, fill_frac=fill_frac)

    return img


def render_C(t: float) -> Image.Image:
    """Capillary dip + fixed wiper."""
    phases = [
        Phase("dip into bed", 1.0),
        Phase("retract through wiper", 1.0),
        Phase("translate to vial", 0.7),
        Phase("plunge eject", 0.8),
        Phase("retract", 0.5),
    ]
    name, p = _phase_at(phases, t)
    img, draw = _new_frame()
    _draw_title(draw, "C — Capillary dip + fixed wiper", name)

    # bed: source pad on left, vial on right
    pad_x0, pad_x1, pad_y = 60, 160, 250
    draw.rectangle([(pad_x0, pad_y), (pad_x1, pad_y + 40)],
                   outline=PART, width=2, fill=(235, 225, 200, 255))
    _powder_grains(draw, (pad_x0 + 4, pad_y + 4, pad_x1 - 4, pad_y + 36),
                   n=40, seed=3)
    draw.text((pad_x0 + 8, pad_y + 44), "powder source bed",
              fill=MUTED, font=F_LABEL)

    # fixed wiper bar between source pad and vial
    wiper_x = 230
    draw.rectangle([(wiper_x - 4, 170), (wiper_x + 4, 240)], fill=ANVIL)
    draw.text((wiper_x + 8, 170), "wiper", fill=MUTED, font=F_LABEL)

    # vial position
    vial_cx = 350

    # capillary tip path: x and y depending on phase
    tip_w = 8
    if name == "dip into bed":
        tip_x = (pad_x0 + pad_x1) // 2
        tip_y_bottom = 200 + int(50 * p)  # plunge into bed
    elif name == "retract through wiper":
        tip_x = (pad_x0 + pad_x1) // 2 + int((wiper_x - (pad_x0 + pad_x1) // 2 + 20) * 0)
        tip_y_bottom = 250 - int(80 * p)
    elif name == "translate to vial":
        tip_x = int((pad_x0 + pad_x1) // 2 + (vial_cx - (pad_x0 + pad_x1) // 2) * p)
        tip_y_bottom = 170
    elif name == "plunge eject":
        tip_x = vial_cx
        tip_y_bottom = 170 + int(30 * p)
    else:  # retract
        tip_x = vial_cx
        tip_y_bottom = 200 - int(30 * p)

    # shank
    draw.rectangle([(tip_x - 4, 35), (tip_x + 4, tip_y_bottom - 30)],
                   fill=PART, outline=PART)
    # capillary tip (hollow rectangle)
    draw.rectangle([(tip_x - tip_w // 2, tip_y_bottom - 30),
                    (tip_x + tip_w // 2, tip_y_bottom)],
                   outline=PART, width=2, fill=(255, 255, 255, 255))
    # plug inside tip if loaded
    plug_loaded = name in ("retract through wiper", "translate to vial",
                            "plunge eject")
    if plug_loaded and not (name == "retract through wiper" and p < 0.3):
        # after passing wiper, plug volume is a clean chunk
        plug_top = tip_y_bottom - 24
        draw.rectangle([(tip_x - tip_w // 2 + 1, plug_top),
                        (tip_x + tip_w // 2 - 1, tip_y_bottom - 1)],
                       fill=POWDER)
    elif name == "dip into bed":
        # filling fraction = p
        fh = max(1, int(24 * p))
        draw.rectangle([(tip_x - tip_w // 2 + 1, tip_y_bottom - fh),
                        (tip_x + tip_w // 2 - 1, tip_y_bottom - 1)],
                       fill=POWDER)

    # plunger inside (animated descent during eject)
    if name == "plunge eject":
        plunger_y = tip_y_bottom - 24 + int(22 * p)
        draw.line([(tip_x, 50), (tip_x, plunger_y)], fill=ACCENT, width=2)
        # falling grains
        _falling_grains(draw, (tip_x - 3, tip_x + 3), tip_y_bottom, 270,
                        n=4, t=p, seed=21)

    fill_frac = {"dip into bed": 0.05, "retract through wiper": 0.05,
                 "translate to vial": 0.05, "plunge eject": 0.16,
                 "retract": 0.16}[name]
    _draw_vial(draw, cx=vial_cx, top=270, fill_frac=fill_frac)
    return img


def render_D(t: float) -> Image.Image:
    """Brush + fixed comb knock-off."""
    phases = [
        Phase("sweep across powder pad", 1.2),
        Phase("translate to comb", 0.8),
        Phase("comb scrapes brush", 1.2),
        Phase("retract", 0.8),
    ]
    name, p = _phase_at(phases, t)
    img, draw = _new_frame()
    _draw_title(draw, "D — Brush + fixed comb knock-off", name)

    # source pad
    pad_x0, pad_x1, pad_y = 60, 170, 270
    draw.rectangle([(pad_x0, pad_y), (pad_x1, pad_y + 30)],
                   outline=PART, width=2, fill=(235, 225, 200, 255))
    _powder_grains(draw, (pad_x0 + 4, pad_y + 4, pad_x1 - 4, pad_y + 26),
                   n=40, seed=5)
    draw.text((pad_x0 + 8, pad_y + 34), "source pad", fill=MUTED, font=F_LABEL)

    # comb at right
    comb_x_center = 350
    for i in range(-25, 26, 7):
        draw.line([(comb_x_center + i, 240), (comb_x_center + i, 270)],
                  fill=ANVIL, width=2)
    draw.line([(comb_x_center - 28, 238), (comb_x_center + 28, 238)],
              fill=ANVIL, width=2)
    draw.text((comb_x_center + 32, 246), "comb", fill=MUTED, font=F_LABEL)

    # disc carrier — moves along arc
    if name == "sweep across powder pad":
        # disc x sweeps over pad
        disc_x = pad_x0 + int((pad_x1 - pad_x0) * p)
        disc_y = pad_y - 10
    elif name == "translate to comb":
        disc_x = pad_x1 + int((comb_x_center - pad_x1) * p)
        disc_y = pad_y - 10 - int(40 * math.sin(p * math.pi))
    elif name == "comb scrapes brush":
        disc_x = comb_x_center
        disc_y = 230
    else:
        disc_x = comb_x_center
        disc_y = 230 - int(60 * p)

    # disc and bristles
    disc_r = 18
    draw.ellipse([(disc_x - disc_r, disc_y - disc_r),
                  (disc_x + disc_r, disc_y + disc_r)],
                 outline=PART, width=2, fill=PART_FILL)
    # bristles around bottom half
    for ang_deg in range(180, 361, 12):
        ang = math.radians(ang_deg)
        x1 = disc_x + (disc_r + 1) * math.cos(ang)
        y1 = disc_y + (disc_r + 1) * math.sin(ang)
        x2 = disc_x + (disc_r + 8) * math.cos(ang)
        y2 = disc_y + (disc_r + 8) * math.sin(ang)
        draw.line([(x1, y1), (x2, y2)], fill=PART, width=1)

    # bristle-laden powder dots: present after sweep until comb
    laden = name in ("sweep across powder pad", "translate to comb",
                     "comb scrapes brush")
    if laden:
        scrape_factor = 1.0
        if name == "sweep across powder pad":
            scrape_factor = p
        if name == "comb scrapes brush":
            scrape_factor = max(0.0, 1.0 - p)
        n_dots = int(20 * scrape_factor)
        rng = random.Random(99)
        for _ in range(n_dots):
            ang_deg = rng.randint(180, 360)
            ang = math.radians(ang_deg)
            r = disc_r + 3 + rng.uniform(0, 4)
            x = disc_x + r * math.cos(ang)
            y = disc_y + r * math.sin(ang)
            draw.ellipse([(x - 1, y - 1), (x + 1, y + 1)], fill=POWDER)

    if name == "comb scrapes brush":
        _falling_grains(draw, (comb_x_center - 12, comb_x_center + 12),
                        260, 295, n=6, t=p, seed=33)

    fill_frac = {"sweep across powder pad": 0.04, "translate to comb": 0.04,
                 "comb scrapes brush": 0.16, "retract": 0.16}[name]
    _draw_vial(draw, cx=comb_x_center, top=290, fill_frac=fill_frac)
    return img


def render_E(t: float) -> Image.Image:
    """Salt-shaker oscillation."""
    phases = [
        Phase("position over vial", 0.6),
        Phase("oscillate (powder leaks)", 2.4),
        Phase("stop on target mass", 1.0),
    ]
    name, p = _phase_at(phases, t)
    img, draw = _new_frame()
    _draw_title(draw, "E — Salt-shaker oscillation", name)

    cup_w, cup_h = 100, 90
    cy = 130
    if name == "position over vial":
        cx = 180 + int(50 * p)
    elif name == "oscillate (powder leaks)":
        cx = 230 + int(8 * math.sin(p * math.pi * 8))
    else:
        cx = 230

    cup_x0, cup_x1 = cx - cup_w // 2, cx + cup_w // 2
    cup_y0, cup_y1 = cy, cy + cup_h
    draw.rectangle([(cup_x0, cup_y0), (cup_x1, cup_y1)],
                   outline=PART, width=2, fill=PART_FILL)
    # powder pile inside diminishes
    pile_frac = {"position over vial": 1.0,
                 "oscillate (powder leaks)": max(0.3, 1.0 - p * 0.6),
                 "stop on target mass": 0.4}[name]
    pile_top = cup_y0 + 20 + int((cup_h - 30) * (1 - pile_frac))
    _powder_grains(draw, (cup_x0 + 6, pile_top, cup_x1 - 6, cup_y1 - 8),
                   n=int(45 * pile_frac), seed=2)

    # multi-hole floor: draw holes as gaps
    floor_y = cup_y1
    for i in range(cup_x0 + 12, cup_x1 - 8, 10):
        draw.ellipse([(i, floor_y - 2), (i + 5, floor_y + 2)], fill=BG)

    # falling grains during oscillation
    if name == "oscillate (powder leaks)":
        _falling_grains(draw, (cup_x0 + 14, cup_x1 - 10),
                        floor_y, 270, n=12, t=p * 4, seed=44)

    # arrows showing X-Y oscillation
    if name == "oscillate (powder leaks)":
        for sx, dx in ((cup_x0 - 18, -10), (cup_x1 + 18, 10)):
            draw.line([(sx, cy + cup_h // 2), (sx + dx, cy + cup_h // 2)],
                      fill=ACCENT, width=2)
            draw.polygon([
                (sx + dx, cy + cup_h // 2 - 4),
                (sx + dx, cy + cup_h // 2 + 4),
                (sx + dx + (3 if dx > 0 else -3), cy + cup_h // 2),
            ], fill=ACCENT)

    fill_frac = {"position over vial": 0.05,
                 "oscillate (powder leaks)": 0.05 + 0.5 * p,
                 "stop on target mass": 0.55}[name]
    _draw_vial(draw, cx=230, top=270, fill_frac=fill_frac)
    return img


def render_F(t: float) -> Image.Image:
    """Passive auger via rack-and-pinion."""
    phases = [
        Phase("rapid horizontally", 0.9),
        Phase("pinion meshes with rack", 1.2),
        Phase("auger rotates → quantized dose", 1.4),
        Phase("retract", 0.5),
    ]
    name, p = _phase_at(phases, t)
    img, draw = _new_frame()
    _draw_title(draw, "F — Passive auger (rack & pinion)", name)

    # bed rack on right side
    rack_y = 130
    rack_x0, rack_x1 = 250, 420
    draw.rectangle([(rack_x0, rack_y), (rack_x1, rack_y + 14)],
                   outline=ANVIL, width=2, fill=PART_FILL)
    for i in range(rack_x0 + 4, rack_x1 - 2, 8):
        draw.polygon([(i, rack_y), (i + 4, rack_y - 6), (i + 8, rack_y)],
                     fill=ANVIL)
    draw.text((rack_x0 + 4, rack_y + 18), "fixed bed-rack",
              fill=MUTED, font=F_LABEL)

    # auger module x position
    if name == "rapid horizontally":
        ax = 100 + int(160 * p)
    else:
        ax = 260
    # pinion rotation angle
    if name == "auger rotates → quantized dose":
        rot_deg = p * 540
    else:
        rot_deg = 0

    # outer tube + auger
    tube_w, tube_h = 36, 130
    tube_x0, tube_x1 = ax - tube_w // 2, ax + tube_w // 2
    tube_y0, tube_y1 = 65, 65 + tube_h
    draw.rectangle([(tube_x0, tube_y0), (tube_x1, tube_y1)],
                   outline=PART, width=2, fill=PART_FILL)
    # helix flighting (drawn as zig-zag line, animated by rot)
    n_turns = 5
    rot_off = rot_deg / 360.0
    for i in range(n_turns * 6):
        f = (i / (n_turns * 6) + rot_off * 0.05) % 1.0
        y = tube_y0 + 10 + f * (tube_h - 20)
        # phase across the tube width using sine
        phase_w = math.sin((i + rot_off * 6) * math.pi / 3)
        x = ax + int(tube_w * 0.35 * phase_w)
        draw.ellipse([(x - 2, y - 1), (x + 2, y + 1)], fill=ACCENT)

    # pinion at top
    pin_cx, pin_cy = ax + tube_w // 2 + 10, 75
    pin_r = 12
    draw.ellipse([(pin_cx - pin_r, pin_cy - pin_r),
                  (pin_cx + pin_r, pin_cy + pin_r)],
                 outline=PART, width=2, fill=PART_FILL)
    # teeth
    for ang_deg in range(0, 360, 30):
        ang = math.radians(ang_deg + rot_deg)
        x1 = pin_cx + pin_r * math.cos(ang)
        y1 = pin_cy + pin_r * math.sin(ang)
        x2 = pin_cx + (pin_r + 4) * math.cos(ang)
        y2 = pin_cy + (pin_r + 4) * math.sin(ang)
        draw.line([(x1, y1), (x2, y2)], fill=PART, width=2)

    # hopper feeding the tube
    draw.polygon([(tube_x0 - 14, tube_y0 - 28), (tube_x1 + 14, tube_y0 - 28),
                  (tube_x1, tube_y0), (tube_x0, tube_y0)],
                 outline=PART, width=2, fill=PART_FILL)
    _powder_grains(draw, (tube_x0 - 8, tube_y0 - 22, tube_x1 + 8, tube_y0 - 4),
                   n=20, seed=8)

    # falling grains when auger rotates
    if name == "auger rotates → quantized dose":
        _falling_grains(draw, (ax - 4, ax + 4), tube_y1, 280,
                        n=5, t=p * 2, seed=55)

    fill_frac = {"rapid horizontally": 0.04,
                 "pinion meshes with rack": 0.04,
                 "auger rotates → quantized dose": 0.04 + 0.4 * p,
                 "retract": 0.45}[name]
    _draw_vial(draw, cx=ax, top=280, fill_frac=fill_frac)
    return img


def render_G(t: float) -> Image.Image:
    """ERM-augmented sieve (continuous bounded vibration)."""
    phases = [
        Phase("lower cup over vial", 0.6),
        Phase("ERM ON — continuous flow", 2.6),
        Phase("ERM OFF on target mass", 0.8),
    ]
    name, p = _phase_at(phases, t)
    img, draw = _new_frame()
    _draw_title(draw, "G — ERM-augmented sieve (top pick)", name)

    # cup with ERM pocket on its side
    cup_w, cup_h = 100, 90
    cx = 230
    if name == "lower cup over vial":
        cy = 60 + int(70 * p)
    else:
        cy = 130
    # vibration jitter when ERM is on
    if name == "ERM ON — continuous flow":
        jx = int(2 * math.sin(p * math.pi * 30))
        jy = int(2 * math.cos(p * math.pi * 30))
    else:
        jx = jy = 0

    cup_x0, cup_x1 = cx - cup_w // 2 + jx, cx + cup_w // 2 + jx
    cup_y0, cup_y1 = cy + jy, cy + cup_h + jy
    draw.rectangle([(cup_x0, cup_y0), (cup_x1, cup_y1)],
                   outline=PART, width=2, fill=PART_FILL)
    # powder
    pile_frac = {"lower cup over vial": 1.0,
                 "ERM ON — continuous flow": max(0.3, 1.0 - p * 0.6),
                 "ERM OFF on target mass": 0.4}[name]
    _powder_grains(draw, (cup_x0 + 6, cup_y0 + 18, cup_x1 - 6, cup_y1 - 8),
                   n=int(45 * pile_frac), seed=4)
    # mesh ticks
    for i in range(cup_x0 + 8, cup_x1 - 4, 5):
        draw.line([(i, cup_y1 - 4), (i, cup_y1)], fill=PART, width=1)
    draw.line([(cup_x0 + 4, cup_y1), (cup_x1 - 4, cup_y1)],
              fill=ANVIL, width=2)

    # ERM motor pocket on side
    erm_x = cup_x1 + 4
    erm_y = cy + 30 + jy
    erm_color = ACCENT if name == "ERM ON — continuous flow" else PART
    draw.ellipse([(erm_x, erm_y), (erm_x + 18, erm_y + 18)],
                 outline=erm_color, width=2, fill=PART_FILL)
    draw.text((erm_x + 22, erm_y + 4), "ERM", fill=MUTED, font=F_LABEL)
    # vibration squiggles
    if name == "ERM ON — continuous flow":
        for k in range(3):
            ang = p * 6 + k
            r = 10 + k * 4
            draw.arc([(erm_x + 9 - r, erm_y + 9 - r),
                       (erm_x + 9 + r, erm_y + 9 + r)],
                     start=ang * 30, end=ang * 30 + 60,
                     fill=ACCENT, width=1)

    # falling stream during ERM ON (continuous)
    if name == "ERM ON — continuous flow":
        _falling_grains(draw, (cup_x0 + 16, cup_x1 - 14),
                        cup_y1 + 2, 270, n=20, t=p * 6, seed=66)

    fill_frac = {"lower cup over vial": 0.05,
                 "ERM ON — continuous flow": 0.05 + 0.55 * p,
                 "ERM OFF on target mass": 0.6}[name]
    _draw_vial(draw, cx=cx, top=270, fill_frac=fill_frac)
    return img


def render_H(t: float) -> Image.Image:
    """Solenoid-tapped sieve, closed-loop with a balance."""
    phases = [
        Phase("lower over balance + vial", 0.6),
        Phase("solenoid pulses (closed loop)", 2.4),
        Phase("hit target → stop", 0.8),
    ]
    name, p = _phase_at(phases, t)
    img, draw = _new_frame()
    _draw_title(draw, "H — Solenoid-tapped sieve (closed loop)", name)

    cup_w, cup_h = 90, 80
    cx = 200
    if name == "lower over balance + vial":
        cy = 60 + int(70 * p)
    else:
        cy = 130

    # solenoid kick: cup nudges right when fired
    if name == "solenoid pulses (closed loop)":
        # ~6 pulses across phase
        pulse = math.sin(p * math.pi * 12)
        kick = max(0, pulse) * 3
    else:
        kick = 0
    cx_eff = cx + int(kick)

    cup_x0, cup_x1 = cx_eff - cup_w // 2, cx_eff + cup_w // 2
    cup_y0, cup_y1 = cy, cy + cup_h
    draw.rectangle([(cup_x0, cup_y0), (cup_x1, cup_y1)],
                   outline=PART, width=2, fill=PART_FILL)
    pile_frac = {"lower over balance + vial": 1.0,
                 "solenoid pulses (closed loop)": max(0.4, 1.0 - p * 0.5),
                 "hit target → stop": 0.5}[name]
    _powder_grains(draw, (cup_x0 + 6, cup_y0 + 16, cup_x1 - 6, cup_y1 - 6),
                   n=int(40 * pile_frac), seed=6)
    # mesh
    draw.line([(cup_x0 + 4, cup_y1), (cup_x1 - 4, cup_y1)],
              fill=ANVIL, width=2)
    for i in range(cup_x0 + 8, cup_x1 - 4, 5):
        draw.line([(i, cup_y1 - 4), (i, cup_y1)], fill=PART, width=1)

    # solenoid bracket on left of cup
    sol_x = cup_x0 - 30
    sol_y = cy + cup_h // 2 - 6
    draw.rectangle([(sol_x, sol_y), (sol_x + 26, sol_y + 12)],
                   outline=PART, width=2, fill=PART_FILL)
    draw.text((sol_x - 4, sol_y + 14), "solenoid", fill=MUTED, font=F_LABEL)
    # plunger
    if name == "solenoid pulses (closed loop)":
        plunger_extend = max(0, math.sin(p * math.pi * 12)) * 6
    else:
        plunger_extend = 0
    px0 = sol_x + 26
    px1 = px0 + 4 + int(plunger_extend)
    draw.rectangle([(px0, sol_y + 4), (px1, sol_y + 8)], fill=ACCENT)

    # falling grains synced to pulses
    if name == "solenoid pulses (closed loop)":
        if math.sin(p * math.pi * 12) > 0.5:
            _falling_grains(draw, (cup_x0 + 12, cup_x1 - 10),
                            cup_y1 + 2, 250, n=8, t=p * 6, seed=77)

    # balance + vial (centred, balance shown as bar with mass readout)
    bal_y = 270
    draw.rectangle([(150, bal_y), (300, bal_y + 14)], outline=PART, width=2,
                   fill=PART_FILL)
    fill_frac = {"lower over balance + vial": 0.05,
                 "solenoid pulses (closed loop)": 0.05 + 0.45 * p,
                 "hit target → stop": 0.5}[name]
    _draw_vial(draw, cx=cx, top=bal_y - 70, fill_frac=fill_frac)
    # mass readout
    target_mg = 5.0
    mass_mg = fill_frac * target_mg / 0.5
    color = ACCENT if name == "hit target → stop" else LABEL
    draw.text((310, bal_y - 4), f"balance: {mass_mg:0.2f} mg",
              fill=color, font=F_LABEL)
    draw.text((310, bal_y + 10), f"target: {target_mg:0.1f} mg",
              fill=MUTED, font=F_LABEL)
    return img


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

CONCEPTS: List[Tuple[str, str, Callable[[float], Image.Image]]] = [
    ("A", "tap-sieve", render_A),
    ("B", "pez-strip", render_B),
    ("C", "capillary-wiper", render_C),
    ("D", "brush-comb", render_D),
    ("E", "shaker", render_E),
    ("F", "passive-auger", render_F),
    ("G", "erm-sieve", render_G),
    ("H", "solenoid-sieve", render_H),
]


def _save_animation(frames: List[Image.Image], path: Path) -> None:
    # Quantize to palette and preserve transparency for GIF
    palettised = []
    for fr in frames:
        # paste over white-with-transparency mask preserving alpha
        p = fr.convert("RGBA")
        # convert to P with adaptive palette, transparency at index 0
        bg = Image.new("RGBA", p.size, (255, 255, 255, 255))
        bg.alpha_composite(p)
        palettised.append(bg.convert("P", palette=Image.ADAPTIVE,
                                     colors=255))
    palettised[0].save(
        path,
        save_all=True,
        append_images=palettised[1:],
        duration=int(1000 / FPS),
        loop=0,
        optimize=True,
        disposal=2,
    )


def _make_composite(per_concept: List[Path], out_path: Path) -> None:
    cols, rows = 4, 2
    sub_w, sub_h = W // 2, H // 2
    cw, ch = sub_w * cols, sub_h * rows
    # Open all 8 GIFs
    gifs = [Image.open(p) for p in per_concept]
    # Frame count is the same (N_FRAMES)
    composite_frames: List[Image.Image] = []
    for fi in range(N_FRAMES):
        canvas = Image.new("RGBA", (cw, ch), (255, 255, 255, 255))
        for idx, g in enumerate(gifs):
            try:
                g.seek(fi)
            except EOFError:
                g.seek(g.n_frames - 1)
            sub = g.convert("RGBA").resize((sub_w, sub_h), Image.LANCZOS)
            r, c = divmod(idx, cols)
            canvas.paste(sub, (c * sub_w, r * sub_h), sub)
        composite_frames.append(canvas)
    _save_animation(composite_frames, out_path)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_paths: List[Path] = []
    for letter, slug, fn in CONCEPTS:
        frames = []
        for fi in range(N_FRAMES):
            t_s = fi / FPS
            frames.append(fn(t_s))
        out = OUT_DIR / f"{letter}-{slug}-animation.gif"
        _save_animation(frames, out)
        out_paths.append(out)
        print(f"  wrote {out.relative_to(REPO)}")

    composite = OUT_DIR / "composite-animation.gif"
    _make_composite(out_paths, composite)
    print(f"  wrote {composite.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
