# Parametric CAD pipeline

This directory holds the **scripted, open-source parametric CAD model** for
the powder-excavator design discussed in `docs/manuscript/main.tex` and
`README.md`. It is the start of a feedback-loop-friendly hardware design
pipeline:

```
ExcavatorParams (single source of truth, mm)
        │
        ├──► excavator.py  ──► CadQuery solids (trough, arms, pin, …)
        │                          │
        │                          ├──► build.py  ──► STEP + STL + manifest.json
        │                          │
        │                          └──► (open in CQ-editor / FreeCAD / KiCAD-AS-PCB / …)
        │
        └──► dfm.py  ──► automated checks
                            • FDM printability (min wall, overhang)
                            • gantry-only kinematics (no second axis on the bucket)
                            • cam-ramp and pin-slot reachability
```

## Why CadQuery (instead of Rhino/Grasshopper, Fusion, nTop, …)?

Per PR #2 the user asked for **something open that you can install and run**.
Rhino + Grasshopper, Fusion 360 (and its Generative Design module), nTop, and
Onshape FeatureScript are all powerful but commercial — they don't survive
the "freshly-cloned repo on a CI runner" test.

[CadQuery](https://github.com/CadQuery/cadquery) is a pip-installable, pure-
Python parametric kernel built on top of OCCT (the same kernel FreeCAD uses).
That makes it a natural fit for this repo:

* `pip install cadquery` is the only setup step.
* The model is plain Python source code, so a "design iteration" is a
  `git diff` plus a `python -m cad.build` re-run.
* Outputs are STEP and STL — every open-source slicer (PrusaSlicer,
  OrcaSlicer, Cura) and every CAD viewer (FreeCAD, OCC's CAD Assistant,
  KiCAD's 3D viewer) can read them.

Sister tools that fit the same niche and are worth considering as the design
matures are [`build123d`](https://github.com/gumyr/build123d) (a re-imagined
CadQuery API by the same community) and
[OpenSCAD](https://openscad.org/) (a constructive solid geometry DSL).
The Edison Scientific generative-CAD literature task (initial submission
`task_id` `524e7e92-a326-440a-b6fd-f6eb220d9019` was sent to the wrong
endpoint and cancelled; resubmitted as
`f5a27ed3-8530-4102-9e31-5af9bbe9b0e0` against the correct
`api.platform.edisonscientific.com` endpoint, see
[`docs/edison/README.md`](../docs/edison/README.md)) is intended to widen
this comparison.

## Files

| File | What it is |
|---|---|
| [`excavator.py`](excavator.py) | Parametric model. `ExcavatorParams` dataclass + `build_*` functions for the trough, arms, pivot pin, strike-off bar, smooth cam ramp, and the pin-slot board (Panel E variant). |
| [`build.py`](build.py) | Exporter — writes STEP + STL for every part and a STEP for the assembly into `cad/build/`, plus a `manifest.json` with the parameter snapshot. |
| [`render.py`](render.py) | **Visualisation.** Renders every part and the full assembly to vector SVGs under [`docs/figures/cad/`](../docs/figures/cad/) using CadQuery's built-in hidden-line SVG exporter — no rasterizer or X server required. Useful for "what does the print actually look like?" without having to load STEP/STL into a viewer. |
| [`dfm.py`](dfm.py) | **Feedback mechanism.** Runs FDM-printability and gantry-only kinematics checks against the current parameter set; non-zero exit code on failure (CI-friendly). |
| [`tests/test_excavator.py`](tests/test_excavator.py) | Unit tests: parts build at default parameters, DFM passes at defaults, deliberate regressions (sub-min-wall trough, off-board slot path) are caught. |

## Usage

From the repo root:

```bash
# install (one-time)
pip install cadquery

# generate STEP/STL for every part + assembly + the manifest
python -m cad.build

# render every part + full assembly to docs/figures/cad/*.svg
python -m cad.render

# run the design-for-manufacturing + gantry-kinematics feedback
python -m cad.dfm

# run the unit tests
python -m unittest discover cad/tests -v
```

The default parameter set in `ExcavatorParams` matches the dimensions called
out in `docs/manuscript/main.tex` (trough length L = 80 mm, L ≈ 3 D, etc.).
Iterate by editing `excavator.py` (or constructing a modified
`ExcavatorParams` with `dataclasses.replace(...)` from a notebook) and
re-running `python -m cad.dfm` — that is the feedback loop.

## What `dfm.py` actually checks

Categories of checks (each prints `[OK]` / `[WARN]` / `[FAIL]`):

* **`sanity.*`** — every dimension must be positive.
* **`fdm.*`** — printability for FDM (min wall thickness ≥ `min_wall`,
  cam-ramp underside overhang ≤ `max_overhang_deg`, rim-lip chamfer present,
  pin clearance positive).
* **`kinematics.cam.*`** — rim lip engages the smooth cam ramp; ramp fits
  inside the gantry's X travel; ramp angle is in the 15–45° band.
* **`kinematics.slot.*`** — the **gantry-only constraint** from PR comment
  4166621470 ("we have a gantry system and would like to avoid installing
  a second axis"): every slot waypoint lies inside the board, the slot's X
  span fits inside `gantry_x_travel`, and the slot's Z span fits inside
  `gantry_z_travel`. Reversals in the slot's X direction are flagged as
  warnings (legal — the gantry just reverses — but worth surfacing).

The exit code is `0` if every error-severity check passes (warnings do not
fail the run), so `python -m cad.dfm` is suitable to drop into CI as a
guardrail for future parameter changes.
