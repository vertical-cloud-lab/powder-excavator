#!/usr/bin/env bash
# ============================================================================
# Powder Excavator — Archimedes auger v3 print-prep pipeline.
#
# v3 splits the auger into TWO printable parts (per PR review):
#   * auger-shaft.scad   — FIXED inner shaft + helical fin (anchored at top)
#   * auger-housing.scad — ROTATING outer tube + funnel + drive cap
# Each part is rendered, manifold-checked, exported to STEP, and sliced
# independently for the project's two FDM rigs (MK3S+, Ender-3).
#
# Outputs (next to this script):
#   auger-shaft.stl                       FIXED shaft, binary STL (single part)
#   auger-shaft.stp                       FIXED shaft, STEP (faceted B-rep)
#   auger-housing.stl                     ROTATING tube, binary STL
#   auger-housing.stp                     ROTATING tube, STEP
#   archimedes-auger-iso.png              Assembled iso preview (both parts)
#   archimedes-auger-cutaway.png          Assembled half-cutaway preview
#   slices/auger-shaft.MK3S.gcode         PrusaSlicer slice of shaft, MK3S+
#   slices/auger-shaft.Ender3.gcode       PrusaSlicer slice of shaft, Ender-3
#   slices/auger-housing.MK3S.gcode       PrusaSlicer slice of housing, MK3S+
#   slices/auger-housing.Ender3.gcode     PrusaSlicer slice of housing, Ender-3
#   slices/SHAFT.gcode                    Ender-3 USB short-name copy of shaft
#   slices/HOUSING.gcode                  Ender-3 USB short-name copy of housing
# Plus optional CuraEngine slices via slice_cura.sh.
#
# Pre-reqs: openscad, admesh, prusa-slicer, freecadcmd, xvfb-run.
#   sudo apt-get install -y openscad admesh prusa-slicer freecad xvfb
# ============================================================================
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ASM_SCAD="${HERE}/archimedes-auger.scad"
ISO_PNG="${HERE}/archimedes-auger-iso.png"
CUT_PNG="${HERE}/archimedes-auger-cutaway.png"
SLICES_REPO_DIR="${HERE}/slices"
SLICE_DIR="${SLICE_DIR:-/tmp/auger}"

NOZZLE_DIAMETER="${NOZZLE_DIAMETER:-0.4}"
LAYER_HEIGHT="${LAYER_HEIGHT:-0.2}"
FILAMENT_TYPE="${FILAMENT_TYPE:-PLA}"

mkdir -p "${SLICE_DIR}" "${SLICES_REPO_DIR}"

# Two parts to process. `name` is the SCAD/STL/STEP basename. `usb_short`
# is the 8.3-DOS copy name for the Ender-3's stock LCD12864.
PARTS=(
    "auger-shaft   SHAFT"
    "auger-housing HOUSING"
)

# ----------------------------------------------------------------------------
# Per-part: SCAD -> STL -> admesh check -> STEP
# ----------------------------------------------------------------------------
for entry in "${PARTS[@]}"; do
    read -r name _ <<<"${entry}"
    scad="${HERE}/${name}.scad"
    stl="${HERE}/${name}.stl"
    stp="${HERE}/${name}.stp"

    echo "==> [${name}] OpenSCAD render -> ${stl}"
    xvfb-run -a openscad -o "${stl}" --export-format=binstl "${scad}"

    echo "==> [${name}] admesh manifold check"
    admesh -fundecvb "${SLICE_DIR}/${name}-clean.stl" "${stl}" \
        | grep -E '(Number of parts|disconnected|Degenerate|Volume)' | head -6

    echo "==> [${name}] STL -> STEP via FreeCAD (faceted B-rep)"
    # OpenSCAD's kernel is mesh-based and has no native STEP exporter; convert
    # via FreeCAD's OCCT bindings. Soft-fail if FreeCAD missing — STL is
    # primary; STEP is the consumer-friendly companion.
    if command -v freecadcmd >/dev/null 2>&1; then
        freecadcmd "${HERE}/stl_to_step.py" "${stl}" "${stp}" 2>&1 | tail -3 || true
        ls -la "${stp}" 2>/dev/null || \
            echo "  (STEP not produced — continuing without)"
    else
        echo "  (freecadcmd missing — skipping STEP for ${name})"
    fi
done

