# Auger slices (PrusaSlicer CLI)

Two g-code files, one per printer in the project's actual hardware list (PR
#7 §6 — *"FDM toolchain (MK3 / Ender)"*). Both are sliced from the same
manifold STL (`../archimedes-auger.stl`) using the headless PrusaSlicer CLI
recommended in PR #7's revised toolchain.

## Files

| Printer | G-code | Bed shape | Filament | Nozzle | Layer | Time | Material |
|---|---|---|---|---|---|---|---|
| Original Prusa MK3S+ | [`archimedes-auger.MK3S.gcode`](archimedes-auger.MK3S.gcode) | 250 × 210 mm | 1.75 mm PLA, 215 °C | 0.4 mm | 0.2 mm | ≈ 2 h 29 m | 20.91 cm³ (~26 g) |
| Creality Ender-3     | [`archimedes-auger.Ender3.gcode`](archimedes-auger.Ender3.gcode) | 220 × 220 mm | 1.75 mm PLA, 205/200 °C | 0.4 mm | 0.2 mm | ≈ 2 h 21 m | 20.91 cm³ (~26 g) |

Common settings: 3 perimeters · 5 top / 4 bottom solid layers · 40 % gyroid
infill · 4 mm brim · auto-supports at 50° · single skirt loop · print
orientation **exit-hole-down** (Z+ = M3 boss). No slicer warnings on either.

## Why two slices

PR #7 §6 calls out *"PrusaSlicer CLI, headless, in CI"* as the canonical
slicer and names the MK3 *and* the Ender-3 as the project's two FDM rigs.
Slicing for both in one CI run gives:

1. **Hardware portability** — whichever rig is free can print without the
   operator re-slicing.
2. **A free DFM signal** — if support volume, time, or filament use
   diverge between the two runs (they don't here, beyond the bed-shape /
   temperature deltas), the helix overhangs are sensitive to acceleration
   limits and that's worth flagging *before* the print.
3. **Profile-bug isolation** — if a future SCAD edit triggers a slicer
   warning on one printer but not the other, it points at a vendor-profile
   interaction (`gcode_flavor`, `seam_position`, etc.) rather than a real
   geometry defect.

Both extrude 8 692.64 mm of 1.75 mm filament (≈ 20.91 cm³) — i.e. the
underlying toolpath geometry is identical; only printer-specific G-code
preamble / feedrate caps and the small first-layer-temperature delta cause
the ~9-minute time difference.

## Regenerate

```bash
bash cad/auger/render_print.sh   # writes both g-code files into this dir
```
