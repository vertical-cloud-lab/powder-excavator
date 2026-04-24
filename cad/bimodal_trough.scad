// =====================================================================
// bimodal_trough.scad
// ---------------------------------------------------------------------
// Parametric, monolithic 3D-printable model of the bimodal compliant
// trough mechanism analysed in scripts/bimodal_compliance.py.
//
// The geometry is a symmetric von Mises truss flexure pair (two shallow
// pre-curved beams joined at an apex) carrying a tiltable trough. The
// design is *monolithic* — the compliant pivots are the flexures
// themselves, so the printed part has no fasteners, no support, and no
// assembly (just bolt the base to the gantry). When pressed downward
// past the dead-centre line the apex snaps from the "scoop" pose to the
// "dump" pose; releasing the load returns it via the second well.
//
// The module is *parametric*: every dimension that the analyser uses is
// re-exposed here so a redesign in scripts/bimodal_compliance.py can be
// reflected by editing the corresponding variable below (and rerunning
// the analyser to confirm it's still bimodal).
//
// Render to STL from the CLI (no GUI required):
//
//     openscad -o cad/bimodal-trough.stl cad/bimodal_trough.scad
//
// Render an isometric preview PNG:
//
//     openscad -o cad/bimodal-trough-iso.png \
//         --imgsize=1100,800 --camera=0,0,8,55,0,25,180 \
//         --colorscheme=Tomorrow cad/bimodal_trough.scad
//
// Tested with OpenSCAD 2021.01.
// =====================================================================

// ---------- Parameters (mirror scripts/bimodal_compliance.py defaults)
half_span      = 20.0;   // b  : half distance between flexure feet [mm]
initial_rise   =  4.0;   // h0 : as-built rise of the apex above feet [mm]
flexure_thick  =  0.6;   // t  : flexure thickness in bending dir.   [mm]
flexure_width  =  6.0;   // w  : flexure width (out-of-plane)        [mm]

// ---------- Frame / base
base_thick     =  3.0;   // base plate thickness                     [mm]
base_pad       = 10.0;   // extra material around feet               [mm]
mount_hole_d   =  3.4;   // M3 clearance                             [mm]
mount_hole_dx  = 30.0;   // hole pitch along x                       [mm]
mount_hole_dy  = 14.0;   // hole pitch along y                       [mm]

// ---------- Trough (the powder-carrying channel sat on top of the apex)
trough_len     = 60.0;   // along the bed                            [mm]
trough_outer_w = 18.0;   // overall channel width                    [mm]
trough_wall    =  1.6;   // channel side-wall thickness              [mm]
trough_depth   =  8.0;   // channel depth                            [mm]
trough_floor   =  1.6;   // channel floor thickness                  [mm]
apex_block_h   =  4.0;   // height of the rigid apex block under the trough

// ---------- Pre-curve "kick" of the flexures
//   The analyser bakes pre-compression in mathematically (1.5%); the
//   printed part bakes it in *geometrically* by shaping each flexure
//   as a shallow arch whose chord is shorter than its arclength. That
//   way the stress-free printed shape already sits at one of the two
//   wells — no assembly pre-stress needed.
flex_arch_kick =  0.6;   // additional sag of the flexure midpoint   [mm]

// ---------- Render quality
$fa = 2;   // facet angle  [deg]
$fs = 0.4; // facet size   [mm]
flex_segments = 60;       // # of segments along each flexure arch

// =====================================================================
// Helpers
// =====================================================================

// A 2-D arch from (x0, y0) to (x1, y1). The straight chord between the
// endpoints is bulged above by ``mid_kick`` at the parametric midpoint
// (i.e. the curve is the chord plus a parabolic offset of ``mid_kick``
// at u=0.5). Returned as a list of [x, y] points.
//
// This shape is what bakes the geometric pre-compression into the
// printed flexure: the arclength of the curve is greater than the
// straight chord between foot and apex, so the as-printed beam is
// already pre-compressed with no assembly stress.
function arch_points(x0, x1, y0, y1, mid_kick, n) =
    [ for (i = [0 : n]) let (
        u  = i / n,
        x  = x0 + (x1 - x0) * u,
        y  = y0 + (y1 - y0) * u + 4 * mid_kick * u * (1 - u)
      ) [x, y] ];

