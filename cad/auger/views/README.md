# Why the slicer "looks empty"

The auger is a **closed cylinder externally** — all the interesting geometry
(helical fin, conical funnel, M3 boss, top-cap loading slots, exit hole) is
**inside** the part. So when the STL/STEP is loaded into Cura (Ultimaker)
or PrusaSlicer (MK3S+ / Ender-3), the bed view shows what looks like a
plain 20 × 100 mm pillar. That's correct — the helix is there, you just
can't see it from the outside.

To verify the helix is in the file (and that the slicer sees it):

| View | What it shows |
|---|---|
| `archimedes-auger-xray.png` | Outer tube rendered semi-transparent so the helix, funnel, and boss read through the wall |
| `archimedes-auger-layer-z12.png` | Top-down cross-section at z=12 mm — outer wall annulus + the conical funnel surface descending toward the exit hole |
| `archimedes-auger-layer-z50.png` | Top-down cross-section at z=50 mm — outer wall annulus + the helical fin pie-slice; this is exactly what the slicer extrudes for that layer |
| `archimedes-auger-layer-z85.png` | Top-down cross-section at z=85 mm — outer wall annulus + the M3 boss column |

The slice PNGs are rendered with `intersection() { archimedes_auger();
translate([-15,-15,Z]) cube([30,30,0.6]); }` — i.e. they are literal layer
slabs of the SCAD source. If the slicer's layer preview at the same Z
matches these shapes, the slicer is doing the right thing.

In Cura / PrusaSlicer's GUI: switch to **Preview** mode and scrub the
layer slider — you'll see the same wall-+-helix-pie shape spiral up the
part. The helix is there.
