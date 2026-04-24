// ================================================================
// Powder Excavator — Archimedes Auger: ASSEMBLED VIEW (v3)
// ================================================================
//
// As of v3 the auger is split into TWO parts (per design call in PR
// review). Each part is its own SCAD file and is sliced independently:
//
//   auger-shaft.scad     — FIXED inner shaft + helical fin.
//                          Anchored to the stationary frame via the M3
//                          stud at the top.
//   auger-housing.scad   — ROTATING outer tube + bottom funnel + top
//                          drive cap + external drive flange. Driven by
//                          the frankenmitsu spindle.
//
// This file is the ASSEMBLED VIEW. It loads both parts at their nominal
// fit (0.5 mm radial clearance per side between helix OD and tube ID,
// and between shaft core OD and the top-cap journal bore) and renders
// them together for visual inspection. It is NOT exported for printing
// — the slicing pipeline operates on the two part files directly.
//
// Render:  Paste into https://openscad.org/demo/ → F6 (Render)
// Headless STL + STEP + slices + checks (CI/local):
//   bash cad/auger/render_print.sh
//
// Background — why two parts (architecture history):
//   v1/v2/v2.1 modelled the auger as a single CSG-`union()`'d solid:
//   the entire cylinder rotated as one rigid piece, driven by an M3
//   spindle through the top cap. After PR review pointed out that this
//   conflicted with how an Archimedes screw is normally built ("real
//   auger design, shaft fixed, outer tube rotated"), v3 splits the part
//   along the helix-OD↔tube-ID interface so the two surfaces can rotate
//   relative to each other.
//
// ================================================================

use <auger-shaft.scad>
use <auger-housing.scad>

// Render both parts at their nominal in-place position. The shaft
// projects above the tube top (the M3 stud is the fixed-frame anchor
// point) and the tube's bottom funnel sits below the shaft tip with the
// `tip_clearance` gap baked into the shaft geometry.
module archimedes_auger() {
    auger_housing();
    auger_shaft();
}

archimedes_auger();

// ================================================================
// Cross-section view — uncomment to inspect interior fit:
// ================================================================
// difference() {
//     archimedes_auger();
//     translate([-11, -0.5, -1]) cube([22, 12, 115]);
// }
