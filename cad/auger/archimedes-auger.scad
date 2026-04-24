// ================================================================
// Powder Excavator — Archimedes Auger Attachment  v2
// ================================================================
//
// One-piece rotating helical dispenser.
// Mounts to frankenmitsu spindle via M3 boss at top.
// Spindle rotation drives powder down the helical channel.
// Conical funnel bottom collects powder at exit hole.
//
// Mechanism: rotating helical chute (gravity-assisted).
// Rotation agitates and advances powder downward; conical base
// funnels it to the exit hole when rotation slows.
// Closed-loop gravimetric feedback (load cell) handles precision.
//
// v2 changes vs v1:
//   - M3 boss added below top cap (12mm total engagement vs 4mm)
//   - Conical funnel bottom replaces flat cap (fixes centrifugal issue)
//   - Exit hole 3.0mm CAD diameter (prints to ~2.5mm on 0.4mm nozzle)
//   - Top cap increased to 6mm
//   - fin_inner_r increased to 2.0mm for cleaner central flow path
//
// v2.1 changes vs v2 (manifold/printability):
//   - Helical fin outer edge overlaps tube wall by 0.4mm and top/bottom
//     overlap funnel/boss by 0.2mm. v2 had zero-thickness coincident
//     surfaces that broke CGAL union (99 disconnected volumes in STL).
//     v2.1 exports as a single manifold solid (admesh: 0 issues, 1 part).
//
// Print:   PLA or PETG, 0.2mm layer height, 0.4mm nozzle
//          Print VERTICALLY (flat bottom — exit hole — on build plate)
//          3+ perimeters on outer walls, 40% gyroid infill
//          ENABLE supports + 4mm brim:
//             - Brim required: bottom contact is a thin annular ring
//               around the 1.5mm exit hole (low bed adhesion).
//             - Supports required: helix inner edge starts at r=2mm
//               above the funnel cavity (floating bridge anchor); top
//               cap also bridges the boss-to-wall annulus at z=94.
//          After printing: tap M3 boss hole with M3 hand tap.
//          Ultimaker note: standard Ultimaker filament is 2.85mm
//          (not 2.4mm); this file slices fine for 2.85mm with the
//          PrusaSlicer settings documented in the PR.
//
// Render:  Paste into https://openscad.org/demo/ → F6 (Render)
// Export:  File → Export → Export as STL
// Headless STL + STEP + checks (CI/local):
//   bash cad/auger/render_print.sh
// One-shot STL only:
//   xvfb-run -a openscad -o archimedes-auger.stl \
//       --export-format=binstl archimedes-auger.scad
//   admesh -fundecvb /tmp/clean.stl archimedes-auger.stl
// One-shot STEP from STL (FreeCAD OCCT bindings):
//   freecadcmd cad/auger/stl_to_step.py \
//       cad/auger/archimedes-auger.stl cad/auger/archimedes-auger.stp
// Headless slice for Ultimaker (PrusaSlicer 2.7+):
//   prusa-slicer --export-gcode -o auger.gcode \
//       --filament-diameter 2.85 --nozzle-diameter 0.4 \
//       --filament-type PLA --layer-height 0.2 \
//       --perimeters 3 --fill-density 40% --fill-pattern gyroid \
//       --brim-width 4 --support-material --support-material-auto \
//       --support-material-threshold 50 archimedes-auger.stl
//
// ================================================================

/* [Main Dimensions] */
outer_diameter  = 20;    // mm — outer cylinder OD
total_height    = 100;   // mm — total length
wall_thickness  = 2;     // mm — outer tube wall

/* [M3 Mount — Top] */
// Boss protrudes below the top cap to give 12mm of M3 engagement.
// After printing, use an M3 hand tap to cut threads.
// M3 minor diameter = 2.459mm; pilot at 2.5mm is correct for tapping.
m3_pilot_d      = 2.5;   // mm — M3 pilot hole (tap after print)
top_cap_height  = 6;     // mm — solid cap at top
m3_boss_r       = 4;     // mm — radius of central boss below cap
m3_boss_h       = 6;     // mm — boss height below cap (adds to cap for total depth)
// Total M3 engagement = top_cap_height + m3_boss_h = 12mm

/* [Powder Exit — Bottom] */
// Conical funnel guides powder from outer wall to exit hole.
// 3.0mm CAD diameter accounts for FDM shrinkage;
// as-printed on 0.4mm nozzle ≈ 2.5mm functional diameter.
// If too small after printing, open with a 2.5mm drill bit.
exit_hole_d     = 3.0;   // mm — exit hole diameter (CAD)
bottom_cap_h    = 6;     // mm — height of conical funnel section

/* [Helical Fin] */
pitch           = 10;    // mm per full 360° rotation
// Helix angle at mid-radius ≈ 18° → printable without support (FDM ok)
// Each layer rotates by (layer_h / pitch) × 360° = 7.2° at 0.2mm layers
// Inner edge overhang per layer ≈ 0.19mm — well within FDM bridge capability

