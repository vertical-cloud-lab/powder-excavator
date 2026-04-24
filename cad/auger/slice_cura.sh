#!/usr/bin/env bash
# ============================================================================
# Powder Excavator — Archimedes auger v3: CuraEngine (Ultimaker Cura) slices.
#
# Companion to render_print.sh. Slices BOTH parts of the v3 split design
# (auger-shaft.stl + auger-housing.stl) with Ultimaker's open-source slicing
# engine, for parity with what most desktop Cura users run.
#
# CuraEngine isn't packaged in the GitHub-hosted runner's apt repos. We
# install via `snap install cura-slicer`; falls back to a system PATH lookup
# if a user installed CuraEngine manually.
#
# Outputs (under cad/auger/slices/):
#   auger-shaft.MK3S.cura.gcode      Cura — shaft on Prusa MK3S+
#   auger-shaft.Ender3.cura.gcode    Cura — shaft on Creality Ender-3
#   auger-housing.MK3S.cura.gcode    Cura — housing on Prusa MK3S+
#   auger-housing.Ender3.cura.gcode  Cura — housing on Creality Ender-3
# ============================================================================
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SLICES_DIR="${HERE}/slices"
mkdir -p "${SLICES_DIR}"

PART_NAMES=(auger-shaft auger-housing)

# ---------------------------------------------------------------------------
# Locate CuraEngine + bundled resources. Try snap first (CI runner), then
# system PATH (manual installs).
# ---------------------------------------------------------------------------
find_cura () {
    local snap_root
    if [[ -d /snap/cura-slicer/current ]]; then
        snap_root=/snap/cura-slicer/current
    elif compgen -G "/snap/cura-slicer/[0-9]*" > /dev/null; then
        snap_root="$(ls -d /snap/cura-slicer/[0-9]* | sort -n | tail -1)"
    fi
    if [[ -n "${snap_root:-}" && -x "${snap_root}/usr/bin/CuraEngine" ]]; then
        CURA="${snap_root}/usr/bin/CuraEngine"
        export LD_LIBRARY_PATH="${snap_root}/usr/lib/x86_64-linux-gnu:${snap_root}/usr/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
        RES="${snap_root}/usr/share/cura/resources"
        return 0
    fi
    if command -v CuraEngine >/dev/null 2>&1; then
        CURA="$(command -v CuraEngine)"
        RES="${CURA_RESOURCES:-/usr/share/cura/resources}"
        return 0
    fi
    echo "ERROR: CuraEngine not found. Install with:" >&2
    echo "  sudo snap install cura-slicer" >&2
    return 1
}

find_cura

if [[ ! -d "${RES}/definitions" ]]; then
    echo "ERROR: Cura resources directory not found at ${RES}" >&2
    exit 1
fi
export CURA_ENGINE_SEARCH_PATH="${RES}/definitions:${RES}/extruders"

# Sanity-check: each part STL must already exist (render_print.sh produces them).
for n in "${PART_NAMES[@]}"; do
    if [[ ! -f "${HERE}/${n}.stl" ]]; then
        echo "ERROR: ${HERE}/${n}.stl missing. Run render_print.sh first." >&2
        exit 1
    fi
done

# ---------------------------------------------------------------------------
# Hand-substituted Marlin start blocks. The bare CuraEngine binary does NOT
# resolve {placeholder} tokens (Cura's frontend does that); we override
# `machine_start_gcode` / `machine_end_gcode` with fully resolved blocks.
# ---------------------------------------------------------------------------
MK3S_START=$'G21 ; mm\nG90 ; absolute pos\nM82 ; absolute extrusion\nM104 S215 ; set hotend\nM140 S60 ; set bed\nM190 S60 ; wait bed\nM109 S215 ; wait hotend\nG28 W ; home no mesh\nG80 ; mesh bed leveling\nG92 E0.0\nG1 Y-3.0 F1000.0 ; outside print area\nG1 X60.0 E9.0 F1000.0 ; intro line\nG1 X100.0 E21.5 F1000.0 ; intro line\nG92 E0.0\n'
MK3S_END=$'M104 S0\nM140 S0\nM107\nG1 X0 Y210\nM84\n'

