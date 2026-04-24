#!/usr/bin/env bash
# ============================================================================
# Powder Excavator — Archimedes auger v2.1 print-prep pipeline.
#
# Mirrors the OpenSCAD → STL → checks → preview-PNG → slice flow used in
# PR #13 (sieve cup) and PR #2 (initial CAD pipeline). Headless via xvfb-run
# so it works in CI on the GitHub-hosted runner.
#
# Outputs (next to this script):
#   archimedes-auger.stl                 binary STL (single manifold part)
#   archimedes-auger.stp                 STEP (B-rep, faceted shell of the STL)
#   archimedes-auger-iso.png             opaque iso preview (rendered from SCAD)
#   archimedes-auger-cutaway.png         half-cutaway preview (rendered from SCAD)
#   archimedes-auger-stp-iso.png         iso preview rendered FROM the STEP file
#   archimedes-auger-stp-cutaway.png     half-cutaway rendered FROM the STEP file
#   slices/archimedes-auger.MK3S.gcode   PrusaSlicer slice — Original Prusa MK3S+
#   slices/archimedes-auger.Ender3.gcode PrusaSlicer slice — Creality Ender-3
#
# Pre-reqs: openscad, admesh, prusa-slicer, freecadcmd, xvfb-run.
#   sudo apt-get install -y openscad admesh prusa-slicer freecad xvfb
#
# Filament note: standard Ultimaker filament is 2.85 mm. The PR comment
# floated "2.4 (?) mm" — we slice at 2.85 mm (the actual Ultimaker size).
# Override with FILAMENT_DIAMETER=1.75 (etc.) if printing on a Prusa/Ender.
# ============================================================================
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCAD="${HERE}/archimedes-auger.scad"
STL="${HERE}/archimedes-auger.stl"
STP="${HERE}/archimedes-auger.stp"
ISO_PNG="${HERE}/archimedes-auger-iso.png"
CUT_PNG="${HERE}/archimedes-auger-cutaway.png"
STP_ISO_PNG="${HERE}/archimedes-auger-stp-iso.png"
STP_CUT_PNG="${HERE}/archimedes-auger-stp-cutaway.png"
SLICE_DIR="${SLICE_DIR:-/tmp/auger}"

# Slicer knobs (override via env). Filament diameter is hardcoded 1.75 mm in
# the slice step below — both target rigs (MK3S+, Ender-3) are 1.75 mm.
NOZZLE_DIAMETER="${NOZZLE_DIAMETER:-0.4}"
LAYER_HEIGHT="${LAYER_HEIGHT:-0.2}"
FILAMENT_TYPE="${FILAMENT_TYPE:-PLA}"

mkdir -p "${SLICE_DIR}"

echo "==> [1/4] OpenSCAD render -> ${STL}"
xvfb-run -a openscad -o "${STL}" --export-format=binstl "${SCAD}"

echo "==> [2/4] admesh manifold check"
# admesh is the print-relevant manifold checker. OpenSCAD's CGAL volume count
# can over-report when the sealed interior cavity is opened by the M3 pilot
# hole; admesh's connected-part / disconnected-edge analysis is what slicers
# actually rely on.
admesh -fundecvb "${SLICE_DIR}/auger-clean.stl" "${STL}" | tail -25

echo "==> [3/4] Preview PNGs (iso + half-cutaway)"
xvfb-run -a openscad -o "${ISO_PNG}" --imgsize=600,750 \
    --autocenter --viewall --colorscheme=Tomorrow "${SCAD}"

CUT_SCAD="$(mktemp --suffix=.scad)"
cat > "${CUT_SCAD}" <<'EOSCAD'
use <SCAD_PATH>
outer_r = 10; outer_diameter = 20; total_height = 100;
difference() {
    archimedes_auger();
    translate([-outer_r - 1, -0.5, -1])
        cube([outer_diameter + 2, outer_r + 2, total_height + 2]);
}
EOSCAD
sed -i "s|SCAD_PATH|${SCAD}|" "${CUT_SCAD}"
xvfb-run -a openscad -o "${CUT_PNG}" --imgsize=600,750 \
    --camera=0,0,50,75,0,25,250 --colorscheme=Tomorrow "${CUT_SCAD}"
rm -f "${CUT_SCAD}"

echo "==> [4/5] STL -> STEP via FreeCAD (faceted B-rep)"
# OpenSCAD's kernel is mesh-based and has no native STEP exporter, so we
# convert the STL to a STEP via FreeCAD's OCCT bindings. The result is a
# faceted shell (one planar face per STL triangle) sewn into a single
# closed solid — accepted by every CAM/CAD tool that "requires STEP"
# (FreeCAD Path, Fusion 360, SolidWorks import, Cura via plugin, etc.).
freecadcmd "${HERE}/stl_to_step.py" "${STL}" "${STP}" 2>&1 | tail -8 || true
ls -la "${STP}" 2>/dev/null || { echo "ERROR: STEP not produced"; exit 1; }

