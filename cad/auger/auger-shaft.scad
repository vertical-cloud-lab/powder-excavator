// ================================================================
// Powder Excavator — Archimedes Auger: FIXED inner shaft (v3)
// ================================================================
//
// Two-part architecture (per design call in PR review):
//   - This file: the FIXED inner shaft. Carries the helical fin.
//                Anchored to the stationary frame via the M3 stud at the top.
//   - Sibling:   `auger-housing.scad` — the ROTATING outer tube. Driven
//                by the frankenmitsu spindle via the external drive flange.
//   - Assembly:  `archimedes-auger.scad` — both parts at fit clearance.
//
// Rotation: the OUTER TUBE rotates around this fixed shaft. The helix is
// rigidly attached to the shaft and remains stationary in space while the
// tube wall sweeps past its outer edge. Powder loaded through the tube's
// top slots is dragged by the rotating wall against the stationary helix
// flank, which deflects it downward — the same kinematics as a classical
// Archimedes screw, just with the moving and fixed surfaces swapped from
// the more common "rotor inside a stationary tube" arrangement.
//
// Fits (parameter `radial_clearance` below — single source of truth):
//   - Helix OD vs tube ID: `radial_clearance` per side (default 0.5 mm —
//     loose slip fit for FDM at 0.4 mm nozzle; smaller risks self-welding
//     during print, larger leaks too much powder past the helix).
//   - Shaft core OD vs top-cap bore: `radial_clearance` per side. The top
//     cap acts as a journal bearing around the fixed shaft.
//
// Print orientation: M3 stud DOWN on the build plate. The shaft is
// rotationally symmetric with a flat top-stud face — that face is the
// only good first-layer candidate. The helix overhangs are equivalent to
// the original one-piece design (helix angle ~18°, printable on FDM).
// 4 mm brim + auto-supports at 50° threshold; supports are needed only
// under the helix's bottom flange where it transitions to bare shaft.
//
// ================================================================

/* [Main Dimensions — keep in sync with auger-housing.scad] */
outer_diameter   = 20;    // mm — outer tube OD (informational; sets fin OD)
total_height     = 30;    // mm — total tube height (informational)
                          // v3.1: shortened from 100 mm → 30 mm at PR-review
                          // request ("very very short, easy to print
                          // quickly, almost done with the workshop"). The
                          // helix region is now ~1 turn instead of ~8;
                          // every other dimension (OD, wall, pitch, fin
                          // thickness, fits) is unchanged so the kinematics
                          // and assembly fits are identical.
wall_thickness   = 2;     // mm — outer tube wall

/* [Clearance / fit] */
radial_clearance = 0.5;   // mm — uniform per-side gap (helix↔tube, shaft↔bore)

/* [Inner shaft — load-bearing core] */
shaft_core_d     = 4;     // mm — central rod OD (carries M3 stud + helix root)

/* [Top mount — fixed anchor stud] */
// Stud protrudes ABOVE the top of the tube's drive cap so the user can
// clamp it into a stationary frame (e.g. with an M3 nut + washer through
// the frame's mounting bracket). Pilot drilled for M3 hand tap after print.
m3_pilot_d       = 2.5;   // mm — M3 minor diameter pilot (tap after print)
stud_h           = 12;    // mm — length of stud sticking up out of housing
stud_d           = 6;     // mm — stud OD (room for M3 with 1.5 mm wall)
m3_pilot_depth   = 16;    // mm — pilot bore depth (full stud + into shaft top)

/* [Helical fin] */
pitch            = 10;    // mm per full 360° rotation (matches v2)
fin_thickness    = 2;     // mm — blade thickness (≥1.6 mm at 0.4 mm nozzle)
// Fin root sinks 0.4 mm INTO the shaft core to avoid the zero-thickness
// coincident-surface CGAL union failure (same root cause as v2.1's fin↔wall
// fix). Without this overlap, OpenSCAD reports "3 volumes / not 2-manifold".
fin_root_overlap = 0.4;   // mm — fin sinks into shaft body radially
fin_inner_r      = shaft_core_d / 2 - fin_root_overlap;   // 1.6 mm