// Build the two surfaces of a constant-thickness arched beam by
// offsetting the centreline normal to itself.
module arched_beam(x0, x1, y0, y1, mid_kick, thick, n) {
    pts = arch_points(x0, x1, y0, y1, mid_kick, n);
    // build top and bottom polylines by offsetting along local normals
    tops = [ for (i = [0 : n]) let (
        prev = pts[max(i-1, 0)],
        next = pts[min(i+1, n)],
        tx   = next[0] - prev[0],
        ty   = next[1] - prev[1],
        L    = sqrt(tx*tx + ty*ty),
        nx   = -ty / L,
        ny   =  tx / L
      ) [pts[i][0] + nx * thick / 2,
         pts[i][1] + ny * thick / 2] ];
    bots = [ for (i = [0 : n]) let (
        prev = pts[max(i-1, 0)],
        next = pts[min(i+1, n)],
        tx   = next[0] - prev[0],
        ty   = next[1] - prev[1],
        L    = sqrt(tx*tx + ty*ty),
        nx   = -ty / L,
        ny   =  tx / L
      ) [pts[i][0] - nx * thick / 2,
         pts[i][1] - ny * thick / 2] ];
    polygon(points = concat(tops, [for (i = [n : -1 : 0]) bots[i]]));
}

// =====================================================================
// Sub-assemblies
// =====================================================================

module base_plate() {
    foot_w = 8.0;
    plate_x = 2 * half_span + 2 * (foot_w + base_pad);
    plate_y = flexure_width + 2 * base_pad;
    difference() {
        translate([-plate_x/2, -plate_y/2, -base_thick])
            cube([plate_x, plate_y, base_thick]);
        // four M3 mounting holes on a rectangular pattern
        for (sx = [-1, 1]) for (sy = [-1, 1])
            translate([sx * mount_hole_dx, sy * mount_hole_dy, -base_thick - 0.1])
                cylinder(d = mount_hole_d, h = base_thick + 0.2);
    }
    // anchor blocks that root the flexures
    for (sx = [-1, 1])
        translate([sx * (half_span + foot_w/2) - foot_w/2, -flexure_width/2, 0])
            cube([foot_w, flexure_width, 2.0]);
}

// One pre-curved flexure (root at +half_span on the bed, apex at the
// trough centreline). Mirrored with ``side = -1`` for the other beam.
//
// The curve runs from foot ``(±half_span, 0)`` to apex ``(0, initial_rise)``
// — i.e. the beam *climbs* from the bed up to the apex carrier — and is
// bulged above the straight chord by ``flex_arch_kick`` at its
// midpoint. The kick is what gives the printed beam an arclength
// greater than its chord, baking in the geometric pre-compression that
// the analyser models mathematically (1.5 % shorter natural length than
// chord). Setting ``flex_arch_kick = 0`` would give a straight foot-to-
// apex flexure that is monostable.
module flexure(side = +1) {
    x_root = side * (half_span);
    x_apex = 0;
    // extrude the 2-D arched beam through the out-of-plane width
    translate([0, -flexure_width / 2, 0])
        rotate([90, 0, 0])
        rotate([0, 0, 0])
        linear_extrude(height = flexure_width)
        // the arch is laid out in (x, z); build it directly
        arched_beam(x_root, x_apex, 0, initial_rise,
                    flex_arch_kick, flexure_thick, flex_segments);
}

// Rigid apex carrier: a small block on top of the apex that the trough
// is fused to and that the two flexures merge into.
module apex_block() {
    bx = 12.0;
    by = flexure_width;
    bz = apex_block_h;
    translate([-bx/2, -by/2, initial_rise - 0.5])
        cube([bx, by, bz]);
}

// The powder-carrying trough sat on top of the apex carrier.
module trough() {
    z0 = initial_rise - 0.5 + apex_block_h;
    // outer body
    difference() {
        translate([-trough_len/2, -trough_outer_w/2, z0])
            cube([trough_len, trough_outer_w, trough_floor + trough_depth]);
        // hollow out the channel
        translate([-trough_len/2 + trough_wall,
                   -trough_outer_w/2 + trough_wall,
                    z0 + trough_floor])
            cube([trough_len - 2 * trough_wall,
                  trough_outer_w - 2 * trough_wall,
                  trough_depth + 1]);
    }
}

// =====================================================================
// Top-level assembly
// =====================================================================

module bimodal_trough() {
    color([0.85, 0.85, 0.88]) base_plate();
    color([0.95, 0.55, 0.45]) flexure(+1);
    color([0.95, 0.55, 0.45]) flexure(-1);
    color([0.85, 0.85, 0.88]) apex_block();
    color([0.85, 0.85, 0.88]) trough();
}

bimodal_trough();
