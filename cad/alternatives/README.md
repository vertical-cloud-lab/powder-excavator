# `cad/alternatives/`

Per-concept preliminary CAD for the eight alternative-dosing concepts
(A–H) brainstormed in
[`docs/alternative-dosing/brainstorm.md`](../../docs/alternative-dosing/brainstorm.md).

| Concept | SCAD | Iso | Cutaway | Spin GIF | **Annotated panel** |
| --- | --- | --- | --- | --- | --- |
| A — Tap-driven sieve cup | [`A_tap_sieve.scad`](A_tap_sieve.scad) | `A-tap-sieve-iso.png` | `A-tap-sieve-cutaway.png` | `A-tap-sieve-spin.gif` | [`A-tap-sieve-panel.png`](A-tap-sieve-panel.png) |
| B — Pez-style chamber strip | [`B_pez_strip.scad`](B_pez_strip.scad) | `B-pez-strip-iso.png` | `B-pez-strip-cutaway.png` | `B-pez-strip-spin.gif` | [`B-pez-strip-panel.png`](B-pez-strip-panel.png) |
| C — Capillary dip + wiper | [`C_capillary_wiper.scad`](C_capillary_wiper.scad) | `C-capillary-wiper-iso.png` | `C-capillary-wiper-cutaway.png` | `C-capillary-wiper-spin.gif` | [`C-capillary-wiper-panel.png`](C-capillary-wiper-panel.png) |
| D — Brush + comb | [`D_brush_comb.scad`](D_brush_comb.scad) | `D-brush-comb-iso.png` | `D-brush-comb-cutaway.png` | `D-brush-comb-spin.gif` | [`D-brush-comb-panel.png`](D-brush-comb-panel.png) |
| E — Salt-shaker oscillation | [`E_shaker.scad`](E_shaker.scad) | `E-shaker-iso.png` | `E-shaker-cutaway.png` | `E-shaker-spin.gif` | [`E-shaker-panel.png`](E-shaker-panel.png) |
| F — Passive auger (rack/pinion) | [`F_passive_auger.scad`](F_passive_auger.scad) | `F-passive-auger-iso.png` | `F-passive-auger-cutaway.png` | `F-passive-auger-spin.gif` | [`F-passive-auger-panel.png`](F-passive-auger-panel.png) |
| G — ERM-augmented sieve | [`G_erm_sieve.scad`](G_erm_sieve.scad) | `G-erm-sieve-iso.png` | `G-erm-sieve-cutaway.png` | `G-erm-sieve-spin.gif` | [`G-erm-sieve-panel.png`](G-erm-sieve-panel.png) |
| H — Solenoid + sieve | [`H_solenoid_sieve.scad`](H_solenoid_sieve.scad) | `H-solenoid-sieve-iso.png` | `H-solenoid-sieve-cutaway.png` | `H-solenoid-sieve-spin.gif` | [`H-solenoid-sieve-panel.png`](H-solenoid-sieve-panel.png) |

Composites (all eight at a glance):

- [`composite-panel.png`](composite-panel.png) — **4×2 tile of annotated explainer panels** (title + iso + cutaway + numbered key parts + 3-step operation cycle, per concept). Best starting point for a reader.
- [`composite-spin.gif`](composite-spin.gif) — 4×2 tile of transparent rotating previews
- [`composite-cutaway.png`](composite-cutaway.png) — 4×2 tile of half-cutaway cross sections

Pipeline: see [`scripts/render_alternatives.py`](../../scripts/render_alternatives.py)
(SCAD → STL → admesh → iso/cutaway PNG → spin GIF → PrusaSlicer slice) and
the per-concept annotator
[`scripts/annotate_alternatives.py`](../../scripts/annotate_alternatives.py)
(pure Pillow; turns the renders into labelled explainer panels).
Design notes per concept:
[`docs/alternative-dosing/per-concept-designs.md`](../../docs/alternative-dosing/per-concept-designs.md).

```bash
sudo apt-get install -y openscad admesh prusa-slicer xvfb
pip install pillow
python scripts/render_alternatives.py     # SCAD → STL → renders → slice
python scripts/annotate_alternatives.py   # renders → labelled panels
```

Render report (manifold + slice status for each part):
[`render-report.txt`](render-report.txt).