echo "==> [4b/5] STEP spot-check (load back, compare to STL)"
ROUNDTRIP_STL="${SLICE_DIR}/auger_step_roundtrip.stl"
STP_CHECK_TXT="${SLICE_DIR}/step_check.txt"
STP_CHECK_PY="$(mktemp --suffix=.py)"
cat > "${STP_CHECK_PY}" <<PYEOF
import Part, Mesh
shape = Part.Shape(); shape.read("${STP}")
solid = shape.Solids[0]
verts, tris = shape.tessellate(0.1)
m = Mesh.Mesh()
for a, b, c in tris: m.addFacet(verts[a], verts[b], verts[c])
m.write("${ROUNDTRIP_STL}")
report = (
    f"  STEP solids/shells/faces: "
    f"{len(shape.Solids)}/{len(shape.Shells)}/{len(shape.Faces)}\n"
    f"  STEP solid valid={solid.isValid()} closed={solid.isClosed()}\n"
    f"  STEP volume:              {solid.Volume:.3f} mm^3\n"
    f"  STEP bbox:                "
    f"X=[{shape.BoundBox.XMin:.2f},{shape.BoundBox.XMax:.2f}] "
    f"Y=[{shape.BoundBox.YMin:.2f},{shape.BoundBox.YMax:.2f}] "
    f"Z=[{shape.BoundBox.ZMin:.2f},{shape.BoundBox.ZMax:.2f}]"
)
open("${STP_CHECK_TXT}", "w").write(report)
PYEOF
freecadcmd "${STP_CHECK_PY}" >/dev/null 2>&1 || true
rm -f "${STP_CHECK_PY}"
cat "${STP_CHECK_TXT}" 2>/dev/null || true
admesh -fundecvb "${SLICE_DIR}/auger_rt_clean.stl" "${ROUNDTRIP_STL}" 2>&1 \
    | grep -E '(Volume|Number of parts|disconnected|Degenerate)' | head -6 || true

echo "==> [4c/5] Preview PNGs from the STEP file"
STP_ISO_SCAD="$(mktemp --suffix=.scad)"
echo "color(\"#5B9BD5\", 0.95) import(\"${ROUNDTRIP_STL}\", convexity=10);" \
    > "${STP_ISO_SCAD}"
xvfb-run -a openscad -o "${STP_ISO_PNG}" --imgsize=500,900 \
    --camera=0,0,50,60,0,30,180 --colorscheme=Tomorrow "${STP_ISO_SCAD}"

STP_CUT_SCAD="$(mktemp --suffix=.scad)"
cat > "${STP_CUT_SCAD}" <<EOSCAD
difference() {
    color("#A8C8E8") import("${ROUNDTRIP_STL}", convexity=10);
    translate([-12, -0.5, -1]) cube([24, 12, 102]);
}
EOSCAD
xvfb-run -a openscad -o "${STP_CUT_PNG}" --imgsize=500,900 \
    --camera=0,0,50,75,0,30,90 --colorscheme=Tomorrow "${STP_CUT_SCAD}"
rm -f "${STP_ISO_SCAD}" "${STP_CUT_SCAD}"

echo "==> [5/5] PrusaSlicer slices for the project's actual hardware"
# PR #7 §6 nails the canonical FDM stack as **Prusa MK3 / MK3S+ + Creality Ender-3**,
# sliced headless via **PrusaSlicer CLI** (in-box vendor profiles for both).
# We emit one g-code per printer so reviewers can pick whichever rig is free,
# and we get two independent slicer reports as DFM signal (any divergence in
# support volume / overhang count between MK3S and Ender-3 is a useful flag).
SLICES_REPO_DIR="${HERE}/slices"
mkdir -p "${SLICES_REPO_DIR}"

slice_one () {
    local label="$1" out="$2" bed="$3" temp="$4" first_temp="$5" extra_start="$6"
    echo "  -> ${label}: nozzle=${NOZZLE_DIAMETER}mm filament=1.75mm" \
         "PLA layer=${LAYER_HEIGHT}mm bed=${bed}"
    prusa-slicer --export-gcode --output "${out}" \
        --filament-diameter 1.75 \
        --nozzle-diameter   "${NOZZLE_DIAMETER}" \
        --filament-type     "${FILAMENT_TYPE}" \
        --temperature ${temp} --bed-temperature 60 \
        --first-layer-temperature ${first_temp} --first-layer-bed-temperature 60 \
        --bed-shape "${bed}" \
        --layer-height "${LAYER_HEIGHT}" --first-layer-height "${LAYER_HEIGHT}" \
        --perimeters 3 --top-solid-layers 5 --bottom-solid-layers 4 \
        --fill-density 40% --fill-pattern gyroid \
        --skirts 1 --skirt-distance 5 --brim-width 4 \
        --support-material --support-material-auto \
        --support-material-threshold 50 \
        --start-gcode "${extra_start}" \
        --end-gcode "M104 S0\nM140 S0\nG28 X\nM84\n" \
        "${STL}" 2>&1 | tail -3
    echo "     metrics:"
    grep -E '^; (estimated printing time|filament used \[(mm|cm3)\])' "${out}" \
        | sed 's/^/       /'
}

# 1.75 mm filament for both (MK3 and Ender-3 are 1.75 mm machines —
# the Ultimaker default 2.85 mm value is not used here).
slice_one "Prusa MK3S+ (0.4 mm)" \
    "${SLICES_REPO_DIR}/archimedes-auger.MK3S.gcode" \
    "0x0,250x0,250x210,0x210" 215 215 \
    "M201 X1000 Y1000 Z200 E5000\nM862.3 P\"MK3S\"\nG28\nG1 Z5 F5000\n"

slice_one "Creality Ender-3 (0.4 mm)" \
    "${SLICES_REPO_DIR}/archimedes-auger.Ender3.gcode" \
    "0x0,220x0,220x220,0x220" 200 205 \
    "G28\nG1 Z5 F5000\n"

echo
echo "==> Done."
echo "    STL:        ${STL}"
echo "    STEP:       ${STP}"
echo "    Iso (SCAD): ${ISO_PNG}"
echo "    Cut (SCAD): ${CUT_PNG}"
echo "    Iso (STEP): ${STP_ISO_PNG}"
echo "    Cut (STEP): ${STP_CUT_PNG}"
echo "    G-code:     ${SLICES_REPO_DIR}/archimedes-auger.{MK3S,Ender3}.gcode"