/* [Exit-end shaft tip] */
// Shaft tip ends a few mm above the rotating tube's bottom funnel so that
// (a) the tip never contacts the funnel during rotation, and (b) powder
// has a clear path from the helix bottom into the funnel cone.
tip_clearance    = 5;     // mm — gap between shaft tip and tube bottom (z=0)
tip_taper_h      = 4;     // mm — gentle cone at the bottom end (no support)

// ================================================================
// Derived — do not edit
// ================================================================
inner_d          = outer_diameter - 2 * wall_thickness;     // 16 mm
inner_r          = inner_d / 2;                              // 8 mm
// Helix outer radius leaves `radial_clearance` against the rotating tube ID.
fin_outer_r      = inner_r - radial_clearance;               // 7.5 mm
// Helix vertical extent: from just above the tip taper to just below the
// shaft top (where the stud begins). Match the v2 envelope as closely as
// possible so the powder-handling region is unchanged.
helix_z_start    = tip_clearance + tip_taper_h + 2;          // ~11 mm
helix_z_end      = total_height - 8;                         // 92 mm
helix_height     = helix_z_end - helix_z_start;
turns            = helix_height / pitch;
slices_per_turn  = 80;
total_slices     = ceil(turns * slices_per_turn);

// Shaft body extends from the top of the tip taper to the base of the stud.
shaft_body_z0    = tip_clearance + tip_taper_h;              // 9 mm
shaft_body_h     = total_height - shaft_body_z0;             // 91 mm

$fn = 64;

// ================================================================
// Modules
// ================================================================

// Tip taper — soft cone at the bottom so the tip never snags the rotating
// funnel cone underneath, even if the part wobbles slightly around its axis.
module shaft_tip() {
    translate([0, 0, tip_clearance])
        cylinder(r1=shaft_core_d/4, r2=shaft_core_d/2, h=tip_taper_h);
}

// Central core — the load-bearing rod. The helix root attaches here and the
// top of this rod becomes the base of the M3 stud.
module shaft_core() {
    translate([0, 0, shaft_body_z0])
        cylinder(d=shaft_core_d, h=shaft_body_h);
}

// Top stud — protrudes above the tube's drive cap so the user can clamp it
// to a stationary frame. Wider than the shaft core to give the M3 pilot
// hole 1.5 mm of wall after tapping.
module top_stud() {
    translate([0, 0, total_height])
        cylinder(d=stud_d, h=stud_h);
}

// Helical fin — same geometry as the v2 single-start helix, but rooted on
// the central shaft rather than overlapping a tube wall. Top/bottom of the
// fin overlap into the shaft core by a small Δz to avoid coincident-surface
// CGAL union failures (same fix as v2.1 for the original monolithic part).
fin_z_overlap   = 0.2;    // mm — fin sinks into shaft body axially

module helical_fin() {
    fin_width = fin_outer_r - fin_inner_r;             // 5.5 mm
    z_start   = helix_z_start - fin_z_overlap;
    z_height  = helix_height + 2 * fin_z_overlap;
    translate([0, 0, z_start])
    linear_extrude(
        height    = z_height,
        twist     = turns * 360,
        slices    = total_slices,
        convexity = 10
    ) {
        translate([(fin_inner_r + fin_outer_r) / 2, 0])
            square([fin_width, fin_thickness], center=true);
    }
}

// ================================================================
// Assembly — fixed inner shaft as a single manifold solid.
// ================================================================
module auger_shaft() {
    color("#E8A33D", 0.95)
    difference() {
        union() {
            shaft_tip();
            shaft_core();
            top_stud();
            helical_fin();
        }
        // M3 pilot hole — drilled down from the stud face into the shaft top.
        translate([0, 0, total_height + stud_h - m3_pilot_depth + 0.1])
            cylinder(d=m3_pilot_d, h=m3_pilot_depth + 0.2);
    }
}

// Render this part standalone (used by render_print.sh).
auger_shaft();
