// ================================================================
// Powder Excavator — Archimedes Auger Attachment
// ================================================================
//
// One-piece rotating helical dispenser.
// The entire unit mounts to the frankenmitsu spindle via M3 and
// rotates as a single body. Powder loaded from the top through
// four loading slots before mounting. Spindle rotation drives
// powder down the helical channel to the exit hole at the bottom.
//
// Mechanism: rotating helical chute (gravity-assisted).
// As the unit spins, the helical fin continuously agitates and
// advances powder downward. Rotation speed controls dose rate.
// Closed-loop gravimetric feedback (load cell) handles precision.
//
// Print:   PLA or PETG, 0.2mm layer height, 0.4mm nozzle
//          Print VERTICALLY (flat bottom on build plate)
//          40% infill on fins, 3+ perimeters on outer walls
//          No supports needed if printed vertically
//
// Render:  Paste into https://openscad.org/demo/ and click Render
//
// Export:  File → Export → Export as STL (Part A: full assembly)
//
// ================================================================

/* [Main Dimensions] */
outer_diameter  = 20;    // mm — outer cylinder OD (= 2cm width)
total_height    = 100;   // mm — total length (= 10cm)
wall_thickness  = 2;     // mm — outer tube wall thickness

/* [M3 Mount — Top] */
m3_pilot_d      = 2.5;   // mm — M3 pilot hole diameter (tap to M3 after printing)
m3_pilot_depth  = 10;    // mm — depth of M3 pilot hole
top_cap_height  = 4;     // mm — solid cap thickness at top

/* [Powder Exit — Bottom] */
// 2.5mm chosen as optimal: large enough to prevent bridging for
// micron-scale cohesive powders with auger-assisted flow,
// small enough for controlled deposition.
exit_hole_d     = 2.5;   // mm — exit hole at bottom center
bottom_cap_h    = 4;     // mm — solid cap thickness at bottom

/* [Helical Fin Geometry] */
pitch           = 10;    // mm per full 360° rotation
// Steeper pitch → larger helix angle → better gravity flow
// 10mm pitch gives ~18° helix angle at mid-radius: good for PLA printing
// and gravity-assisted powder flow.

fin_thickness   = 2;     // mm — fin blade thickness (printable on Prusa: min ~1.6mm)
fin_inner_r     = 1.5;   // mm — fin inner edge radius (leaves center clear for exit flow)
// fin outer edge = inner_r of tube (full contact with inner wall)

/* [Loading Slots — Top Cap] */
slot_count      = 4;     // number of powder loading slots
slot_width      = 3;     // mm
slot_length     = 6;     // mm
slot_radius     = 5;     // mm from center to slot midpoint

// ================================================================
// Derived values — do not edit below unless you know what you're doing
// ================================================================

inner_d         = outer_diameter - 2 * wall_thickness;  // 16mm
inner_r         = inner_d / 2;                           // 8mm
outer_r         = outer_diameter / 2;                    // 10mm
helix_z_start   = bottom_cap_h;
helix_z_end     = total_height - top_cap_height;
helix_height    = helix_z_end - helix_z_start;           // 92mm
turns           = helix_height / pitch;                  // 9.2 turns
slices_per_turn = 80;
total_slices    = ceil(turns * slices_per_turn);

$fn = 64;

// ================================================================
// Modules
// ================================================================

// Outer tube walls (hollow cylinder)
module tube_walls() {
    difference() {
        cylinder(r=outer_r, h=total_height);
        translate([0, 0, -0.1])
            cylinder(r=inner_r, h=total_height + 0.2);
    }
}

// Bottom cap with exit hole
module bottom_cap() {
    difference() {
        cylinder(r=outer_r, h=bottom_cap_h);
        translate([0, 0, -0.1])
            cylinder(d=exit_hole_d, h=bottom_cap_h + 0.2);
    }
}

// Top cap with M3 pilot hole and powder loading slots
module top_cap() {
    difference() {
        translate([0, 0, total_height - top_cap_height])
            cylinder(r=outer_r, h=top_cap_height);

        // M3 pilot hole (center)
        translate([0, 0, total_height - m3_pilot_depth])
            cylinder(d=m3_pilot_d, h=m3_pilot_depth + 0.1);

        // Powder loading slots (4x, evenly spaced)
        for (i = [0 : slot_count - 1]) {
            angle = i * (360 / slot_count);
            translate([0, 0, total_height - top_cap_height - 0.1])
            rotate([0, 0, angle])
            translate([slot_radius, 0, 0])
                cube([slot_length, slot_width, top_cap_height + 0.2], center=true);
        }
    }
}

// Helical fin — the Archimedes element
// A thin rectangular blade, extruded with twist, spans from
// fin_inner_r to inner_r (inner wall). Connects to the tube walls
// structurally. One-start helix.
module helical_fin() {
    fin_width = inner_r - fin_inner_r;  // 6.5mm
    translate([0, 0, helix_z_start])
    linear_extrude(
        height    = helix_height,
        twist     = turns * 360,
        slices    = total_slices,
        convexity = 10
    ) {
        // 2D cross-section: rectangle from fin_inner_r to inner_r
        translate([(fin_inner_r + inner_r) / 2, 0])
            square([fin_width, fin_thickness], center=true);
    }
}

// ================================================================
// Assembly
// ================================================================

module archimedes_auger() {
    color("#5B9BD5", 0.85)
    union() {
        tube_walls();
        bottom_cap();
        top_cap();
        helical_fin();
    }
}

// ================================================================
// Render
// ================================================================

archimedes_auger();

// ================================================================
// Cross-section preview (comment out above, uncomment below)
// ================================================================
// difference() {
//     archimedes_auger();
//     translate([-outer_r - 1, -0.5, -1])
//         cube([outer_diameter + 2, outer_r + 1, total_height + 2]);
// }