fin_thickness   = 2;     // mm — blade thickness (≥1.6mm for Prusa 0.4mm nozzle)
fin_inner_r     = 2.0;   // mm — inner edge radius (clear of exit hole and M3)

/* [Loading Slots — Top Cap] */
slot_count      = 4;     // slots for loading powder from top before mounting
slot_width      = 4;     // mm — wider than v1 (3mm → 4mm) for easier loading
slot_length     = 6;     // mm
slot_radius     = 5;     // mm from center

// ================================================================
// Derived — do not edit
// ================================================================
inner_d         = outer_diameter - 2 * wall_thickness;  // 16mm
inner_r         = inner_d / 2;                           // 8mm
outer_r         = outer_diameter / 2;                    // 10mm
m3_pilot_depth  = top_cap_height + m3_boss_h;            // 12mm total
helix_z_start   = bottom_cap_h;
helix_z_end     = total_height - top_cap_height - m3_boss_h;
helix_height    = helix_z_end - helix_z_start;
turns           = helix_height / pitch;
slices_per_turn = 80;
total_slices    = ceil(turns * slices_per_turn);

$fn = 64;

// ================================================================
// Modules
// ================================================================

// Outer tube walls — hollow cylinder, full height
module tube_walls() {
    difference() {
        cylinder(r=outer_r, h=total_height);
        translate([0, 0, -0.1])
            cylinder(r=inner_r, h=total_height + 0.2);
    }
}

// Conical funnel bottom — directs powder to exit hole as rotation slows.
// Inner surface tapers from inner_r at the top to exit_hole_d/2 at the base.
// Outer surface is flat cylinder (matches tube OD).
module bottom_funnel() {
    difference() {
        cylinder(r=outer_r, h=bottom_cap_h);
        // Conical void: wide at top (inner_r - 0.5), narrow at bottom (exit hole)
        translate([0, 0, -0.1])
            cylinder(
                r1 = exit_hole_d / 2,       // narrow at z=0 (exit)
                r2 = inner_r - 0.5,          // wide at top of funnel (7.5mm)
                h  = bottom_cap_h + 0.2
            );
    }
}

// Top cap with M3 boss, pilot hole, and powder loading slots.
// Boss protrudes below the cap to extend M3 engagement depth.
module top_cap() {
    difference() {
        union() {
            // Solid disc cap
            translate([0, 0, total_height - top_cap_height])
                cylinder(r=outer_r, h=top_cap_height);
            // Central boss below cap for M3 depth
            translate([0, 0, total_height - top_cap_height - m3_boss_h])
                cylinder(r=m3_boss_r, h=m3_boss_h);
        }

        // M3 pilot hole — full depth through cap + boss
        translate([0, 0, total_height - m3_pilot_depth - 0.1])
            cylinder(d=m3_pilot_d, h=m3_pilot_depth + 0.2);

        // Powder loading slots (4x, 90° apart)
        for (i = [0 : slot_count - 1]) {
            angle = i * (360 / slot_count);
            translate([0, 0, total_height - top_cap_height - 0.1])
            rotate([0, 0, angle])
            translate([slot_radius, 0, 0])
                cube([slot_length, slot_width, top_cap_height + 0.2], center=true);
        }
    }
}

// Helical fin — Archimedes element.
// Single-start helix from fin_inner_r to inner_r.
// Outer edge overlaps tube inner wall by `fin_wall_overlap` (avoids
// zero-thickness coincident surfaces that break CGAL union → manifold STL).
// Vertical extent overlaps funnel/boss by `fin_z_overlap` for the same reason.
// Inner edge (fin_inner_r=2mm) clear of M3 boss (boss_r=4mm in overlap zone).
fin_wall_overlap = 0.4;   // mm — fin outer edge sinks into outer wall
fin_z_overlap    = 0.2;   // mm — fin top/bottom sink into boss/funnel

module helical_fin() {
    fin_outer = inner_r + fin_wall_overlap;        // 8.4mm
    fin_width = fin_outer - fin_inner_r;           // 6.4mm
    z_start   = helix_z_start - fin_z_overlap;
    z_height  = helix_height + 2 * fin_z_overlap;
    translate([0, 0, z_start])
    linear_extrude(
        height    = z_height,
        twist     = turns * 360,
        slices    = total_slices,
        convexity = 10
    ) {
        translate([(fin_inner_r + fin_outer) / 2, 0])
            square([fin_width, fin_thickness], center=true);
    }
}

// ================================================================
// Assembly
// ================================================================

module archimedes_auger() {
    color("#5B9BD5", 0.9)
    union() {
        tube_walls();
        bottom_funnel();
        top_cap();
        helical_fin();
    }
}

// ================================================================
// Full render
// ================================================================
archimedes_auger();

// ================================================================
// Cross-section view — uncomment to inspect interior geometry:
// ================================================================
// difference() {
//     archimedes_auger();
//     translate([-outer_r - 1, -0.5, -1])
//         cube([outer_diameter + 2, outer_r + 1, total_height + 2]);
// }
