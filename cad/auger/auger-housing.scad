// ================================================================
// Powder Excavator — Archimedes Auger: ROTATING outer tube (v3)
// ================================================================
//
// Two-part architecture. This file is the ROTATING outer housing.
// It rotates around the FIXED inner shaft (`auger-shaft.scad`).
//
// Drive: the frankenmitsu spindle attaches to the EXTERNAL drive flange
// at the top of this part (a 22 mm OD disc with a flat for a set-screw
// coupler). The shaft passes through the central clearance bore in the
// drive flange — that bore is the upper journal bearing.
//
// Powder path:
//   - Loaded through the four sectoral slots in the top drive cap that
//     surround the central shaft-clearance bore.
//   - Falls into the helix region between the rotating wall and the fixed
//     helix. The wall drags the powder against the helix flank; the fixed
//     helix deflects it downward (relative to the rotating reference frame
//     this is the same kinematics as a stationary tube + rotating screw).
//   - Exits through the on-axis hole in the bottom funnel cone.
//
// Fits (must match the value in `auger-shaft.scad`):
//   - Helix OD vs tube ID: 0.5 mm radial clearance per side.
//   - Shaft core OD vs top-cap bore: 0.5 mm radial clearance per side.
//
// Print orientation: exit-hole-down on the build plate (Z+ = drive cap).
// Same orientation as the v2 monolithic part, so the brim + support
// recipe carries over: 4 mm brim around the small annular bottom contact,
// auto-supports at 50° threshold for the funnel-cone underside and the
// top-cap bridges.
//
// ================================================================

/* [Main Dimensions — keep in sync with auger-shaft.scad] */
outer_diameter   = 20;    // mm — outer tube OD
total_height     = 100;   // mm — total tube height
wall_thickness   = 2;     // mm — outer tube wall

/* [Clearance / fit] */
radial_clearance = 0.5;   // mm — per-side gap (helix↔tube ID, shaft↔bore)

/* [Inner shaft — informational] */
shaft_core_d     = 4;     // mm — must match auger-shaft.scad
// Top-cap bore = shaft OD + 2*radial_clearance → 5.0 mm clearance bore.

/* [Top drive flange — external coupler attachment] */
// The flange is wider than the tube OD so a standard coupler can grip it
// with a set-screw on the external flat. Sits flush on top of the tube cap.
drive_flange_d   = 22;    // mm — flange OD (>= outer_diameter)
drive_flange_h   = 4;     // mm — flange thickness
flat_depth       = 0.6;   // mm — depth of set-screw flat machined into flange OD

/* [Top cap — closed lid with central shaft bore + loading slots] */
top_cap_h        = 4;     // mm — cap thickness (top of the rotating tube)
slot_count       = 4;     // sectoral powder-loading slots around shaft bore
slot_inner_r     = 4;     // mm — slot inner edge (just outside shaft-bore wall)
slot_outer_r     = inner_r() - 0.5;  // mm — slot outer edge (just inside outer wall)
slot_arc_deg     = 50;    // ° — angular width of each slot

/* [Bottom funnel — closed funnel with on-axis exit hole] */
exit_hole_d      = 3.0;   // mm — exit hole CAD (≈2.5 mm as printed at 0.4 mm)
bottom_cap_h     = 6;     // mm — funnel section height

// ================================================================
// Derived — do not edit
// ================================================================
function inner_r() = (outer_diameter - 2 * wall_thickness) / 2;   // 8 mm
function outer_r() = outer_diameter / 2;                           // 10 mm
function shaft_bore_d() = shaft_core_d + 2 * radial_clearance;     // 5 mm

$fn = 64;

// ================================================================
// Modules
// ================================================================

// Outer tube body — hollow cylinder, full height. Closed by top_cap and
// bottom_funnel; the inner cylindrical surface is what sweeps past the
// fixed helix during rotation.
module tube_walls() {
    difference() {
        cylinder(r=outer_r(), h=total_height);
        translate([0, 0, -0.1])
            cylinder(r=inner_r(), h=total_height + 0.2);
    }
}

// Bottom funnel — closes the bottom end of the tube and directs powder to
// the on-axis exit hole. Inner conical void widens upward from the exit
// hole to nearly the inner radius, matching the v2 funnel profile.
module bottom_funnel() {
    difference() {
        cylinder(r=outer_r(), h=bottom_cap_h);
        translate([0, 0, -0.1])
            cylinder(
                r1 = exit_hole_d / 2,         // narrow at z=0 (exit)
                r2 = inner_r() - 0.5,         // wide at top of funnel
                h  = bottom_cap_h + 0.2
            );
    }
}

// Top drive cap — closed lid with central shaft-clearance bore (the upper
// journal bearing) and four sectoral powder-loading slots around it. The
// drive flange + set-screw flat sit on top of this cap.
module top_drive_cap() {
    z_cap = total_height - top_cap_h;
    difference() {
        union() {
            // Flat closing disc that seals the tube against the rotating wall
            translate([0, 0, z_cap])
                cylinder(r=outer_r(), h=top_cap_h);
            // External drive flange — wider than the tube so a coupler can
            // grip the OD with a radial set-screw.
            translate([0, 0, total_height])
                cylinder(d=drive_flange_d, h=drive_flange_h);
        }
        // Central clearance bore — shaft passes through here. This bore is
        // the upper journal bearing.
        translate([0, 0, z_cap - 0.1])
            cylinder(d=shaft_bore_d(),
                     h=top_cap_h + drive_flange_h + 0.2);
        // Set-screw flat on flange OD — gives a coupler's grub screw a
        // square contact patch, prevents slip under torque.
        translate([drive_flange_d/2 - flat_depth,
                   -drive_flange_d/2,
                   total_height - 0.1])
            cube([flat_depth + 1, drive_flange_d, drive_flange_h + 0.2]);
        // Powder loading slots — sectoral cut-outs through the cap.
        for (i = [0 : slot_count - 1]) {
            angle = i * (360 / slot_count);
            rotate([0, 0, angle])
                slot_sector();
        }
    }
}

// One pie-slice slot through the cap, from slot_inner_r out to slot_outer_r,
// spanning slot_arc_deg degrees centred on +X. Built as the intersection of
// an annulus and a wedge so the inner/outer radii are exact circular arcs.
module slot_sector() {
    z_cap = total_height - top_cap_h;
    intersection() {
        // Annulus
        translate([0, 0, z_cap - 0.1])
        difference() {
            cylinder(r=slot_outer_r, h=top_cap_h + 0.2);
            translate([0, 0, -0.1])
                cylinder(r=slot_inner_r, h=top_cap_h + 0.4);
        }
        // Wedge
        translate([0, 0, z_cap - 0.2])
        rotate([0, 0, -slot_arc_deg / 2])
        linear_extrude(top_cap_h + 0.4)
        polygon([
            [0, 0],
            [slot_outer_r * 1.1, 0],
            [slot_outer_r * 1.1 * cos(slot_arc_deg),
             slot_outer_r * 1.1 * sin(slot_arc_deg)],
        ]);
    }
}

// ================================================================
// Assembly — rotating outer tube as a single manifold solid.
// ================================================================
module auger_housing() {
    color("#5B9BD5", 0.95)
    union() {
        tube_walls();
        bottom_funnel();
        top_drive_cap();
    }
}

// Render this part standalone (used by render_print.sh).
auger_housing();