# ----------------------------------------------------------------------------
# Assembled-view preview PNGs (iso + half-cutaway). Operate on the assembly
# SCAD (which `use<>`s both part files) so the preview shows the in-place
# fit between the fixed shaft and rotating housing.
# ----------------------------------------------------------------------------
echo "==> Assembled preview PNGs (iso + half-cutaway)"
xvfb-run -a openscad -o "${ISO_PNG}" --imgsize=600,800 \
    --autocenter --viewall --colorscheme=Tomorrow "${ASM_SCAD}"

CUT_SCAD="$(mktemp --suffix=.scad)"
cat > "${CUT_SCAD}" <<EOSCAD
use <${HERE}/auger-shaft.scad>
use <${HERE}/auger-housing.scad>
difference() {
    union() { auger_housing(); auger_shaft(); }
    translate([-11, -0.5, -1]) cube([22, 12, 115]);
}
EOSCAD
xvfb-run -a openscad -o "${CUT_PNG}" --imgsize=600,800 \
    --camera=0,0,55,75,0,30,260 --colorscheme=Tomorrow "${CUT_SCAD}"
rm -f "${CUT_SCAD}"

# ----------------------------------------------------------------------------
# Slice each part with PrusaSlicer CLI for the project's two FDM rigs
# (PR #7 §6: Original Prusa MK3S+ and Creality Ender-3, both 1.75 mm PLA).
# Identical settings across parts so any slicer-time/material delta is
# attributable to geometry, not configuration drift.
# ----------------------------------------------------------------------------
slice_one () {
    local stl="$1" out="$2" temp="$3" first_temp="$4" bed="$5" extra_start="$6"
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
        --end-gcode $'M104 S0\nM140 S0\nG28 X\nM84\n' \
        "${stl}" 2>&1 | tail -3
    grep -E '^; (estimated printing time|filament used \[(mm|cm3)\])' "${out}" \
        | sed 's/^/      /'
}

# Bed-shape strings (PrusaSlicer expects polygon vertices) and start blocks.
# NOTE: $'...' ANSI-C quoting expands \n to real newlines BEFORE the string
# is handed to PrusaSlicer; plain "..." would write a literal "\n" into the
# start-gcode block, producing one mangled line that Marlin would reject.
MK3S_BED='0x0,250x0,250x210,0x210'
ENDER_BED='0x0,220x0,220x220,0x220'
MK3S_START=$'M201 X1000 Y1000 Z200 E5000\nM862.3 P"MK3S"\nG28\nG1 Z5 F5000\n'
ENDER_START=$'G28\nG1 Z5 F5000\n'

for entry in "${PARTS[@]}"; do
    read -r name usb_short <<<"${entry}"
    stl="${HERE}/${name}.stl"
    mk3s_out="${SLICES_REPO_DIR}/${name}.MK3S.gcode"
    ender_out="${SLICES_REPO_DIR}/${name}.Ender3.gcode"
    short_out="${SLICES_REPO_DIR}/${usb_short}.gcode"

    echo "==> [${name}] PrusaSlicer -> MK3S+"
    slice_one "${stl}" "${mk3s_out}" 215 215 "${MK3S_BED}" "${MK3S_START}"

    echo "==> [${name}] PrusaSlicer -> Ender-3"
    slice_one "${stl}" "${ender_out}" 200 205 "${ENDER_BED}" "${ENDER_START}"

    # Short-name 8.3 copy for the Ender-3's stock LCD12864, which truncates
    # long filenames. Same toolpath as the long-named Ender-3 file.
    cp "${ender_out}" "${short_out}"
done

# ----------------------------------------------------------------------------
# Optional CuraEngine slices for parity with what most desktop Cura users run.
# Soft-fail if the snap isn't installed — PrusaSlicer outputs are primary.
# ----------------------------------------------------------------------------
echo
echo "==> [bonus] CuraEngine slices (Ultimaker Cura toolchain)"
if bash "${HERE}/slice_cura.sh"; then
    echo "    (CuraEngine slices written under ${SLICES_REPO_DIR}/)"
else
    echo "    (CuraEngine slice skipped — install with 'sudo snap install cura-slicer')" >&2
fi

echo
echo "==> Done."
echo "    Shaft:    ${HERE}/auger-shaft.{stl,stp}"
echo "    Housing:  ${HERE}/auger-housing.{stl,stp}"
echo "    Iso:      ${ISO_PNG}"
echo "    Cutaway:  ${CUT_PNG}"
echo "    G-code:   ${SLICES_REPO_DIR}/{auger-shaft,auger-housing}.{MK3S,Ender3}.gcode"
echo "    USB:      ${SLICES_REPO_DIR}/{SHAFT,HOUSING}.gcode"
