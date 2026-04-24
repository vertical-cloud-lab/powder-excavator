# Auger slices

Two slicer toolchains, two printer profiles each = four g-code files. The
PrusaSlicer outputs are the canonical CI deliverables (PR #7 §6 toolchain).
The CuraEngine outputs are added for parity with what most desktop Ender-3
/ MK3 users actually run (Ultimaker Cura), per the request in the PR
discussion.

## Files

### PrusaSlicer CLI (canonical)

| Printer | G-code | Bed | Filament | Time | Material |
|---|---|---|---|---|---|
| Original Prusa MK3S+ | [`archimedes-auger.MK3S.gcode`](archimedes-auger.MK3S.gcode) | 250 × 210 mm | 1.75 mm PLA, 215 °C | ≈ 2 h 28 m | 20.91 cm³ (~26 g) |
| Creality Ender-3     | [`archimedes-auger.Ender3.gcode`](archimedes-auger.Ender3.gcode) | 220 × 220 mm | 1.75 mm PLA, 205/200 °C | ≈ 2 h 21 m | 20.91 cm³ (~26 g) |
| Creality Ender-3 (USB short-name copy) | [`AUGER.gcode`](AUGER.gcode) | same as above | same | ≈ 2 h 21 m | 20.91 cm³ (~26 g) |

### CuraEngine (Ultimaker Cura's open-source slice engine)

| Printer | G-code | Bed | Filament | Time | Material |
|---|---|---|---|---|---|
| Original Prusa MK3S+ | [`archimedes-auger.MK3S.cura.gcode`](archimedes-auger.MK3S.cura.gcode)   | 250 × 210 mm | 1.75 mm PLA, 215 °C     | ≈ 2 h 22 m | 18.77 cm³ (~23 g) |
| Creality Ender-3     | [`archimedes-auger.Ender3.cura.gcode`](archimedes-auger.Ender3.cura.gcode) | 235 × 235 mm | 1.75 mm PLA, 205/200 °C | ≈ 2 h 04 m | 18.72 cm³ (~23 g) |

Common settings (both slicers, both printers): 0.4 mm nozzle · 0.2 mm
layers · 3 perimeters/walls · 5 top / 4 bottom solid layers · 40 % gyroid
infill · 4 mm brim · auto-supports at 50° · single skirt loop · print
orientation **exit-hole-down** (Z+ = M3 boss). No slicer warnings on any
of the four runs.

### Why both slicers

The user asked specifically: "are you slicing this with prusa slicer?",
then "yeah, try with cura-engine". The PrusaSlicer slices are kept as the
canonical CI artefact (matches PR #7's toolchain decision and is what
runs in the GitHub-hosted runner without extra setup). The CuraEngine
slices are added so the Cura toolchain (i.e. what the printer
manufacturers ship) is also represented end-to-end.

The two slicers diverge by ~10 % in time and ~10 % in filament for
the same STL + same nominal settings. Cura is a touch faster / a touch
leaner because:

- Cura's default perimeter speeds are higher and more loosely capped
  than PrusaSlicer's (PrusaSlicer enforces stricter inner/outer wall
  speed ratios).
- Cura's gyroid line spacing at "40 %" is computed from a slightly
  different cell formula than PrusaSlicer's, yielding fewer infill
  passes.
- Cura's brim line count at 4 mm width × 0.4 mm line ≈ 10 lines vs
  PrusaSlicer's brim_loops_count derivation; small bed contact delta.

These deltas are normal between slicers and small enough that **either
file is print-ready** — pick the one matching your desktop tooling.

## Printing on the Ender-3 from a USB stick

(This section applies to either Ender-3 g-code file —
`archimedes-auger.Ender3.gcode` or `archimedes-auger.Ender3.cura.gcode`
— both produce the same Marlin g-code dialect.)

1. Format a USB stick as **FAT32** (Marlin on the stock Ender-3 8-bit board
   does not read exFAT/NTFS).
2. Copy **`AUGER.gcode`** (the short-named PrusaSlicer copy — the stock
   LCD12864 truncates long filenames and some firmware revisions refuse
   names over ~20 chars) to the **root** of the stick. Do not put it in a
   subfolder. If you'd rather use the Cura output, rename
   `archimedes-auger.Ender3.cura.gcode` to something like `AUGER.gcode`
   on the stick.
3. Insert the stick, **Print from media → AUGER.gcode**, confirm.
4. Pre-flight: bed levelled, nozzle clean, **PLA at 200/205 °C, bed 60 °C**
   (the file sets these — don't override on the LCD before start). The
   PrusaSlicer file's start-block is `G28` → `G1 Z5 F5000`; the Cura
   Ender-3 file uses Cura's stock Ender-3 prime-line block (`G28` → two
   priming lines along X=0.1 / X=0.4) — both correct for the printer.

If your Ender has the newer Creality 32-bit board / TFT (Ender-3 V2 / S1 /
Pro with the silent board), the long-named files work fine — the
short-named copy is just defensive for stock 8-bit boards.

## Why two printers per slicer

PR #7 §6 calls out *"PrusaSlicer CLI, headless, in CI"* as the canonical
slicer and names the MK3 *and* the Ender-3 as the project's two FDM rigs.
Slicing both rigs in one CI run gives:

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

## Regenerate

```bash
bash cad/auger/render_print.sh   # writes all four g-code files into this dir
                                 # (PrusaSlicer always; CuraEngine if available)
bash cad/auger/slice_cura.sh     # CuraEngine only — needs `snap install cura-slicer`
```