ENDER3_START=$'G21 ; mm\nG90 ; absolute pos\nM82 ; absolute extrusion\nM140 S60\nM104 S205\nM190 S60\nM109 S205\n; Ender-3 custom start\nG92 E0\nG28 ; home all axes\nG1 Z2.0 F3000\nG1 X0.1 Y20 Z0.3 F5000.0\nG1 X0.1 Y200.0 Z0.3 F1500.0 E15 ; first prime line\nG1 X0.4 Y200.0 Z0.3 F5000.0\nG1 X0.4 Y20 Z0.3 F1500.0 E30 ; second prime line\nG92 E0\nG1 Z2.0 F3000\nG1 X5 Y20 Z0.3 F5000.0\n'
ENDER3_END=$'M140 S0\nM104 S0\nM107\nG91\nG1 E-2 F2700\nG1 E-2 Z0.2 F2400\nG1 X5 Y5 F3000\nG1 Z10\nG90\nG1 X0 Y220\nM84 X Y E\n'

common_settings=(
    -s layer_height=0.2
    -s layer_height_0=0.2
    -s wall_line_count=3
    -s top_layers=5
    -s bottom_layers=4
    -s infill_sparse_density=40
    -s infill_pattern=gyroid
    -s adhesion_type=brim
    -s brim_width=4
    -s support_enable=True
    -s support_angle=50
    -s material_diameter=1.75
    -s machine_nozzle_size=0.4
    -s machine_gcode_flavor=Marlin
)

slice_one () {
    local stl="$1" def="$2" out="$3" temp="$4" first_temp="$5" start="$6" end="$7"
    echo "  -> ${out##*/}"
    "${CURA}" slice -p -v \
        -j "${RES}/definitions/${def}" \
        "${common_settings[@]}" \
        -s material_print_temperature="${temp}" \
        -s material_print_temperature_layer_0="${first_temp}" \
        -s material_bed_temperature=60 \
        -s material_bed_temperature_layer_0=60 \
        -s machine_start_gcode="${start}" \
        -s machine_end_gcode="${end}" \
        -e0 -s extruder_nr=0 \
        -l "${stl}" \
        -o "${out}" 2>&1 \
        | grep -iE '^(Print time|Filament \()' | sed 's/^/      /'
}

for n in "${PART_NAMES[@]}"; do
    stl="${HERE}/${n}.stl"
    echo "==> [${n}] CuraEngine -> MK3S+ + Ender-3"
    slice_one "${stl}" "prusa_i3_mk3.def.json" \
        "${SLICES_DIR}/${n}.MK3S.cura.gcode" 215 215 \
        "${MK3S_START}" "${MK3S_END}"
    slice_one "${stl}" "creality_ender3.def.json" \
        "${SLICES_DIR}/${n}.Ender3.cura.gcode" 200 205 \
        "${ENDER3_START}" "${ENDER3_END}"
done

# Sanity check: no unresolved {placeholder} braces left in the start blocks.
# If the bundled definition adds new templated tokens in a future Cura
# release, this guard fails the script before we ship a brick to a printer.
for gcode in "${SLICES_DIR}"/auger-{shaft,housing}.{MK3S,Ender3}.cura.gcode; do
    if [[ -f "${gcode}" ]] && head -200 "${gcode}" | grep -nE '\{[a-z_]+\}'; then
        echo "ERROR: unresolved {} placeholder(s) in ${gcode##*/} start block." >&2
        exit 1
    fi
done

echo
echo "==> Done."
echo "    Shaft:    ${SLICES_DIR}/auger-shaft.{MK3S,Ender3}.cura.gcode"
echo "    Housing:  ${SLICES_DIR}/auger-housing.{MK3S,Ender3}.cura.gcode"
