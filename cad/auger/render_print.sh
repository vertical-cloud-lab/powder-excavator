#!/usr/bin/env bash
# ============================================================================
# Powder Excavator — Archimedes auger v2.1 print-prep pipeline.
#
# Mirrors the OpenSCAD → STL → checks → preview-PNG → slice flow used in
# PR #13 (sieve cup) and PR #2 (initial CAD pipeline). Headless via xvfb-run
# so it works in CI on the GitHub-hosted runner.
#
# Outputs (next to this script):
#   archimedes-auger.stl              binary STL (single manifold part)
#   archimedes-auger-iso.png          opaque isometric preview
#   archimedes-auger-cutaway.png      half-cutaway showing helix + funnel
#   /tmp/auger/archimedes-auger.gcode Ultimaker-class slice (PrusaSlicer CLI)
#
# Pre-reqs: openscad, admesh, prusa-slicer, xvfb-run.
#   sudo apt-get install -y openscad admesh prusa-slicer xvfb
#
# Filament note: standard Ultimaker filament is 2.85 mm. The PR comment
# floated "2.4 (?) mm" — we slice at 2.85 mm (the actual Ultimaker size).
# Override with FILAMENT_DIAMETER=1.75 (etc.) if printing on a Prusa/Ender.
# ============================================================================
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCAD="${HERE}/archimedes-auger.scad"
STL="${HERE}/archimedes-auger.stl"
ISO_PNG="${HERE}/archimedes-auger-iso.png"
CUT_PNG="${HERE}/archimedes-auger-cutaway.png"
SLICE_DIR="${SLICE_DIR:-/tmp/auger}"
GCODE="${SLICE_DIR}/archimedes-auger.gcode"

FILAMENT_DIAMETER="${FILAMENT_DIAMETER:-2.85}"   # Ultimaker default
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

echo "==> [4/4] PrusaSlicer slice for Ultimaker-class FDM"
echo "    filament=${FILAMENT_DIAMETER}mm nozzle=${NOZZLE_DIAMETER}mm" \
     "layer=${LAYER_HEIGHT}mm material=${FILAMENT_TYPE}"
prusa-slicer --export-gcode --output "${GCODE}" \
    --filament-diameter "${FILAMENT_DIAMETER}" \
    --nozzle-diameter   "${NOZZLE_DIAMETER}" \
    --filament-type     "${FILAMENT_TYPE}" \
    --temperature 205 --bed-temperature 60 \
    --first-layer-temperature 210 --first-layer-bed-temperature 60 \
    --layer-height "${LAYER_HEIGHT}" --first-layer-height "${LAYER_HEIGHT}" \
    --perimeters 3 --top-solid-layers 4 --bottom-solid-layers 4 \
    --fill-density 40% --fill-pattern gyroid \
    --skirts 1 --skirt-distance 5 \
    --brim-width 4 \
    --support-material --support-material-auto \
    --support-material-threshold 50 \
    "${STL}" 2>&1 | tail -15

echo
echo "==> Done."
echo "    STL:     ${STL}"
echo "    Iso:     ${ISO_PNG}"
echo "    Cutaway: ${CUT_PNG}"
echo "    G-code:  ${GCODE}"
grep -E '^; (estimated|filament used|total)' "${GCODE}" | head -6 || true
