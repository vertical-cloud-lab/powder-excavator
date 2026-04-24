# `cad/alternatives/`

Per-concept preliminary CAD for the eight alternative-dosing concepts
(A–H) brainstormed in
[`docs/alternative-dosing/brainstorm.md`](../../docs/alternative-dosing/brainstorm.md).

| Concept | SCAD | Iso | Cutaway | Spin GIF |
| --- | --- | --- | --- | --- |
| A — Tap-driven sieve cup | [`A_tap_sieve.scad`](A_tap_sieve.scad) | `A-tap-sieve-iso.png` | `A-tap-sieve-cutaway.png` | `A-tap-sieve-spin.gif` |
| B — Pez-style chamber strip | [`B_pez_strip.scad`](B_pez_strip.scad) | `B-pez-strip-iso.png` | `B-pez-strip-cutaway.png` | `B-pez-strip-spin.gif` |
| C — Capillary dip + wiper | [`C_capillary_wiper.scad`](C_capillary_wiper.scad) | `C-capillary-wiper-iso.png` | `C-capillary-wiper-cutaway.png` | `C-capillary-wiper-spin.gif` |
| D — Brush + comb | [`D_brush_comb.scad`](D_brush_comb.scad) | `D-brush-comb-iso.png` | `D-brush-comb-cutaway.png` | `D-brush-comb-spin.gif` |
| E — Salt-shaker oscillation | [`E_shaker.scad`](E_shaker.scad) | `E-shaker-iso.png` | `E-shaker-cutaway.png` | `E-shaker-spin.gif` |
| F — Passive auger (rack/pinion) | [`F_passive_auger.scad`](F_passive_auger.scad) | `F-passive-auger-iso.png` | `F-passive-auger-cutaway.png` | `F-passive-auger-spin.gif` |
| G — ERM-augmented sieve | [`G_erm_sieve.scad`](G_erm_sieve.scad) | `G-erm-sieve-iso.png` | `G-erm-sieve-cutaway.png` | `G-erm-sieve-spin.gif` |
| H — Solenoid + sieve | [`H_solenoid_sieve.scad`](H_solenoid_sieve.scad) | `H-solenoid-sieve-iso.png` | `H-solenoid-sieve-cutaway.png` | `H-solenoid-sieve-spin.gif` |

Composites (all eight at a glance):

- [`composite-spin.gif`](composite-spin.gif) — 4×2 tile of transparent rotating previews
- [`composite-cutaway.png`](composite-cutaway.png) — 4×2 tile of half-cutaway cross sections

Pipeline: see [`scripts/render_alternatives.py`](../../scripts/render_alternatives.py)
and the design notes in
[`docs/alternative-dosing/per-concept-designs.md`](../../docs/alternative-dosing/per-concept-designs.md).

```bash
sudo apt-get install -y openscad admesh prusa-slicer xvfb
pip install pillow
python scripts/render_alternatives.py
```

Render report (manifold + slice status for each part):
[`render-report.txt`](render-report.txt).
