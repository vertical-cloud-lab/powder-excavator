# Printing & prototyping the bimodal compliant trough

This folder contains the parametric, printable CAD for the bimodal
(bistable) trough mechanism analysed in
[`scripts/bimodal_compliance.py`](../scripts/bimodal_compliance.py).
It's everything you need to take the design from "interesting plot in a
PR" to "physical part on a 3018-PROVer V2 gantry tonight".

## Files

| File | What it is |
| ---- | ---------- |
| [`bimodal_trough.scad`](bimodal_trough.scad) | Parametric source, OpenSCAD 2021.01+. All dimensions are exposed as variables that mirror `FlexureParams` in the analyser, so a redesign upstream can be re-emitted by editing one variable here. |
| [`bimodal-trough.stl`](bimodal-trough.stl) | Ready-to-slice mesh. 76 × 26 × 20 mm, 1 264 triangles, manifold (CGAL `Simple: yes`). Fits every consumer FDM bed including the 3018-PROVer V2's 200 × 200 mm. |
| [`bimodal-trough-iso.png`](bimodal-trough-iso.png) | Isometric preview render. |

## Re-rendering from source

```bash
sudo apt-get install -y openscad           # or use the GUI app
openscad -o cad/bimodal-trough.stl cad/bimodal_trough.scad
openscad -o cad/bimodal-trough-iso.png \
         --imgsize=1100,800 \
         --camera=0,0,8,55,0,25,180 \
         --colorscheme=Tomorrow \
         cad/bimodal_trough.scad
```

## Recommended print settings (PETG, Bambu A1 / Prusa MK4 / Ender 3 V2)

The mechanism is *monolithic* — the compliant pivots are the flexures
themselves, so there are no fasteners, no support material, and no
post-print assembly. The two parameters that matter are **flexure
thickness in layers** and **flexure-grain orientation**.

| Setting | Value | Why |
| ------- | ----- | --- |
| Material | **PETG** | Matches the analyser's `youngs_modulus = 2.0 GPa`. PLA is too brittle at the snap-through strain (~3 %); ABS warps; TPU is too compliant. PCTG / co-PETG also fine. |
| Print orientation | **base flat on bed (default STL orientation)** | Layer lines then run *along* the flexure length, which is the strongest direction for axial load and the snap-through cycle. Printing the part on its side would put the failure plane perpendicular to the load — flexures would delaminate after a few snaps. |
| Layer height | **0.15 mm** (≤ 0.2 mm) | The flexure is 0.6 mm thick, so 0.15 mm gives **4 layers across the bending direction** — enough for clean bending without delamination. 0.20 mm = 3 layers also works; do not exceed. |
| Wall count | **3 perimeters** | At 0.4 mm nozzle, 3 walls = 1.2 mm of contour shell, which fully fills the 0.6 mm flexure (it'll print as solid contour, no infill in the beam). |
| Top/bottom layers | **5** | Keeps the trough floor and base plate stiff. |
| Infill | **30 % gyroid** | Only the trough body and base plate need infill; gyroid for slight extra trough rigidity. |
| Nozzle | **0.4 mm** (or 0.3 mm if you have it) | A 0.6 mm nozzle will struggle with the thin flexures. |
| Print speed | **≤ 40 mm/s on the flexures** | Lower speeds give better axial fibre alignment in the beam. The slicer's "small features" detection usually does this automatically; if not, override the outer-wall speed. |
| Brim | **5 mm** | The base plate footprint is small (76 × 26 mm); a brim resists the slight pull from the flexure-arch overhangs during cooling. |
| Bed temp | 75–80 °C (PETG) | Standard. |
| Nozzle temp | 235–245 °C (PETG) | Standard. |
| Cooling | **30 % fan** (PETG) | Enough to crisp the flexure underside without compromising layer adhesion. |
| Estimated print time | **~45 min** | Tested in PrusaSlicer with the above settings. |
| Estimated material   | **~6 g PETG**   | < $0.20 per copy — print 3-4 to test parameter variations. |

## Mounting & test procedure

1. **Bolt the base** to the gantry / breadboard with four M3×8 mm cap
   screws on the 30 × 14 mm hole pattern.
2. **Verify it's bistable** in the as-printed state by pressing the
   trough down with a fingernail past the dead-centre line; it should
   snap audibly to the dump pose and stay there. Pry up to snap back.
   If it doesn't snap (the printed pre-curve was too shallow), bump
   `flex_arch_kick` from 0.6 mm to 0.9 mm in the `.scad` and reprint.
3. **Measure the actuation force** by hanging weights from the trough
   centre line until it snaps. The analyser predicts **~2.4 N peak
   snap-through force** (≈ 245 g hanging mass) with the default
   geometry. If your measurement is wildly off, the most likely
   culprits are (a) under-extruded flexure thickness — measure with
   calipers, expect 0.55–0.65 mm — or (b) PETG modulus drift; the
   2 GPa value used in the analyser assumes ~22 °C and dry filament.
4. **Cycle test**: 100 manual snaps, look for whitening or surface
   crazing on the flexure underside. Whitening indicates the flexure
   is yielding — increase `flexure_thick` to 0.8 mm and reprint.
5. **Powder test**: scoop ~5 g of test powder (sugar, glass beads, or
   the actual sim regolith) into the trough in the scoop pose, drive
   the gantry to push the apex down, watch the snap eject the powder.

## Tweaking the geometry without breaking bistability

The single source of truth for "is this design still bimodal?" is
`scripts/bimodal_compliance.py`. The recommended workflow when you want
to change `half_span`, `initial_rise`, `flexure_thick`, etc.:

```bash
# 1. edit the variable in BOTH places (they need to match)
$EDITOR cad/bimodal_trough.scad         # geometry the printer will see
$EDITOR scripts/bimodal_compliance.py   # FlexureParams the analyser uses

# 2. confirm the analyser still reports `bimodal: True`
python scripts/bimodal_compliance.py

# 3. re-render the STL
openscad -o cad/bimodal-trough.stl cad/bimodal_trough.scad

# 4. (optional) cross-check with CalculiX FEA
python -m scripts.calculix_crosscheck
```

Variable names are deliberately the same in both files
(`half_span`, `initial_rise`, `flexure_thick`, `flexure_width`,
`pre_compression` ↔ `flex_arch_kick`) so a future PR could close the
loop and have one file emit both.
