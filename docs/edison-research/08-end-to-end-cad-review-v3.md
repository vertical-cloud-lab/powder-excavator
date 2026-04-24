# End-to-End Review of Gantry-Only Powder Excavator CAD

- **Trajectory ID:** `ac68bc56-557c-4009-a03d-dc4cb9774691`
- **Crow / job:** `job-futurehouse-data-analysis-crow-high` (analysis (Crow, high))
- **Source:** Edison Scientific (`api.platform.edisonscientific.com`)

## Prompt

```
You are reviewing the **current state** of the powder-excavator project,
an open-hardware bulk powder dispenser intended to feed a downstream
precision gravimetric dispenser inside a self-driving lab.

**Hard constraint:** the entire dispensing motion must be achievable on a
3-axis gantry (X, Y, Z) -- *no* second actuator on the bucket itself. All
trough rotation / scoop opening / closing must come from passive mechanical
interaction with fixed external features (cam ramps, routed slots, fixed
posts, compliant flexures, etc.) driven by gantry motion alone.

The full design state has been uploaded to the job bucket and includes:

- ``README.md``, ``powder-excavator-sketch.jpg``, ``PXL_*.jpg``: design
  intent and the original hand sketch.
- ``cad/excavator.py`` + ``cad/build.py`` + ``cad/dfm.py`` + ``cad/render.py``:
  the CadQuery parametric source, exporter, DFM/feedback checks, and figure
  renderer.
- ``cad/tests/*.py``: the unit + regression tests for the CAD model.
- ``cad/build/*.step``, ``cad/build/*.stl``, ``cad/build/manifest.json``:
  STEP + STL exports of every part and the assembly, plus the parameter
  snapshot used to build them.
- ``docs/figures/*.svg`` + ``*.png`` + ``mechanism.gif``: schematic panels
  A-E of the mechanism.
- ``docs/figures/cad/*.svg`` + ``*.png``: hidden-line renders of the
  parametric model (per-part + assembly + 3 assembly views).
- ``docs/manuscript/main.tex`` + ``references.bib``: the manuscript draft.
- ``docs/edison/*.md``: every prior Edison analysis (analysis-v1 through
  analysis-v3) and the literature-review responses.
- ``docs/brainstorming-and-literature.md``: ideation + lit notes.
- ``scripts/edison_submit.py``: the script being used to submit this query.

Please review the current state end-to-end and provide:

1. A geometry / kinematics / statics critique of the parametric CAD as it
   currently stands (do the dimensions in ``ExcavatorParams``, the pivot
   placement, the cam-ramp rise vs. lever arc, the slot-board path, and
   the strike-off bar geometry actually compose into a working
   gantry-only powder-excavation cycle?). Cross-reference the rendered
   PNGs/SVGs against the schematic panels and call out any place the CAD
   and the schematic disagree.
2. Specific, parameter-level edits to ``ExcavatorParams`` you would make
   next, with justification (cite the figures or STEP/STL files when
   relevant).
3. A ranked list of the 3 highest-impact remaining risks to a successful
   first physical prototype, given the gantry-only constraint, and the
   cheapest experiment to retire each one.
4. A check on whether the DFM rules in ``cad/dfm.py`` cover the failure
   modes you would actually expect on a printed PETG / nylon / ESD-safe
   build -- what's missing? what's over-conservative?
5. Concrete next-iteration recommendations for: (a) the manuscript text,
   (b) the schematic figures (panels A-E + mechanism.gif), (c) the
   parametric model, and (d) the test suite.

Reply in the structure above with section headings 1-5.


--- Embedded repository bundle (inline fallback because the Edison chunked-upload endpoint is unavailable on this cluster) ---

=== file: README.md ===
````md
# powder-excavator

A pure-mechanical, gantry-mounted "ladle / trough" for picking up loose
powder from a bed and depositing it at a target location. The trough is
suspended between two vertical arms that grip its **two short end caps**;
a single **longitudinal pivot pin** runs through both end caps along the
trough's long axis L. There are no actuators on the bucket itself — the
gantry's existing X / Z motion plus a fixed wall-/post-mounted **smooth
inclined cam ramp** does all the work.

> **Geometry note (post-review).** An earlier revision of this design used
> a **transverse** pivot pin (running across the trough's width D) and
> tipped the trough **end-over-end** against a **sawtooth** ledge. Both
> choices were retired after a high-effort review by Edison Scientific
> identified (i) a kinematic impossibility — a fixed sawtooth tooth
> cannot engage a fixed-radius hook on a horizontally-translating pivot
> without the lip plunging through the tooth — and (ii) a severe trapped-
> volume / arching problem when cohesive powders are forced to bottleneck
> through the narrow ~13 mm spill point of an end-over-end half-cylinder.
> The current design uses a **longitudinal** pivot pin and **sideways
> tilt** so powder pours over the full 80 mm long edge, and replaces the
> sawtooth with a **smooth cam ramp** that the trough's chamfered bumper
> slides up. A follow-on hand sketch
> ([`PXL_20260423_231729467.jpg`](PXL_20260423_231729467.jpg)) refines the
> cam ramp into a **pin-defined-path** (peg-in-routed-slot) variant in
> which a peg on a stem hanging from the gantry is captured in a slot
> routed into a fixed external board, so the slot path deterministically
> programs the trough's tilt schedule. The full review and the verbatim
> Edison answers live in [`docs/edison/`](docs/edison/); the
> literature-aware brainstorming doc has been ported to a LaTeX manuscript
> with a proper BibTeX bibliography (see
> [`docs/manuscript/main.tex`](docs/manuscript/main.tex) and
> [`docs/manuscript/refs.bib`](docs/manuscript/refs.bib); build with
> `cd docs/manuscript && make`).

## Original concept sketch

![Design sketch](powder-excavator-sketch.jpg)

## Cleaned-up design diagram

The sketch above has been recreated as four labelled subpanels. Each is a
self-contained SVG with its own caption. All four are produced (along with
the mechanism animation below) by a single reproducible script,
[`scripts/generate_figures.py`](scripts/generate_figures.py).

### Panel A — Orthographic views (end / side / top)

![Panel A — orthographic](docs/figures/panel-A-orthographic.svg)

### Panel B — End-cap pivot detail

![Panel B — pivot detail](docs/figures/panel-B-pivot-detail.svg)

### Panel C — 3D / isometric view of trough on gantry

![Panel C — isometric](docs/figures/panel-C-isometric.svg)

### Panel D — Mechanism of action (4 steps)

![Panel D — mechanism of action](docs/figures/panel-D-mechanism.svg)

### Panel E — Pin-defined-path actuation variant

A follow-on hand sketch
([`PXL_20260423_231729467.jpg`](PXL_20260423_231729467.jpg)) refines the
smooth cam ramp into a peg-in-routed-slot mechanism. A vertical stem hangs
from the gantry carriage on a pin pivot; a transverse peg at the top of the
stem rides in a slot routed into a fixed external board. The slot's shape
over `X` deterministically programs the trough's tilt schedule, with the peg
captive in the slot for the entire stroke (no approach-and-contact
ambiguity, and bidirectional return without relying on gravity). See
[`docs/manuscript/main.tex`](docs/manuscript/main.tex) §"Pin-defined-path
actuation" for the full trade-off discussion.

![Panel E — pin-defined-path actuation](docs/figures/panel-E-pin-slot.svg)

### Animation — cam-engagement and sideways tilt

![Mechanism animation — trough rolls sideways about its longitudinal pin as its bumper rides up the cam ramp](docs/figures/mechanism.gif)

The full literature-aware design discussion — framed roughly as the
introduction to a *Digital Discovery* manuscript on a new powder
dispenser, with references to recent SDL / powder-handling literature —
is now a LaTeX manuscript with a proper BibTeX bibliography:
[`docs/manuscript/main.tex`](docs/manuscript/main.tex),
[`docs/manuscript/refs.bib`](docs/manuscript/refs.bib). Build with
`cd docs/manuscript && make` (requires `pdflatex`, `bibtex`, and
`cairosvg`).

## Parametric CAD pipeline ([`cad/`](cad/))

The same dimensions used in the figures and the manuscript also drive an
**open, scriptable parametric CAD model** built on
[CadQuery](https://github.com/CadQuery/cadquery), so the design can be
iterated as plain Python source and exported to STEP / STL for any
open-source slicer. A small `cad/dfm.py` runs design-for-manufacturing and
**gantry-only kinematics** checks (the explicit constraint from PR comment
4166621470 — "we have a gantry system and would like to avoid installing a
second axis"), so a parameter regression is caught the next time anyone
edits `ExcavatorParams`. See [`cad/README.md`](cad/README.md) for the
rationale (why CadQuery over Rhino / Grasshopper / Fusion / nTop) and the
full feedback-loop description.

```bash
pip install cadquery
python -m cad.build      # writes STEP + STL + manifest into cad/build/
python -m cad.dfm        # design-for-manufacturing + gantry-only kinematics checks
python -m unittest discover cad/tests -v
```


## Design brainstorming

### Core idea

The bucket is an **elongated half-cylinder trough** (think: a long,
narrow ladle with a semicircular cross-section and an open top). It is
suspended between **two parallel vertical arms** that hang from the
gantry carriage and grip the trough on its **two short end caps**. A
**single horizontal pivot pin** runs from one arm, through a printed
boss in the first end cap, lengthwise along L through the trough, out
through a matching boss in the second end cap, and into the second arm
(panels B and C). The pivot axis is therefore **parallel to the
trough's long axis L** — the trough rolls about that axis like a
spit-roast rotating about its skewer.

- The two arms are rigidly bolted to the carriage and **always stay
  vertical** during operation.
- The trough is the **only** part that ever rotates, and only about the
  longitudinal pin — rolling **sideways** when its rim-mounted bumper
  catches the cam ramp. Powder pours over the **full 80 mm long edge**,
  not through a narrow end-cap point.
- The pin sits a few millimetres above the loaded trough's centre of
  mass, so gravity returns the trough to "open-up" once the dump cam is
  cleared (a stable pendulum / gondola-style pivot).

Picking shape matters:

- A **half-cylinder** maximises retained volume per unit "scoop depth"
  while presenting a long flat top edge that pours uniformly along its
  whole length.
- An **elongated** trough (length L ≈ 3 × diameter D) gives the spill
  edge a large area (≈ L × few-mm depth) so cohesive powders cannot
  arch across it, eliminating the bottleneck/bridging failure mode of
  an end-over-end tilt of the same trough (Edison v2 §3).
- **No moving lid / hinge in the baseline design** — powder is held in
  by gravity alone, which keeps the part count and the failure modes to
  a minimum.

### Mechanism of action (4 steps — see Panel D)

1. **J-curve plunge into the bed.** The gantry lowers the carriage
   (Z↓) so the trough enters the powder bed, then translates a few
   millimetres in X while continuing down — a shallow J-curve rather
   than a pure Z-plunge. A blunt flat half-cylinder driven straight
   down compresses the bed underneath it instead of flowing in (Edison
   v1 §2); the J-curve lets powder spill into the open top as the
   bucket sweeps forward.
2. **Lift past the strike-off bar.** The carriage rises (Z↑) along an
   X-coordinate that takes the rim of the trough **under a fixed bed-
   edge strike-off bar**. The bar wipes the heaped powder back into the
   bed and leaves a defined fill volume. Without this step, dose CV
   sits in the 15–30 % range across powder classes (Edison v2 §4); with
   it, ≈10 % CV is realistic on cohesive inorganics — comparable to the
   positive-displacement-pipette baseline reported by Alsenz (see
   [`docs/manuscript/main.tex`](docs/manuscript/main.tex)).
3. **Transport to the deposit X.** The carriage translates in X over to
   the deposit station. Arms still vertical; trough still open-up,
   level under gravity.
4. **Sideways tilt against the cam → deposit.** The gantry pushes the
   trough in X into a fixed, wall-/post-mounted **smooth inclined cam
   ramp** at end-cap-rim height. The chamfered bumper on the trough's
   long-side rim **slides up the cam's hypotenuse**; because the cam
   surface is a continuous incline rather than a fixed point, pure-X
   gantry travel is geometrically compatible with the resulting roll of
   the trough about its longitudinal pin (Edison v2 §1). Continued
   X-push rolls the trough sideways and powder pours over the **full
   long edge**. Backing the carriage off lets gravity right the trough
   under its pendulum action.

The "push against a cam to dump" trick is what makes this fully
mechanical — no servo / solenoid is needed on the bucket itself.

### What is the cam ramp?

A **fixed, wall- or post-mounted inclined block** at roughly trough-
end-cap-rim height (see Panel D, Step 4, and the GIF above). Its top
surface is a **smooth ramp** (a chamfered, ideally polished
hypotenuse), *not* a comb of teeth. It is *not* on the floor of the
powder bed and is *not* part of the moving assembly. The trough's rim
bumper rides up the ramp as the gantry pushes the carriage in X; the
height the bumper reaches up the ramp (set by how far in X the gantry
pushes) determines the tilt angle and therefore how much powder is
poured.

Why a smooth ramp and not a sawtooth?

- **Kinematic compatibility.** A fixed sawtooth tooth cannot engage a
  fixed-radius hook on a horizontally-translating pivot pin without the
  lip having to plunge through the tooth — the pin-to-tooth distance
  must change as the pivot moves in X, but the hook's radius is fixed.
  An inclined cam removes the constraint entirely: the contact point
  slides continuously along the cam surface as the gantry travels
  (Edison v2 §1).
- **Continuous tilt control.** With a smooth ramp, the tilt angle is a
  continuous function of gantry X position, so pour rate and final
  dose can be modulated in software without changing hardware.
- **No catch-and-skip failure mode.** A printed sawtooth tooth and a
  printed hook can mis-engage, snag, or skip; a chamfered bumper on a
  smooth incline cannot.

### Optional: knock-to-de-bridge

Because the bumper is in continuous frictional contact with the cam
during the tilt, the gantry can be driven to **rapidly oscillate ±2 mm
in X** while the bumper is engaged. This momentarily slams the trough
against the cam and acts as a free pneumatic-knocker analogue to break
up bridges of cohesive powder that would otherwise refuse to pour
(Edison v1 §6). It is a software-only feature — the same hardware that
performs the tilt also performs the knock.

### Open questions / things to prototype

- **Manufacturing.** Target is a **3D-printable** trough + arms + end-
  cap pivot bosses (PETG / nylon for the prototype, with a glued-in
  brass sleeve for the pin holes if wear becomes an issue). The pivot
  pin itself is a stock dowel pin or shoulder bolt, ideally **metal**
  so it can also serve as the ground path for an optional conductive
  trough lining (e.g. interior copper tape) that mitigates triboelectric
  charging on fine dry inorganics (Edison v1 §2). The cam ramp can be
  printed too. A machined-aluminium revision would only be needed if
  the printed parts wear or charge problematically.
- **Target powders are dozens-of-microns in diameter** — catalysts,
  ceramics, salts. Many are cohesive, hygroscopic, and/or
  triboelectrically charged; some clump and resist removal from a
  scoop. This drives several of the open questions below.
- **Trough geometry sweep.** Pure semicircle vs. a slightly deeper "U"
  vs. a V-bottom — which retains powder best while still pouring
  cleanly when rolled? A 3D-printed bake-off across our worst-case
  cohesive powders is cheap.
- **Cam-ramp angle sweep.** Cam slope, length, and surface finish are
  the three knobs most likely to dominate dose CV. Steeper slopes give
  more aggressive tilts per unit gantry travel but risk bumper slip;
  shallower slopes give finer control but a longer dump stroke.
- **Strike-off bar profile.** Square cross-section vs. a chamfered or
  rounded leading edge — which leaves the cleanest fill at the rim
  without flicking powder away? Worth varying.
- **Bumper profile.** Chamfer angle and surface finish on the rim
  bumper directly affect cam engagement; too sharp and it digs in,
  too rounded and it slips. Print + sand a small set and characterise.
- **Bed depletion.** Repeated scoops from the same X, Y in a static
  bed will form a crater and the dose will decay (Edison v1 §3). The
  gantry must raster the plunge X, Y across the bed, or a separate
  "bed-stir" cycle must be added.
- **Cleaning / cross-contamination.** For multi-material campaigns the
  pivot pin is the natural quick-release point — pull the pin, swap the
  trough, re-insert. For very sticky powders a **per-material
  consumable trough** (snap-in printed liner) may be cheaper than
  cleaning.
- **Use-environment caveat.** A bulk-transfer scoop unavoidably
  exposes the powder to ambient air during transport and leaves an
  open crater in the stock bed. For hygroscopic salts this is a real
  limitation; the device's intended envelope is **bulk transfer in
  ambient or globally-controlled environments (e.g. inside a glovebox
  or on a benchtop with a desiccated stock container)**, not as a
  direct loader for highly moisture-sensitive workflows.

### Possible variations (all still pure-mechanical)

- **Reversible tilt** — cam ramps on both sides of the work area let
  the same bucket dump left or right by which way it's pushed.
- **Two troughs back-to-back** — one fills while the other is being
  dumped, doubling throughput with no extra actuators.
- **Auger / screw inside the trough** — adds one rotary actuator but
  gives controlled metered dosing instead of "tilt and pour all".
- **Passive flap lid for fine powders.** A lightweight flap hinged on
  the trough's long upper edge that gravity holds *closed* over the
  mouth while the trough hangs open-up (so fluffy powder is not shed
  during X-travel). When the trough rolls against the cam ramp in
  step 4, a small projection on the flap strikes a separate fixed tang
  on the same cam assembly, swinging the flap clear so powder can
  pour out. Returns to closed under gravity once the trough returns
  upright. Still purely mechanical — no actuator on the bucket.

### Acknowledgements

The design changes between PR #2 and the present revision were prompted
by a high-effort design review from [Edison Scientific](https://edisonscientific.com/),
plus a literature search via the same service. Verbatim responses are
archived under [`docs/edison/`](docs/edison/) for traceability.

````

=== file: cad/__init__.py ===
```py
"""Mark ``cad/`` as a Python package so ``python -m cad.build`` works."""

```

=== file: cad/build.py ===
```py
"""Export every part and the full assembly to STEP and STL.

Run from the repo root::

    python -m cad.build

Outputs land under ``cad/build/`` (gitignored). Each part is exported
twice -- once as STEP (parametric, lossless, CAD-tool-friendly) and once as
STL (mesh, slicer-friendly).

A small JSON manifest lists every exported file plus the parameter values
used; the next step in the feedback loop (``cad/dfm.py``) reads it back to
report what was built.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import cadquery as cq

from .excavator import (
    ExcavatorParams,
    build_arm,
    build_assembly,
    build_cam_ramp,
    build_pin,
    build_slot_board,
    build_strike_off_bar,
    build_trough,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = REPO_ROOT / "cad" / "build"


def _export(part: cq.Workplane, stem: str) -> list[Path]:
    """Export a single part as STEP and STL, return both paths."""
    step_path = BUILD_DIR / f"{stem}.step"
    stl_path = BUILD_DIR / f"{stem}.stl"
    cq.exporters.export(part, str(step_path), exportType="STEP")
    cq.exporters.export(part, str(stl_path), exportType="STL")
    return [step_path, stl_path]


def main() -> None:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    p = ExcavatorParams()

    parts = {
        "trough":         build_trough(p),
        "arm":            build_arm(p),
        "pin":            build_pin(p),
        "strike_off_bar": build_strike_off_bar(p),
        "cam_ramp":       build_cam_ramp(p),
        "slot_board":     build_slot_board(p),
    }

    written: list[str] = []
    for name, part in parts.items():
        for path in _export(part, name):
            written.append(str(path.relative_to(REPO_ROOT)))
            print(f"wrote {path.relative_to(REPO_ROOT)}")

    # Full assembly: STEP only (STL of an Assembly needs flattening that
    # CadQuery's STL exporter doesn't natively support).
    asm = build_assembly(p)
    asm_path = BUILD_DIR / "assembly.step"
    asm.save(str(asm_path), "STEP")
    written.append(str(asm_path.relative_to(REPO_ROOT)))
    print(f"wrote {asm_path.relative_to(REPO_ROOT)}")

    # Manifest: parameter snapshot + list of files that were written.
    # ``slot_path`` is a tuple-of-tuples; jsonify it to nested lists.
    params_dict = asdict(p)
    params_dict["slot_path"] = [list(pt) for pt in p.slot_path]
    manifest = {
        "params": params_dict,
        "files":  written,
    }
    manifest_path = BUILD_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True))
    print(f"wrote {manifest_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()

```

=== file: cad/dfm.py ===
```py
"""Design-for-manufacturing and gantry-kinematics feedback for the CAD model.

This is the closed-loop feedback half of the open CAD pipeline. It reads the
parametric model in :mod:`cad.excavator`, runs a battery of automated checks,
and prints a summary plus a non-zero exit code if any check fails. Each
check is intentionally conservative; the goal is to catch obvious mistakes
the next time a parameter is changed, not to replace a slicer or a real
simulator.

Run from the repo root::

    python -m cad.dfm

Categories of checks:

* **FDM printability** -- min wall thickness, FDM overhang angles
  (cam-ramp slope, rim-lip chamfer), dowel-pin clearance.

* **Gantry-only kinematics** (per the user's hard constraint that the rig
  has only the existing gantry X / Y / Z axes; no second axis on the
  bucket). The dispense cycle has to be achievable with pure carriage
  motion. The two actuator variants are checked separately:

  - **Smooth cam ramp:** (a) the rim lip must be tall enough to engage the
    ramp before the trough body would clash with the ramp's
    base; (b) the cam ramp's angle has to be shallow enough to avoid
    lift-off, but not so shallow that it doesn't fit in the gantry's X
    travel.

  - **Pin-defined slot:** (a) every slot waypoint must lie inside the
    board; (b) the slot path must always be reachable -- i.e. the gantry
    X travel covers the slot's X range; (c) consecutive waypoints must
    not double back in X (which would require negative gantry-X motion
    relative to the schedule -- still legal, but flagged so the user is
    aware that it requires bidirectional gantry motion).

* **Sanity checks** -- positive dimensions, no zero-width arms, etc.

Exit code is 0 if every check passes, 1 if any check fails (i.e. suitable
for use in CI). Warnings do not fail the run.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass

from .excavator import ExcavatorParams


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str
    severity: str = "error"   # "error" or "warning"

    def render(self) -> str:
        marker = {
            ("error", True):    "[OK]   ",
            ("error", False):   "[FAIL] ",
            ("warning", True):  "[OK]   ",
            ("warning", False): "[WARN] ",
        }[(self.severity, self.ok)]
        return f"{marker}{self.name}: {self.detail}"


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------


def _check(name: str, ok: bool, detail: str, severity: str = "error") -> CheckResult:
    return CheckResult(name=name, ok=ok, detail=detail, severity=severity)


def check_sanity(p: ExcavatorParams) -> list[CheckResult]:
    rs: list[CheckResult] = []
    for f in (
        "trough_length", "trough_radius", "trough_wall", "end_cap_thickness",
        "pin_diameter", "arm_thickness", "arm_width", "arm_length",
        "cam_ramp_length", "cam_ramp_rise", "slot_board_length",
        "slot_board_height", "slot_board_thickness",
    ):
        v = getattr(p, f)
        rs.append(_check(
            f"sanity.positive.{f}", v > 0,
            f"{f} = {v} (must be > 0)",
        ))
    return rs


def check_printability(p: ExcavatorParams) -> list[CheckResult]:
    rs: list[CheckResult] = []
    rs.append(_check(
        "fdm.min_wall.trough",
        p.trough_wall >= p.min_wall,
        f"trough_wall = {p.trough_wall:.2f} mm "
        f"(>= min_wall = {p.min_wall:.2f} mm required for FDM)",
    ))
    # Cam-ramp face is at angle atan(rise / length) from horizontal; the
    # printable overhang angle is measured from VERTICAL, so the worst
    # overhang on the ramp's underside is (90 deg - ramp angle). We want
    # the worst overhang to stay <= max_overhang_deg.
    ramp_angle_deg = math.degrees(math.atan2(p.cam_ramp_rise, p.cam_ramp_length))
    underside_overhang = 90.0 - ramp_angle_deg
    rs.append(_check(
        "fdm.overhang.cam_ramp_underside",
        underside_overhang <= p.max_overhang_deg,
        f"cam-ramp underside overhang = {underside_overhang:.1f} deg "
        f"(<= max_overhang_deg = {p.max_overhang_deg:.1f} deg)",
        severity="warning",  # overhangs can be supported, just slower
    ))
    rs.append(_check(
        "fdm.overhang.bumper_chamfer",
        p.bumper_chamfer > 0,
        f"bumper_chamfer = {p.bumper_chamfer:.2f} mm "
        "(must be > 0 to avoid a sharp 90 deg overhang on the rim lip)",
    ))
    rs.append(_check(
        "fdm.pin_clearance.positive",
        p.pin_clearance > 0,
        f"pin_clearance = {p.pin_clearance:.2f} mm "
        "(must be > 0 for the printed pivot hole to slide on the dowel)",
    ))
    return rs


def check_gantry_only_cam_ramp(p: ExcavatorParams) -> list[CheckResult]:
    rs: list[CheckResult] = []
    # The chamfered rim lip must be at least as tall as the ramp's first
    # ~1 mm, otherwise the trough body will hit the ramp's base before the
    # lip engages.
    rs.append(_check(
        "kinematics.cam.bumper_engages_ramp",
        p.bumper_height >= 2.0,
        f"bumper_height = {p.bumper_height:.2f} mm "
        "(rim lip must be >= 2 mm tall to reliably engage the ramp's leading edge)",
    ))
    # Whole cam stroke must fit inside the gantry's X travel.
    rs.append(_check(
        "kinematics.cam.fits_in_x_travel",
        p.cam_ramp_length <= p.gantry_x_travel,
        f"cam_ramp_length = {p.cam_ramp_length} mm "
        f"(<= gantry_x_travel = {p.gantry_x_travel} mm)",
    ))
    # Ramp angle: too steep (> 45 deg from horizontal) and the trough will
    # tend to skip over the bumper on the return stroke; too shallow and the
    # tilt resolution per mm of gantry X is poor.
    ramp_angle_deg = math.degrees(math.atan2(p.cam_ramp_rise, p.cam_ramp_length))
    rs.append(_check(
        "kinematics.cam.angle_in_band",
        15.0 <= ramp_angle_deg <= 45.0,
        f"ramp angle = {ramp_angle_deg:.1f} deg "
        "(15 deg <= angle <= 45 deg for clean engagement and useful resolution)",
        severity="warning",
    ))
    return rs


def check_gantry_only_slot_board(p: ExcavatorParams) -> list[CheckResult]:
    rs: list[CheckResult] = []
    if len(p.slot_path) < 2:
        rs.append(_check(
            "kinematics.slot.has_path",
            False,
            f"slot_path has {len(p.slot_path)} waypoints (need >= 2)",
        ))
        return rs

    # Every waypoint must lie strictly inside the board, with at least
    # slot_width/2 margin to the edges (so the routed slot doesn't break out).
    margin = p.slot_width / 2 + 1.0
    out_of_board: list[tuple[float, float]] = []
    for x, z in p.slot_path:
        if not (margin <= x <= p.slot_board_length - margin and
                margin <= z <= p.slot_board_height - margin):
            out_of_board.append((x, z))
    rs.append(_check(
        "kinematics.slot.waypoints_inside_board",
        not out_of_board,
        ("all waypoints inside the board with margin "
         f"{margin:.1f} mm" if not out_of_board
         else f"out-of-board waypoints: {out_of_board}"),
    ))

    # The slot's X span must fit in the gantry's X travel, since gantry X
    # is what walks the peg through the slot.
    xs = [pt[0] for pt in p.slot_path]
    x_span = max(xs) - min(xs)
    rs.append(_check(
        "kinematics.slot.x_span_in_gantry_travel",
        x_span <= p.gantry_x_travel,
        f"slot X span = {x_span:.1f} mm (<= gantry_x_travel = {p.gantry_x_travel} mm)",
    ))

    # Hard constraint per user comment 4166621470: "we have a gantry system
    # and would like to avoid installing a second axis." The pin-slot
    # actuation mechanism honours this iff the slot is monotonic in X over
    # each stage of the dispense (i.e. the gantry can walk the peg through
    # the slot by pure +X / pure -X motion). We don't require strict
    # monotonicity over the whole path -- multi-stage paths with a reversal
    # are fine -- but we flag any non-monotonic *segment*, since that would
    # require the peg to physically move sideways inside the slot, which is
    # impossible without a second axis on the bucket.
    non_monotonic: list[int] = []
    last_dx_sign = 0
    for i, ((x0, _), (x1, _)) in enumerate(zip(p.slot_path, p.slot_path[1:])):
        dx = x1 - x0
        sign = 0 if dx == 0 else (1 if dx > 0 else -1)
        if sign != 0 and last_dx_sign != 0 and sign != last_dx_sign:
            # Sign reversal between adjacent segments -- record the index of
            # the second of the two segments. This is a *legal* design
            # (the gantry just reverses), so we report it as a warning, not
            # an error.
            non_monotonic.append(i)
        if sign != 0:
            last_dx_sign = sign
    rs.append(_check(
        "kinematics.slot.gantry_x_only",
        not non_monotonic,
        ("slot path requires only gantry-X motion to traverse"
         + (f" (with {len(non_monotonic)} reversal(s) at segment indices {non_monotonic})"
            if non_monotonic else "")),
        severity="warning" if non_monotonic else "error",
    ))

    # The peg must always be reachable: at every X along the slot, the slot
    # must stay within the gantry's Z travel (roughly).
    zs = [pt[1] for pt in p.slot_path]
    z_span = max(zs) - min(zs)
    rs.append(_check(
        "kinematics.slot.z_span_in_gantry_travel",
        z_span <= p.gantry_z_travel,
        f"slot Z span = {z_span:.1f} mm (<= gantry_z_travel = {p.gantry_z_travel} mm)",
    ))

    # Pin-slot friction proxy (Edison v3 sec. 4): sharp corners in the
    # slot path spike the normal force on the peg and bind the mechanism.
    # We measure the largest direction change across any interior
    # waypoint and fail if it exceeds slot_max_corner_deg.
    worst_corner_deg = 0.0
    worst_idx = -1
    for i in range(1, len(p.slot_path) - 1):
        x0, z0 = p.slot_path[i - 1]
        x1, z1 = p.slot_path[i]
        x2, z2 = p.slot_path[i + 1]
        a1 = math.atan2(z1 - z0, x1 - x0)
        a2 = math.atan2(z2 - z1, x2 - x1)
        d = math.degrees(abs(a2 - a1))
        if d > 180.0:
            d = 360.0 - d
        if d > worst_corner_deg:
            worst_corner_deg = d
            worst_idx = i
    rs.append(_check(
        "kinematics.slot.peg_friction.corner_angle",
        worst_corner_deg <= p.slot_max_corner_deg,
        (f"largest slot-path corner = {worst_corner_deg:.1f} deg at waypoint "
         f"{worst_idx} (<= slot_max_corner_deg = {p.slot_max_corner_deg:.1f} deg "
         "to avoid binding the peg)") if worst_idx >= 0
        else "no interior waypoints to evaluate corner angle",
    ))
    return rs


# ---------------------------------------------------------------------------
# Physics-of-mechanism checks (Edison v3 sec. 4)
# ---------------------------------------------------------------------------


def _loaded_cg_y(p: ExcavatorParams) -> tuple[float, float]:
    """Return ``(cg_y_mm, total_mass_g)`` for the loaded trough.

    Treats the half-cylinder shell as a thin-walled half-cylinder (centroid
    at -2 r / pi from the rim), the powder column as a uniform half-disk
    extruded by the cavity length (centroid at -4 r / (3 pi) from the
    rim), and each rim lip as a small rectangular bar at Y ~ +bumper_height/2.
    Densities come from ``p.print_material_density`` and
    ``p.powder_bulk_density`` (g/cm^3); lengths in mm so volumes are in
    mm^3 and masses divided by 1000 give grams.
    """
    r_in = p.trough_radius                           # mm
    r_out = p.trough_radius + p.trough_wall          # mm
    L = p.trough_length                              # mm
    cavity_len = L - 2 * p.end_cap_thickness         # mm
    rho_p = p.print_material_density / 1000.0        # g/mm^3
    rho_pw = p.powder_bulk_density / 1000.0          # g/mm^3

    # Thin-walled half-cylinder shell, full length L.
    shell_vol = 0.5 * math.pi * (r_out ** 2 - r_in ** 2) * L
    shell_cg_y = -2 * ((r_out + r_in) / 2) / math.pi  # ~ -2 r_mean / pi
    # End caps (two thin half-disks at +/- L/2). Their CG is the half-disk
    # centroid at -4 r_out / (3 pi).
    cap_vol = 2 * 0.5 * math.pi * r_out ** 2 * p.end_cap_thickness
    cap_cg_y = -4 * r_out / (3 * math.pi)
    # Powder column: uniform half-disk of inner radius r_in extruded by
    # cavity length.
    powder_vol = 0.5 * math.pi * r_in ** 2 * cavity_len
    powder_cg_y = -4 * r_in / (3 * math.pi)
    # Two rim lips along the full length L. Each lip is a bumper_width x
    # bumper_height x L bar. The chamfer trims a corner, but for the CG
    # estimate we approximate the lip as a solid bar centred at
    # Y = bumper_height/2.
    lip_vol = 2 * (p.bumper_width * p.bumper_height * L)
    lip_cg_y = p.bumper_height / 2.0
    # Pivot bosses (two short cylinders, axis along Z) at Y = pivot_offset_y.
    boss_vol = 2 * math.pi * (p.pivot_boss_diameter / 2) ** 2 * p.pivot_boss_thickness
    boss_cg_y = p.pivot_offset_y

    pieces = [
        (shell_vol, shell_cg_y, rho_p),
        (cap_vol, cap_cg_y, rho_p),
        (lip_vol, lip_cg_y, rho_p),
        (boss_vol, boss_cg_y, rho_p),
        (powder_vol, powder_cg_y, rho_pw),
    ]
    total_m = sum(v * rho for v, _, rho in pieces)
    if total_m <= 0:
        return (0.0, 0.0)
    cg_y = sum(v * rho * y for v, y, rho in pieces) / total_m
    return (cg_y, total_m)


def check_pendulum_stability(p: ExcavatorParams) -> list[CheckResult]:
    """The loaded CG must sit BELOW the pivot for a stable pendulum."""
    cg_y, mass_g = _loaded_cg_y(p)
    margin = p.pivot_offset_y - cg_y  # positive => pivot above CG => stable
    return [_check(
        "physics.pendulum.cg_below_pivot",
        margin > 0.5,
        (f"loaded CG at Y = {cg_y:+.2f} mm, pivot at Y = {p.pivot_offset_y:+.2f} mm, "
         f"margin = {margin:+.2f} mm (need pivot >= 0.5 mm above CG for a "
         f"stable pendulum; loaded mass ~ {mass_g:.1f} g)"),
    )]


def _cam_lever_arm(p: ExcavatorParams) -> float:
    """Distance from the pivot pin to the outer corner of the rim lip.

    The cam ramp pushes on the outer-top corner of one rim lip; the
    moment arm for the cam reaction is the distance from that corner to
    the pivot. Used for both the sensitivity and the rise-utilisation
    checks below.
    """
    outer_r = p.trough_radius + p.trough_wall
    lip_outer_x = outer_r + p.bumper_width
    lip_outer_y = p.bumper_height
    return math.hypot(lip_outer_x, lip_outer_y - p.pivot_offset_y)


def check_cam_sensitivity(p: ExcavatorParams) -> list[CheckResult]:
    """Cam tilt sensitivity d(theta)/d(X) must stay finite at the target tilt.

    Modelling the lip's outer corner as a point on a rigid lever of
    length ``R`` rotating about the pivot, the horizontal contact
    point with the ramp moves like ``X(theta) = R * sin(theta + phi0)``
    where ``phi0`` is the lever's initial angle from horizontal. So
    ``dX/dtheta = R * cos(theta + phi0)`` and the sensitivity
    ``dtheta/dX = 1 / (R * cos(theta + phi0))`` blows up to infinity
    as the lever passes vertical. (Edison v3 sec. 1 "Cam Singularity".)
    """
    outer_r = p.trough_radius + p.trough_wall
    lip_outer_x = outer_r + p.bumper_width
    lip_outer_y = p.bumper_height
    R = _cam_lever_arm(p)
    phi0 = math.atan2(lip_outer_y - p.pivot_offset_y, lip_outer_x)
    target = math.radians(p.cam_target_tilt_deg)
    cos_term = math.cos(target + phi0)
    if cos_term <= 0:
        return [_check(
            "physics.cam.sensitivity",
            False,
            (f"cam lever passes vertical before reaching target tilt "
             f"{p.cam_target_tilt_deg:.0f} deg (lever R = {R:.1f} mm, "
             f"initial phi0 = {math.degrees(phi0):.1f} deg); sensitivity is "
             "infinite (snap-through singularity)"),
        )]
    sens_deg_per_mm = math.degrees(1.0 / (R * cos_term))
    return [_check(
        "physics.cam.sensitivity",
        sens_deg_per_mm <= p.cam_sensitivity_ceiling_deg_per_mm,
        (f"cam dtheta/dX at target tilt {p.cam_target_tilt_deg:.0f} deg = "
         f"{sens_deg_per_mm:.2f} deg/mm (<= "
         f"{p.cam_sensitivity_ceiling_deg_per_mm:.1f} deg/mm; lever R = "
         f"{R:.1f} mm)"),
    )]


def check_cam_rise_utilisation(p: ExcavatorParams) -> list[CheckResult]:
    """The configured ramp rise must not exceed what the lever can lift.

    Over a 0->target_tilt sweep, the lip's outer corner rises by
    ``R * (sin(target + phi0) - sin(phi0))``. If ``cam_ramp_rise``
    exceeds this, the extra material is unreachable -- the ramp is
    physically taller than the cam can ride up. (Edison v3 sec. 1 -- the
    20 mm cam_ramp_rise was wasted because the lever could only lift
    ~9.5 mm.)
    """
    outer_r = p.trough_radius + p.trough_wall
    lip_outer_x = outer_r + p.bumper_width
    lip_outer_y = p.bumper_height
    R = _cam_lever_arm(p)
    phi0 = math.atan2(lip_outer_y - p.pivot_offset_y, lip_outer_x)
    target = math.radians(p.cam_target_tilt_deg)
    max_rise = R * (math.sin(target + phi0) - math.sin(phi0))
    if max_rise <= 0:
        return [_check(
            "physics.cam.rise_utilisation",
            False,
            (f"cam lever cannot lift over a 0 -> {p.cam_target_tilt_deg:.0f} deg "
             f"sweep (R = {R:.1f} mm, phi0 = {math.degrees(phi0):.1f} deg)"),
        )]
    return [_check(
        "physics.cam.rise_utilisation",
        p.cam_ramp_rise <= max_rise + 0.5,
        (f"cam_ramp_rise = {p.cam_ramp_rise:.1f} mm vs max achievable rise "
         f"= {max_rise:.1f} mm at target tilt {p.cam_target_tilt_deg:.0f} deg "
         "(extra ramp height above this is unreachable)"),
        severity="warning",
    )]


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def run_all(p: ExcavatorParams | None = None) -> list[CheckResult]:
    p = p or ExcavatorParams()
    return (
        check_sanity(p)
        + check_printability(p)
        + check_gantry_only_cam_ramp(p)
        + check_gantry_only_slot_board(p)
        + check_pendulum_stability(p)
        + check_cam_sensitivity(p)
        + check_cam_rise_utilisation(p)
    )


def main() -> int:
    p = ExcavatorParams()
    results = run_all(p)
    for r in results:
        print(r.render())
    n_fail = sum(1 for r in results if not r.ok and r.severity == "error")
    n_warn = sum(1 for r in results if not r.ok and r.severity == "warning")
    print()
    print(f"summary: {len(results)} checks, "
          f"{n_fail} failure(s), {n_warn} warning(s).")
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())

```

=== file: cad/excavator.py ===
```py
"""Parametric CAD model of the powder-excavator (CadQuery / open-source).

This is the start of a **feedback-loop friendly** CAD pipeline for the
powder-excavator design described in ``docs/manuscript/main.tex``. CadQuery
was chosen over closed-source authoring tools (Rhino + Grasshopper, Fusion
Generative Design, nTop, Onshape FeatureScript) because it is

* pure Python and pip-installable on every major OS,
* fully scripted (no GUI required for parametric updates), so a design
  iteration is just a ``git diff`` and a re-run, and
* produces standards-compliant STEP and STL output that any open-source
  slicer (PrusaSlicer, OrcaSlicer, Cura) can consume.

The single source of truth for every dimension is :class:`ExcavatorParams`.
Changing one number there propagates through every part.

Usage
-----

Build all parts and the assembly to ``cad/build/`` (run from the repo root)::

    python -m cad.build

Run the design-for-manufacturing checks (per-part wall thickness, FDM
overhang angles, gantry-only kinematics)::

    python -m cad.dfm

Both modules import :func:`build_assembly` from this file, so the same
parametric model drives both the export and the feedback checks.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

import cadquery as cq

# Type alias for cadquery objects we hand back to the caller.
CQObject = Any


# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ExcavatorParams:
    """All design parameters for the powder-excavator, in millimetres.

    Defaults match the dimensions called out in the README and
    ``docs/manuscript/main.tex`` for the longitudinal-pivot, sideways-tilt
    geometry (trough length L = 80 mm, L ~ 3 D, etc.). Mutating values is
    forbidden so the model is reproducible: build a new instance instead.
    """

    # ----- trough (the half-cylinder ladle, open at the top) -----
    trough_length: float = 80.0           # L, along the long pivot axis
    trough_radius: float = 13.0           # inner radius of the half-cylinder
    trough_wall: float = 1.6              # printed wall thickness
    end_cap_thickness: float = 2.0        # closed end caps at +/- L/2

    # ----- pivot (a metal dowel pin running along L through both end caps) -
    pin_diameter: float = 3.0
    # Diametral clearance for the printed pivot hole. 0.3 mm is the lower
    # end of the standard FDM sliding-fit window (0.3-0.4 mm); 0.2 mm
    # was found to fuse / bind in print (Edison v3 analysis, docs/edison/
    # analysis-v3-longitudinal-tilt-cad.md sec. 3).
    pin_clearance: float = 0.3
    pivot_boss_diameter: float = 8.0      # local boss around the pin hole
    pivot_boss_thickness: float = 4.0
    # Y-coordinate of the pivot pin axis in trough-local coords (rim is at
    # Y = 0, half-cylinder hangs into -Y). To keep the loaded trough as a
    # *stable* pendulum, the pivot has to sit ABOVE the loaded centre of
    # gravity. For a half-cylinder filled with powder, the powder centroid
    # is at -4 r / (3 pi) ~ -5.5 mm for r = 13 mm; combined with the shell
    # and small rim lips the loaded CG is around -5 mm. Putting the pivot
    # at Y = -4 mm keeps it ~1 mm above the loaded CG (stable) while
    # leaving the 8 mm pivot boss fully inscribed in the half-disk
    # end-cap envelope. (Edison v3 sec. 1, "Inverted Pendulum" flaw.)
    pivot_offset_y: float = -4.0

    # ----- arms (two parallel verticals dropping from the gantry) -----
    # Axis assignments below match :func:`build_arm`: the arm's wide face
    # (``arm_width``) is along X (perpendicular to both Y and the pin
    # axis), giving good bending stiffness against the cam reaction load.
    # The arm is thin along Z (``arm_thickness``), which is the trough's
    # longitudinal pin axis. ``arm_length`` is the vertical drop in Y
    # from the carriage down to the pin-hole height.
    arm_thickness: float = 4.0            # along Z (pin axis = along trough length L)
    arm_width: float = 8.0                # along X (perpendicular face), must clear pivot boss
    arm_length: float = 60.0              # vertical drop from carriage (Y)
    arm_gap: float = 1.0                  # gap between arm inside face and trough end cap

    # ----- chamfered rim lip on the trough (defines the pour edge AND
    #       engages the cam ramp) -----
    # The lip runs continuously along the full trough length L on BOTH
    # long-side rims (the trough is symmetric, so it can dump in either
    # direction; whichever rim is on the cam-side becomes the "bumper" for
    # that stroke). A continuous lip — rather than a localised spout —
    # avoids reintroducing a powder-arching bottleneck at the pour edge,
    # while the chamfer (a) detaches the powder stream cleanly, (b) defines
    # a sharp geometric tip-over angle (better dose-vs-tilt repeatability),
    # and (c) provides a low-overhang printable surface for the cam to
    # ride on.
    #
    # Lip cross-section is kept SMALL (2 x 2 mm with a 1 mm chamfer): the
    # earlier 6 x 6 mm lips added ~7 g of PETG well above the rim and
    # pushed the loaded CG above the pivot, ruining pendulum stability.
    # (Edison v3 sec. 1 + sec. 3, lip geometry.)
    bumper_height: float = 2.0            # radial protrusion of the lip
    bumper_chamfer: float = 1.0           # outside-edge chamfer dimension
    bumper_width: float = 2.0             # lip thickness in X (cross-section)

    # ----- fixed bed-edge strike-off bar -----
    strike_off_length: float = 100.0      # spans the bed edge
    strike_off_section: float = 4.0       # square cross-section side

    # ----- smooth inclined cam ramp (baseline tilt actuator) -----
    # NB Edison v3 sec. 1 flagged the cam ramp as kinematically marginal
    # (snap-through singularity past ~40 deg, cam_ramp_rise was wasted
    # above the lever's max reach). The pin-slot variant (Panel E) is
    # therefore the recommended baseline; the cam ramp is kept here as
    # a fallback option whose dimensions are clamped to the
    # max-achievable lift (~R*(sin(target+phi0)-sin(phi0))) instead of
    # an unreachable 20 mm. dfm.py's physics.cam.rise_utilisation check
    # enforces this.
    cam_ramp_length: float = 35.0         # along gantry X
    cam_ramp_rise: float = 10.0           # vertical rise across the ramp (within lever's reach)
    cam_ramp_width: float = 10.0          # along gantry Y
    cam_ramp_thickness: float = 8.0       # below the running surface

    # ----- pin-slot variant (per PXL_20260423_231729467.jpg, manuscript Sec. ``Pin-defined-path actuation'') -----
    slot_board_length: float = 220.0      # along gantry X
    slot_board_height: float = 60.0       # along gantry Z
    slot_board_thickness: float = 6.0     # along gantry Y
    slot_width: float = 4.2               # peg diameter + clearance
    slot_depth: float = 5.0               # routed depth into the board
    # Polyline of (X, Z) waypoints describing the slot path on the board, in
    # the board's local frame (origin at the bottom-left corner of the board).
    # Default is the same path baked into ``panel-E-pin-slot.svg``: flat for
    # the scoop+transport stretch, rising over the deposit station.
    slot_path: tuple[tuple[float, float], ...] = (
        (10.0, 30.0),
        (140.0, 30.0),
        (170.0, 24.0),
        (200.0, 12.0),
        (210.0, 12.0),
    )

    # ----- gantry working envelope (used by dfm.py's kinematic checks) -----
    gantry_x_travel: float = 250.0
    gantry_z_travel: float = 80.0

    # ----- physics-of-mechanism feedback targets (used by dfm.py) -----
    # Target useful tilt angle for the cam ramp (deg from horizontal). The
    # cam ramp must be able to drive the trough this far before the
    # tilt-vs-X sensitivity saturates (snap-through singularity).
    cam_target_tilt_deg: float = 45.0
    # Maximum acceptable d(theta)/d(X) sensitivity for the cam ramp at the
    # target tilt, in deg per mm of gantry X travel. >15 deg/mm makes
    # metered pouring uncontrollable. (Edison v3 sec. 1, "Cam Singularity"
    # flaw and sec. 4, dfm.py shortfalls.)
    cam_sensitivity_ceiling_deg_per_mm: float = 15.0
    # Maximum acceptable change in slot direction at any waypoint, in
    # degrees. Sharp corners spike the normal force on the peg and make
    # the slot bind. (Edison v3 sec. 4, pin-slot friction.)
    slot_max_corner_deg: float = 60.0
    # Powder bulk density (g/cm^3) used for the loaded centre-of-gravity
    # calculation in the pendulum-stability check. 1.0 g/cm^3 is a
    # reasonable default for inorganic powders at packed bulk density.
    powder_bulk_density: float = 1.0
    # Print material density (g/cm^3) used for the loaded CG calculation.
    # 1.27 g/cm^3 is PETG; PLA is 1.24, nylon 1.14.
    print_material_density: float = 1.27

    # ----- FDM-printability targets (used by dfm.py's printability checks) -
    min_wall: float = 0.8                 # absolute minimum FDM wall (4-perimeter @ 0.2 mm)
    max_overhang_deg: float = 50.0        # measured from vertical; >50 needs supports

    # Optional metadata (e.g. the git SHA of the design used). Excluded from
    # geometry but useful when the build script writes a manifest.
    metadata: dict[str, str] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Individual parts
# ---------------------------------------------------------------------------


def _half_disk_solid(radius: float) -> cq.Workplane:
    return (
        cq.Workplane("XY")
        .moveTo(-radius, 0)
        .lineTo(radius, 0)
        .threePointArc((0, -radius), (-radius, 0))
        .close()
    )


def build_trough(p: ExcavatorParams) -> CQObject:
    """The open-top half-cylinder ladle with closed end caps and pivot bosses.

    The trough is built lying along the +Z axis (length L along Z), with its
    open top facing +Y, so that the longitudinal pivot pin runs through the
    centre of the two end caps along Z.
    """
    # Outer solid (full length, full outer radius)
    outer = _half_disk_solid(p.trough_radius + p.trough_wall).extrude(p.trough_length)
    # Inner cavity (full outer minus end caps -> length L - 2 * cap)
    cavity_len = p.trough_length - 2 * p.end_cap_thickness
    cavity = (
        _half_disk_solid(p.trough_radius)
        .extrude(cavity_len)
        .translate((0, 0, p.end_cap_thickness))
    )
    body = outer.cut(cavity)

    # Pivot bosses sit on the OUTSIDE of each end cap. Their axis is along
    # Z. We place them on the longitudinal centre line of the half-cylinder
    # at (X=0, Y=p.pivot_offset_y); ``pivot_offset_y`` is chosen above the
    # loaded CG to give a stable pendulum (Edison v3 sec. 1).
    pivot_centre_y = p.pivot_offset_y
    boss = (
        cq.Workplane("XY")
        .center(0, pivot_centre_y)
        .circle(p.pivot_boss_diameter / 2)
        .extrude(p.pivot_boss_thickness)
    )
    boss0 = boss.translate((0, 0, -p.pivot_boss_thickness))
    boss1 = boss.translate((0, 0, p.trough_length))

    # Drill the pin clearance hole through caps + bosses (one pass along Z).
    pin_hole_len = p.trough_length + 2 * p.pivot_boss_thickness + 2.0
    pin_hole = (
        cq.Workplane("XY")
        .center(0, pivot_centre_y)
        .circle((p.pin_diameter + p.pin_clearance) / 2)
        .extrude(pin_hole_len)
        .translate((0, 0, -p.pivot_boss_thickness - 1.0))
    )

    # Continuous chamfered lip on each long-side rim, running the full
    # trough length L. Replaces the localised mid-length "bumper": a
    # localised spout would reintroduce a powder-arching bottleneck at the
    # pour edge (cf. Edison v2 §3 on the 90° V-pocket retention problem).
    # The lip is symmetric (one per long side) so the trough can dump
    # either way and either rim can be the cam-engagement surface; the
    # outside chamfer on each lip is what actually rides up the cam ramp
    # and what defines the pour edge's tip-over angle.
    outer_r = p.trough_radius + p.trough_wall
    lip_x_centre = outer_r - p.bumper_width / 2

    def _make_lip(sign: int) -> CQObject:
        # ``sign`` is +1 for the right rim, -1 for the left rim.  The
        # chamfered edge is the OUTER top edge (the one furthest from the
        # trough centre line, on the +Y side), since that is what the cam
        # ramp rides on and what the powder stream detaches from.
        lip = (
            cq.Workplane("XY")
            .box(
                p.bumper_width,        # X (lip thickness, sits on the rim wall)
                p.bumper_height,       # Y (radial protrusion above the rim)
                p.trough_length,       # Z (runs the full length L)
                centered=(True, False, False),
            )
        )
        outer_edge = ">X and >Y" if sign > 0 else "<X and >Y"
        lip = lip.edges(outer_edge).chamfer(p.bumper_chamfer)
        return lip.translate((sign * lip_x_centre, 0, 0))

    lip_right = _make_lip(+1)
    lip_left = _make_lip(-1)

    return body.union(boss0).union(boss1).union(lip_right).union(lip_left).cut(pin_hole)


def build_arm(p: ExcavatorParams) -> CQObject:
    """One vertical arm.

    Two of these are mirrored about z = L/2 to grip the trough's two end
    caps. The arm hangs from a carriage above it (not modelled here) down
    to the pivot pin at its lower end. In model coordinates:

    * +Y is the trough's open-top direction (and also "world up"), so the
      arm extends from Y = 0 (its pin-hole height, which is placed at the
      pivot height in :func:`build_assembly`) up in +Y to the carriage.
    * +Z is the trough's longitudinal pin axis, so the arm is thin along
      Z (``arm_thickness``) and the pin clearance hole runs along Z too.
    * The arm's wide face (``arm_width``) is along X, perpendicular to
      both, giving good bending stiffness against the cam reaction load.
    """
    arm = (
        cq.Workplane("XY")
        .box(
            p.arm_width,        # X (wide face — bending stiffness)
            p.arm_length,       # Y (vertical drop from gantry carriage)
            p.arm_thickness,    # Z (along pin axis = along trough length L)
            centered=(True, False, True),
        )
    )
    # Pin clearance hole at the bottom of the arm (Y = 0 in arm-local
    # coords), drilled along +Z so it matches the pin's axis. Extruded
    # ``both=True`` so it punches all the way through the arm regardless
    # of arm_thickness.
    pin_hole = (
        cq.Workplane("XY")
        .circle((p.pin_diameter + p.pin_clearance) / 2)
        .extrude(p.arm_thickness * 2, both=True)
    )
    return arm.cut(pin_hole)


def build_pin(p: ExcavatorParams) -> CQObject:
    """Stock metal dowel pin (the pivot)."""
    total_length = (
        p.trough_length
        + 2 * p.pivot_boss_thickness
        + 2 * (p.arm_gap + p.arm_thickness)
    )
    return (
        cq.Workplane("XY")
        .circle(p.pin_diameter / 2)
        .extrude(total_length)
    )


def build_strike_off_bar(p: ExcavatorParams) -> CQObject:
    """The fixed bed-edge strike-off bar (square cross-section)."""
    return (
        cq.Workplane("XY")
        .box(p.strike_off_section, p.strike_off_length, p.strike_off_section)
    )


def build_cam_ramp(p: ExcavatorParams) -> CQObject:
    """The fixed smooth inclined cam ramp the bumper rides up.

    Built as a triangular prism plus a flat mounting base.
    """
    triangle = (
        cq.Workplane("XZ")
        .moveTo(0, 0)
        .lineTo(p.cam_ramp_length, 0)
        .lineTo(p.cam_ramp_length, p.cam_ramp_rise)
        .close()
    )
    ramp = triangle.extrude(p.cam_ramp_width)
    base = (
        cq.Workplane("XY")
        .box(
            p.cam_ramp_length,
            p.cam_ramp_width,
            p.cam_ramp_thickness,
            centered=(False, False, False),
        )
        .translate((0, 0, -p.cam_ramp_thickness))
    )
    return ramp.union(base)


def build_slot_board(p: ExcavatorParams) -> CQObject:
    """Routed slot board for the pin-defined-path actuation variant.

    The board is a rectangular slab with a slot routed along the polyline
    given by ``params.slot_path``. The slot is a fixed-width channel of
    depth ``slot_depth`` routed in from the +Y face of the board (the
    face the peg engages). The peg on the trough's stem rides inside it.
    If ``slot_depth >= slot_board_thickness`` the slot becomes a
    through-slot.
    """
    board = (
        cq.Workplane("XZ")
        .box(p.slot_board_length, p.slot_board_height, p.slot_board_thickness)
    )
    # Cut depth is clamped at the board thickness (a routed slot deeper
    # than the board itself just becomes a through-slot, not a cut into
    # both faces).
    cut_depth = min(p.slot_depth, p.slot_board_thickness)
    # Y-centre of the cut so it removes material from the +Y face inward
    # by exactly ``cut_depth`` (board is centred on Y=0 with thickness
    # ``slot_board_thickness``, so its +Y face is at +thickness/2).
    cut_y_centre = p.slot_board_thickness / 2 - cut_depth / 2
    # Build the slot as the union of "fat segments" (one per polyline edge),
    # avoiding CadQuery's arbitrary-path sweep which is brittle across
    # versions.
    slot_solid: CQObject = None
    for (x0, z0), (x1, z1) in zip(p.slot_path, p.slot_path[1:]):
        wx0 = x0 - p.slot_board_length / 2
        wz0 = z0 - p.slot_board_height / 2
        wx1 = x1 - p.slot_board_length / 2
        wz1 = z1 - p.slot_board_height / 2
        seg_len = math.hypot(wx1 - wx0, wz1 - wz0)
        if seg_len <= 0:
            continue
        ang_deg = math.degrees(math.atan2(wz1 - wz0, wx1 - wx0))
        seg = (
            cq.Workplane("XZ")
            .box(
                seg_len + p.slot_width,
                p.slot_width,
                cut_depth,
                centered=(True, True, True),
            )
        )
        seg = seg.rotate((0, 0, 0), (0, 1, 0), -ang_deg)
        seg = seg.translate(((wx0 + wx1) / 2, cut_y_centre, (wz0 + wz1) / 2))
        slot_solid = seg if slot_solid is None else slot_solid.union(seg)
    if slot_solid is not None:
        board = board.cut(slot_solid)
    return board


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------


def build_assembly(p: ExcavatorParams | None = None) -> cq.Assembly:
    """Build the full assembly (trough + two arms + pin)."""
    p = p or ExcavatorParams()
    trough = build_trough(p)
    arm = build_arm(p)
    pin = build_pin(p)

    asm = cq.Assembly(name="powder_excavator")
    asm.add(trough, name="trough", color=cq.Color(0.7, 0.7, 0.75))

    pivot_centre_y = p.pivot_offset_y
    arm_outer_z0 = -p.pivot_boss_thickness - p.arm_gap - p.arm_thickness / 2
    arm_outer_z1 = (
        p.trough_length + p.pivot_boss_thickness + p.arm_gap + p.arm_thickness / 2
    )
    asm.add(
        arm,
        name="arm_left",
        loc=cq.Location(cq.Vector(0, pivot_centre_y, arm_outer_z0)),
        color=cq.Color(0.4, 0.4, 0.45),
    )
    asm.add(
        arm,
        name="arm_right",
        loc=cq.Location(cq.Vector(0, pivot_centre_y, arm_outer_z1)),
        color=cq.Color(0.4, 0.4, 0.45),
    )
    asm.add(
        pin,
        name="pin",
        loc=cq.Location(cq.Vector(
            0, pivot_centre_y,
            -(p.pivot_boss_thickness + p.arm_gap + p.arm_thickness),
        )),
        color=cq.Color(0.85, 0.2, 0.2),
    )

    return asm


__all__ = [
    "ExcavatorParams",
    "build_arm",
    "build_assembly",
    "build_cam_ramp",
    "build_pin",
    "build_slot_board",
    "build_strike_off_bar",
    "build_trough",
]

```

=== file: cad/render.py ===
```py
"""Render the parametric CAD model to SVG views of the actual 3D geometry.

Where ``scripts/generate_figures.py`` draws hand-laid-out *schematic* figures
that explain the design intent, this module produces *honest renders* of the
geometry returned by :mod:`cad.excavator` -- i.e.\\ what the part will
actually look like when it comes off the FDM printer. Each part gets a small
vector SVG (hidden-line removed) under ``docs/figures/cad/``; the full
assembly gets one extra render so the trough/arms/pin relationship is
visible at a glance.

Run from the repo root::

    python -m cad.render

Outputs land under ``docs/figures/cad/`` (committed alongside the schematic
figures so they appear in the GitHub preview without requiring a full CAD
toolchain on the reader's machine).

Implementation notes:

* CadQuery's built-in SVG exporter is used (``cq.exporters.export(... ,
  exportType='SVG', opt=...)``). This is a vector projection with hidden-
  line removal; no raster renderer or X server is required.

* The model uses CadQuery's +Y as "world up" (open top of the trough) and
  +Z as the trough's longitudinal pin axis L. The default isometric
  projection direction sits the camera on the +X / +Y / +Z octant so the
  open ladle interior is visible.

* The assembly is rendered by collapsing it to a single ``Compound`` via
  ``asm.toCompound()``; this loses per-part colour but keeps geometry,
  which is the point of a "what does the print look like" view.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

import cadquery as cq

from .excavator import (
    ExcavatorParams,
    build_arm,
    build_assembly,
    build_cam_ramp,
    build_pin,
    build_slot_board,
    build_strike_off_bar,
    build_trough,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
RENDER_DIR = REPO_ROOT / "docs" / "figures" / "cad"

# Isometric viewpoint: camera on +X / +Y / +Z octant, looking back toward
# the origin. CadQuery's ``projectionDir`` is the camera's look-at direction
# (from camera to scene), so a vector with all-negative components puts the
# camera in the all-positive octant. With the trough's open top facing +Y
# this exposes the ladle interior, end caps, and rim lips simultaneously.
_ISO_DIR = (-0.7, -1.0, -0.6)

# Shared SVG exporter options. Picked so every part renders into the same
# isometric viewpoint with hidden-line dashes turned on, which is what a
# reader expects from a "CAD render" -- a clean orthographic-style line
# drawing rather than a shaded raster.
_BASE_OPT: dict[str, Any] = {
    "width": 720,
    "height": 540,
    "marginLeft": 20,
    "marginTop": 20,
    "showAxes": False,
    "projectionDir": _ISO_DIR,
    "strokeWidth": 0.4,
    "strokeColor": (40, 40, 40),
    "hiddenColor": (180, 180, 180),
    "showHidden": True,
}


def _render(part: cq.Workplane | cq.Shape, stem: str, **opt_overrides: Any) -> Path:
    """Render a single part to ``RENDER_DIR / f"{stem}.svg"`` and return the path."""
    opt = {**_BASE_OPT, **opt_overrides}
    out = RENDER_DIR / f"{stem}.svg"
    cq.exporters.export(part, str(out), exportType="SVG", opt=opt)
    return out


def main() -> None:
    RENDER_DIR.mkdir(parents=True, exist_ok=True)
    p = ExcavatorParams()

    # Per-part renders. Order them so the printable parts come first
    # (they are the ones a reader will actually slice and print).
    parts: dict[str, Callable[[ExcavatorParams], Any]] = {
        "trough":         build_trough,
        "arm":            build_arm,
        "pin":            build_pin,
        "strike_off_bar": build_strike_off_bar,
        "cam_ramp":       build_cam_ramp,
        "slot_board":     build_slot_board,
    }
    for name, fn in parts.items():
        out = _render(fn(p), name)
        print(f"wrote {out.relative_to(REPO_ROOT)}")

    # Full assembly. We render three views so the arm / pin / trough
    # relationship is unambiguous: an isometric (default), an end view
    # (looking along the pin axis -- shows the half-cylinder cross-section
    # and how the arms grip the end caps), and a side view (perpendicular
    # to the pin axis -- shows the full length L and both arms).
    asm = build_assembly(p)
    comp = asm.toCompound()
    for view, proj in (
        ("assembly",          _ISO_DIR),         # iso
        ("assembly-end",      (0.0, 0.0, -1.0)), # along the pin axis
        ("assembly-side",     (1.0, 0.0, 0.0)),  # perpendicular to pin axis
    ):
        out = _render(comp, view, width=900, height=600, projectionDir=proj)
        print(f"wrote {out.relative_to(REPO_ROOT)}")


if __name__ == "__main__":  # pragma: no cover
    main()

```

=== file: cad/README.md ===
````md
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

````

=== file: cad/tests/__init__.py ===
```py

```

=== file: cad/tests/test_excavator.py ===
```py
"""Unit tests for the parametric CAD model and the DFM feedback loop.

Run from the repo root::

    python -m unittest discover cad/tests

These tests are deliberately fast (no STL/STEP export, no slicing). They
exercise three things:

1. The parametric model builds without errors at default parameters.
2. The DFM check passes (no errors) at default parameters.
3. Deliberate parameter regressions -- making the trough wall thinner than
   the FDM minimum, and routing the slot path off the board -- are correctly
   caught by the DFM checks.
"""

from __future__ import annotations

import unittest
from dataclasses import replace

from cad.dfm import run_all
from cad.excavator import (
    ExcavatorParams,
    build_arm,
    build_assembly,
    build_cam_ramp,
    build_pin,
    build_slot_board,
    build_strike_off_bar,
    build_trough,
)


class BuildTests(unittest.TestCase):
    def test_parts_build_at_defaults(self) -> None:
        p = ExcavatorParams()
        for part_fn in (
            build_trough, build_arm, build_pin,
            build_strike_off_bar, build_cam_ramp, build_slot_board,
        ):
            with self.subTest(part=part_fn.__name__):
                obj = part_fn(p)
                vol = obj.val().Volume()
                self.assertGreater(vol, 0.0, f"{part_fn.__name__} has zero volume")

    def test_assembly_builds(self) -> None:
        asm = build_assembly()
        names = {c.name for c in asm.children}
        self.assertIn("trough", names)
        self.assertIn("arm_left", names)
        self.assertIn("arm_right", names)
        self.assertIn("pin", names)


class DFMTests(unittest.TestCase):
    def test_defaults_pass(self) -> None:
        results = run_all(ExcavatorParams())
        failures = [r for r in results if not r.ok and r.severity == "error"]
        self.assertFalse(
            failures,
            f"DFM should pass at default parameters; failures: "
            f"{[r.name for r in failures]}",
        )

    def test_thin_wall_fails(self) -> None:
        bad = replace(ExcavatorParams(), trough_wall=0.4)
        results = run_all(bad)
        names = [r.name for r in results if not r.ok and r.severity == "error"]
        self.assertIn("fdm.min_wall.trough", names)

    def test_slot_off_board_fails(self) -> None:
        bad = replace(
            ExcavatorParams(),
            slot_path=((10.0, 30.0), (5000.0, 30.0)),
        )
        results = run_all(bad)
        names = [r.name for r in results if not r.ok and r.severity == "error"]
        self.assertIn("kinematics.slot.waypoints_inside_board", names)

    def test_inverted_pendulum_fails(self) -> None:
        # Old defaults (pivot at -trough_radius/2 = -6.5 mm with the
        # heavy 6x6 lips) put the loaded CG above the pivot. This is
        # the Edison-v3 inverted-pendulum failure mode.
        bad = replace(
            ExcavatorParams(),
            pivot_offset_y=-6.5,
            bumper_height=6.0,
            bumper_chamfer=2.0,
            bumper_width=6.0,
        )
        results = run_all(bad)
        names = [r.name for r in results if not r.ok and r.severity == "error"]
        self.assertIn("physics.pendulum.cg_below_pivot", names)

    def test_cam_sensitivity_singularity_fails(self) -> None:
        # A short lever arm + a tilt target near the singularity must
        # blow the d(theta)/d(X) ceiling.
        bad = replace(
            ExcavatorParams(),
            cam_target_tilt_deg=80.0,
            cam_sensitivity_ceiling_deg_per_mm=15.0,
        )
        results = run_all(bad)
        names = [r.name for r in results if not r.ok and r.severity == "error"]
        self.assertIn("physics.cam.sensitivity", names)

    def test_sharp_slot_corner_fails(self) -> None:
        bad = replace(
            ExcavatorParams(),
            slot_path=((20.0, 30.0), (100.0, 30.0), (100.0, 10.0), (180.0, 10.0)),
        )
        results = run_all(bad)
        names = [r.name for r in results if not r.ok and r.severity == "error"]
        self.assertIn("kinematics.slot.peg_friction.corner_angle", names)

    def test_slot_x_reversal_warns(self) -> None:
        # Path that goes +X then -X requires a gantry-X reversal; this
        # should be flagged (not-ok at warning severity) by
        # kinematics.slot.gantry_x_only.
        bad = replace(
            ExcavatorParams(),
            slot_path=((20.0, 30.0), (180.0, 30.0), (50.0, 30.0)),
        )
        results = run_all(bad)
        match = next(r for r in results if r.name == "kinematics.slot.gantry_x_only")
        self.assertFalse(match.ok)
        self.assertEqual(match.severity, "warning")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

```

=== file: cad/build/manifest.json ===
```json
{
  "files": [
    "cad/build/trough.step",
    "cad/build/trough.stl",
    "cad/build/arm.step",
    "cad/build/arm.stl",
    "cad/build/pin.step",
    "cad/build/pin.stl",
    "cad/build/strike_off_bar.step",
    "cad/build/strike_off_bar.stl",
    "cad/build/cam_ramp.step",
    "cad/build/cam_ramp.stl",
    "cad/build/slot_board.step",
    "cad/build/slot_board.stl",
    "cad/build/assembly.step"
  ],
  "params": {
    "arm_gap": 1.0,
    "arm_length": 60.0,
    "arm_thickness": 4.0,
    "arm_width": 8.0,
    "bumper_chamfer": 1.0,
    "bumper_height": 2.0,
    "bumper_width": 2.0,
    "cam_ramp_length": 35.0,
    "cam_ramp_rise": 10.0,
    "cam_ramp_thickness": 8.0,
    "cam_ramp_width": 10.0,
    "cam_sensitivity_ceiling_deg_per_mm": 15.0,
    "cam_target_tilt_deg": 45.0,
    "end_cap_thickness": 2.0,
    "gantry_x_travel": 250.0,
    "gantry_z_travel": 80.0,
    "max_overhang_deg": 50.0,
    "metadata": {},
    "min_wall": 0.8,
    "pin_clearance": 0.3,
    "pin_diameter": 3.0,
    "pivot_boss_diameter": 8.0,
    "pivot_boss_thickness": 4.0,
    "pivot_offset_y": -4.0,
    "powder_bulk_density": 1.0,
    "print_material_density": 1.27,
    "slot_board_height": 60.0,
    "slot_board_length": 220.0,
    "slot_board_thickness": 6.0,
    "slot_depth": 5.0,
    "slot_max_corner_deg": 60.0,
    "slot_path": [
      [
        10.0,
        30.0
      ],
      [
        140.0,
        30.0
      ],
      [
        170.0,
        24.0
      ],
      [
        200.0,
        12.0
      ],
      [
        210.0,
        12.0
      ]
    ],
    "slot_width": 4.2,
    "strike_off_length": 100.0,
    "strike_off_section": 4.0,
    "trough_length": 80.0,
    "trough_radius": 13.0,
    "trough_wall": 1.6
  }
}
```

=== file: docs/figures/panel-A-orthographic.svg ===
```svg
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 720" font-family="Helvetica, Arial, sans-serif" font-size="13">
  <defs>
    <linearGradient id="metal" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"   stop-color="#dfe4ea"/>
      <stop offset="0.5" stop-color="#aab2bd"/>
      <stop offset="1"   stop-color="#7e8794"/>
    </linearGradient>
    <linearGradient id="metalH" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0"   stop-color="#dfe4ea"/>
      <stop offset="0.5" stop-color="#aab2bd"/>
      <stop offset="1"   stop-color="#7e8794"/>
    </linearGradient>
    <pattern id="powder" width="6" height="6" patternUnits="userSpaceOnUse">
      <rect width="6" height="6" fill="#e8d9a8"/>
      <circle cx="1.5" cy="1.5" r="0.6" fill="#b89a55"/>
      <circle cx="4"   cy="3.5" r="0.6" fill="#b89a55"/>
      <circle cx="2"   cy="5"   r="0.5" fill="#b89a55"/>
    </pattern>
    <marker id="arrowK" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#222"/>
    </marker>
    <marker id="arrowB" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#1f5fbf"/>
    </marker>
    <marker id="arrowR" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#c0392b"/>
    </marker>
  </defs>
<text x="600" y="34" text-anchor="middle" font-size="22" font-weight="700">Subpanel A — Orthographic views (end, side, top)</text><text x="600" y="56" text-anchor="middle" font-size="13" fill="#555" font-style="italic">longitudinal pivot axis along L; arms grip the two short end caps; trough rolls SIDEWAYS to pour</text><g transform="translate(60,110)"><text x="160" y="0" text-anchor="middle" font-size="16" font-weight="600">End view (along L)</text><rect x="155" y="20" width="10" height="160" fill="url(#metal)" stroke="#333"/><rect x="158" y="22" width="10" height="160" fill="none" stroke="#888" stroke-width="1" stroke-dasharray="3 3"/><text x="170" y="35" font-size="11" fill="#444">arms (TWO, one per end cap;</text><text x="170" y="49" font-size="11" fill="#444">far arm shown dashed/hidden)</text><g transform="translate(160,180) rotate(0)">
  <path d="M -60 0 L 60 0 A 60 60 0 0 1 -60 0 Z" fill="url(#metal)" stroke="#222" stroke-width="2"/>
  <path d="M -59.1 9.0 L 59.1 9.0 A 59.1 59.1 0 0 1 -59.1 9.0 Z" fill="url(#powder)" opacity="0.95"/>
  <path d="M 60 0 L 66 -2 L 66 4 L 60 6 Z" fill="#7e8794" stroke="#222" stroke-width="1.2"/>
  <path d="M -60 0 L -66 -2 L -66 4 L -60 6 Z" fill="#7e8794" stroke="#222" stroke-width="1.2"/>
</g><circle cx="160" cy="180" r="7" fill="#c0392b" stroke="#7a1f15" stroke-width="1.5"/><line x1="155" y1="180" x2="165" y2="180" stroke="#fff" stroke-width="1.4"/><line x1="160" y1="175" x2="160" y2="185" stroke="#fff" stroke-width="1.4"/><text x="174" y="184" font-size="11" fill="#c0392b">pivot pin (axis ⊥ page = along L)</text><line x1="100" y1="270" x2="220" y2="270" stroke="#222" stroke-width="1.2" marker-start="url(#arrowK)" marker-end="url(#arrowK)"/><text x="160" y="290" text-anchor="middle" font-size="13">D ≈ 27 mm</text></g><g transform="translate(430,110)"><text x="200" y="0" text-anchor="middle" font-size="16" font-weight="600">Side view (along pin axis)</text><rect x="32" y="20" width="12" height="140" fill="url(#metal)" stroke="#333"/><rect x="356" y="20" width="12" height="140" fill="url(#metal)" stroke="#333"/><path d="M 60 140 L 340 140 L 340 150 Q 200.0 200 60 150 Z" fill="url(#metalH)" stroke="#222" stroke-width="2"/><path d="M 70 144 L 330 144 L 330 152 Q 200.0 194 70 152 Z" fill="url(#powder)" opacity="0.95"/><line x1="30" y1="148" x2="60" y2="148" stroke="#c0392b" stroke-width="3"/><line x1="60" y1="148" x2="340" y2="148" stroke="#c0392b" stroke-width="2.2" stroke-dasharray="6 4" opacity="0.7"/><line x1="340" y1="148" x2="370" y2="148" stroke="#c0392b" stroke-width="3"/><circle cx="38" cy="148" r="4" fill="#c0392b" stroke="#7a1f15" stroke-width="1.2"/><circle cx="362" cy="148" r="4" fill="#c0392b" stroke="#7a1f15" stroke-width="1.2"/><text x="200.0" y="142" text-anchor="middle" font-size="11" fill="#c0392b">pin stubs (red dots) sit in bushings on each arm — pin axis runs ALONG L</text><text x="200.0" y="174" text-anchor="middle" font-size="10" fill="#c0392b" font-style="italic">(dashed segment = pin hidden inside trough body)</text><line x1="60" y1="230" x2="340" y2="230" stroke="#222" stroke-width="1.2" marker-start="url(#arrowK)" marker-end="url(#arrowK)"/><text x="200.0" y="250" text-anchor="middle" font-size="13">L ≈ 3 D ≈ 80 mm</text><path d="M 60 140 L 340 140 L 340 135 L 60 135 Z" fill="#7e8794" stroke="#222" stroke-width="1.2"/><text x="200.0" y="128" text-anchor="middle" font-size="11" fill="#444">continuous chamfered lip (full length L; both long sides) — also rides cam ramp</text><text x="30" y="14" text-anchor="middle" font-size="10" fill="#444">arm L</text><text x="370" y="14" text-anchor="middle" font-size="10" fill="#444">arm R</text></g><g transform="translate(880,110)"><text x="130" y="0" text-anchor="middle" font-size="16" font-weight="600">Top view</text><rect x="20" y="40" width="220" height="50" fill="url(#metalH)" stroke="#222" stroke-width="2"/><rect x="26" y="46" width="208" height="38" fill="url(#powder)" opacity="0.95"/><line x1="0" y1="65.0" x2="20" y2="65.0" stroke="#c0392b" stroke-width="3"/><line x1="20" y1="65.0" x2="240" y2="65.0" stroke="#c0392b" stroke-width="2.2" stroke-dasharray="6 4" opacity="0.7"/><line x1="240" y1="65.0" x2="260" y2="65.0" stroke="#c0392b" stroke-width="3"/><text x="130.0" y="108" text-anchor="middle" font-size="11" fill="#c0392b">pivot pin axis (along centre line of trough length)</text><rect x="0" y="34" width="12" height="62" fill="url(#metal)" stroke="#333"/><circle cx="6" cy="65.0" r="4" fill="#c0392b" stroke="#7a1f15" stroke-width="1.2"/><rect x="248" y="34" width="12" height="62" fill="url(#metal)" stroke="#333"/><circle cx="254" cy="65.0" r="4" fill="#c0392b" stroke="#7a1f15" stroke-width="1.2"/><text x="-8" y="32" font-size="11" fill="#444">arms grip the two end caps via pin stubs</text><line x1="80.0" y1="140" x2="180.0" y2="140" stroke="#5a4a30" stroke-width="6"/><text x="130.0" y="160" text-anchor="middle" font-size="11" fill="#5a4a30">fixed strike-off bar (bed-edge mounted)</text></g><text x="600" y="660" text-anchor="middle" font-size="13" fill="#444" font-style="italic">The pivot pin runs along the trough's LONG axis L (not across its width).  Arms grip the two end caps,</text><text x="600" y="680" text-anchor="middle" font-size="13" fill="#444" font-style="italic">so when the trough rolls about the pin it pours over the FULL 80 mm long edge — eliminating the narrow-bottleneck</text><text x="600" y="700" text-anchor="middle" font-size="13" fill="#444" font-style="italic">and trapped-volume problems of an end-over-end tilt of a half-cylinder (Edison analysis-v2 §3).</text></svg>

```

=== file: docs/figures/panel-B-pivot-detail.svg ===
```svg
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600" font-family="Helvetica, Arial, sans-serif" font-size="13">
  <defs>
    <linearGradient id="metal" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"   stop-color="#dfe4ea"/>
      <stop offset="0.5" stop-color="#aab2bd"/>
      <stop offset="1"   stop-color="#7e8794"/>
    </linearGradient>
    <linearGradient id="metalH" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0"   stop-color="#dfe4ea"/>
      <stop offset="0.5" stop-color="#aab2bd"/>
      <stop offset="1"   stop-color="#7e8794"/>
    </linearGradient>
    <pattern id="powder" width="6" height="6" patternUnits="userSpaceOnUse">
      <rect width="6" height="6" fill="#e8d9a8"/>
      <circle cx="1.5" cy="1.5" r="0.6" fill="#b89a55"/>
      <circle cx="4"   cy="3.5" r="0.6" fill="#b89a55"/>
      <circle cx="2"   cy="5"   r="0.5" fill="#b89a55"/>
    </pattern>
    <marker id="arrowK" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#222"/>
    </marker>
    <marker id="arrowB" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#1f5fbf"/>
    </marker>
    <marker id="arrowR" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#c0392b"/>
    </marker>
  </defs>
<text x="450" y="34" text-anchor="middle" font-size="22" font-weight="700">Subpanel B — Pivot pin / end-cap detail (longitudinal axis)</text><text x="450" y="56" text-anchor="middle" font-size="13" fill="#555" font-style="italic">single horizontal pin runs ALONG L, through both end caps and both arms; quick-release to swap troughs</text><path d="M 220 320 L 480 320 A 130 130 0 0 1 220 320 Z" fill="url(#metal)" stroke="#222" stroke-width="2.5"/><text x="350" y="480" text-anchor="middle" font-size="12" fill="#444">trough end cap (cross-section, looking down L)</text><circle cx="350" cy="320" r="20" fill="#7e8794" stroke="#222" stroke-width="2"/><text x="378" y="296" font-size="11" fill="#444">pivot boss (printed</text><text x="378" y="308" font-size="11" fill="#444">into end cap)</text><rect x="342" y="120" width="16" height="180" fill="url(#metal)" stroke="#333"/><text x="368" y="160" font-size="12" fill="#444">arm (one of two; bolted to gantry carriage)</text><line x1="270" y1="320" x2="440" y2="320" stroke="#c0392b" stroke-width="6"/><circle cx="445" cy="320" r="6" fill="#c0392b" stroke="#7a1f15" stroke-width="1.5"/><text x="455" y="325" font-size="12" fill="#c0392b">pin (along L)</text><path d="M 450 302 q 14 18 0 36" fill="none" stroke="#c0392b" stroke-width="2"/><text x="460" y="350" font-size="11" fill="#c0392b">e-clip / retaining ring</text><line x1="343" y1="358" x2="357" y2="358" stroke="#222" stroke-width="1.6"/><line x1="350" y1="351" x2="350" y2="365" stroke="#222" stroke-width="1.6"/><circle cx="350" cy="358" r="9" fill="none" stroke="#222" stroke-width="1.2"/><text x="366" y="363" font-size="11" fill="#222">centre of mass (loaded)</text><text x="110" y="420" font-size="12" fill="#222">pivot pin sits ~3 mm above loaded COM</text><text x="110" y="436" font-size="12" fill="#222">→ gravity returns trough to "open-up" (stable pendulum)</text><text x="110" y="472" font-size="11" fill="#5a3a8a">metal pivot pin doubles as ground path for an</text><text x="110" y="488" font-size="11" fill="#5a3a8a">optional conductive (e.g. copper-tape) trough lining,</text><text x="110" y="504" font-size="11" fill="#5a3a8a">mitigating triboelectric charging on fine inorganic powders.</text></svg>

```

=== file: docs/figures/panel-C-isometric.svg ===
```svg
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 680" font-family="Helvetica, Arial, sans-serif" font-size="13">
  <defs>
    <linearGradient id="metal" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"   stop-color="#dfe4ea"/>
      <stop offset="0.5" stop-color="#aab2bd"/>
      <stop offset="1"   stop-color="#7e8794"/>
    </linearGradient>
    <linearGradient id="metalH" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0"   stop-color="#dfe4ea"/>
      <stop offset="0.5" stop-color="#aab2bd"/>
      <stop offset="1"   stop-color="#7e8794"/>
    </linearGradient>
    <pattern id="powder" width="6" height="6" patternUnits="userSpaceOnUse">
      <rect width="6" height="6" fill="#e8d9a8"/>
      <circle cx="1.5" cy="1.5" r="0.6" fill="#b89a55"/>
      <circle cx="4"   cy="3.5" r="0.6" fill="#b89a55"/>
      <circle cx="2"   cy="5"   r="0.5" fill="#b89a55"/>
    </pattern>
    <marker id="arrowK" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#222"/>
    </marker>
    <marker id="arrowB" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#1f5fbf"/>
    </marker>
    <marker id="arrowR" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#c0392b"/>
    </marker>
  </defs>
<text x="500" y="34" text-anchor="middle" font-size="22" font-weight="700">Subpanel C — 3D / isometric view of the assembly on a gantry</text><text x="500" y="56" text-anchor="middle" font-size="13" fill="#555" font-style="italic">two arms grip the two end caps via pin stubs (red dots); cam track on a fixed post drives the sideways tilt</text><rect x="180" y="80" width="640" height="22" fill="url(#metalH)" stroke="#222" stroke-width="1.5"/><text x="500" y="76" text-anchor="middle" font-size="12" fill="#444">gantry carriage (carries the two arms; X / Z stage)</text><polygon points="250,102 268,102 268,308 250,308" fill="url(#metal)" stroke="#333"/><polygon points="690,102 708,102 718,298 700,298" fill="url(#metal)" stroke="#333"/><text x="246" y="98" text-anchor="end" font-size="11" fill="#444">arm L</text><text x="722" y="98" text-anchor="start" font-size="11" fill="#444">arm R</text><polygon points="280,300 686,290 686,260 280,270" fill="#dfe4ea" stroke="#222" stroke-width="2"/><path d="M 280,270 C 350,420 616,410 686,260 L 686,290 C 616,440 350,450 280,300 Z" fill="url(#metalH)" stroke="#222" stroke-width="2"/><polygon points="286,295 680,287 680,265 286,275" fill="url(#powder)" opacity="0.95"/><line x1="268" y1="285" x2="280" y2="284" stroke="#c0392b" stroke-width="5"/><line x1="280" y1="284" x2="686" y2="276" stroke="#c0392b" stroke-width="3" stroke-dasharray="7 4" opacity="0.65"/><line x1="686" y1="276" x2="702" y2="275" stroke="#c0392b" stroke-width="5"/><circle cx="259" cy="286" r="6" fill="#c0392b" stroke="#7a1f15" stroke-width="1.5"/><circle cx="709" cy="274" r="6" fill="#c0392b" stroke="#7a1f15" stroke-width="1.5"/><line x1="259" y1="297" x2="220" y2="345" stroke="#c0392b" stroke-width="1"/><text x="214" y="357" text-anchor="end" font-size="11" fill="#c0392b">pin stub through end cap → bushing on arm L</text><line x1="709" y1="287" x2="750" y2="335" stroke="#c0392b" stroke-width="1"/><text x="754" y="347" text-anchor="start" font-size="11" fill="#c0392b">pin stub through end cap → bushing on arm R</text><text x="483" y="248" text-anchor="middle" font-size="11" fill="#c0392b" font-style="italic">(dashed segment = pin hidden inside trough body)</text><polygon points="286,272 680,262 680,254 286,264" fill="#7e8794" stroke="#222" stroke-width="1.2"/><text x="483" y="232" text-anchor="middle" font-size="11" fill="#444">continuous chamfered lip (full length L; both long sides) — also rides the cam ramp</text><rect x="850" y="180" width="18" height="320" fill="#8a7a5e" stroke="#444"/><text x="858" y="510" text-anchor="middle" font-size="11" fill="#5a4a30">fixed post</text><polygon points="730,300 850,300 850,250 730,300" fill="#8a7a5e" stroke="#444" stroke-width="1.5"/><text x="780" y="320" text-anchor="middle" font-size="12" fill="#5a4a30">smooth inclined cam track</text><text x="780" y="336" text-anchor="middle" font-size="11" fill="#7a6a4a">(replaces sawtooth; rim lip slides up its hypotenuse)</text><rect x="220" y="510" width="350" height="10" fill="#5a4a30" stroke="#222"/><text x="395" y="535" text-anchor="middle" font-size="11" fill="#5a4a30">fixed strike-off bar (bed-edge mounted; trough wipes under during the lift-out)</text><rect x="180" y="555" width="430" height="55" fill="url(#powder)" stroke="#7a5a1a"/><text x="395" y="595" text-anchor="middle" font-size="12" fill="#7a5a1a">powder bed</text><g transform="translate(880,590)"><rect x="-6" y="-46" width="100" height="64" fill="#fff" stroke="#aaa" stroke-width="1" rx="3"/><line x1="0" y1="0" x2="40" y2="0" stroke="#222" stroke-width="2" marker-end="url(#arrowK)"/><text x="44" y="4" font-size="10" fill="#222">L (pin axis)</text><line x1="0" y1="0" x2="0" y2="-30" stroke="#1f5fbf" stroke-width="2" marker-end="url(#arrowB)"/><text x="4" y="-32" font-size="10" fill="#1f5fbf">Z gantry</text><circle cx="0" cy="0" r="3" fill="#c0392b"/><circle cx="0" cy="0" r="6" fill="none" stroke="#c0392b"/><text x="-10" y="14" font-size="10" fill="#c0392b" text-anchor="end">X (out of page)</text></g></svg>

```

=== file: docs/figures/panel-D-mechanism.svg ===
```svg
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1860 600" font-family="Helvetica, Arial, sans-serif" font-size="13">
  <defs>
    <linearGradient id="metal" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"   stop-color="#dfe4ea"/>
      <stop offset="0.5" stop-color="#aab2bd"/>
      <stop offset="1"   stop-color="#7e8794"/>
    </linearGradient>
    <linearGradient id="metalH" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0"   stop-color="#dfe4ea"/>
      <stop offset="0.5" stop-color="#aab2bd"/>
      <stop offset="1"   stop-color="#7e8794"/>
    </linearGradient>
    <pattern id="powder" width="6" height="6" patternUnits="userSpaceOnUse">
      <rect width="6" height="6" fill="#e8d9a8"/>
      <circle cx="1.5" cy="1.5" r="0.6" fill="#b89a55"/>
      <circle cx="4"   cy="3.5" r="0.6" fill="#b89a55"/>
      <circle cx="2"   cy="5"   r="0.5" fill="#b89a55"/>
    </pattern>
    <marker id="arrowK" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#222"/>
    </marker>
    <marker id="arrowB" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#1f5fbf"/>
    </marker>
    <marker id="arrowR" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#c0392b"/>
    </marker>
  </defs>
<text x="930" y="34" text-anchor="middle" font-size="22" font-weight="700">Subpanel D — Mechanism of action (side view, 4 steps)</text><text x="930" y="56" text-anchor="middle" font-size="13" fill="#555" font-style="italic">all four frames share the same powder-bed line, pivot height and arm length so motion is comparable</text><g transform="translate(40,80)"><text x="200" y="0" text-anchor="middle" font-size="17" font-weight="600">1. J-curve plunge</text>
<line x1="0" y1="360" x2="400" y2="360" stroke="#bdb085" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="0" y="360" width="400" height="50" fill="url(#powder)" stroke="#7a5a1a"/>
<text x="200" y="424" text-anchor="middle" font-size="11" fill="#7a5a1a">powder bed</text>
<rect x="192" y="40" width="16" height="230" fill="url(#metal)" stroke="#333"/>
<circle cx="200" cy="270" r="7" fill="#c0392b" stroke="#7a1f15" stroke-width="1.5"/>
<g transform="translate(200,270) rotate(0)">
  <path d="M -38 0 L 38 0 A 38 38 0 0 1 -38 0 Z" fill="url(#metal)" stroke="#222" stroke-width="2"/>
  <path d="M -37.43 0.0 L 37.43 0.0 A 37.43 37.43 0 0 1 -37.43 0.0 Z" fill="url(#powder)" opacity="0.95"/>
  <path d="M 38 0 L 44 -2 L 44 4 L 38 6 Z" fill="#7e8794" stroke="#222" stroke-width="1.2"/>
  <path d="M -38 0 L -44 -2 L -44 4 L -38 6 Z" fill="#7e8794" stroke="#222" stroke-width="1.2"/>
</g>
<path d="M 60 60 L 60 210 Q 60 260 152 266" fill="none" stroke="#1f5fbf" stroke-width="3" marker-end="url(#arrowB)"/><text x="48" y="160" font-size="11" fill="#1f5fbf" transform="rotate(-90 48 160)" text-anchor="middle">Z ↓</text><text x="120" y="274" font-size="11" fill="#1f5fbf">then X →</text><text x="20" y="20" font-size="10" fill="#1f5fbf">J-curve avoids flat-blunt compaction</text></g><g transform="translate(500,80)"><text x="200" y="0" text-anchor="middle" font-size="17" font-weight="600">2. Lift past strike-off bar</text>
<line x1="0" y1="360" x2="400" y2="360" stroke="#bdb085" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="0" y="360" width="400" height="50" fill="url(#powder)" stroke="#7a5a1a"/>
<text x="200" y="424" text-anchor="middle" font-size="11" fill="#7a5a1a">powder bed</text>
<rect x="234" y="263" width="114" height="6" fill="#5a4a30" stroke="#222"/>
<text x="291" y="258" text-anchor="middle" font-size="10" fill="#5a4a30">strike-off bar</text>
<rect x="192" y="40" width="16" height="230" fill="url(#metal)" stroke="#333"/>
<circle cx="200" cy="270" r="7" fill="#c0392b" stroke="#7a1f15" stroke-width="1.5"/>
<g transform="translate(200,270) rotate(0)">
  <path d="M -38 0 L 38 0 A 38 38 0 0 1 -38 0 Z" fill="url(#metal)" stroke="#222" stroke-width="2"/>
  <path d="M -37.43 0.0 L 37.43 0.0 A 37.43 37.43 0 0 1 -37.43 0.0 Z" fill="url(#powder)" opacity="0.95"/>
  <path d="M 38 0 L 44 -2 L 44 4 L 38 6 Z" fill="#7e8794" stroke="#222" stroke-width="1.2"/>
  <path d="M -38 0 L -44 -2 L -44 4 L -38 6 Z" fill="#7e8794" stroke="#222" stroke-width="1.2"/>
</g>
<line x1="40" y1="300" x2="40" y2="80" stroke="#1f5fbf" stroke-width="3" marker-end="url(#arrowB)"/><text x="26" y="200" font-size="11" fill="#1f5fbf" transform="rotate(-90 26 200)" text-anchor="middle">Z ↑</text><text x="298" y="294" text-anchor="middle" font-size="10" fill="#5a4a30">rim wipes past bar → defines fill volume</text></g><g transform="translate(960,80)"><text x="200" y="0" text-anchor="middle" font-size="17" font-weight="600">3. Transport (X →)</text>
<line x1="0" y1="360" x2="400" y2="360" stroke="#bdb085" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="192" y="40" width="16" height="230" fill="url(#metal)" stroke="#333"/>
<circle cx="200" cy="270" r="7" fill="#c0392b" stroke="#7a1f15" stroke-width="1.5"/>
<g transform="translate(200,270) rotate(0)">
  <path d="M -38 0 L 38 0 A 38 38 0 0 1 -38 0 Z" fill="url(#metal)" stroke="#222" stroke-width="2"/>
  <path d="M -37.43 0.0 L 37.43 0.0 A 37.43 37.43 0 0 1 -37.43 0.0 Z" fill="url(#powder)" opacity="0.95"/>
  <path d="M 38 0 L 44 -2 L 44 4 L 38 6 Z" fill="#7e8794" stroke="#222" stroke-width="1.2"/>
  <path d="M -38 0 L -44 -2 L -44 4 L -38 6 Z" fill="#7e8794" stroke="#222" stroke-width="1.2"/>
</g>
<line x1="120" y1="120" x2="280" y2="120" stroke="#1f5fbf" stroke-width="3" marker-end="url(#arrowB)"/><text x="200" y="110" font-size="12" fill="#1f5fbf" text-anchor="middle">X →</text><text x="200" y="338" font-size="10" fill="#444" text-anchor="middle">trough hangs level under gravity</text></g><g transform="translate(1420,80)"><text x="200" y="0" text-anchor="middle" font-size="17" font-weight="600">4. Sideways tilt → deposit</text>
<line x1="0" y1="360" x2="400" y2="360" stroke="#bdb085" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="297.8" y="293.1" width="14" height="66.9" fill="#8a7a5e" stroke="#444"/>
<polygon points="221.8,301.1 291.8,360 297.8,360 297.8,293.1" fill="#8a7a5e" stroke="#444" stroke-width="1.5"/>
<text x="256.8" y="374" text-anchor="middle" font-size="10" fill="#5a4a30">smooth cam ramp</text>
<circle cx="221.8" cy="301.1" r="4" fill="#c0392b" stroke="#7a1f15" stroke-width="1.2"/>
<rect x="192" y="40" width="16" height="230" fill="url(#metal)" stroke="#333"/>
<circle cx="200" cy="270" r="7" fill="#c0392b" stroke="#7a1f15" stroke-width="1.5"/>
<g transform="translate(200,270) rotate(55)">
  <path d="M -38 0 L 38 0 A 38 38 0 0 1 -38 0 Z" fill="url(#metal)" stroke="#222" stroke-width="2"/>
  <path d="M -37.43 0.0 L 37.43 0.0 A 37.43 37.43 0 0 1 -37.43 0.0 Z" fill="url(#powder)" opacity="0.95"/>
  <path d="M 38 0 L 44 -2 L 44 4 L 38 6 Z" fill="#7e8794" stroke="#222" stroke-width="1.2"/>
  <path d="M -38 0 L -44 -2 L -44 4 L -38 6 Z" fill="#7e8794" stroke="#222" stroke-width="1.2"/>
</g>
<g fill="url(#powder)" opacity="0.95"><path d="M 215.79590458133976 301.1277776829817 Q 225.79590458133976 329.56388884149084 235.79590458133976 358 L 251.79590458133976 358 Q 247.79590458133976 329.56388884149084 235.79590458133976 297.1277776829817 Z"/></g>
<text x="233.79590458133976" y="374" text-anchor="middle" font-size="11" fill="#7a5a1a">powder pours over FULL long edge</text>
<line x1="20" y1="60" x2="80" y2="60" stroke="#1f5fbf" stroke-width="3" marker-end="url(#arrowB)"/><text x="50" y="52" text-anchor="middle" font-size="11" fill="#1f5fbf">gantry pushes X →</text><path d="M 140 280 a 36 36 0 0 1 38 -42" fill="none" stroke="#1f5fbf" stroke-width="2.5" marker-end="url(#arrowB)"/><text x="150" y="302" font-size="10" fill="#1f5fbf">trough rolls sideways</text><text x="150" y="316" font-size="10" fill="#1f5fbf">about its long axis</text><text x="242" y="226" font-size="10" fill="#c0392b">rim lip rides up cam</text></g><line x1="448" y1="350" x2="492" y2="350" stroke="#222" stroke-width="2.5" marker-end="url(#arrowK)"/><line x1="908" y1="350" x2="952" y2="350" stroke="#222" stroke-width="2.5" marker-end="url(#arrowK)"/><line x1="1368" y1="350" x2="1412" y2="350" stroke="#222" stroke-width="2.5" marker-end="url(#arrowK)"/><text x="930" y="550" text-anchor="middle" font-size="13" fill="#444" font-style="italic">Pure-X gantry travel works because the smooth cam ramp gives a continuously varying engagement point</text><text x="930" y="570" text-anchor="middle" font-size="13" fill="#444" font-style="italic">(unlike a fixed sawtooth tooth, which is kinematically incompatible with a horizontally-translating pivot — Edison v2 §1).</text></svg>

```

=== file: docs/figures/panel-E-pin-slot.svg ===
```svg
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 560" font-family="Helvetica, Arial, sans-serif" font-size="13">
  <defs>
    <linearGradient id="metal" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"   stop-color="#dfe4ea"/>
      <stop offset="0.5" stop-color="#aab2bd"/>
      <stop offset="1"   stop-color="#7e8794"/>
    </linearGradient>
    <linearGradient id="metalH" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0"   stop-color="#dfe4ea"/>
      <stop offset="0.5" stop-color="#aab2bd"/>
      <stop offset="1"   stop-color="#7e8794"/>
    </linearGradient>
    <pattern id="powder" width="6" height="6" patternUnits="userSpaceOnUse">
      <rect width="6" height="6" fill="#e8d9a8"/>
      <circle cx="1.5" cy="1.5" r="0.6" fill="#b89a55"/>
      <circle cx="4"   cy="3.5" r="0.6" fill="#b89a55"/>
      <circle cx="2"   cy="5"   r="0.5" fill="#b89a55"/>
    </pattern>
    <marker id="arrowK" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#222"/>
    </marker>
    <marker id="arrowB" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#1f5fbf"/>
    </marker>
    <marker id="arrowR" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#c0392b"/>
    </marker>
  </defs>
<text x="380" y="28" text-anchor="middle" font-size="15" font-weight="600">Pin-defined-path actuation (cam-slot variant)</text><text x="380" y="46" text-anchor="middle" font-size="11" fill="#555" font-style="italic">peg on top of stem rides in routed slot in a fixed external board; slot path = tilt schedule</text><rect x="60" y="100" width="640" height="56" fill="#e8e2cc" stroke="#7a6f4a" stroke-width="2" rx="3"/><text x="68" y="94" font-size="10" fill="#555">fixed external slot board (mounted to lab frame)</text><polyline points="90,144 260,144 430,144 520,132 600,112 680,112" fill="none" stroke="#3a342a" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/><polyline points="90,144 260,144 430,144 520,132 600,112 680,112" fill="none" stroke="#857a5a" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/><rect x="118" y="230" width="44" height="20" fill="#cfd8dc" stroke="#37474f" stroke-width="1.5" rx="2"/><text x="140" y="226" text-anchor="middle" font-size="10" fill="#37474f">carriage</text><circle cx="140" cy="240" r="3" fill="#222"/><g transform="translate(140,240) rotate(0.0)">  <line x1="0" y1="0" x2="0" y2="-96" stroke="#444" stroke-width="3"/>  <rect x="-9" y="-100" width="18" height="8" fill="#9aa0a6" stroke="#222" stroke-width="1.2" rx="1"/>  <line x1="0" y1="0" x2="0" y2="100" stroke="#444" stroke-width="3"/>  <g transform="translate(0,100) rotate(0.0)">
  <path d="M -38 0 L 38 0 A 38 38 0 0 1 -38 0 Z" fill="url(#metal)" stroke="#222" stroke-width="2"/>
  <path d="M -37.43 11.400000000000002 L 37.43 11.400000000000002 A 37.43 37.43 0 0 1 -37.43 11.400000000000002 Z" fill="url(#powder)" opacity="0.95"/>
</g></g><text x="140" y="438" text-anchor="middle" font-size="12" font-weight="600">Scoop</text><text x="140" y="454" text-anchor="middle" font-size="10" fill="#555">trough flat, peg in flat section of slot</text><rect x="358" y="230" width="44" height="20" fill="#cfd8dc" stroke="#37474f" stroke-width="1.5" rx="2"/><text x="380" y="226" text-anchor="middle" font-size="10" fill="#37474f">carriage</text><circle cx="380" cy="240" r="3" fill="#222"/><g transform="translate(380,240) rotate(0.0)">  <line x1="0" y1="0" x2="0" y2="-96" stroke="#444" stroke-width="3"/>  <rect x="-9" y="-100" width="18" height="8" fill="#9aa0a6" stroke="#222" stroke-width="1.2" rx="1"/>  <line x1="0" y1="0" x2="0" y2="100" stroke="#444" stroke-width="3"/>  <g transform="translate(0,100) rotate(0.0)">
  <path d="M -38 0 L 38 0 A 38 38 0 0 1 -38 0 Z" fill="url(#metal)" stroke="#222" stroke-width="2"/>
  <path d="M -37.43 11.400000000000002 L 37.43 11.400000000000002 A 37.43 37.43 0 0 1 -37.43 11.400000000000002 Z" fill="url(#powder)" opacity="0.95"/>
</g></g><text x="380" y="438" text-anchor="middle" font-size="12" font-weight="600">Transport</text><text x="380" y="454" text-anchor="middle" font-size="10" fill="#555">trough still flat (slot still flat)</text><rect x="618" y="230" width="44" height="20" fill="#cfd8dc" stroke="#37474f" stroke-width="1.5" rx="2"/><text x="640" y="226" text-anchor="middle" font-size="10" fill="#37474f">carriage</text><circle cx="640" cy="240" r="3" fill="#222"/><g transform="translate(640,240) rotate(0.0)">  <line x1="0" y1="0" x2="0" y2="-96" stroke="#444" stroke-width="3"/>  <rect x="-9" y="-100" width="18" height="8" fill="#9aa0a6" stroke="#222" stroke-width="1.2" rx="1"/>  <line x1="0" y1="0" x2="0" y2="100" stroke="#444" stroke-width="3"/>  <g transform="translate(0,100) rotate(45.0)">
  <path d="M -38 0 L 38 0 A 38 38 0 0 1 -38 0 Z" fill="url(#metal)" stroke="#222" stroke-width="2"/>
  <path d="M -37.43 28.5 L 37.43 28.5 A 37.43 37.43 0 0 1 -37.43 28.5 Z" fill="url(#powder)" opacity="0.95"/>
</g></g><text x="640" y="438" text-anchor="middle" font-size="12" font-weight="600">Pour</text><text x="640" y="454" text-anchor="middle" font-size="10" fill="#555">slot rises -> stem tilts -> trough rolls sideways</text><text x="170" y="180" text-anchor="middle" font-size="10" fill="#3a342a">flat slot section -> trough level</text><text x="555" y="86" text-anchor="middle" font-size="10" fill="#3a342a">rising slot section -> stem leans -> trough tilts</text><rect x="80" y="374" width="130" height="34" fill="url(#powder)" stroke="#7a6a3a" stroke-width="1.2"/><text x="145" y="424" text-anchor="middle" font-size="10" fill="#7a6a3a">stock powder bed</text><rect x="580" y="394" width="120" height="6" fill="#cfd8dc" stroke="#37474f" stroke-width="1"/><text x="640" y="416" text-anchor="middle" font-size="10" fill="#555">deposit / target plate</text><text x="380" y="540" text-anchor="middle" font-size="10" fill="#555" font-style="italic">See manuscript Sec. "Pin-defined-path actuation" for the trade-off vs. the smooth cam ramp.</text></svg>

```

=== file: docs/figures/cad/arm.svg ===
```svg
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   width="720.0"
   height="540.0"

>
    <g transform="scale(13.183080064992398, -13.183080064992398)   translate(4.794023831185496,-26.00707307249501)" stroke-width="0.4"  fill="none">
       <!-- hidden lines -->
       <g  stroke="rgb(180,180,180)" fill="none" stroke-dasharray="0.4,0.4" >
			<path d="M37.68466834387586,18.87643572992885 L31.13081297972354,20.900201653750194 " />
			<path d="M-3.2769276820761615,-0.7830046729070679 L31.130812979723537,20.900201653750194 " />
			<path d="M1.3517326688564162,-2.212289356605893 L1.4199601471251515,-2.165596776290685 L1.4799162445033054,-2.1167447857167097 L1.531251711950944,-2.0660179516178427 L1.5736675162837108,-2.0137117618407343 L1.5914512626462205,-1.9870613123242988 L1.606916582064927,-1.9601309041045845 L1.6200409446552666,-1.9329597694128833 L1.6308052308396797,-1.9055874911709225 L1.639193759201018,-1.8780539453264473 L1.6451943093272403,-1.8503992427619238 L1.648798139614117,-1.8226636708609822 L1.65,-1.794887634817747 " />
			<path d="M1.65,-1.7948876348177403 L1.648798139614117,-1.767111598774499 L1.6451943093272405,-1.7393760268735572 L1.639193759201018,-1.7117213243090335 L1.6308052308396797,-1.6841877784645587 L1.6200409446552666,-1.6568155002225977 L1.606916582064927,-1.6296443655308963 L1.5914512626462205,-1.6027139573111824 L1.5736675162837108,-1.5760635077947467 L1.5312517119509443,-1.5237573180176385 L1.4799162445033052,-1.473030483918771 L1.4199601471251515,-1.4241784933447956 L1.3517326688564175,-1.3774859130295887 " />
			<path d="M31.130812979723537,24.489976923385676 L31.130812979723537,20.900201653750194 " />
			<path d="M1.3517326688564164,0.41740172178815244 L1.4199601471251515,0.37070914147294454 L1.4799162445033052,0.32185715089896944 L1.531251711950944,0.2711303168001021 L1.5736675162837108,0.2188241270229937 L1.5914512626462205,0.19217367750655792 L1.606916582064927,0.1652432692868439 L1.6200409446552668,0.13807213459514242 L1.6308052308396799,0.11069985635318133 L1.639193759201018,0.08316631050870647 L1.6451943093272405,0.0555116079441826 L1.648798139614117,0.02777603604324113 L1.65,2.8961999753116498e-15 " />
			<path d="M1.65,-3.361587425872791e-16 L1.648798139614117,-0.027776036043241796 L1.6451943093272405,-0.05551160794418327 L1.639193759201018,-0.08316631050870714 L1.6308052308396797,-0.11069985635318198 L1.6200409446552666,-0.13807213459514278 L1.606916582064927,-0.16524326928684427 L1.5914512626462205,-0.1921736775065583 L1.5736675162837108,-0.21882412702299373 L1.5312517119509441,-0.27113031680010213 L1.4799162445033054,-0.3218571508989695 L1.4199601471251517,-0.3707091414729446 L1.3517326688564208,-0.4174017217881498 " />
			<path d="M1.65,1.7948876348177403 L1.65,0.0 " />
			<path d="M1.65,-1.7948876348177403 L1.65,0.0 " />

       </g>

       <!-- solid lines -->
       <g  stroke="rgb(40,40,40)" fill="none">
			<path d="M3.2769276820761615,0.7830046729070679 L3.2769276820761615,-2.8067705967284127 " />
			<path d="M3.2769276820761615,-2.8067705967284127 L37.68466834387586,18.87643572992885 " />
			<path d="M37.68466834387586,22.466210999564332 L37.68466834387586,18.87643572992885 " />
			<path d="M3.2769276820761615,0.7830046729070679 L37.68466834387586,22.466210999564332 " />
			<path d="M1.3517326688564166,1.377485913029588 L1.3517326688564166,-0.4174017217881523 " />
			<path d="M1.3517326688564166,-2.2122893566058925 L1.3517326688564166,-0.4174017217881523 " />
			<path d="M3.2769276820761615,-2.8067705967284127 L1.3517326688564166,-2.2122893566058925 " />
			<path d="M3.2769276820761615,0.7830046729070679 L1.3517326688564166,1.377485913029588 " />
			<path d="M-1.3517326688564166,-1.3774859130295878 L-3.2769276820761615,-0.7830046729070679 " />
			<path d="M1.3517326688564164,-1.377485913029588 L1.2925570552498862,-1.3424786753558648 L1.2287289503171297,-1.3090998600030401 L1.1604780999740918,-1.2774696122662696 L1.0880501695768496,-1.2477017835632864 L1.01170585966205,-1.2199035216321956 L0.931719967569,-1.1941748848588092 L0.8483803983210574,-1.1706084821217355 L0.7619871283266004,-1.1492891394515774 L0.6728511256296786,-1.1302935947040842 L0.5812932305968487,-1.1136902213462658 L0.4876430010691032,-1.0995387823496818 L0.3922375261357068,-1.0878902150767633 L0.29542021279970004,-1.078786447934446 L0.19753954990240313,-1.072260249455069 L0.09894785375610975,-1.0683351103477623 L9.054395166147101e-17,-1.0670251589448707 L-0.09894785375610957,-1.0683351103477623 L-0.1975395499024029,-1.072260249455069 L-0.2954202127996999,-1.078786447934446 L-0.3922375261357066,-1.0878902150767633 L-0.4876430010691029,-1.0995387823496818 L-0.5812932305968485,-1.1136902213462658 L-0.6728511256296784,-1.1302935947040842 L-0.7619871283266002,-1.1492891394515774 L-0.8483803983210573,-1.1706084821217355 L-0.9317199675689998,-1.194174884858809 L-1.0117058596620498,-1.2199035216321952 L-1.0880501695768496,-1.247701783563286 L-1.1604780999740916,-1.2774696122662692 L-1.2287289503171297,-1.3090998600030401 L-1.292557055249886,-1.3424786753558648 L-1.3517326688564122,-1.377485913029585 " />
			<path d="M37.68466834387586,22.466210999564332 L31.13081297972354,24.489976923385676 " />
			<path d="M-3.2769276820761615,2.8067705967284127 L31.130812979723537,24.489976923385676 " />
			<path d="M-1.3517326688564166,2.2122893566058925 L-3.2769276820761615,2.8067705967284127 " />
			<path d="M-1.3517326688564164,2.212289356605893 L-1.2727496300662022,2.2580956124481757 L-1.18580948481548,2.301005937225705 L-1.0914557744065685,2.3407520597762326 L-0.9902783890275547,2.3770854912209898 L-0.8829098798164148,2.4097790784929076 L-0.7700215042130386,2.4386284244754175 L-0.6523190293232337,2.463453165873276 L-0.5305383195316671,2.484098100826282 L-0.4054407359495552,2.500434159216156 L-0.27780837645931017,2.5123592096003255 L-0.14843918611491458,2.5197986977277322 L-0.018141968467328094,2.5227061126447348 L0.11226867099637018,2.5210632774770505 L0.24197741768697736,2.5148804630697983 L0.37017334518039924,2.504196323775179 L0.49605498505050494,2.489077655789238 L0.6188353375714976,2.4696189795485664 L0.7377467919633859,2.4459419487977576 L0.852045925419659,2.418194590022071 L0.9610181509141099,2.386550377000291 L1.0639821847291757,2.351207146263599 L1.1602943057752435,2.312385860240887 L1.249352380072074,2.270329225823218 L1.3305996252316725,2.2253001769840366 L1.4035280914074342,2.1775802309416266 L1.467681836947007,2.127467728140942 L1.5226597788950018,2.075275967058265 L1.5465981099042705,2.048501880217146 L1.568118200524479,2.0213312454897094 L1.5871864022260063,1.9938065465217536 L1.6037729002203776,1.9659708205692505 L1.6178517600782762,1.937867591205859 L1.6294009682802741,1.9095408002700394 L1.6384024666368797,1.8810347391581768 L1.644842180524085,1.8523939795711366 L1.6487100408902622,1.823663303822542 L1.65,1.7948876348177432 " />
			<path d="M1.65,1.7948876348177398 L1.648798139614117,1.7671115987744985 L1.6451943093272405,1.739376026873557 L1.639193759201018,1.7117213243090332 L1.6308052308396797,1.6841877784645582 L1.6200409446552666,1.6568155002225975 L1.606916582064927,1.629644365530896 L1.5914512626462205,1.602713957311182 L1.5736675162837108,1.5760635077947465 L1.5312517119509441,1.5237573180176383 L1.4799162445033054,1.473030483918771 L1.4199601471251517,1.4241784933447956 L1.3517326688564208,1.3774859130295904 " />
			<path d="M-1.3517326688564164,0.41740172178815255 L-1.2925570552498862,0.4524089594618754 L-1.2287289503171297,0.48578777481470026 L-1.1604780999740918,0.517418022551471 L-1.0880501695768496,0.5471858512544541 L-1.01170585966205,0.574984113185545 L-0.931719967569,0.6007127499589313 L-0.8483803983210574,0.6242791526960048 L-0.7619871283266004,0.6455984953661629 L-0.6728511256296786,0.664594040113656 L-0.5812932305968487,0.6811974134714746 L-0.48764300106910313,0.6953488524680584 L-0.3922375261357067,0.7069974197409769 L-0.2954202127997,0.7161011868832944 L-0.19753954990240308,0.7226273853626713 L-0.09894785375610972,0.7265525244699779 L-5.601161896658446e-17,0.7278624758728696 L0.0989478537561096,0.726552524469978 L0.19753954990240297,0.7226273853626713 L0.29542021279969993,0.7161011868832944 L0.39223752613570667,0.706997419740977 L0.48764300106910297,0.6953488524680584 L0.5812932305968485,0.6811974134714746 L0.6728511256296784,0.664594040113656 L0.7619871283266002,0.645598495366163 L0.8483803983210573,0.6242791526960049 L0.9317199675689998,0.6007127499589311 L1.0117058596620498,0.5749841131855448 L1.0880501695768496,0.547185851254454 L1.1604780999740916,0.5174180225514708 L1.2287289503171297,0.48578777481470015 L1.292557055249886,0.4524089594618754 L1.3517326688564122,0.4174017217881551 " />
			<path d="M-1.3517326688564166,0.4174017217881523 L-1.3517326688564166,2.2122893566058925 " />
			<path d="M-1.3517326688564166,0.4174017217881523 L-1.3517326688564166,-1.377485913029588 " />
			<path d="M-3.2769276820761615,2.8067705967284127 L-3.2769276820761615,-0.7830046729070679 " />

       </g>
    </g>
    
</svg>

```

=== file: docs/figures/cad/assembly-end.svg ===
```svg
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   width="900.0"
   height="600.0"

>
    <g transform="scale(6.373937677053824, -6.373937677053824)   translate(17.73777777777778,-59.13777777777778)" stroke-width="0.4"  fill="none">
       <!-- hidden lines -->
       <g  stroke="rgb(180,180,180)" fill="none" stroke-dasharray="0.4,0.4" >
			<path d="M4.0,0.0 L-2.1316282072803006e-14,0.0 " />
			<path d="M-2.1316282072803006e-14,0.0 L-4.000000000000002,0.0 " />
			<path d="M12.6,0.0 L-12.600000000000001,0.0 " />
			<path d="M-4.0,-4.0 L-3.996192886327431,-3.8255224505386565 L-3.984778792366982,-3.6513770290093683 L-3.965779445495242,-3.4778952311197955 L-3.9392310120488325,-3.305407289332281 L-3.9051840284797343,-3.1342415442475913 L-3.863703305156274,-2.9647238195899206 L-3.814867802992909,-2.7971768019829115 L-3.758770483143635,-2.63191942669733 L-3.695518130045149,-2.469266270539646 L-3.6252311481466024,-2.3095269530372082 L-3.54804333271289,-2.1530055470598706 L-3.4641016151377584,-2.000000000000006 L-3.373565783251547,-1.8508015666127116 L-3.276608177155972,-1.7056942545958225 L-3.1734133611649464,-1.564954283965125 L-3.0641777724759187,-1.42884956125385 L-2.9491093472405034,-1.297639169537367 L-2.828427124746198,-1.1715728752538177 L-2.70236083046265,-1.0508906527595117 L-2.5711504387461668,-0.9358222275240959 L-2.435045716034893,-0.8265866388350673 L-2.2943057454041957,-0.7233918228440408 L-2.1491984333873075,-0.6264342167484651 L-2.000000000000013,-0.5358983848622527 L-1.846994452940149,-0.45195666728712025 L-1.6904730469628113,-0.37476885185340647 L-1.5307337294603731,-0.3044818699548588 L-1.3680805733026895,-0.24122951685637162 L-1.2028231980171074,-0.18513219700709715 L-1.0352761804100985,-0.13629669484373075 L-0.8657584557524273,-0.0948159715202701 L-0.6945927106677374,-0.06076898795117058 L-0.5221047688802227,-0.03422055450476069 L-0.3486229709906493,-0.015221207633019151 L-0.1744775494613609,-0.0038071136725696952 L-1.712031933413185e-14,0.0 " />
			<path d="M-2.1561211432632476e-14,0.0 L0.17776742974531912,-0.003952109781247604 L0.35518358129171784,-0.015800629539130195 L0.5318978705852356,-0.03552214594823466 L0.7075611004902709,-0.06307768820960913 L0.8818261508222669,-0.09841280505920436 L1.0543486642762503,-0.1414576723665597 L1.2247877268957674,-0.19212723111111574 L1.3928065417375755,-0.2503213554635093 L1.5580730944008898,-0.31592505063970844 L1.7202608091060632,-0.38880868013701697 L1.879049194026254,-0.46882822190292117 L2.0341244745968656,-0.5558255529305685 L2.1851802135513116,-0.6496287617185104 L2.3319179164578747,-0.750052487977265 L2.4740476215610863,-0.8568982889114243 L2.6112884727620753,-0.9699550313535097 L2.7433692746056315,-1.0889993089747008 L2.8700290281773153,-1.2137958837480025 L2.991017446851636,-1.3440981507915017 L3.1060954508721625,-1.4796486256731471 L3.215035639786248,-1.6201794532141225 L3.317622741800802,-1.7654129367853826 L3.4136540391711745,-1.9150620870514334 L3.502939768782544,-2.068831189077014 L3.585303497132248,-2.22641638667604 L3.6605824689720716,-2.387506282848106 L3.72862792892155,-2.551782555116051 L3.7893054154167642,-2.718920584548646 L3.8424950264137756,-2.888590097225422 L3.8880916563216426,-3.060455816876064 L3.9260052036968403,-3.234178127404725 L3.956160749288656,-3.4094137439900756 L3.9784987040837443,-3.5858163914349497 L3.992974927057286,-3.7630374884251454 L3.9995608123980757,-3.940726836345233 L3.9982433460351774,-4.118533311290244 L3.98902513135444,-4.2961055579057765 L3.9719243840540672,-4.473092683685469 L3.9469748961493942,-4.649144952353847 L3.9142259691980144,-4.823914474964401 L3.873742316877192,-4.997055897347247 L3.8256039371060866,-5.168227082547913 L3.7699059539654716,-5.33708978690875 L3.706758429727329,-5.503310328456964 L3.6362861473657615,-5.666560246278504 L3.5586283639789826,-5.826516949574865 L3.473938535609649,-5.98286435512021 L3.382384014007296,-6.135293511859176 L3.284145715932094,-6.283503211411114 L3.1794177656534024,-6.427200583274388 L3.0684071113495532,-6.566101673554556 L2.9513331161668956,-6.699932006072856 L2.8284271247461756,-6.828427124746205 L2.6999320060728262,-6.951333116166923 L2.5661016735545235,-7.06840711134958 L2.427200583274356,-7.179417765653426 L2.2835032114110834,-7.284145715932116 L2.1352935118591456,-7.3823840140073145 L1.9828643551201806,-7.4739385356096655 L1.8265169495748357,-7.558628363978998 L1.6665602462784757,-7.636286147365775 L1.503310328456937,-7.706758429727341 L1.337089786908725,-7.7699059539654804 L1.1682270825478887,-7.825603937106094 L0.9970558973472237,-7.873742316877198 L0.8239144749643801,-7.914225969198019 L0.6491449523538271,-7.946974896149397 L0.4730926836854512,-7.97192438405407 L0.2961055579057602,-7.989025131354442 L0.1185333112902285,-7.998243346035178 L-0.05927316365478014,-7.999560812398076 L-0.23696251157486597,-7.9929749270572845 L-0.4141836085650597,-7.978498704083743 L-0.5905862560099321,-7.956160749288655 L-0.7658218725952806,-7.926005203696839 L-0.9395441831239402,-7.888091656321642 L-1.11140990277458,-7.842495026413776 L-1.2810794154513543,-7.789305415416765 L-1.4482174448839478,-7.728627928921551 L-1.612493717151891,-7.660582468972073 L-1.7735836133239555,-7.58530349713225 L-1.93116881092298,-7.5029397687825465 L-2.0849379129485595,-7.413654039171179 L-2.234587063214609,-7.3176227418008075 L-2.3798205467858677,-7.2150356397862545 L-2.520351374326842,-7.106095450872171 L-2.6559018492084867,-6.991017446851647 L-2.786204116251985,-6.870029028177328 L-2.9110006910252864,-6.743369274605645 L-3.0300449686464765,-6.611288472762091 L-3.1431017110885615,-6.474047621561104 L-3.249947512022721,-6.331917916457894 L-3.3503712382814754,-6.185180213551334 L-3.4441744470694173,-6.03412447459689 L-3.531171778097065,-5.87904919402628 L-3.6111913198629697,-5.720260809106091 L-3.684074949360279,-5.558073094400919 L-3.749678644536479,-5.392806541737606 L-3.807872768888874,-5.2247877268958 L-3.858542327633431,-5.054348664276284 L-3.9015871949407877,-4.8818261508223015 L-3.9369223117903847,-4.707561100490307 L-3.9644778540517605,-4.531897870585273 L-3.9841993704608663,-4.355183581291756 L-3.9960478902187506,-4.177767429745359 L-4.0,-4.000000000000019 " />
			<path d="M-12.6,0.0 L-12.6,2.0 " />
			<path d="M13.0,0.0 L12.6,0.0 " />
			<path d="M-13.0,0.0 L-12.99602274429008,-0.32154755463993434 L-12.984093410785396,-0.6428983589956069 L-12.964219298872072,-0.9638557831714003 L-12.936412569230885,-1.2842234379753237 L-12.90069023639634,-1.6038052950867085 L-12.8570741583457,-1.9224058070030963 L-12.805591023124423,-2.2398300266929168 L-12.74627233251613,-2.555883726880751 L-12.679154382767114,-2.8703735188921806 L-12.604278242377205,-3.1831069709855155 L-12.521689726970543,-3.4938927260979837 L-12.431439371261657,-3.8025406189343416 L-12.333582398134025,-4.108861792326259 L-12.22817868484997,-4.412668812791285 L-12.11529272641265,-4.713775785220671 L-11.994993596102487,-5.011998466625896 L-11.86735490321224,-5.307154378874275 L-11.73245474800654,-5.599062920344686 L-11.590375673933476,-5.887545476435074 L-11.44120461711745,-6.172425528854146 L-11.285032853164223,-6.4535287636303424 L-11.121955941310706,-6.7306831777720335 L-10.952073665953646,-7.003719184513655 L-10.77548997559299,-7.272469717083389 L-10.592312919227316,-7.536770330928894 L-10.402654580240222,-7.796459304338546 L-10.206631007818116,-8.05137773739661 L-10.004362145941409,-8.301369649211784 L-9.795971759992543,-8.546282073359652 L-9.581587361025733,-8.785965151480621 L-9.36134012774481,-9.020272224976072 L-9.135364826236875,-9.249059924746627 L-8.903799727510888,-9.47218825891763 L-8.666786522891636,-9.68952069849814 L-8.424470237320872,-9.900924260921038 L-8.176999140618658,-10.10626959141313 L-7.924524656759209,-10.305431042145463 L-7.6672012712167605,-10.498286749115403 L-7.405186436438152,-10.684718706713454 L-7.138640475499951,-10.86461283992917 L-6.867726484009096,-11.037859074152017 L-6.5926102303070575,-11.20435140252441 L-6.313460054038595,-11.363987950805779 L-6.030446763147168,-11.51667103970795 L-5.743743529360033,-11.662307244663669 L-5.453525782226983,-11.800807452991746 L-5.159971101777539,-11.93208691842381 L-4.863259109862316,-12.05606531295933 L-4.563571360245013,-12.172666776017136 L-4.261091227512301,-12.281819960853428 L-3.9560037948695723,-12.38345807821779 L-3.648495740891212,-12.477518937220598 L-3.3387552252946846,-12.563944983386683 L-3.0269717738083393,-12.642683333872107 L-2.713336162203356,-12.713685809822401 L-2.398040299560826,-12.776908965852508 L-2.0812771108453654,-12.832314116630371 L-1.763240418857131,-12.879867360547953 L-1.444124825634456,-12.91953960046511 L-1.1241255933796905,-12.951306561513734 L-0.8034385249810885,-12.975148805951173 L-0.4822598442038635,-12.991051745053916 L-0.16078607562371153,-12.999005648044218 L0.16078607562372502,-12.999005648044218 L0.4822598442038769,-12.991051745053916 L0.803438524981102,-12.975148805951173 L1.1241255933797039,-12.951306561513734 L1.4441248256344696,-12.919539600465109 L1.7632404188571442,-12.879867360547951 L2.0812771108453787,-12.83231411663037 L2.3980402995608388,-12.776908965852504 L2.713336162203369,-12.713685809822401 L3.026971773808352,-12.642683333872105 L3.3387552252946984,-12.56394498338668 L3.648495740891225,-12.477518937220596 L3.956003794869585,-12.383458078217789 L4.261091227512314,-12.281819960853422 L4.563571360245025,-12.172666776017133 L4.863259109862328,-12.056065312959326 L5.159971101777551,-11.932086918423808 L5.4535257822269925,-11.800807452991743 L5.743743529360044,-11.662307244663664 L6.030446763147178,-11.516671039707946 L6.313460054038606,-11.363987950805775 L6.592610230307067,-11.204351402524402 L6.867726484009105,-11.03785907415201 L7.138640475499961,-10.864612839929164 L7.4051864364381625,-10.684718706713443 L7.667201271216773,-10.498286749115394 L7.924524656759222,-10.305431042145452 L8.176999140618673,-10.106269591413117 L8.424470237320888,-9.900924260921023 L8.666786522891652,-9.689520698498127 L8.903799727510904,-9.472188258917614 L9.135364826236891,-9.24905992474661 L9.361340127744826,-9.020272224976054 L9.58158736102575,-8.785965151480603 L9.795971759992561,-8.546282073359633 L10.004362145941428,-8.301369649211761 L10.206631007818133,-8.051377737396585 L10.402654580240242,-7.796459304338521 L10.592312919227338,-7.536770330928867 L10.775489975593011,-7.272469717083361 L10.952073665953666,-7.003719184513626 L11.121955941310727,-6.730683177772002 L11.285032853164239,-6.453528763630309 L11.441204617117466,-6.172425528854111 L11.590375673933494,-5.887545476435038 L11.732454748006557,-5.5990629203446485 L11.867354903212256,-5.3071543788742375 L11.994993596102502,-5.011998466625857 L12.115292726412664,-4.713775785220632 L12.228178684849984,-4.412668812791244 L12.333582398134038,-4.108861792326217 L12.43143937126167,-3.802540618934298 L12.521689726970552,-3.4938927260979398 L12.604278242377216,-3.1831069709854707 L12.679154382767123,-2.8703735188921344 L12.746272332516138,-2.5558837268807038 L12.805591023124432,-2.239830026692869 L12.857074158345707,-1.9224058070030472 L12.900690236396345,-1.6038052950866588 L12.93641256923089,-1.2842234379752733 L12.964219298872074,-0.9638557831713491 L12.9840934107854,-0.6428983589955546 L12.996022744290082,-0.3215475546398813 L13.0,5.391911039236627e-14 " />
			<path d="M-12.600000000000001,0.0 L-13.0,0.0 " />
			<path d="M-1.65,-4.0 L-1.6460684992970585,-4.113835388267136 L-1.6342927325794792,-4.227128299068828 L-1.6147288167383262,-4.339338840091795 L-1.587469982741941,-4.449932277007664 L-1.552646131347921,-4.558381581725556 L-1.5104232140668543,-4.664169943920946 L-1.4610024423277963,-4.766793233872218 L-1.4046193286141795,-4.865762404868363 L-1.3415425641395786,-4.960605823739272 L-1.2720727384117165,-5.050871518402567 L-1.1965409067865713,-5.136129331716407 L-1.115307012838845,-5.215972971374155 L-1.0287581730669106,-5.290021946072249 L-0.9373068321064074,-5.357923378724532 L-0.8413887972437247,-5.419353688082276 L-0.7414611615958165,-5.474020130746179 L-0.6380001258533414,-5.521662196221987 L-0.5314987289675097,-5.562052848371629 L-0.4224644985949529,-5.594999607343812 L-0.31141703249731256,-5.62034546682816 L-0.19888552242128296,-5.637969642261789 L-0.0854062322589453,-5.647788146422752 L0.028480057493891313,-5.6497541896674015 L0.1422306268030224,-5.6438584029043435 L0.25530340240396454,-5.630128882242431 L0.36715954102791937,-5.608631055100009 L0.47726599723533725,-5.579467368413466 L0.5850980636201846,-5.542776800430934 L0.6901418712796834,-5.498734198417644 L0.7918968386336483,-5.447549445429079 L0.8898780569236795,-5.389466460122638 L0.9836186010242227,-5.324762034374155 L1.072671754553429,-5.253744514238554 L1.1566131386801475,-5.176752330540483 L1.2350427344823178,-5.094152386097311 L1.3075867892193,-5.006338307260119 L1.3738995974338915,-4.913728568104878 L1.4336651483962617,-4.816764496212907 L1.4865986320389923,-4.715908169543969 L1.5324477962067495,-4.61164021442436 L1.5709941487526788,-4.50445751514359 L1.6020539987529863,-4.394870846074468 L1.625479331877842,-4.2834024376006035 L1.641158515747068,-4.170583487450808 L1.6490168319092662,-4.056951629300015 L1.6490168319092662,-3.943048370699979 L1.6411585157470676,-3.8294165125491864 L1.625479331877841,-3.7165975623993917 L1.602053998752985,-3.605129153925527 L1.5709941487526773,-3.4955424848564047 L1.5324477962067475,-3.3883597855756356 L1.4865986320389901,-3.284091830456026 L1.433665148396259,-3.1832355037870874 L1.3738995974338883,-3.0862714318951174 L1.3075867892192967,-2.993661692739877 L1.235042734482314,-2.9058476139026848 L1.1566131386801437,-2.8232476694595134 L1.0726717545534254,-2.7462554857614427 L0.983618601024219,-2.6752379656258416 L0.8898780569236757,-2.610533539877359 L0.7918968386336441,-2.5524505545709193 L0.6901418712796791,-2.5012658015823543 L0.5850980636201801,-2.4572231995690643 L0.47726599723533275,-2.420532631586533 L0.36715954102791476,-2.39136894489999 L0.2553034024039599,-2.369871117757568 L0.1422306268030177,-2.356141597095656 L0.028480057493886587,-2.3502458103325985 L-0.08540623225895001,-2.3522118535772476 L-0.19888552242128765,-2.3620303577382114 L-0.31141703249731717,-2.379654533171841 L-0.42246449859495744,-2.405000392656189 L-0.5314987289675142,-2.437947151628372 L-0.6380001258533458,-2.478337803778015 L-0.7414611615958208,-2.525979869253823 L-0.8413887972437287,-2.5806463119177265 L-0.9373068321064114,-2.64207662127547 L-1.0287581730669146,-2.7099780539277543 L-1.1153070128388487,-2.7840270286258484 L-1.196540906786575,-2.863870668283597 L-1.2720727384117199,-2.9491284815974375 L-1.3415425641395822,-3.0393941762607333 L-1.4046193286141826,-3.134237595131642 L-1.4610024423277992,-3.2332067661277875 L-1.510423214066857,-3.3358300560790592 L-1.5526461313479232,-3.44161841827445 L-1.5874699827419425,-3.5500677229923414 L-1.6147288167383274,-3.6606611599082113 L-1.63429273257948,-3.772871700931179 L-1.646068499297059,-3.8861646117328705 L-1.65,-4.000000000000007 " />
			<path d="M12.6,0.0 L12.6,2.0 " />
			<path d="M-12.6,2.0 L-13.6,2.0 " />
			<path d="M-14.6,0.9999999999999999 L-13.6,2.0 " />
			<path d="M-14.6,0.0 L-14.6,1.0 " />
			<path d="M-14.600000000000001,0.0 L-14.596046921220143,-0.3397267630612223 L-14.58418982554246,-0.6792695580871011 L-14.564435133793435,-1.0184445166642293 L-14.536793543487146,-1.3570679695691261 L-14.50128002303237,-1.6949565462283613 L-14.457913803626928,-2.0319272740169554 L-14.406718368843658,-2.3677976773412843 L-14.347721441913636,-2.702385876452833 L-14.280954970713564,-3.0355106859392853 L-14.206455110465429,-3.3669917128396256 L-14.124262204157814,-3.696649454330105 L-14.034420760699458,-4.024305394928187 L-13.936979430816887,-4.349782103161837 L-13.83199098070921,-4.672903327651785 L-13.719512263474265,-4.993494092554764 L-13.59960418832168,-5.311380792316013 L-13.47233168758946,-5.6263912856797464 L-13.337763681581974,-5.938354988906684 L-13.1959730412484,-6.247102968148154 L-13.04703654872182,-6.552468030926749 L-12.891034855740333,-6.8542848166740065 L-12.72805243997273,-7.152389886276072 L-12.558177559272334,-7.44662181057886 L-12.381502203883818,-7.736821257804793 L-12.198122046628873,-8.022831079833768 L-12.008136391097668,-8.304496397301635 L-11.811648117874233,-8.581664683470107 L-11.608763628824779,-8.854185846822675 L-11.399592789479227,-9.121912312341816 L-11.18424886953708,-9.384699101423472 L-10.96284848152989,-9.64240391038551 L-10.735511517673501,-9.894887187527688 L-10.50236108494431,-10.142012208701358 L-10.263523438414664,-10.383645151347999 L-10.019127912883514,-10.619655166966508 L-9.769306852839334,-10.849914451969951 L-9.514195540793251,-11.074298316893481 L-9.253932124021174,-11.29268525391587 L-8.988657539754616,-11.504957002658136 L-8.718515438860685,-11.710998614223636 L-8.44365210805261,-11.910698513444906 L-8.164216390672912,-12.103948559303603 L-7.880359606092095,-12.290644103490754 L-7.592235467766553,-12.470684047075668 L-7.300000000000009,-12.6439708952528 L-7.003811453453604,-12.81041081013689 L-6.70383021945038,-12.969913661577854 L-6.400218743120541,-13.122393075967832 L-6.0931414354345526,-13.26776648301403 L-5.7827645841717015,-13.405955160451995 L-5.469256263872329,-13.536884276675089 L-5.152786244822499,-13.660482931257153 L-4.833525901120402,-13.776684193346314 L-4.5116481178742465,-13.885425137909236 L-4.187327197581934,-13.986646879806132 L-3.860738765743169,-14.080294605678104 L-3.5320596757551654,-14.166317603629544 L-3.201467913143406,-14.244669290689524 L-2.869142499179338,-14.315307238037294 L-2.535263393937202,-14.378193193978234 L-2.2000113988424728,-14.433293104657828 L-1.8635680587647014,-14.480577132502416 L-1.5261155637077612,-14.520019672376788 L-1.1878366501507522,-14.551599365449787 L-0.848914502092969,-14.575299110760513 L-0.5095326518565367,-14.591106074478796 L-0.16987488070041956,-14.599011696854928 L0.16987488070037268,-14.59901169685493 L0.50953265185649,-14.591106074478798 L0.8489145020929222,-14.575299110760517 L1.1878366501507056,-14.551599365449789 L1.5261155637077148,-14.520019672376792 L1.8635680587646546,-14.480577132502424 L2.2000113988424266,-14.433293104657833 L2.535263393937156,-14.378193193978243 L2.869142499179292,-14.315307238037304 L3.20146791314336,-14.244669290689535 L3.53205967575512,-14.166317603629556 L3.8607387657431236,-14.080294605678118 L4.187327197581888,-13.986646879806147 L4.511648117874203,-13.885425137909252 L4.833525901120358,-13.77668419334633 L5.152786244822456,-13.660482931257171 L5.4692562638722855,-13.536884276675108 L5.782764584171659,-13.405955160452015 L6.0931414354345135,-13.267766483014052 L6.400218743120505,-13.122393075967851 L6.703830219450348,-12.969913661577873 L7.003811453453575,-12.810410810136908 L7.299999999999983,-12.643970895252814 L7.592235467766531,-12.47068404707568 L7.880359606092076,-12.290644103490767 L8.164216390672895,-12.103948559303616 L8.443652108052596,-11.910698513444917 L8.718515438860672,-11.710998614223643 L8.988657539754607,-11.504957002658141 L9.25393212402117,-11.292685253915874 L9.514195540793247,-11.074298316893485 L9.769306852839334,-10.849914451969953 L10.019127912883516,-10.619655166966506 L10.263523438414667,-10.383645151347995 L10.502361084944315,-10.14201220870135 L10.735511517673508,-9.89488718752768 L10.962848481529901,-9.6424039103855 L11.184248869537093,-9.38469910142346 L11.39959278947924,-9.1219123123418 L11.608763628824793,-8.854185846822656 L11.81164811787425,-8.581664683470086 L12.008136391097688,-8.30449639730161 L12.19812204662889,-8.022831079833741 L12.381502203883839,-7.736821257804762 L12.558177559272355,-7.446621810578826 L12.72805243997275,-7.152389886276034 L12.891034855740353,-6.854284816673967 L13.04703654872184,-6.552468030926707 L13.19597304124842,-6.247102968148108 L13.337763681581993,-5.938354988906636 L13.47233168758948,-5.626391285679696 L13.599604188321699,-5.311380792315959 L13.719512263474282,-4.993494092554707 L13.831990980709229,-4.672903327651726 L13.936979430816907,-4.349782103161776 L14.034420760699476,-4.024305394928124 L14.124262204157832,-3.6966494543300374 L14.206455110465445,-3.366991712839556 L14.280954970713578,-3.0355106859392125 L14.347721441913649,-2.7023858764527566 L14.40671836884367,-2.3677976773412053 L14.457913803626939,-2.0319272740168732 L14.501280023032379,-1.694956546228276 L14.536793543487153,-1.3570679695690382 L14.564435133793442,-1.0184445166641387 L14.584189825542463,-0.6792695580870075 L14.596046921220145,-0.339726763061126 L14.600000000000001,9.90202663092091e-14 " />
			<path d="M14.6,0.0 L14.6,1.0 " />
			<path d="M14.6,1.0 L13.6,2.0 " />
			<path d="M13.6,2.0 L12.6,2.0 " />
			<path d="M-4.0,-4.0 L-3.9960849060798944,-3.8230666130984847 L-3.9843472882997792,-3.64647958161063 L-3.9648101235976583,-3.4705845829431103 L-3.9375116568909023,-3.2957259398158554 L-3.902505326210027,-3.122245946234158 L-3.85985965809124,-2.9504841974320835 L-3.8096581334325257,-2.780776925098854 L-3.75199902407587,-2.613456339189523 L-3.6869952004355135,-2.4488499776083916 L-3.6147739105488155,-2.2872800650381793 L-3.5354765309822445,-2.1290628821700732 L-3.4492582900801114,-1.9745081465694247 L-3.356287964097795,-1.8239184063890712 L-3.2567475468142972,-1.6775884481171177 L-3.1508318932708734,-1.5358047195185436 L-3.03874833833314,-1.3988447689002528 L-2.9207162908233375,-1.2669767017972267 L-2.7969668040172566,-1.1404586561433505 L-2.6677421233466037,-1.0195382969542863 L-2.5332952121921886,-0.9044523315115733 L-2.39388925669623,-0.795426045997008 L-2.2497971505631233,-0.6926728644843658 L-2.101300960857196,-0.5963939311517521 L-1.9486913758431865,-0.5067777165324294 L-1.7922671359503142,-0.42399964857489714 L-1.6323344489738596,-0.34822176923444514 L-1.4692063906590267,-0.279592417268415 L-1.303202291840469,-0.21824593785611857 L-1.1346471133371856,-0.16430241961183922 L-0.963870809826456,-0.1178674595057303 L-0.791207683942067,-0.07903195615278813 L-0.6169957318612068,-0.04787193187454353 L-0.4415759816610762,-0.024448383881797042 L-0.2652918257404126,-0.008807164869715667 L-0.08848834861274403,-0.000978893259028002 L0.08848834861275154,-0.000978893259028002 L0.2652918257404201,-0.008807164869716111 L0.4415759816610837,-0.024448383881797486 L0.6169957318612143,-0.047871931874544416 L0.7912076839420744,-0.0790319561527899 L0.9638708098264632,-0.11786745950573208 L1.1346471133371927,-0.16430241961184144 L1.3032022918404762,-0.2182459378561208 L1.4692063906590338,-0.27959241726841766 L1.6323344489738665,-0.34822176923444825 L1.79226713595032,-0.42399964857490025 L1.9486913758431916,-0.5067777165324321 L2.1013009608572,-0.5963939311517548 L2.249797150563127,-0.692672864484368 L2.3938892566962333,-0.7954260459970106 L2.5332952121921912,-0.9044523315115756 L2.667742123346606,-1.0195382969542885 L2.796966804017259,-1.1404586561433523 L2.920716290823339,-1.266976701797228 L3.0387483383331415,-1.398844768900254 L3.1508318932708743,-1.535804719518545 L3.2567475468142977,-1.6775884481171182 L3.356287964097795,-1.8239184063890717 L3.4492582900801114,-1.9745081465694247 L3.5354765309822445,-2.1290628821700723 L3.614773910548815,-2.2872800650381784 L3.686995200435513,-2.4488499776083903 L3.7519990240758694,-2.613456339189521 L3.809658133432525,-2.780776925098851 L3.859859658091239,-2.950484197432081 L3.9025053262100267,-3.1222459462341545 L3.937511656890902,-3.2957259398158514 L3.964810123597658,-3.470584582943106 L3.984347288299779,-3.6464795816106252 L3.996084906079894,-3.8230666130984794 L4.0,-3.9999999999999942 " />
			<path d="M-12.600000000000001,0.0 L-13.0,0.0 " />
			<path d="M12.6,0.0 L-12.600000000000001,0.0 " />
			<path d="M-2.1316282072803006e-14,0.0 L-12.6,0.0 " />
			<path d="M12.6,0.0 L-2.1316282072803006e-14,0.0 " />
			<path d="M-4.0,-4.0 L-3.996192886327431,-3.8255224505386565 L-3.984778792366982,-3.6513770290093683 L-3.965779445495242,-3.4778952311197955 L-3.9392310120488325,-3.305407289332281 L-3.9051840284797343,-3.1342415442475913 L-3.863703305156274,-2.9647238195899206 L-3.814867802992909,-2.7971768019829115 L-3.758770483143635,-2.63191942669733 L-3.695518130045149,-2.469266270539646 L-3.6252311481466024,-2.3095269530372082 L-3.54804333271289,-2.1530055470598706 L-3.4641016151377584,-2.000000000000006 L-3.373565783251547,-1.8508015666127116 L-3.276608177155972,-1.7056942545958225 L-3.1734133611649464,-1.564954283965125 L-3.0641777724759187,-1.42884956125385 L-2.9491093472405034,-1.297639169537367 L-2.828427124746198,-1.1715728752538177 L-2.70236083046265,-1.0508906527595117 L-2.5711504387461668,-0.9358222275240959 L-2.435045716034893,-0.8265866388350673 L-2.2943057454041957,-0.7233918228440408 L-2.1491984333873075,-0.6264342167484651 L-2.000000000000013,-0.5358983848622527 L-1.846994452940149,-0.45195666728712025 L-1.6904730469628113,-0.37476885185340647 L-1.5307337294603731,-0.3044818699548588 L-1.3680805733026895,-0.24122951685637162 L-1.2028231980171074,-0.18513219700709715 L-1.0352761804100985,-0.13629669484373075 L-0.8657584557524273,-0.0948159715202701 L-0.6945927106677374,-0.06076898795117058 L-0.5221047688802227,-0.03422055450476069 L-0.3486229709906493,-0.015221207633019151 L-0.1744775494613609,-0.0038071136725696952 L-1.712031933413185e-14,0.0 " />
			<path d="M-2.1561211432632476e-14,0.0 L0.17776742974531912,-0.003952109781247604 L0.35518358129171784,-0.015800629539130195 L0.5318978705852356,-0.03552214594823466 L0.7075611004902709,-0.06307768820960913 L0.8818261508222669,-0.09841280505920436 L1.0543486642762503,-0.1414576723665597 L1.2247877268957674,-0.19212723111111574 L1.3928065417375755,-0.2503213554635093 L1.5580730944008898,-0.31592505063970844 L1.7202608091060632,-0.38880868013701697 L1.879049194026254,-0.46882822190292117 L2.0341244745968656,-0.5558255529305685 L2.1851802135513116,-0.6496287617185104 L2.3319179164578747,-0.750052487977265 L2.4740476215610863,-0.8568982889114243 L2.6112884727620753,-0.9699550313535097 L2.7433692746056315,-1.0889993089747008 L2.8700290281773153,-1.2137958837480025 L2.991017446851636,-1.3440981507915017 L3.1060954508721625,-1.4796486256731471 L3.215035639786248,-1.6201794532141225 L3.317622741800802,-1.7654129367853826 L3.4136540391711745,-1.9150620870514334 L3.502939768782544,-2.068831189077014 L3.585303497132248,-2.22641638667604 L3.6605824689720716,-2.387506282848106 L3.72862792892155,-2.551782555116051 L3.7893054154167642,-2.718920584548646 L3.8424950264137756,-2.888590097225422 L3.8880916563216426,-3.060455816876064 L3.9260052036968403,-3.234178127404725 L3.956160749288656,-3.4094137439900756 L3.9784987040837443,-3.5858163914349497 L3.992974927057286,-3.7630374884251454 L3.9995608123980757,-3.940726836345233 L3.9982433460351774,-4.118533311290244 L3.98902513135444,-4.2961055579057765 L3.9719243840540672,-4.473092683685469 L3.9469748961493942,-4.649144952353847 L3.9142259691980144,-4.823914474964401 L3.873742316877192,-4.997055897347247 L3.8256039371060866,-5.168227082547913 L3.7699059539654716,-5.33708978690875 L3.706758429727329,-5.503310328456964 L3.6362861473657615,-5.666560246278504 L3.5586283639789826,-5.826516949574865 L3.473938535609649,-5.98286435512021 L3.382384014007296,-6.135293511859176 L3.284145715932094,-6.283503211411114 L3.1794177656534024,-6.427200583274388 L3.0684071113495532,-6.566101673554556 L2.9513331161668956,-6.699932006072856 L2.8284271247461756,-6.828427124746205 L2.6999320060728262,-6.951333116166923 L2.5661016735545235,-7.06840711134958 L2.427200583274356,-7.179417765653426 L2.2835032114110834,-7.284145715932116 L2.1352935118591456,-7.3823840140073145 L1.9828643551201806,-7.4739385356096655 L1.8265169495748357,-7.558628363978998 L1.6665602462784757,-7.636286147365775 L1.503310328456937,-7.706758429727341 L1.337089786908725,-7.7699059539654804 L1.1682270825478887,-7.825603937106094 L0.9970558973472237,-7.873742316877198 L0.8239144749643801,-7.914225969198019 L0.6491449523538271,-7.946974896149397 L0.4730926836854512,-7.97192438405407 L0.2961055579057602,-7.989025131354442 L0.1185333112902285,-7.998243346035178 L-0.05927316365478014,-7.999560812398076 L-0.23696251157486597,-7.9929749270572845 L-0.4141836085650597,-7.978498704083743 L-0.5905862560099321,-7.956160749288655 L-0.7658218725952806,-7.926005203696839 L-0.9395441831239402,-7.888091656321642 L-1.11140990277458,-7.842495026413776 L-1.2810794154513543,-7.789305415416765 L-1.4482174448839478,-7.728627928921551 L-1.612493717151891,-7.660582468972073 L-1.7735836133239555,-7.58530349713225 L-1.93116881092298,-7.5029397687825465 L-2.0849379129485595,-7.413654039171179 L-2.234587063214609,-7.3176227418008075 L-2.3798205467858677,-7.2150356397862545 L-2.520351374326842,-7.106095450872171 L-2.6559018492084867,-6.991017446851647 L-2.786204116251985,-6.870029028177328 L-2.9110006910252864,-6.743369274605645 L-3.0300449686464765,-6.611288472762091 L-3.1431017110885615,-6.474047621561104 L-3.249947512022721,-6.331917916457894 L-3.3503712382814754,-6.185180213551334 L-3.4441744470694173,-6.03412447459689 L-3.531171778097065,-5.87904919402628 L-3.6111913198629697,-5.720260809106091 L-3.684074949360279,-5.558073094400919 L-3.749678644536479,-5.392806541737606 L-3.807872768888874,-5.2247877268958 L-3.858542327633431,-5.054348664276284 L-3.9015871949407877,-4.8818261508223015 L-3.9369223117903847,-4.707561100490307 L-3.9644778540517605,-4.531897870585273 L-3.9841993704608663,-4.355183581291756 L-3.9960478902187506,-4.177767429745359 L-4.0,-4.000000000000019 " />
			<path d="M13.0,0.0 L12.6,0.0 " />
			<path d="M-13.0,0.0 L-12.99602274429008,-0.32154755463993434 L-12.984093410785396,-0.6428983589956069 L-12.964219298872072,-0.9638557831714003 L-12.936412569230885,-1.2842234379753237 L-12.90069023639634,-1.6038052950867085 L-12.8570741583457,-1.9224058070030963 L-12.805591023124423,-2.2398300266929168 L-12.74627233251613,-2.555883726880751 L-12.679154382767114,-2.8703735188921806 L-12.604278242377205,-3.1831069709855155 L-12.521689726970543,-3.4938927260979837 L-12.431439371261657,-3.8025406189343416 L-12.333582398134025,-4.108861792326259 L-12.22817868484997,-4.412668812791285 L-12.11529272641265,-4.713775785220671 L-11.994993596102487,-5.011998466625896 L-11.86735490321224,-5.307154378874275 L-11.73245474800654,-5.599062920344686 L-11.590375673933476,-5.887545476435074 L-11.44120461711745,-6.172425528854146 L-11.285032853164223,-6.4535287636303424 L-11.121955941310706,-6.7306831777720335 L-10.952073665953646,-7.003719184513655 L-10.77548997559299,-7.272469717083389 L-10.592312919227316,-7.536770330928894 L-10.402654580240222,-7.796459304338546 L-10.206631007818116,-8.05137773739661 L-10.004362145941409,-8.301369649211784 L-9.795971759992543,-8.546282073359652 L-9.581587361025733,-8.785965151480621 L-9.36134012774481,-9.020272224976072 L-9.135364826236875,-9.249059924746627 L-8.903799727510888,-9.47218825891763 L-8.666786522891636,-9.68952069849814 L-8.424470237320872,-9.900924260921038 L-8.176999140618658,-10.10626959141313 L-7.924524656759209,-10.305431042145463 L-7.6672012712167605,-10.498286749115403 L-7.405186436438152,-10.684718706713454 L-7.138640475499951,-10.86461283992917 L-6.867726484009096,-11.037859074152017 L-6.5926102303070575,-11.20435140252441 L-6.313460054038595,-11.363987950805779 L-6.030446763147168,-11.51667103970795 L-5.743743529360033,-11.662307244663669 L-5.453525782226983,-11.800807452991746 L-5.159971101777539,-11.93208691842381 L-4.863259109862316,-12.05606531295933 L-4.563571360245013,-12.172666776017136 L-4.261091227512301,-12.281819960853428 L-3.9560037948695723,-12.38345807821779 L-3.648495740891212,-12.477518937220598 L-3.3387552252946846,-12.563944983386683 L-3.0269717738083393,-12.642683333872107 L-2.713336162203356,-12.713685809822401 L-2.398040299560826,-12.776908965852508 L-2.0812771108453654,-12.832314116630371 L-1.763240418857131,-12.879867360547953 L-1.444124825634456,-12.91953960046511 L-1.1241255933796905,-12.951306561513734 L-0.8034385249810885,-12.975148805951173 L-0.4822598442038635,-12.991051745053916 L-0.16078607562371153,-12.999005648044218 L0.16078607562372502,-12.999005648044218 L0.4822598442038769,-12.991051745053916 L0.803438524981102,-12.975148805951173 L1.1241255933797039,-12.951306561513734 L1.4441248256344696,-12.919539600465109 L1.7632404188571442,-12.879867360547951 L2.0812771108453787,-12.83231411663037 L2.3980402995608388,-12.776908965852504 L2.713336162203369,-12.713685809822401 L3.026971773808352,-12.642683333872105 L3.3387552252946984,-12.56394498338668 L3.648495740891225,-12.477518937220596 L3.956003794869585,-12.383458078217789 L4.261091227512314,-12.281819960853422 L4.563571360245025,-12.172666776017133 L4.863259109862328,-12.056065312959326 L5.159971101777551,-11.932086918423808 L5.4535257822269925,-11.800807452991743 L5.743743529360044,-11.662307244663664 L6.030446763147178,-11.516671039707946 L6.313460054038606,-11.363987950805775 L6.592610230307067,-11.204351402524402 L6.867726484009105,-11.03785907415201 L7.138640475499961,-10.864612839929164 L7.4051864364381625,-10.684718706713443 L7.667201271216773,-10.498286749115394 L7.924524656759222,-10.305431042145452 L8.176999140618673,-10.106269591413117 L8.424470237320888,-9.900924260921023 L8.666786522891652,-9.689520698498127 L8.903799727510904,-9.472188258917614 L9.135364826236891,-9.24905992474661 L9.361340127744826,-9.020272224976054 L9.58158736102575,-8.785965151480603 L9.795971759992561,-8.546282073359633 L10.004362145941428,-8.301369649211761 L10.206631007818133,-8.051377737396585 L10.402654580240242,-7.796459304338521 L10.592312919227338,-7.536770330928867 L10.775489975593011,-7.272469717083361 L10.952073665953666,-7.003719184513626 L11.121955941310727,-6.730683177772002 L11.285032853164239,-6.453528763630309 L11.441204617117466,-6.172425528854111 L11.590375673933494,-5.887545476435038 L11.732454748006557,-5.5990629203446485 L11.867354903212256,-5.3071543788742375 L11.994993596102502,-5.011998466625857 L12.115292726412664,-4.713775785220632 L12.228178684849984,-4.412668812791244 L12.333582398134038,-4.108861792326217 L12.43143937126167,-3.802540618934298 L12.521689726970552,-3.4938927260979398 L12.604278242377216,-3.1831069709854707 L12.679154382767123,-2.8703735188921344 L12.746272332516138,-2.5558837268807038 L12.805591023124432,-2.239830026692869 L12.857074158345707,-1.9224058070030472 L12.900690236396345,-1.6038052950866588 L12.93641256923089,-1.2842234379752733 L12.964219298872074,-0.9638557831713491 L12.9840934107854,-0.6428983589955546 L12.996022744290082,-0.3215475546398813 L13.0,5.391911039236627e-14 " />
			<path d="M1.65,-4.0 L1.6461534691643895,-3.8874000179482926 L1.6346318109599456,-3.7753250289911926 L1.6154887446758326,-3.6642975784631537 L1.5888135241238686,-3.554835327590909 L1.5547305214960532,-3.4474486399178716 L1.5133986474839967,-3.3426382017537 L1.4650106103639182,-3.2408926877435973 L1.4097920175017047,-3.142686482441533 L1.3480003234672278,-3.048477468510467 L1.2799236296622907,-2.958704891862011 L1.2058793410589026,-2.8737873136892187 L1.1262126863107764,-2.794120658941093 L1.041295108137984,-2.720076370337705 L0.9515225314895274,-2.6519996765327685 L0.8573135175584615,-2.5902079824982915 L0.7591073122563967,-2.5349893896360784 L0.6573617982462937,-2.4866013525160007 L0.552551360082122,-2.4452694785039446 L0.4451646724090844,-2.4111864758761294 L0.33570242153683977,-2.384511255324166 L0.22467497100880054,-2.3653681890400535 L0.11259998205170042,-2.35384653083561 L-7.024371879737063e-15,-2.35 L-0.11259998205171443,-2.353846530835611 L-0.22467497100881442,-2.3653681890400557 L-0.33570242153685353,-2.3845112553241687 L-0.445164672409098,-2.4111864758761334 L-0.5525513600821352,-2.445269478503949 L-0.6573617982463065,-2.486601352516006 L-0.7591073122564092,-2.534989389636085 L-0.8573135175584736,-2.590207982498299 L-0.9515225314895387,-2.6519996765327765 L-1.0412951081379949,-2.720076370337714 L-1.1262126863107869,-2.794120658941102 L-1.2058793410589121,-2.8737873136892285 L-1.2799236296622996,-2.9587048918620216 L-1.3480003234672358,-3.0484774685104785 L-1.409792017501712,-3.142686482441545 L-1.4650106103639244,-3.2408926877436097 L-1.5133986474840024,-3.342638201753713 L-1.554730521496058,-3.447448639917885 L-1.5888135241238723,-3.5548353275909226 L-1.6154887446758353,-3.6642975784631675 L-1.6346318109599476,-3.775325028991207 L-1.6461534691643906,-3.887400017948307 L-1.65,-4.000000000000014 " />
			<path d="M-1.65,-4.0 L-1.6460684992970585,-4.113835388267136 L-1.6342927325794792,-4.227128299068828 L-1.6147288167383262,-4.339338840091795 L-1.587469982741941,-4.449932277007664 L-1.552646131347921,-4.558381581725556 L-1.5104232140668543,-4.664169943920946 L-1.4610024423277963,-4.766793233872218 L-1.4046193286141795,-4.865762404868363 L-1.3415425641395786,-4.960605823739272 L-1.2720727384117165,-5.050871518402567 L-1.1965409067865713,-5.136129331716407 L-1.115307012838845,-5.215972971374155 L-1.0287581730669106,-5.290021946072249 L-0.9373068321064074,-5.357923378724532 L-0.8413887972437247,-5.419353688082276 L-0.7414611615958165,-5.474020130746179 L-0.6380001258533414,-5.521662196221987 L-0.5314987289675097,-5.562052848371629 L-0.4224644985949529,-5.594999607343812 L-0.31141703249731256,-5.62034546682816 L-0.19888552242128296,-5.637969642261789 L-0.0854062322589453,-5.647788146422752 L0.028480057493891313,-5.6497541896674015 L0.1422306268030224,-5.6438584029043435 L0.25530340240396454,-5.630128882242431 L0.36715954102791937,-5.608631055100009 L0.47726599723533725,-5.579467368413466 L0.5850980636201846,-5.542776800430934 L0.6901418712796834,-5.498734198417644 L0.7918968386336483,-5.447549445429079 L0.8898780569236795,-5.389466460122638 L0.9836186010242227,-5.324762034374155 L1.072671754553429,-5.253744514238554 L1.1566131386801475,-5.176752330540483 L1.2350427344823178,-5.094152386097311 L1.3075867892193,-5.006338307260119 L1.3738995974338915,-4.913728568104878 L1.4336651483962617,-4.816764496212907 L1.4865986320389923,-4.715908169543969 L1.5324477962067495,-4.61164021442436 L1.5709941487526788,-4.50445751514359 L1.6020539987529863,-4.394870846074468 L1.625479331877842,-4.2834024376006035 L1.641158515747068,-4.170583487450808 L1.6490168319092662,-4.056951629300015 L1.6490168319092662,-3.943048370699979 L1.6411585157470676,-3.8294165125491864 L1.625479331877841,-3.7165975623993917 L1.602053998752985,-3.605129153925527 L1.5709941487526773,-3.4955424848564047 L1.5324477962067475,-3.3883597855756356 L1.4865986320389901,-3.284091830456026 L1.433665148396259,-3.1832355037870874 L1.3738995974338883,-3.0862714318951174 L1.3075867892192967,-2.993661692739877 L1.235042734482314,-2.9058476139026848 L1.1566131386801437,-2.8232476694595134 L1.0726717545534254,-2.7462554857614427 L0.983618601024219,-2.6752379656258416 L0.8898780569236757,-2.610533539877359 L0.7918968386336441,-2.5524505545709193 L0.6901418712796791,-2.5012658015823543 L0.5850980636201801,-2.4572231995690643 L0.47726599723533275,-2.420532631586533 L0.36715954102791476,-2.39136894489999 L0.2553034024039599,-2.369871117757568 L0.1422306268030177,-2.356141597095656 L0.028480057493886587,-2.3502458103325985 L-0.08540623225895001,-2.3522118535772476 L-0.19888552242128765,-2.3620303577382114 L-0.31141703249731717,-2.379654533171841 L-0.42246449859495744,-2.405000392656189 L-0.5314987289675142,-2.437947151628372 L-0.6380001258533458,-2.478337803778015 L-0.7414611615958208,-2.525979869253823 L-0.8413887972437287,-2.5806463119177265 L-0.9373068321064114,-2.64207662127547 L-1.0287581730669146,-2.7099780539277543 L-1.1153070128388487,-2.7840270286258484 L-1.196540906786575,-2.863870668283597 L-1.2720727384117199,-2.9491284815974375 L-1.3415425641395822,-3.0393941762607333 L-1.4046193286141826,-3.134237595131642 L-1.4610024423277992,-3.2332067661277875 L-1.510423214066857,-3.3358300560790592 L-1.5526461313479232,-3.44161841827445 L-1.5874699827419425,-3.5500677229923414 L-1.6147288167383274,-3.6606611599082113 L-1.63429273257948,-3.772871700931179 L-1.646068499297059,-3.8861646117328705 L-1.65,-4.000000000000007 " />
			<path d="M-4.0,-4.0 L-3.9960291851288026,-3.821812594163231 L-3.9841246242005814,-3.6439789629269406 L-3.9643099526191206,-3.466852178504885 L-3.9366245105807116,-3.290783909731898 L-3.9011232649678362,-3.116123723857976 L-3.8578767002175063,-2.943218392514856 L-3.806970678380942,-2.7724112032330406 L-3.748506268652414,-2.604041277876184 L-3.682599546705715,-2.438442899346021 L-3.6093813642366546,-2.275944847894608 L-3.528997089169127,-2.1168697483615673 L-3.4416063170405575,-1.9615334296323303 L-3.3473825541397324,-1.8102442975891209 L-3.246512873026125,-1.6633027227996227 L-3.1391975411146444,-1.521000444159021 L-3.025649623063222,-1.3836199896694321 L-2.9060945577526534,-1.2514341155067048 L-2.78076971069857,-1.1247052644882838 L-2.6499239027841783,-1.003685045017285 L-2.513816916249428,-0.8886137315373044 L-2.3727189789174226,-0.7797197874897495 L-2.2269102276820885,-0.6772194117208237 L-2.0766801523223033,-0.5813161092387302 L-1.9223270207467376,-0.4922002871733153 L-1.7641572868105289,-0.4100488767403374 L-1.6024849818795213,-0.335024981960915 L-1.4376310913500545,-0.2672775558335907 L-1.2699229173621738,-0.20694110460194093 L-1.099693428971525,-0.1541354207048773 L-0.9272806010701171,-0.10896534493985222 L-0.7530267433684582,-0.07152055831115556 L-0.577277820771311,-0.04187540397658429 L-0.4003827664963982,-0.020088739645984344 L-0.22269278929979788,-0.0062038207247137045 L-0.04456067618346754,-0.0002482144340416603 L0.13365990803069278,-0.0022337450789815527 L0.3116151228696075,-0.012156470572226574 L0.4889516547265319,-0.029996690260801984 L0.665317418332514,-0.055718984039884845 L0.8403622557891054,-0.0892722826761454 L1.0137386317744568,-0.13058996920098265 L1.1851023235425293,-0.17959001117234807 L1.3541131043454955,-0.23617512354256753 L1.5204354189224523,-0.3002329618087969 L1.683739049713333,-0.37163634506263366 L1.843699772475306,-0.4502435084960399 L1.9999999999999947,-0.5358983848622425 L2.152329412653486,-0.6284309143328088 L2.3003855744872372,-0.7276573821356935 L2.443874533696658,-0.8333807833039124 L2.582511406235207,-0.9453912138106695 L2.716020941425298,-1.0634662873143719 L2.8441380684430415,-1.1873715766861266 L2.966608422591829,-1.3168610794431048 L3.083188850319893,-1.451677706163701 L3.193647891979177,-1.5915537909147819 L3.2977662413670417,-1.7362116226776196 L3.3953371811384296,-1.8853639967174152 L3.4861669932240207,-2.038714784801713 L3.570075343439526,-2.1959595231355946 L3.646895639522519,-2.3567860168463644 L3.716475361885952,-2.520874959817567 L3.7786763664316765,-2.6879005686417274 L3.833375158822767,-2.8575312294331523 L3.8804631396700917,-3.0294301562165993 L3.9198468201463483,-3.2032560595846618 L3.951448007599479,-3.378663824296293 L3.97520396079694,-3.555305194471173 L3.991067514492613,-3.732829465019522 L3.9990071730690366,-3.910884177934594 L3.999007173069036,-4.089115822065424 L3.9910675144926118,-4.2671705349804965 L3.9752039607969376,-4.4446948055288455 L3.9514480075994762,-4.621336175703725 L3.919846820146345,-4.7967439404153565 L3.8804631396700873,-4.9705698437834185 L3.833375158822762,-5.1424687705668655 L3.7786763664316707,-5.312099431358289 L3.7164753618859447,-5.479125040182451 L3.6468956395225116,-5.643213983153653 L3.5700753434395174,-5.804040476864422 L3.4861669932240114,-5.961285215198304 L3.39533718113842,-6.1146360032826 L3.297766241367031,-6.2637883773223955 L3.193647891979166,-6.408446209085233 L3.0831888503198814,-6.548322293836313 L2.9666084225918166,-6.6831389205569085 L2.8441380684430286,-6.812628423313886 L2.7160209414252843,-6.936533712685641 L2.582511406235194,-7.054608786189341 L2.443874533696646,-7.1666192166960965 L2.3003855744872266,-7.2723426178643145 L2.152329412653476,-7.371569085667197 L1.9999999999999862,-7.464101615137762 L1.8436997724752988,-7.549756491503964 L1.6837390497133276,-7.628363654937369 L1.5204354189224474,-7.6997670381912044 L1.3541131043454913,-7.763824876457434 L1.185102323542526,-7.820409988827652 L1.0137386317744541,-7.869410030799018 L0.8403622557891037,-7.910727717323855 L0.6653174183325132,-7.944281015960115 L0.488951654726532,-7.970003309739198 L0.31161512286960846,-7.9878435294277725 L0.13365990803069464,-7.997766254921018 L-0.044560676183464785,-7.999751785565959 L-0.22269278929979425,-7.993796179275287 L-0.4003827664963937,-7.979911260354016 L-0.5772778207713056,-7.958124596023416 L-0.7530267433684521,-7.928479441688845 L-0.9272806010701101,-7.89103465506015 L-1.0996934289715172,-7.8458645792951245 L-1.2699229173621653,-7.793058895398062 L-1.4376310913500454,-7.732722444166413 L-1.6024849818795113,-7.664975018039089 L-1.7641572868105184,-7.589951123259668 L-1.9223270207467267,-7.5077997128266905 L-2.0766801523222918,-7.418683890761277 L-2.2269102276820765,-7.322780588279184 L-2.37271897891741,-7.220280212510259 L-2.5138169162494157,-7.111386268462706 L-2.6499239027841655,-6.996314954982726 L-2.780769710698557,-6.875294735511728 L-2.9060945577526405,-6.748565884493308 L-3.025649623063209,-6.616380010330583 L-3.1391975411146316,-6.4789995558409945 L-3.2465128730261124,-6.336697277200395 L-3.34738255413972,-6.189755702410897 L-3.4416063170405455,-6.03846657036769 L-3.5289970891691156,-5.8831302516384545 L-3.6093813642366435,-5.724055152105415 L-3.682599546705705,-5.561557100654004 L-3.748506268652404,-5.395958722123842 L-3.806970678380933,-5.2275887967669865 L-3.8578767002174983,-5.056781607485172 L-3.901123264967829,-4.883876276142054 L-3.936624510580706,-4.709216090268133 L-3.964309952619116,-4.533147821495148 L-3.9841246242005783,-4.356021037073093 L-3.9960291851288012,-4.1781874058368045 L-4.0,-4.000000000000036 " />
			<path d="M-1.65,-4.0 L-1.6460684992970585,-4.113835388267136 L-1.6342927325794792,-4.227128299068828 L-1.6147288167383262,-4.339338840091795 L-1.587469982741941,-4.449932277007664 L-1.552646131347921,-4.558381581725556 L-1.5104232140668543,-4.664169943920946 L-1.4610024423277963,-4.766793233872218 L-1.4046193286141795,-4.865762404868363 L-1.3415425641395786,-4.960605823739272 L-1.2720727384117165,-5.050871518402567 L-1.1965409067865713,-5.136129331716407 L-1.115307012838845,-5.215972971374155 L-1.0287581730669106,-5.290021946072249 L-0.9373068321064074,-5.357923378724532 L-0.8413887972437247,-5.419353688082276 L-0.7414611615958165,-5.474020130746179 L-0.6380001258533414,-5.521662196221987 L-0.5314987289675097,-5.562052848371629 L-0.4224644985949529,-5.594999607343812 L-0.31141703249731256,-5.62034546682816 L-0.19888552242128296,-5.637969642261789 L-0.0854062322589453,-5.647788146422752 L0.028480057493891313,-5.6497541896674015 L0.1422306268030224,-5.6438584029043435 L0.25530340240396454,-5.630128882242431 L0.36715954102791937,-5.608631055100009 L0.47726599723533725,-5.579467368413466 L0.5850980636201846,-5.542776800430934 L0.6901418712796834,-5.498734198417644 L0.7918968386336483,-5.447549445429079 L0.8898780569236795,-5.389466460122638 L0.9836186010242227,-5.324762034374155 L1.072671754553429,-5.253744514238554 L1.1566131386801475,-5.176752330540483 L1.2350427344823178,-5.094152386097311 L1.3075867892193,-5.006338307260119 L1.3738995974338915,-4.913728568104878 L1.4336651483962617,-4.816764496212907 L1.4865986320389923,-4.715908169543969 L1.5324477962067495,-4.61164021442436 L1.5709941487526788,-4.50445751514359 L1.6020539987529863,-4.394870846074468 L1.625479331877842,-4.2834024376006035 L1.641158515747068,-4.170583487450808 L1.6490168319092662,-4.056951629300015 L1.6490168319092662,-3.943048370699979 L1.6411585157470676,-3.8294165125491864 L1.625479331877841,-3.7165975623993917 L1.602053998752985,-3.605129153925527 L1.5709941487526773,-3.4955424848564047 L1.5324477962067475,-3.3883597855756356 L1.4865986320389901,-3.284091830456026 L1.433665148396259,-3.1832355037870874 L1.3738995974338883,-3.0862714318951174 L1.3075867892192967,-2.993661692739877 L1.235042734482314,-2.9058476139026848 L1.1566131386801437,-2.8232476694595134 L1.0726717545534254,-2.7462554857614427 L0.983618601024219,-2.6752379656258416 L0.8898780569236757,-2.610533539877359 L0.7918968386336441,-2.5524505545709193 L0.6901418712796791,-2.5012658015823543 L0.5850980636201801,-2.4572231995690643 L0.47726599723533275,-2.420532631586533 L0.36715954102791476,-2.39136894489999 L0.2553034024039599,-2.369871117757568 L0.1422306268030177,-2.356141597095656 L0.028480057493886587,-2.3502458103325985 L-0.08540623225895001,-2.3522118535772476 L-0.19888552242128765,-2.3620303577382114 L-0.31141703249731717,-2.379654533171841 L-0.42246449859495744,-2.405000392656189 L-0.5314987289675142,-2.437947151628372 L-0.6380001258533458,-2.478337803778015 L-0.7414611615958208,-2.525979869253823 L-0.8413887972437287,-2.5806463119177265 L-0.9373068321064114,-2.64207662127547 L-1.0287581730669146,-2.7099780539277543 L-1.1153070128388487,-2.7840270286258484 L-1.196540906786575,-2.863870668283597 L-1.2720727384117199,-2.9491284815974375 L-1.3415425641395822,-3.0393941762607333 L-1.4046193286141826,-3.134237595131642 L-1.4610024423277992,-3.2332067661277875 L-1.510423214066857,-3.3358300560790592 L-1.5526461313479232,-3.44161841827445 L-1.5874699827419425,-3.5500677229923414 L-1.6147288167383274,-3.6606611599082113 L-1.63429273257948,-3.772871700931179 L-1.646068499297059,-3.8861646117328705 L-1.65,-4.000000000000007 " />
			<path d="M4.0,-4.0 L4.0,56.0 " />
			<path d="M4.0,-4.0 L1.65,-4.0 " />
			<path d="M4.0,56.0 L-4.0,56.0 " />
			<path d="M-4.0,-4.0 L-4.0,56.0 " />
			<path d="M-1.6500000000000004,-4.0 L-4.0,-4.0 " />
			<path d="M1.65,-4.0 L1.6461534691643895,-3.8874000179482926 L1.6346318109599456,-3.7753250289911926 L1.6154887446758326,-3.6642975784631537 L1.5888135241238686,-3.554835327590909 L1.5547305214960532,-3.4474486399178716 L1.5133986474839967,-3.3426382017537 L1.4650106103639182,-3.2408926877435973 L1.4097920175017047,-3.142686482441533 L1.3480003234672278,-3.048477468510467 L1.2799236296622907,-2.958704891862011 L1.2058793410589026,-2.8737873136892187 L1.1262126863107764,-2.794120658941093 L1.041295108137984,-2.720076370337705 L0.9515225314895274,-2.6519996765327685 L0.8573135175584615,-2.5902079824982915 L0.7591073122563967,-2.5349893896360784 L0.6573617982462937,-2.4866013525160007 L0.552551360082122,-2.4452694785039446 L0.4451646724090844,-2.4111864758761294 L0.33570242153683977,-2.384511255324166 L0.22467497100880054,-2.3653681890400535 L0.11259998205170042,-2.35384653083561 L-7.024371879737063e-15,-2.35 L-0.11259998205171443,-2.353846530835611 L-0.22467497100881442,-2.3653681890400557 L-0.33570242153685353,-2.3845112553241687 L-0.445164672409098,-2.4111864758761334 L-0.5525513600821352,-2.445269478503949 L-0.6573617982463065,-2.486601352516006 L-0.7591073122564092,-2.534989389636085 L-0.8573135175584736,-2.590207982498299 L-0.9515225314895387,-2.6519996765327765 L-1.0412951081379949,-2.720076370337714 L-1.1262126863107869,-2.794120658941102 L-1.2058793410589121,-2.8737873136892285 L-1.2799236296622996,-2.9587048918620216 L-1.3480003234672358,-3.0484774685104785 L-1.409792017501712,-3.142686482441545 L-1.4650106103639244,-3.2408926877436097 L-1.5133986474840024,-3.342638201753713 L-1.554730521496058,-3.447448639917885 L-1.5888135241238723,-3.5548353275909226 L-1.6154887446758353,-3.6642975784631675 L-1.6346318109599476,-3.775325028991207 L-1.6461534691643906,-3.887400017948307 L-1.65,-4.000000000000014 " />
			<path d="M-1.65,-4.0 L-1.6461534691643895,-3.887400017948293 L-1.6346318109599456,-3.775325028991193 L-1.6154887446758328,-3.664297578463154 L-1.5888135241238686,-3.55483532759091 L-1.5547305214960538,-3.447448639917873 L-1.5133986474839976,-3.3426382017537017 L-1.465010610363919,-3.240892687743599 L-1.4097920175017062,-3.142686482441535 L-1.3480003234672293,-3.0484774685104696 L-1.2799236296622927,-2.958704891862013 L-1.205879341058905,-2.8737873136892214 L-1.1262126863107795,-2.794120658941096 L-1.0412951081379873,-2.7200763703377078 L-0.9515225314895311,-2.651999676532771 L-0.8573135175584657,-2.590207982498294 L-0.7591073122564014,-2.534989389636081 L-0.6573617982462988,-2.4866013525160024 L-0.5525513600821277,-2.4452694785039464 L-0.4451646724090907,-2.411186475876131 L-0.3357024215368464,-2.3845112553241674 L-0.2246749710088076,-2.3653681890400544 L-0.11259998205170789,-2.3538465308356105 L-8.3378055718226e-16,-2.35 L0.11259998205170621,-2.35384653083561 L0.22467497100880596,-2.365368189040054 L0.33570242153684476,-2.384511255324167 L0.445164672409089,-2.411186475876131 L0.5525513600821261,-2.445269478503946 L0.6573617982462974,-2.4866013525160024 L0.7591073122564003,-2.5349893896360807 L0.857313517558465,-2.5902079824982938 L0.9515225314895306,-2.6519996765327707 L1.041295108137987,-2.7200763703377073 L1.1262126863107795,-2.794120658941096 L1.205879341058905,-2.8737873136892214 L1.2799236296622933,-2.9587048918620136 L1.3480003234672302,-3.0484774685104705 L1.409792017501707,-3.142686482441536 L1.46501061036392,-3.240892687743601 L1.5133986474839984,-3.3426382017537035 L1.5547305214960547,-3.447448639917875 L1.5888135241238697,-3.554835327590913 L1.6154887446758333,-3.6642975784631573 L1.6346318109599463,-3.7753250289911966 L1.64615346916439,-3.8874000179482966 L1.65,-4.000000000000004 " />
			<path d="M4.0,-4.0 L4.0,56.0 " />
			<path d="M4.0,-4.0 L4.0,56.0 " />
			<path d="M4.0,-4.0 L1.65,-4.0 " />
			<path d="M4.0,-4.0 L1.65,-4.0 " />
			<path d="M4.0,56.0 L-4.0,56.0 " />
			<path d="M-4.0,-4.0 L-4.0,56.0 " />
			<path d="M-1.6500000000000004,-4.0 L-4.0,-4.0 " />
			<path d="M1.65,-4.0 L1.6461534691643895,-3.8874000179482926 L1.6346318109599456,-3.7753250289911926 L1.6154887446758326,-3.6642975784631537 L1.5888135241238686,-3.554835327590909 L1.5547305214960532,-3.4474486399178716 L1.5133986474839967,-3.3426382017537 L1.4650106103639182,-3.2408926877435973 L1.4097920175017047,-3.142686482441533 L1.3480003234672278,-3.048477468510467 L1.2799236296622907,-2.958704891862011 L1.2058793410589026,-2.8737873136892187 L1.1262126863107764,-2.794120658941093 L1.041295108137984,-2.720076370337705 L0.9515225314895274,-2.6519996765327685 L0.8573135175584615,-2.5902079824982915 L0.7591073122563967,-2.5349893896360784 L0.6573617982462937,-2.4866013525160007 L0.552551360082122,-2.4452694785039446 L0.4451646724090844,-2.4111864758761294 L0.33570242153683977,-2.384511255324166 L0.22467497100880054,-2.3653681890400535 L0.11259998205170042,-2.35384653083561 L-7.024371879737063e-15,-2.35 L-0.11259998205171443,-2.353846530835611 L-0.22467497100881442,-2.3653681890400557 L-0.33570242153685353,-2.3845112553241687 L-0.445164672409098,-2.4111864758761334 L-0.5525513600821352,-2.445269478503949 L-0.6573617982463065,-2.486601352516006 L-0.7591073122564092,-2.534989389636085 L-0.8573135175584736,-2.590207982498299 L-0.9515225314895387,-2.6519996765327765 L-1.0412951081379949,-2.720076370337714 L-1.1262126863107869,-2.794120658941102 L-1.2058793410589121,-2.8737873136892285 L-1.2799236296622996,-2.9587048918620216 L-1.3480003234672358,-3.0484774685104785 L-1.409792017501712,-3.142686482441545 L-1.4650106103639244,-3.2408926877436097 L-1.5133986474840024,-3.342638201753713 L-1.554730521496058,-3.447448639917885 L-1.5888135241238723,-3.5548353275909226 L-1.6154887446758353,-3.6642975784631675 L-1.6346318109599476,-3.775325028991207 L-1.6461534691643906,-3.887400017948307 L-1.65,-4.000000000000014 " />
			<path d="M4.0,56.0 L-4.0,56.0 " />
			<path d="M-4.0,-4.0 L-4.0,56.0 " />
			<path d="M-1.6500000000000004,-4.0 L-4.0,-4.0 " />
			<path d="M-1.65,-4.0 L-1.6461534691643895,-3.887400017948293 L-1.6346318109599456,-3.775325028991193 L-1.6154887446758328,-3.664297578463154 L-1.5888135241238686,-3.55483532759091 L-1.5547305214960538,-3.447448639917873 L-1.5133986474839976,-3.3426382017537017 L-1.465010610363919,-3.240892687743599 L-1.4097920175017062,-3.142686482441535 L-1.3480003234672293,-3.0484774685104696 L-1.2799236296622927,-2.958704891862013 L-1.205879341058905,-2.8737873136892214 L-1.1262126863107795,-2.794120658941096 L-1.0412951081379873,-2.7200763703377078 L-0.9515225314895311,-2.651999676532771 L-0.8573135175584657,-2.590207982498294 L-0.7591073122564014,-2.534989389636081 L-0.6573617982462988,-2.4866013525160024 L-0.5525513600821277,-2.4452694785039464 L-0.4451646724090907,-2.411186475876131 L-0.3357024215368464,-2.3845112553241674 L-0.2246749710088076,-2.3653681890400544 L-0.11259998205170789,-2.3538465308356105 L-8.3378055718226e-16,-2.35 L0.11259998205170621,-2.35384653083561 L0.22467497100880596,-2.365368189040054 L0.33570242153684476,-2.384511255324167 L0.445164672409089,-2.411186475876131 L0.5525513600821261,-2.445269478503946 L0.6573617982462974,-2.4866013525160024 L0.7591073122564003,-2.5349893896360807 L0.857313517558465,-2.5902079824982938 L0.9515225314895306,-2.6519996765327707 L1.041295108137987,-2.7200763703377073 L1.1262126863107795,-2.794120658941096 L1.205879341058905,-2.8737873136892214 L1.2799236296622933,-2.9587048918620136 L1.3480003234672302,-3.0484774685104705 L1.409792017501707,-3.142686482441536 L1.46501061036392,-3.240892687743601 L1.5133986474839984,-3.3426382017537035 L1.5547305214960547,-3.447448639917875 L1.5888135241238697,-3.554835327590913 L1.6154887446758333,-3.6642975784631573 L1.6346318109599463,-3.7753250289911966 L1.64615346916439,-3.8874000179482966 L1.65,-4.000000000000004 " />
			<path d="M-1.65,-4.0 L-1.6461534691643895,-3.887400017948293 L-1.6346318109599456,-3.775325028991193 L-1.6154887446758328,-3.664297578463154 L-1.5888135241238686,-3.55483532759091 L-1.5547305214960538,-3.447448639917873 L-1.5133986474839976,-3.3426382017537017 L-1.465010610363919,-3.240892687743599 L-1.4097920175017062,-3.142686482441535 L-1.3480003234672293,-3.0484774685104696 L-1.2799236296622927,-2.958704891862013 L-1.205879341058905,-2.8737873136892214 L-1.1262126863107795,-2.794120658941096 L-1.0412951081379873,-2.7200763703377078 L-0.9515225314895311,-2.651999676532771 L-0.8573135175584657,-2.590207982498294 L-0.7591073122564014,-2.534989389636081 L-0.6573617982462988,-2.4866013525160024 L-0.5525513600821277,-2.4452694785039464 L-0.4451646724090907,-2.411186475876131 L-0.3357024215368464,-2.3845112553241674 L-0.2246749710088076,-2.3653681890400544 L-0.11259998205170789,-2.3538465308356105 L-8.3378055718226e-16,-2.35 L0.11259998205170621,-2.35384653083561 L0.22467497100880596,-2.365368189040054 L0.33570242153684476,-2.384511255324167 L0.445164672409089,-2.411186475876131 L0.5525513600821261,-2.445269478503946 L0.6573617982462974,-2.4866013525160024 L0.7591073122564003,-2.5349893896360807 L0.857313517558465,-2.5902079824982938 L0.9515225314895306,-2.6519996765327707 L1.041295108137987,-2.7200763703377073 L1.1262126863107795,-2.794120658941096 L1.205879341058905,-2.8737873136892214 L1.2799236296622933,-2.9587048918620136 L1.3480003234672302,-3.0484774685104705 L1.409792017501707,-3.142686482441536 L1.46501061036392,-3.240892687743601 L1.5133986474839984,-3.3426382017537035 L1.5547305214960547,-3.447448639917875 L1.5888135241238697,-3.554835327590913 L1.6154887446758333,-3.6642975784631573 L1.6346318109599463,-3.7753250289911966 L1.64615346916439,-3.8874000179482966 L1.65,-4.000000000000004 " />
			<path d="M-1.5,-4.0 L-1.4960898472769246,-3.891763366299076 L-1.484379774833456,-3.784091028288821 L-1.46493083356513,-3.6775443396834637 L-1.437844421246162,-3.57267878558245 L-1.4032617538884016,-3.4700410864283464 L-1.3613631295064355,-3.370166347659603 L-1.3123669881272244,-3.2735752699185707 L-1.256528772944947,-3.1807714343594546 L-1.1941395985584657,-3.092238677209352 L-1.1255247332346037,-3.0084385672701996 L-1.051041903110014,-2.9298079995127604 L-0.9710794271727416,-2.8567569173085454 L-0.8860541927468271,-2.7896661751748946 L-0.7964094820348305,-2.7288855531758704 L-0.7026126610496856,-2.674731933330966 L-0.6051527429847131,-2.627487647538982 L-0.5045378387252633,-2.587399005630238 L-0.4012925077938318,-2.554675011221166 L-0.29595502353960074,-2.52948627206623 L-0.18907456683043478,-2.511964110588093 L-0.08120836287812708,-2.502199879223314 L0.027081223875839805,-2.500244484153038 L0.13522962166809693,-2.506108119901744 L0.24267299482914612,-2.5197602161877106 L0.3488511833614646,-2.541129597302315 L0.453210623354358,-2.5701048531872157 L0.5552072330098704,-2.6065349202748123 L0.65430924923335,-2.6502298690637396 L0.7499999999999991,-2.7009618943233416 L0.8417805980435729,-2.758466502764664 L0.929172541823584,-2.822443891985991 L1.0117202102107707,-2.892560513503752 L1.0889932378846963,-2.968450811719865 L1.1605887590592545,-3.0497191297593647 L1.226133507838338,-3.135941772242141 L1.2852857642513842,-3.226669214234468 L1.3377371358230739,-3.3214284448638605 L1.3832141653889003,-3.4197254333787424 L1.4214797567742041,-3.5210477047960316 L1.4523344109038454,-3.624867011708407 L1.4756172658980045,-3.7306420883216944 L1.4912069357315398,-3.83782147236409 L1.4990221430845156,-3.945846380155098 L1.4990221430845154,-4.054153619844907 L1.491206935731539,-4.162178527635916 L1.4756172658980036,-4.269357911678311 L1.4523344109038439,-4.375132988291599 L1.4214797567742024,-4.478952295203974 L1.383214165388898,-4.580274566621263 L1.3377371358230714,-4.678571555136145 L1.2852857642513813,-4.773330785765537 L1.2261335078383349,-4.864058227757864 L1.160588759059251,-4.95028087024064 L1.0889932378846925,-5.031549188280139 L1.0117202102107665,-5.107439486496252 L0.9291725418235801,-5.177556108014012 L0.8417805980435694,-5.241533497235339 L0.749999999999996,-5.29903810567666 L0.6543092492333473,-5.349770130936262 L0.555207233009868,-5.393465079725189 L0.45321062335435575,-5.429895146812785 L0.3488511833614627,-5.458870402697686 L0.24267299482914448,-5.48023978381229 L0.13522962166809563,-5.493891880098257 L0.02708122387583884,-5.499755515846962 L-0.0812083628781277,-5.497800120776686 L-0.18907456683043505,-5.488035889411906 L-0.2959550235396007,-5.4705137279337706 L-0.40129250779383147,-5.445324988778834 L-0.5045378387252626,-5.412600994369762 L-0.6051527429847121,-5.372512352461019 L-0.7026126610496843,-5.325268066669035 L-0.7964094820348291,-5.27111444682413 L-0.8860541927468253,-5.210333824825106 L-0.9710794271727397,-5.143243082691456 L-1.0510419031100118,-5.070192000487242 L-1.1255247332346017,-4.991561432729803 L-1.1941395985584635,-4.90776132279065 L-1.2565287729449452,-4.8192285656405485 L-1.3123669881272224,-4.726424730081433 L-1.3613631295064337,-4.629833652340401 L-1.4032617538883998,-4.529958913571658 L-1.4378444212461605,-4.427321214417555 L-1.4649308335651288,-4.322455660316542 L-1.484379774833455,-4.215908971711185 L-1.4960898472769242,-4.108236633700931 L-1.5,-4.000000000000007 " />

       </g>

       <!-- solid lines -->
       <g  stroke="rgb(40,40,40)" fill="none">
			<path d="M12.6,0.0 L4.0,0.0 " />
			<path d="M-4.000000000000002,0.0 L-12.6,0.0 " />
			<path d="M-12.6,0.0 L-12.6,2.0 " />
			<path d="M-12.6,2.0 L-13.6,2.0 " />
			<path d="M-14.6,0.9999999999999999 L-13.6,2.0 " />
			<path d="M-14.6,0.0 L-14.6,1.0 " />
			<path d="M-14.600000000000001,0.0 L-14.596046921220143,-0.3397267630612223 L-14.58418982554246,-0.6792695580871011 L-14.564435133793435,-1.0184445166642293 L-14.536793543487146,-1.3570679695691261 L-14.50128002303237,-1.6949565462283613 L-14.457913803626928,-2.0319272740169554 L-14.406718368843658,-2.3677976773412843 L-14.347721441913636,-2.702385876452833 L-14.280954970713564,-3.0355106859392853 L-14.206455110465429,-3.3669917128396256 L-14.124262204157814,-3.696649454330105 L-14.034420760699458,-4.024305394928187 L-13.936979430816887,-4.349782103161837 L-13.83199098070921,-4.672903327651785 L-13.719512263474265,-4.993494092554764 L-13.59960418832168,-5.311380792316013 L-13.47233168758946,-5.6263912856797464 L-13.337763681581974,-5.938354988906684 L-13.1959730412484,-6.247102968148154 L-13.04703654872182,-6.552468030926749 L-12.891034855740333,-6.8542848166740065 L-12.72805243997273,-7.152389886276072 L-12.558177559272334,-7.44662181057886 L-12.381502203883818,-7.736821257804793 L-12.198122046628873,-8.022831079833768 L-12.008136391097668,-8.304496397301635 L-11.811648117874233,-8.581664683470107 L-11.608763628824779,-8.854185846822675 L-11.399592789479227,-9.121912312341816 L-11.18424886953708,-9.384699101423472 L-10.96284848152989,-9.64240391038551 L-10.735511517673501,-9.894887187527688 L-10.50236108494431,-10.142012208701358 L-10.263523438414664,-10.383645151347999 L-10.019127912883514,-10.619655166966508 L-9.769306852839334,-10.849914451969951 L-9.514195540793251,-11.074298316893481 L-9.253932124021174,-11.29268525391587 L-8.988657539754616,-11.504957002658136 L-8.718515438860685,-11.710998614223636 L-8.44365210805261,-11.910698513444906 L-8.164216390672912,-12.103948559303603 L-7.880359606092095,-12.290644103490754 L-7.592235467766553,-12.470684047075668 L-7.300000000000009,-12.6439708952528 L-7.003811453453604,-12.81041081013689 L-6.70383021945038,-12.969913661577854 L-6.400218743120541,-13.122393075967832 L-6.0931414354345526,-13.26776648301403 L-5.7827645841717015,-13.405955160451995 L-5.469256263872329,-13.536884276675089 L-5.152786244822499,-13.660482931257153 L-4.833525901120402,-13.776684193346314 L-4.5116481178742465,-13.885425137909236 L-4.187327197581934,-13.986646879806132 L-3.860738765743169,-14.080294605678104 L-3.5320596757551654,-14.166317603629544 L-3.201467913143406,-14.244669290689524 L-2.869142499179338,-14.315307238037294 L-2.535263393937202,-14.378193193978234 L-2.2000113988424728,-14.433293104657828 L-1.8635680587647014,-14.480577132502416 L-1.5261155637077612,-14.520019672376788 L-1.1878366501507522,-14.551599365449787 L-0.848914502092969,-14.575299110760513 L-0.5095326518565367,-14.591106074478796 L-0.16987488070041956,-14.599011696854928 L0.16987488070037268,-14.59901169685493 L0.50953265185649,-14.591106074478798 L0.8489145020929222,-14.575299110760517 L1.1878366501507056,-14.551599365449789 L1.5261155637077148,-14.520019672376792 L1.8635680587646546,-14.480577132502424 L2.2000113988424266,-14.433293104657833 L2.535263393937156,-14.378193193978243 L2.869142499179292,-14.315307238037304 L3.20146791314336,-14.244669290689535 L3.53205967575512,-14.166317603629556 L3.8607387657431236,-14.080294605678118 L4.187327197581888,-13.986646879806147 L4.511648117874203,-13.885425137909252 L4.833525901120358,-13.77668419334633 L5.152786244822456,-13.660482931257171 L5.4692562638722855,-13.536884276675108 L5.782764584171659,-13.405955160452015 L6.0931414354345135,-13.267766483014052 L6.400218743120505,-13.122393075967851 L6.703830219450348,-12.969913661577873 L7.003811453453575,-12.810410810136908 L7.299999999999983,-12.643970895252814 L7.592235467766531,-12.47068404707568 L7.880359606092076,-12.290644103490767 L8.164216390672895,-12.103948559303616 L8.443652108052596,-11.910698513444917 L8.718515438860672,-11.710998614223643 L8.988657539754607,-11.504957002658141 L9.25393212402117,-11.292685253915874 L9.514195540793247,-11.074298316893485 L9.769306852839334,-10.849914451969953 L10.019127912883516,-10.619655166966506 L10.263523438414667,-10.383645151347995 L10.502361084944315,-10.14201220870135 L10.735511517673508,-9.89488718752768 L10.962848481529901,-9.6424039103855 L11.184248869537093,-9.38469910142346 L11.39959278947924,-9.1219123123418 L11.608763628824793,-8.854185846822656 L11.81164811787425,-8.581664683470086 L12.008136391097688,-8.30449639730161 L12.19812204662889,-8.022831079833741 L12.381502203883839,-7.736821257804762 L12.558177559272355,-7.446621810578826 L12.72805243997275,-7.152389886276034 L12.891034855740353,-6.854284816673967 L13.04703654872184,-6.552468030926707 L13.19597304124842,-6.247102968148108 L13.337763681581993,-5.938354988906636 L13.47233168758948,-5.626391285679696 L13.599604188321699,-5.311380792315959 L13.719512263474282,-4.993494092554707 L13.831990980709229,-4.672903327651726 L13.936979430816907,-4.349782103161776 L14.034420760699476,-4.024305394928124 L14.124262204157832,-3.6966494543300374 L14.206455110465445,-3.366991712839556 L14.280954970713578,-3.0355106859392125 L14.347721441913649,-2.7023858764527566 L14.40671836884367,-2.3677976773412053 L14.457913803626939,-2.0319272740168732 L14.501280023032379,-1.694956546228276 L14.536793543487153,-1.3570679695690382 L14.564435133793442,-1.0184445166641387 L14.584189825542463,-0.6792695580870075 L14.596046921220145,-0.339726763061126 L14.600000000000001,9.90202663092091e-14 " />
			<path d="M14.6,0.0 L14.6,1.0 " />
			<path d="M14.6,1.0 L13.6,2.0 " />
			<path d="M13.6,2.0 L12.6,2.0 " />
			<path d="M12.6,0.0 L12.6,2.0 " />
			<path d="M4.0,-3.9999999999999996 L3.9960849060798944,-4.176933386901514 L3.9843472882997792,-4.353520418389368 L3.9648101235976587,-4.529415417056888 L3.9375116568909028,-4.704274060184142 L3.902505326210028,-4.877754053765839 L3.8598596580912408,-5.049515802567913 L3.8096581334325266,-5.219223074901143 L3.7519990240758716,-5.386543660810473 L3.6869952004355153,-5.551150022391604 L3.6147739105488177,-5.712719934961816 L3.535476530982247,-5.8709371178299214 L3.4492582900801145,-6.0254918534305695 L3.3562879640977985,-6.176081593610923 L3.2567475468143012,-6.322411551882876 L3.1508318932708783,-6.46419528048145 L3.0387483383331455,-6.601155231099741 L2.9207162908233433,-6.733023298202767 L2.7969668040172633,-6.859541343856643 L2.6677421233466108,-6.980461703045707 L2.533295212192196,-7.09554766848842 L2.3938892566962386,-7.204573954002986 L2.2497971505631322,-7.307327135515628 L2.1013009608572055,-7.403606068848243 L1.9486913758431972,-7.493222283467565 L1.7922671359503257,-7.5760003514250975 L1.632334448973872,-7.651778230765549 L1.4692063906590405,-7.72040758273158 L1.303202291840484,-7.781754062143877 L1.1346471133372014,-7.835697580388157 L0.9638708098264728,-7.882132540494265 L0.7912076839420848,-7.920968043847209 L0.6169957318612258,-7.952128068125454 L0.44157598166109613,-7.975551616118201 L0.2652918257404335,-7.991192835130283 L0.08848834861276583,-7.9990211067409716 L-0.08848834861272885,-7.999021106740972 L-0.26529182574039656,-7.991192835130286 L-0.4415759816610593,-7.975551616118205 L-0.6169957318611892,-7.952128068125459 L-0.7912076839420487,-7.920968043847216 L-0.9638708098264369,-7.882132540494274 L-1.1346471133371658,-7.8356975803881665 L-1.303202291840449,-7.7817540621438885 L-1.469206390659006,-7.7204075827315926 L-1.6323344489738383,-7.651778230765564 L-1.7922671359502926,-7.5760003514251135 L-1.9486913758431648,-7.493222283467583 L-2.101300960857174,-7.403606068848262 L-2.2497971505631016,-7.307327135515649 L-2.393889256696209,-7.204573954003008 L-2.5332952121921672,-7.095547668488444 L-2.667742123346583,-6.980461703045732 L-2.7969668040172366,-6.8595413438566695 L-2.920716290823318,-6.733023298202794 L-3.0387483383331215,-6.601155231099769 L-3.150831893270855,-6.46419528048148 L-3.2567475468142795,-6.322411551882906 L-3.3562879640977785,-6.176081593610954 L-3.449258290080096,-6.0254918534306015 L-3.53547653098223,-5.870937117829954 L-3.614773910548802,-5.712719934961849 L-3.686995200435501,-5.551150022391638 L-3.7519990240758587,-5.386543660810508 L-3.8096581334325155,-5.219223074901178 L-3.859859658091231,-5.0495158025679485 L-3.9025053262100196,-4.877754053765876 L-3.9375116568908965,-4.704274060184178 L-3.964810123597654,-4.529415417056924 L-3.984347288299776,-4.353520418389405 L-3.9960849060798926,-4.176933386901552 L-4.0,-4.000000000000036 " />
			<path d="M-1.65,-4.0 L-1.6461534691643895,-4.112599982051707 L-1.6346318109599456,-4.224674971008807 L-1.6154887446758328,-4.335702421536846 L-1.5888135241238686,-4.44516467240909 L-1.5547305214960538,-4.552551360082127 L-1.5133986474839976,-4.657361798246298 L-1.465010610363919,-4.7591073122564005 L-1.4097920175017062,-4.857313517558465 L-1.3480003234672293,-4.95152253148953 L-1.2799236296622927,-5.041295108137987 L-1.205879341058905,-5.126212686310779 L-1.1262126863107795,-5.205879341058904 L-1.0412951081379873,-5.279923629662292 L-0.9515225314895311,-5.348000323467229 L-0.8573135175584657,-5.409792017501706 L-0.7591073122564014,-5.465010610363919 L-0.6573617982462988,-5.5133986474839976 L-0.5525513600821277,-5.554730521496054 L-0.4451646724090907,-5.588813524123869 L-0.3357024215368464,-5.615488744675833 L-0.2246749710088076,-5.634631810959945 L-0.11259998205170789,-5.646153469164389 L-8.3378055718226e-16,-5.65 L0.11259998205170621,-5.64615346916439 L0.22467497100880596,-5.634631810959946 L0.33570242153684476,-5.615488744675833 L0.445164672409089,-5.588813524123869 L0.5525513600821261,-5.5547305214960545 L0.6573617982462974,-5.5133986474839976 L0.7591073122564003,-5.465010610363919 L0.857313517558465,-5.409792017501706 L0.9515225314895306,-5.348000323467229 L1.041295108137987,-5.279923629662292 L1.1262126863107795,-5.205879341058904 L1.205879341058905,-5.126212686310779 L1.2799236296622933,-5.041295108137986 L1.3480003234672302,-4.9515225314895295 L1.409792017501707,-4.857313517558464 L1.46501061036392,-4.759107312256399 L1.5133986474839984,-4.6573617982462965 L1.5547305214960547,-4.552551360082124 L1.5888135241238697,-4.445164672409087 L1.6154887446758333,-4.335702421536842 L1.6346318109599463,-4.224674971008803 L1.64615346916439,-4.112599982051703 L1.65,-3.999999999999996 " />
			<path d="M4.0,-4.0 L4.0,56.0 " />
			<path d="M4.0,-4.0 L1.65,-4.0 " />
			<path d="M4.0,56.0 L-4.0,56.0 " />
			<path d="M-4.0,-4.0 L-4.0,56.0 " />
			<path d="M-1.6500000000000004,-4.0 L-4.0,-4.0 " />
			<path d="M-1.65,-4.0 L-1.6461534691643895,-3.887400017948293 L-1.6346318109599456,-3.775325028991193 L-1.6154887446758328,-3.664297578463154 L-1.5888135241238686,-3.55483532759091 L-1.5547305214960538,-3.447448639917873 L-1.5133986474839976,-3.3426382017537017 L-1.465010610363919,-3.240892687743599 L-1.4097920175017062,-3.142686482441535 L-1.3480003234672293,-3.0484774685104696 L-1.2799236296622927,-2.958704891862013 L-1.205879341058905,-2.8737873136892214 L-1.1262126863107795,-2.794120658941096 L-1.0412951081379873,-2.7200763703377078 L-0.9515225314895311,-2.651999676532771 L-0.8573135175584657,-2.590207982498294 L-0.7591073122564014,-2.534989389636081 L-0.6573617982462988,-2.4866013525160024 L-0.5525513600821277,-2.4452694785039464 L-0.4451646724090907,-2.411186475876131 L-0.3357024215368464,-2.3845112553241674 L-0.2246749710088076,-2.3653681890400544 L-0.11259998205170789,-2.3538465308356105 L-8.3378055718226e-16,-2.35 L0.11259998205170621,-2.35384653083561 L0.22467497100880596,-2.365368189040054 L0.33570242153684476,-2.384511255324167 L0.445164672409089,-2.411186475876131 L0.5525513600821261,-2.445269478503946 L0.6573617982462974,-2.4866013525160024 L0.7591073122564003,-2.5349893896360807 L0.857313517558465,-2.5902079824982938 L0.9515225314895306,-2.6519996765327707 L1.041295108137987,-2.7200763703377073 L1.1262126863107795,-2.794120658941096 L1.205879341058905,-2.8737873136892214 L1.2799236296622933,-2.9587048918620136 L1.3480003234672302,-3.0484774685104705 L1.409792017501707,-3.142686482441536 L1.46501061036392,-3.240892687743601 L1.5133986474839984,-3.3426382017537035 L1.5547305214960547,-3.447448639917875 L1.5888135241238697,-3.554835327590913 L1.6154887446758333,-3.6642975784631573 L1.6346318109599463,-3.7753250289911966 L1.64615346916439,-3.8874000179482966 L1.65,-4.000000000000004 " />
			<path d="M-1.5,-4.0 L-1.4960898472769246,-3.891763366299076 L-1.484379774833456,-3.784091028288821 L-1.46493083356513,-3.6775443396834637 L-1.437844421246162,-3.57267878558245 L-1.4032617538884016,-3.4700410864283464 L-1.3613631295064355,-3.370166347659603 L-1.3123669881272244,-3.2735752699185707 L-1.256528772944947,-3.1807714343594546 L-1.1941395985584657,-3.092238677209352 L-1.1255247332346037,-3.0084385672701996 L-1.051041903110014,-2.9298079995127604 L-0.9710794271727416,-2.8567569173085454 L-0.8860541927468271,-2.7896661751748946 L-0.7964094820348305,-2.7288855531758704 L-0.7026126610496856,-2.674731933330966 L-0.6051527429847131,-2.627487647538982 L-0.5045378387252633,-2.587399005630238 L-0.4012925077938318,-2.554675011221166 L-0.29595502353960074,-2.52948627206623 L-0.18907456683043478,-2.511964110588093 L-0.08120836287812708,-2.502199879223314 L0.027081223875839805,-2.500244484153038 L0.13522962166809693,-2.506108119901744 L0.24267299482914612,-2.5197602161877106 L0.3488511833614646,-2.541129597302315 L0.453210623354358,-2.5701048531872157 L0.5552072330098704,-2.6065349202748123 L0.65430924923335,-2.6502298690637396 L0.7499999999999991,-2.7009618943233416 L0.8417805980435729,-2.758466502764664 L0.929172541823584,-2.822443891985991 L1.0117202102107707,-2.892560513503752 L1.0889932378846963,-2.968450811719865 L1.1605887590592545,-3.0497191297593647 L1.226133507838338,-3.135941772242141 L1.2852857642513842,-3.226669214234468 L1.3377371358230739,-3.3214284448638605 L1.3832141653889003,-3.4197254333787424 L1.4214797567742041,-3.5210477047960316 L1.4523344109038454,-3.624867011708407 L1.4756172658980045,-3.7306420883216944 L1.4912069357315398,-3.83782147236409 L1.4990221430845156,-3.945846380155098 L1.4990221430845154,-4.054153619844907 L1.491206935731539,-4.162178527635916 L1.4756172658980036,-4.269357911678311 L1.4523344109038439,-4.375132988291599 L1.4214797567742024,-4.478952295203974 L1.383214165388898,-4.580274566621263 L1.3377371358230714,-4.678571555136145 L1.2852857642513813,-4.773330785765537 L1.2261335078383349,-4.864058227757864 L1.160588759059251,-4.95028087024064 L1.0889932378846925,-5.031549188280139 L1.0117202102107665,-5.107439486496252 L0.9291725418235801,-5.177556108014012 L0.8417805980435694,-5.241533497235339 L0.749999999999996,-5.29903810567666 L0.6543092492333473,-5.349770130936262 L0.555207233009868,-5.393465079725189 L0.45321062335435575,-5.429895146812785 L0.3488511833614627,-5.458870402697686 L0.24267299482914448,-5.48023978381229 L0.13522962166809563,-5.493891880098257 L0.02708122387583884,-5.499755515846962 L-0.0812083628781277,-5.497800120776686 L-0.18907456683043505,-5.488035889411906 L-0.2959550235396007,-5.4705137279337706 L-0.40129250779383147,-5.445324988778834 L-0.5045378387252626,-5.412600994369762 L-0.6051527429847121,-5.372512352461019 L-0.7026126610496843,-5.325268066669035 L-0.7964094820348291,-5.27111444682413 L-0.8860541927468253,-5.210333824825106 L-0.9710794271727397,-5.143243082691456 L-1.0510419031100118,-5.070192000487242 L-1.1255247332346017,-4.991561432729803 L-1.1941395985584635,-4.90776132279065 L-1.2565287729449452,-4.8192285656405485 L-1.3123669881272224,-4.726424730081433 L-1.3613631295064337,-4.629833652340401 L-1.4032617538883998,-4.529958913571658 L-1.4378444212461605,-4.427321214417555 L-1.4649308335651288,-4.322455660316542 L-1.484379774833455,-4.215908971711185 L-1.4960898472769242,-4.108236633700931 L-1.5,-4.000000000000007 " />

       </g>
    </g>
    
</svg>

```

=== file: docs/figures/cad/assembly-side.svg ===
```svg
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   width="900.0"
   height="600.0"

>
    <g transform="scale(6.373937668025583, -6.373937668025583)   translate(12.137777882222222,-17.737777882222222)" stroke-width="0.4"  fill="none">
       <!-- hidden lines -->
       <g  stroke="rgb(180,180,180)" fill="none" stroke-dasharray="0.4,0.4" >
			<path d="M0.0,0.0 L2.0,0.0 " />
			<path d="M0.0,0.0 L2.0,0.0 " />
			<path d="M0.0,0.0 L0.0,-2.0 " />
			<path d="M0.0,14.6 L0.0,14.508198264441342 L0.0,14.233947517854624 L0.0,13.780696622502166 L0.0,13.154145471375319 L0.0,12.362173308732947 L0.0,11.414739644033235 L0.0,10.323759005323591 L0.0,9.102951107137509 L0.0,7.7676683171239125 L0.0,6.334702591116347 L0.0,4.822074304545438 L0.0,3.2488056357621886 L0.0,1.6346813511082932 L0.0,6.972200594645983e-14 " />
			<path d="M0.0,0.0 L0.0,-1.0 " />
			<path d="M0.0,-1.0 L0.0,-2.0 " />
			<path d="M0.0,0.0 L0.0,-2.0 " />
			<path d="M0.0,4.0 L0.0,3.55214209558677 L0.0,3.1099162641747453 L0.0,2.6788837521793356 L0.0,2.264465043529773 L0.0,1.8718716939386604 L0.0,1.5060407925650727 L0.0,1.1715728752538173 L0.0,0.8726740701278879 L0.0,0.6131032030868706 L0.0,0.3961245283903301 L0.0,0.22446667876653548 L0.0,0.10028835127270996 L0.0,0.025151160427031805 L0.0,4.996003610813204e-16 " />
			<path d="M0.0,0.0 L0.0,0.10028835127270108 L0.0,0.39612452839031587 L0.0,0.8726740701278706 L0.0,1.5060407925650545 L0.0,2.264465043529756 L0.0,3.1099162641747315 L0.0,3.9999999999999907 L0.0,4.89008373582525 L0.0,5.735534956470227 L0.0,6.493959207434931 L0.0,7.127325929872116 L0.0,7.603875471609674 L0.0,7.899711648727294 L0.0,7.9999999999999964 " />
			<path d="M0.0,8.0 L0.0,7.974848839572971 L0.0,7.899711648727294 L0.0,7.77553332123347 L0.0,7.603875471609677 L0.0,7.3868967969131365 L0.0,7.12732592987212 L0.0,6.828427124746191 L0.0,6.493959207434935 L0.0,6.128128306061347 L0.0,5.735534956470233 L0.0,5.321116247820669 L0.0,4.890083735825258 L0.0,4.447857904413232 L0.0,4.000000000000036 " />
			<path d="M2.0,0.0 L78.0,0.0 " />
			<path d="M78.0,0.0 L80.0,0.0 " />
			<path d="M80.0,0.0 L80.0,-2.0 " />
			<path d="M0.0,-2.0 L80.0,-2.0 " />
			<path d="M2.0,0.0 L2.0,1.4555381893430022 L2.0,2.8927721414320873 L2.0,4.293627805417172 L2.0,5.640488608528256 L2.0,6.916416994699375 L2.0,8.105367424163536 L2.0,9.192388155425117 L2.0,10.163809272084388 L2.0,11.007414589967693 L2.0,11.712595282731447 L2.0,12.270483294008777 L2.0,12.674062858363705 L2.0,12.918258728612152 L2.0,12.999999999999996 " />
			<path d="M2.0,12.999999999999998 L2.0,12.918258728612152 L2.0,12.674062858363705 L2.0,12.270483294008777 L2.0,11.712595282731447 L2.0,11.007414589967691 L2.0,10.163809272084386 L2.0,9.192388155425116 L2.0,8.105367424163534 L2.0,6.916416994699373 L2.0,5.640488608528253 L2.0,4.29362780541717 L2.0,2.892772141432085 L2.0,1.4555381893430002 L2.0,6.17284001691587e-14 " />
			<path d="M2.0,4.0 L2.0,4.184741385570458 L2.0,4.3671595410279185 L2.0,4.544960452226025 L2.0,4.715908169543971 L2.0,4.877852926250306 L2.0,5.02875817306691 L2.0,5.166726188957803 L2.0,5.290021946072249 L2.0,5.397094928726669 L2.0,5.486598632038992 L2.0,5.557407495008807 L2.0,5.608631055100009 L2.0,5.6396251463238505 L2.0,5.65 " />
			<path d="M2.0,5.65 L2.0,5.608631055100009 L2.0,5.486598632038992 L2.0,5.290021946072249 L2.0,5.02875817306691 L2.0,4.715908169543971 L2.0,4.3671595410279185 L2.0,4.0 L2.0,3.6328404589720815 L2.0,3.2840918304560294 L2.0,2.97124182693309 L2.0,2.709978053927751 L2.0,2.5134013679610088 L2.0,2.391368944899991 L2.0,2.350000000000002 " />
			<path d="M2.0,2.35 L2.0,2.3603748536761495 L2.0,2.391368944899991 L2.0,2.4425925049911936 L2.0,2.5134013679610083 L2.0,2.602905071273331 L2.0,2.7099780539277507 L2.0,2.833273811042196 L2.0,2.971241826933089 L2.0,3.1221470737496944 L2.0,3.284091830456029 L2.0,3.455039547773974 L2.0,3.6328404589720806 L2.0,3.8152586144295415 L2.0,3.999999999999985 " />
			<path d="M2.0,0.0 L78.0,0.0 " />
			<path d="M78.0,0.0 L80.0,0.0 " />
			<path d="M80.0,0.0 L80.0,-2.0 " />
			<path d="M0.0,-2.0 L80.0,-2.0 " />
			<path d="M0.0,2.3594865558827754e-15 L80.0,2.3594865558827754e-15 " />
			<path d="M80.0,14.6 L80.0,14.508198264441342 L80.0,14.233947517854624 L80.0,13.780696622502166 L80.0,13.154145471375319 L80.0,12.362173308732947 L80.0,11.414739644033235 L80.0,10.323759005323591 L80.0,9.102951107137509 L80.0,7.7676683171239125 L80.0,6.334702591116347 L80.0,4.822074304545438 L80.0,3.2488056357621886 L80.0,1.6346813511082932 L80.0,6.972200594645983e-14 " />
			<path d="M80.0,0.0 L80.0,-1.0 " />
			<path d="M0.0,-1.0 L80.0,-1.0 " />
			<path d="M0.0,-2.0 L80.0,-2.0 " />
			<path d="M80.0,-1.0 L80.0,-2.0 " />
			<path d="M-4.0,0.0 L-4.0,0.10028835127270552 L-4.0,0.3961245283903234 L-4.0,0.8726740701278803 L-4.0,1.5060407925650656 L-4.0,2.264465043529767 L-4.0,3.1099162641747418 L-4.0,3.9999999999999996 L-4.0,4.890083735825257 L-4.0,5.735534956470232 L-4.0,6.4939592074349335 L-4.0,7.127325929872119 L-4.0,7.603875471609676 L-4.0,7.899711648727294 L-4.0,7.9999999999999964 " />
			<path d="M2.0,0.0 L78.0,0.0 " />
			<path d="M80.0,4.0 L80.0,3.55214209558677 L80.0,3.1099162641747453 L80.0,2.6788837521793356 L80.0,2.264465043529773 L80.0,1.8718716939386604 L80.0,1.5060407925650727 L80.0,1.1715728752538173 L80.0,0.8726740701278879 L80.0,0.6131032030868706 L80.0,0.3961245283903301 L80.0,0.22446667876653548 L80.0,0.10028835127270996 L80.0,0.025151160427031805 L80.0,4.996003610813204e-16 " />
			<path d="M80.0,0.0 L80.0,0.10028835127270108 L80.0,0.39612452839031587 L80.0,0.8726740701278706 L80.0,1.5060407925650545 L80.0,2.264465043529756 L80.0,3.1099162641747315 L80.0,3.9999999999999907 L80.0,4.89008373582525 L80.0,5.735534956470227 L80.0,6.493959207434931 L80.0,7.127325929872116 L80.0,7.603875471609674 L80.0,7.899711648727294 L80.0,7.9999999999999964 " />
			<path d="M80.0,8.0 L80.0,7.974848839572971 L80.0,7.899711648727294 L80.0,7.77553332123347 L80.0,7.603875471609677 L80.0,7.3868967969131365 L80.0,7.12732592987212 L80.0,6.828427124746191 L80.0,6.493959207434935 L80.0,6.128128306061347 L80.0,5.735534956470233 L80.0,5.321116247820669 L80.0,4.890083735825258 L80.0,4.447857904413232 L80.0,4.000000000000036 " />
			<path d="M2.0,1.9062434440709366e-15 L78.0,1.9062434440709366e-15 " />
			<path d="M78.0,0.0 L78.0,1.4555381893430022 L78.0,2.8927721414320873 L78.0,4.293627805417172 L78.0,5.640488608528256 L78.0,6.916416994699375 L78.0,8.105367424163536 L78.0,9.192388155425117 L78.0,10.163809272084388 L78.0,11.007414589967693 L78.0,11.712595282731447 L78.0,12.270483294008777 L78.0,12.674062858363705 L78.0,12.918258728612152 L78.0,12.999999999999996 " />
			<path d="M78.0,12.999999999999998 L78.0,12.918258728612152 L78.0,12.674062858363705 L78.0,12.270483294008777 L78.0,11.712595282731447 L78.0,11.007414589967691 L78.0,10.163809272084386 L78.0,9.192388155425116 L78.0,8.105367424163534 L78.0,6.916416994699373 L78.0,5.640488608528253 L78.0,4.29362780541717 L78.0,2.892772141432085 L78.0,1.4555381893430002 L78.0,6.17284001691587e-14 " />
			<path d="M-4.0,4.0 L-4.0,4.184741385570458 L-4.0,4.3671595410279185 L-4.0,4.544960452226025 L-4.0,4.715908169543971 L-4.0,4.877852926250306 L-4.0,5.02875817306691 L-4.0,5.166726188957803 L-4.0,5.290021946072249 L-4.0,5.397094928726669 L-4.0,5.486598632038992 L-4.0,5.557407495008807 L-4.0,5.608631055100009 L-4.0,5.6396251463238505 L-4.0,5.65 " />
			<path d="M-4.0,5.65 L-4.0,5.608631055100009 L-4.0,5.486598632038992 L-4.0,5.290021946072249 L-4.0,5.02875817306691 L-4.0,4.715908169543971 L-4.0,4.3671595410279185 L-4.0,4.0 L-4.0,3.6328404589720815 L-4.0,3.2840918304560294 L-4.0,2.97124182693309 L-4.0,2.709978053927751 L-4.0,2.5134013679610088 L-4.0,2.391368944899991 L-4.0,2.350000000000002 " />
			<path d="M-4.0,2.35 L-4.0,2.3603748536761495 L-4.0,2.391368944899991 L-4.0,2.4425925049911936 L-4.0,2.5134013679610083 L-4.0,2.602905071273331 L-4.0,2.7099780539277507 L-4.0,2.833273811042196 L-4.0,2.971241826933089 L-4.0,3.1221470737496944 L-4.0,3.284091830456029 L-4.0,3.455039547773974 L-4.0,3.6328404589720806 L-4.0,3.8152586144295415 L-4.0,3.999999999999985 " />
			<path d="M78.0,4.0 L78.0,4.184741385570458 L78.0,4.3671595410279185 L78.0,4.544960452226025 L78.0,4.715908169543971 L78.0,4.877852926250306 L78.0,5.02875817306691 L78.0,5.166726188957803 L78.0,5.290021946072249 L78.0,5.397094928726669 L78.0,5.486598632038992 L78.0,5.557407495008807 L78.0,5.608631055100009 L78.0,5.6396251463238505 L78.0,5.65 " />
			<path d="M78.0,5.65 L78.0,5.608631055100009 L78.0,5.486598632038992 L78.0,5.290021946072249 L78.0,5.02875817306691 L78.0,4.715908169543971 L78.0,4.3671595410279185 L78.0,4.0 L78.0,3.6328404589720815 L78.0,3.2840918304560294 L78.0,2.97124182693309 L78.0,2.709978053927751 L78.0,2.5134013679610088 L78.0,2.391368944899991 L78.0,2.350000000000002 " />
			<path d="M78.0,2.35 L78.0,2.3603748536761495 L78.0,2.391368944899991 L78.0,2.4425925049911936 L78.0,2.5134013679610083 L78.0,2.602905071273331 L78.0,2.7099780539277507 L78.0,2.833273811042196 L78.0,2.971241826933089 L78.0,3.1221470737496944 L78.0,3.284091830456029 L78.0,3.455039547773974 L78.0,3.6328404589720806 L78.0,3.8152586144295415 L78.0,3.999999999999985 " />
			<path d="M84.0,0.0 L84.0,0.10028835127270552 L84.0,0.3961245283903234 L84.0,0.8726740701278803 L84.0,1.5060407925650656 L84.0,2.264465043529767 L84.0,3.1099162641747418 L84.0,3.9999999999999996 L84.0,4.890083735825257 L84.0,5.735534956470232 L84.0,6.4939592074349335 L84.0,7.127325929872119 L84.0,7.603875471609676 L84.0,7.899711648727294 L84.0,7.9999999999999964 " />
			<path d="M84.0,4.0 L84.0,4.184741385570458 L84.0,4.3671595410279185 L84.0,4.544960452226025 L84.0,4.715908169543971 L84.0,4.877852926250306 L84.0,5.02875817306691 L84.0,5.166726188957803 L84.0,5.290021946072249 L84.0,5.397094928726669 L84.0,5.486598632038992 L84.0,5.557407495008807 L84.0,5.608631055100009 L84.0,5.6396251463238505 L84.0,5.65 " />
			<path d="M84.0,5.65 L84.0,5.608631055100009 L84.0,5.486598632038992 L84.0,5.290021946072249 L84.0,5.02875817306691 L84.0,4.715908169543971 L84.0,4.3671595410279185 L84.0,4.0 L84.0,3.6328404589720815 L84.0,3.2840918304560294 L84.0,2.97124182693309 L84.0,2.709978053927751 L84.0,2.5134013679610088 L84.0,2.391368944899991 L84.0,2.350000000000002 " />
			<path d="M84.0,2.35 L84.0,2.3603748536761495 L84.0,2.391368944899991 L84.0,2.4425925049911936 L84.0,2.5134013679610083 L84.0,2.602905071273331 L84.0,2.7099780539277507 L84.0,2.833273811042196 L84.0,2.971241826933089 L84.0,3.1221470737496944 L84.0,3.284091830456029 L84.0,3.455039547773974 L84.0,3.6328404589720806 L84.0,3.8152586144295415 L84.0,3.999999999999985 " />
			<path d="M-9.0,4.0 L-5.0,4.0 " />
			<path d="M-5.0,4.0 L-5.0,-56.0 " />
			<path d="M-9.0,-56.0 L-5.0,-56.0 " />
			<path d="M-9.0,4.0 L-9.0,-56.0 " />
			<path d="M-9.0,4.0 L-7.0,4.0 " />
			<path d="M-5.0,4.0 L-7.0,4.0 " />
			<path d="M-5.0,4.0 L-5.0,3.8152586144295424 L-5.0,3.6328404589720815 L-5.0,3.455039547773975 L-5.0,3.2840918304560294 L-5.0,3.122147073749695 L-5.0,2.97124182693309 L-5.0,2.8332738110421967 L-5.0,2.709978053927751 L-5.0,2.602905071273331 L-5.0,2.5134013679610088 L-5.0,2.442592504991194 L-5.0,2.391368944899991 L-5.0,2.3603748536761495 L-5.0,2.350000000000001 " />
			<path d="M-5.0,2.35 L-5.0,2.3603748536761495 L-5.0,2.391368944899991 L-5.0,2.4425925049911936 L-5.0,2.5134013679610083 L-5.0,2.602905071273331 L-5.0,2.7099780539277507 L-5.0,2.833273811042196 L-5.0,2.971241826933089 L-5.0,3.1221470737496944 L-5.0,3.284091830456029 L-5.0,3.455039547773974 L-5.0,3.6328404589720806 L-5.0,3.8152586144295415 L-5.0,3.999999999999985 " />
			<path d="M-9.0,4.0 L-9.0,3.815258614429542 L-9.0,3.6328404589720815 L-9.0,3.4550395477739744 L-9.0,3.2840918304560294 L-9.0,3.122147073749695 L-9.0,2.97124182693309 L-9.0,2.8332738110421967 L-9.0,2.7099780539277507 L-9.0,2.602905071273331 L-9.0,2.5134013679610083 L-9.0,2.4425925049911936 L-9.0,2.391368944899991 L-9.0,2.3603748536761495 L-9.0,2.35 " />
			<path d="M-9.0,2.35 L-9.0,2.3603748536761495 L-9.0,2.391368944899991 L-9.0,2.4425925049911936 L-9.0,2.5134013679610083 L-9.0,2.602905071273331 L-9.0,2.7099780539277507 L-9.0,2.8332738110421967 L-9.0,2.9712418269330896 L-9.0,3.1221470737496944 L-9.0,3.284091830456029 L-9.0,3.455039547773974 L-9.0,3.632840458972081 L-9.0,3.815258614429542 L-9.0,3.999999999999993 " />
			<path d="M-7.0,4.0 L-7.0,3.815258614429542 L-7.0,3.6328404589720815 L-7.0,3.4550395477739744 L-7.0,3.2840918304560294 L-7.0,3.122147073749695 L-7.0,2.97124182693309 L-7.0,2.8332738110421967 L-7.0,2.7099780539277507 L-7.0,2.602905071273331 L-7.0,2.5134013679610083 L-7.0,2.4425925049911936 L-7.0,2.391368944899991 L-7.0,2.3603748536761495 L-7.0,2.35 " />
			<path d="M-7.0,2.35 L-7.0,2.3603748536761495 L-7.0,2.391368944899991 L-7.0,2.4425925049911936 L-7.0,2.5134013679610083 L-7.0,2.602905071273331 L-7.0,2.7099780539277507 L-7.0,2.8332738110421967 L-7.0,2.9712418269330896 L-7.0,3.1221470737496944 L-7.0,3.284091830456029 L-7.0,3.455039547773974 L-7.0,3.632840458972081 L-7.0,3.815258614429542 L-7.0,3.999999999999993 " />
			<path d="M-7.0,4.0 L-9.0,4.0 " />
			<path d="M-7.0,4.0 L-5.0,4.0 " />
			<path d="M85.0,4.0 L89.0,4.0 " />
			<path d="M89.0,4.0 L89.0,-56.0 " />
			<path d="M85.0,-56.0 L89.0,-56.0 " />
			<path d="M85.0,4.0 L85.0,-56.0 " />
			<path d="M85.0,4.0 L87.0,4.0 " />
			<path d="M89.0,4.0 L87.0,4.0 " />
			<path d="M89.0,4.0 L89.0,3.8152586144295424 L89.0,3.6328404589720815 L89.0,3.455039547773975 L89.0,3.2840918304560294 L89.0,3.122147073749695 L89.0,2.97124182693309 L89.0,2.8332738110421967 L89.0,2.709978053927751 L89.0,2.602905071273331 L89.0,2.5134013679610088 L89.0,2.442592504991194 L89.0,2.391368944899991 L89.0,2.3603748536761495 L89.0,2.350000000000001 " />
			<path d="M89.0,2.35 L89.0,2.3603748536761495 L89.0,2.391368944899991 L89.0,2.4425925049911936 L89.0,2.5134013679610083 L89.0,2.602905071273331 L89.0,2.7099780539277507 L89.0,2.833273811042196 L89.0,2.971241826933089 L89.0,3.1221470737496944 L89.0,3.284091830456029 L89.0,3.455039547773974 L89.0,3.6328404589720806 L89.0,3.8152586144295415 L89.0,3.999999999999985 " />
			<path d="M85.0,4.0 L85.0,3.815258614429542 L85.0,3.6328404589720815 L85.0,3.4550395477739744 L85.0,3.2840918304560294 L85.0,3.122147073749695 L85.0,2.97124182693309 L85.0,2.8332738110421967 L85.0,2.7099780539277507 L85.0,2.602905071273331 L85.0,2.5134013679610083 L85.0,2.4425925049911936 L85.0,2.391368944899991 L85.0,2.3603748536761495 L85.0,2.35 " />
			<path d="M85.0,2.35 L85.0,2.3603748536761495 L85.0,2.391368944899991 L85.0,2.4425925049911936 L85.0,2.5134013679610083 L85.0,2.602905071273331 L85.0,2.7099780539277507 L85.0,2.8332738110421967 L85.0,2.9712418269330896 L85.0,3.1221470737496944 L85.0,3.284091830456029 L85.0,3.455039547773974 L85.0,3.632840458972081 L85.0,3.815258614429542 L85.0,3.999999999999993 " />
			<path d="M87.0,4.0 L87.0,3.815258614429542 L87.0,3.6328404589720815 L87.0,3.4550395477739744 L87.0,3.2840918304560294 L87.0,3.122147073749695 L87.0,2.97124182693309 L87.0,2.8332738110421967 L87.0,2.7099780539277507 L87.0,2.602905071273331 L87.0,2.5134013679610083 L87.0,2.4425925049911936 L87.0,2.391368944899991 L87.0,2.3603748536761495 L87.0,2.35 " />
			<path d="M87.0,2.35 L87.0,2.3603748536761495 L87.0,2.391368944899991 L87.0,2.4425925049911936 L87.0,2.5134013679610083 L87.0,2.602905071273331 L87.0,2.7099780539277507 L87.0,2.8332738110421967 L87.0,2.9712418269330896 L87.0,3.1221470737496944 L87.0,3.284091830456029 L87.0,3.455039547773974 L87.0,3.632840458972081 L87.0,3.815258614429542 L87.0,3.999999999999993 " />
			<path d="M87.0,4.0 L85.0,4.0 " />
			<path d="M87.0,4.0 L89.0,4.0 " />
			<path d="M-9.0,4.0 L-9.0,3.832053285845038 L-9.0,3.6662185990655285 L-9.0,3.504581407067249 L-9.0,3.349174391323663 L-9.0,3.201951885226995 L-9.0,3.0647652972119 L-9.0,2.939339828220179 L-9.0,2.8272527762979554 L-9.0,2.7299137011575736 L-9.0,2.6485466981463714 L-9.0,2.5841750045374487 L-9.0,2.5376081317272643 L-9.0,2.509431685160136 L-9.0,2.5 " />
			<path d="M-9.0,2.5 L-9.0,2.5376081317272643 L-9.0,2.6485466981463714 L-9.0,2.8272527762979554 L-9.0,3.0647652972118995 L-9.0,3.349174391323663 L-9.0,3.6662185990655285 L-9.0,4.0 L-9.0,4.3337814009344715 L-9.0,4.650825608676337 L-9.0,4.9352347027881 L-9.0,5.172747223702045 L-9.0,5.3514533018536286 L-9.0,5.462391868272736 L-9.0,5.499999999999998 " />
			<path d="M89.0,4.0 L89.0,3.832053285845038 L89.0,3.6662185990655285 L89.0,3.504581407067249 L89.0,3.349174391323663 L89.0,3.201951885226995 L89.0,3.0647652972119 L89.0,2.939339828220179 L89.0,2.8272527762979554 L89.0,2.7299137011575736 L89.0,2.6485466981463714 L89.0,2.5841750045374487 L89.0,2.5376081317272643 L89.0,2.509431685160136 L89.0,2.5 " />
			<path d="M89.0,2.5 L89.0,2.5376081317272643 L89.0,2.6485466981463714 L89.0,2.8272527762979554 L89.0,3.0647652972118995 L89.0,3.349174391323663 L89.0,3.6662185990655285 L89.0,4.0 L89.0,4.3337814009344715 L89.0,4.650825608676337 L89.0,4.9352347027881 L89.0,5.172747223702045 L89.0,5.3514533018536286 L89.0,5.462391868272736 L89.0,5.499999999999998 " />
			<path d="M78.0,12.999999999999998 L2.0,12.999999999999998 " />
			<path d="M2.0,5.65 L-4.0,5.65 " />
			<path d="M2.0,2.35 L-4.0,2.35 " />
			<path d="M84.0,5.65 L78.0,5.65 " />
			<path d="M84.0,2.35 L78.0,2.35 " />
			<path d="M-9.0,2.35 L-7.0,2.35 " />
			<path d="M-5.0,2.35 L-7.0,2.35 " />
			<path d="M85.0,2.35 L87.0,2.35 " />
			<path d="M89.0,2.35 L87.0,2.35 " />
			<path d="M84.0,5.5 L-4.0,5.5 " />
			<path d="M89.0,2.5 L85.0,2.5 " />
			<path d="M84.0,2.5 L-4.0,2.5 " />
			<path d="M-5.0,2.5 L-9.0,2.5 " />

       </g>

       <!-- solid lines -->
       <g  stroke="rgb(40,40,40)" fill="none">
			<path d="M0.0,-0.9999999999999999 L0.0,-2.0 " />
			<path d="M0.0,0.0 L0.0,-1.0 " />
			<path d="M0.0,0.0 L0.0,1.634681351108295 L0.0,3.2488056357621904 L0.0,4.82207430454544 L0.0,6.334702591116349 L0.0,7.767668317123915 L0.0,9.10295110713751 L0.0,10.323759005323595 L0.0,11.414739644033236 L0.0,12.362173308732949 L0.0,13.154145471375319 L0.0,13.780696622502166 L0.0,14.233947517854624 L0.0,14.508198264441342 L0.0,14.599999999999998 " />
			<path d="M0.0,-2.0 L80.0,-2.0 " />
			<path d="M0.0,-1.0 L80.0,-1.0 " />
			<path d="M80.0,-0.9999999999999999 L80.0,-2.0 " />
			<path d="M80.0,0.0 L80.0,-1.0 " />
			<path d="M0.0,0.0 L80.0,0.0 " />
			<path d="M80.0,0.0 L80.0,1.634681351108295 L80.0,3.2488056357621904 L80.0,4.82207430454544 L80.0,6.334702591116349 L80.0,7.767668317123915 L80.0,9.10295110713751 L80.0,10.323759005323595 L80.0,11.414739644033236 L80.0,12.362173308732949 L80.0,13.154145471375319 L80.0,13.780696622502166 L80.0,14.233947517854624 L80.0,14.508198264441342 L80.0,14.599999999999998 " />
			<path d="M-4.0,4.0 L-4.0,3.5521420955867686 L-4.0,3.1099162641747427 L-4.0,2.6788837521793316 L-4.0,2.2644650435297677 L-4.0,1.8718716939386537 L-4.0,1.506040792565066 L-4.0,1.1715728752538102 L-4.0,0.8726740701278808 L-4.0,0.6131032030868635 L-4.0,0.3961245283903234 L-4.0,0.2244666787665297 L-4.0,0.10028835127270552 L-4.0,0.025151160427029584 L-4.0,4.961309141293668e-16 " />
			<path d="M-4.0,8.0 L-4.0,7.974848839572971 L-4.0,7.899711648727294 L-4.0,7.77553332123347 L-4.0,7.603875471609677 L-4.0,7.3868967969131365 L-4.0,7.12732592987212 L-4.0,6.828427124746191 L-4.0,6.493959207434935 L-4.0,6.128128306061347 L-4.0,5.735534956470233 L-4.0,5.321116247820669 L-4.0,4.890083735825258 L-4.0,4.447857904413232 L-4.0,4.000000000000036 " />
			<path d="M84.0,4.0 L84.0,3.5521420955867686 L84.0,3.1099162641747427 L84.0,2.6788837521793316 L84.0,2.2644650435297677 L84.0,1.8718716939386537 L84.0,1.506040792565066 L84.0,1.1715728752538102 L84.0,0.8726740701278808 L84.0,0.6131032030868635 L84.0,0.3961245283903234 L84.0,0.2244666787665297 L84.0,0.10028835127270552 L84.0,0.025151160427029584 L84.0,4.961309141293668e-16 " />
			<path d="M84.0,8.0 L84.0,7.974848839572971 L84.0,7.899711648727294 L84.0,7.77553332123347 L84.0,7.603875471609677 L84.0,7.3868967969131365 L84.0,7.12732592987212 L84.0,6.828427124746191 L84.0,6.493959207434935 L84.0,6.128128306061347 L84.0,5.735534956470233 L84.0,5.321116247820669 L84.0,4.890083735825258 L84.0,4.447857904413232 L84.0,4.000000000000036 " />
			<path d="M-5.0,4.0 L-5.0,-56.0 " />
			<path d="M-9.0,-56.0 L-5.0,-56.0 " />
			<path d="M-9.0,4.0 L-9.0,-56.0 " />
			<path d="M-9.0,4.0 L-5.0,4.0 " />
			<path d="M89.0,4.0 L89.0,-56.0 " />
			<path d="M85.0,-56.0 L89.0,-56.0 " />
			<path d="M85.0,4.0 L85.0,-56.0 " />
			<path d="M85.0,4.0 L89.0,4.0 " />
			<path d="M-9.0,5.5 L-9.0,5.490568314839864 L-9.0,5.462391868272736 L-9.0,5.415824995462551 L-9.0,5.351453301853629 L-9.0,5.270086298842426 L-9.0,5.172747223702045 L-9.0,5.060660171779821 L-9.0,4.935234702788101 L-9.0,4.798048114773005 L-9.0,4.650825608676337 L-9.0,4.495418592932751 L-9.0,4.3337814009344715 L-9.0,4.167946714154962 L-9.0,4.000000000000013 " />
			<path d="M89.0,5.5 L89.0,5.490568314839864 L89.0,5.462391868272736 L89.0,5.415824995462551 L89.0,5.351453301853629 L89.0,5.270086298842426 L89.0,5.172747223702045 L89.0,5.060660171779821 L89.0,4.935234702788101 L89.0,4.798048114773005 L89.0,4.650825608676337 L89.0,4.495418592932751 L89.0,4.3337814009344715 L89.0,4.167946714154962 L89.0,4.000000000000013 " />
			<path d="M80.0,14.6 L0.0,14.6 " />
			<path d="M0.0,8.0 L-4.0,8.0 " />
			<path d="M0.0,0.0 L-4.0,0.0 " />
			<path d="M84.0,8.0 L80.0,8.0 " />
			<path d="M84.0,0.0 L80.0,0.0 " />
			<path d="M89.0,5.5 L84.0,5.5 " />
			<path d="M-4.0,5.5 L-9.0,5.5 " />
			<path d="M85.0,2.5 L84.0,2.5 " />
			<path d="M-4.0,2.5 L-5.0,2.5 " />

       </g>
    </g>
    
</svg>

```

=== file: docs/figures/cad/assembly.svg ===
```svg
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   width="900.0"
   height="600.0"

>
    <g transform="scale(4.030218890888361, -4.030218890888361)   translate(19.562509615846576,-34.28904617265052)" stroke-width="0.4"  fill="none">
       <!-- hidden lines -->
       <g  stroke="rgb(180,180,180)" fill="none" stroke-dasharray="0.4,0.4" >
			<path d="M1.7061506225466871,-0.5268424917801267 L-1.7763568394002505e-14,5.329070518200751e-15 " />
			<path d="M-1.7763568394002505e-14,5.329070518200751e-15 L-6.293849377453313,1.9434786384550677 " />
			<path d="M-10.322322198539908,3.187431330018618 L-10.322322198539908,1.3925436952008776 " />
			<path d="M10.32232219853991,-4.982318964836358 L-10.32232219853991,1.3925436952008772 " />
			<path d="M10.322322198539908,-3.187431330018618 L10.322322198539908,-4.982318964836358 " />
			<path d="M-5.570777059529474,-0.4336641265331447 L-5.454276002414901,-0.3639533501152974 L-5.330161200740118,-0.29684822774950637 L-5.19873165793353,-0.23251042155326518 L-5.060303999275629,-0.17109492693702677 L-4.915211709120951,-0.11274969920668321 L-4.7638043275050626,-0.05761529712627622 L-4.606446608071997,-0.0058245442996198715 L-4.443517639350778,0.04249779081339189 L-4.275409931497945,0.08723529547493514 L-4.102528470706213,0.12828019311773753 L-3.925289743557257,0.16553360298826902 L-3.7441207336690576,0.19890577835913859 L-3.559457893054966,0.22831632273682012 L-3.371746090672577,0.25369438354384855 L-3.1814375406954407,0.2749788228088841 L-2.9889907130895135,0.29211836445344064 L-2.7948692291188486,0.3050717178204496 L-2.599540744441365,0.31380767714707036 L-2.4034758224854063,0.31830519674210533 L-2.2071468008212225,0.31855344168691424 L-2.0110266532583942,0.3145518139376806 L-1.8155878504104965,0.30630995376615444 L-1.6213012214720073,0.2938477165353899 L-1.4286348199495378,0.27719512486643927 L-1.2380527960799401,0.25639229631122795 L-1.050014278651729,0.2314893467058574 L-0.8649722689236186,0.20254626943716847 L-0.6833725493048093,0.16963279091341543 L-0.5056526094261198,0.13282820258724182 L-0.33224059218914626,0.09222116993562679 L-0.16355426233251125,0.047909518856984246 L-3.108624468950438e-14,9.547918011776346e-15 " />
			<path d="M-1.687538997430238e-14,4.884981308350689e-15 L0.19238380234804042,-0.06328258384711405 L0.37581853876742466,-0.1315405562792602 L0.4639723507588691,-0.16745921058195212 L0.5496439455454794,-0.2045282263047692 L0.6327562131732773,-0.24271423894570288 L0.7132343472475875,-0.2819828786335623 L0.7910059122636186,-0.3222988010630776 L0.8660009088030787,-0.3636257193070489 L0.9381518365381587,-0.40592643647691706 L1.0073937549861824,-0.4491628792023621 L1.07366434196022,-0.49329613189978805 L1.1369039496630688,-0.5382864717988526 L1.1970556583741172,-0.5840934046955233 L1.2540653276807592,-0.6306757013994683 L1.3078816452082496,-0.6779914348429807 L1.3584561728041504,-0.7259980178180434 L1.4057433901357879,-0.7746522413075593 L1.4497007356614828,-0.82391031337625 L1.4902886449386803,-0.8737278985862165 L1.5274705862344953,-0.9240601579016903 L1.561213093406629,-0.9748617890470568 L1.5914857960250504,-1.0260870672818179 L1.6182614467073382,-1.077689886555805 L1.6415159456430817,-1.1296238010075932 L1.6612283622852644,-1.1818420667687717 L1.6773809541891023,-1.2342976840364341 L1.689959182981386,-1.2869434393760264 L1.6989517274459565,-1.3397319482164844 L1.7043504937135272,-1.3926156974993973 L1.7061506225466867,-1.4455470884438104 " />
			<path d="M-6.293849377453313,-1.4455470884438157 L-6.2909357765178395,-1.3782112434905034 L-6.282199218246623,-1.3109734934276145 L-6.267652430061841,-1.2439317902408902 L-6.247316603731324,-1.177183800314891 L-6.221221364496383,-1.1108267621525612 L-6.189404727913741,-1.0449573447181337 L-6.151913044474454,-0.9796715066097363 L-6.108800932080491,-0.9150643562668621 L-6.060131196477354,-0.8512300134163495 L-6.005974739758632,-0.788261471958721 L-5.946410457075807,-0.7262504644946248 L-5.881525121703751,-0.6652873286887394 L-5.811413258629381,-0.6054608756658213 L-5.73617700684762,-0.5468582606306176 L-5.655925970565253,-0.4895648559001222 L-5.570777059529477,-0.43366412653314623 " />
			<path d="M-10.322322198539908,1.3925436952008776 L-10.32232219853991,-66.81318642787326 " />
			<path d="M-10.32232219853991,-66.81318642787326 L-10.32232219853991,-68.608074062691 " />
			<path d="M-10.32232219853991,-68.608074062691 L-9.175397509813253,-67.8853005184691 " />
			<path d="M-9.175397509813251,2.833272293349882 L-9.175397509813253,-67.8853005184691 " />
			<path d="M10.650014966747525,-5.0835072610274255 L10.32232219853991,-4.982318964836358 " />
			<path d="M-10.650014966747525,1.4937319913919456 L-10.790347048948027,1.4034757813749097 L-10.926748927613808,1.3120546209492676 L-11.059170920640735,1.219501808744459 L-11.187564795531497,1.1258510555751589 L-11.311883786963474,1.0311364721626852 L-11.432082613822221,0.935392556710746 L-11.548117495694374,0.8386541823400291 L-11.659946168813923,0.7409565843862616 L-11.76752790145607,0.6423353475663307 L-11.870823508773105,0.5428263930171353 L-11.969795367066817,0.44246596521191583 L-12.064407427492288,0.3412906187588216 L-12.154625229188103,0.23933720508648748 L-12.240415911828132,0.13664285902152784 L-12.321748227590344,0.03324498526280206 L-12.398592552538325,-0.07081875524263626 L-12.470920897411295,-0.17551045901690188 L-12.538706917818706,-0.2807919938569787 L-12.601925923835784,-0.38662501272375205 L-12.660554888996392,-0.4929709677092706 L-12.714572458680045,-0.5997911240771681 L-12.763958957889978,-0.7070465743711585 L-12.808696398419427,-0.8146982525864216 L-12.848768485403536,-0.922706948398731 L-12.884160623254491,-1.031033321446178 L-12.914859920977715,-1.13963791565823 L-12.940855196867199,-1.2484811736269392 L-12.962136982578256,-1.3575234510150822 L-12.978697526576198,-1.4667250309959379 L-12.990530796959709,-1.576046138719472 L-12.997632483657862,-1.6854469557996754 L-12.999999999999998,-1.7948876348177127 " />
			<path d="M-12.999999999999998,-1.794887634817738 L-12.997458923101599,-1.908268493164945 L-12.989836685802064,-2.0216050269767876 L-12.977136267900026,-2.1348529290459104 L-12.959362634432182,-2.247967926814199 L-12.936522733732287,-2.3609057996804705 L-12.908625494714807,-2.4736223962878485 L-12.875681823384294,-2.586073651784071 L-12.837704598571856,-2.6982156050479755 L-12.794708666900354,-2.810004415875445 L-12.746710836980357,-2.9213963821180666 L-12.693729872839066,-3.032347956767826 L-12.635786486584792,-3.1428157649811554 L-12.572903330309876,-3.252756621035675 L-12.505104987235196,-3.362127545213 L-12.43241796209973,-3.4708857806010087 L-12.354870670798922,-3.5789888098090152 L-12.272493429275917,-3.6863943715893033 L-12.185318441670006,-3.793060477358517 L-12.0933797877269,-3.898945427612471 L-11.99671340947577,-4.004007828227936 L-11.895357097178254,-4.108206606645052 L-11.78935047455491,-4.211501027924028 L-11.678734983294948,-4.313850710669835 L-11.563553866855205,-4.415215642818725 L-11.443852153554777,-4.515556197280328 L-11.319676638971872,-4.614833147429275 L-11.191075867649793,-4.713007682440245 L-11.058100114119172,-4.810041422460482 L-10.920801363243909,-4.905896433613811 L-10.77923328989847,-5.000535242830319 L-10.633451237984508,-5.093920852495884 L-10.483512198794992,-5.186016754915833 L-10.329474788734332,-5.276786946587079 L-10.171399226403171,-5.366195942273144 L-10.009347309056837,-5.4542087888765725 L-9.843382388446644,-5.5407910791033235 L-9.673569346053467,-5.625908964913782 L-9.499974567723317,-5.709529170755134 L-9.322665917714797,-5.7916190065699515 L-9.141712712168584,-5.872146380575866 L-8.95718569200934,-5.951079811811375 L-8.769156995290619,-6.028388442442839 L-8.577700128993564,-6.104042049827904 L-8.382889940290477,-6.178011058330567 L-8.184802587284453,-6.250266550883334 L-7.983515509236505,-6.320780280291913 L-7.779107396291859,-6.389524680278023 L-7.571658158717232,-6.456472876256017 L-7.361248895661114,-6.521598695839098 L-7.147961863449282,-6.584876679071016 L-6.931880443427937,-6.64628208837925 L-6.713089109367012,-6.705790918245797 L-6.49167339443644,-6.76337990459176 L-6.2677198577682445,-6.819026533872093 L-6.041316050617555,-6.87270905187693 L-5.812550482135764,-6.924406472236059 L-5.581512584769216,-6.974098584623241 L-5.348292679296931,-7.021765962657116 L-5.112981939521071,-7.067389971495667 L-4.8756723566239115,-7.110952775121219 L-4.636456703205278,-7.15243734331317 L-4.3954284970145,-7.191827458305692 L-4.152681964391055,-7.229107721127828 L-3.9083120034282204,-7.264263557623479 L-3.6624141468740548,-7.297281224148961 L-3.415084524784341,-7.3281478129458675 L-3.16641982694201,-7.356851257187162 L-2.9165172650576987,-7.383380335694529 L-2.665474534766307,-7.407724677325115 L-2.413389777434367,-7.429874765025978 L-2.1603615417931543,-7.449821939554636 L-1.9064887454125505,-7.467558402864256 L-1.6518706360307125,-7.483077221152199 L-1.3966067527546648,-7.496372327570673 L-1.1407968871469905,-7.507438524598481 L-0.8845410442138246,-7.516271486072911 L-0.6279394033094069,-7.522867758880987 L-0.37109227897247477,-7.527224764309412 L-0.11410008170980857,-7.529340799052668 L0.14293672125774048,-7.52921503587891 L0.399917645271394,-7.5268475239533545 L0.6567422275174073,-7.5222391888190545 L0.9133100663014903,-7.515391832035081 L1.1695208602993339,-7.506308130472222 L1.4252744477679002,-7.494991635266511 L1.6804708457021433,-7.481446770430951 L1.9350102889218563,-7.4656788311260245 L2.188793269073351,-7.447693981589623 L2.4417205735307825,-7.4274992527272365 L2.6936933241818024,-7.405102539363323 L2.944613016082446,-7.380512597154949 L3.1943815559661823,-7.353739039168895 L3.44290130059199,-7.324792332123575 L3.690075094916506,-7.2936837922972275 L3.935806310075321,-7.260425581103992 L4.179998881158582,-7.225030700339583 L4.422557344766112,-7.187512987098435 L4.663386876327391,-7.147887108364301 L4.902393327171788,-7.10616855527642 L5.139483261334564,-7.0623736370734775 L5.37456399208425,-7.0165194747177715 L5.607543618157126,-6.968623994202016 L5.83833105968464,-6.918705919541455 L6.066836093799696,-6.866784765453985 L6.292969389907933,-6.812880829731173 L6.516642544610165,-6.757015185303145 L6.7377681162623615,-6.699209672000431 L6.956259659159634,-6.639486888016027 L7.172031757330884,-6.577870181070959 L7.38500005793088,-6.514383639286858 L7.595081304216739,-6.449052081769056 L7.802193368095882,-6.38190104890395 L8.006255282232793,-6.312956792374355 L8.207187271701963,-6.242246264896813 L8.404910785174678,-6.169797109684842 L8.5993485256275,-6.095637649642228 L8.79042448056036,-6.019796876290621 L8.9780639517125,-5.94230443843573 L9.162193584264633,-5.863190630576578 L9.3427413955159,-5.7824863810623155 L9.519636803024415,-5.700223240001258 L9.692810652200423,-5.6164333669268425 L9.86219524334122,-5.531149518225345 L10.02772435809735,-5.444405034330264 L10.18933328535965,-5.35623382668838 L10.346958846557103,-5.266670364502596 L10.500539420355528,-5.175749661256709 L10.650014966747458,-5.083507261027469 " />
			<path d="M-10.32232219853991,1.3925436952008772 L-10.650014966747525,1.493731991391945 " />
			<path d="M-3.6455820463097295,-2.823033001473405 L-3.7138095245784646,-2.8697255817886127 L-3.7737656219566182,-2.918577572362588 L-3.8251010894042574,-2.9693044064614553 L-3.867516893737024,-3.0216105962385638 L-3.885300640099534,-3.0482610457549995 L-3.90076595951824,-3.075191453974713 L-3.9138903221085797,-3.1023625886664146 L-3.924654608292993,-3.1297348669083758 L-3.933043136654331,-3.1572684127528503 L-3.9390436867805536,-3.184923115317374 L-3.94264751706743,-3.212658687218316 L-3.943849377453313,-3.240434723261554 " />
			<path d="M-3.943849377453313,-3.240434723261557 L-3.9418618801918477,-3.276149242182835 L-3.9359041764624383,-3.3117777216998094 L-3.925990618895202,-3.3472343296846376 L-3.912145090118644,-3.3824336480630515 L-3.8944009452243114,-3.417290878593982 L-3.872800931411458,-3.451722047155947 L-3.847397085005298,-3.485644206048067 L-3.818250606096937,-3.5189756338183393 L-3.7854317111069955,-3.5516360321377785 L-3.749019463628099,-3.5835467192461197 L-3.709101583953762,-3.6146308195030725 L-3.6657742377525135,-3.6448134485884722 L-3.619141804396378,-3.6740218939051665 L-3.56931662550183,-3.702185789750029 L-3.5164187342889965,-3.7292372868311046 L-3.4605755664111175,-3.7551112157224935 L-3.401921652950894,-3.779745243863207 L-3.340598296323329,-3.8030800257217683 L-3.2767532298658293,-3.8250593457647954 L-3.210540261935658,-3.845630253885143 L-3.0716539932162097,-3.882352118255083 L-2.925277040855712,-3.912891967203492 L-2.772819094923178,-3.936955685290218 L-2.6157484087799254,-3.9543115257555197 L-2.455577658997088,-3.964792342368048 L-2.2938493774533137,-3.9682971991344274 L-2.132121095909539,-3.964792342368048 L-1.9719503461267016,-3.9543115257555197 L-1.8148796599834496,-3.936955685290218 L-1.662421714050915,-3.912891967203492 L-1.5160447616904174,-3.882352118255083 L-1.3771584929709704,-3.8456302538851435 L-1.310945525040799,-3.8250593457647963 L-1.2471004585832992,-3.803080025721769 L-1.1857771019557342,-3.779745243863208 L-1.1271231884955102,-3.755111215722494 L-1.0712800206176303,-3.729237286831105 L-1.018382129404797,-3.7021857897500294 L-0.9685569505102489,-3.6740218939051665 L-0.9219245171541137,-3.6448134485884727 L-0.8785971709528646,-3.614630819503073 L-0.8386792912785279,-3.58354671924612 L-0.8022670437996322,-3.5516360321377793 L-0.7694481488096907,-3.51897563381834 L-0.7403016699013296,-3.4856442060480677 L-0.7148978234951693,-3.4517220471559487 L-0.6932978096823161,-3.4172908785939837 L-0.6755536647879834,-3.382433648063053 L-0.6617081360114248,-3.347234329684638 L-0.6517945784441885,-3.3117777216998103 L-0.6458368747147789,-3.276149242182836 L-0.6438493774533134,-3.2404347232615645 " />
			<path d="M-0.6438493774533134,-3.240434723261558 L-0.6451393365630511,-3.2116590542567556 L-0.6490071969292286,-3.1829283785081612 L-0.6554469108164338,-3.154287618921121 L-0.6644484091730394,-3.1257815578092587 L-0.675997617375037,-3.0974547668734393 L-0.690076477232936,-3.0693515375100473 L-0.7066629752273075,-3.041515811557544 L-0.7257311769288346,-3.013991112589588 L-0.7472512675490433,-2.9868204778621514 L-0.7711895985583115,-2.9600463910210326 L-0.8261675405063065,-2.9078546299383556 L-0.8903212860458798,-2.8577421271376715 L-0.9632497522216412,-2.8100221810952615 L-1.0444969973812395,-2.7649931322560795 L-1.13355507167807,-2.722936497838411 L-1.229867192724138,-2.6841152118156986 L-1.3328312265392035,-2.6487719810790074 L-1.4418034520336542,-2.6171277680572276 L-1.5561025854899273,-2.5893804092815405 L-1.675014039881816,-2.5657033785307317 L-1.7977943924028086,-2.54624470229006 L-1.9236760322729143,-2.531126034304119 L-2.0518719597663364,-2.5204418950095 L-2.1815807064569435,-2.5142590806022476 L-2.311991345920642,-2.512616245434563 L-2.442288563568228,-2.515523660351566 L-2.5716577539126235,-2.5229631484789725 L-2.6992901134028684,-2.534888198863142 L-2.82438769698498,-2.5512242572530166 L-2.946168406776547,-2.571869192206022 L-3.0638708816663516,-2.5966939336038806 L-3.176759257269728,-2.6255432795863904 L-3.2841277664808675,-2.6582368668583083 L-3.385305151859882,-2.6945702983030655 L-3.479658862268793,-2.7343164208535926 L-3.5665990075195153,-2.7772267456311224 L-3.6455820463097255,-2.8230330014734024 " />
			<path d="M10.322322198539908,-4.982318964836358 L10.322322198539906,-73.18804908791049 " />
			<path d="M10.322322198539906,-73.18804908791049 L10.322322198539906,-74.98293672272823 " />
			<path d="M10.322322198539906,-74.98293672272823 L11.469246887266562,-74.26016317850632 " />
			<path d="M11.469246887266564,-2.4646577857967094 L11.469246887266562,-74.26016317850632 " />
			<path d="M-9.994629430332292,4.163175614718194 L-9.994629430332294,-67.63232977799142 " />
			<path d="M-9.175397509813253,-67.8853005184691 L-9.994629430332294,-67.63232977799143 " />
			<path d="M-11.387323695214661,4.054759583084909 L-11.387323695214663,-67.74074580962471 " />
			<path d="M-11.387323695214663,-67.7407458096247 L-9.994629430332294,-67.63232977799142 " />
			<path d="M-11.960786039577991,-68.10213258173566 L-11.387323695214663,-67.7407458096247 " />
			<path d="M-11.960786039577991,3.6933728109739548 L-11.960786039577993,-68.10213258173566 " />
			<path d="M-11.960786039577995,-68.10213258173566 L-12.11838976266471,-68.20349724837018 L-12.27157956485859,-68.30617024392512 L-12.420299649334984,-68.41011417147823 L-12.564495847289225,-68.51529117119144 L-12.704115637666675,-68.62166293410083 L-12.839108166292654,-68.72919071606994 L-12.969424264395226,-68.83783535190166 L-13.095016466514101,-68.94755726960358 L-13.21583902778913,-69.05831650480135 L-13.331847940622108,-69.17007271529506 L-13.443000950705814,-69.28278519575323 L-13.54925757241442,-69.39641289253902 L-13.65057910354972,-69.51091441866333 L-13.746928639437751,-69.62624806885935 L-13.8382710863707,-69.74237183477301 L-13.924573174389202,-69.85924342026372 L-14.005803469400382,-69.97682025681021 L-14.081932384627168,-70.09505951901522 L-14.15293219138481,-70.21391814020406 L-14.218777029180568,-70.33335282811088 L-14.27944291513298,-70.45332008064713 L-14.334907752707212,-70.57377620174653 L-14.385151339763363,-70.6946773172806 L-14.430155375914746,-70.81597939103904 L-14.46990346919351,-70.93763824076925 L-14.504381142021131,-71.05960955426893 L-14.53357583648163,-71.1818489055261 L-14.557476918895585,-71.30431177090047 L-14.576075683693274,-71.42695354534051 L-14.589365356585525,-71.54972955863002 L-14.597341097031142,-71.67259509165856 L-14.600000000000003,-71.79550539270959 " />
			<path d="M12.288478807785605,-2.7176285262743773 L12.288478807785603,-74.513133918984 " />
			<path d="M12.534248383941316,-75.12749143157261 L12.288478807785603,-74.51313391898398 " />
			<path d="M12.288478807785603,-74.513133918984 L11.469246887266564,-74.26016317850632 " />
			<path d="M-4.317000528868546,3.666401128475622 L-4.105537460624087,3.7173818504517406 L-3.887498782587298,3.7626527348633676 L-3.663675876718308,3.802049468839205 L-3.4348811191127897,3.835429060021946 L-3.201944931443501,3.8626703555659736 L-2.9657127669045407,3.8836744818674935 L-2.727042041597961,3.898365203431074 L-2.486799022500427,3.906689199570077 L-2.245855683305198,3.908616257936674 L-2.0050865395513044,3.9041393841790337 L-1.7653654745269718,3.8932748273276543 L-1.527562567467828,3.8760620208187255 L-1.292540935562107,3.852563439368554 L-1.0611536012249387,3.822864372218553 L-0.8342403960121099,3.7870726135738 L-0.6126249124106862,3.745318071358741 L-0.3971115145701254,3.6977522957100772 L-0.18848241882357186,3.6445479289181906 L0.012505145404274387,3.5858980788135737 L0.20512168399809028,3.522015617872592 L0.3886680858862137,3.4531324105865036 L0.47683044808290953,3.416892972108305 L0.5624781604981965,3.379498471898038 L0.6455334898626717,3.3409828489445803 L0.7259210557357982,3.3013810597600313 L0.8035678989206736,3.260729046653421 L0.8784035476812853,3.2190637051097237 L0.9503600817021689,3.176422850303772 L1.0193721937324178,3.1328451827794637 L1.0853772488580913,3.0883702533254196 L1.1483153413492269,3.04303842707896 L1.2081293490298632,2.996890846890988 L1.2647649851217317,2.9499693959850233 L1.3181708475145615,2.902316659944277 L1.368298465418278,2.853975888061274 L1.415102343354751,2.8049909540850955 L1.4585400024491793,2.755406316401869 L1.4985720189836225,2.7052669776846416 L1.5351620601776927,2.6546184440492704 L1.5682769171639328,2.6035066837533893 L1.5978865351279556,2.551978085475931 L1.6239640405859865,2.5000794162150877 L1.6464857657750422,2.447857778842918 " />
			<path d="M-10.650014966747525,1.493731991391945 L-10.650014966747527,-66.7119981316822 " />
			<path d="M-10.322322198539911,-66.81318642787325 L-10.650014966747527,-66.71199813168218 " />
			<path d="M10.322322198539908,-73.18804908791049 L-10.322322198539911,-66.81318642787325 " />
			<path d="M-1.9539925233402755e-14,-71.79550539270961 L-10.32232219853991,-68.608074062691 " />
			<path d="M10.322322198539908,-74.98293672272823 L-1.9539925233402755e-14,-71.79550539270961 " />
			<path d="M-5.570777059529476,-72.22916951924276 L-5.454276002414904,-72.15945874282491 L-5.33016120074012,-72.09235362045912 L-5.198731657933532,-72.02801581426289 L-5.0603039992756305,-71.96660031964664 L-4.915211709120953,-71.9082550919163 L-4.763804327505065,-71.85312068983589 L-4.606446608072,-71.80132993700923 L-4.44351763935078,-71.75300760189623 L-4.275409931497947,-71.70827009723467 L-4.102528470706216,-71.66722519959188 L-3.9252897435572596,-71.62997178972134 L-3.74412073366906,-71.59659961435048 L-3.5594578930549683,-71.5671890699728 L-3.371746090672579,-71.54181100916577 L-3.181437540695443,-71.52052656990072 L-2.9889907130895157,-71.50338702825617 L-2.794869229118851,-71.49043367488916 L-2.5995407444413674,-71.48169771556255 L-2.4034758224854085,-71.47720019596751 L-2.2071468008212247,-71.4769519510227 L-2.0110266532583965,-71.48095357877193 L-1.8155878504104987,-71.48919543894345 L-1.6213012214720095,-71.50165767617422 L-1.42863481994954,-71.51831026784318 L-1.2380527960799423,-71.53911309639838 L-1.0500142786517312,-71.56401604600376 L-0.8649722689236208,-71.59295912327245 L-0.6833725493048115,-71.6258726017962 L-0.505652609426122,-71.66267719012237 L-0.3322405921891485,-71.70328422277399 L-0.16355426233251347,-71.74759587385263 L-3.3306690738754696e-14,-71.7955053927096 " />
			<path d="M-1.9095836023552692e-14,-71.79550539270961 L0.1923838023480382,-71.85878797655673 L0.37581853876742244,-71.92704594898888 L0.4639723507588669,-71.96296460329157 L0.5496439455454771,-72.00003361901439 L0.6327562131732751,-72.03821963165532 L0.7132343472475853,-72.07748827134317 L0.7910059122636164,-72.11780419377268 L0.8660009088030765,-72.15913111201667 L0.9381518365381565,-72.20143182918653 L1.0073937549861802,-72.24466827191198 L1.0736643419602179,-72.2888015246094 L1.1369039496630666,-72.33379186450847 L1.197055658374115,-72.37959879740514 L1.254065327680757,-72.42618109410908 L1.3078816452082473,-72.4734968275526 L1.3584561728041482,-72.52150341052766 L1.4057433901357856,-72.57015763401718 L1.4497007356614806,-72.61941570608586 L1.490288644938678,-72.66923329129582 L1.527470586234493,-72.7195655506113 L1.5612130934066268,-72.77036718175667 L1.5914857960250481,-72.82159245999144 L1.618261446707336,-72.87319527926542 L1.6415159456430795,-72.92512919371721 L1.6612283622852622,-72.97734745947838 L1.6773809541891,-73.02980307674605 L1.6899591829813838,-73.08244883208565 L1.6989517274459542,-73.1352373409261 L1.704350493713525,-73.18812109020901 L1.7061506225466845,-73.24105248115343 " />
			<path d="M1.7061506225466845,-73.24105248115343 L1.7049458973315015,-73.28435584928349 L1.701332447367374,-73.32763313308381 L1.6953124492614453,-73.37085826393685 L1.6868895292354718,-73.4140052046401 L1.6760687609415243,-73.45704796508984 L1.662856662405808,-73.49996061793665 L1.6472611921024494,-73.54271731420307 L1.6292917441596062,-73.58529229885403 L1.6089591427007988,-73.62765992631076 L1.5862756353248604,-73.6697946758987 L1.5612548857284443,-73.71167116722025 L1.5339119654755198,-73.75326417544287 L1.5042633449188303,-73.79454864649367 L1.4723268832787668,-73.83549971215103 L1.401668752591831,-73.9163031734123 L1.3221077950404574,-73.99547989661093 L1.2338356799401038,-74.0728391380857 L1.1370650625477712,-74.14819453264802 L1.032029071756864,-74.22136454255201 L0.9189807484692634,-74.2921728948349 L0.7981924359976307,-74.36044900597398 L0.6699551239665182,-74.42602839283718 L0.5345777472928726,-74.48875306893753 L0.39238644193475647,-74.54847192503622 L0.2437237592012651,-74.60504109317819 L0.08894784051641702,-74.65832429328249 L-0.07156844537490992,-74.70819316145304 L-0.2374384006804342,-74.75452755921839 L-0.4082624301493303,-74.79721586295592 L-0.5836290037321921,-74.83615523280288 L-0.7631156479929608,-74.8712518604066 L-0.9462899638844391,-74.90242119491711 L-1.1327106684354693,-74.92958814667746 L-1.3219286578402625,-74.9526872681213 L-1.5134880893888045,-74.97166291144183 L-1.7069274796318699,-74.98646936265222 L-1.9017808161350738,-74.99707095171462 L-2.0975786801436436,-75.0034421384724 L-2.2938493774533186,-75.00556757417857 L-2.4901200747629932,-75.00344213847238 L-2.685917938771563,-74.99707095171462 L-2.8807712752747667,-74.98646936265222 L-3.0742106655178323,-74.97166291144183 L-3.2657700970663743,-74.9526872681213 L-3.4549880864711673,-74.92958814667746 L-3.6414087910221973,-74.90242119491711 L-3.8245831069136758,-74.8712518604066 L-4.004069751174444,-74.83615523280287 L-4.179436324757306,-74.79721586295592 L-4.350260354226202,-74.75452755921839 L-4.516130309531726,-74.70819316145304 L-4.676646595423053,-74.65832429328249 L-4.831422514107901,-74.60504109317819 L-4.980085196841392,-74.54847192503621 L-5.122276502199508,-74.48875306893751 L-5.257653878873153,-74.42602839283718 L-5.385891190904264,-74.36044900597398 L-5.506679503375896,-74.2921728948349 L-5.619727826663498,-74.22136454255201 L-5.7247638174544075,-74.148194532648 L-5.821534434846738,-74.0728391380857 L-5.909806549947091,-73.99547989661093 L-5.989367507498464,-73.91630317341229 L-6.0600256381854,-73.83549971215103 L-6.091962099825463,-73.79454864649367 L-6.121610720382152,-73.75326417544287 L-6.148953640635076,-73.71167116722025 L-6.173974390231492,-73.6697946758987 L-6.19665789760743,-73.62765992631076 L-6.216990499066238,-73.58529229885403 L-6.234959947009081,-73.54271731420307 L-6.250555417312439,-73.49996061793665 L-6.263767515848155,-73.45704796508984 L-6.274588284142103,-73.4140052046401 L-6.283011204168076,-73.37085826393685 L-6.289031202274005,-73.32763313308381 L-6.292644652238133,-73.28435584928349 L-6.2938493774533155,-73.24105248115345 " />
			<path d="M-6.2938493774533155,-73.24105248115343 L-6.290935776517841,-73.17371663620011 L-6.2821992182466255,-73.10647888613723 L-6.267652430061844,-73.03943718295051 L-6.247316603731327,-72.97268919302451 L-6.221221364496386,-72.90633215486217 L-6.189404727913744,-72.84046273742774 L-6.1519130444744565,-72.77517689931935 L-6.108800932080493,-72.71056974897648 L-6.060131196477355,-72.64673540612597 L-6.005974739758635,-72.58376686466833 L-5.946410457075809,-72.52175585720424 L-5.881525121703753,-72.46079272139835 L-5.811413258629383,-72.40096626837544 L-5.7361770068476226,-72.34236365334023 L-5.655925970565256,-72.28507024860974 L-5.57077705952948,-72.22916951924276 " />
			<path d="M10.650014966747523,-73.28923738410155 L10.322322198539908,-73.18804908791049 " />
			<path d="M10.650014966747523,-5.083507261027426 L10.650014966747522,-73.28923738410155 " />
			<path d="M-10.650014966747529,-66.7119981316822 L-10.79034704894803,-66.80225434169922 L-10.926748927613811,-66.89367550212486 L-11.059170920640739,-66.98622831432968 L-11.1875647955315,-67.07987906749898 L-11.311883786963477,-67.17459365091145 L-11.432082613822224,-67.2703375663634 L-11.548117495694378,-67.36707594073411 L-11.659946168813926,-67.46477353868788 L-11.767527901456074,-67.5633947755078 L-11.870823508773109,-67.662903730057 L-11.969795367066821,-67.76326415786222 L-12.064407427492291,-67.86443950431531 L-12.154625229188106,-67.96639291798765 L-12.240415911828135,-68.06908726405261 L-12.321748227590348,-68.17248513781134 L-12.398592552538329,-68.27654887831677 L-12.470920897411299,-68.38124058209104 L-12.53870691781871,-68.48652211693111 L-12.601925923835788,-68.59235513579789 L-12.660554888996396,-68.6987010907834 L-12.714572458680049,-68.8055212471513 L-12.763958957889981,-68.9127766974453 L-12.80869639841943,-69.02042837566056 L-12.84876848540354,-69.12843707147286 L-12.884160623254495,-69.2367634445203 L-12.914859920977719,-69.34536803873236 L-12.940855196867203,-69.45421129670108 L-12.96213698257826,-69.56325357408922 L-12.978697526576202,-69.67245515407008 L-12.990530796959712,-69.78177626179361 L-12.997632483657865,-69.89117707887381 L-13.000000000000002,-70.00061775789185 " />
			<path d="M-13.000000000000002,-70.00061775789187 L-12.997458923101602,-70.11399861623907 L-12.989836685802068,-70.22733515005092 L-12.977136267900029,-70.34058305212004 L-12.959362634432186,-70.45369804988833 L-12.936522733732291,-70.5666359227546 L-12.90862549471481,-70.67935251936198 L-12.875681823384298,-70.79180377485821 L-12.83770459857186,-70.90394572812211 L-12.794708666900357,-71.01573453894957 L-12.74671083698036,-71.1271265051922 L-12.69372987283907,-71.23807807984196 L-12.635786486584795,-71.34854588805528 L-12.57290333030988,-71.4584867441098 L-12.5051049872352,-71.56785766828713 L-12.432417962099734,-71.67661590367514 L-12.354870670798926,-71.78471893288315 L-12.27249342927592,-71.89212449466343 L-12.18531844167001,-71.99879060043266 L-12.093379787726903,-72.10467555068661 L-11.996713409475774,-72.20973795130207 L-11.895357097178257,-72.31393672971919 L-11.789350474554913,-72.41723115099816 L-11.678734983294952,-72.51958083374397 L-11.563553866855209,-72.62094576589286 L-11.443852153554781,-72.72128632035447 L-11.319676638971876,-72.82056327050341 L-11.191075867649797,-72.91873780551438 L-11.058100114119176,-73.01577154553462 L-10.920801363243912,-73.11162655668795 L-10.779233289898473,-73.20626536590446 L-10.633451237984511,-73.29965097557002 L-10.483512198794996,-73.39174687798997 L-10.329474788734336,-73.48251706966121 L-10.171399226403175,-73.57192606534728 L-10.00934730905684,-73.6599389119507 L-9.843382388446647,-73.74652120217746 L-9.67356934605347,-73.83163908798791 L-9.49997456772332,-73.91525929382927 L-9.3226659177148,-73.99734912964409 L-9.141712712168587,-74.07787650365 L-8.957185692009343,-74.1568099348855 L-8.769156995290622,-74.23411856551698 L-8.577700128993568,-74.30977217290204 L-8.38288994029048,-74.3837411814047 L-8.184802587284457,-74.45599667395747 L-7.983515509236507,-74.52651040336605 L-7.77910739629186,-74.59525480335216 L-7.571658158717233,-74.66220299933015 L-7.361248895661116,-74.72732881891324 L-7.147961863449284,-74.79060680214515 L-6.931880443427938,-74.85201221145338 L-6.713089109367014,-74.91152104131993 L-6.491673394436442,-74.96911002766589 L-6.267719857768246,-75.02475665694622 L-6.0413160506175565,-75.07843917495106 L-5.812550482135766,-75.13013659531019 L-5.581512584769218,-75.17982870769737 L-5.348292679296933,-75.22749608573125 L-5.112981939521073,-75.2731200945698 L-4.875672356623913,-75.31668289819535 L-4.63645670320528,-75.3581674663873 L-4.3954284970145014,-75.39755758137983 L-4.152681964391057,-75.43483784420197 L-3.9083120034282226,-75.46999368069761 L-3.662414146874057,-75.5030113472231 L-3.4150845247843433,-75.53387793602 L-3.166419826942012,-75.56258138026129 L-2.916517265057701,-75.58911045876866 L-2.665474534766309,-75.61345480039925 L-2.4133897774343693,-75.63560488810012 L-2.1603615417931565,-75.65555206262877 L-1.9064887454125525,-75.67328852593839 L-1.6518706360307145,-75.68880734422633 L-1.3966067527546668,-75.7021024506448 L-1.1407968871469925,-75.71316864767262 L-0.8845410442138267,-75.72200160914704 L-0.627939403309409,-75.72859788195512 L-0.3710922789724769,-75.73295488738354 L-0.11410008170981067,-75.7350709221268 L0.14293672125773838,-75.73494515895304 L0.3999176452713919,-75.73257764702748 L0.6567422275174052,-75.72796931189319 L0.9133100663014881,-75.72112195510921 L1.1695208602993319,-75.71203825354635 L1.4252744477678982,-75.70072175834065 L1.6804708457021413,-75.68717689350508 L1.9350102889218543,-75.67140895420016 L2.188793269073349,-75.65342410466376 L2.4417205735307803,-75.63322937580136 L2.6936933241818,-75.61083266243746 L2.9446130160824437,-75.58624272022908 L3.19438155596618,-75.55946916224303 L3.4429013005919877,-75.53052245519771 L3.6900750949165038,-75.49941391537136 L3.9358063100753187,-75.46615570417812 L4.17999888115858,-75.43076082341372 L4.42255734476611,-75.39324311017256 L4.663386876327389,-75.35361723143843 L4.9023933271717866,-75.31189867835056 L5.139483261334562,-75.26810376014761 L5.374563992084248,-75.2222495977919 L5.607543618157124,-75.17435411727615 L5.838331059684638,-75.12443604261559 L6.066836093799695,-75.07251488852812 L6.292969389907931,-75.0186109528053 L6.516642544610163,-74.96274530837728 L6.73776811626236,-74.90493979507457 L6.956259659159632,-74.84521701109016 L7.172031757330882,-74.7836003041451 L7.3850000579308785,-74.720113762361 L7.5950813042167375,-74.65478220484319 L7.80219336809588,-74.58763117197809 L8.00625528223279,-74.51868691544848 L8.20718727170196,-74.44797638797095 L8.404910785174675,-74.37552723275897 L8.599348525627496,-74.30136777271636 L8.790424480560356,-74.22552699936476 L8.978063951712496,-74.14803456150986 L9.16219358426463,-74.06892075365072 L9.342741395515896,-73.98821650413645 L9.519636803024412,-73.9059533630754 L9.69281065220042,-73.82216349000097 L9.862195243341217,-73.73687964129948 L10.027724358097347,-73.65013515740439 L10.189333285359647,-73.56196394976251 L10.346958846557099,-73.47240048757673 L10.500539420355524,-73.38147978433085 L10.650014966747454,-73.2892373841016 " />
			<path d="M-3.6455820463097295,2.5616299029798157 L-3.687005738727623,2.53422577445848 L-3.725576514423694,2.5060230057512842 L-3.761215387855461,2.4770793507132023 L-3.7938493774533097,2.447454080392157 " />
			<path d="M-0.7938493774533135,2.4474540803921534 L-0.8421841598018829,2.490217178446785 L-0.8967754446916156,2.5314891055246513 L-0.9573879502486442,2.5710919845825457 L-1.0237604438620105,2.608855131973544 L-1.0956068680648094,2.6446157930729965 L-1.1726175734074764,2.6782198437313953 L-1.254460653009682,2.7095224545309224 L-1.3407833730390784,2.73838871498283 L-1.431213692951705,2.7646942149754237 L-1.525361868941998,2.788325580966684 L-1.6228221336917317,2.809180964610604 L-1.7231744451783686,2.8271704817113097 L-1.825986297005672,2.842216599613141 L-1.9308145824542704,2.8542544713570726 L-2.037207504218339,2.8632322151633107 L-2.1447065215976635,2.8691111380355263 L-2.2528483267529236,2.871865902523017 L-2.3611668415067735,2.871484635922071 L-2.4691952260847434,2.8679689814458964 L-2.576467891138539,2.8613340911425658 L-2.6825225043801457,2.8516085605915134 L-2.786901983178403,2.8388343056600247 L-2.8891564645301853,2.823066381850891 L-2.9888452439158524,2.8043727470198077 L-3.0855386746827413,2.782833968485191 L-3.1788200197705763,2.7585428757927217 L-3.268287247798095,2.731604160631166 L-3.353554765769956,2.702133925623783 L-3.434255080936191,2.6702591839399803 L-3.5100403846417656,2.6361173118838246 L-3.5805840513400664,2.5998554568186902 L-3.6455820463097255,2.5616299029798184 " />
			<path d="M-3.645582046309732,-71.02876312454754 L-3.713809524578467,-71.07545570486275 L-3.7737656219566205,-71.12430769543673 L-3.825101089404259,-71.1750345295356 L-3.867516893737026,-71.22734071931269 L-3.885300640099536,-71.25399116882913 L-3.900765959518242,-71.28092157704884 L-3.913890322108582,-71.30809271174054 L-3.924654608292995,-71.33546498998251 L-3.9330431366543332,-71.36299853582699 L-3.939043686780556,-71.39065323839151 L-3.9426475170674324,-71.41838881029246 L-3.9438493774533154,-71.44616484633569 " />
			<path d="M-3.9438493774533154,-71.44616484633569 L-3.94186188019185,-71.48187936525697 L-3.93590417646244,-71.51750784477395 L-3.925990618895204,-71.55296445275877 L-3.912145090118646,-71.58816377113719 L-3.894400945224313,-71.62302100166812 L-3.8728009314114606,-71.65745217023009 L-3.8473970850052996,-71.6913743291222 L-3.818250606096939,-71.72470575689248 L-3.7854317111069973,-71.75736615521191 L-3.749019463628102,-71.78927684232025 L-3.7091015839537644,-71.82036094257721 L-3.6657742377525153,-71.8505435716626 L-3.61914180439638,-71.8797520169793 L-3.5693166255018323,-71.90791591282417 L-3.516418734288999,-71.93496740990524 L-3.4605755664111193,-71.96084133879663 L-3.401921652950896,-71.98547536693734 L-3.340598296323331,-72.0088101487959 L-3.2767532298658315,-72.03078946883893 L-3.2105402619356602,-72.05136037695928 L-3.071653993216212,-72.08808224132922 L-2.9252770408557147,-72.11862209027763 L-2.77281909492318,-72.14268580836435 L-2.615748408779928,-72.16004164882965 L-2.45557765899709,-72.17052246544218 L-2.293849377453316,-72.17402732220856 L-2.1321210959095414,-72.17052246544218 L-1.9719503461267038,-72.16004164882965 L-1.8148796599834518,-72.14268580836435 L-1.6624217140509172,-72.11862209027763 L-1.5160447616904196,-72.08808224132922 L-1.3771584929709726,-72.05136037695928 L-1.3109455250408013,-72.03078946883893 L-1.2471004585833014,-72.0088101487959 L-1.1857771019557364,-71.98547536693734 L-1.1271231884955124,-71.96084133879663 L-1.0712800206176325,-71.93496740990524 L-1.0183821294047992,-71.90791591282417 L-0.9685569505102511,-71.8797520169793 L-0.9219245171541159,-71.85054357166261 L-0.8785971709528668,-71.82036094257721 L-0.8386792912785301,-71.78927684232025 L-0.8022670437996344,-71.75736615521191 L-0.7694481488096929,-71.72470575689248 L-0.7403016699013318,-71.6913743291222 L-0.7148978234951715,-71.65745217023009 L-0.6932978096823184,-71.62302100166812 L-0.6755536647879856,-71.58816377113719 L-0.661708136011427,-71.55296445275877 L-0.6517945784441908,-71.51750784477395 L-0.6458368747147811,-71.48187936525697 L-0.6438493774533156,-71.44616484633569 " />
			<path d="M-0.6438493774533156,-71.44616484633569 L-0.6451393365630533,-71.41738917733089 L-0.6490071969292308,-71.3886585015823 L-0.655446910816436,-71.36001774199525 L-0.6644484091730416,-71.3315116808834 L-0.6759976173750393,-71.30318488994757 L-0.6900764772329382,-71.27508166058418 L-0.7066629752273097,-71.24724593463168 L-0.7257311769288368,-71.21972123566373 L-0.7472512675490455,-71.19255060093629 L-0.7711895985583137,-71.16577651409517 L-0.8261675405063087,-71.11358475301249 L-0.890321286045882,-71.0634722502118 L-0.9632497522216434,-71.0157523041694 L-1.0444969973812417,-70.97072325533021 L-1.1335550716780722,-70.92866662091254 L-1.2298671927241402,-70.88984533488983 L-1.3328312265392057,-70.85450210415314 L-1.4418034520336565,-70.82285789113136 L-1.5561025854899295,-70.79511053235568 L-1.6750140398818183,-70.77143350160486 L-1.7977943924028108,-70.75197482536419 L-1.9236760322729165,-70.73685615737826 L-2.0518719597663386,-70.72617201808363 L-2.1815807064569457,-70.71998920367638 L-2.311991345920644,-70.71834636850869 L-2.4422885635682303,-70.7212537834257 L-2.5716577539126257,-70.72869327155311 L-2.6992901134028706,-70.74061832193728 L-2.8243876969849824,-70.75695438032714 L-2.946168406776549,-70.77759931528016 L-3.063870881666354,-70.802424056678 L-3.17675925726973,-70.83127340266053 L-3.2841277664808697,-70.86396698993244 L-3.3853051518598836,-70.9003004213772 L-3.479658862268795,-70.94004654392772 L-3.5665990075195175,-70.98295686870526 L-3.6455820463097277,-71.02876312454754 " />
			<path d="M-5.570777059529476,-75.81894478887824 L-5.4775290225478095,-75.76258691088589 L-5.379303026098654,-75.70789932016967 L-5.276252655053447,-75.65496752552457 L-5.168539037612055,-75.60387429040597 L-5.056330593364856,-75.55469950352185 L-4.939802769954088,-75.50752005391985 L-4.819137768746231,-75.46240971076459 L-4.694524259944357,-75.41943900799316 L-4.566157087585893,-75.37867513402918 L-4.434236964887049,-75.3401818267279 L-4.298970160410289,-75.30401927371648 L-4.160568175545531,-75.27024401828545 L-4.019247413809355,-75.23890887097836 L-3.875228842479337,-75.21006282701792 L-3.7287376470925153,-75.18375098969766 L-3.580002879348266,-75.16001449985912 L-3.4292570989660893,-75.13889047156445 L-3.276736010058298,-75.12041193406549 L-3.122678092586182,-75.1046077801595 L-2.967324229475886,-75.09150272101294 L-2.810917329977049,-75.08111724752331 L-2.6537019498531085,-75.07346759827985 L-2.495923908997132,-75.06856573417312 L-2.3378299070710806,-75.06641931969317 L-2.179667137769476,-75.06703171094532 L-2.0216829023106,-75.07040195040271 L-1.8641242227595731,-75.07652476840339 L-1.707237455787916,-75.08539059138998 L-1.551267907473512,-75.09698555687868 L-1.396459449743257,-75.11129153513451 L-1.2430541390581362,-75.12828615751872 L-1.09129183793694,-75.14794285146407 L-0.9414098399103898,-75.17023088202339 L-0.7936424984921093,-75.19511539992631 L-0.6482208607465658,-75.2225574960691 L-0.5053723060269255,-75.2525142623525 L-0.36532019044770236,-75.2849388587722 L-0.22828349764808165,-75.3197805866572 L-0.0944764963919984,-75.35698496794176 L0.03589159445967827,-75.39649383034637 L0.16261693308099323,-75.43824539833533 L0.28550137340529247,-75.48217438970805 L0.4043527749437992,-75.5282121176735 L0.5189853032139418,-75.57628659824795 L0.6292197203077055,-75.62632266280818 L0.7348836651456518,-75.67824207562411 L0.8358119229784293,-75.73196365618725 L0.9318466837143755,-75.78740340614334 L1.0228377886692925,-75.84447464063119 L1.1086429653525856,-75.90308812382192 L1.189128049922647,-75.9631522084469 L1.2641671969636716,-76.0245729790963 L1.3336430762558877,-76.0872543990639 L1.3974470562315378,-76.15109846050885 L1.4554793738297644,-76.21600533769944 L1.5076492904848156,-76.2818735430993 L1.5538752340036694,-76.34860008605192 L1.5940849261112362,-76.41608063381555 L1.628215495463718,-76.4842096746965 L1.65621357595341,-76.55288068302576 L1.6780353901512415,-76.62198628572119 L1.6936468177565875,-76.69141843017462 L1.7030234489473202,-76.76106855320151 L1.7061506225466845,-76.83082775078891 " />
			<path d="M1.7061506225466845,-76.83082775078891 L1.7044940243874374,-76.88160556433277 L1.6995256020684262,-76.9323413186604 L1.6912494709292853,-76.98299298939321 L1.6796724860818197,-77.03351862179892 L1.664804236731924,-77.08387636554274 L1.6466570382368495,-77.13402450935185 L1.6252459219044084,-77.18392151556489 L1.6005886225425519,-77.23352605453755 L1.572705563769647,-77.28279703887584 L1.5416198410976136,-77.3316936574688 L1.5073572028019293,-77.38017540929225 L1.4699460285943609,-77.42820213695575 L1.429417306116071,-77.475734059965 L1.3858046052705877,-77.52273180767193 L1.3391440504178806,-77.56915645188535 L1.2894742904525893,-77.6149695391152 L1.236836466791178,-77.66013312242346 L1.1812741792945385,-77.70460979285569 L1.1228334501542667,-77.74836271042668 L1.0615626857725218,-77.79135563463507 L0.9975126366670484,-77.83355295448133 L0.9307363554345716,-77.87491971796425 L0.8612891528073758,-77.91542166103171 L0.7892285518394804,-77.95502523596157 L0.6375080210355737,-78.03140683827844 L0.4760773388346258,-78.10381151007513 L0.3054712460243363,-78.17199941013493 L0.12625487703402571,-78.2357446653407 " />
			<path d="M-5.756414163772761,-77.71425848231374 L-5.820176068253684,-77.66373448938236 L-5.880150810753452,-77.61231598127675 L-5.936273980318529,-77.5600581798286 L-5.988485302461418,-77.50701720824377 L-6.036728703893527,-77.45325003082782 L-6.080952372746081,-77.39881439180809 L-6.121108814214425,-77.34376875331829 L-6.15715490156591,-77.28817223261203 L-6.189051922456628,-77.2320845385728 L-6.216765620507226,-77.17556590758853 L-6.240266232093171,-77.11867703885963 L-6.259528518309922,-77.06147902920995 L-6.2745317920787045,-77.00403330747086 L-6.285259940363778,-76.94640156850856 L-6.291701441477311,-76.88864570696576 L-6.2938493774533155,-76.83082775078893 " />
			<path d="M-6.2938493774533155,-76.83082775078891 L-6.290935776517841,-76.7634919058356 L-6.2821992182466255,-76.6962541557727 L-6.267652430061844,-76.62921245258599 L-6.247316603731327,-76.56246446265999 L-6.221221364496386,-76.49610742449765 L-6.189404727913744,-76.43023800706322 L-6.1519130444744565,-76.36495216895483 L-6.108800932080493,-76.30034501861196 L-6.060131196477355,-76.23651067576145 L-6.005974739758635,-76.17354213430382 L-5.946410457075809,-76.11153112683972 L-5.881525121703753,-76.05056799103383 L-5.811413258629383,-75.99074153801092 L-5.7361770068476226,-75.93213892297571 L-5.655925970565256,-75.87484551824522 L-5.57077705952948,-75.81894478887824 " />
			<path d="M-3.645582046309732,-76.41342602900076 L-3.713809524578467,-76.46011860931597 L-3.7737656219566205,-76.50897059988995 L-3.825101089404259,-76.55969743398882 L-3.867516893737026,-76.61200362376591 L-3.885300640099536,-76.63865407328235 L-3.900765959518242,-76.66558448150207 L-3.913890322108582,-76.69275561619376 L-3.924654608292995,-76.72012789443573 L-3.9330431366543332,-76.74766144028021 L-3.939043686780556,-76.77531614284473 L-3.9426475170674324,-76.80305171474568 L-3.9438493774533154,-76.83082775078891 " />
			<path d="M-3.9438493774533154,-76.83082775078891 L-3.94186188019185,-76.8665422697102 L-3.93590417646244,-76.90217074922717 L-3.925990618895204,-76.937627357212 L-3.912145090118646,-76.97282667559041 L-3.894400945224313,-77.00768390612134 L-3.8728009314114606,-77.04211507468331 L-3.8473970850052996,-77.07603723357542 L-3.818250606096939,-77.1093686613457 L-3.7854317111069973,-77.14202905966513 L-3.749019463628102,-77.17393974677347 L-3.7091015839537644,-77.20502384703043 L-3.6657742377525153,-77.23520647611582 L-3.61914180439638,-77.26441492143252 L-3.5693166255018323,-77.29257881727739 L-3.516418734288999,-77.31963031435846 L-3.4605755664111193,-77.34550424324985 L-3.401921652950896,-77.37013827139056 L-3.340598296323331,-77.39347305324912 L-3.2767532298658315,-77.41545237329215 L-3.2105402619356602,-77.4360232814125 L-3.071653993216212,-77.47274514578244 L-2.9252770408557147,-77.50328499473085 L-2.77281909492318,-77.52734871281757 L-2.615748408779928,-77.54470455328287 L-2.45557765899709,-77.5551853698954 L-2.293849377453316,-77.55869022666178 L-2.1321210959095414,-77.5551853698954 L-1.9719503461267038,-77.54470455328287 L-1.8148796599834518,-77.52734871281757 L-1.6624217140509172,-77.50328499473085 L-1.5160447616904196,-77.47274514578244 L-1.3771584929709726,-77.4360232814125 L-1.3109455250408013,-77.41545237329215 L-1.2471004585833014,-77.39347305324912 L-1.1857771019557364,-77.37013827139056 L-1.1271231884955124,-77.34550424324985 L-1.0712800206176325,-77.31963031435846 L-1.0183821294047992,-77.29257881727739 L-0.9685569505102511,-77.26441492143252 L-0.9219245171541159,-77.23520647611583 L-0.8785971709528668,-77.20502384703043 L-0.8386792912785301,-77.17393974677347 L-0.8022670437996344,-77.14202905966513 L-0.7694481488096929,-77.1093686613457 L-0.7403016699013318,-77.07603723357542 L-0.7148978234951715,-77.04211507468331 L-0.6932978096823184,-77.00768390612134 L-0.6755536647879856,-76.97282667559041 L-0.661708136011427,-76.937627357212 L-0.6517945784441908,-76.90217074922717 L-0.6458368747147811,-76.8665422697102 L-0.6438493774533156,-76.83082775078891 " />
			<path d="M-0.6438493774533156,-76.83082775078891 L-0.6451393365630533,-76.80205208178411 L-0.6490071969292308,-76.77332140603552 L-0.655446910816436,-76.74468064644847 L-0.6644484091730416,-76.71617458533662 L-0.6759976173750393,-76.6878477944008 L-0.6900764772329382,-76.6597445650374 L-0.7066629752273097,-76.6319088390849 L-0.7257311769288368,-76.60438414011695 L-0.7472512675490455,-76.57721350538951 L-0.7711895985583137,-76.5504394185484 L-0.8261675405063087,-76.49824765746571 L-0.890321286045882,-76.44813515466502 L-0.9632497522216434,-76.40041520862262 L-1.0444969973812417,-76.35538615978344 L-1.1335550716780722,-76.31332952536576 L-1.2298671927241402,-76.27450823934305 L-1.3328312265392057,-76.23916500860636 L-1.4418034520336565,-76.20752079558459 L-1.5561025854899295,-76.1797734368089 L-1.6750140398818183,-76.15609640605808 L-1.7977943924028108,-76.13663772981741 L-1.9236760322729165,-76.12151906183148 L-2.0518719597663386,-76.11083492253685 L-2.1815807064569457,-76.1046521081296 L-2.311991345920644,-76.10300927296191 L-2.4422885635682303,-76.10591668787892 L-2.5716577539126257,-76.11335617600633 L-2.6992901134028706,-76.1252812263905 L-2.8243876969849824,-76.14161728478037 L-2.946168406776549,-76.16226221973338 L-3.063870881666354,-76.18708696113123 L-3.17675925726973,-76.21593630711375 L-3.2841277664808697,-76.24862989438566 L-3.3853051518598836,-76.28496332583042 L-3.479658862268795,-76.32470944838094 L-3.5665990075195175,-76.36761977315848 L-3.6455820463097277,-76.41342602900076 " />
			<path d="M35.39081896642255,23.712995363347126 L28.836963602270227,25.73676128716847 " />
			<path d="M-5.570777059529474,4.053554960511206 L28.836963602270224,25.73676128716847 " />
			<path d="M-3.64558204630973,3.4590737203886857 L-3.7938493774533124,3.5048572105196323 " />
			<path d="M-0.9421167085968971,2.6242702768123807 L-0.8738892303281618,2.6709628571275887 L-0.8139331329500079,2.719814847701564 L-0.7625976655023694,2.770541681800431 L-0.7201818611696025,2.8228478715775394 L-0.7023981148070928,2.849498321093975 L-0.6869327953883864,2.876428729313689 L-0.6738084327980467,2.90359986400539 L-0.6630441466136336,2.9309721422473514 L-0.6546556182522953,2.9585056880918263 L-0.648655068126073,2.98616039065635 L-0.6450512378391964,3.0138959625572914 L-0.6438493774533134,3.0416719986005267 " />
			<path d="M-0.6438493774533134,3.0416719986005334 L-0.6451393365630511,3.0704476676053356 L-0.6490071969292286,3.09917834335393 L-0.6554469108164338,3.12781910294097 L-0.6644484091730394,3.1563251640528325 L-0.675997617375037,3.1846519549886523 L-0.690076477232936,3.212755184352044 L-0.7066629752273075,3.2405909103045474 L-0.7257311769288346,3.268115609272503 L-0.7472512675490433,3.2952862439999397 L-0.7711895985583115,3.322060330841058 L-0.8261675405063065,3.3742520919237355 L-0.8903212860458798,3.4243645947244197 L-0.9632497522216412,3.47208454076683 L-1.0444969973812395,3.5171135896060117 L-1.13355507167807,3.55917022402368 L-1.229867192724138,3.597991510046392 L-1.3328312265392035,3.6333347407830843 L-1.4418034520336542,3.6649789538048636 L-1.5561025854899273,3.6927263125805507 L-1.675014039881816,3.7164033433313595 L-1.7977943924028086,3.735862019572031 L-1.9236760322729143,3.750980687557972 L-2.0518719597663364,3.7616648268525914 L-2.1815807064569435,3.7678476412598436 L-2.311991345920642,3.769490476427528 L-2.442288563568228,3.7665830615105254 L-2.5716577539126235,3.7591435733831187 L-2.6992901134028684,3.747218522998949 L-2.82438769698498,3.730882464609075 L-2.946168406776547,3.7102375296560695 L-3.0638708816663516,3.6854127882582106 L-3.176759257269728,3.6565634422757007 L-3.2841277664808675,3.6238698550037833 L-3.385305151859882,3.5875364235590257 L-3.479658862268793,3.5477903010084986 L-3.5665990075195153,3.504879976230969 L-3.6455820463097255,3.4590737203886888 " />
			<path d="M28.836963602270224,29.32653655680395 L28.836963602270224,25.73676128716847 " />
			<path d="M-3.6455820463097295,5.253961355206426 L-3.5665990075195158,5.2997676110487095 L-3.4796588622687934,5.342677935826239 L-3.385305151859882,5.382424058376766 L-3.284127766480868,5.418757489821523 L-3.176759257269728,5.451451077093441 L-3.063870881666352,5.480300423075951 L-2.946168406776547,5.505125164473809 L-2.8243876969849806,5.525770099426815 L-2.6992901134028684,5.542106157816689 L-2.5716577539126235,5.5540312082008585 L-2.442288563568228,5.561470696328266 L-2.3119913459206414,5.564378111245269 L-2.181580706456943,5.562735276077584 L-2.051871959766336,5.556552461670331 L-1.923676032272914,5.545868322375712 L-1.7977943924028084,5.530749654389771 L-1.6750140398818156,5.511290978149099 L-1.5561025854899273,5.487613947398291 L-1.4418034520336542,5.459866588622604 L-1.3328312265392035,5.428222375600824 L-1.2298671927241376,5.392879144864133 L-1.1335550716780698,5.35405785884142 L-1.0444969973812392,5.312001224423752 L-0.9632497522216408,5.26697217558457 L-0.8903212860458791,5.2192522295421595 L-0.8261675405063063,5.169139726741475 L-0.7711895985583115,5.116947965658799 L-0.7472512675490428,5.09017387881768 L-0.7257311769288344,5.063003244090243 L-0.706662975227307,5.035478545122287 L-0.6900764772329357,5.007642819169784 L-0.675997617375037,4.979539589806392 L-0.6644484091730392,4.951212798870572 L-0.6554469108164336,4.92270673775871 L-0.6490071969292284,4.89406597817167 L-0.6451393365630511,4.865335302423076 L-0.6438493774533134,4.836559633418276 " />
			<path d="M-0.6438493774533134,4.836559633418274 L-0.6450512378391964,4.808783597375032 L-0.6486550681260728,4.781048025474091 L-0.6546556182522953,4.753393322909567 L-0.6630441466136336,4.725859777065092 L-0.6738084327980467,4.69848749882313 L-0.6869327953883864,4.671316364131429 L-0.7023981148070928,4.644385955911716 L-0.7201818611696025,4.61773550639528 L-0.7625976655023692,4.565429316618172 L-0.8139331329500079,4.514702482519304 L-0.8738892303281616,4.4658504919453295 L-0.9421167085968924,4.419157911630124 " />
			<path d="M-3.64558204630973,5.2539613552064255 L-3.64558204630973,6.918289126070202 " />
			<path d="M-3.64558204630973,5.2539613552064255 L-3.64558204630973,3.459073720388685 " />
			<path d="M10.900609370265819,-76.08006078157511 L12.534248383941316,-75.05056767579471 " />
			<path d="M1.8670203229947986,-78.18310844697402 L12.534248383941316,-71.46079240615923 " />
			<path d="M-0.9421167085968991,-78.14567328998594 L-0.9421167085968991,-78.4915366136187 " />
			<path d="M-0.2706982260380818,-78.35300069807288 L-0.942116708596899,-78.14567328998594 " />
			<path d="M35.39081896642255,-60.64672347308667 L28.836963602270227,-58.62295754926533 " />
			<path d="M-5.570777059529477,-80.30616387592259 L28.836963602270224,-58.62295754926533 " />
			<path d="M-3.645582046309732,-80.90064511604511 L-3.7938493774533146,-80.85486162591417 " />
			<path d="M-0.9421167085968998,-81.73544855962142 L-0.8738892303281645,-81.68875597930621 L-0.8139331329500106,-81.63990398873223 L-0.7625976655023721,-81.58917715463336 L-0.7201818611696051,-81.53687096485626 L-0.7023981148070955,-81.51022051533982 L-0.686932795388389,-81.48329010712011 L-0.6738084327980494,-81.45611897242841 L-0.6630441466136363,-81.42874669418644 L-0.654655618252298,-81.40121314834197 L-0.6486550681260757,-81.37355844577745 L-0.645051237839199,-81.3458228738765 L-0.643849377453316,-81.31804683783326 " />
			<path d="M-0.643849377453316,-81.31804683783326 L-0.6451393365630538,-81.28927116882846 L-0.6490071969292313,-81.26054049307987 L-0.6554469108164365,-81.23189973349282 L-0.664448409173042,-81.20339367238097 L-0.6759976173750397,-81.17506688144515 L-0.6900764772329386,-81.14696365208175 L-0.7066629752273101,-81.11912792612925 L-0.7257311769288373,-81.0916032271613 L-0.7472512675490459,-81.06443259243386 L-0.7711895985583141,-81.03765850559274 L-0.8261675405063091,-80.98546674451006 L-0.8903212860458825,-80.93535424170938 L-0.9632497522216439,-80.88763429566697 L-1.0444969973812421,-80.84260524682779 L-1.1335550716780727,-80.80054861241011 L-1.2298671927241407,-80.7617273263874 L-1.3328312265392062,-80.72638409565072 L-1.441803452033657,-80.69473988262894 L-1.55610258548993,-80.66699252385325 L-1.6750140398818187,-80.64331549310243 L-1.7977943924028112,-80.62385681686176 L-1.923676032272917,-80.60873814887583 L-2.051871959766339,-80.5980540095812 L-2.181580706456946,-80.59187119517395 L-2.3119913459206445,-80.59022836000626 L-2.4422885635682308,-80.59313577492327 L-2.571657753912626,-80.60057526305069 L-2.699290113402871,-80.61250031343485 L-2.824387696984983,-80.62883637182472 L-2.9461684067765495,-80.64948130677773 L-3.0638708816663542,-80.6743060481756 L-3.1767592572697305,-80.7031553941581 L-3.28412776648087,-80.73584898143001 L-3.3853051518598845,-80.77218241287477 L-3.4796588622687956,-80.8119285354253 L-3.566599007519518,-80.85483886020283 L-3.645582046309728,-80.90064511604511 " />
			<path d="M28.83696360227022,-55.03318227962985 L28.83696360227022,-58.62295754926533 " />
			<path d="M-5.570777059529477,-76.71638860628711 L12.534248383941314,-65.30689194392698 " />
			<path d="M-3.645582046309732,-77.31086984640963 L-5.570777059529477,-76.71638860628711 " />
			<path d="M-3.645582046309732,-77.31086984640963 L-3.5665990075195175,-77.26506359056735 L-3.4796588622687956,-77.22215326578981 L-3.385305151859884,-77.18240714323929 L-3.28412776648087,-77.14607371179453 L-3.1767592572697305,-77.11338012452262 L-3.0638708816663542,-77.08453077854011 L-2.9461684067765495,-77.05970603714225 L-2.8243876969849824,-77.03906110218924 L-2.6992901134028706,-77.02272504379937 L-2.5716577539126257,-77.0107999934152 L-2.4422885635682303,-77.00336050528779 L-2.3119913459206436,-77.00045309037078 L-2.1815807064569452,-77.00209592553847 L-2.051871959766338,-77.00827873994572 L-1.9236760322729163,-77.01896287924035 L-1.7977943924028106,-77.03408154722628 L-1.6750140398818179,-77.05354022346695 L-1.5561025854899295,-77.07721725421777 L-1.4418034520336565,-77.10496461299346 L-1.3328312265392057,-77.13660882601523 L-1.2298671927241398,-77.17195205675192 L-1.133555071678072,-77.21077334277463 L-1.0444969973812415,-77.2528299771923 L-0.963249752221643,-77.29785902603149 L-0.8903212860458813,-77.3455789720739 L-0.8261675405063085,-77.39569147487458 L-0.7711895985583137,-77.44788323595726 L-0.747251267549045,-77.47465732279838 L-0.7257311769288366,-77.50182795752582 L-0.7066629752273093,-77.52935265649377 L-0.690076477232938,-77.55718838244627 L-0.6759976173750393,-77.58529161180967 L-0.6644484091730414,-77.61361840274549 L-0.6554469108164358,-77.64212446385734 L-0.6490071969292306,-77.67076522344439 L-0.6451393365630533,-77.69949589919298 L-0.6438493774533156,-77.72827156819778 " />
			<path d="M-0.6438493774533156,-77.72827156819778 L-0.6450512378391986,-77.75604760424102 L-0.648655068126075,-77.78378317614197 L-0.6546556182522976,-77.81143787870649 L-0.6630441466136359,-77.83897142455096 L-0.6738084327980489,-77.86634370279293 L-0.6869327953883886,-77.89351483748463 L-0.702398114807095,-77.92044524570434 L-0.7201818611696047,-77.94709569522078 L-0.7625976655023714,-77.99940188499788 L-0.8139331329500101,-78.05012871909675 L-0.8738892303281638,-78.09898070967073 L-0.9421167085968947,-78.14567328998594 " />
			<path d="M-3.645582046309732,-79.10575748122737 L-3.5665990075195175,-79.05995122538509 L-3.4796588622687956,-79.01704090060755 L-3.385305151859884,-78.97729477805703 L-3.28412776648087,-78.94096134661227 L-3.1767592572697305,-78.90826775934036 L-3.0638708816663542,-78.87941841335785 L-2.9461684067765495,-78.85459367195999 L-2.8243876969849824,-78.83394873700698 L-2.6992901134028706,-78.81761267861711 L-2.5716577539126257,-78.80568762823295 L-2.4422885635682303,-78.79824814010553 L-2.3119913459206436,-78.79534072518852 L-2.1815807064569452,-78.79698356035621 L-2.051871959766338,-78.80316637476346 L-1.9236760322729163,-78.81385051405809 L-1.7977943924028106,-78.82896918204402 L-1.6750140398818179,-78.8484278582847 L-1.5561025854899295,-78.87210488903551 L-1.4418034520336565,-78.8998522478112 L-1.3328312265392057,-78.93149646083297 L-1.2298671927241398,-78.96683969156966 L-1.133555071678072,-79.00566097759237 L-1.0444969973812415,-79.04771761201005 L-0.963249752221643,-79.09274666084923 L-0.8903212860458813,-79.14046660689164 L-0.8261675405063085,-79.19057910969232 L-0.7711895985583137,-79.242770870775 L-0.747251267549045,-79.26954495761612 L-0.7257311769288366,-79.29671559234356 L-0.7066629752273093,-79.32424029131151 L-0.690076477232938,-79.35207601726401 L-0.6759976173750393,-79.3801792466274 L-0.6644484091730414,-79.40850603756323 L-0.6554469108164358,-79.43701209867508 L-0.6490071969292306,-79.46565285826213 L-0.6451393365630533,-79.49438353401072 L-0.6438493774533156,-79.52315920301552 " />
			<path d="M-0.6438493774533156,-79.52315920301552 L-0.6450512378391986,-79.55093523905876 L-0.648655068126075,-79.57867081095971 L-0.6546556182522976,-79.60632551352423 L-0.6630441466136359,-79.6338590593687 L-0.6738084327980489,-79.66123133761067 L-0.6869327953883886,-79.68840247230237 L-0.702398114807095,-79.71533288052208 L-0.7201818611696047,-79.74198333003852 L-0.7625976655023714,-79.79428951981562 L-0.8139331329500101,-79.84501635391449 L-0.8738892303281638,-79.89386834448847 L-0.9421167085968947,-79.94056092480368 " />
			<path d="M-3.645582046309732,-79.10575748122737 L-3.645582046309732,-77.31086984640963 " />
			<path d="M-3.645582046309732,-79.10575748122737 L-3.645582046309732,-80.90064511604511 " />
			<path d="M-5.570777059529477,-76.71638860628711 L-5.570777059529477,-77.84271071269958 " />
			<path d="M-3.5226972582318763,-80.93859072711676 L-3.450894495695318,-80.89694867635104 L-3.3718580000128435,-80.85793929018966 L-3.286081899641106,-80.82180645150736 L-3.194102458387457,-80.78877605928486 L-3.0964947227409656,-80.75905461631038 L-2.9938689267378966,-80.73282793814447 L-2.886866676838074,-80.71025999141914 L-2.776156940663922,-80.69149186873459 L-2.6624318646801846,-80.67664090656197 L-2.5464024469617796,-80.66579995166728 L-2.4287940921032383,-80.65903678064237 L-2.3103420760599778,-80.65639367617236 L-2.1917869492747974,-80.65788716268844 L-2.0738699068287914,-80.66350790305867 L-1.957328154562044,-80.67322075696286 L-1.842890300134675,-80.68696500058645 L-1.7312717978428638,-80.70465470625979 L-1.6231704756684198,-80.72617927966961 L-1.5192621725263533,-80.75140415128388 L-1.4201965129859433,-80.7801716176673 L-1.326592845881338,-80.81230182742794 L-1.2390363722030946,-80.8475939056304 L-1.1580744864787031,-80.88582720964646 L-1.0842133545154318,-80.92676270859118 L-1.0179147489011031,-80.97014447772064 L-0.9595931620469458,-81.01570129844853 L-0.9096132148214959,-81.06314835397825 L-0.8682873769765167,-81.11218900994966 L-0.8509526481569467,-81.1372114635569 L-0.8358740136166092,-81.16251666896825 L-0.8230750501094284,-81.18806505929861 L-0.8125757699257938,-81.21381668742208 L-0.8043925896016071,-81.23973128843286 L-0.7985383042496024,-81.26576834260291 L-0.7950220675530777,-81.29188713873799 L-0.793849377453316,-81.31804683783326 " />
			<path d="M-0.793849377453316,-81.31804683783326 L-0.7962046422745162,-81.35511280524157 L-0.8032630403749454,-81.3920623724244 L-0.8150024058922845,-81.42877950469412 L-0.831385873073698,-81.46514889729075 L-0.8523619920473176,-81.50105633747968 L-0.8778648903930037,-81.53638906322 L-0.9078144800050074,-81.57103611727706 L-0.942116708596896,-81.60488869566746 " />
			<path d="M-3.793849377453316,-81.31804683783326 L-3.7927567771025132,-81.29279589597577 L-3.7894805677508074,-81.2675817397022 L-3.784025522181514,-81.24244110100717 L-3.77639958730757,-81.21741060478492 L-3.7666138725944673,-81.19252671547405 L-3.7546826338759764,-81.16782568393613 L-3.7244562104385075,-81.1191158132669 L-3.6858963883178104,-81.07156473165135 L-3.63922778154723,-81.02544942792511 L-3.584722238476181,-80.98103852740331 L-3.5226972582318776,-80.93859072711676 " />
			<path d="M-13.000000000000002,-70.00061775789187 L-13.0,-1.794887634817739 " />
			<path d="M-0.6438493774533135,-3.2404347232615573 L-0.6438493774533133,2.1442281811916635 " />
			<path d="M-3.943849377453313,-3.2404347232615573 L-3.943849377453313,2.1442281811916635 " />
			<path d="M1.706150622546684,-76.83082775078891 L1.706150622546684,-73.24105248115343 " />
			<path d="M-6.293849377453315,-76.83082775078891 L-6.293849377453315,-73.24105248115343 " />
			<path d="M-0.6438493774533157,-76.83082775078891 L-0.6438493774533156,-71.44616484633569 " />
			<path d="M-3.943849377453316,-76.83082775078891 L-3.9438493774533154,-71.44616484633569 " />
			<path d="M-0.6438493774533132,6.631447268236014 L-0.6438493774533132,4.836559633418274 " />
			<path d="M-0.6438493774533132,3.0416719986005334 L-0.6438493774533132,4.836559633418274 " />
			<path d="M-0.6438493774533158,-77.72827156819778 L-0.6438493774533158,-79.52315920301552 " />
			<path d="M-0.6438493774533158,-81.31804683783326 L-0.6438493774533158,-79.52315920301552 " />
			<path d="M-0.793849377453316,-81.31804683783325 L-0.7938493774533134,1.8410022819911722 " />
			<path d="M-0.7938493774533134,2.5784867866814345 L-0.7938493774533133,6.328221369035524 " />
			<path d="M-3.793849377453315,-78.46657702120773 L-3.7938493774533124,1.841002281991173 " />

       </g>

       <!-- solid lines -->
       <g  stroke="rgb(40,40,40)" fill="none">
			<path d="M10.322322198539908,-3.187431330018618 L1.7061506225466871,-0.5268424917801267 " />
			<path d="M-6.293849377453313,1.9434786384550677 L-10.322322198539908,3.1874313300186174 " />
			<path d="M-10.322322198539908,3.187431330018618 L-9.175397509813251,3.9102048742405264 " />
			<path d="M-9.175397509813251,3.9102048742405264 L-9.994629430332292,4.163175614718194 " />
			<path d="M-11.387323695214661,4.054759583084909 L-9.994629430332292,4.163175614718195 " />
			<path d="M-11.96078603957799,3.6933728109739543 L-11.387323695214661,4.054759583084909 " />
			<path d="M-11.960786039577991,3.6933728109739556 L-12.118389762664707,3.592008144339438 L-12.271579564858586,3.4893351487844857 L-12.42029964933498,3.385391221231393 L-12.564495847289221,3.280214221518179 L-12.704115637666671,3.1738424586087857 L-12.83910816629265,3.0663146766396845 L-12.969424264395222,2.9576700408079564 L-13.095016466514098,2.8479481231060326 L-13.215839027789126,2.7371888879082644 L-13.331847940622104,2.6254326774145524 L-13.44300095070581,2.512720196956383 L-13.549257572414417,2.3990925001706 L-13.650579103549717,2.284590974046287 L-13.746928639437748,2.169257323850255 L-13.838271086370696,2.0531335579366092 L-13.924573174389199,1.9362619724458865 L-14.005803469400378,1.8186851358994036 L-14.081932384627164,1.7004458736943941 L-14.152932191384807,1.581587252505556 L-14.218777029180565,1.4621525645987428 L-14.279442915132977,1.342185312062489 L-14.334907752707208,1.221729190963084 L-14.38515133976336,1.1008280754290196 L-14.430155375914742,0.9795260016705797 L-14.469903469193506,0.8578671519403701 L-14.504381142021128,0.735895838440681 L-14.533575836481626,0.613656487183515 L-14.557476918895581,0.4911936218091391 L-14.57607568369327,0.3685518473691011 L-14.589365356585521,0.2457758340795935 L-14.597341097031139,0.12291030105105742 L-14.6,3.0935239496280174e-14 " />
			<path d="M-14.6,2.3337623560835863e-15 L-14.597146175175643,-0.12733542552839924 L-14.58858581636232,-0.2546210711940073 L-14.574322270103108,-0.38180717659471436 L-14.554361112516144,-0.5088440202421771 L-14.528710147114724,-0.635681938999682 L-14.49737940175663,-0.7622713474971989 L-14.460381124723902,-0.8885627575160333 L-14.417729779934547,-1.0145067973354953 L-14.36944204128809,-1.1400542310340378 L-14.315536786147172,-1.2651559777372903 L-14.256035087957722,-1.3897631308054812 L-14.190960208010614,-1.5138269769527588 L-14.120337586348017,-1.637299015290912 L-14.044194831817991,-1.7601309762900612 L-13.96256171128124,-1.8822748406489014 L-13.875470137974174,-2.003682858067125 L-13.782954159032954,-2.124307565912679 L-13.685049942183237,-2.2441018077765653 L-13.58179576160098,-2.3630187519079295 L-13.473231982949713,-2.4810119095222207 L-13.359401047600194,-2.59803515297529 L-13.240347456038593,-2.7140427337962922 L-13.116117750469712,-2.8289893005723536 L-12.986760496622,-2.9428299166780296 L-12.852326264761519,-3.0555200778426 L-12.712867609922258,-3.1670157295483397 L-12.568439051360539,-3.277273284252968 L-12.419097051241533,-3.3862496384295415 L-12.264899992566239,-3.4939021894171267 L-12.105908156347514,-3.600188852075666 L-11.94218369804414,-3.7050680752385317 L-11.77379062326207,-3.80849885795632 L-11.600794762732406,-3.9104407655255655 L-11.42326374657587,-4.010853945296069 L-11.241266977863834,-4.1096991422506886 L-11.054875605486231,-4.206937714351501 L-10.864162496336972,-4.302531647646323 L-10.669202206827727,-4.396443571129689 L-10.470070953741235,-4.488636771352484 L-10.266846584435486,-4.579075206774511 L-10.059608546410491,-4.6677235218543895 L-9.848437856249465,-4.754547060871266 L-9.63341706794662,-4.839511881472953 L-9.414630240633922,-4.922584767945175 L-9.192162905719464,-5.003733244196744 L-8.966102033450229,-5.08292558645561 L-8.736535998912395,-5.160130835670779 L-8.50355454748243,-5.235318809615296 L-8.26724875974248,-5.308460114685526 L-8.027711015873809,-5.37952615739214 L-7.785034959542145,-5.448489155538311 L-7.539315461289107,-5.51532214908074 L-7.290648581444002,-5.579999010669284 L-7.039131532570491,-5.642494455861043 L-6.7848626414627935,-5.702784053004936 L-6.52794131070632,-5.7608442327928815 L-6.268467979817736,-5.81665229747387 L-6.006544085979631,-5.870186429727299 L-5.742272024385204,-5.921425701192134 L-5.475755108208394,-5.970350080648523 L-5.207097528215159,-6.016940441848713 L-4.936404312031669,-6.061178570994161 L-4.66378128308534,-6.103047173855945 L-4.389335019234771,-6.142529882535676 L-4.1131728111047074,-6.179611261864294 L-3.835402620142414,-6.214276815436205 L-3.5561330364117962,-6.246512991276428 L-3.2754732361417234,-6.276307187138547 L-2.9935329390452377,-6.30364775543136 L-2.710422365426289,-6.32852400777233 L-2.4262521930907734,-6.350926219166052 L-2.141133514078711,-6.3708456318060875 L-1.8551777912344924,-6.3882744584987 L-1.568496814632162,-6.40320588570714 L-1.281202657872774,-6.4156340762152935 L-0.993407634270911,-6.425554171409654 L-0.705224252947488,-6.432962293178725 L-0.4167651748460102,-6.437855545429108 L-0.12814316868947737,-6.440232015217688 L0.16052893310484698,-6.440090773499469 L0.44913827853556554,-6.437431875490767 L0.7375720401349343,-6.432256360647631 L1.0257174590770584,-6.424566252259475 L1.3134618892592522,-6.414364556658112 L1.6006928413393344,-6.401655262042466 L1.8872980267116382,-6.386443336919452 L2.1731654014045465,-6.368734728161612 L2.458183209882379,-6.348536358682269 L2.7422400287345714,-6.325856124729127 L3.0252248102349477,-6.300702892797347 L3.3070269257541316,-6.273086496163327 L3.5875362090081744,-6.243017731040528 L3.8666429991263893,-6.210508352358861 L4.144238183521615,-6.175571069169271 L4.42021324054613,-6.13821953967533 L4.6944602819165615,-6.098468365893763 L4.966872094891172,-6.056333087946011 L5.2373421841830705,-6.011830177983062 L5.505764813592933,-5.964977033745902 L5.772035047344972,-5.915791971764136 L6.036048791110003,-5.864294220195419 L6.297702832699542,-5.810503911308494 L6.556894882415057,-5.754442073612787 L6.813523613036582,-5.696130623637629 L7.067488699435064,-5.635592357364318 L7.318690857792956,-5.572850941314379 L7.56703188441773,-5.507930903297485 L7.812414694133128,-5.4408576228226915 L8.054743358233148,-5.371657321176693 L8.293923141983912,-5.300357051173009 L8.5298605416588,-5.226984686576094 L8.7624633210923,-5.151568911204513 L8.991640547738369,-5.07413920771743 L9.217302628219128,-4.994725846088805 L9.439361343350024,-4.913359871773821 L9.657729882627809,-4.830073093572117 L9.872322878167788,-4.74489807119262 L10.083056438077115,-4.657868102524819 L10.28984817925105,-4.569017210621464 L10.492617259579395,-4.478380130397754 L10.691284409550498,-4.385992295052259 L10.885771963240476,-4.29188982221484 L11.076003888675526,-4.196109499827004 L11.261905817555485,-4.098688771760219 L11.443405074326993,-3.999665723177797 L11.6204307045949,-3.8990790656460694 L11.792913502860825,-3.7969681220006883 L11.960786039577915,-3.693372810974004 " />
			<path d="M11.96078603957799,-3.6933728109739543 L12.534248383941318,-3.331986038863 " />
			<path d="M12.534248383941318,-3.331986038863 L12.288478807785605,-2.7176285262743773 " />
			<path d="M12.288478807785605,-2.7176285262743773 L11.469246887266564,-2.4646577857967094 " />
			<path d="M10.322322198539908,-3.187431330018618 L11.469246887266564,-2.4646577857967094 " />
			<path d="M1.7061506225466867,-1.4455470884438184 L1.7049458973315037,-1.4888504565738767 L1.7013324473673763,-1.53212774037419 L1.6953124492614475,-1.5753528712272395 L1.686889529235474,-1.6184998119304912 L1.6760687609415266,-1.6615425723802333 L1.6628566624058103,-1.7044552252270435 L1.6472611921024516,-1.7472119214934545 L1.6292917441596084,-1.7897869061444107 L1.608959142700801,-1.83215453360114 L1.5862756353248626,-1.8742892831890903 L1.5612548857284465,-1.916165774510629 L1.533911965475522,-1.957758782733248 L1.5042633449188325,-1.999043253784056 L1.472326883278769,-2.039994319441417 L1.4016687525918332,-2.120797780702684 L1.3221077950404596,-2.199974503901324 L1.233835679940106,-2.2773337453760902 L1.1370650625477734,-2.3526891399384002 L1.0320290717568663,-2.4258591498424 L0.9189807484692656,-2.4966675021252946 L0.7981924359976329,-2.5649436132643566 L0.6699551239665205,-2.6305230001275706 L0.5345777472928748,-2.693247676227906 L0.3923864419347587,-2.752966532326605 L0.24372375920126732,-2.8095357004685724 L0.08894784051641924,-2.86281890057288 L-0.0715684453749077,-2.91268776874342 L-0.23743840068043198,-2.959022166508772 L-0.40826243014932806,-3.001710470246304 L-0.5836290037321898,-3.0406498400932604 L-0.7631156479929586,-3.075746467696993 L-0.9462899638844369,-3.106915802207503 L-1.132710668435467,-3.134082753967844 L-1.3219286578402603,-3.1571818754116805 L-1.5134880893888023,-3.1761575187322104 L-1.7069274796318676,-3.190963969942605 L-1.9017808161350716,-3.2015655590050063 L-2.0975786801436413,-3.207936745762773 L-2.2938493774533164,-3.210062181468956 L-2.490120074762991,-3.2079367457627725 L-2.685917938771561,-3.2015655590050063 L-2.880771275274765,-3.1909639699426045 L-3.07421066551783,-3.17615751873221 L-3.2657700970663717,-3.1571818754116796 L-3.454988086471165,-3.134082753967843 L-3.641408791022195,-3.106915802207502 L-3.824583106913673,-3.075746467696992 L-4.004069751174442,-3.040649840093259 L-4.179436324757304,-3.001710470246303 L-4.350260354226199,-2.9590221665087704 L-4.516130309531723,-2.9126877687434183 L-4.67664659542305,-2.8628189005728784 L-4.831422514107898,-2.8095357004685706 L-4.980085196841389,-2.752966532326603 L-5.122276502199505,-2.6932476762279034 L-5.2576538788731515,-2.6305230001275683 L-5.385891190904262,-2.5649436132643553 L-5.506679503375894,-2.4966675021252938 L-5.619727826663496,-2.425859149842397 L-5.724763817454405,-2.3526891399383967 L-5.821534434846736,-2.277333745376087 L-5.909806549947088,-2.199974503901321 L-5.9893675074984625,-2.120797780702681 L-6.060025638185397,-2.0399943194414143 L-6.09196209982546,-1.9990432537840532 L-6.121610720382149,-1.9577587827332459 L-6.1489536406350735,-1.9161657745106278 L-6.173974390231489,-1.874289283189089 L-6.1966578976074285,-1.8321545336011387 L-6.2169904990662355,-1.7897869061444094 L-6.234959947009079,-1.747211921493453 L-6.250555417312437,-1.7044552252270422 L-6.263767515848153,-1.661542572380232 L-6.2745882841421015,-1.6184998119304899 L-6.283011204168075,-1.5753528712272382 L-6.289031202274003,-1.5321277403741886 L-6.29264465223813,-1.4888504565738738 L-6.293849377453313,-1.4455470884438317 " />
			<path d="M-9.175397509813251,3.9102048742405264 L-9.175397509813251,2.833272293349882 " />
			<path d="M11.96078603957799,-3.6933728109739556 L11.960786039577988,-75.48887820368357 " />
			<path d="M-14.600000000000003,-71.79550539270961 L-14.597146175175647,-71.92284081823802 L-14.588585816362324,-72.05012646390362 L-14.574322270103112,-72.17731256930433 L-14.554361112516148,-72.3043494129518 L-14.528710147114728,-72.4311873317093 L-14.497379401756634,-72.55777674020682 L-14.460381124723906,-72.68406815022564 L-14.41772977993455,-72.81001219004511 L-14.369442041288094,-72.93555962374366 L-14.315536786147176,-73.06066137044691 L-14.256035087957725,-73.18526852351509 L-14.190960208010617,-73.30933236966237 L-14.12033758634802,-73.43280440800052 L-14.044194831817995,-73.55563636899967 L-13.962561711281243,-73.67778023335852 L-13.875470137974178,-73.79918825077674 L-13.782954159032958,-73.91981295862229 L-13.685049942183241,-74.03960720048617 L-13.581795761600983,-74.15852414461754 L-13.473231982949716,-74.27651730223184 L-13.359401047600198,-74.3935405456849 L-13.240347456038597,-74.5095481265059 L-13.116117750469716,-74.62449469328197 L-12.986760496622004,-74.73833530938765 L-12.852326264761523,-74.85102547055222 L-12.712867609922261,-74.96252112225795 L-12.568439051360542,-75.07277867696259 L-12.419097051241536,-75.18175503113916 L-12.264899992566242,-75.28940758212674 L-12.105908156347517,-75.39569424478528 L-11.942183698044143,-75.50057346794814 L-11.773790623262073,-75.60400425066594 L-11.60079476273241,-75.70594615823518 L-11.423263746575874,-75.80635933800568 L-11.241266977863837,-75.9052045349603 L-11.054875605486234,-76.00244310706111 L-10.864162496336975,-76.09803704035593 L-10.66920220682773,-76.19194896383931 L-10.470070953741239,-76.2841421640621 L-10.26684658443549,-76.37458059948412 L-10.059608546410495,-76.463228914564 L-9.848437856249468,-76.55005245358088 L-9.633417067946624,-76.63501727418257 L-9.414630240633926,-76.7180901606548 L-9.192162905719467,-76.79923863690635 L-8.966102033450232,-76.87843097916523 L-8.736535998912398,-76.9556362283804 L-8.503554547482434,-77.03082420232491 L-8.267248759742484,-77.10396550739515 L-8.027711015873813,-77.17503155010175 L-7.785034959542147,-77.24399454824793 L-7.5393154612891085,-77.31082754179036 L-7.290648581444004,-77.3755044033789 L-7.039131532570493,-77.43799984857066 L-6.784862641462795,-77.49828944571455 L-6.527941310706322,-77.55634962550249 L-6.268467979817737,-77.61215769018348 L-6.006544085979633,-77.66569182243691 L-5.742272024385206,-77.71693109390175 L-5.4757551082083955,-77.76585547335814 L-5.207097528215161,-77.81244583455833 L-4.936404312031671,-77.85668396370377 L-4.663781283085342,-77.89855256656556 L-4.389335019234773,-77.9380352752453 L-4.113172811104709,-77.97511665457391 L-3.8354026201424163,-78.00978220814582 L-3.5561330364117985,-78.04201838398605 L-3.2754732361417256,-78.07181257984816 L-2.99353293904524,-78.09915314814097 L-2.7104223654262913,-78.12402940048194 L-2.4262521930907757,-78.14643161187567 L-2.1411335140787133,-78.1663510245157 L-1.8551777912344947,-78.18377985120831 L-1.5684968146321643,-78.19871127841675 L-1.2812026578727762,-78.21113946892491 L-0.9934076342709133,-78.22105956411927 L-0.7052242529474902,-78.22846768588835 L-0.41676517484601244,-78.23336093813873 L-0.1281431686894796,-78.2357374079273 L0.16052893310484476,-78.23559616620908 L0.4491382785355633,-78.23293726820039 L0.737572040134932,-78.22776175335724 L1.0257174590770561,-78.2200716449691 L1.31346188925925,-78.20986994936773 L1.6006928413393322,-78.19716065475208 L1.887298026711636,-78.18194872962907 L2.1731654014045443,-78.16424012087123 L2.458183209882377,-78.14404175139188 L2.742240028734569,-78.12136151743874 L3.0252248102349455,-78.09620828550696 L3.3070269257541294,-78.06859188887294 L3.587536209008172,-78.03852312375014 L3.866642999126387,-78.00601374506847 L4.1442381835216135,-77.97107646187888 L4.420213240546128,-77.93372493238495 L4.69446028191656,-77.89397375860338 L4.96687209489117,-77.85183848065563 L5.237342184183069,-77.80733557069267 L5.505764813592931,-77.76048242645552 L5.77203504734497,-77.71129736447375 L6.036048791110002,-77.65979961290503 L6.297702832699541,-77.60600930401812 L6.5568948824150555,-77.54994746632241 L6.813523613036581,-77.49163601634724 L7.067488699435062,-77.43109775007393 L7.318690857792954,-77.368356334024 L7.5670318844177284,-77.3034362960071 L7.8124146941331265,-77.2363630155323 L8.054743358233145,-77.16716271388631 L8.293923141983909,-77.09586244388262 L8.529860541658797,-77.0224900792857 L8.762463321092296,-76.94707430391412 L8.991640547738365,-76.86964460042705 L9.217302628219125,-76.79023123879843 L9.43936134335002,-76.70886526448344 L9.657729882627805,-76.62557848628174 L9.872322878167784,-76.54040346390224 L10.083056438077111,-76.45337349523443 L10.289848179251047,-76.36452260333108 L10.492617259579392,-76.27388552310737 L10.691284409550494,-76.18149768776188 L10.885771963240472,-76.08739521492446 L11.076003888675523,-75.99161489253662 L11.261905817555482,-75.89419416446984 L11.44340507432699,-75.79517111588741 L11.620430704594897,-75.69458445835568 L11.792913502860822,-75.5924735147103 L11.960786039577911,-75.48887820368361 " />
			<path d="M11.960786039577988,-75.48887820368357 L12.534248383941316,-75.12749143157261 " />
			<path d="M12.534248383941318,-3.331986038863 L12.534248383941316,-75.12749143157261 " />
			<path d="M-5.570777059529474,3.156111143102336 L-5.4428787680793045,3.2322715534667017 L-5.305894419613394,3.305292576137349 L-5.160219262141855,3.374963519789101 L-5.006273619714534,3.441083359252663 L-4.844501679638349,3.503461315542922 L-4.67537021084072,3.561917406323395 L-4.499367217077099,3.616282965218554 L-4.317000528868554,3.6664011284756204 " />
			<path d="M1.6464857657750454,2.4478577788429106 L1.6725525124403435,2.372448294507247 L1.6912064924758297,2.2966122920104883 L1.7024128436550923,2.2204915004573134 L1.7061506225466867,2.14422818119167 " />
			<path d="M1.7061506225466867,2.144228181191662 L1.7049458973315037,2.100924813061604 L1.7013324473673763,2.0576475292612906 L1.6953124492614475,2.0144223984082408 L1.686889529235474,1.9712754577049894 L1.6760687609415266,1.9282326972552473 L1.6628566624058103,1.885320044408437 L1.6472611921024516,1.842563348142026 L1.6292917441596084,1.7999883634910698 L1.608959142700801,1.7576207360343405 L1.5862756353248626,1.7154859864463903 L1.5612548857284465,1.6736094951248515 L1.533911965475522,1.6320164869022324 L1.5042633449188325,1.5907320158514247 L1.472326883278769,1.5497809501940636 L1.4016687525918332,1.4689774889327967 L1.3221077950404596,1.3898007657341567 L1.233835679940106,1.31244152425939 L1.1370650625477734,1.23708612969708 L1.0320290717568663,1.1639161197930807 L0.9189807484692656,1.0931077675101861 L0.7981924359976329,1.024831656371124 L0.6699551239665205,0.95925226950791 L0.5345777472928748,0.8965275934075747 L0.3923864419347587,0.8368087373088755 L0.24372375920126732,0.780239569166908 L0.08894784051641924,0.7269563690626004 L-0.0715684453749077,0.6770875008920603 L-0.23743840068043198,0.6307531031267084 L-0.40826243014932806,0.5880647993891761 L-0.5836290037321898,0.5491254295422201 L-0.7631156479929586,0.5140288019384875 L-0.9462899638844369,0.48285946742797736 L-1.132710668435467,0.4556925156676366 L-1.3219286578402603,0.43259339422380005 L-1.5134880893888023,0.41361775090327013 L-1.7069274796318676,0.39881129969287565 L-1.9017808161350716,0.3882097106304745 L-2.0975786801436413,0.38183852387270756 L-2.2938493774533164,0.3797130881665245 L-2.490120074762991,0.3818385238727078 L-2.685917938771561,0.3882097106304745 L-2.880771275274765,0.3988112996928759 L-3.07421066551783,0.4136177509032706 L-3.2657700970663717,0.4325933942238007 L-3.454988086471165,0.45569251566763747 L-3.641408791022195,0.48285946742797825 L-3.824583106913673,0.5140288019384887 L-4.004069751174442,0.5491254295422212 L-4.179436324757304,0.5880647993891777 L-4.350260354226199,0.6307531031267102 L-4.516130309531723,0.6770875008920623 L-4.67664659542305,0.7269563690626024 L-4.831422514107898,0.78023956916691 L-4.980085196841389,0.8368087373088775 L-5.122276502199505,0.8965275934075769 L-5.2576538788731515,0.9592522695079124 L-5.385891190904262,1.0248316563711255 L-5.506679503375894,1.093107767510187 L-5.619727826663496,1.1639161197930832 L-5.724763817454405,1.237086129697084 L-5.821534434846736,1.3124415242593934 L-5.909806549947088,1.3898007657341593 L-5.9893675074984625,1.4689774889327993 L-6.060025638185397,1.5497809501940663 L-6.09196209982546,1.5907320158514273 L-6.121610720382149,1.6320164869022347 L-6.1489536406350735,1.6736094951248528 L-6.173974390231489,1.7154859864463916 L-6.1966578976074285,1.7576207360343419 L-6.2169904990662355,1.7999883634910712 L-6.234959947009079,1.8425633481420276 L-6.250555417312437,1.8853200444084384 L-6.263767515848153,1.9282326972552486 L-6.2745882841421015,1.9712754577049907 L-6.283011204168075,2.0144223984082426 L-6.289031202274003,2.057647529261292 L-6.29264465223813,2.100924813061607 L-6.293849377453313,2.144228181191649 " />
			<path d="M-6.293849377453313,2.144228181191665 L-6.2909357765178395,2.2115640261449774 L-6.282199218246623,2.278801776207866 L-6.267652430061841,2.34584347939459 L-6.247316603731324,2.4125914693205894 L-6.221221364496383,2.478948507482919 L-6.189404727913741,2.544817924917347 L-6.151913044474454,2.6101037630257444 L-6.108800932080491,2.674710913368618 L-6.060131196477354,2.738545256219131 L-6.005974739758632,2.8015137976767597 L-5.946410457075807,2.8635248051408557 L-5.881525121703751,2.924487940946741 L-5.811413258629381,2.984314393969659 L-5.73617700684762,3.0429170090048627 L-5.655925970565253,3.1002104137353586 L-5.570777059529477,3.1561111431023345 " />
			<path d="M-3.793849377453313,2.447454080392154 L-3.82858958679045,2.411492698754289 L-3.858903091802396,2.374760436814555 L-3.8847024581970606,2.3373632427078963 L-3.9059132719686636,2.2994089824561277 L-3.922474354032634,2.261007128846236 L-3.934337936686557,2.222268445674228 L-3.941469801388215,2.1833046682652784 L-3.943849377453313,2.144228181191667 " />
			<path d="M-3.943849377453313,2.144228181191664 L-3.9418618801918477,2.108513662270386 L-3.9359041764624383,2.0728851827534114 L-3.925990618895202,2.037428574768583 L-3.912145090118644,2.0022292563901694 L-3.8944009452243114,1.9673720258592389 L-3.872800931411458,1.9329408572972737 L-3.847397085005298,1.899018698405154 L-3.818250606096937,1.8656872706348815 L-3.7854317111069955,1.8330268723154424 L-3.749019463628099,1.8011161852071012 L-3.709101583953762,1.7700320849501483 L-3.6657742377525135,1.7398494558647486 L-3.619141804396378,1.7106410105480545 L-3.56931662550183,1.6824771147031916 L-3.5164187342889965,1.655425617622116 L-3.4605755664111175,1.6295516887307275 L-3.401921652950894,1.6049176605900137 L-3.340598296323329,1.5815828787314523 L-3.2767532298658293,1.5596035586884254 L-3.210540261935658,1.5390326505680778 L-3.0716539932162097,1.502310786198138 L-2.925277040855712,1.4717709372497287 L-2.772819094923178,1.4477072191630027 L-2.6157484087799254,1.4303513786977011 L-2.455577658997088,1.4198705620851728 L-2.2938493774533137,1.4163657053187935 L-2.132121095909539,1.4198705620851728 L-1.9719503461267016,1.4303513786977011 L-1.8148796599834496,1.4477072191630027 L-1.662421714050915,1.4717709372497287 L-1.5160447616904174,1.5023107861981377 L-1.3771584929709704,1.5390326505680774 L-1.310945525040799,1.5596035586884245 L-1.2471004585832992,1.5815828787314514 L-1.1857771019557342,1.6049176605900128 L-1.1271231884955102,1.6295516887307269 L-1.0712800206176303,1.6554256176221158 L-1.018382129404797,1.6824771147031912 L-0.9685569505102489,1.710641010548054 L-0.9219245171541137,1.7398494558647482 L-0.8785971709528646,1.7700320849501479 L-0.8386792912785279,1.8011161852071005 L-0.8022670437996322,1.8330268723154415 L-0.7694481488096907,1.8656872706348804 L-0.7403016699013296,1.8990186984051531 L-0.7148978234951693,1.9329408572972724 L-0.6932978096823161,1.967372025859237 L-0.6755536647879834,2.002229256390168 L-0.6617081360114248,2.0374285747685827 L-0.6517945784441885,2.0728851827534105 L-0.6458368747147789,2.1085136622703846 L-0.6438493774533134,2.1442281811916564 " />
			<path d="M-0.6438493774533134,2.144228181191663 L-0.6462289535184114,2.1833046682652775 L-0.6533608182200696,2.222268445674227 L-0.6652244008739925,2.2610071288462352 L-0.6817854829379628,2.2994089824561272 L-0.702996296709566,2.3373632427078954 L-0.7287956631042305,2.374760436814555 L-0.7591091681161768,2.4114926987542886 L-0.7938493774533133,2.447454080392153 " />
			<path d="M0.1262548770339973,-78.23574466534072 L-0.045883550877308554,-78.29033412260111 L-0.2243367357565833,-78.34082368300264 L-0.40860338506665994,-78.38707151640733 L-0.59816587567736,-78.42894770810527 L-0.7924917079197356,-78.46633462375782 L-0.9910350014299922,-78.499127239844 L-1.1932380285810835,-78.52723343868192 L-1.398532781194433,-78.55057426719637 L-1.6063425661307504,-78.5690841587058 L-1.8160836252777384,-78.58271111710556 L-2.027166775384002,-78.59141686293003 L-2.238999063132727,-78.59517694088352 L-2.4509854308058245,-78.59398078853741 L-2.66253038785955,-78.58783176600124 L-2.8730396837159846,-78.57674714648374 L-3.081921977071311,-78.56075806777066 L-3.2885904970316537,-78.53990944475575 L-3.492464691410206,-78.51425984327034 L-3.692971857555391,-78.4838813155662 L-3.8895487511288973,-78.44885919791365 L-4.081643168314383,-78.40929187088368 L-4.268715497012279,-78.3652904829871 L-4.450240232663223,-78.31697863844761 L-4.62570745444202,-78.26449204998525 L-4.7946242576753475,-78.20797815758613 L-4.956516138459445,-78.14759571432894 L-5.110928326588223,-78.08351434043205 L-5.257427063047469,-78.01591404677352 L-5.395600818486548,-77.94498472922291 L-5.525061449244806,-77.87092563520515 L-5.645445287685266,-77.79394480399489 L-5.756414163772743,-77.71425848231375 " />
			<path d="M0.9830783046228484,5.6195643063253415 L0.9830783046228483,2.029789036689861 " />
			<path d="M0.9830783046228483,2.029789036689861 L35.39081896642255,23.712995363347126 " />
			<path d="M35.39081896642255,27.302770632982607 L35.39081896642255,23.712995363347126 " />
			<path d="M0.9830783046228484,5.6195643063253415 L35.39081896642255,27.302770632982604 " />
			<path d="M-0.9421167085968964,6.214045546447862 L-0.9421167085968964,4.419157911630121 " />
			<path d="M-0.9421167085968964,2.6242702768123807 L-0.9421167085968964,4.419157911630121 " />
			<path d="M0.9830783046228483,2.029789036689861 L-0.9421167085968966,2.624270276812381 " />
			<path d="M0.9830783046228484,5.6195643063253415 L-0.9421167085968964,6.214045546447862 " />
			<path d="M-3.7938493774533124,3.5048572105196323 L-5.570777059529474,4.053554960511206 " />
			<path d="M35.39081896642255,27.302770632982607 L28.836963602270227,29.32653655680395 " />
			<path d="M-5.570777059529474,7.643330230146686 L28.836963602270224,29.32653655680395 " />
			<path d="M-3.6455820463097295,7.048848990024166 L-5.570777059529474,7.643330230146686 " />
			<path d="M-3.6455820463097295,7.048848990024167 L-3.566599007519515,7.09465524586645 L-3.479658862268793,7.13756557064398 L-3.3853051518598813,7.177311693194507 L-3.2841277664808675,7.213645124639264 L-3.176759257269728,7.246338711911181 L-3.0638708816663516,7.275188057893692 L-2.946168406776547,7.30001279929155 L-2.8243876969849797,7.320657734244556 L-2.699290113402868,7.33699379263443 L-2.571657753912623,7.348918843018599 L-2.4422885635682277,7.356358331146007 L-2.311991345920641,7.359265746063009 L-2.1815807064569426,7.357622910895325 L-2.0518719597663355,7.351440096488072 L-1.9236760322729136,7.340755957193453 L-1.797794392402808,7.325637289207512 L-1.6750140398818152,7.30617861296684 L-1.5561025854899269,7.282501582216032 L-1.4418034520336538,7.254754223440345 L-1.332831226539203,7.223110010418565 L-1.2298671927241371,7.187766779681874 L-1.1335550716780693,7.148945493659161 L-1.0444969973812388,7.106888859241493 L-0.9632497522216403,7.061859810402311 L-0.8903212860458787,7.0141398643599 L-0.8261675405063058,6.964027361559216 L-0.771189598558311,6.9118356004765396 L-0.7472512675490424,6.885061513635421 L-0.7257311769288339,6.857890878907984 L-0.7066629752273066,6.830366179940028 L-0.6900764772329353,6.802530453987525 L-0.6759976173750366,6.774427224624133 L-0.6644484091730387,6.746100433688313 L-0.6554469108164331,6.717594372576451 L-0.6490071969292279,6.688953612989411 L-0.6451393365630507,6.660222937240817 L-0.6438493774533129,6.631447268236017 " />
			<path d="M-0.6438493774533129,6.631447268236014 L-0.6450512378391959,6.603671232192773 L-0.6486550681260723,6.575935660291831 L-0.6546556182522949,6.548280957727307 L-0.6630441466136332,6.520747411882833 L-0.6738084327980463,6.493375133640871 L-0.6869327953883859,6.46620399894917 L-0.7023981148070924,6.4392735907294565 L-0.720181861169602,6.412623141213021 L-0.7625976655023687,6.360316951435912 L-0.8139331329500075,6.309590117337045 L-0.8738892303281611,6.26073812676307 L-0.942116708596892,6.214045546447864 " />
			<path d="M-3.64558204630973,6.918289126070202 L-3.64558204630973,7.048848990024165 " />
			<path d="M-5.570777059529474,7.643330230146686 L-5.570777059529474,4.053554960511206 " />
			<path d="M0.9830783046228458,-78.74015453010846 L0.9830783046228457,-82.32992979974394 " />
			<path d="M0.9830783046228457,-82.32992979974394 L10.900609370265819,-76.08006078157511 " />
			<path d="M12.534248383941316,-75.05056767579471 L35.39081896642254,-60.64672347308667 " />
			<path d="M35.39081896642255,-57.05694820345119 L35.39081896642255,-60.64672347308667 " />
			<path d="M0.9830783046228458,-78.74015453010846 L1.8670203229947986,-78.18310844697402 " />
			<path d="M12.534248383941316,-71.46079240615923 L35.39081896642254,-57.05694820345119 " />
			<path d="M-0.9421167085968991,-78.4915366136187 L-0.9421167085968991,-79.94056092480368 " />
			<path d="M-0.9421167085968991,-81.73544855962142 L-0.9421167085968991,-79.94056092480368 " />
			<path d="M0.9830783046228457,-82.32992979974394 L-0.9421167085968991,-81.73544855962142 " />
			<path d="M0.9830783046228458,-78.74015453010846 L-0.2706982260380818,-78.35300069807288 " />
			<path d="M-3.7938493774533146,-80.85486162591417 L-5.570777059529477,-80.30616387592259 " />
			<path d="M35.39081896642255,-57.05694820345119 L28.836963602270227,-55.03318227962985 " />
			<path d="M12.534248383941314,-65.30689194392698 L28.836963602270224,-55.03318227962985 " />
			<path d="M-5.570777059529477,-77.84271071269958 L-5.570777059529477,-80.30616387592259 " />
			<path d="M-3.522697258231873,7.010903378952516 L-3.450894495695315,7.052545429718228 L-3.37185800001284,7.0915548158796184 L-3.2860818996411023,7.1276876545619166 L-3.1941024583874533,7.160718046784423 L-3.096494722740963,7.1904394897588935 L-2.9938689267378935,7.216666167924812 L-2.886866676838071,7.239234114650138 L-2.7761569406639195,7.258002237334688 L-2.6624318646801814,7.272853199507301 L-2.5464024469617765,7.283694154402001 L-2.428794092103235,7.2904573254269165 L-2.3103420760599747,7.293100429896919 L-2.1917869492747943,7.291606943380842 L-2.0738699068287882,7.285986203010612 L-1.957328154562041,7.276273349106413 L-1.842890300134672,7.26252910548283 L-1.7312717978428607,7.244839399809493 L-1.6231704756684167,7.223314826399666 L-1.5192621725263502,7.198089954785406 L-1.4201965129859402,7.16932248840197 L-1.326592845881335,7.137192278641341 L-1.2390363722030915,7.101900200438875 L-1.1580744864787,7.063666896422813 L-1.0842133545154287,7.022731397478102 L-1.0179147489011,6.979349628348638 L-0.9595931620469427,6.933792807620743 L-0.9096132148214928,6.886345752091037 L-0.8682873769765136,6.837305096119623 L-0.8509526481569436,6.812282642512391 L-0.8358740136166061,6.786977437101024 L-0.8230750501094253,6.761429046770668 L-0.8125757699257907,6.735677418647195 L-0.804392589601604,6.7097628176364115 L-0.7985383042495993,6.6837257634663745 L-0.7950220675530746,6.657606967331288 L-0.7938493774533129,6.631447268236017 " />
			<path d="M-0.7938493774533129,6.631447268236014 L-0.7956561931455544,6.598979523762124 L-0.8010722874450176,6.566589996928512 L-0.8100846125061416,6.5343567169423045 L-0.8226714568484672,6.502357336598292 L-0.838802497661497,6.470668945206537 L-0.8584388738549995,6.439367882877478 L-0.881533279678782,6.4085295566119145 L-0.9080300786863829,6.37822825863894 L-0.9378654377681479,6.3485369874394495 L-0.9709674809307807,6.319527271886412 L-1.0072564624529052,6.2912689989255455 L-1.0466449589994955,6.263830245211546 L-1.0890380802323458,6.237277113105461 L-1.134333697409208,6.211673571428312 L-1.1824226894208751,6.187081301354607 L-1.2331892056734923,6.163559547816981 L-1.3422594512078452,6.119951538726731 L-1.4604940279239107,6.081269513123663 L-1.5867542722143184,6.047886000060082 L-1.7198242289056798,6.020122501016074 L-1.8584223615716207,5.9982463936645045 L-2.0012138944291213,5.982468356877867 L-2.146823666958972,5.972940341775569 L-2.2938493774533137,5.969754108351587 L-2.4408750879476555,5.972940341775569 L-2.5864848604775066,5.982468356877868 L-2.7292763933350073,5.9982463936645045 L-2.8678745260009477,6.020122501016074 L-3.0009444826923093,6.047886000060083 L-3.1272047269827166,6.081269513123664 L-3.2454393036987823,6.119951538726732 L-3.3545095492331347,6.163559547816982 L-3.405276065485752,6.187081301354608 L-3.4533650574974186,6.211673571428313 L-3.4986606746742805,6.237277113105461 L-3.541053795907131,6.263830245211547 L-3.5804422924537223,6.291268998925547 L-3.616731273975846,6.319527271886414 L-3.6498333171384787,6.34853698743945 L-3.6796686762202437,6.3782282586389405 L-3.7061654752278446,6.408529556611915 L-3.729259881051626,6.4393678828774785 L-3.748896257245129,6.470668945206538 L-3.7650272980581585,6.502357336598292 L-3.777614142400484,6.534356716942305 L-3.786626467461608,6.566589996928513 L-3.7920425617610714,6.598979523762125 L-3.793849377453313,6.631447268236009 " />
			<path d="M-3.793849377453313,6.631447268236015 L-3.79275677710251,6.6566982100935075 L-3.789480567750804,6.681912366367091 L-3.784025522181511,6.707053005062112 L-3.776399587307567,6.732083501284362 L-3.7666138725944642,6.756967390595236 L-3.754682633875974,6.781668422133146 L-3.7244562104385044,6.830378292802373 L-3.6858963883178077,6.877929374417926 L-3.639227781547227,6.924044678144169 L-3.5847222384761777,6.9684555786659645 L-3.522697258231874,7.010903378952516 " />
			<path d="M-0.9421167085968991,-81.60488869566746 L-1.0015634914345672,-81.6539996884238 L-1.070158712222723,-81.70073238095945 L-1.147416767018871,-81.74475594002571 L-1.232790725358071,-81.78575871105541 L-1.3256762021201998,-81.82345042444902 L-1.4254156361341161,-81.85756425047103 L-1.5313029452293305,-81.88785868820898 L-1.6425885247808292,-81.91411927522316 L-1.7584845543610061,-81.93616010578371 L-1.8781705749315059,-81.95382514694705 L-2.000799297092533,-81.96698934315486 L-2.1255025992714747,-81.97555950153591 L-2.2513976733880527,-81.97947495164333 L-2.3775932744892043,-81.97870797495696 L-2.5031960301108427,-81.97326400111027 L-2.6273167647008364,-81.96318156945233 L-2.7490767943309202,-81.94853205621766 L-2.8676141471356025,-81.92941916923459 L-2.982089665441894,-81.90597821374982 L-3.0916929463912606,-81.87837513456633 L-3.195648078998536,-81.84680534127565 L-3.293219137033633,-81.81149232490111 L-3.383715388840457,-81.77268607574484 L-3.4664961872113276,-81.73066131363963 L-3.540975504700162,-81.68571554313354 L-3.606626082267756,-81.63816694737558 L-3.6629831618897524,-81.5883521356119 L-3.687549312353349,-81.56270454348073 L-3.7096477767031915,-81.53662376023884 L-3.729239427382301,-81.51015596453986 L-3.746289575399803,-81.48334802028207 L-3.7607680317512724,-81.45624739363096 L-3.7726491608714117,-81.42890206897569 L-3.7819119260243985,-81.4013604639679 L-3.788539926551547,-81.37367134379336 L-3.7925214269103256,-81.3458837348283 L-3.793849377453316,-81.31804683783326 " />
			<path d="M-14.600000000000003,-71.79550539270961 L-14.600000000000001,8.881784197001252e-16 " />
			<path d="M1.7061506225466863,-1.4455470884438175 L1.7061506225466863,2.144228181191663 " />
			<path d="M-6.293849377453313,-1.4455470884438175 L-6.293849377453313,2.144228181191663 " />
			<path d="M-0.7938493774533134,1.8410022819911722 L-0.7938493774533134,2.5784867866814345 " />
			<path d="M-0.7938493774533133,6.328221369035524 L-0.7938493774533133,6.6314472682360135 " />
			<path d="M-3.793849377453315,-81.31804683783325 L-3.793849377453315,-78.46657702120773 " />
			<path d="M-3.7938493774533124,1.841002281991173 L-3.7938493774533124,6.631447268236014 " />

       </g>
    </g>
    
</svg>

```

=== file: docs/figures/cad/cam_ramp.svg ===
```svg
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   width="720.0"
   height="540.0"

>
    <g transform="scale(13.452122515298367, -13.452122515298367)   translate(35.89449488792685,-21.134148403226035)" stroke-width="0.4"  fill="none">
       <!-- hidden lines -->
       <g  stroke="rgb(180,180,180)" fill="none" stroke-dasharray="0.4,0.4" >
			<path d="M-28.673117218166414,-0.12046225737031868 L-34.4077406617997,-3.7343299784798623 " />
			<path d="M-28.673117218166414,-0.12046225737031868 L0.0,-1.6375789613221059e-15 " />
			<path d="M-28.673117218166414,8.853975916718383 L-28.673117218166414,-0.12046225737031868 " />
			<path d="M-28.673117218166414,8.853975916718383 L-22.938493774533132,12.467843637827926 " />
			<path d="M-22.938493774533132,19.64739417709889 L-22.938493774533132,12.467843637827928 " />
			<path d="M5.734623443633283,3.6138677211095436 L-22.93849377453313,12.467843637827926 " />

       </g>

       <!-- solid lines -->
       <g  stroke="rgb(40,40,40)" fill="none">
			<path d="M0.0,0.0 L-5.734623443633283,-3.6138677211095436 " />
			<path d="M-28.673117218166414,8.853975916718383 L-34.4077406617997,5.24010819560884 " />
			<path d="M0.0,0.0 L-28.67311721816641,8.853975916718383 " />
			<path d="M-5.734623443633283,-3.6138677211095436 L-34.40774066179969,5.24010819560884 " />
			<path d="M-34.4077406617997,-3.7343299784798623 L-5.734623443633286,-3.6138677211095454 " />
			<path d="M-34.4077406617997,5.24010819560884 L-34.4077406617997,-3.7343299784798623 " />
			<path d="M2.2204460492503126e-16,7.179550539270961 L-28.67311721816641,16.033526455989346 " />
			<path d="M-28.673117218166414,16.033526455989346 L-28.673117218166414,8.853975916718385 " />
			<path d="M2.2204460492503126e-16,7.179550539270961 L0.0,0.0 " />
			<path d="M2.2204460492503126e-16,7.179550539270961 L5.734623443633283,10.793418260380506 " />
			<path d="M5.734623443633283,10.793418260380506 L-22.93849377453313,19.64739417709889 " />
			<path d="M-28.673117218166414,16.033526455989346 L-22.938493774533132,19.64739417709889 " />
			<path d="M0.0,0.0 L5.734623443633283,3.6138677211095436 " />
			<path d="M5.734623443633283,10.793418260380506 L5.734623443633283,3.6138677211095445 " />

       </g>
    </g>
    
</svg>

```

=== file: docs/figures/cad/pin.svg ===
```svg
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   width="720.0"
   height="540.0"

>
    <g transform="scale(4.536652094881678, -4.536652094881678)   translate(5.908537304979663,-5.070230464864087)" stroke-width="0.4"  fill="none">
       <!-- hidden lines -->
       <g  stroke="rgb(180,180,180)" fill="none" stroke-dasharray="0.4,0.4" >
			<path d="M-1.228847880778563,-87.57003799535276 L-1.1570451182420047,-87.52839594458705 L-1.07800862255953,-87.48938655842566 L-0.9922325221877923,-87.45325371974336 L-0.9002530809341434,-87.42022332752086 L-0.8026453452876525,-87.39050188454638 L-0.7000195492845832,-87.36427520638047 L-0.5930172993847606,-87.34170725965514 L-0.48230756321060914,-87.32293913697059 L-0.36858248722687115,-87.30808817479797 L-0.25255306950846657,-87.29724721990328 L-0.13494471464992516,-87.29048404887837 L-0.016492698606664673,-87.28784094440836 L0.10206242817851559,-87.28933443092444 L0.21997947062452208,-87.29495517129467 L0.3365212228912693,-87.30466802519886 L0.45095907731863816,-87.31841226882246 L0.5625775796104496,-87.33610197449579 L0.6706789017848935,-87.35762654790561 L0.77458720492696,-87.38285141951988 L0.87365286446737,-87.41161888590331 L0.9672565315719753,-87.44374909566395 L1.0548130052502187,-87.4790411738664 L1.1357748909746102,-87.51727447788247 L1.2096360229378815,-87.55820997682719 L1.2759346285522102,-87.60159174595664 L1.3342562154063675,-87.64714856668454 L1.3842361626318174,-87.69459562221425 L1.4255620004767966,-87.74363627818566 L1.4428967292963666,-87.7686587317929 L1.4579753638367041,-87.79396393720425 L1.470774327343885,-87.81951232753461 L1.4812736075275195,-87.84526395565808 L1.4894567878517062,-87.87117855666887 L1.495311073203711,-87.89721561083891 L1.4988273099002356,-87.92333440697399 L1.4999999999999973,-87.94949410606927 " />
			<path d="M-1.5000000000000027,-87.94949410606927 L-1.4989073996492,-87.92424316421177 L-1.495631190297494,-87.8990290079382 L-1.4901761447282007,-87.87388836924318 L-1.482550209854257,-87.84885787302092 L-1.472764495141154,-87.82397398371005 L-1.4608332564226634,-87.79927295217213 L-1.4306068329851942,-87.7505630815029 L-1.3920470108644973,-87.70301199988735 L-1.3453784040939167,-87.65689669616111 L-1.2908728610228677,-87.61248579563932 L-1.228847880778564,-87.57003799535276 " />

       </g>

       <!-- solid lines -->
       <g  stroke="rgb(40,40,40)" fill="none">
			<path d="M-1.2288478807785603,0.37945611071650226 L-1.157045118242002,0.4210981614822141 L-1.0780086225595273,0.4601075476436045 L-0.9922325221877897,0.49624038632590195 L-0.9002530809341407,0.5292707785484086 L-0.8026453452876499,0.5589922215228793 L-0.7000195492845805,0.5852188996887974 L-0.5930172993847579,0.6077868464141235 L-0.4823075632106064,0.626554969098674 L-0.3685824872268684,0.641405931271287 L-0.25255306950846385,0.6522468861659865 L-0.13494471464992244,0.6590100571909019 L-0.016492698606661953,0.6616531616609043 L0.10206242817851831,0.6601596751448274 L0.2199794706245248,0.654538934774598 L0.336521222891272,0.6448260808703988 L0.4509590773186409,0.631081837246816 L0.5625775796104523,0.6133921315734782 L0.6706789017848962,0.5918675581636522 L0.7745872049269626,0.5666426865493913 L0.8736528644673727,0.5378752201659553 L0.967256531571978,0.5057450104053263 L1.0548130052502214,0.47045293220286066 L1.1357748909746128,0.43221962818679827 L1.2096360229378842,0.3912841292420876 L1.2759346285522128,0.34790236011262377 L1.3342562154063702,0.30234553938472897 L1.38423616263182,0.2548984838550225 L1.4255620004767993,0.20585782788360835 L1.4428967292963693,0.1808353742763758 L1.4579753638367068,0.1555301688650094 L1.4707743273438876,0.12998177853465331 L1.4812736075275221,0.10423015041118094 L1.4894567878517089,0.07831554940039678 L1.4953110732037136,0.05227849523036029 L1.4988273099002383,0.026159699095274363 L1.5,2.6329090684651364e-15 " />
			<path d="M1.5,-3.055988568975264e-16 L1.4981931843077585,-0.032467744473889684 L1.4927770900082953,-0.06485727130750263 L1.4837647649471712,-0.09709055129370976 L1.4711779206048456,-0.12908993163772242 L1.455046879791816,-0.16077832302947723 L1.4354105035983133,-0.19207938535853644 L1.4123160977745308,-0.22291771162409976 L1.38581929876693,-0.25321900959707494 L1.355983939685165,-0.2829102807965649 L1.3228818965225322,-0.31191999634960227 L1.2865929150004076,-0.3401782693104685 L1.2472044184538174,-0.3676170230244683 L1.204811297220967,-0.3941701551305538 L1.1595156800441049,-0.4197736968077021 L1.1114266880324377,-0.4443659668814073 L1.0606601717798205,-0.46788772041903304 L0.9515899262454677,-0.5114957295092831 L0.8333553495294022,-0.5501777551123509 L0.7070951052389944,-0.5835612681759325 L0.574025148547633,-0.6113247672199408 L0.43542701588169225,-0.6332008745715099 L0.2926354830241916,-0.6489789113581473 L0.14702571049434066,-0.6585069264604457 L-1.097650956072099e-15,-0.6616931598844269 L-0.1470257104943428,-0.6585069264604456 L-0.2926354830241938,-0.6489789113581471 L-0.43542701588169447,-0.6332008745715095 L-0.574025148547635,-0.6113247672199403 L-0.7070951052389964,-0.583561268175932 L-0.8333553495294039,-0.5501777551123503 L-0.9515899262454695,-0.5114957295092823 L-1.060660171779822,-0.46788772041903226 L-1.1114266880324393,-0.44436596688140645 L-1.1595156800441058,-0.41977369680770155 L-1.2048112972209677,-0.3941701551305535 L-1.2472044184538185,-0.3676170230244674 L-1.2865929150004094,-0.34017826931046713 L-1.3228818965225335,-0.31191999634960105 L-1.3559839396851658,-0.28291028079656383 L-1.3858192987669309,-0.25321900959707383 L-1.4123160977745317,-0.22291771162409874 L-1.4354105035983136,-0.19207938535853564 L-1.4550468797918161,-0.16077832302947673 L-1.4711779206048459,-0.12908993163772195 L-1.4837647649471715,-0.09709055129370923 L-1.4927770900082953,-0.06485727130750209 L-1.4981931843077585,-0.03246774447388916 L-1.5,-5.358600242318549e-15 " />
			<path d="M-1.5,6.8048369046080885e-16 L-1.4989073996491973,0.025250941857492812 L-1.4956311902974913,0.05046509813107614 L-1.490176144728198,0.07560573682609775 L-1.4825502098542542,0.1006362330483475 L-1.4727644951411514,0.1255201223592211 L-1.4608332564226607,0.15022115389713142 L-1.4306068329851915,0.19893102456635828 L-1.3920470108644947,0.24648210618191116 L-1.345378404093914,0.29259740990815425 L-1.290872861022865,0.3370083104299499 L-1.2288478807785614,0.3794561107165017 " />
			<path d="M1.4999999999999973,-87.94949410606927 L1.4981931843077558,-87.98196185054316 L1.4927770900082926,-88.01435137737677 L1.4837647649471686,-88.04658465736297 L1.471177920604843,-88.07858403770699 L1.4550468797918132,-88.11027242909874 L1.4354105035983107,-88.1415734914278 L1.4123160977745282,-88.17241181769337 L1.3858192987669273,-88.20271311566634 L1.3559839396851623,-88.23240438686584 L1.3228818965225295,-88.26141410241887 L1.286592915000405,-88.28967237537974 L1.2472044184538147,-88.31711112909373 L1.2048112972209644,-88.34366426119982 L1.1595156800441022,-88.36926780287696 L1.111426688032435,-88.39386007295067 L1.0606601717798179,-88.4173818264883 L0.951589926245465,-88.46098983557854 L0.8333553495293995,-88.49967186118161 L0.7070951052389918,-88.5330553742452 L0.5740251485476303,-88.56081887328921 L0.4354270158816895,-88.58269498064078 L0.2926354830241889,-88.59847301742741 L0.14702571049433794,-88.60800103252971 L-3.817697366403732e-15,-88.61118726595369 L-0.1470257104943455,-88.60800103252971 L-0.2926354830241965,-88.59847301742741 L-0.4354270158816972,-88.58269498064078 L-0.5740251485476376,-88.56081887328921 L-0.7070951052389991,-88.5330553742452 L-0.8333553495294066,-88.49967186118161 L-0.9515899262454721,-88.46098983557854 L-1.0606601717798247,-88.4173818264883 L-1.111426688032442,-88.39386007295067 L-1.1595156800441084,-88.36926780287696 L-1.2048112972209704,-88.34366426119982 L-1.2472044184538211,-88.31711112909373 L-1.286592915000412,-88.28967237537974 L-1.3228818965225362,-88.26141410241887 L-1.3559839396851685,-88.23240438686582 L-1.3858192987669335,-88.20271311566634 L-1.4123160977745344,-88.17241181769336 L-1.4354105035983162,-88.1415734914278 L-1.4550468797918188,-88.11027242909874 L-1.4711779206048485,-88.07858403770699 L-1.4837647649471741,-88.04658465736297 L-1.492777090008298,-88.01435137737677 L-1.4981931843077612,-87.98196185054316 L-1.5000000000000027,-87.94949410606927 " />
			<path d="M1.4999999999999973,-87.94949410606927 L1.5,-5.551115123125783e-17 " />
			<path d="M-1.5000000000000027,-87.94949410606927 L-1.5,5.551115123125783e-17 " />

       </g>
    </g>
    
</svg>

```

=== file: docs/figures/cad/slot_board.svg ===
```svg
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   width="720.0"
   height="540.0"

>
    <g transform="scale(2.9400267763140944, -2.9400267763140944)   translate(98.63855742279068,-62.636915423748704)" stroke-width="0.4"  fill="none">
       <!-- hidden lines -->
       <g  stroke="rgb(180,180,180)" fill="none" stroke-dasharray="0.4,0.4" >
			<path d="M91.83589829018443,-53.66593565847673 L-88.39512422400445,1.987627246610252 " />
			<path d="M-88.39512422400445,1.9876272466102485 L-91.83589829018442,-0.18069338605547758 " />
			<path d="M-88.39512422400445,55.83425629114245 L-88.39512422400445,1.987627246610245 " />
			<path d="M85.36396611808401,-22.859520269878423 L85.36396611808401,-26.62878430299568 " />
			<path d="M85.36396611808401,-22.859520269878423 L-22.68621869527331,10.50531156390339 " />
			<path d="M-22.68621869527332,10.50531156390339 L-46.94124754546361,23.309155606539747 " />
			<path d="M-46.941247545463604,23.309155606539754 L-70.29009878053367,40.750235113050195 " />
			<path d="M-70.29009878053367,41.35890913423818 L-70.29009878053367,40.750235113050195 " />
			<path d="M-70.29009878053367,41.35890913423818 L-71.67916954372524,41.78784049145119 " />
			<path d="M-71.67916954372525,41.78784049145119 L-72.96888936933883,42.75123289963369 " />
			<path d="M-72.96888936933881,42.75123289963369 L-73.17524454143698,42.24981370135917 " />
			<path d="M-73.175244541437,42.24981370135918 L-81.92319205190404,44.95109364902107 " />
			<path d="M-81.92319205190402,44.95109364902107 L-81.92319205190402,41.181829615903816 " />
			<path d="M-72.34180208352207,38.22319085391412 L-81.92319205190404,41.18182961590381 " />
			<path d="M-49.40115793762784,21.087033085340984 L-72.34180208352207,38.223190853914126 " />
			<path d="M-49.40115793762784,21.087033085340988 L-49.457902133281166,20.793747373927143 " />
			<path d="M-47.92580885064143,19.984979692352688 L-49.457902133281166,20.793747373927147 " />
			<path d="M-46.47512464233726,18.901350422495128 L-47.925808850641424,19.9849796923527 " />
			<path d="M-46.36766655283325,19.16246114988497 L-46.475124642337256,18.901350422495128 " />
			<path d="M-24.57695761557121,7.659492403302901 L-46.367666552833256,19.16246114988497 " />
			<path d="M-24.576957615571207,7.659492403302901 L-24.576957615571207,7.319889069107381 " />
			<path d="M-23.02692246968914,6.8412534974224215 L-24.576957615571203,7.319889069107376 " />
			<path d="M-21.506987958995406,6.038904238217537 L-23.026922469689133,6.841253497422421 " />
			<path d="M-21.446190578567656,6.353139073438166 L-21.506987958995406,6.038904238217536 " />
			<path d="M85.36396611808401,-26.628784302995676 L-21.446190578567666,6.353139073438172 " />
			<path d="M85.36396611808401,-22.859520269878423 L82.49665439626736,-24.666454130433195 " />
			<path d="M82.49665439626736,-24.666454130433195 L82.49665439626736,-28.43571816355045 " />
			<path d="M85.36396611808401,-26.628784302995676 L82.49665439626736,-28.435718163550447 " />
			<path d="M-25.553530417090162,8.698377703348683 L-22.68621869527352,10.505311563903454 " />
			<path d="M82.49665439626736,-24.666454130433195 L-25.55353041708996,8.69837770334862 " />
			<path d="M-49.808559267280174,21.502221745984933 L-46.94124754546353,23.309155606539704 " />
			<path d="M-25.55353041708996,8.69837770334862 L-49.80855926728026,21.502221745984976 " />
			<path d="M-73.15741050235032,38.943301252495424 L-70.29009878053367,40.750235113050195 " />
			<path d="M-49.808559267280245,21.502221745984983 L-73.15741050235032,38.943301252495424 " />
			<path d="M-73.15741050235032,39.55197527368341 L-73.15741050235032,38.943301252495424 " />
			<path d="M-70.29009878053367,41.35890913423818 L-73.15741050235032,39.55197527368341 " />
			<path d="M-71.67916954372524,41.78784049145119 L-74.54648126554189,39.98090663089642 " />
			<path d="M-73.15741050235032,39.55197527368341 L-74.54648126554189,39.98090663089642 " />
			<path d="M-72.96888936933881,42.75123289963369 L-75.83620109115546,40.94429903907892 " />
			<path d="M-74.54648126554189,39.98090663089642 L-75.83620109115546,40.94429903907893 " />
			<path d="M-75.83620109115546,40.94429903907893 L-76.04255626325363,40.44287984080441 " />
			<path d="M-73.175244541437,42.24981370135919 L-76.04255626325364,40.442879840804416 " />
			<path d="M-81.92319205190402,44.95109364902107 L-84.79050377372067,43.1441597884663 " />
			<path d="M-76.04255626325364,40.44287984080441 L-84.79050377372069,43.1441597884663 " />
			<path d="M-84.79050377372067,43.1441597884663 L-84.79050377372067,39.374895755349044 " />
			<path d="M-81.92319205190402,41.18182961590381 L-84.79050377372067,39.37489575534904 " />
			<path d="M-75.20911380533872,36.41625699335935 L-84.79050377372069,39.37489575534904 " />
			<path d="M-72.34180208352205,38.22319085391412 L-75.2091138053387,36.41625699335935 " />
			<path d="M-52.268469659444484,19.280099224786213 L-75.20911380533872,36.416256993359355 " />
			<path d="M-49.401157937627836,21.087033085340984 L-52.26846965944448,19.280099224786213 " />
			<path d="M-52.268469659444484,19.280099224786216 L-52.32521385509781,18.986813513372372 " />
			<path d="M-49.457902133281166,20.793747373927147 L-52.32521385509781,18.986813513372375 " />
			<path d="M-50.79312057245807,18.178045831797917 L-52.325213855097815,18.986813513372375 " />
			<path d="M-50.793120572457994,18.178045831797874 L-47.92580885064135,19.984979692352645 " />
			<path d="M-49.342436364153905,17.094416561940356 L-50.793120572458065,18.178045831797927 " />
			<path d="M-46.47512464233726,18.901350422495128 L-49.342436364153905,17.094416561940356 " />
			<path d="M-49.23497827464989,17.355527289330198 L-49.3424363641539,17.094416561940356 " />
			<path d="M-49.2349782746499,17.355527289330198 L-46.367666552833256,19.16246114988497 " />
			<path d="M-27.44426933738785,5.852558542748129 L-49.23497827464989,17.355527289330198 " />
			<path d="M-24.576957615571207,7.6594924033029 L-27.444269337387848,5.8525585427481275 " />
			<path d="M-27.444269337387848,5.852558542748129 L-27.444269337387848,5.51295520855261 " />
			<path d="M-24.576957615571207,7.31988906910738 L-27.444269337387848,5.512955208552608 " />
			<path d="M-25.894234191505788,5.03431963686765 L-27.44426933738785,5.512955208552604 " />
			<path d="M-25.894234191505976,5.034319636867711 L-23.026922469689335,6.841253497422483 " />
			<path d="M-24.374299680812047,4.2319703776627655 L-25.894234191505774,5.034319636867649 " />
			<path d="M-21.506987958995406,6.038904238217537 L-24.374299680812047,4.2319703776627655 " />
			<path d="M-24.313502300384297,4.546205212883395 L-24.374299680812047,4.231970377662765 " />
			<path d="M-24.3135023003843,4.546205212883397 L-21.44619057856766,6.353139073438168 " />
			<path d="M82.49665439626736,-28.435718163550447 L-24.313502300384314,4.5462052128834 " />

       </g>

       <!-- solid lines -->
       <g  stroke="rgb(40,40,40)" fill="none">
			<path d="M91.83589829018443,0.18069338605547713 L88.39512422400446,-1.987627246610249 " />
			<path d="M88.39512422400445,-1.9876272466102485 L88.39512422400445,-55.83425629114245 " />
			<path d="M91.83589829018443,-53.66593565847673 L88.39512422400446,-55.83425629114245 " />
			<path d="M91.83589829018443,0.18069338605547713 L91.83589829018443,-53.66593565847673 " />
			<path d="M91.83589829018443,0.18069338605547713 L-88.39512422400445,55.83425629114245 " />
			<path d="M-88.39512422400445,55.83425629114245 L-91.83589829018442,53.66593565847673 " />
			<path d="M88.39512422400445,-1.9876272466102485 L-91.83589829018443,53.66593565847673 " />
			<path d="M88.39512422400445,-55.83425629114245 L-91.83589829018443,-0.18069338605547358 " />
			<path d="M-91.83589829018443,53.66593565847673 L-91.83589829018443,-0.1806933860554807 " />

       </g>
    </g>
    
</svg>

```

=== file: docs/figures/cad/strike_off_bar.svg ===
```svg
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   width="720.0"
   height="540.0"

>
    <g transform="scale(8.907486530400268, -8.907486530400268)   translate(32.556883359886314,-22.61547002200261)" stroke-width="0.4"  fill="none">
       <!-- hidden lines -->
       <g  stroke="rgb(180,180,180)" fill="none" stroke-dasharray="0.4,0.4" >
			<path d="M-30.3115810592045,-19.358284759410125 L27.03465337712833,16.78039245168531 " />
			<path d="M27.034653377128336,20.370167721320797 L27.034653377128336,16.780392451685316 " />
			<path d="M30.3115810592045,15.768509489774644 L27.034653377128336,16.780392451685316 " />

       </g>

       <!-- solid lines -->
       <g  stroke="rgb(40,40,40)" fill="none">
			<path d="M-27.034653377128336,-16.780392451685316 L-27.034653377128336,-20.370167721320797 " />
			<path d="M-27.034653377128336,-20.370167721320797 L30.311581059204492,15.768509489774637 " />
			<path d="M30.3115810592045,19.358284759410125 L30.3115810592045,15.768509489774644 " />
			<path d="M-27.034653377128336,-16.780392451685316 L30.311581059204492,19.358284759410118 " />
			<path d="M-30.3115810592045,-15.768509489774644 L-30.3115810592045,-19.358284759410125 " />
			<path d="M-30.3115810592045,-15.768509489774644 L27.03465337712833,20.37016772132079 " />
			<path d="M-27.034653377128336,-16.780392451685316 L-30.3115810592045,-15.768509489774644 " />
			<path d="M-27.034653377128336,-20.370167721320797 L-30.3115810592045,-19.358284759410125 " />
			<path d="M30.3115810592045,19.358284759410125 L27.034653377128336,20.370167721320797 " />

       </g>
    </g>
    
</svg>

```

=== file: docs/figures/cad/trough.svg ===
```svg
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   width="720.0"
   height="540.0"

>
    <g transform="scale(4.893756045221291, -4.893756045221291)   translate(18.686840417705298,-8.250016032423492)" stroke-width="0.4"  fill="none">
       <!-- hidden lines -->
       <g  stroke="rgb(180,180,180)" fill="none" stroke-dasharray="0.4,0.4" >
			<path d="M1.7061506225466871,-0.5268424917801267 L-1.7763568394002505e-14,5.329070518200751e-15 " />
			<path d="M-1.7763568394002505e-14,5.329070518200751e-15 L-6.293849377453313,1.9434786384550677 " />
			<path d="M-10.322322198539908,3.187431330018618 L-10.322322198539908,1.3925436952008776 " />
			<path d="M10.32232219853991,-4.982318964836358 L-10.32232219853991,1.3925436952008772 " />
			<path d="M10.322322198539908,-3.187431330018618 L10.322322198539908,-4.982318964836358 " />
			<path d="M-5.570777059529474,-0.4336641265331447 L-5.454276002414901,-0.3639533501152974 L-5.330161200740118,-0.29684822774950637 L-5.19873165793353,-0.23251042155326518 L-5.060303999275629,-0.17109492693702677 L-4.915211709120951,-0.11274969920668321 L-4.7638043275050626,-0.05761529712627622 L-4.606446608071997,-0.0058245442996198715 L-4.443517639350778,0.04249779081339189 L-4.275409931497945,0.08723529547493514 L-4.102528470706213,0.12828019311773753 L-3.925289743557257,0.16553360298826902 L-3.7441207336690576,0.19890577835913859 L-3.559457893054966,0.22831632273682012 L-3.371746090672577,0.25369438354384855 L-3.1814375406954407,0.2749788228088841 L-2.9889907130895135,0.29211836445344064 L-2.7948692291188486,0.3050717178204496 L-2.599540744441365,0.31380767714707036 L-2.4034758224854063,0.31830519674210533 L-2.2071468008212225,0.31855344168691424 L-2.0110266532583942,0.3145518139376806 L-1.8155878504104965,0.30630995376615444 L-1.6213012214720073,0.2938477165353899 L-1.4286348199495378,0.27719512486643927 L-1.2380527960799401,0.25639229631122795 L-1.050014278651729,0.2314893467058574 L-0.8649722689236186,0.20254626943716847 L-0.6833725493048093,0.16963279091341543 L-0.5056526094261198,0.13282820258724182 L-0.33224059218914626,0.09222116993562679 L-0.16355426233251125,0.047909518856984246 L-3.108624468950438e-14,9.547918011776346e-15 " />
			<path d="M-1.687538997430238e-14,4.884981308350689e-15 L0.19238380234804042,-0.06328258384711405 L0.37581853876742466,-0.1315405562792602 L0.4639723507588691,-0.16745921058195212 L0.5496439455454794,-0.2045282263047692 L0.6327562131732773,-0.24271423894570288 L0.7132343472475875,-0.2819828786335623 L0.7910059122636186,-0.3222988010630776 L0.8660009088030787,-0.3636257193070489 L0.9381518365381587,-0.40592643647691706 L1.0073937549861824,-0.4491628792023621 L1.07366434196022,-0.49329613189978805 L1.1369039496630688,-0.5382864717988526 L1.1970556583741172,-0.5840934046955233 L1.2540653276807592,-0.6306757013994683 L1.3078816452082496,-0.6779914348429807 L1.3584561728041504,-0.7259980178180434 L1.4057433901357879,-0.7746522413075593 L1.4497007356614828,-0.82391031337625 L1.4902886449386803,-0.8737278985862165 L1.5274705862344953,-0.9240601579016903 L1.561213093406629,-0.9748617890470568 L1.5914857960250504,-1.0260870672818179 L1.6182614467073382,-1.077689886555805 L1.6415159456430817,-1.1296238010075932 L1.6612283622852644,-1.1818420667687717 L1.6773809541891023,-1.2342976840364341 L1.689959182981386,-1.2869434393760264 L1.6989517274459565,-1.3397319482164844 L1.7043504937135272,-1.3926156974993973 L1.7061506225466867,-1.4455470884438104 " />
			<path d="M-6.293849377453313,-1.4455470884438157 L-6.2909357765178395,-1.3782112434905034 L-6.282199218246623,-1.3109734934276145 L-6.267652430061841,-1.2439317902408902 L-6.247316603731324,-1.177183800314891 L-6.221221364496383,-1.1108267621525612 L-6.189404727913741,-1.0449573447181337 L-6.151913044474454,-0.9796715066097363 L-6.108800932080491,-0.9150643562668621 L-6.060131196477354,-0.8512300134163495 L-6.005974739758632,-0.788261471958721 L-5.946410457075807,-0.7262504644946248 L-5.881525121703751,-0.6652873286887394 L-5.811413258629381,-0.6054608756658213 L-5.73617700684762,-0.5468582606306176 L-5.655925970565253,-0.4895648559001222 L-5.570777059529477,-0.43366412653314623 " />
			<path d="M-10.322322198539908,1.3925436952008776 L-10.32232219853991,-66.81318642787326 " />
			<path d="M-10.32232219853991,-66.81318642787326 L-10.32232219853991,-68.608074062691 " />
			<path d="M-10.32232219853991,-68.608074062691 L-9.175397509813253,-67.8853005184691 " />
			<path d="M-9.175397509813251,2.833272293349882 L-9.175397509813253,-67.8853005184691 " />
			<path d="M10.650014966747525,-5.0835072610274255 L10.32232219853991,-4.982318964836358 " />
			<path d="M-10.650014966747525,1.4937319913919456 L-10.790347048948027,1.4034757813749097 L-10.926748927613808,1.3120546209492676 L-11.059170920640735,1.219501808744459 L-11.187564795531497,1.1258510555751589 L-11.311883786963474,1.0311364721626852 L-11.432082613822221,0.935392556710746 L-11.548117495694374,0.8386541823400291 L-11.659946168813923,0.7409565843862616 L-11.76752790145607,0.6423353475663307 L-11.870823508773105,0.5428263930171353 L-11.969795367066817,0.44246596521191583 L-12.064407427492288,0.3412906187588216 L-12.154625229188103,0.23933720508648748 L-12.240415911828132,0.13664285902152784 L-12.321748227590344,0.03324498526280206 L-12.398592552538325,-0.07081875524263626 L-12.470920897411295,-0.17551045901690188 L-12.538706917818706,-0.2807919938569787 L-12.601925923835784,-0.38662501272375205 L-12.660554888996392,-0.4929709677092706 L-12.714572458680045,-0.5997911240771681 L-12.763958957889978,-0.7070465743711585 L-12.808696398419427,-0.8146982525864216 L-12.848768485403536,-0.922706948398731 L-12.884160623254491,-1.031033321446178 L-12.914859920977715,-1.13963791565823 L-12.940855196867199,-1.2484811736269392 L-12.962136982578256,-1.3575234510150822 L-12.978697526576198,-1.4667250309959379 L-12.990530796959709,-1.576046138719472 L-12.997632483657862,-1.6854469557996754 L-12.999999999999998,-1.7948876348177127 " />
			<path d="M-12.999999999999998,-1.794887634817738 L-12.997458923101599,-1.908268493164945 L-12.989836685802064,-2.0216050269767876 L-12.977136267900026,-2.1348529290459104 L-12.959362634432182,-2.247967926814199 L-12.936522733732287,-2.3609057996804705 L-12.908625494714807,-2.4736223962878485 L-12.875681823384294,-2.586073651784071 L-12.837704598571856,-2.6982156050479755 L-12.794708666900354,-2.810004415875445 L-12.746710836980357,-2.9213963821180666 L-12.693729872839066,-3.032347956767826 L-12.635786486584792,-3.1428157649811554 L-12.572903330309876,-3.252756621035675 L-12.505104987235196,-3.362127545213 L-12.43241796209973,-3.4708857806010087 L-12.354870670798922,-3.5789888098090152 L-12.272493429275917,-3.6863943715893033 L-12.185318441670006,-3.793060477358517 L-12.0933797877269,-3.898945427612471 L-11.99671340947577,-4.004007828227936 L-11.895357097178254,-4.108206606645052 L-11.78935047455491,-4.211501027924028 L-11.678734983294948,-4.313850710669835 L-11.563553866855205,-4.415215642818725 L-11.443852153554777,-4.515556197280328 L-11.319676638971872,-4.614833147429275 L-11.191075867649793,-4.713007682440245 L-11.058100114119172,-4.810041422460482 L-10.920801363243909,-4.905896433613811 L-10.77923328989847,-5.000535242830319 L-10.633451237984508,-5.093920852495884 L-10.483512198794992,-5.186016754915833 L-10.329474788734332,-5.276786946587079 L-10.171399226403171,-5.366195942273144 L-10.009347309056837,-5.4542087888765725 L-9.843382388446644,-5.5407910791033235 L-9.673569346053467,-5.625908964913782 L-9.499974567723317,-5.709529170755134 L-9.322665917714797,-5.7916190065699515 L-9.141712712168584,-5.872146380575866 L-8.95718569200934,-5.951079811811375 L-8.769156995290619,-6.028388442442839 L-8.577700128993564,-6.104042049827904 L-8.382889940290477,-6.178011058330567 L-8.184802587284453,-6.250266550883334 L-7.983515509236505,-6.320780280291913 L-7.779107396291859,-6.389524680278023 L-7.571658158717232,-6.456472876256017 L-7.361248895661114,-6.521598695839098 L-7.147961863449282,-6.584876679071016 L-6.931880443427937,-6.64628208837925 L-6.713089109367012,-6.705790918245797 L-6.49167339443644,-6.76337990459176 L-6.2677198577682445,-6.819026533872093 L-6.041316050617555,-6.87270905187693 L-5.812550482135764,-6.924406472236059 L-5.581512584769216,-6.974098584623241 L-5.348292679296931,-7.021765962657116 L-5.112981939521071,-7.067389971495667 L-4.8756723566239115,-7.110952775121219 L-4.636456703205278,-7.15243734331317 L-4.3954284970145,-7.191827458305692 L-4.152681964391055,-7.229107721127828 L-3.9083120034282204,-7.264263557623479 L-3.6624141468740548,-7.297281224148961 L-3.415084524784341,-7.3281478129458675 L-3.16641982694201,-7.356851257187162 L-2.9165172650576987,-7.383380335694529 L-2.665474534766307,-7.407724677325115 L-2.413389777434367,-7.429874765025978 L-2.1603615417931543,-7.449821939554636 L-1.9064887454125505,-7.467558402864256 L-1.6518706360307125,-7.483077221152199 L-1.3966067527546648,-7.496372327570673 L-1.1407968871469905,-7.507438524598481 L-0.8845410442138246,-7.516271486072911 L-0.6279394033094069,-7.522867758880987 L-0.37109227897247477,-7.527224764309412 L-0.11410008170980857,-7.529340799052668 L0.14293672125774048,-7.52921503587891 L0.399917645271394,-7.5268475239533545 L0.6567422275174073,-7.5222391888190545 L0.9133100663014903,-7.515391832035081 L1.1695208602993339,-7.506308130472222 L1.4252744477679002,-7.494991635266511 L1.6804708457021433,-7.481446770430951 L1.9350102889218563,-7.4656788311260245 L2.188793269073351,-7.447693981589623 L2.4417205735307825,-7.4274992527272365 L2.6936933241818024,-7.405102539363323 L2.944613016082446,-7.380512597154949 L3.1943815559661823,-7.353739039168895 L3.44290130059199,-7.324792332123575 L3.690075094916506,-7.2936837922972275 L3.935806310075321,-7.260425581103992 L4.179998881158582,-7.225030700339583 L4.422557344766112,-7.187512987098435 L4.663386876327391,-7.147887108364301 L4.902393327171788,-7.10616855527642 L5.139483261334564,-7.0623736370734775 L5.37456399208425,-7.0165194747177715 L5.607543618157126,-6.968623994202016 L5.83833105968464,-6.918705919541455 L6.066836093799696,-6.866784765453985 L6.292969389907933,-6.812880829731173 L6.516642544610165,-6.757015185303145 L6.7377681162623615,-6.699209672000431 L6.956259659159634,-6.639486888016027 L7.172031757330884,-6.577870181070959 L7.38500005793088,-6.514383639286858 L7.595081304216739,-6.449052081769056 L7.802193368095882,-6.38190104890395 L8.006255282232793,-6.312956792374355 L8.207187271701963,-6.242246264896813 L8.404910785174678,-6.169797109684842 L8.5993485256275,-6.095637649642228 L8.79042448056036,-6.019796876290621 L8.9780639517125,-5.94230443843573 L9.162193584264633,-5.863190630576578 L9.3427413955159,-5.7824863810623155 L9.519636803024415,-5.700223240001258 L9.692810652200423,-5.6164333669268425 L9.86219524334122,-5.531149518225345 L10.02772435809735,-5.444405034330264 L10.18933328535965,-5.35623382668838 L10.346958846557103,-5.266670364502596 L10.500539420355528,-5.175749661256709 L10.650014966747458,-5.083507261027469 " />
			<path d="M-10.32232219853991,1.3925436952008772 L-10.650014966747525,1.493731991391945 " />
			<path d="M-3.6455820463097295,-2.823033001473405 L-3.7138095245784646,-2.8697255817886127 L-3.7737656219566182,-2.918577572362588 L-3.8251010894042574,-2.9693044064614553 L-3.867516893737024,-3.0216105962385638 L-3.885300640099534,-3.0482610457549995 L-3.90076595951824,-3.075191453974713 L-3.9138903221085797,-3.1023625886664146 L-3.924654608292993,-3.1297348669083758 L-3.933043136654331,-3.1572684127528503 L-3.9390436867805536,-3.184923115317374 L-3.94264751706743,-3.212658687218316 L-3.943849377453313,-3.240434723261554 " />
			<path d="M-3.943849377453313,-3.240434723261557 L-3.9418618801918477,-3.276149242182835 L-3.9359041764624383,-3.3117777216998094 L-3.925990618895202,-3.3472343296846376 L-3.912145090118644,-3.3824336480630515 L-3.8944009452243114,-3.417290878593982 L-3.872800931411458,-3.451722047155947 L-3.847397085005298,-3.485644206048067 L-3.818250606096937,-3.5189756338183393 L-3.7854317111069955,-3.5516360321377785 L-3.749019463628099,-3.5835467192461197 L-3.709101583953762,-3.6146308195030725 L-3.6657742377525135,-3.6448134485884722 L-3.619141804396378,-3.6740218939051665 L-3.56931662550183,-3.702185789750029 L-3.5164187342889965,-3.7292372868311046 L-3.4605755664111175,-3.7551112157224935 L-3.401921652950894,-3.779745243863207 L-3.340598296323329,-3.8030800257217683 L-3.2767532298658293,-3.8250593457647954 L-3.210540261935658,-3.845630253885143 L-3.0716539932162097,-3.882352118255083 L-2.925277040855712,-3.912891967203492 L-2.772819094923178,-3.936955685290218 L-2.6157484087799254,-3.9543115257555197 L-2.455577658997088,-3.964792342368048 L-2.2938493774533137,-3.9682971991344274 L-2.132121095909539,-3.964792342368048 L-1.9719503461267016,-3.9543115257555197 L-1.8148796599834496,-3.936955685290218 L-1.662421714050915,-3.912891967203492 L-1.5160447616904174,-3.882352118255083 L-1.3771584929709704,-3.8456302538851435 L-1.310945525040799,-3.8250593457647963 L-1.2471004585832992,-3.803080025721769 L-1.1857771019557342,-3.779745243863208 L-1.1271231884955102,-3.755111215722494 L-1.0712800206176303,-3.729237286831105 L-1.018382129404797,-3.7021857897500294 L-0.9685569505102489,-3.6740218939051665 L-0.9219245171541137,-3.6448134485884727 L-0.8785971709528646,-3.614630819503073 L-0.8386792912785279,-3.58354671924612 L-0.8022670437996322,-3.5516360321377793 L-0.7694481488096907,-3.51897563381834 L-0.7403016699013296,-3.4856442060480677 L-0.7148978234951693,-3.4517220471559487 L-0.6932978096823161,-3.4172908785939837 L-0.6755536647879834,-3.382433648063053 L-0.6617081360114248,-3.347234329684638 L-0.6517945784441885,-3.3117777216998103 L-0.6458368747147789,-3.276149242182836 L-0.6438493774533134,-3.2404347232615645 " />
			<path d="M-0.6438493774533134,-3.240434723261558 L-0.6451393365630511,-3.2116590542567556 L-0.6490071969292286,-3.1829283785081612 L-0.6554469108164338,-3.154287618921121 L-0.6644484091730394,-3.1257815578092587 L-0.675997617375037,-3.0974547668734393 L-0.690076477232936,-3.0693515375100473 L-0.7066629752273075,-3.041515811557544 L-0.7257311769288346,-3.013991112589588 L-0.7472512675490433,-2.9868204778621514 L-0.7711895985583115,-2.9600463910210326 L-0.8261675405063065,-2.9078546299383556 L-0.8903212860458798,-2.8577421271376715 L-0.9632497522216412,-2.8100221810952615 L-1.0444969973812395,-2.7649931322560795 L-1.13355507167807,-2.722936497838411 L-1.229867192724138,-2.6841152118156986 L-1.3328312265392035,-2.6487719810790074 L-1.4418034520336542,-2.6171277680572276 L-1.5561025854899273,-2.5893804092815405 L-1.675014039881816,-2.5657033785307317 L-1.7977943924028086,-2.54624470229006 L-1.9236760322729143,-2.531126034304119 L-2.0518719597663364,-2.5204418950095 L-2.1815807064569435,-2.5142590806022476 L-2.311991345920642,-2.512616245434563 L-2.442288563568228,-2.515523660351566 L-2.5716577539126235,-2.5229631484789725 L-2.6992901134028684,-2.534888198863142 L-2.82438769698498,-2.5512242572530166 L-2.946168406776547,-2.571869192206022 L-3.0638708816663516,-2.5966939336038806 L-3.176759257269728,-2.6255432795863904 L-3.2841277664808675,-2.6582368668583083 L-3.385305151859882,-2.6945702983030655 L-3.479658862268793,-2.7343164208535926 L-3.5665990075195153,-2.7772267456311224 L-3.6455820463097255,-2.8230330014734024 " />
			<path d="M10.322322198539908,-4.982318964836358 L10.322322198539906,-73.18804908791049 " />
			<path d="M10.322322198539906,-73.18804908791049 L10.322322198539906,-74.98293672272823 " />
			<path d="M10.322322198539906,-74.98293672272823 L11.469246887266562,-74.26016317850632 " />
			<path d="M11.469246887266564,-2.4646577857967094 L11.469246887266562,-74.26016317850632 " />
			<path d="M-9.994629430332292,4.163175614718194 L-9.994629430332294,-67.63232977799142 " />
			<path d="M-9.175397509813253,-67.8853005184691 L-9.994629430332294,-67.63232977799143 " />
			<path d="M-11.387323695214661,4.054759583084909 L-11.387323695214663,-67.74074580962471 " />
			<path d="M-11.387323695214663,-67.7407458096247 L-9.994629430332294,-67.63232977799142 " />
			<path d="M-11.960786039577991,-68.10213258173566 L-11.387323695214663,-67.7407458096247 " />
			<path d="M-11.960786039577991,3.6933728109739548 L-11.960786039577993,-68.10213258173566 " />
			<path d="M-11.960786039577995,-68.10213258173566 L-12.11838976266471,-68.20349724837018 L-12.27157956485859,-68.30617024392512 L-12.420299649334984,-68.41011417147823 L-12.564495847289225,-68.51529117119144 L-12.704115637666675,-68.62166293410083 L-12.839108166292654,-68.72919071606994 L-12.969424264395226,-68.83783535190166 L-13.095016466514101,-68.94755726960358 L-13.21583902778913,-69.05831650480135 L-13.331847940622108,-69.17007271529506 L-13.443000950705814,-69.28278519575323 L-13.54925757241442,-69.39641289253902 L-13.65057910354972,-69.51091441866333 L-13.746928639437751,-69.62624806885935 L-13.8382710863707,-69.74237183477301 L-13.924573174389202,-69.85924342026372 L-14.005803469400382,-69.97682025681021 L-14.081932384627168,-70.09505951901522 L-14.15293219138481,-70.21391814020406 L-14.218777029180568,-70.33335282811088 L-14.27944291513298,-70.45332008064713 L-14.334907752707212,-70.57377620174653 L-14.385151339763363,-70.6946773172806 L-14.430155375914746,-70.81597939103904 L-14.46990346919351,-70.93763824076925 L-14.504381142021131,-71.05960955426893 L-14.53357583648163,-71.1818489055261 L-14.557476918895585,-71.30431177090047 L-14.576075683693274,-71.42695354534051 L-14.589365356585525,-71.54972955863002 L-14.597341097031142,-71.67259509165856 L-14.600000000000003,-71.79550539270959 " />
			<path d="M12.288478807785605,-2.7176285262743773 L12.288478807785603,-74.513133918984 " />
			<path d="M12.534248383941316,-75.12749143157261 L12.288478807785603,-74.51313391898398 " />
			<path d="M12.288478807785603,-74.513133918984 L11.469246887266564,-74.26016317850632 " />
			<path d="M-10.650014966747525,1.493731991391945 L-10.650014966747527,-66.7119981316822 " />
			<path d="M-10.322322198539911,-66.81318642787325 L-10.650014966747527,-66.71199813168218 " />
			<path d="M10.322322198539908,-73.18804908791049 L-10.322322198539911,-66.81318642787325 " />
			<path d="M-1.9539925233402755e-14,-71.79550539270961 L-10.32232219853991,-68.608074062691 " />
			<path d="M10.322322198539908,-74.98293672272823 L-1.9539925233402755e-14,-71.79550539270961 " />
			<path d="M-5.570777059529476,-72.22916951924276 L-5.454276002414904,-72.15945874282491 L-5.33016120074012,-72.09235362045912 L-5.198731657933532,-72.02801581426289 L-5.0603039992756305,-71.96660031964664 L-4.915211709120953,-71.9082550919163 L-4.763804327505065,-71.85312068983589 L-4.606446608072,-71.80132993700923 L-4.44351763935078,-71.75300760189623 L-4.275409931497947,-71.70827009723467 L-4.102528470706216,-71.66722519959188 L-3.9252897435572596,-71.62997178972134 L-3.74412073366906,-71.59659961435048 L-3.5594578930549683,-71.5671890699728 L-3.371746090672579,-71.54181100916577 L-3.181437540695443,-71.52052656990072 L-2.9889907130895157,-71.50338702825617 L-2.794869229118851,-71.49043367488916 L-2.5995407444413674,-71.48169771556255 L-2.4034758224854085,-71.47720019596751 L-2.2071468008212247,-71.4769519510227 L-2.0110266532583965,-71.48095357877193 L-1.8155878504104987,-71.48919543894345 L-1.6213012214720095,-71.50165767617422 L-1.42863481994954,-71.51831026784318 L-1.2380527960799423,-71.53911309639838 L-1.0500142786517312,-71.56401604600376 L-0.8649722689236208,-71.59295912327245 L-0.6833725493048115,-71.6258726017962 L-0.505652609426122,-71.66267719012237 L-0.3322405921891485,-71.70328422277399 L-0.16355426233251347,-71.74759587385263 L-3.3306690738754696e-14,-71.7955053927096 " />
			<path d="M-1.9095836023552692e-14,-71.79550539270961 L0.1923838023480382,-71.85878797655673 L0.37581853876742244,-71.92704594898888 L0.4639723507588669,-71.96296460329157 L0.5496439455454771,-72.00003361901439 L0.6327562131732751,-72.03821963165532 L0.7132343472475853,-72.07748827134317 L0.7910059122636164,-72.11780419377268 L0.8660009088030765,-72.15913111201667 L0.9381518365381565,-72.20143182918653 L1.0073937549861802,-72.24466827191198 L1.0736643419602179,-72.2888015246094 L1.1369039496630666,-72.33379186450847 L1.197055658374115,-72.37959879740514 L1.254065327680757,-72.42618109410908 L1.3078816452082473,-72.4734968275526 L1.3584561728041482,-72.52150341052766 L1.4057433901357856,-72.57015763401718 L1.4497007356614806,-72.61941570608586 L1.490288644938678,-72.66923329129582 L1.527470586234493,-72.7195655506113 L1.5612130934066268,-72.77036718175667 L1.5914857960250481,-72.82159245999144 L1.618261446707336,-72.87319527926542 L1.6415159456430795,-72.92512919371721 L1.6612283622852622,-72.97734745947838 L1.6773809541891,-73.02980307674605 L1.6899591829813838,-73.08244883208565 L1.6989517274459542,-73.1352373409261 L1.704350493713525,-73.18812109020901 L1.7061506225466845,-73.24105248115343 " />
			<path d="M1.7061506225466845,-73.24105248115343 L1.7049458973315015,-73.28435584928349 L1.701332447367374,-73.32763313308381 L1.6953124492614453,-73.37085826393685 L1.6868895292354718,-73.4140052046401 L1.6760687609415243,-73.45704796508984 L1.662856662405808,-73.49996061793665 L1.6472611921024494,-73.54271731420307 L1.6292917441596062,-73.58529229885403 L1.6089591427007988,-73.62765992631076 L1.5862756353248604,-73.6697946758987 L1.5612548857284443,-73.71167116722025 L1.5339119654755198,-73.75326417544287 L1.5042633449188303,-73.79454864649367 L1.4723268832787668,-73.83549971215103 L1.401668752591831,-73.9163031734123 L1.3221077950404574,-73.99547989661093 L1.2338356799401038,-74.0728391380857 L1.1370650625477712,-74.14819453264802 L1.032029071756864,-74.22136454255201 L0.9189807484692634,-74.2921728948349 L0.7981924359976307,-74.36044900597398 L0.6699551239665182,-74.42602839283718 L0.5345777472928726,-74.48875306893753 L0.39238644193475647,-74.54847192503622 L0.2437237592012651,-74.60504109317819 L0.08894784051641702,-74.65832429328249 L-0.07156844537490992,-74.70819316145304 L-0.2374384006804342,-74.75452755921839 L-0.4082624301493303,-74.79721586295592 L-0.5836290037321921,-74.83615523280288 L-0.7631156479929608,-74.8712518604066 L-0.9462899638844391,-74.90242119491711 L-1.1327106684354693,-74.92958814667746 L-1.3219286578402625,-74.9526872681213 L-1.5134880893888045,-74.97166291144183 L-1.7069274796318699,-74.98646936265222 L-1.9017808161350738,-74.99707095171462 L-2.0975786801436436,-75.0034421384724 L-2.2938493774533186,-75.00556757417857 L-2.4901200747629932,-75.00344213847238 L-2.685917938771563,-74.99707095171462 L-2.8807712752747667,-74.98646936265222 L-3.0742106655178323,-74.97166291144183 L-3.2657700970663743,-74.9526872681213 L-3.4549880864711673,-74.92958814667746 L-3.6414087910221973,-74.90242119491711 L-3.8245831069136758,-74.8712518604066 L-4.004069751174444,-74.83615523280287 L-4.179436324757306,-74.79721586295592 L-4.350260354226202,-74.75452755921839 L-4.516130309531726,-74.70819316145304 L-4.676646595423053,-74.65832429328249 L-4.831422514107901,-74.60504109317819 L-4.980085196841392,-74.54847192503621 L-5.122276502199508,-74.48875306893751 L-5.257653878873153,-74.42602839283718 L-5.385891190904264,-74.36044900597398 L-5.506679503375896,-74.2921728948349 L-5.619727826663498,-74.22136454255201 L-5.7247638174544075,-74.148194532648 L-5.821534434846738,-74.0728391380857 L-5.909806549947091,-73.99547989661093 L-5.989367507498464,-73.91630317341229 L-6.0600256381854,-73.83549971215103 L-6.091962099825463,-73.79454864649367 L-6.121610720382152,-73.75326417544287 L-6.148953640635076,-73.71167116722025 L-6.173974390231492,-73.6697946758987 L-6.19665789760743,-73.62765992631076 L-6.216990499066238,-73.58529229885403 L-6.234959947009081,-73.54271731420307 L-6.250555417312439,-73.49996061793665 L-6.263767515848155,-73.45704796508984 L-6.274588284142103,-73.4140052046401 L-6.283011204168076,-73.37085826393685 L-6.289031202274005,-73.32763313308381 L-6.292644652238133,-73.28435584928349 L-6.2938493774533155,-73.24105248115345 " />
			<path d="M-6.2938493774533155,-73.24105248115343 L-6.290935776517841,-73.17371663620011 L-6.2821992182466255,-73.10647888613723 L-6.267652430061844,-73.03943718295051 L-6.247316603731327,-72.97268919302451 L-6.221221364496386,-72.90633215486217 L-6.189404727913744,-72.84046273742774 L-6.1519130444744565,-72.77517689931935 L-6.108800932080493,-72.71056974897648 L-6.060131196477355,-72.64673540612597 L-6.005974739758635,-72.58376686466833 L-5.946410457075809,-72.52175585720424 L-5.881525121703753,-72.46079272139835 L-5.811413258629383,-72.40096626837544 L-5.7361770068476226,-72.34236365334023 L-5.655925970565256,-72.28507024860974 L-5.57077705952948,-72.22916951924276 " />
			<path d="M10.650014966747523,-73.28923738410155 L10.322322198539908,-73.18804908791049 " />
			<path d="M10.650014966747523,-5.083507261027426 L10.650014966747522,-73.28923738410155 " />
			<path d="M-10.650014966747529,-66.7119981316822 L-10.79034704894803,-66.80225434169922 L-10.926748927613811,-66.89367550212486 L-11.059170920640739,-66.98622831432968 L-11.1875647955315,-67.07987906749898 L-11.311883786963477,-67.17459365091145 L-11.432082613822224,-67.2703375663634 L-11.548117495694378,-67.36707594073411 L-11.659946168813926,-67.46477353868788 L-11.767527901456074,-67.5633947755078 L-11.870823508773109,-67.662903730057 L-11.969795367066821,-67.76326415786222 L-12.064407427492291,-67.86443950431531 L-12.154625229188106,-67.96639291798765 L-12.240415911828135,-68.06908726405261 L-12.321748227590348,-68.17248513781134 L-12.398592552538329,-68.27654887831677 L-12.470920897411299,-68.38124058209104 L-12.53870691781871,-68.48652211693111 L-12.601925923835788,-68.59235513579789 L-12.660554888996396,-68.6987010907834 L-12.714572458680049,-68.8055212471513 L-12.763958957889981,-68.9127766974453 L-12.80869639841943,-69.02042837566056 L-12.84876848540354,-69.12843707147286 L-12.884160623254495,-69.2367634445203 L-12.914859920977719,-69.34536803873236 L-12.940855196867203,-69.45421129670108 L-12.96213698257826,-69.56325357408922 L-12.978697526576202,-69.67245515407008 L-12.990530796959712,-69.78177626179361 L-12.997632483657865,-69.89117707887381 L-13.000000000000002,-70.00061775789185 " />
			<path d="M-13.000000000000002,-70.00061775789187 L-12.997458923101602,-70.11399861623907 L-12.989836685802068,-70.22733515005092 L-12.977136267900029,-70.34058305212004 L-12.959362634432186,-70.45369804988833 L-12.936522733732291,-70.5666359227546 L-12.90862549471481,-70.67935251936198 L-12.875681823384298,-70.79180377485821 L-12.83770459857186,-70.90394572812211 L-12.794708666900357,-71.01573453894957 L-12.74671083698036,-71.1271265051922 L-12.69372987283907,-71.23807807984196 L-12.635786486584795,-71.34854588805528 L-12.57290333030988,-71.4584867441098 L-12.5051049872352,-71.56785766828713 L-12.432417962099734,-71.67661590367514 L-12.354870670798926,-71.78471893288315 L-12.27249342927592,-71.89212449466343 L-12.18531844167001,-71.99879060043266 L-12.093379787726903,-72.10467555068661 L-11.996713409475774,-72.20973795130207 L-11.895357097178257,-72.31393672971919 L-11.789350474554913,-72.41723115099816 L-11.678734983294952,-72.51958083374397 L-11.563553866855209,-72.62094576589286 L-11.443852153554781,-72.72128632035447 L-11.319676638971876,-72.82056327050341 L-11.191075867649797,-72.91873780551438 L-11.058100114119176,-73.01577154553462 L-10.920801363243912,-73.11162655668795 L-10.779233289898473,-73.20626536590446 L-10.633451237984511,-73.29965097557002 L-10.483512198794996,-73.39174687798997 L-10.329474788734336,-73.48251706966121 L-10.171399226403175,-73.57192606534728 L-10.00934730905684,-73.6599389119507 L-9.843382388446647,-73.74652120217746 L-9.67356934605347,-73.83163908798791 L-9.49997456772332,-73.91525929382927 L-9.3226659177148,-73.99734912964409 L-9.141712712168587,-74.07787650365 L-8.957185692009343,-74.1568099348855 L-8.769156995290622,-74.23411856551698 L-8.577700128993568,-74.30977217290204 L-8.38288994029048,-74.3837411814047 L-8.184802587284457,-74.45599667395747 L-7.983515509236507,-74.52651040336605 L-7.77910739629186,-74.59525480335216 L-7.571658158717233,-74.66220299933015 L-7.361248895661116,-74.72732881891324 L-7.147961863449284,-74.79060680214515 L-6.931880443427938,-74.85201221145338 L-6.713089109367014,-74.91152104131993 L-6.491673394436442,-74.96911002766589 L-6.267719857768246,-75.02475665694622 L-6.0413160506175565,-75.07843917495106 L-5.812550482135766,-75.13013659531019 L-5.581512584769218,-75.17982870769737 L-5.348292679296933,-75.22749608573125 L-5.112981939521073,-75.2731200945698 L-4.875672356623913,-75.31668289819535 L-4.63645670320528,-75.3581674663873 L-4.3954284970145014,-75.39755758137983 L-4.152681964391057,-75.43483784420197 L-3.9083120034282226,-75.46999368069761 L-3.662414146874057,-75.5030113472231 L-3.4150845247843433,-75.53387793602 L-3.166419826942012,-75.56258138026129 L-2.916517265057701,-75.58911045876866 L-2.665474534766309,-75.61345480039925 L-2.4133897774343693,-75.63560488810012 L-2.1603615417931565,-75.65555206262877 L-1.9064887454125525,-75.67328852593839 L-1.6518706360307145,-75.68880734422633 L-1.3966067527546668,-75.7021024506448 L-1.1407968871469925,-75.71316864767262 L-0.8845410442138267,-75.72200160914704 L-0.627939403309409,-75.72859788195512 L-0.3710922789724769,-75.73295488738354 L-0.11410008170981067,-75.7350709221268 L0.14293672125773838,-75.73494515895304 L0.3999176452713919,-75.73257764702748 L0.6567422275174052,-75.72796931189319 L0.9133100663014881,-75.72112195510921 L1.1695208602993319,-75.71203825354635 L1.4252744477678982,-75.70072175834065 L1.6804708457021413,-75.68717689350508 L1.9350102889218543,-75.67140895420016 L2.188793269073349,-75.65342410466376 L2.4417205735307803,-75.63322937580136 L2.6936933241818,-75.61083266243746 L2.9446130160824437,-75.58624272022908 L3.19438155596618,-75.55946916224303 L3.4429013005919877,-75.53052245519771 L3.6900750949165038,-75.49941391537136 L3.9358063100753187,-75.46615570417812 L4.17999888115858,-75.43076082341372 L4.42255734476611,-75.39324311017256 L4.663386876327389,-75.35361723143843 L4.9023933271717866,-75.31189867835056 L5.139483261334562,-75.26810376014761 L5.374563992084248,-75.2222495977919 L5.607543618157124,-75.17435411727615 L5.838331059684638,-75.12443604261559 L6.066836093799695,-75.07251488852812 L6.292969389907931,-75.0186109528053 L6.516642544610163,-74.96274530837728 L6.73776811626236,-74.90493979507457 L6.956259659159632,-74.84521701109016 L7.172031757330882,-74.7836003041451 L7.3850000579308785,-74.720113762361 L7.5950813042167375,-74.65478220484319 L7.80219336809588,-74.58763117197809 L8.00625528223279,-74.51868691544848 L8.20718727170196,-74.44797638797095 L8.404910785174675,-74.37552723275897 L8.599348525627496,-74.30136777271636 L8.790424480560356,-74.22552699936476 L8.978063951712496,-74.14803456150986 L9.16219358426463,-74.06892075365072 L9.342741395515896,-73.98821650413645 L9.519636803024412,-73.9059533630754 L9.69281065220042,-73.82216349000097 L9.862195243341217,-73.73687964129948 L10.027724358097347,-73.65013515740439 L10.189333285359647,-73.56196394976251 L10.346958846557099,-73.47240048757673 L10.500539420355524,-73.38147978433085 L10.650014966747454,-73.2892373841016 " />
			<path d="M-3.645582046309732,-71.02876312454754 L-3.713809524578467,-71.07545570486275 L-3.7737656219566205,-71.12430769543673 L-3.825101089404259,-71.1750345295356 L-3.867516893737026,-71.22734071931269 L-3.885300640099536,-71.25399116882913 L-3.900765959518242,-71.28092157704884 L-3.913890322108582,-71.30809271174054 L-3.924654608292995,-71.33546498998251 L-3.9330431366543332,-71.36299853582699 L-3.939043686780556,-71.39065323839151 L-3.9426475170674324,-71.41838881029246 L-3.9438493774533154,-71.44616484633569 " />
			<path d="M-3.9438493774533154,-71.44616484633569 L-3.94186188019185,-71.48187936525697 L-3.93590417646244,-71.51750784477395 L-3.925990618895204,-71.55296445275877 L-3.912145090118646,-71.58816377113719 L-3.894400945224313,-71.62302100166812 L-3.8728009314114606,-71.65745217023009 L-3.8473970850052996,-71.6913743291222 L-3.818250606096939,-71.72470575689248 L-3.7854317111069973,-71.75736615521191 L-3.749019463628102,-71.78927684232025 L-3.7091015839537644,-71.82036094257721 L-3.6657742377525153,-71.8505435716626 L-3.61914180439638,-71.8797520169793 L-3.5693166255018323,-71.90791591282417 L-3.516418734288999,-71.93496740990524 L-3.4605755664111193,-71.96084133879663 L-3.401921652950896,-71.98547536693734 L-3.340598296323331,-72.0088101487959 L-3.2767532298658315,-72.03078946883893 L-3.2105402619356602,-72.05136037695928 L-3.071653993216212,-72.08808224132922 L-2.9252770408557147,-72.11862209027763 L-2.77281909492318,-72.14268580836435 L-2.615748408779928,-72.16004164882965 L-2.45557765899709,-72.17052246544218 L-2.293849377453316,-72.17402732220856 L-2.1321210959095414,-72.17052246544218 L-1.9719503461267038,-72.16004164882965 L-1.8148796599834518,-72.14268580836435 L-1.6624217140509172,-72.11862209027763 L-1.5160447616904196,-72.08808224132922 L-1.3771584929709726,-72.05136037695928 L-1.3109455250408013,-72.03078946883893 L-1.2471004585833014,-72.0088101487959 L-1.1857771019557364,-71.98547536693734 L-1.1271231884955124,-71.96084133879663 L-1.0712800206176325,-71.93496740990524 L-1.0183821294047992,-71.90791591282417 L-0.9685569505102511,-71.8797520169793 L-0.9219245171541159,-71.85054357166261 L-0.8785971709528668,-71.82036094257721 L-0.8386792912785301,-71.78927684232025 L-0.8022670437996344,-71.75736615521191 L-0.7694481488096929,-71.72470575689248 L-0.7403016699013318,-71.6913743291222 L-0.7148978234951715,-71.65745217023009 L-0.6932978096823184,-71.62302100166812 L-0.6755536647879856,-71.58816377113719 L-0.661708136011427,-71.55296445275877 L-0.6517945784441908,-71.51750784477395 L-0.6458368747147811,-71.48187936525697 L-0.6438493774533156,-71.44616484633569 " />
			<path d="M-0.6438493774533156,-71.44616484633569 L-0.6451393365630533,-71.41738917733089 L-0.6490071969292308,-71.3886585015823 L-0.655446910816436,-71.36001774199525 L-0.6644484091730416,-71.3315116808834 L-0.6759976173750393,-71.30318488994757 L-0.6900764772329382,-71.27508166058418 L-0.7066629752273097,-71.24724593463168 L-0.7257311769288368,-71.21972123566373 L-0.7472512675490455,-71.19255060093629 L-0.7711895985583137,-71.16577651409517 L-0.8261675405063087,-71.11358475301249 L-0.890321286045882,-71.0634722502118 L-0.9632497522216434,-71.0157523041694 L-1.0444969973812417,-70.97072325533021 L-1.1335550716780722,-70.92866662091254 L-1.2298671927241402,-70.88984533488983 L-1.3328312265392057,-70.85450210415314 L-1.4418034520336565,-70.82285789113136 L-1.5561025854899295,-70.79511053235568 L-1.6750140398818183,-70.77143350160486 L-1.7977943924028108,-70.75197482536419 L-1.9236760322729165,-70.73685615737826 L-2.0518719597663386,-70.72617201808363 L-2.1815807064569457,-70.71998920367638 L-2.311991345920644,-70.71834636850869 L-2.4422885635682303,-70.7212537834257 L-2.5716577539126257,-70.72869327155311 L-2.6992901134028706,-70.74061832193728 L-2.8243876969849824,-70.75695438032714 L-2.946168406776549,-70.77759931528016 L-3.063870881666354,-70.802424056678 L-3.17675925726973,-70.83127340266053 L-3.2841277664808697,-70.86396698993244 L-3.3853051518598836,-70.9003004213772 L-3.479658862268795,-70.94004654392772 L-3.5665990075195175,-70.98295686870526 L-3.6455820463097277,-71.02876312454754 " />
			<path d="M-5.570777059529476,-75.81894478887824 L-5.4775290225478095,-75.76258691088589 L-5.379303026098654,-75.70789932016967 L-5.276252655053447,-75.65496752552457 L-5.168539037612055,-75.60387429040597 L-5.056330593364856,-75.55469950352185 L-4.939802769954088,-75.50752005391985 L-4.819137768746231,-75.46240971076459 L-4.694524259944357,-75.41943900799316 L-4.566157087585893,-75.37867513402918 L-4.434236964887049,-75.3401818267279 L-4.298970160410289,-75.30401927371648 L-4.160568175545531,-75.27024401828545 L-4.019247413809355,-75.23890887097836 L-3.875228842479337,-75.21006282701792 L-3.7287376470925153,-75.18375098969766 L-3.580002879348266,-75.16001449985912 L-3.4292570989660893,-75.13889047156445 L-3.276736010058298,-75.12041193406549 L-3.122678092586182,-75.1046077801595 L-2.967324229475886,-75.09150272101294 L-2.810917329977049,-75.08111724752331 L-2.6537019498531085,-75.07346759827985 L-2.495923908997132,-75.06856573417312 L-2.3378299070710806,-75.06641931969317 L-2.179667137769476,-75.06703171094532 L-2.0216829023106,-75.07040195040271 L-1.8641242227595731,-75.07652476840339 L-1.707237455787916,-75.08539059138998 L-1.551267907473512,-75.09698555687868 L-1.396459449743257,-75.11129153513451 L-1.2430541390581362,-75.12828615751872 L-1.09129183793694,-75.14794285146407 L-0.9414098399103898,-75.17023088202339 L-0.7936424984921093,-75.19511539992631 L-0.6482208607465658,-75.2225574960691 L-0.5053723060269255,-75.2525142623525 L-0.36532019044770236,-75.2849388587722 L-0.22828349764808165,-75.3197805866572 L-0.0944764963919984,-75.35698496794176 L0.03589159445967827,-75.39649383034637 L0.16261693308099323,-75.43824539833533 L0.28550137340529247,-75.48217438970805 L0.4043527749437992,-75.5282121176735 L0.5189853032139418,-75.57628659824795 L0.6292197203077055,-75.62632266280818 L0.7348836651456518,-75.67824207562411 L0.8358119229784293,-75.73196365618725 L0.9318466837143755,-75.78740340614334 L1.0228377886692925,-75.84447464063119 L1.1086429653525856,-75.90308812382192 L1.189128049922647,-75.9631522084469 L1.2641671969636716,-76.0245729790963 L1.3336430762558877,-76.0872543990639 L1.3974470562315378,-76.15109846050885 L1.4554793738297644,-76.21600533769944 L1.5076492904848156,-76.2818735430993 L1.5538752340036694,-76.34860008605192 L1.5940849261112362,-76.41608063381555 L1.628215495463718,-76.4842096746965 L1.65621357595341,-76.55288068302576 L1.6780353901512415,-76.62198628572119 L1.6936468177565875,-76.69141843017462 L1.7030234489473202,-76.76106855320151 L1.7061506225466845,-76.83082775078891 " />
			<path d="M1.7061506225466845,-76.83082775078891 L1.7044940243874374,-76.88160556433277 L1.6995256020684262,-76.9323413186604 L1.6912494709292853,-76.98299298939321 L1.6796724860818197,-77.03351862179892 L1.664804236731924,-77.08387636554274 L1.6466570382368495,-77.13402450935185 L1.6252459219044084,-77.18392151556489 L1.6005886225425519,-77.23352605453755 L1.572705563769647,-77.28279703887584 L1.5416198410976136,-77.3316936574688 L1.5073572028019293,-77.38017540929225 L1.4699460285943609,-77.42820213695575 L1.429417306116071,-77.475734059965 L1.3858046052705877,-77.52273180767193 L1.3391440504178806,-77.56915645188535 L1.2894742904525893,-77.6149695391152 L1.236836466791178,-77.66013312242346 L1.1812741792945385,-77.70460979285569 L1.1228334501542667,-77.74836271042668 L1.0615626857725218,-77.79135563463507 L0.9975126366670484,-77.83355295448133 L0.9307363554345716,-77.87491971796425 L0.8612891528073758,-77.91542166103171 L0.7892285518394804,-77.95502523596157 L0.6375080210355737,-78.03140683827844 L0.4760773388346258,-78.10381151007513 L0.3054712460243363,-78.17199941013493 L0.12625487703402571,-78.2357446653407 " />
			<path d="M-5.756414163772761,-77.71425848231374 L-5.820176068253684,-77.66373448938236 L-5.880150810753452,-77.61231598127675 L-5.936273980318529,-77.5600581798286 L-5.988485302461418,-77.50701720824377 L-6.036728703893527,-77.45325003082782 L-6.080952372746081,-77.39881439180809 L-6.121108814214425,-77.34376875331829 L-6.15715490156591,-77.28817223261203 L-6.189051922456628,-77.2320845385728 L-6.216765620507226,-77.17556590758853 L-6.240266232093171,-77.11867703885963 L-6.259528518309922,-77.06147902920995 L-6.2745317920787045,-77.00403330747086 L-6.285259940363778,-76.94640156850856 L-6.291701441477311,-76.88864570696576 L-6.2938493774533155,-76.83082775078893 " />
			<path d="M-6.2938493774533155,-76.83082775078891 L-6.290935776517841,-76.7634919058356 L-6.2821992182466255,-76.6962541557727 L-6.267652430061844,-76.62921245258599 L-6.247316603731327,-76.56246446265999 L-6.221221364496386,-76.49610742449765 L-6.189404727913744,-76.43023800706322 L-6.1519130444744565,-76.36495216895483 L-6.108800932080493,-76.30034501861196 L-6.060131196477355,-76.23651067576145 L-6.005974739758635,-76.17354213430382 L-5.946410457075809,-76.11153112683972 L-5.881525121703753,-76.05056799103383 L-5.811413258629383,-75.99074153801092 L-5.7361770068476226,-75.93213892297571 L-5.655925970565256,-75.87484551824522 L-5.57077705952948,-75.81894478887824 " />
			<path d="M-3.645582046309732,-76.41342602900076 L-3.713809524578467,-76.46011860931597 L-3.7737656219566205,-76.50897059988995 L-3.825101089404259,-76.55969743398882 L-3.867516893737026,-76.61200362376591 L-3.885300640099536,-76.63865407328235 L-3.900765959518242,-76.66558448150207 L-3.913890322108582,-76.69275561619376 L-3.924654608292995,-76.72012789443573 L-3.9330431366543332,-76.74766144028021 L-3.939043686780556,-76.77531614284473 L-3.9426475170674324,-76.80305171474568 L-3.9438493774533154,-76.83082775078891 " />
			<path d="M-3.9438493774533154,-76.83082775078891 L-3.94186188019185,-76.8665422697102 L-3.93590417646244,-76.90217074922717 L-3.925990618895204,-76.937627357212 L-3.912145090118646,-76.97282667559041 L-3.894400945224313,-77.00768390612134 L-3.8728009314114606,-77.04211507468331 L-3.8473970850052996,-77.07603723357542 L-3.818250606096939,-77.1093686613457 L-3.7854317111069973,-77.14202905966513 L-3.749019463628102,-77.17393974677347 L-3.7091015839537644,-77.20502384703043 L-3.6657742377525153,-77.23520647611582 L-3.61914180439638,-77.26441492143252 L-3.5693166255018323,-77.29257881727739 L-3.516418734288999,-77.31963031435846 L-3.4605755664111193,-77.34550424324985 L-3.401921652950896,-77.37013827139056 L-3.340598296323331,-77.39347305324912 L-3.2767532298658315,-77.41545237329215 L-3.2105402619356602,-77.4360232814125 L-3.071653993216212,-77.47274514578244 L-2.9252770408557147,-77.50328499473085 L-2.77281909492318,-77.52734871281757 L-2.615748408779928,-77.54470455328287 L-2.45557765899709,-77.5551853698954 L-2.293849377453316,-77.55869022666178 L-2.1321210959095414,-77.5551853698954 L-1.9719503461267038,-77.54470455328287 L-1.8148796599834518,-77.52734871281757 L-1.6624217140509172,-77.50328499473085 L-1.5160447616904196,-77.47274514578244 L-1.3771584929709726,-77.4360232814125 L-1.3109455250408013,-77.41545237329215 L-1.2471004585833014,-77.39347305324912 L-1.1857771019557364,-77.37013827139056 L-1.1271231884955124,-77.34550424324985 L-1.0712800206176325,-77.31963031435846 L-1.0183821294047992,-77.29257881727739 L-0.9685569505102511,-77.26441492143252 L-0.9219245171541159,-77.23520647611583 L-0.8785971709528668,-77.20502384703043 L-0.8386792912785301,-77.17393974677347 L-0.8022670437996344,-77.14202905966513 L-0.7694481488096929,-77.1093686613457 L-0.7403016699013318,-77.07603723357542 L-0.7148978234951715,-77.04211507468331 L-0.6932978096823184,-77.00768390612134 L-0.6755536647879856,-76.97282667559041 L-0.661708136011427,-76.937627357212 L-0.6517945784441908,-76.90217074922717 L-0.6458368747147811,-76.8665422697102 L-0.6438493774533156,-76.83082775078891 " />
			<path d="M-0.6438493774533156,-76.83082775078891 L-0.6451393365630533,-76.80205208178411 L-0.6490071969292308,-76.77332140603552 L-0.655446910816436,-76.74468064644847 L-0.6644484091730416,-76.71617458533662 L-0.6759976173750393,-76.6878477944008 L-0.6900764772329382,-76.6597445650374 L-0.7066629752273097,-76.6319088390849 L-0.7257311769288368,-76.60438414011695 L-0.7472512675490455,-76.57721350538951 L-0.7711895985583137,-76.5504394185484 L-0.8261675405063087,-76.49824765746571 L-0.890321286045882,-76.44813515466502 L-0.9632497522216434,-76.40041520862262 L-1.0444969973812417,-76.35538615978344 L-1.1335550716780722,-76.31332952536576 L-1.2298671927241402,-76.27450823934305 L-1.3328312265392057,-76.23916500860636 L-1.4418034520336565,-76.20752079558459 L-1.5561025854899295,-76.1797734368089 L-1.6750140398818183,-76.15609640605808 L-1.7977943924028108,-76.13663772981741 L-1.9236760322729165,-76.12151906183148 L-2.0518719597663386,-76.11083492253685 L-2.1815807064569457,-76.1046521081296 L-2.311991345920644,-76.10300927296191 L-2.4422885635682303,-76.10591668787892 L-2.5716577539126257,-76.11335617600633 L-2.6992901134028706,-76.1252812263905 L-2.8243876969849824,-76.14161728478037 L-2.946168406776549,-76.16226221973338 L-3.063870881666354,-76.18708696113123 L-3.17675925726973,-76.21593630711375 L-3.2841277664808697,-76.24862989438566 L-3.3853051518598836,-76.28496332583042 L-3.479658862268795,-76.32470944838094 L-3.5665990075195175,-76.36761977315848 L-3.6455820463097277,-76.41342602900076 " />
			<path d="M-13.000000000000002,-70.00061775789187 L-13.0,-1.794887634817739 " />
			<path d="M-0.6438493774533135,-3.2404347232615573 L-0.6438493774533133,2.1442281811916635 " />
			<path d="M-3.943849377453313,-3.2404347232615573 L-3.943849377453313,2.1442281811916635 " />
			<path d="M1.706150622546684,-76.83082775078891 L1.706150622546684,-73.24105248115343 " />
			<path d="M-6.293849377453315,-76.83082775078891 L-6.293849377453315,-73.24105248115343 " />
			<path d="M-0.6438493774533157,-76.83082775078891 L-0.6438493774533156,-71.44616484633569 " />
			<path d="M-3.943849377453316,-76.83082775078891 L-3.9438493774533154,-71.44616484633569 " />

       </g>

       <!-- solid lines -->
       <g  stroke="rgb(40,40,40)" fill="none">
			<path d="M10.322322198539908,-3.187431330018618 L1.7061506225466871,-0.5268424917801267 " />
			<path d="M-6.293849377453313,1.9434786384550677 L-10.322322198539908,3.1874313300186174 " />
			<path d="M-10.322322198539908,3.187431330018618 L-9.175397509813251,3.9102048742405264 " />
			<path d="M-9.175397509813251,3.9102048742405264 L-9.994629430332292,4.163175614718194 " />
			<path d="M-11.387323695214661,4.054759583084909 L-9.994629430332292,4.163175614718195 " />
			<path d="M-11.96078603957799,3.6933728109739543 L-11.387323695214661,4.054759583084909 " />
			<path d="M-11.960786039577991,3.6933728109739556 L-12.118389762664707,3.592008144339438 L-12.271579564858586,3.4893351487844857 L-12.42029964933498,3.385391221231393 L-12.564495847289221,3.280214221518179 L-12.704115637666671,3.1738424586087857 L-12.83910816629265,3.0663146766396845 L-12.969424264395222,2.9576700408079564 L-13.095016466514098,2.8479481231060326 L-13.215839027789126,2.7371888879082644 L-13.331847940622104,2.6254326774145524 L-13.44300095070581,2.512720196956383 L-13.549257572414417,2.3990925001706 L-13.650579103549717,2.284590974046287 L-13.746928639437748,2.169257323850255 L-13.838271086370696,2.0531335579366092 L-13.924573174389199,1.9362619724458865 L-14.005803469400378,1.8186851358994036 L-14.081932384627164,1.7004458736943941 L-14.152932191384807,1.581587252505556 L-14.218777029180565,1.4621525645987428 L-14.279442915132977,1.342185312062489 L-14.334907752707208,1.221729190963084 L-14.38515133976336,1.1008280754290196 L-14.430155375914742,0.9795260016705797 L-14.469903469193506,0.8578671519403701 L-14.504381142021128,0.735895838440681 L-14.533575836481626,0.613656487183515 L-14.557476918895581,0.4911936218091391 L-14.57607568369327,0.3685518473691011 L-14.589365356585521,0.2457758340795935 L-14.597341097031139,0.12291030105105742 L-14.6,3.0935239496280174e-14 " />
			<path d="M-14.6,2.3337623560835863e-15 L-14.597146175175643,-0.12733542552839924 L-14.58858581636232,-0.2546210711940073 L-14.574322270103108,-0.38180717659471436 L-14.554361112516144,-0.5088440202421771 L-14.528710147114724,-0.635681938999682 L-14.49737940175663,-0.7622713474971989 L-14.460381124723902,-0.8885627575160333 L-14.417729779934547,-1.0145067973354953 L-14.36944204128809,-1.1400542310340378 L-14.315536786147172,-1.2651559777372903 L-14.256035087957722,-1.3897631308054812 L-14.190960208010614,-1.5138269769527588 L-14.120337586348017,-1.637299015290912 L-14.044194831817991,-1.7601309762900612 L-13.96256171128124,-1.8822748406489014 L-13.875470137974174,-2.003682858067125 L-13.782954159032954,-2.124307565912679 L-13.685049942183237,-2.2441018077765653 L-13.58179576160098,-2.3630187519079295 L-13.473231982949713,-2.4810119095222207 L-13.359401047600194,-2.59803515297529 L-13.240347456038593,-2.7140427337962922 L-13.116117750469712,-2.8289893005723536 L-12.986760496622,-2.9428299166780296 L-12.852326264761519,-3.0555200778426 L-12.712867609922258,-3.1670157295483397 L-12.568439051360539,-3.277273284252968 L-12.419097051241533,-3.3862496384295415 L-12.264899992566239,-3.4939021894171267 L-12.105908156347514,-3.600188852075666 L-11.94218369804414,-3.7050680752385317 L-11.77379062326207,-3.80849885795632 L-11.600794762732406,-3.9104407655255655 L-11.42326374657587,-4.010853945296069 L-11.241266977863834,-4.1096991422506886 L-11.054875605486231,-4.206937714351501 L-10.864162496336972,-4.302531647646323 L-10.669202206827727,-4.396443571129689 L-10.470070953741235,-4.488636771352484 L-10.266846584435486,-4.579075206774511 L-10.059608546410491,-4.6677235218543895 L-9.848437856249465,-4.754547060871266 L-9.63341706794662,-4.839511881472953 L-9.414630240633922,-4.922584767945175 L-9.192162905719464,-5.003733244196744 L-8.966102033450229,-5.08292558645561 L-8.736535998912395,-5.160130835670779 L-8.50355454748243,-5.235318809615296 L-8.26724875974248,-5.308460114685526 L-8.027711015873809,-5.37952615739214 L-7.785034959542145,-5.448489155538311 L-7.539315461289107,-5.51532214908074 L-7.290648581444002,-5.579999010669284 L-7.039131532570491,-5.642494455861043 L-6.7848626414627935,-5.702784053004936 L-6.52794131070632,-5.7608442327928815 L-6.268467979817736,-5.81665229747387 L-6.006544085979631,-5.870186429727299 L-5.742272024385204,-5.921425701192134 L-5.475755108208394,-5.970350080648523 L-5.207097528215159,-6.016940441848713 L-4.936404312031669,-6.061178570994161 L-4.66378128308534,-6.103047173855945 L-4.389335019234771,-6.142529882535676 L-4.1131728111047074,-6.179611261864294 L-3.835402620142414,-6.214276815436205 L-3.5561330364117962,-6.246512991276428 L-3.2754732361417234,-6.276307187138547 L-2.9935329390452377,-6.30364775543136 L-2.710422365426289,-6.32852400777233 L-2.4262521930907734,-6.350926219166052 L-2.141133514078711,-6.3708456318060875 L-1.8551777912344924,-6.3882744584987 L-1.568496814632162,-6.40320588570714 L-1.281202657872774,-6.4156340762152935 L-0.993407634270911,-6.425554171409654 L-0.705224252947488,-6.432962293178725 L-0.4167651748460102,-6.437855545429108 L-0.12814316868947737,-6.440232015217688 L0.16052893310484698,-6.440090773499469 L0.44913827853556554,-6.437431875490767 L0.7375720401349343,-6.432256360647631 L1.0257174590770584,-6.424566252259475 L1.3134618892592522,-6.414364556658112 L1.6006928413393344,-6.401655262042466 L1.8872980267116382,-6.386443336919452 L2.1731654014045465,-6.368734728161612 L2.458183209882379,-6.348536358682269 L2.7422400287345714,-6.325856124729127 L3.0252248102349477,-6.300702892797347 L3.3070269257541316,-6.273086496163327 L3.5875362090081744,-6.243017731040528 L3.8666429991263893,-6.210508352358861 L4.144238183521615,-6.175571069169271 L4.42021324054613,-6.13821953967533 L4.6944602819165615,-6.098468365893763 L4.966872094891172,-6.056333087946011 L5.2373421841830705,-6.011830177983062 L5.505764813592933,-5.964977033745902 L5.772035047344972,-5.915791971764136 L6.036048791110003,-5.864294220195419 L6.297702832699542,-5.810503911308494 L6.556894882415057,-5.754442073612787 L6.813523613036582,-5.696130623637629 L7.067488699435064,-5.635592357364318 L7.318690857792956,-5.572850941314379 L7.56703188441773,-5.507930903297485 L7.812414694133128,-5.4408576228226915 L8.054743358233148,-5.371657321176693 L8.293923141983912,-5.300357051173009 L8.5298605416588,-5.226984686576094 L8.7624633210923,-5.151568911204513 L8.991640547738369,-5.07413920771743 L9.217302628219128,-4.994725846088805 L9.439361343350024,-4.913359871773821 L9.657729882627809,-4.830073093572117 L9.872322878167788,-4.74489807119262 L10.083056438077115,-4.657868102524819 L10.28984817925105,-4.569017210621464 L10.492617259579395,-4.478380130397754 L10.691284409550498,-4.385992295052259 L10.885771963240476,-4.29188982221484 L11.076003888675526,-4.196109499827004 L11.261905817555485,-4.098688771760219 L11.443405074326993,-3.999665723177797 L11.6204307045949,-3.8990790656460694 L11.792913502860825,-3.7969681220006883 L11.960786039577915,-3.693372810974004 " />
			<path d="M11.96078603957799,-3.6933728109739543 L12.534248383941318,-3.331986038863 " />
			<path d="M12.534248383941318,-3.331986038863 L12.288478807785605,-2.7176285262743773 " />
			<path d="M12.288478807785605,-2.7176285262743773 L11.469246887266564,-2.4646577857967094 " />
			<path d="M10.322322198539908,-3.187431330018618 L11.469246887266564,-2.4646577857967094 " />
			<path d="M1.7061506225466867,-1.4455470884438184 L1.7049458973315037,-1.4888504565738767 L1.7013324473673763,-1.53212774037419 L1.6953124492614475,-1.5753528712272395 L1.686889529235474,-1.6184998119304912 L1.6760687609415266,-1.6615425723802333 L1.6628566624058103,-1.7044552252270435 L1.6472611921024516,-1.7472119214934545 L1.6292917441596084,-1.7897869061444107 L1.608959142700801,-1.83215453360114 L1.5862756353248626,-1.8742892831890903 L1.5612548857284465,-1.916165774510629 L1.533911965475522,-1.957758782733248 L1.5042633449188325,-1.999043253784056 L1.472326883278769,-2.039994319441417 L1.4016687525918332,-2.120797780702684 L1.3221077950404596,-2.199974503901324 L1.233835679940106,-2.2773337453760902 L1.1370650625477734,-2.3526891399384002 L1.0320290717568663,-2.4258591498424 L0.9189807484692656,-2.4966675021252946 L0.7981924359976329,-2.5649436132643566 L0.6699551239665205,-2.6305230001275706 L0.5345777472928748,-2.693247676227906 L0.3923864419347587,-2.752966532326605 L0.24372375920126732,-2.8095357004685724 L0.08894784051641924,-2.86281890057288 L-0.0715684453749077,-2.91268776874342 L-0.23743840068043198,-2.959022166508772 L-0.40826243014932806,-3.001710470246304 L-0.5836290037321898,-3.0406498400932604 L-0.7631156479929586,-3.075746467696993 L-0.9462899638844369,-3.106915802207503 L-1.132710668435467,-3.134082753967844 L-1.3219286578402603,-3.1571818754116805 L-1.5134880893888023,-3.1761575187322104 L-1.7069274796318676,-3.190963969942605 L-1.9017808161350716,-3.2015655590050063 L-2.0975786801436413,-3.207936745762773 L-2.2938493774533164,-3.210062181468956 L-2.490120074762991,-3.2079367457627725 L-2.685917938771561,-3.2015655590050063 L-2.880771275274765,-3.1909639699426045 L-3.07421066551783,-3.17615751873221 L-3.2657700970663717,-3.1571818754116796 L-3.454988086471165,-3.134082753967843 L-3.641408791022195,-3.106915802207502 L-3.824583106913673,-3.075746467696992 L-4.004069751174442,-3.040649840093259 L-4.179436324757304,-3.001710470246303 L-4.350260354226199,-2.9590221665087704 L-4.516130309531723,-2.9126877687434183 L-4.67664659542305,-2.8628189005728784 L-4.831422514107898,-2.8095357004685706 L-4.980085196841389,-2.752966532326603 L-5.122276502199505,-2.6932476762279034 L-5.2576538788731515,-2.6305230001275683 L-5.385891190904262,-2.5649436132643553 L-5.506679503375894,-2.4966675021252938 L-5.619727826663496,-2.425859149842397 L-5.724763817454405,-2.3526891399383967 L-5.821534434846736,-2.277333745376087 L-5.909806549947088,-2.199974503901321 L-5.9893675074984625,-2.120797780702681 L-6.060025638185397,-2.0399943194414143 L-6.09196209982546,-1.9990432537840532 L-6.121610720382149,-1.9577587827332459 L-6.1489536406350735,-1.9161657745106278 L-6.173974390231489,-1.874289283189089 L-6.1966578976074285,-1.8321545336011387 L-6.2169904990662355,-1.7897869061444094 L-6.234959947009079,-1.747211921493453 L-6.250555417312437,-1.7044552252270422 L-6.263767515848153,-1.661542572380232 L-6.2745882841421015,-1.6184998119304899 L-6.283011204168075,-1.5753528712272382 L-6.289031202274003,-1.5321277403741886 L-6.29264465223813,-1.4888504565738738 L-6.293849377453313,-1.4455470884438317 " />
			<path d="M-9.175397509813251,3.9102048742405264 L-9.175397509813251,2.833272293349882 " />
			<path d="M11.96078603957799,-3.6933728109739556 L11.960786039577988,-75.48887820368357 " />
			<path d="M-14.600000000000003,-71.79550539270961 L-14.597146175175647,-71.92284081823802 L-14.588585816362324,-72.05012646390362 L-14.574322270103112,-72.17731256930433 L-14.554361112516148,-72.3043494129518 L-14.528710147114728,-72.4311873317093 L-14.497379401756634,-72.55777674020682 L-14.460381124723906,-72.68406815022564 L-14.41772977993455,-72.81001219004511 L-14.369442041288094,-72.93555962374366 L-14.315536786147176,-73.06066137044691 L-14.256035087957725,-73.18526852351509 L-14.190960208010617,-73.30933236966237 L-14.12033758634802,-73.43280440800052 L-14.044194831817995,-73.55563636899967 L-13.962561711281243,-73.67778023335852 L-13.875470137974178,-73.79918825077674 L-13.782954159032958,-73.91981295862229 L-13.685049942183241,-74.03960720048617 L-13.581795761600983,-74.15852414461754 L-13.473231982949716,-74.27651730223184 L-13.359401047600198,-74.3935405456849 L-13.240347456038597,-74.5095481265059 L-13.116117750469716,-74.62449469328197 L-12.986760496622004,-74.73833530938765 L-12.852326264761523,-74.85102547055222 L-12.712867609922261,-74.96252112225795 L-12.568439051360542,-75.07277867696259 L-12.419097051241536,-75.18175503113916 L-12.264899992566242,-75.28940758212674 L-12.105908156347517,-75.39569424478528 L-11.942183698044143,-75.50057346794814 L-11.773790623262073,-75.60400425066594 L-11.60079476273241,-75.70594615823518 L-11.423263746575874,-75.80635933800568 L-11.241266977863837,-75.9052045349603 L-11.054875605486234,-76.00244310706111 L-10.864162496336975,-76.09803704035593 L-10.66920220682773,-76.19194896383931 L-10.470070953741239,-76.2841421640621 L-10.26684658443549,-76.37458059948412 L-10.059608546410495,-76.463228914564 L-9.848437856249468,-76.55005245358088 L-9.633417067946624,-76.63501727418257 L-9.414630240633926,-76.7180901606548 L-9.192162905719467,-76.79923863690635 L-8.966102033450232,-76.87843097916523 L-8.736535998912398,-76.9556362283804 L-8.503554547482434,-77.03082420232491 L-8.267248759742484,-77.10396550739515 L-8.027711015873813,-77.17503155010175 L-7.785034959542147,-77.24399454824793 L-7.5393154612891085,-77.31082754179036 L-7.290648581444004,-77.3755044033789 L-7.039131532570493,-77.43799984857066 L-6.784862641462795,-77.49828944571455 L-6.527941310706322,-77.55634962550249 L-6.268467979817737,-77.61215769018348 L-6.006544085979633,-77.66569182243691 L-5.742272024385206,-77.71693109390175 L-5.4757551082083955,-77.76585547335814 L-5.207097528215161,-77.81244583455833 L-4.936404312031671,-77.85668396370377 L-4.663781283085342,-77.89855256656556 L-4.389335019234773,-77.9380352752453 L-4.113172811104709,-77.97511665457391 L-3.8354026201424163,-78.00978220814582 L-3.5561330364117985,-78.04201838398605 L-3.2754732361417256,-78.07181257984816 L-2.99353293904524,-78.09915314814097 L-2.7104223654262913,-78.12402940048194 L-2.4262521930907757,-78.14643161187567 L-2.1411335140787133,-78.1663510245157 L-1.8551777912344947,-78.18377985120831 L-1.5684968146321643,-78.19871127841675 L-1.2812026578727762,-78.21113946892491 L-0.9934076342709133,-78.22105956411927 L-0.7052242529474902,-78.22846768588835 L-0.41676517484601244,-78.23336093813873 L-0.1281431686894796,-78.2357374079273 L0.16052893310484476,-78.23559616620908 L0.4491382785355633,-78.23293726820039 L0.737572040134932,-78.22776175335724 L1.0257174590770561,-78.2200716449691 L1.31346188925925,-78.20986994936773 L1.6006928413393322,-78.19716065475208 L1.887298026711636,-78.18194872962907 L2.1731654014045443,-78.16424012087123 L2.458183209882377,-78.14404175139188 L2.742240028734569,-78.12136151743874 L3.0252248102349455,-78.09620828550696 L3.3070269257541294,-78.06859188887294 L3.587536209008172,-78.03852312375014 L3.866642999126387,-78.00601374506847 L4.1442381835216135,-77.97107646187888 L4.420213240546128,-77.93372493238495 L4.69446028191656,-77.89397375860338 L4.96687209489117,-77.85183848065563 L5.237342184183069,-77.80733557069267 L5.505764813592931,-77.76048242645552 L5.77203504734497,-77.71129736447375 L6.036048791110002,-77.65979961290503 L6.297702832699541,-77.60600930401812 L6.5568948824150555,-77.54994746632241 L6.813523613036581,-77.49163601634724 L7.067488699435062,-77.43109775007393 L7.318690857792954,-77.368356334024 L7.5670318844177284,-77.3034362960071 L7.8124146941331265,-77.2363630155323 L8.054743358233145,-77.16716271388631 L8.293923141983909,-77.09586244388262 L8.529860541658797,-77.0224900792857 L8.762463321092296,-76.94707430391412 L8.991640547738365,-76.86964460042705 L9.217302628219125,-76.79023123879843 L9.43936134335002,-76.70886526448344 L9.657729882627805,-76.62557848628174 L9.872322878167784,-76.54040346390224 L10.083056438077111,-76.45337349523443 L10.289848179251047,-76.36452260333108 L10.492617259579392,-76.27388552310737 L10.691284409550494,-76.18149768776188 L10.885771963240472,-76.08739521492446 L11.076003888675523,-75.99161489253662 L11.261905817555482,-75.89419416446984 L11.44340507432699,-75.79517111588741 L11.620430704594897,-75.69458445835568 L11.792913502860822,-75.5924735147103 L11.960786039577911,-75.48887820368361 " />
			<path d="M11.960786039577988,-75.48887820368357 L12.534248383941316,-75.12749143157261 " />
			<path d="M12.534248383941318,-3.331986038863 L12.534248383941316,-75.12749143157261 " />
			<path d="M-5.570777059529474,3.156111143102336 L-5.477529022547807,3.2124690210946953 L-5.379303026098652,3.2671566118109006 L-5.276252655053445,3.320088406456002 L-5.168539037612053,3.3711816415746085 L-5.056330593364853,3.420356428458736 L-4.939802769954086,3.467535878060735 L-4.819137768746229,3.512646221215992 L-4.694524259944355,3.5556169239874196 L-4.56615708758589,3.596380797951392 L-4.434236964887046,3.634874105252675 L-4.298970160410287,3.6710366582640956 L-4.160568175545528,3.7048119136951234 L-4.019247413809353,3.7361470610022094 L-3.875228842479334,3.764993104962659 L-3.7287376470925127,3.7913049422829124 L-3.580002879348264,3.8150414321214607 L-3.4292570989660867,3.8361654604161206 L-3.276736010058296,3.854643997915095 L-3.1226780925861797,3.870448151821073 L-2.9673242294758837,3.8835532109676274 L-2.810917329977047,3.8939386844572668 L-2.6537019498531063,3.901588333700735 L-2.49592390899713,3.906490197807452 L-2.3378299070710784,3.908636612287408 L-2.179667137769474,3.9080242210352543 L-2.021682902310598,3.9046539815778694 L-1.864124222759571,3.8985311635771813 L-1.7072374557879137,3.889665340590591 L-1.5512679074735098,3.8780703751018906 L-1.3964594497432548,3.8637643968460598 L-1.243054139058134,3.8467697744618565 L-1.0912918379369378,3.827113080516506 L-0.9414098399103876,3.8048250499571865 L-0.7936424984921071,3.7799405320542716 L-0.6482208607465636,3.752498435911471 L-0.5053723060269233,3.722541669628069 L-0.36532019044770014,3.6901170732083877 L-0.22828349764807943,3.655275345323373 L-0.09447649639199618,3.618070964038825 L0.03589159445968049,3.57856210163421 L0.16261693308099545,3.536810533645255 L0.2855013734052947,3.4928815422725332 L0.4043527749438014,3.446843814307078 L0.518985303213944,3.398769333732625 L0.6292197203077077,3.3487332691724 L0.7348836651456541,3.2968138563564584 L0.8358119229784315,3.2430922757933263 L0.9318466837143777,3.18765252583723 L1.0228377886692948,3.1305812913493787 L1.1086429653525878,3.07196780815866 L1.1891280499226493,3.0119037235336727 L1.2641671969636739,2.9504829528842738 L1.33364307625589,2.887801532916675 L1.39744705623154,2.823957471471723 L1.4554793738297667,2.759050594281132 L1.5076492904848178,2.693182388881285 L1.5538752340036717,2.6264558459286653 L1.5940849261112384,2.5589752981650213 L1.6282154954637202,2.4908462572840717 L1.6562135759534122,2.4221752489548125 L1.6780353901512437,2.353069646259388 L1.6936468177565898,2.2836375018059574 L1.7030234489473224,2.2139873787790614 L1.7061506225466867,2.14422818119167 " />
			<path d="M1.7061506225466867,2.144228181191662 L1.7049458973315037,2.100924813061604 L1.7013324473673763,2.0576475292612906 L1.6953124492614475,2.0144223984082408 L1.686889529235474,1.9712754577049894 L1.6760687609415266,1.9282326972552473 L1.6628566624058103,1.885320044408437 L1.6472611921024516,1.842563348142026 L1.6292917441596084,1.7999883634910698 L1.608959142700801,1.7576207360343405 L1.5862756353248626,1.7154859864463903 L1.5612548857284465,1.6736094951248515 L1.533911965475522,1.6320164869022324 L1.5042633449188325,1.5907320158514247 L1.472326883278769,1.5497809501940636 L1.4016687525918332,1.4689774889327967 L1.3221077950404596,1.3898007657341567 L1.233835679940106,1.31244152425939 L1.1370650625477734,1.23708612969708 L1.0320290717568663,1.1639161197930807 L0.9189807484692656,1.0931077675101861 L0.7981924359976329,1.024831656371124 L0.6699551239665205,0.95925226950791 L0.5345777472928748,0.8965275934075747 L0.3923864419347587,0.8368087373088755 L0.24372375920126732,0.780239569166908 L0.08894784051641924,0.7269563690626004 L-0.0715684453749077,0.6770875008920603 L-0.23743840068043198,0.6307531031267084 L-0.40826243014932806,0.5880647993891761 L-0.5836290037321898,0.5491254295422201 L-0.7631156479929586,0.5140288019384875 L-0.9462899638844369,0.48285946742797736 L-1.132710668435467,0.4556925156676366 L-1.3219286578402603,0.43259339422380005 L-1.5134880893888023,0.41361775090327013 L-1.7069274796318676,0.39881129969287565 L-1.9017808161350716,0.3882097106304745 L-2.0975786801436413,0.38183852387270756 L-2.2938493774533164,0.3797130881665245 L-2.490120074762991,0.3818385238727078 L-2.685917938771561,0.3882097106304745 L-2.880771275274765,0.3988112996928759 L-3.07421066551783,0.4136177509032706 L-3.2657700970663717,0.4325933942238007 L-3.454988086471165,0.45569251566763747 L-3.641408791022195,0.48285946742797825 L-3.824583106913673,0.5140288019384887 L-4.004069751174442,0.5491254295422212 L-4.179436324757304,0.5880647993891777 L-4.350260354226199,0.6307531031267102 L-4.516130309531723,0.6770875008920623 L-4.67664659542305,0.7269563690626024 L-4.831422514107898,0.78023956916691 L-4.980085196841389,0.8368087373088775 L-5.122276502199505,0.8965275934075769 L-5.2576538788731515,0.9592522695079124 L-5.385891190904262,1.0248316563711255 L-5.506679503375894,1.093107767510187 L-5.619727826663496,1.1639161197930832 L-5.724763817454405,1.237086129697084 L-5.821534434846736,1.3124415242593934 L-5.909806549947088,1.3898007657341593 L-5.9893675074984625,1.4689774889327993 L-6.060025638185397,1.5497809501940663 L-6.09196209982546,1.5907320158514273 L-6.121610720382149,1.6320164869022347 L-6.1489536406350735,1.6736094951248528 L-6.173974390231489,1.7154859864463916 L-6.1966578976074285,1.7576207360343419 L-6.2169904990662355,1.7999883634910712 L-6.234959947009079,1.8425633481420276 L-6.250555417312437,1.8853200444084384 L-6.263767515848153,1.9282326972552486 L-6.2745882841421015,1.9712754577049907 L-6.283011204168075,2.0144223984082426 L-6.289031202274003,2.057647529261292 L-6.29264465223813,2.100924813061607 L-6.293849377453313,2.144228181191649 " />
			<path d="M-6.293849377453313,2.144228181191665 L-6.2909357765178395,2.2115640261449774 L-6.282199218246623,2.278801776207866 L-6.267652430061841,2.34584347939459 L-6.247316603731324,2.4125914693205894 L-6.221221364496383,2.478948507482919 L-6.189404727913741,2.544817924917347 L-6.151913044474454,2.6101037630257444 L-6.108800932080491,2.674710913368618 L-6.060131196477354,2.738545256219131 L-6.005974739758632,2.8015137976767597 L-5.946410457075807,2.8635248051408557 L-5.881525121703751,2.924487940946741 L-5.811413258629381,2.984314393969659 L-5.73617700684762,3.0429170090048627 L-5.655925970565253,3.1002104137353586 L-5.570777059529477,3.1561111431023345 " />
			<path d="M-3.6455820463097295,2.5616299029798157 L-3.7138095245784646,2.514937322664608 L-3.7737656219566182,2.466085332090633 L-3.8251010894042574,2.4153584979917655 L-3.867516893737024,2.363052308214657 L-3.885300640099534,2.3364018586982214 L-3.90076595951824,2.3094714504785077 L-3.9138903221085797,2.2823003157868063 L-3.924654608292993,2.254928037544845 L-3.933043136654331,2.2273944917003705 L-3.9390436867805536,2.199739789135847 L-3.94264751706743,2.172004217234905 L-3.943849377453313,2.144228181191667 " />
			<path d="M-3.943849377453313,2.144228181191664 L-3.9418618801918477,2.108513662270386 L-3.9359041764624383,2.0728851827534114 L-3.925990618895202,2.037428574768583 L-3.912145090118644,2.0022292563901694 L-3.8944009452243114,1.9673720258592389 L-3.872800931411458,1.9329408572972737 L-3.847397085005298,1.899018698405154 L-3.818250606096937,1.8656872706348815 L-3.7854317111069955,1.8330268723154424 L-3.749019463628099,1.8011161852071012 L-3.709101583953762,1.7700320849501483 L-3.6657742377525135,1.7398494558647486 L-3.619141804396378,1.7106410105480545 L-3.56931662550183,1.6824771147031916 L-3.5164187342889965,1.655425617622116 L-3.4605755664111175,1.6295516887307275 L-3.401921652950894,1.6049176605900137 L-3.340598296323329,1.5815828787314523 L-3.2767532298658293,1.5596035586884254 L-3.210540261935658,1.5390326505680778 L-3.0716539932162097,1.502310786198138 L-2.925277040855712,1.4717709372497287 L-2.772819094923178,1.4477072191630027 L-2.6157484087799254,1.4303513786977011 L-2.455577658997088,1.4198705620851728 L-2.2938493774533137,1.4163657053187935 L-2.132121095909539,1.4198705620851728 L-1.9719503461267016,1.4303513786977011 L-1.8148796599834496,1.4477072191630027 L-1.662421714050915,1.4717709372497287 L-1.5160447616904174,1.5023107861981377 L-1.3771584929709704,1.5390326505680774 L-1.310945525040799,1.5596035586884245 L-1.2471004585832992,1.5815828787314514 L-1.1857771019557342,1.6049176605900128 L-1.1271231884955102,1.6295516887307269 L-1.0712800206176303,1.6554256176221158 L-1.018382129404797,1.6824771147031912 L-0.9685569505102489,1.710641010548054 L-0.9219245171541137,1.7398494558647482 L-0.8785971709528646,1.7700320849501479 L-0.8386792912785279,1.8011161852071005 L-0.8022670437996322,1.8330268723154415 L-0.7694481488096907,1.8656872706348804 L-0.7403016699013296,1.8990186984051531 L-0.7148978234951693,1.9329408572972724 L-0.6932978096823161,1.967372025859237 L-0.6755536647879834,2.002229256390168 L-0.6617081360114248,2.0374285747685827 L-0.6517945784441885,2.0728851827534105 L-0.6458368747147789,2.1085136622703846 L-0.6438493774533134,2.1442281811916564 " />
			<path d="M-0.6438493774533134,2.144228181191663 L-0.6451393365630511,2.1730038501964652 L-0.6490071969292286,2.2017345259450596 L-0.6554469108164338,2.2303752855320997 L-0.6644484091730394,2.258881346643962 L-0.675997617375037,2.287208137579782 L-0.690076477232936,2.3153113669431735 L-0.7066629752273075,2.343147092895677 L-0.7257311769288346,2.3706717918636326 L-0.7472512675490433,2.3978424265910694 L-0.7711895985583115,2.4246165134321878 L-0.8261675405063065,2.476808274514865 L-0.8903212860458798,2.5269207773155493 L-0.9632497522216412,2.57464072335796 L-1.0444969973812395,2.6196697721971414 L-1.13355507167807,2.6617264066148096 L-1.229867192724138,2.700547692637522 L-1.3328312265392035,2.735890923374214 L-1.4418034520336542,2.7675351363959932 L-1.5561025854899273,2.7952824951716804 L-1.675014039881816,2.818959525922489 L-1.7977943924028086,2.8384182021631608 L-1.9236760322729143,2.8535368701491017 L-2.0518719597663364,2.864221009443721 L-2.1815807064569435,2.8704038238509733 L-2.311991345920642,2.8720466590186575 L-2.442288563568228,2.869139244101655 L-2.5716577539126235,2.8616997559742483 L-2.6992901134028684,2.849774705590079 L-2.82438769698498,2.8334386472002047 L-2.946168406776547,2.812793712247199 L-3.0638708816663516,2.7879689708493403 L-3.176759257269728,2.7591196248668304 L-3.2841277664808675,2.726426037594913 L-3.385305151859882,2.6900926061501553 L-3.479658862268793,2.650346483599628 L-3.5665990075195153,2.6074361588220984 L-3.6455820463097255,2.5616299029798184 " />
			<path d="M0.1262548770339973,-78.23574466534072 L-0.045883550877308554,-78.29033412260111 L-0.2243367357565833,-78.34082368300264 L-0.40860338506665994,-78.38707151640733 L-0.59816587567736,-78.42894770810527 L-0.7924917079197356,-78.46633462375782 L-0.9910350014299922,-78.499127239844 L-1.1932380285810835,-78.52723343868192 L-1.398532781194433,-78.55057426719637 L-1.6063425661307504,-78.5690841587058 L-1.8160836252777384,-78.58271111710556 L-2.027166775384002,-78.59141686293003 L-2.238999063132727,-78.59517694088352 L-2.4509854308058245,-78.59398078853741 L-2.66253038785955,-78.58783176600124 L-2.8730396837159846,-78.57674714648374 L-3.081921977071311,-78.56075806777066 L-3.2885904970316537,-78.53990944475575 L-3.492464691410206,-78.51425984327034 L-3.692971857555391,-78.4838813155662 L-3.8895487511288973,-78.44885919791365 L-4.081643168314383,-78.40929187088368 L-4.268715497012279,-78.3652904829871 L-4.450240232663223,-78.31697863844761 L-4.62570745444202,-78.26449204998525 L-4.7946242576753475,-78.20797815758613 L-4.956516138459445,-78.14759571432894 L-5.110928326588223,-78.08351434043205 L-5.257427063047469,-78.01591404677352 L-5.395600818486548,-77.94498472922291 L-5.525061449244806,-77.87092563520515 L-5.645445287685266,-77.79394480399489 L-5.756414163772743,-77.71425848231375 " />
			<path d="M-14.600000000000003,-71.79550539270961 L-14.600000000000001,8.881784197001252e-16 " />
			<path d="M1.7061506225466863,-1.4455470884438175 L1.7061506225466863,2.144228181191663 " />
			<path d="M-6.293849377453313,-1.4455470884438175 L-6.293849377453313,2.144228181191663 " />

       </g>
    </g>
    
</svg>

```

=== file: docs/manuscript/main.tex ===
```tex
% !TEX program = pdflatex
% Powder-Excavator design brainstorming and prior-art review.
%
% Build:
%   cd docs/manuscript
%   pdflatex main
%   bibtex   main
%   pdflatex main
%   pdflatex main
%
% Or use the Makefile in this directory: ``make``.

\documentclass[11pt,a4paper]{article}

\usepackage[margin=1in]{geometry}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{microtype}
\usepackage{textcomp}
\usepackage[hyphens]{url}
\usepackage{xcolor}
\usepackage{hyperref}
\hypersetup{
  colorlinks=true,
  linkcolor=blue!50!black,
  citecolor=blue!50!black,
  urlcolor=blue!50!black,
  pdftitle={Powder-Excavator: design brainstorming and prior-art notes},
  pdfauthor={vertical-cloud-lab},
}
\usepackage{enumitem}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{longtable}
\usepackage{caption}
\usepackage{siunitx}

\sisetup{
  range-units = single,
  per-mode    = symbol,
}

\title{Powder-Excavator: design brainstorming and prior-art notes}
\author{vertical-cloud-lab}
\date{April 2026}

\begin{document}
\maketitle

\begin{abstract}
\noindent
This document captures a literature-aware brainstorm for the gantry-mounted
``powder excavator'' sketched in \texttt{powder-excavator-sketch.jpg} and
recreated as the labelled subpanels under \texttt{docs/figures/}. It is
structured roughly like the introduction to a \emph{Digital Discovery}
manuscript on a new powder-handling tool: where does this device sit in the
landscape of automated powder dispensing, what gap is it trying to fill, and
what would we need to measure to defend that claim. The current revision
adopts the corrected \emph{longitudinal-pivot, sideways-tilt} geometry
identified by the Edison Scientific design-review tasks~\cite{edisonscientific},
and adds a cam-slot / pin-defined-path actuation variant (Sec.~\ref{sec:pinslot})
based on a follow-on hand sketch.
\end{abstract}

\paragraph{Provenance.}
This brainstorm was prompted by feedback on PR~\#2 to ``send the idea to
Edison for a high-effort literature search'' and to consider the discussion
at the Accelerated Discovery
thread~\cite{accdiscthread}. The Edison Scientific service was wired in via
the \texttt{futurehouse\_client} SDK (pinned to the Edison endpoint
\texttt{api.platform.edisonscientific.com}) through the in-repo
\texttt{scripts/edison\_submit.py} helper for a follow-up session: a
high-effort PaperQA3
literature search and two high-effort design-review tasks were
run~\cite{edisonscientific}, and their verbatim responses are archived under
\texttt{docs/edison/}. Peer-reviewed citations marked
\cite{tom2024selfdrivinglaboratoriesfor,yang2007meteringanddispensing,bahr2018collaborativeevaluationof,bahr2020recentadvancesin,jiang2023autonomousbiomimeticsolid,szymanski2023anautonomouslaboratory,szymanski2024automatingthesynthesis,fei2024alabosapythonbased,lunt2023modularmultirobotintegration,lunt2024aroboticworkflow,carruthers2025amobilerobotic,alsenz2011powderpickinganinexpensive,hernandezdelvalle2024pelletdispensomixerand,doloi2025democratizingselfdrivinglabs,moravkar2020traditionalandadvanced,freeman2017characterisingpowderflow,ghoroi2013multifacetedcharacterizationof,mccalla2023semiautomatedexperimentsto}
are taken directly from the Edison literature task and are listed in the
\hyperref[sec:references]{References} section.

\paragraph{Geometry note (post-review).}
The mechanism described in Sec.~\ref{sec:fits} and Sec.~\ref{sec:variations}
has been updated to the \textbf{longitudinal-pivot, sideways-tilt,
smooth-cam-ramp} geometry adopted after the Edison design-review tasks
identified two design-blocking issues with the earlier ``ferris-wheel
gondola'' (transverse pivot, end-over-end tilt, sawtooth and hooked-lip)
revision: a kinematic impossibility in the push-to-tilt mechanism and a
trapped-volume / bridging problem for cohesive powders. Section~\ref{sec:pinslot}
adds a \emph{pin-defined-path} actuation variant in which a peg on a stem
descending from the gantry rides in a routed slot in a fixed external board;
this captures the cam-ramp idea in a fully constrained ``peg in slot'' form
that removes the approach/contact ambiguity of a free cam follower.

% --------------------------------------------------------------------------
\section{Why powder handling is the pinch point in self-driving labs}
\label{sec:why}

Self-driving laboratories (SDLs) for chemistry and materials science have
matured rapidly over the past five years, with closed-loop platforms now
routinely combining robotic execution, automated characterization, and
Bayesian or generative experiment design~\cite{tom2024selfdrivinglaboratoriesfor,szymanski2023anautonomouslaboratory,fei2024alabosapythonbased,mccalla2023semiautomatedexperimentsto}.
Across nearly every published SDL, \textbf{solids handling --- and powder
dispensing in particular --- is repeatedly called out as the dominant
bottleneck}: it is the step most likely to be left to a human, the one most
sensitive to material properties (cohesion, hygroscopicity, triboelectric
charging), and the one that most often limits end-to-end
autonomy~\cite{tom2024selfdrivinglaboratoriesfor,yang2007meteringanddispensing,carruthers2025amobilerobotic,jiang2023autonomousbiomimeticsolid}.
Tom et al.'s 2024 \emph{Chemical Reviews} survey of SDLs makes the point
bluntly: solid-dispensing hardware ``remains rare and costly relative to
liquid handling, and many labs simply avoid direct powder
manipulation'' wherever pre-dissolved stocks will
do~\cite{tom2024selfdrivinglaboratoriesfor}.

Compared with liquid handling, powder dispensing is hard for three coupled
reasons:

\begin{enumerate}[leftmargin=*]
  \item \textbf{No universal flow regime.} Free-flowing crystalline powders,
    fluffy nanopowders, sticky organics, and hygroscopic salts each demand
    different feeders, hoppers, and tip
    geometries~\cite{yang2007meteringanddispensing,bahr2018collaborativeevaluationof,carruthers2025amobilerobotic}.
  \item \textbf{Dose accuracy scales poorly down.} Sub-milligram gravimetric
    dosing needs a draft-shielded balance, vibration isolation, and feedback
    control; the 17{,}797-dispense ETC benchmark across four commercial
    platforms found that \SI{2}{\milli\gram} targets exhibited
    \SIrange{190}{680}{\percent} higher \%RSD than \SI{50}{\milli\gram}
    targets, and that across the full dataset the percent error spanned
    \SI{-10}{\percent} to \SI{+3245}{\percent} (\SI{95.3}{\percent} of
    dispenses fell between \SI{-25}{\percent} and
    \SI{+100}{\percent})~\cite{bahr2018collaborativeevaluationof,bahr2020recentadvancesin}.
  \item \textbf{Cross-contamination is expensive.} Reservoirs and
    end-effectors must either be disposable, easily cleaned, or dedicated
    per material, which blows up the part count of a multi-reagent
    platform~\cite{tom2024selfdrivinglaboratoriesfor,carruthers2025amobilerobotic}.
\end{enumerate}

% --------------------------------------------------------------------------
\section{Prior art (representative, not exhaustive)}
\label{sec:priorart}

Table~\ref{tab:priorart} summarises the device classes that any new
powder-handling tool has to position itself against. The rows are not
intended as a complete vendor list; they are the classes of mechanism that
recur across the SDL literature
\cite{tom2024selfdrivinglaboratoriesfor,yang2007meteringanddispensing,bahr2018collaborativeevaluationof,bahr2020recentadvancesin,jiang2023autonomousbiomimeticsolid,szymanski2023anautonomouslaboratory,fei2024alabosapythonbased,lunt2023modularmultirobotintegration,lunt2024aroboticworkflow,carruthers2025amobilerobotic,alsenz2011powderpickinganinexpensive}.

\begin{small}
\begin{longtable}{@{}p{0.21\linewidth}p{0.36\linewidth}p{0.36\linewidth}@{}}
\caption{Prior-art device classes for automated powder handling. Quantitative
claims in the ``Strengths'' and ``Limits'' columns are taken from the cited
sources.}
\label{tab:priorart}\\
\toprule
\textbf{Class} & \textbf{Strengths} & \textbf{Limits relevant to us} \\
\midrule
\endfirsthead
\multicolumn{3}{c}{\tablename\ \thetable{} -- continued from previous page}\\
\toprule
\textbf{Class} & \textbf{Strengths} & \textbf{Limits relevant to us} \\
\midrule
\endhead
\midrule
\multicolumn{3}{r}{\emph{continued on next page}}\\
\endfoot
\bottomrule
\endlastfoot
Gravimetric vibratory-head dispensers (Quantos QX1/QX5, Chemspeed SWING /
Powdernium / FLEX GDU-Pfd, Unchained Labs Freeslate/Junior) &
High precision on dense free-flowing powders; closed-loop weight feedback;
integrated workflow software; ETC benchmark established Quantos as the best
overall \% error / \%RSD / time balance and Chemspeed SWING as the fastest
(\SIrange{13}{65}{\second})~\cite{bahr2018collaborativeevaluationof,bahr2020recentadvancesin} &
Per-reagent consumable cartridges/heads; abrasive solids damage Quantos
heads; hygroscopic powders clog them; Chemspeed SWING and one Unchained
system \emph{failed outright} on fumed silica in the ETC
benchmark~\cite{bahr2018collaborativeevaluationof,carruthers2025amobilerobotic} \\
\addlinespace
Auger / screw feeders on robot arms (Berlinguette \& MacLeod ``Ada''
thin-film SDL; Aspuru-Guzik group platforms; Chemspeed FLEX GDU-Pfd
hopper/auger module) &
Robust to mildly cohesive powders; metered dosing; \SI{\pm10}{\percent}
tolerance setting on GDU-Pfd~\cite{bahr2020recentadvancesin} &
Mechanical complexity; cleaning between materials non-trivial; the Lunt
modular-workflow paper notes ``grinding, mixing and recovering solids
remains an unsolved challenge in commercial
automation''~\cite{lunt2023modularmultirobotintegration,lunt2024aroboticworkflow} \\
\addlinespace
Spatula-mimicking dual-arm robots (Cooper group's
PowderBot~\cite{jiang2023autonomousbiomimeticsolid}) &
Versatile across material classes; \(\sim\)\SI{0.07}{\percent} error at
\SI{200}{\milli\gram} for non-challenging solids; comparable failure rate
to commercial systems (\SI{23.1}{\percent} vs.\ \SI{26.9}{\percent} vs.\
\SI{26.5}{\percent}) at lower hardware
cost~\cite{jiang2023autonomousbiomimeticsolid} &
Slow throughput due to manipulator motions and corrective restarts;
struggles with compressible powders (CaCO\textsubscript{3}) and highly
hygroscopic materials~\cite{jiang2023autonomousbiomimeticsolid} \\
\addlinespace
Slurry-conversion workflows (Ceder group A-Lab: Quantos doses precursors
into vials, ball-milled with ethanol into pumpable
slurry)~\cite{szymanski2023anautonomouslaboratory,szymanski2024automatingthesynthesis,fei2024alabosapythonbased} &
Sidesteps last-mile dry-transfer issues; well-characterised end-to-end
workflow; 36 novel compounds in 17 days &
Adds ethanol handling, drying, and a dedicated \texttt{RecoverPowder}
regrinding task downstream; upstream powder loading is still
manual~\cite{szymanski2024automatingthesynthesis} \\
\addlinespace
Capsule / cartridge ``drop a pre-weighed slug'' &
Eliminates real-time dosing error &
Needs upstream weighing; Quantos cartridge ecosystem in particular
criticised for high cost, single-vendor procurement, RFID-locked reuse,
and clogging on hygroscopic
powders~\cite{carruthers2025amobilerobotic} \\
\addlinespace
Acoustic / ultrasonic non-contact transfer (Echo-style platforms; ultrasonic
capillaries, \SIrange{14}{16}{\micro\gram} through \SI{0.2}{\milli\meter}
nozzles)~\cite{yang2007meteringanddispensing} &
Non-contact, no cross-contamination, very high throughput &
Limited to specific particle sizes / suspensions; mostly demonstrated in
solid-freeforming / additive-manufacturing contexts, not chemistry SDLs \\
\addlinespace
Vacuum / electrostatic pickup (DryPette, Electronic Spatula, automated
electrostatic pipettes)~\cite{yang2007meteringanddispensing,alsenz2011powderpickinganinexpensive} &
Gentle on the powder; good for fragile crystals; \SI{0.3}{\milli\gram}-class
doses possible &
Hard to release a clean dose; \emph{exquisitely} sensitive to humidity,
charge decay, and powder conductivity~\cite{yang2007meteringanddispensing} \\
\addlinespace
Positive-displacement ``PowderPicking'' (standard Gilson MICROMAN pipettes
with disposable capillary-piston tips,
Alsenz)~\cite{alsenz2011powderpickinganinexpensive,cook2021guideto} &
Cheap; \SIrange{0.6}{25}{\milli\gram} range; mean CV \(\sim\)\SI{6}{\percent}
across 10 powders; disposable tips eliminate carryover &
Manual / medium throughput; depends on complete homogeneous filling of the
probe cylinder; tip clogging with adhesive
powders~\cite{alsenz2011powderpickinganinexpensive} \\
\addlinespace
Bulk ``scoop and dump'' mechanical scoops (\textbf{this project}; closest
commercial analogue: MTI PF-A glass dispenser referenced in the community
thread)~\cite{mtipfaglassdispenser} &
Cheap, mechanically simple, no actuators on the end-effector, easy to clean;
the present design has \emph{no consumable} at all &
Not a precision dosing tool; dose CV likely \SIrange{5}{20}{\percent}
depending on whether a strike-off bar is used; not for sub-mg work \\
\end{longtable}
\end{small}

Two recent overviews are particularly relevant for situating a new device
in this landscape: Tom et al.'s 2024 \emph{Chemical Reviews}
survey~\cite{tom2024selfdrivinglaboratoriesfor} and Lunt et al.'s
solid-state-workflow papers~\cite{lunt2023modularmultirobotintegration,lunt2024aroboticworkflow}.
Both flag \emph{bulk powder transfer from stock containers into a precision
dispenser} as a step that is still almost universally manual. On the
frugal-hardware side, recent open-hardware platforms have demonstrated cost
reductions of up to \SI{94}{\percent} relative to commercial analogues for
adjacent dispensing problems (pellet dispensers, 3D-printed
autosamplers)~\cite{hernandezdelvalle2024pelletdispensomixerand,doloi2025democratizingselfdrivinglabs},
albeit for liquid or pellet handling rather than fine inorganic powders.

\subsection{Community prior art from the Accelerated Discovery thread}
\label{sec:thread}

The Accelerated Discovery thread ``Accurate powder dispensing for chemistry
and materials science applications''~\cite{accdiscthread} is a useful,
opinionated cross-section of what practitioners have actually tried. The
points most relevant to our design:

\begin{itemize}[leftmargin=*]
  \item \textbf{Framing (sgbaird, post 1).} Accurate powder dispensing is
    ``around an order of magnitude more complex and more expensive than
    liquid handling.''  This matches the SDL
    surveys~\cite{tom2024selfdrivinglaboratoriesfor} and is the gap we are
    trying to chip away at on the cheap, mechanical end of the design space.
  \item \textbf{3D-printed calibrated spatulas (post 2, after Cook
    et al.~\cite{cook2021guideto}).} Sets of spatulas with known volumes
    give a calibration curve from volume to mass; decent accuracy in
    isolation, but degraded by static in gloveboxes and by lighter powders.
    Two takeaways for us: (i) \textbf{a strike-off bar is essentially
    required} (``just manually tapped the spatula until each scoop is level
    \dots\ it doesn't seem too difficult to physically level it by passing
    something against the top of the scoop'') --- directly endorses the
    strike-off bar variant in Sec.~\ref{sec:variations}; (ii) per-material
    calibration is realistic if the trough is geometrically well-defined.
  \item \textbf{Positive-displacement-pipette method (post 3,
    Alsenz~\cite{alsenz2011powderpickinganinexpensive}).} Packs a pipette
    tip into the powder; spans \SIrange{0.6}{20}{\milli\gram} with
    \(\sim\)\SI{10}{\percent} CV across tip sizes. The
    \SI{10}{\percent} CV is a \textbf{useful baseline target} for our scoop
    on cohesive powders.
  \item \textbf{Auger / screw-feed builds (loppe35, post 4).} Cheap (jewelry-
    scale load cell \(\approx\) USD 25, stepper + control board) but ``leaky
    when dispensing vertically'' and needs hopper flow aids. Reinforces
    keeping the excavator's bucket \emph{un-augered} in the baseline design;
    the auger is positioned in Sec.~\ref{sec:variations} as an optional
    add-on, not the core mechanism.
  \item \textbf{The ``pick it back up'' problem (muon, posts 5/7/14).}
    Dispensing is only half the workflow; recovering powder \emph{after}
    an operation (ball-milling, acoustic mixing, weighing) is at least as
    hard, and a vacuum/pipette approach is awkward when the milled powder
    is fine and multi-precursor cross-contamination matters.
  \item \textbf{Autotrickler v4 + A\&D FX-120i (sgbaird, post 6).}
    \SI{\pm1}{\milli\gram}, fast-response scale, BLE-controllable from a
    Pico W; community-validated reference for the ``scale + metered feed''
    downstream of a bulk-transfer device. Suggests a concrete integration
    target: excavator $\rightarrow$ tared Autotrickler-style
    trickler/scale.
  \item \textbf{PowderBot (Cooper group)~\cite{jiang2023autonomousbiomimeticsolid}
    and A-Lab (Ceder
    group)~\cite{szymanski2023anautonomouslaboratory,fei2024alabosapythonbased}.}
    Two published end-to-end SDLs that \emph{did} solve solids handling, but
    with workflow-specific workarounds (typically involving milling).
  \item \textbf{Manual MTI PF-A glass dispenser (sgbaird, post~24 --- the
    specific post linked in the review feedback)~\cite{mtipfaglassdispenser}.}
    A \SI{250}{\milli\litre} hand dispenser whose geometry is reminiscent
    of Owen Melville's earlier scoop. The closest existing artifact to our
    bucket and effectively a manual ancestor of the excavator's scoop motion.
\end{itemize}

% --------------------------------------------------------------------------
\section{Where the powder-excavator fits}
\label{sec:fits}

The proposed mini excavator is \textbf{not} competing with Quantos-class
precision dispensers. It is aimed at the \textbf{upstream, bulk-transfer
step}: moving a relatively coarse aliquot of powder from a stock bed (e.g.\
a tray, jar, or hopper) to a downstream station --- which might itself be
a precision dispenser, a sieve, a press, a crucible, a dissolution vial,
or simply a weigh boat for a human-in-the-loop workflow. In that niche, the
design choices shown in Fig.~\ref{fig:panels} (post-review) make sense:

\begin{itemize}[leftmargin=*]
  \item \textbf{Half-cylinder ladle suspended on a longitudinal pivot pin.}
    The pin runs along the trough's long axis $L$, through the two short
    end caps, with the two arms gripping those end caps. The trough rolls
    \emph{sideways} about the pin to pour, dispensing over the
    \emph{full long edge} rather than through a narrow end-cap point. This
    eliminates the trapped-volume / arching failure mode that an end-over-
    end tilt of a half-cylinder would have for cohesive powders (Edison v2
    \S3, archived in \texttt{docs/edison/}).
  \item \textbf{Pure mechanical actuation via a fixed smooth inclined cam
    ramp.} Removes the servo and its wiring/maintenance burden; the deposit
    angle is set by how far up the cam the trough's chamfered rim lip has
    ridden (i.e.\ by gantry $X$ position), not by a torque setpoint. A
    smooth ramp --- rather than a sawtooth tooth --- is required because a
    fixed point engaging a fixed-radius hook on a horizontally-translating
    pivot is geometrically impossible (Edison v2 \S1).
    Sec.~\ref{sec:pinslot} below describes a stricter ``peg in routed slot''
    refinement of this idea.
  \item \textbf{Mandatory bed-edge strike-off bar.} Promoted from
    ``optional variation'' to a baseline-required part: without a
    level-defining strike-off, dose CV will sit in the
    \SIrange{15}{30}{\percent} range across powder classes, which would
    put the device below the \(\approx\) \SI{10}{\percent} CV baseline
    achievable with Alsenz's positive-displacement-pipette
    method~\cite{alsenz2011powderpickinganinexpensive} and below the
    Cooper PowderBot's \SI{0.07}{\percent} at
    \SI{200}{\milli\gram}~\cite{jiang2023autonomousbiomimeticsolid}.
  \item \textbf{Open top with no lid.} Trades some retention loss for
    radically simpler cleaning --- which, per
    \cite{tom2024selfdrivinglaboratoriesfor,carruthers2025amobilerobotic},
    is the single biggest hidden cost in multi-material SDLs.
  \item \textbf{Optional grounded conductive lining.} Because the pivot
    pin is a metal dowel, it can double as the ground path for an
    inexpensive copper-tape lining of the trough interior. This is the
    prototype-friendly equivalent of using ESD-safe filament and
    dramatically reduces triboelectric charging on fine inorganics
    (Edison v1 \S2).
\end{itemize}

A reasonable framing for a write-up: \emph{``A purely mechanical,
gantry-mounted ladle for bulk powder transfer in self-driving materials
labs, designed to bridge stock containers and precision dispensers without
adding servo count or cleaning burden, and to take over the upstream-loading
and post-process recovery roles flagged as unsolved by Lunt
et al.''}~\cite{lunt2023modularmultirobotintegration,lunt2024aroboticworkflow}.

The design intentionally makes \textbf{no claim} of being a precision
dispenser, and tempers the ``bidirectional dispense + recover'' claim made
in earlier framing: a half-cylinder cannot scoop cleanly out of a flat bed
without leaving a trail of retained powder, so recovery is a meaningful but
lossy operation rather than a complete one (Edison v2 \S7).

% --------------------------------------------------------------------------
\section{Pin-defined-path actuation: a routed-slot refinement}
\label{sec:pinslot}

A hand-sketch (\texttt{PXL\_20260423\_231729467.jpg}) suggests an actuation
refinement that fully resolves the ``approach-and-contact'' ambiguity of
the smooth cam ramp described in Sec.~\ref{sec:fits}. Rather than a free
cam follower that approaches a fixed inclined surface and slides up it, the
trough is suspended from the gantry carriage by a short \emph{stem} that
carries a transverse \emph{peg} at its top end. This peg rides in a
\emph{routed slot} cut into a fixed external board mounted at fixed height
in the work area (Fig.~\ref{fig:pinslot}). The carriage--stem joint is a
pin pivot; the peg is captured in the slot for the entire stroke. Pure-$X$
gantry travel therefore drives a deterministic tilt-vs.-$X$ schedule given
by the slot's routed path: where the slot is straight and horizontal the
trough holds level (scoop, transport); where it deviates, the difference
between the carriage's straight-line path and the slot's routed path forces
the stem (and the trough rigidly attached to it) to rotate about the
carriage pivot.

This is mechanically the same idea as the cam paths used in coin-op
mechanisms, player pianos, and Geneva-style indexing devices, applied to
the gantry geometry of a self-driving lab. Compared with the smooth
inclined cam ramp of Sec.~\ref{sec:fits}, the pin-in-slot refinement has
several concrete advantages:

\begin{itemize}[leftmargin=*]
  \item \textbf{No engagement event.} The peg never has to ``find'' the
    cam; it is captive in the slot from the moment the trough is mounted.
    There is no lift-off direction in which the contact can lose registration.
  \item \textbf{Bidirectional and reversible.} The slot path constrains
    motion in both $+X$ and $-X$ directions, so the trough can be tipped,
    held, and \emph{returned to level} purely by gantry motion. The smooth
    cam ramp relies on gravity for the return.
  \item \textbf{Programmable schedule.} The slot is the program. Different
    routed slots --- straight-then-rising, multi-stage with a hold detent,
    a small ``knock'' wiggle to dislodge bridges (Edison v1 \S6) ---
    implement different dispensing schedules without any change to the
    trough or carriage. The strike-off bar sweep can be encoded as a small
    detent in the slot near the bed-edge $X$ coordinate.
  \item \textbf{Deterministic tilt at deposit.} Because the peg is captured
    on both sides of the slot wall, the deposit angle is set by slot
    geometry to the tolerance of the routing operation, not by friction at
    a sliding cam interface.
  \item \textbf{Simpler statics analysis.} The slot wall provides both the
    tilt-up reaction force and (on the return stroke) the tilt-down force.
    The smooth cam ramp only provides the former; the latter relies on
    gravity, which fails for very light troughs or when the trough is empty.
\end{itemize}

\paragraph{Caveats.} The slot must be cut to the same accuracy as the
finished tilt schedule requires; a cleanly milled slot in acrylic or
aluminium is straightforward, but FDM-printed slots will have layer-line
ripples that the peg will feel as a low-amplitude tilt jitter. The peg
should be a hardened dowel pin with a low-friction sleeve (PTFE or oil-
impregnated bronze) to minimise stick-slip, and the slot should be slightly
oversized in the direction perpendicular to the desired motion to allow
thermal play without binding. The board itself becomes a second
\emph{registered} fixture in the work area --- it must be mounted in a
known relationship to the gantry's $X$ axis, which is the same registration
problem the bed and the deposit station already face, and so does not
introduce a new class of failure.

% Place the four-panel layout figure environment up here so it floats
% sensibly relative to the references that point at it.
\begin{figure}[ht]
  \centering
  \includegraphics[width=0.95\linewidth]{../figures/panel-A-orthographic}
  \caption{Orthographic views of the half-cylinder trough with the
    longitudinal pivot pin, end-cap pivot bosses, and the continuous
    chamfered rim lip (full length $L$, both long sides) that defines the
    pour edge and engages the cam ramp. Generated by
    \texttt{scripts/generate\_figures.py}.}
  \label{fig:panels}
\end{figure}

\begin{figure}[ht]
  \centering
  \includegraphics[width=0.85\linewidth]{../figures/panel-E-pin-slot}
  \caption{Pin-defined-path actuation variant (Sec.~\ref{sec:pinslot}). A
    vertical stem hangs from the gantry carriage on a pivot; a transverse
    peg at the top of the stem rides in a routed slot cut into a fixed
    external board. The slot's shape over $X$ is the program for the
    trough's tilt schedule. Generated by
    \texttt{scripts/generate\_figures.py}.}
  \label{fig:pinslot}
\end{figure}

\begin{figure}[ht]
  \centering
  \includegraphics[width=0.95\linewidth]{../figures/cad/assembly}
  \caption{Honest hidden-line render of the parametric CAD assembly
    (trough + two arms + pivot pin) at the default
    \texttt{ExcavatorParams}, projected from
    \texttt{(-0.7,\,-1.0,\,-0.6)}. Unlike the schematic figures above
    (which are hand-laid-out for clarity), this image is generated
    directly from the same CadQuery solids that
    \texttt{python -m cad.build} writes to STEP/STL for the slicer ---
    so what you see here is what the printer will produce. End-on and
    side views (\texttt{docs/figures/cad/assembly-end} and
    \texttt{assembly-side}) and per-part renders are produced
    alongside it by \texttt{python -m cad.render}.}
  \label{fig:cadrender}
\end{figure}

% --------------------------------------------------------------------------
\section{Open questions and what we'd actually need to measure}
\label{sec:measure}

To defend the design in a manuscript-style argument we would need at
minimum:

\begin{itemize}[leftmargin=*]
  \item \textbf{Dose statistics across powder classes.} Mean and CV of
    delivered mass for at least three archetypal powders (e.g.\
    free-flowing crystalline like NaCl, cohesive metal-oxide nanopowder
    like TiO\textsubscript{2}, hygroscopic salt like LiCl) across at least
    30 scoops each. Following Cooper-group
    practice~\cite{jiang2023autonomousbiomimeticsolid}, this should also
    include the known ``hard'' cases --- fumed silica (which broke the
    Chemspeed SWING and one Unchained system in the ETC
    benchmark~\cite{bahr2018collaborativeevaluationof}) and CaCO\textsubscript{3}
    (which broke the PowderBot~\cite{jiang2023autonomousbiomimeticsolid}).
  \item \textbf{Standardised flowability descriptors per powder.} Report
    Carr's compressibility index (CI $\le$ \SI{10}{\percent} = excellent;
    \SIrange{21}{25}{\percent} = passable; $>$\SI{35}{\percent} = very poor)
    and the Hausner ratio (HR \numrange{1.00}{1.11} = excellent;
    \numrange{1.26}{1.34} = passable; $>$\num{1.45} = poor) for every test
    powder, plus Freeman FT4 basic flow energy (BFE) and specific energy
    (SE) where
    available~\cite{moravkar2020traditionalandadvanced,freeman2017characterisingpowderflow,ghoroi2013multifacetedcharacterizationof}.
  \item \textbf{Carryover / cross-contamination.} Mass remaining in the
    trough after a ``tip and pour'' event vs.\ after a programmed cleaning
    cycle (knock-oscillation against the cam, inverted shake, brush, or
    air blast), stratified by powder class, following the approach
    Carruthers used to expose Quantos-cartridge
    limitations~\cite{carruthers2025amobilerobotic}.
  \item \textbf{Sensitivity to bed depletion.} How much does the dose
    change as the powder bed depletes / gets cratered? Run 30 consecutive
    scoops from the same $X,Y$ location and plot dispensed mass vs.\ scoop
    number (Edison v1 \S3). The expected steep decay curve will set the
    requirement that the gantry must raster across the bed.
  \item \textbf{Coupling to a downstream balance.} Demonstrate that the
    excavator $\rightarrow$ balance $\rightarrow$ vibratory-head pipeline
    reduces total wall-clock time per dispensed dose vs.\ a one-stage
    precision dispenser doing both bulk and fine work --- i.e.\ directly
    attack the upstream-loading bottleneck flagged
    by~\cite{tom2024selfdrivinglaboratoriesfor,lunt2023modularmultirobotintegration,lunt2024aroboticworkflow,carruthers2025amobilerobotic}.
  \item \textbf{Mandatory benchmark experiments (Edison v2 \S6).}
    \begin{enumerate}
      \item \textbf{Cam-engagement test.} 3D print the trough (with its
        continuous chamfered rim lip) and the inclined cam track. Drive
        the gantry purely in $X$ and verify the lip rides up the cam
        without binding, skipping, or requiring coordinated $Z$ motion.
      \item \textbf{Pin-slot equivalence test.} Repeat the same dispense
        schedule with the cam ramp of Sec.~\ref{sec:fits} and the routed
        slot of Sec.~\ref{sec:pinslot}; compare tilt-angle repeatability
        and dose CV.
      \item \textbf{Trapped-volume bake-off.} Compare retained mass of a
        cohesive test powder (TiO\textsubscript{2} or flour) for a sideways
        tilt vs.\ a hypothetical end-over-end tilt of the same trough. The
        expected \SIrange{7}{26}{\percent} retention penalty of the
        end-over-end case (Edison v2 \S3) is the empirical justification
        for the longitudinal-pivot geometry.
      \item \textbf{Strike-off efficacy.} Measure the dose mass of 30
        consecutive scoops with and without the bed-edge strike-off bar.
        The expected $2$--$3\times$ CV improvement is the empirical
        justification for keeping the strike-off bar in the baseline.
    \end{enumerate}
  \item \textbf{Cam-ramp / strike-off / lip geometry sweep.} Cam slope,
    ramp length, strike-off cross-section, and rim-lip chamfer angle are
    the four knobs most likely to dominate dose CV; small parameter sweeps
    are cheap with 3D-printed parts. For the pin-slot variant, the
    equivalent sweep is over slot path shape, peg diameter, and peg sleeve
    material.
\end{itemize}

% --------------------------------------------------------------------------
\section{Design variations worth prototyping (still pure-mechanical)}
\label{sec:variations}

Carrying over from the original brainstorming, with the literature in mind:

\begin{itemize}[leftmargin=*]
  \item \textbf{Pin-defined-path actuation (Sec.~\ref{sec:pinslot}).}
    Replaces or augments the smooth cam ramp; the slot board is the new
    fixed-fixture part. Worth prototyping side-by-side with the cam ramp
    to compare schedule programmability and dose CV.
  \item \textbf{Dual cam ramps (or dual slot boards), left and right} ---
    for two-output workflows (e.g.\ one for ``real'' deposit, one for
    ``purge / waste'' to clear residual material between materials).
  \item \textbf{Strike-off bar variants} --- a square cross-section vs.\ a
    chamfered blade vs.\ a thin compliant flap, scored for fill
    repeatability and for how cleanly the bar sweeps the rim of cohesive
    powders without flicking material away.
  \item \textbf{Twin troughs back-to-back} --- fill one while dumping the
    other for doubled throughput at the cost of one extra carriage stop.
  \item \textbf{Replaceable, snap-in trough liners} --- a thin,
    single-material liner (e.g.\ ESD-safe filament or copper-tape-lined
    PETG) that snaps into the printed trough body. Lets us treat the
    trough as consumable per-material and bypass the cleaning problem
    entirely; this is the prototype-friendly analogue of Quantos
    cartridges~\cite{carruthers2025amobilerobotic} without the RFID
    lock-in.
  \item \textbf{Spring-loaded passive flap lid actuated by the same cam or
    slot} --- closes during transport (curing the fine-powder retention
    problem) and opens at the same instant the cam (or slot detent)
    engages, with no extra actuator.
  \item \textbf{Internal auger as an \emph{option}} --- adds one rotary
    actuator but converts the device from ``tilt and pour all'' to a
    coarse metered dispenser, which would squarely overlap with mid-range
    commercial systems~\cite{bahr2020recentadvancesin}.
\end{itemize}

% --------------------------------------------------------------------------
\section{Open parametric CAD pipeline and design-for-manufacturing feedback}
\label{sec:cad-pipeline}

A central pragmatic constraint placed on this design by the project's
requirements is that the dispenser must run on an \emph{existing} gantry
(X / Y / Z) without any additional actuator on the bucket --- a ``no second
axis'' constraint. To make this constraint enforceable as the design
iterates, the same dimensions that drive Figures~\ref{fig:panels} and~\ref{fig:pinslot} and
the prior-art arguments above also drive a small open-source parametric
CAD pipeline shipped with this manuscript under \texttt{cad/} in the
project repository.

The choice of authoring tool was deliberately restricted to \emph{open,
pip-installable} options so that anyone re-running this pipeline pays only
the price of \texttt{pip install cadquery}. CadQuery
(\url{https://github.com/CadQuery/cadquery}) was chosen over the
commercial parametric / generative-CAD ecosystems (Rhino + Grasshopper,
Fusion 360 Generative Design, nTop, Onshape FeatureScript) because it is
pure Python, runs unattended on a CI runner, and emits standards-compliant
STEP and STL output that any open-source slicer (PrusaSlicer, OrcaSlicer,
Cura) can consume. Sister tools (\texttt{build123d} and OpenSCAD) fit the
same niche and remain candidates as the design matures; a separate
high-effort literature task on generative / computational CAD for
mechanical hardware is in flight and will be folded into a future revision.

The pipeline has three stages, all driven by a single
\texttt{ExcavatorParams} dataclass that holds every dimension in
millimetres:

\begin{enumerate}
  \item \textbf{Authoring} (\texttt{cad/excavator.py}). Each part --- the
    half-cylinder trough with its closed end caps and pivot bosses, the
    two vertical arms, the dowel pin, the bed-edge strike-off bar, the
    smooth inclined cam ramp, and the routed slot board for the
    pin-defined-path variant of \S\ref{sec:pinslot} --- is a plain Python
    function that takes \texttt{ExcavatorParams} and returns a CadQuery
    solid. Because every dimension lives in the dataclass, a design
    iteration is a \texttt{git diff} on a single file.
  \item \textbf{Build} (\texttt{cad/build.py}). Exports STEP and STL for
    every part plus a STEP for the full assembly into \texttt{cad/build/}
    (gitignored), along with a JSON manifest containing the parameter
    snapshot used.
  \item \textbf{Feedback} (\texttt{cad/dfm.py}). Runs an automated battery
    of design-for-manufacturing and gantry-only-kinematics checks against
    the current parameter set and exits non-zero on failure --- making it
    suitable to drop into CI. Categories of checks include FDM
    printability (minimum wall thickness, FDM overhang angle on the
    cam-ramp underside, rim-lip chamfer presence, dowel-pin clearance);
    cam-ramp kinematics (lip engagement, ramp fits inside the gantry's
    X travel, ramp angle in a 15--45\textdegree band); and, most
    importantly for the no-second-axis constraint, slot-path kinematics
    (every waypoint inside the routed board, the slot's X and Z spans
    fitting inside the gantry's travel, and a flag on any X-direction
    reversal in the slot path so that bidirectional gantry motion is
    surfaced explicitly to the designer).
\end{enumerate}

Three small unit tests (\texttt{cad/tests/test\_excavator.py}) exercise (i)
that every part builds at default parameters, (ii) that the DFM check
passes at default parameters, and (iii) that two deliberate parameter
regressions --- a sub-minimum trough wall and a slot path routed off the
board --- are correctly caught by the DFM check. This is the start of a
closed-loop generative-CAD workflow rather than the finished product;
near-term extensions are to add a \emph{slicer-side} check
(e.g.\ delegating support volume estimation to PrusaSlicer's CLI) and a
\emph{print-then-measure} loop in which a successful print of the trough
is photographed and analysed with classical CV to extract its as-built
inner radius and wall thickness, closing the loop on the parametric
inputs.

% --------------------------------------------------------------------------
\bibliographystyle{plainurl}
\bibliography{refs}
\label{sec:references}

\end{document}

```

=== file: docs/edison/README.md ===
````md
# Edison Scientific raw responses

This directory holds the **verbatim** answers returned by the
[Edison Scientific](https://edisonscientific.com/) tasks submitted from PR #2
of this repository, archived here for provenance so future readers can see
exactly what the model said before any of it was paraphrased into the
`README.md` or `docs/manuscript/main.tex`.

| File | Edison `task_id` | `job_name` | Status |
|---|---|---|---|
| `literature-high-powder-dispensing.md` | `86968176-9927-43b4-aa09-e7e4f86855be` | `job-futurehouse-paperqa3-high` | success |
| `analysis-v1-pre-ferris-wheel.md` | `faeecd89-ea28-403b-94f3-c8402a79e78a` | `job-futurehouse-data-analysis-crow-high` | success — superseded by v2 |
| `analysis-v2-corrected-gondola.md` | `844f6123-36b7-4e61-a0f6-c2e357f804b0` | `job-futurehouse-data-analysis-crow-high` | success |
| _generative-CAD lit-review (resubmitted)_ | `f5a27ed3-8530-4102-9e31-5af9bbe9b0e0` | `job-futurehouse-paperqa3-high` | submitted, polling |
| _gantry-only analysis iter 1 of 3_ | `d6e32c46-2774-4477-a060-9993ef51ab10` | `job-futurehouse-data-analysis-crow-high` | submitted, polling |

A previous generative-CAD literature query (`task_id`
`524e7e92-a326-440a-b6fd-f6eb220d9019`) was sent to the **wrong endpoint**
(`api.platform.futurehouse.org`) and ended up cancelled; it has been
resubmitted at the correct Edison endpoint (`f5a27ed3-…`). Iterations 2 and
3 of the gantry-only analysis cycle are queued behind iter 1 because each
iteration's prompt builds on the prior iteration's verbatim answer.

## Submitting / polling tasks

All Edison traffic must go through `https://api.platform.edisonscientific.com`
(the `api.platform.futurehouse.org` endpoint is a different cluster).
`scripts/edison_submit.py` pins the SDK's `service_uri` to the Edison host
and exposes three subcommands:

```bash
export EDISON_API_KEY=...                              # provided by Edison
python scripts/edison_submit.py submit-cad-litreview   # paperqa3-high
python scripts/edison_submit.py submit-analysis 1      # data-analysis-crow-high
python scripts/edison_submit.py poll <task_id>         # status + answer
```

The script embeds the design-context files (README, manuscript, prior
analyses, CadQuery model, DFM checks) inline as fenced code blocks rather
than using `upload_file`, because the chunked-upload endpoint currently 404s
on the Edison cluster.

## How the feedback was applied

The two analysis tasks identified two design-blocking issues with the
"ferris-wheel gondola" geometry that PR #2 had landed:

1. **Kinematic impossibility of push-to-tilt with a fixed sawtooth tooth**
   (`analysis-v2-corrected-gondola.md` §1). The pivot pin translates purely
   horizontally while the tooth is fixed in space; the trough's hooked end-lip
   sits at a fixed radius from the pin, so the pin-to-tooth distance must
   change as the gantry moves in X — i.e. the lip has to plunge through the
   solid tooth. Resolved in the present PR by **replacing the sawtooth +
   hook with a smooth inclined cam track** that the trough's end bumper
   slides up.
2. **Trapped-volume / arching of cohesive powder in an end-over-end tilt**
   (`analysis-v2-corrected-gondola.md` §3). At 45 ° end-over-end tilt, the
   semicircular cross-section + vertical end cap form a 90 ° V-pocket that
   retains 7–26 % of the dose for cohesive powders, and the powder must
   bottleneck through a ~13 mm spill point that is well below typical arching
   diameters. Resolved by **switching the pivot axis from transverse to
   longitudinal** (axis parallel to the trough's long axis L), so the trough
   tilts **sideways** and pours over the full 80 mm long edge where arching
   is impossible.

Two further items from the v1 review (still useful even though the geometry
has since changed) were also adopted:

- The **strike-off bar** is promoted from "optional variation" to a
  baseline-required feature (`analysis-v1-…` §3, `analysis-v2-…` §4); without
  it, dose CV will sit in the 15–30 % range, well above the 10 % CV baseline
  established by Alsenz's positive-displacement-pipette method.
- The **knock / oscillate-against-the-cam** behaviour for breaking bridged
  powder (`analysis-v1-…` §6) and **J-curve plunge trajectory** to avoid
  flat-blunt compaction during the dip step (`analysis-v1-…` §2) are added to
  the README as part of the standard motion sequence.

The literature-high task was used to expand the prior-art and benchmarking
sections of `docs/manuscript/main.tex` with peer-reviewed
references (Bahr ETC 2018, Bahr 2020, Jiang/Cooper PowderBot 2023, Szymanski
A-Lab 2023, Tom et al. *Chemical Reviews* 2024, Yang & Evans 2007, Carruthers
2025, Lunt 2023/2024, Hernandez del Valle 2024, Doloi 2025) and standardised
flowability descriptors (Carr index, Hausner ratio, Freeman FT4).

````

=== file: docs/edison/analysis-v1-pre-ferris-wheel.md ===
```md
This is an incredibly clever, high-leverage mechanism. The decision to offload the actuation from the end-effector to the gantry kinematics directly solves the mass, wiring, and reliability penalties that sink most custom lab automation.

Here is high-effort feedback across the six areas requested.

### 1. Mechanical Soundness

The core kinematic trick (translating X-motion into rotation via a fixed snag point) is valid, but the current geometry in the diagrams has critical flaws that will cause it to bind or drop powder prematurely.

**Pitfall 1: The pivot pin location.**
In Panel A and B, the pivot pin is shown spanning the *very top rim* of the trough. This is statically unstable. The centroid of a uniform half-cylinder shell sits at $r(1 - 2/\pi)$ below the diameter (about 0.36r), and the powder centroid sits even lower ($4r/3\pi$, about 0.42r below). If the pin is at the top rim, the trough is highly stable (a deep pendulum). However, when you hit the sawtooth to tilt it (Panel D, Step 3), the required force $F_x$ applied by the gantry will be huge because the lever arm from the pivot to the lip is almost zero. More severely, if the pivot is at the rim, pushing the *lip* against the sawtooth won't generate torque; the force vector passes almost directly through the pivot.
*Fix:* Drop the pivot pin down the side walls, about halfway between the rim and the bottom (slightly above the loaded centre of mass). This creates a sufficient lever arm for the sawtooth force to apply torque.

**Pitfall 2: The hooked lip vs. the sawtooth engagement.**
A downward-facing hooked lip pushed horizontally into an upward-facing sawtooth will "cam up" or skip out if the friction/catch isn't perfect. As the trough rotates, the angle of the lip relative to the tooth changes. The hook must have enough clearance to accommodate this sweep angle, or it will bind against the tooth. Furthermore, the engagement is only self-aligning in Z; in Y, if the gantry is slightly misaligned, one corner of the lip will hit first, applying a yaw torque that will cause the trough to skew and bind against the vertical arms.
*Fix:* The teeth should be wide enough in Y to span the entire lip, or the lip should have a defined "catch point" (like a notch or protruding pin) rather than relying on a continuous long edge to seat squarely.

**Pitfall 3: Trough swing during X-transport.**
A pendulum with a moving pivot will oscillate. Gantry accelerations/decelerations in X will cause the trough to swing, potentially spilling powder over the low front/back rims.
*Fix:* You need a mild friction damper (e.g., a wave washer on the pivot pin) or a soft mechanical detent/magnetic catch that holds the trough horizontal during transport but easily breaks loose when the lip hits the sawtooth.

**Worst-case force:**
Assuming the pivot is lowered to $\sim 0.5r$, the peak force to hold a 90° dump angle is roughly the weight of the loaded trough, $mg$. For a typical gantry (NEMA 17/23 steppers on belts or lead screws), this is trivial (a few Newtons). The risk is not stalling the motor; the risk is snapping a 3D-printed arm or boss if the lip binds in the sawtooth.

### 2. Powder-Handling Realism

For dozens-of-microns cohesive, hygroscopic, and triboelectrically charged powders, a pure "scoop and dump" from a static bed is fundamentally brutal.

**Sticking / Retention:** Cohesive powders (like TiO2 or damp salts) will bridge across the trough. Gravity alone will not empty a half-cylinder; the powder will form a stable arch across the diameter. Tipping it 90° (as in Panel D) will leave a substantial wedge of material in the back half. A 180° inversion is likely required for full clearing, which the current sawtooth geometry cannot achieve (the lip would slip off past 90°).

**Plunging (Dip down):** Pushing a blunt, flat half-cylinder straight down into a compacted powder bed will require massive Z-force. It will compress the powder beneath it rather than flowing into the scoop, and powder will spill out the open ends.
*Fix:* The trough needs a chamfered or knife-edge cutting lip on the plunging edge, and ideally the gantry should perform a scooped trajectory (a J-curve: plunge Z, translate X, lift Z) rather than a pure Z-plunge.

**ESD / Surface Treatment for 3D Prints:**
Standard PETG/Nylon will charge instantly and permanently, turning the trough into a magnet for fine powders.
*Recommendation:* Print in an ESD-safe filament (e.g., 3DXSTAT ESD PETG). Vapour smoothing helps with mechanical retention (reduces surface roughness where powders pack into layer lines), but does not solve charging. A simple and highly effective mitigation for prototyping is wrapping the interior in conductive copper tape, grounded to the gantry frame via the pivot pin (use a metal shoulder bolt).

### 3. Repeatability / Dose CV

**Without a strike-off bar:** Expect a CV of 15–30% for free-flowing powders, and upwards of 50% for cohesive powders. The "angle of repose" of the powder cone sitting above the rim will dictate the variable volume, and plunging straight down yields terrible bed-packing consistency.

**With a strike-off bar:** You can realistically hit a 5–10% CV for free-flowing materials (like NaCl or coarse silica) by strictly defining the volume. For cohesive materials, the variability in how the powder packs *into* the trough during the plunge will dominate, leaving CVs in the 10–20% range.

**Cheapest way to measure:**
Print 5 calibration weights (e.g., 1g, 2g, 5g, 10g). Mount a basic load cell (e.g., HX711 + 1kg bar cell, <$10) directly beneath the deposit location (the target tray). Script the gantry to scoop, dump into a lightweight cup on the load cell, tare, dump again. Run 50 cycles per powder. You do not need an analytical balance for 10% CV on a multi-gram scoop.

### 4. Benchmark Experiments

Since the excavator is a bulk-transfer tool, benchmark it against the true alternatives: manual lab-spatula transfer, and gravimetric drop-dispensers.

1.  **Transfer Rate vs. Pre-weighing (Throughput):** Compare the total cycle time (pick → transport → dump → return) of the excavator moving 5g of powder vs. the time required for an automated pick-and-place system to retrieve, open, dump, and dispose of a pre-weighed vial. The core value prop here is eliminating the vial bottleneck.
2.  **Holdup Mass (Carryover):** Measure the residual mass left in the scoop after one tip against the ledge for a known sticky powder (TiO2). Plot holdup mass vs. tip angle. This proves (or disproves) the "easy to clean/empty" claim.
3.  **Dose Consistency vs. Bed Depletion:** This is the most critical benchmark for a stationary bed. Scoop 30 times from the exact same X,Y location in a static bed. Plot dispensed mass vs. scoop number. You will almost certainly see a steep decay curve as a crater forms. This forces the design requirement that the gantry must update its X,Y plunging coordinates to raster across the bed.

### 5. Diagram Improvements

*   **General:** The lines indicating the trough walls in the front view (Panel A and B) give the illusion of a full cylinder. Change the shading/perspective to clearly show it is a hollow, open-topped half-pipe.
*   **Panel A:** The "Top" view is highly confusing. The dashed line representing the pivot pin implies it runs through the middle of the powder bed. If it's a single long rod spanning from arm to arm *above* the trough, it should be a solid line. If it's two stub pins, it should not connect. (The text says "single horizontal pivot pin", so the pin runs straight across the open mouth of the scoop). This directly blocks powder entering and leaving!
*   **Panel B:** Add a prominent "Center of Mass" symbol below the pin to clarify the gravity-return stability.
*   **Panel C:** The hooked lip is drawn on the short edge (the circular face) in the Isometric view, but described as being on the "long upper edge". It must be on the long edge to engage a linear sawtooth. Fix this CAD/drawing discrepancy.
*   **Panel D:** Add a zoomed-in callout on Step 3 showing exactly how the lip interfaces with the tooth. Show the force vectors (X-push from arms, Reaction force from tooth) to clarify the resulting torque direction.

### 6. Critique of the Documentation

**The claim of "purely mechanical / no actuators" is slightly overstated.**
Yes, there is no motor on the *bucket*, but the gantry axes are doing complex, force-loaded work to achieve this. You are trading a cheap micro-servo for complex path-planning and high off-axis loads on the gantry Z/X carriages. I would not bury this tradeoff.

**Missing capability: The "Knock".**
In the *brainstorming-and-literature.md* section on cohesive powders, you note clumps might bridge. With this setup, you can program the gantry to rapidly oscillate in X (+/- 2mm) while the lip is engaged with the sawtooth. This will repeatedly slam the trough against the ledge, acting as a pneumatic knocker to dislodge bridged powder. This is a massive feature of this design that commercial continuous-rotation augers cannot do. Add this explicitly to the README and the manuscript outline.

**Literature Context:**
The framing in Section 3 of the brainstorming doc ("where it fits") is excellent. However, the manuscript needs to acknowledge that bulk-transfer scoops *ruin* the protective microclimate of the powder. If you are handling hygroscopic salts, exposing a massive open trough of powder to the air during transport, and leaving a cratered, unsealed stock bed behind, is a severe chemical limitation. The document should explicitly bracket its use case: "For bulk transfer in ambient or globally controlled environments (gloveboxes)."

```

=== file: docs/edison/analysis-v2-corrected-gondola.md ===
```md
The "ferris-wheel gondola" redesign solves the major issues of the previous axis-of-rotation error, creating a mechanically sound baseline with stable pendulum action. However, the proposed pure-X actuation for end-over-end tipping contains a fatal kinematic flaw, and the behavior of cohesive powders inside a long, narrow semicircular channel necessitates a fundamental re-evaluation of both geometry and framing.

### 1. The Fatal Flaw: Kinematic impossibility of the push-to-tilt mechanism
The most critical issue with the current design is that step 3 ("Tip end-over-end -> deposit") **is kinematically impossible as drawn.**

*   The pivot pin translates purely horizontally (constant Z).
*   The sawtooth ledge is fixed in space (constant X, Z).
*   The hooked end-lip is at a fixed radius ($r_p \approx 40$ mm for $L=80$ mm) from the pivot pin.

For a fixed tooth to engage a point-like hook on the lip while the pivot translates purely in X, the distance from the pivot to the tooth must equal the constant radius $r_p$. However, pure horizontal translation necessarily changes this distance. As the gantry pushes forward, the distance drops below $r_p$, meaning the lip must physically plunge *through* the solid tooth/ledge. 

**The fix:** To achieve rotation without an actuator, the gantry *must* coordinate X and Z motion (moving the carriage in a circular arc centered on the engaged tooth), OR the "tooth" cannot be a fixed point but rather an inclined cam track that the lip slides up, OR the arm must be a telescopic/sprung compliant member. 

### 2. Mechanical Soundness of the Gondola
Assuming the kinematic issue is patched, the gondola arrangement itself is excellent.
*   **Stability:** The geometric center of mass of a semicircular cross-section is $4r/3\pi$, or 5.66 mm below the flat rim for a 26.7 mm diameter trough. Placing the pivot pin 2-4 mm above the loaded centroid ensures gravity strongly rights the trough ($>0.003$ Nm restoring moment), returning it to open-up without actuators.
*   **Structural Loads:** For an 80 mm long, 22.3 mL trough holding $\sim$22 g of powder (bulk density 1000 kg/m$^3$), the vertical force per 3D-printed PETG arm is just $\sim$0.11 N. The resulting bending moment at the carriage root is a negligible $\sim$0.003 Nm, producing $<0.2$ MPa of stress (well within PETG's 50 MPa yield strength).

### 3. Powder-Handling Realism
The geometry presents severe powder retention risks for dozens-of-microns cohesive powders (where wall friction angles $\phi_w$ routinely exceed 45° and unconfined yield strengths $\sigma_c$ exceed 100-500 Pa):
*   **The "Trapped Volume" problem:** When tilted end-over-end to 45°, the semicircular channel and the vertical end-cap form a 90° V-pocket. By integrating the enclosed volume, a perfectly fluid powder at 45° tilt still leaves 7.1% (1.58 mL) trapped below the spill lip. For a cohesive powder with a 30° angle of repose, the *effective* tilt at 45° is only 15°, trapping 26.4% (5.9 mL) of the dose.
*   **Bridging & Flow:** To pour, the powder must flow down a narrow 26.7 mm wide half-pipe. Cohesive powders will bridge across this small diameter and slump as a single solid plug, or stick entirely.
*   **Mitigation:** An ESD-safe filament is insufficient here. You will need a significant geometry change: either (a) eliminate the end-cap entirely, making it an open chute (but sacrificing transport capacity), or (b) abandon the end-over-end tilt in favor of tilting sideways (axis parallel to L), which pours over a massive 80 mm long edge where arching is impossible.

### 4. Repeatability & Dose CV
Volumetric scooping into cohesive powders is notoriously variable. Without a leveling step, dose CV will likely sit between 15-30% due to variable mounding and bridging. 
*   **Strike-off bar:** Implementing the strike-off bar (§5) is mandatory to hit the 10% CV baseline established by Alsenz's positive-displacement method.
*   **End-over-end vs. sideways pour:** A sideways tilt drops the entire dose uniformly over the long 80 mm edge. The current end-over-end tilt forces 22 mL of powder to bottleneck through a $\sim$13 mm radius spill point, massively increasing the likelihood of rat-holing and chugging (flow-stop-flow behavior).

### 5. Sawtooth Engagement
Given the kinematic impossibility outlined in §1, a printed end-lip + tooth will simply snap or stall the gantry. The sawtooth ledge must be converted into a smooth, inclined cam profile. A chamfered lip sliding along a polished/lubricated cam track will tilt the bucket repeatably without jamming.

### 6. Suggested Benchmark Experiments
1.  **Kinematic Cam Profile Test:** 3D print the trough and a passive inclined cam track. Drive the gantry purely in X to verify the bucket tilts without binding or requiring Z-coordination.
2.  **The "Trapped Volume" Bake-off:** Compare the retained mass of a cohesive test powder (e.g., TiO2 or flour) dumped from an end-over-end tilt versus a sideways tilt.
3.  **Strike-off Efficacy:** Measure the dose mass of 30 consecutive scoops with and without a fixed bed-leveling blade.

### 7. Framing Pushback: The "Bulk-Transfer" Position
Your positioning in the literature section is highly defensible and smartly avoids competing with Quantos-class systems. Claiming the "bulk transfer feeds precision dispenser" niche directly answers the unsolved automation bottleneck cited by *Materials Horizons* and *ChemRxiv*. However, the "dispense AND recover" (bidirectional) feature highlighted from the community thread is compromised by the trapped volume problem—an open half-pipe simply cannot scoop cleanly out of a flat bed without leaving a trail.

**Discretionary Analytical Decisions:**
*   Assumed a standard gantry translating purely in X and Z axes without rotary or coordinated multi-axis interpolation during the dump phase.
*   Estimated trough volume ($\sim$22.3 mL) and dimensions based on the $L \approx 3D$ and $L \approx 80$ mm constraints provided in the prompt.
*   Calculated structural loads assuming standard 3D printed PETG mechanical properties and typical inorganic powder bulk densities ($800-1600$ kg/m$^3$).
*   Assessed powder flow assuming typical cohesive unconfined yield strengths ($>100$ Pa) and high wall friction angles ($>40^\circ$) characteristic of dozens-of-microns ceramic/catalyst powders.
*   Trapped volume integral modeled the powder as fluid with definable angles of repose to establish the geometric bounds of the end-cap spill problem.

```

=== file: docs/edison/analysis-v3-longitudinal-tilt-cad.md ===
```md
# Edison Analysis v3 — Longitudinal-tilt / pin-in-slot CAD review

**Task ID:** `7f85494a-ce97-4ebf-bea9-6ac2359014dd`  
**Submitted:** 2026-04-24  
**Files uploaded:** `assembly.png`, `assembly-end.png`, `assembly-side.png`, `README.md`,
`manuscript.tex`, `cad/README.md`, `repo-snapshot.zip` (cad/, docs/figures, docs/manuscript,
docs/edison)

---

Based on a quantitative analysis of the CadQuery model (`cad/excavator.py`) and your provided design documents, here is high-effort feedback across your five focus areas. I'm pushing back hard on the baseline geometry because the math shows it won't work as currently parameterized.

### 1. Mechanism viability under the gantry-only constraint

**The current cam-ramp baseline is critically flawed in two ways: it is statically unstable (an inverted pendulum) and kinematically uncontrollable (a snap-through singularity).**

*   **Fatal Flaw A: The Inverted Pendulum.** The README claims "gravity returns the trough... (a stable pendulum)". This is false for the current CAD parameters. The pivot pin is at `Y = -6.5 mm` (halfway down the trough). A full load of powder has a centroid at `Y = -5.52 mm` (higher up). Even worse, the two massive chamfered lips (`6×6×80 mm`) add 7.3 g of PETG *above* the rim. My calculation shows the combined loaded center of gravity is at `Y = -4.35 mm`, which is **2.15 mm ABOVE the pivot**. The trough is an inverted pendulum and will spontaneously flip open-side-down the moment the gantry moves.
*   **Fatal Flaw B: The Cam Singularity.** The cam ramp relies on a 16 mm lever arm (from pivot to the lip's outer edge) pushing against a 26.6° ramp. As the gantry pushes forward, the lip traces a circular arc. My kinematics model shows that at ~40° of tilt, the lever arm is nearly vertical. The sensitivity skyrockets to **86 degrees of tilt per mm of gantry travel**. This is a "snap-through" singularity; it is impossible to command a controlled metered pour with this geometry. Furthermore, the maximum vertical rise the lip can physically achieve is only ~9.5 mm, so the 20 mm `cam_ramp_rise` is wasted material.

**The Fix: The pin-in-slot variant (Panel E) is vastly superior and should be the baseline.**
The routed slot directly constrains the stem angle at every X coordinate. It eliminates the friction ambiguity, prevents the inverted pendulum from flipping during transport, and allows for a linear, programmable tilt schedule without the 86 deg/mm singularity. A compliant/spring-loaded lid is unnecessary complexity if the slot handles the kinematics.

### 2. Powder-handling realism

The longitudinal pivot / sideways tilt is a massive improvement over the end-over-end gondola (Edison v2 §3), as pouring over an 80 mm edge guarantees the powder won't bridge (arch spans for these powders are typically <10 mm).

*   **Retention:** For dozens-of-microns cohesive powders (TiO2, CaCO3), the FDM layer lines will act as anchor points. Vapour smoothing is mandatory to prevent a 10–20% hold-up mass. The "knock-to-debridge" oscillation (Edison v1 §6) is an excellent software-only feature, but it's much easier to execute with the pin-slot design (by coding a high-frequency zigzag into the slot path) than by trying to repeatedly ram a free-hanging bumper against a cam.
*   **Charging:** The brass pivot pin is already a perfect ground path. Lining the interior with copper tape (as you suggested) is the cheapest way to mitigate triboelectric charging on fine inorganics.
*   **Measurements:** You must measure dose CV (target ~10% to match Alsenz) and carryover mass (mg remaining after a knock cycle).

### 3. CAD geometry critique

Looking at `assembly-end.png` and `assembly-side.png`:

*   **Arm placement:** The arms drop from the gantry and end in a J-hook gripping the bosses. Because the pivot must be moved *up* toward the rim to fix the inverted pendulum, the arms will need to clear the trough's side walls as it rotates.
*   **Boss geometry:** The pivot bosses (`8 mm` diameter) sit on the end caps. The `arm_width` is also 8 mm. This is structurally fine, but the `pin_clearance` of `0.2 mm` diametral is too tight for FDM. It will fuse or bind. It needs to be 0.3–0.4 mm for a reliable sliding fit.
*   **Lip geometry:** The continuous `6×6 mm` chamfered lips run the full 80 mm length. As calculated above, they add 7.3 g of mass high above the pivot, ruining the pendulum stability. They are unnecessarily massive; a 2×2 mm lip would still provide a clean pour detachment point without destroying the mass distribution.

### 4. Closed-loop architecture and `dfm.py` shortfalls

The parametric pipeline (`cad/build.py` -> `dfm.py`) is a great start, but `dfm.py` is entirely missing the physics checks that would have caught the flaws above.

It currently checks 24 items (min wall, overhangs, basic slot/cam bounding boxes). **It falls short by only checking static geometry, not dynamic kinematics or statics.**

To fix the loop, `dfm.py` needs these automated checks added:
1.  **Pendulum stability:** `CG_loaded_y` must be < `pivot_y` (with a safety margin).
2.  **Cam sensitivity ceiling:** Calculate `d(theta)/d(X)` over the 0–45° range and fail if it exceeds ~15 deg/mm.
3.  **Cam rise utilization:** Check if `cam_ramp_rise` > `max_achievable_rise`.
4.  **Pin-slot friction:** Estimate the normal force on the peg based on the maximum curvature of the slot path.

### 5. Three concrete next experiments

Ranked by information value to derisk the design:

1.  **The "Pendulum Flip" and Pin-Slot Engagement Test.** Print the trough (with adjusted 2×2 mm lips), the arms, and a laser-cut or 3D-printed slot board (Panel E). Load it with 20 g of powder. Confirm that the slot prevents the inverted-pendulum flip during rapid X-transport, and verify that pure X-motion successfully walks the peg through the slot to achieve a 60°+ tilt without binding.
2.  **The Strike-Off vs. J-Curve Plunge Bake-off.** Print the bed-edge strike-off bar. Using a cohesive powder (e.g., TiO2 or flour), script the J-curve plunge. Scoop 30 times with the strike-off bar and 30 times without. Weigh each dose on a standard laboratory balance. If the strike-off doesn't cut the CV down to the ~10% range, the volumetric concept is dead for cohesive powders.
3.  **Carryover / Holdup Mass Test.** After the 30-scoop run, measure the mass of powder permanently retained in the trough. Test the software "knock" (oscillating the gantry rapidly in X while the peg is in a detent in the slot) to see if it meaningfully reduces the holdup mass compared to a single smooth pour.

---

**Discretionary Analytical Decisions:**
*   Computed trough mass properties assuming PETG with a density of 1.27 g/cm³ and a typical inorganic powder bulk density of 1.0 g/cm³.
*   Modelled the loaded center of gravity (CG) by treating the powder volume as a uniform solid half-disk (CG at 4r/3π from the flat edge) and the shell as a thin-walled half-cylinder.
*   Analysed the cam kinematics using small-angle geometric approximations of the lever arm's arc, defining the sensitivity singularity mathematically as the point where the tangent to the arc becomes vertical.
*   Selected 0.3–0.4 mm as the target FDM pin clearance based on standard desktop 3D printing tolerances rather than precision machining tolerances.
*   Assumed the pin-slot stem would be long enough to decouple minor Z-axis arc errors, modelling the mechanism as a rigid kinematic constraint.

```

=== file: docs/edison/literature-high-powder-dispensing.md ===
```md
Question: I am writing the Introduction to a Digital Discovery manuscript on a new low-cost, purely-mechanical powder dispenser for self-driving laboratories. The device ("powder excavator") is a gantry-mounted, elongated half-cylinder trough that is suspended between two vertical arms via a single horizontal pivot pin. Gravity keeps the trough level during pickup and transport. To deposit, the gantry pushes the trough sideways into a fixed wall-mounted sawtooth ledge; the hooked lip on the trough's upper long edge catches a tooth, and continued sideways gantry motion (the arms remaining vertical) applies a torque about the pin that rotates only the trough, pouring powder out at a controlled X coordinate. There are no actuators on the bucket. The intended target powders are dozens-of-microns-diameter inorganic powders (catalysts, ceramics, salts), some cohesive / electrostatically charged / prone to clumping. The device is positioned as a *bulk-transfer* tool that upstreams a precision dispenser, not as a competitor to one.

Please perform a high-effort literature search and synthesis covering:

1. The full landscape of automated and semi-automated powder/solids dispensing for chemistry and materials science. Cover commercial gravimetric vibratory-head dispensers (Mettler-Toledo Quantos, Chemspeed Powdernium / SWING / FLEX, Unchained Labs, Hamilton, Trajan, Thermo Fisher) with typical accuracy, dose ranges, and known failure modes on cohesive / hygroscopic / electrostatic powders.

2. Auger / screw-feed dispensers in autonomous chemistry and materials labs (MacLeod & Berlinguette's Ada thin-film SDL, Aspuru-Guzik group platforms, Cooper group's PowderBot, Ceder group's A-Lab, and others). Reported accuracy, throughput, hopper flow aids, cross-contamination.

3. Other modalities: positive-displacement-pipette solid dosing (Alsenz), 3D-printed calibrated spatulas (Cook et al. Nature Protocols), acoustic / non-contact solids dispensing, vacuum / electrostatic pickup, capsule / pre-weighed cartridge approaches, and trickler-style devices borrowed from the firearms reloading community (Autotrickler v4, OpenTrickler).

4. Bulk transfer of powder from stock containers into a precision dispenser, and the related "pick it back up" / recovery problem after ball milling or acoustic mixing. Published platforms that address this.

5. Powder-handling techniques borrowed from adjacent fields: directed-energy-deposition / powder-bed AM (Insstek's clogged vibration mechanism / blow disk), pharmaceutical continuous manufacturing (CMAC and similar), and standardised flowability characterisation (Freeman FT4, Carr index, Hausner ratio).

6. Benchmarks the community uses or should use to compare powder dispensers: dose CV across powder classes (free-flowing crystalline, cohesive nanopowder, hygroscopic salt), carryover/cross-contamination metrics, throughput, footprint, cost, and integration burden.

7. Explicit gaps where a cheap, gantry-mounted, actuator-free bucket-on-a-pin scoop+tip mechanism would (or would not) be useful, and prior art most directly comparable to this scoop-on-gantry geometry (Owen Melville's scoop, MTI PF-A glass dispenser, mreish's low-cost solid doser, Tourlomousis's biopolymer dispenser, etc.).

Please ground every claim in cited references, prefer peer-reviewed sources but include preprints and credible vendor documentation where peer-reviewed work is sparse. Output should be suitable for direct incorporation into the Introduction of a manuscript.

## Introduction: Automated Powder Dispensing for Self-Driving Laboratories — Landscape, Gaps, and the Case for a Low-Cost Mechanical Bulk-Transfer Tool

### 1. The Powder-Handling Bottleneck in Self-Driving Laboratories

Self-driving laboratories (SDLs) have emerged as transformative platforms for accelerating materials discovery, yet the handling and dispensing of dry powders remains one of the most persistent bottlenecks in closing the experimental loop (tom2024selfdrivinglaboratoriesfor pages 4-5). Unlike liquids, which can be metered with volumetric precision using mature syringe-pump and pipetting technologies, powders require real-time gravimetric measurement and contend with interparticle forces — van der Waals adhesion, electrostatic charging, and moisture-induced cohesion — that make automated transfer unreliable across the diverse material classes encountered in chemistry and materials science (yang2007meteringanddispensing pages 3-4, tom2024selfdrivinglaboratoriesfor pages 4-5). Consequently, many automated platforms avoid direct powder handling entirely, working instead from pre-dissolved stock solutions whenever possible (tom2024selfdrivinglaboratoriesfor pages 4-5). For solid-state synthesis of inorganic materials — catalysts, ceramics, battery precursors, and salts — dissolution is not an option, and robust powder dispensing is inescapable.

### 2. Commercial Gravimetric Vibratory-Head Dispensers

The most widely deployed commercial powder dispensers in high-throughput experimentation (HTE) are gravimetric systems from Mettler-Toledo (Quantos), Chemspeed (SWING, FLEX Powderdose), and Unchained Labs (Freeslate, Junior). A landmark collaborative evaluation by the Enabling Technologies Consortium tested these platforms across 17,797 dispenses using seven representative pharmaceutical powders at target masses of 2, 10, and 50 mg (bahr2018collaborativeevaluationof pages 2-3, bahr2018collaborativeevaluationof pages 3-5). All systems are gravity-fed and employ different agitation modes: Quantos uses rotary and tapping motion through consumable dosing heads with RFID-embedded learning algorithms; Chemspeed SWING/SDU uses rotary-action capillary (SWILE) heads available in three internal diameters (0.6, 1.0, 2.0 mm); and Unchained Labs systems employ tapping or vibratory heads with adaptive learning software (bahr2018collaborativeevaluationof pages 2-3, bahr2020recentadvancesin pages 2-3). Accuracy improved markedly with increasing target mass: dispenses at 2 mg exhibited 190–680% higher %RSD than those at 50 mg, and low-mass variability remained a critical gap (bahr2018collaborativeevaluationof pages 5-7). Across the full dataset, the % error range spanned −10% to +3,245%, with 95.3% of dispenses falling between −25% and +100% (bahr2018collaborativeevaluationof pages 7-8).

Platform-specific failure modes were well documented. Chemspeed SWING delivered the shortest dispense times (13–65 s) and excelled with dense, free-flowing powders such as sodium chloride, but experienced a large percentage of machine stalls that terminated runs and required researcher intervention (bahr2018collaborativeevaluationof pages 7-8, bahr2018collaborativeevaluationof pages 5-7). Attempts to dispense highly cohesive fumed silica on Chemspeed SWING and one Unchained system failed outright (bahr2018collaborativeevaluationof pages 2-3). Quantos offered the best overall balance of low % error, low %RSD, and moderate dispense time, but its consumable dosing heads can be abraded by hard particles and clogged by hygroscopic or deliquescent powders (bahr2018collaborativeevaluationof pages 7-8, carruthers2025amobilerobotic pages 115-119). A follow-up study evaluated newer-generation platforms including the Chemspeed FLEX GDU-Pfd (hopper/auger design with ±10% tolerance setting) and Mettler-Toledo CHRONECT, confirming the persistent gap in reliable sub-milligram dispensing and the strong dependence of accuracy on powder-specific parameter tuning (bahr2020recentadvancesin pages 2-3, bahr2020recentadvancesin pages 1-2).

### 3. Auger/Screw-Feed and Robotic Dispensers in Autonomous Synthesis Platforms

Several flagship SDLs have integrated powder dispensing into end-to-end autonomous workflows. The A-Lab at UC Berkeley, designed for accelerated solid-state synthesis of inorganic materials, uses a Quantos dispenser-balance to meter precursor powders (loaded manually in 50–100 g dosing bottles) into plastic vials, which are then mixed with ethanol and ZrO₂ milling media in a dual asymmetric centrifuge to form a slurry (szymanski2024automatingthesynthesis pages 78-80, szymanski2023anautonomouslaboratory pages 7-7). The slurry is pipetted by an automated pipettor into alumina crucibles for drying, furnace loading by a UR5e robot arm, and firing — a workflow that synthesised 36 novel compounds in 17 days of continuous operation, with a projected throughput of 100–200 samples per day (szymanski2023anautonomouslaboratory pages 7-7, mccalla2023semiautomatedexperimentsto pages 3-4). The A-Lab's strategy of converting dry powders to pumpable slurries elegantly sidesteps some last-mile dry-transfer difficulties, though it introduces ethanol handling, drying steps, and a dedicated powder-recovery (regrinding) task downstream (szymanski2024automatingthesynthesis pages 78-80, fei2024alabosapythonbased pages 20-25).

The Cooper group at Liverpool developed a dual-arm robotic manipulator ("PowderBot") that mimics the way a scientist uses a spatula and analytical balance (jiang2023autonomousbiomimeticsolid pages 2-3, jiang2023autonomousbiomimeticsolid pages 1-2). The system uses fuzzy-logic motion control to scoop powder with appropriately sized spatulas, deposit it onto a balance, and retry if the mass falls outside a tolerance window, achieving errors as low as 0.07% at a 200 mg target for non-challenging solids (jiang2023autonomousbiomimeticsolid pages 8-10). In a head-to-head comparison with Quantos and Chemspeed across 13 materials at 20–1000 mg, the dual-arm robot and Quantos dispensed a wider range of solids than Chemspeed, with average failure rates of 23.1%, 26.9%, and 26.5% respectively (jiang2023autonomousbiomimeticsolid pages 10-11). The dual-arm system's principal limitations are its slow throughput (due to manipulator motions and corrective restarts) and its struggles with compressible powders like CaCO₃ and highly hygroscopic materials (jiang2023autonomousbiomimeticsolid pages 10-11, jiang2023autonomousbiomimeticsolid pages 8-10). This modular robotic workflow was subsequently extended to an autonomous solid-state PXRD pipeline, illustrating how powder grinding, transfer, and sample loading are each discrete "last-mile" bottlenecks requiring dedicated robotic solutions (lunt2023modularmultirobotintegration pages 1-3).

### 4. Alternative and Emerging Dispensing Modalities

Beyond the dominant gravimetric paradigm, a diverse array of powder-dispensing mechanisms has been explored. Yang and Evans provided a comprehensive taxonomy, classifying methods as pneumatic/aspiration, volumetric (rotating-groove/piston), screw/auger, electrostatic, vibratory/acoustic, and piezoelectric drop-on-demand (yang2007meteringanddispensing pages 3-4, yang2007meteringanddispensing pages 4-6). Vacuum-aspiration powder pipettes achieved 5–25 mg doses at <2% error (yang2007meteringanddispensing pages 10-12), while ultrasonic capillary systems dispensed sub-milligram doses (minimum ~14–16 μg for tungsten carbide and glass beads through 0.2 mm nozzles) by pulsing piezoelectric excitation (yang2007meteringanddispensing pages 13-14, yang2007meteringanddispensing pages 9-10). Electrostatic approaches — including triboelectric charging, electrostatic valves, and automated electrostatic pipette tips — can handle masses as small as 0.3 mg but are exquisitely sensitive to humidity and charge-decay dynamics (yang2007meteringanddispensing pages 7-9).

At the low-cost end, Alsenz's PowderPicking technique uses standard Gilson MICROMAN positive-displacement pipettes with disposable capillary-piston tips to compact and transfer 0.6–25 mg of powder at an average CV of 6% across ten diverse drug and excipient powders (alsenz2011powderpickinganinexpensive pages 1-2, alsenz2011powderpickinganinexpensive pages 3-4). The method handles electrostatic, flyaway, and sticky powders better than loose-transfer approaches and uses disposable tips to eliminate cross-contamination, though it remains a manual, medium-throughput technique (alsenz2011powderpickinganinexpensive pages 4-5, alsenz2011powderpickinganinexpensive pages 5-6). Other handheld alternatives include the DryPette (vacuum pickup, 2–700 mg, SD <5% above 50 mg) and the Electronic Spatula (charged collector tips, down to 0.2 mg), each with limitations in access geometry and automation potential (alsenz2011powderpickinganinexpensive pages 4-5).

### 5. Bulk Transfer, Powder Recovery, and the "Last-Mile" Problem

A critical but underserved step in most SDL powder workflows is the bulk transfer of powder from stock containers into precision dispensers, and the recovery of product powder after thermal processing or mechanical mixing. The A-Lab addresses the former by manual loading of 50–100 g dosing bottles and the latter through a dedicated RecoverPowder regrinding task (szymanski2024automatingthesynthesis pages 78-80, fei2024alabosapythonbased pages 20-25). Lunt et al. noted that "grinding, mixing and recovering solids remains an unsolved challenge in commercial automation," with most commercial platforms built as stand-alone equipment manually integrated into workflows (lunt2024aroboticworkflow pages 11-16). Carruthers documented practical frustrations with the Quantos cartridge ecosystem — high cost, single-vendor procurement, embedded ID chips limiting reuse, clogging with hygroscopic powders, and fragile internal mechanisms damaged by hard particles such as titanium dioxide — all of which create handling bottlenecks and increase consumable costs (carruthers2025amobilerobotic pages 115-119). The comprehensive SDL review by Tom et al. emphasized that solid dispensing hardware remains rare and costly relative to liquid handling, and that many labs simply avoid direct powder manipulation (tom2024selfdrivinglaboratoriesfor pages 4-5). These observations collectively identify a gap for inexpensive, robust tools that can reliably scoop, transport, and deliver bulk quantities of powder — particularly cohesive, electrostatic, or clumping inorganic materials — without the consumable cost, vendor lock-in, or clogging vulnerabilities of precision dispensing heads.

### 6. Powder Handling in Adjacent Fields and Flowability Characterization

Insights from adjacent industries reinforce the difficulty of powder handling. In additive manufacturing, directed energy deposition (DED) systems rely on vibration-assisted and carrier-gas-coupled powder feeders, yet cohesive powders cause erratic flow, frequent clogging, and intermittent surges even with vibration and pneumatic assistance (yang2007meteringanddispensing pages 3-4, yang2007meteringanddispensing pages 6-7). The pharmaceutical continuous-manufacturing literature provides standardised flowability metrics: Carr's compressibility index (CI ≤ 10% = excellent flow; 21–25% = passable; >35% = very poor) and Hausner ratio (HR 1.00–1.11 = excellent; 1.26–1.34 = passable; >1.45 = poor) offer rapid, inexpensive screening of powder behaviour (moravkar2020traditionalandadvanced pages 2-3, ghoroi2013multifacetedcharacterizationof pages 2-3). For more discriminating characterisation, the Freeman FT4 Powder Rheometer measures dynamic flow energy by driving a twisted blade through a powder column under controlled conditions, capturing metrics such as basic flow energy (BFE) and specific energy (SE) that differentiate powders indistinguishable by Carr/Hausner alone (freeman2017characterisingpowderflow pages 2-3, moravkar2020traditionalandadvanced pages 9-10). Adopting such standardised flowability descriptors as benchmarks would improve comparability across powder-dispensing studies, which currently report accuracy in inconsistent formats.

### 7. Benchmarks and Metrics for Dispenser Evaluation

The community lacks a unified benchmarking framework for powder dispensers. The most systematic effort to date is the Enabling Technologies Consortium (ETC) evaluation, which reported % error, %RSD, dispense time, and run-retention rate across seven powders and four platforms (bahr2018collaborativeevaluationof pages 7-8, bahr2018collaborativeevaluationof pages 3-5, bahr2018collaborativeevaluationof pages 5-7). The Cooper group extended this to 13 solids and four target masses, adding per-material failure rate as a metric (jiang2023autonomousbiomimeticsolid pages 10-11, jiang2023autonomousbiomimeticsolid pages 10-10). Notably absent from published evaluations are standardised cross-contamination/carryover metrics, powder-class-stratified CV benchmarks (e.g., free-flowing crystalline vs. cohesive nanopowder vs. hygroscopic salt), footprint, cost-per-dispense, and integration burden (time to set up, clean, and change between powders). For a bulk-transfer tool like the proposed powder excavator, the relevant performance metrics would differ from those of a precision dispenser: mass-per-scoop repeatability, residual carryover after tipping, maximum fill fraction as a function of powder class, and time to complete a pickup–transport–deposit cycle would be more informative than sub-milligram accuracy benchmarks.

### 8. The Case for a Low-Cost, Actuator-Free Bulk-Transfer Tool

The landscape reviewed above reveals a clear stratification: precision gravimetric dispensers (Quantos, Chemspeed) deliver milligram-level accuracy but at high cost ($10K–$100K+), with consumable dependencies, clogging vulnerabilities, and a design philosophy centred on final-dose metering rather than bulk stock transfer (tom2024selfdrivinglaboratoriesfor pages 4-5, jiang2023autonomousbiomimeticsolid pages 1-2, tom2024selfdrivinglaboratoriesfor pages 5-6). Robotic spatula-based systems (Cooper group) offer versatility across material classes but are slow and require sophisticated dual-arm manipulators (jiang2023autonomousbiomimeticsolid pages 10-11, jiang2023autonomousbiomimeticsolid pages 8-10). Low-cost frugal alternatives such as open-hardware pellet dispensers and 3D-printed autosamplers have demonstrated that cost reductions of up to 94% relative to commercial analogues are achievable (hernandezdelvalle2024pelletdispensomixerand pages 2-3, doloi2025democratizingselfdrivinglabs pages 18-19), but these designs target liquid handling or pellet dispensing rather than bulk transfer of fine inorganic powders.

A purely mechanical, gantry-mounted powder excavator — an elongated half-cylinder trough suspended between vertical arms on a single horizontal pivot pin, with gravity maintaining a level orientation during pickup and transport, and a fixed wall-mounted sawtooth ledge providing the torque for controlled tipping — occupies a design niche that is, to the best of our knowledge, without direct precedent in the SDL literature or patent landscape. The closest prior art includes the Cooper group's spatula-scooping mechanism (jiang2023autonomousbiomimeticsolid pages 2-3), the A-Lab's manual bottle-loading step (szymanski2024automatingthesynthesis pages 78-80), and open-hardware pellet dispensomixers adapted from food-pellet dispensers (hernandezdelvalle2024pelletdispensomixerand pages 2-3). The proposed device contains no actuators, sensors, or consumable parts on the bucket itself, making it intrinsically low-cost, robust to abrasive or corrosive powders, and trivial to clean between materials. Its intended role is explicitly as a bulk-transfer tool upstream of a precision dispenser — scooping tens to hundreds of milligrams of powder from stock containers, transporting it via gantry motion, and depositing it at a controlled X coordinate — rather than as a competitor to gravimetric metering. This positioning addresses the documented gap in automated stock-to-dispenser transfer and post-processing powder recovery (lunt2023modularmultirobotintegration pages 1-3, carruthers2025amobilerobotic pages 115-119, lunt2024aroboticworkflow pages 11-16), while maintaining the cost and simplicity targets of the frugal-SDL movement (doloi2025democratizingselfdrivinglabs pages 18-19, tom2024selfdrivinglaboratoriesfor pages 5-6).

The following table summarises the landscape of automated powder-dispensing technologies and contextualises the proposed powder excavator within the broader field.

| Technology/Platform | Mechanism | Typical Dose Range | Accuracy/Precision | Key Limitations | Approximate Cost Class |
|---|---|---|---|---|---|
| Mettler-Toledo Quantos | Gravimetric dispensing with rotary/tapping vibratory dosing head and learning algorithm | 2–50 mg in ETC benchmark tests; 20–1000 mg in Jiang et al. comparison; commercial/use-case operation often extends into gram scale | In the ETC study, Quantos gave a strong balance of low % error, low %RSD, and short dispense time; accuracy improved markedly from 2 to 10 to 50 mg. In Jiang et al., many powders showed near-zero mean error, e.g. Al2O3 at 1000 mg: −0.02 ± 0.05% (bahr2018collaborativeevaluationof pages 7-8, bahr2018collaborativeevaluationof pages 3-5, bahr2018collaborativeevaluationof pages 5-7, jiang2023autonomousbiomimeticsolid pages 10-10) | Performance depends strongly on powder/head matching; difficult powders include very cohesive, compressible, hygroscopic, or deliquescent solids; abrasive solids can damage consumable heads; cartridge/head ecosystem increases integration burden (jiang2023autonomousbiomimeticsolid pages 10-10, jiang2023autonomousbiomimeticsolid pages 2-3, carruthers2025amobilerobotic pages 115-119) | High; commercial powder-dispensing hardware is typically in the expensive special-purpose SDL class rather than open-hardware class (tom2024selfdrivinglaboratoriesfor pages 4-5, tom2024selfdrivinglaboratoriesfor pages 5-6) |
| Chemspeed SWING/FLEX (GDU-S, GDU-Pfd) | Gravity-fed gravimetric dispensing using SWILE capillary heads and/or hopper–auger style GDU-Pfd modules with on-deck weighing | 2–50 mg in ETC/OPRD studies; 20–1000 mg in Jiang et al. comparison; heads available in 0.6, 1.0, and 2.0 mm IDs | Fastest commercial platform in ETC tests (13–65 s dispenses). Accuracy improved at higher target mass, but performance was powder-dependent; some rows in Jiang et al. show large negative bias or complete failures for difficult solids (bahr2018collaborativeevaluationof pages 7-8, bahr2020recentadvancesin pages 2-3, bahr2018collaborativeevaluationof pages 5-7, jiang2023autonomousbiomimeticsolid pages 10-10) | Large fraction of machine stalls; unsuccessful dispensing for highly cohesive powders such as fumed silica in benchmark tests; clogging and sensitivity to head geometry; some compressible solids completely failed (bahr2018collaborativeevaluationof pages 2-3, bahr2018collaborativeevaluationof pages 3-5, bahr2018collaborativeevaluationof pages 5-7, jiang2023autonomousbiomimeticsolid pages 10-10) | High (commercial integrated HTE platform) (tom2024selfdrivinglaboratoriesfor pages 4-5, tom2024selfdrivinglaboratoriesfor pages 5-6) |
| Unchained Labs (Freeslate/Junior vibratory heads) | Gravity-fed vibratory/tapping powder dispensing with adaptive learning | 2–50 mg in ETC benchmark | Delivered low % error and %RSD across several powders in the ETC study, but performance was strongly head- and environment-dependent; part of a 17,797-dispense evaluation (bahr2018collaborativeevaluationof pages 7-8, bahr2018collaborativeevaluationof pages 3-5) | Sensitive to dispense-head selection and user expertise; some systems failed on fumed silica; still subject to machine timeouts/stalls and low-mass variability (bahr2018collaborativeevaluationof pages 7-8, bahr2018collaborativeevaluationof pages 2-3, bahr2018collaborativeevaluationof pages 3-5) | High (commercial laboratory automation platform) (tom2024selfdrivinglaboratoriesfor pages 4-5, tom2024selfdrivinglaboratoriesfor pages 5-6) |
| Cooper group dual-arm robot (PowderBot; spatula-based) | Biomimetic dual-arm robot manipulates spatulas, funnels, vials, and balance to mimic manual scoop-and-weigh with restart logic | 20 mg to multiple grams; explicitly demonstrated at 20, 200, 500, and 1000 mg | For non-challenging solids at 200 mg, average error was ~0.07%; many 1000 mg cases were near zero error, e.g. Al2O3 0.06 ± 0.10%. More precise than Chemspeed for many benign powders, but slower (jiang2023autonomousbiomimeticsolid pages 8-10, jiang2023autonomousbiomimeticsolid pages 2-3, jiang2023autonomousbiomimeticsolid pages 10-10) | Slow throughput because of manipulator motions and corrective restarts; failures for compressible powders (e.g. CaCO3) and highly hygroscopic materials; occasional manipulation errors (jiang2023autonomousbiomimeticsolid pages 10-11, jiang2023autonomousbiomimeticsolid pages 8-10) | Medium to high, but positioned as significantly cheaper than most commercial solid dispensers (jiang2023autonomousbiomimeticsolid pages 1-2) |
| A-Lab (Quantos + slurry transfer) | Quantos dispenses precursor powder into vials; powders are ball-mixed with ethanol into slurry, then automatically pipetted into crucibles | Precursor bottles contain 50–100 g; individual dose range not reported in the cited workflow descriptions | No standalone dispensing accuracy reported for A-Lab in the cited workflow papers; the platform demonstrated end-to-end autonomous synthesis at >2 new materials per day and is described elsewhere as aiming for ~100–200 samples/day throughput (szymanski2024automatingthesynthesis pages 78-80, mccalla2023semiautomatedexperimentsto pages 3-4) | Avoids some last-mile dry-powder transfer issues by converting powder to slurry, but adds ethanol handling, drying, and recovery steps; upstream powder loading is still manual; recovery/regrinding remains a dedicated task (szymanski2024automatingthesynthesis pages 78-80, szymanski2023anautonomouslaboratory pages 7-7, fei2024alabosapythonbased pages 20-25) | Very high/infrastructure scale autonomous laboratory (tom2024selfdrivinglaboratoriesfor pages 4-5, szymanski2024automatingthesynthesis pages 78-80, mccalla2023semiautomatedexperimentsto pages 3-4) |
| PowderPicking (Alsenz) | Positive-displacement pipette tip compacts and transfers powder volumetrically from a compacted powder bed | ~0.6–25 mg per dispense; larger totals achievable by repeated dispenses | Average CV across ten powders was ~6%; worst case ~10% CV at smallest tip/lowest setting, best ~3.5% CV at largest tip/highest setting (alsenz2011powderpickinganinexpensive pages 1-2, alsenz2011powderpickinganinexpensive pages 3-4) | Manual/semi-automated rather than fully autonomous; performance depends on complete homogeneous filling of the probe cylinder; tip clogging with adhesive powders and particle dropout with coarse granules; not ideal for one-off high-accuracy analytical dosing (alsenz2011powderpickinganinexpensive pages 3-4, alsenz2011powderpickinganinexpensive pages 4-5, alsenz2011powderpickinganinexpensive pages 5-6) | Low (inexpensive manual/frugal method using standard pipettes and disposable tips) (alsenz2011powderpickinganinexpensive pages 1-2, alsenz2011powderpickinganinexpensive pages 5-6) |
| Acoustic/ultrasonic powder dispensing | Powder mobilized in capillaries/nozzles by acoustic or ultrasonic vibration; can provide on/off switching and fine metering | From ~0.1 mg down to tens of micrograms in selected systems; examples include 14–16 μg minima in 0.2 mm nozzles and ~10 μg s−1 flow regimes | Highly powder- and geometry-dependent; literature examples include fine resolution and pulsed dosing but mostly in specialized freeforming/AM contexts rather than chemistry SDLs (yang2007meteringanddispensing pages 13-14, yang2007meteringanddispensing pages 9-10) | Specialized hardware; strong dependence on particle size, capillary/nozzle ratio, waveform, and vibration amplitude; not a common chemistry-lab product; may trade simplicity and throughput for resolution (yang2007meteringanddispensing pages 13-14, yang2007meteringanddispensing pages 9-10, yang2007meteringanddispensing pages 7-9) | Medium to high for bespoke systems; not widely available as routine chemistry SDL hardware (tom2024selfdrivinglaboratoriesfor pages 4-5) |
| Electrostatic pickup/dispensing | Pickup and release by triboelectric charging, electrostatic valves, electrostatic pipettes, or latent-image development | Broad literature range from ~0.3 mg electrostatic pipette dispensing to 2 μg–50 mg zonal deposition in patterning systems | Can achieve high spatial precision and low masses in specialized systems; examples include automated electrostatic pipette tips dispensing ~0.3 mg with high accuracy (yang2007meteringanddispensing pages 7-9) | Extremely sensitive to humidity, charge decay, powder conductivity, clustering, and surface interactions; generally specialized and not general-purpose for routine inorganic SDL bulk transfer (yang2007meteringanddispensing pages 6-7, yang2007meteringanddispensing pages 7-9, yang2007meteringanddispensing pages 3-4) | Medium to high for bespoke instruments; uncommon in standard chemistry SDLs (tom2024selfdrivinglaboratoriesfor pages 4-5) |
| Vacuum aspiration / powder pipette | Partial-vacuum pickup from powder bed followed by pneumatic ejection or air-assisted release | ~0.5–10 mg in aspiration devices; robotic powder pipettes achieved ~5–25 mg | Robotic powder pipettes in the Yang & Evans review achieved 5–25 mg at <2% error (yang2007meteringanddispensing pages 10-12, yang2007meteringanddispensing pages 4-6) | Requires careful control of vacuum, airflow, and particle entrainment; pickup can be inconsistent for cohesive or electrostatic powders; more suited to small-dose transfer than bulk refill operations (yang2007meteringanddispensing pages 10-12, yang2007meteringanddispensing pages 4-6) | Medium for bespoke lab devices; limited commercial penetration in chemistry SDLs (tom2024selfdrivinglaboratoriesfor pages 4-5) |
| Proposed Powder Excavator (gantry-mounted trough) | Purely mechanical scoop-and-tip: gravity-leveled pivoted trough excavates bulk powder, transports on a gantry, then tips against a fixed sawtooth ledge at the target X coordinate | Intended for bulk transfer rather than precision final dosing; practical range would likely be tens of milligrams to grams depending on trough geometry and powder fill, but this remains to be experimentally established | Precision should be evaluated as upstream bulk-transfer repeatability rather than final analytical-dose accuracy; no published benchmark data yet | Likely strong value as a cheap upstream loader or recovery tool for powders that clog precision heads or are awkward to recover after mixing/milling, but likely unsuitable as a direct competitor to high-precision gravimetric dispensers for sub-10 mg dosing. Performance risks include fill variability, adhesion/carryover, poor emptying of cohesive powders, and dependence on powder flowability/class (yang2007meteringanddispensing pages 3-4, lunt2023modularmultirobotintegration pages 1-3, lunt2024aroboticworkflow pages 11-16, alsenz2011powderpickinganinexpensive pages 4-5) | Low to medium; conceptually aligned with frugal/open-hardware SDL hardware rather than proprietary special-purpose dispensing systems (hernandezdelvalle2024pelletdispensomixerand pages 2-3, doloi2025democratizingselfdrivinglabs pages 18-19, tom2024selfdrivinglaboratoriesfor pages 5-6) |


*Table: This table compares major powder-dispensing modalities relevant to chemistry and materials-science self-driving laboratories, spanning commercial gravimetric systems, robotic/manual alternatives, and literature mechanisms. It is useful for positioning the proposed Powder Excavator as a low-cost bulk-transfer tool upstream of precision dispensers rather than as a direct replacement.*

In the remainder of this work, we describe the design, fabrication, and characterisation of the powder excavator, benchmarking its performance across representative powder classes (free-flowing crystalline, cohesive micron-scale, and hygroscopic salts) using standardised flowability descriptors and evaluating its suitability as a bulk-transfer front-end for precision dispensing in self-driving solid-state synthesis workflows.

References

1. (tom2024selfdrivinglaboratoriesfor pages 4-5): Gary Tom, Stefan P. Schmid, Sterling G. Baird, Yang Cao, Kourosh Darvish, Han Hao, Stanley Lo, Sergio Pablo-García, Ella M. Rajaonson, Marta Skreta, Naruki Yoshikawa, Samantha Corapi, Gun Deniz Akkoc, Felix Strieth-Kalthoff, Martin Seifrid, and Alán Aspuru-Guzik. Self-driving laboratories for chemistry and materials science. Chemical Reviews, 124:9633-9732, Aug 2024. URL: https://doi.org/10.1021/acs.chemrev.4c00055, doi:10.1021/acs.chemrev.4c00055. This article has 638 citations and is from a highest quality peer-reviewed journal.

2. (yang2007meteringanddispensing pages 3-4): Shoufeng Yang and Jrg Evans. Metering and dispensing of powder; the quest for new solid freeforming techniques. Powder Technology, 178:56-72, Sep 2007. URL: https://doi.org/10.1016/j.powtec.2007.04.004, doi:10.1016/j.powtec.2007.04.004. This article has 199 citations and is from a domain leading peer-reviewed journal.

3. (bahr2018collaborativeevaluationof pages 2-3): Matthew N. Bahr, David B. Damon, Simon D. Yates, Alexander S. Chin, J. David Christopher, Samuel Cromer, Nicholas Perrotto, Jorge Quiroz, and Victor Rosso. Collaborative evaluation of commercially available automated powder dispensing platforms for high-throughput experimentation in pharmaceutical applications. Organic Process Research & Development, 22:1500-1508, Oct 2018. URL: https://doi.org/10.1021/acs.oprd.8b00259, doi:10.1021/acs.oprd.8b00259. This article has 62 citations and is from a peer-reviewed journal.

4. (bahr2018collaborativeevaluationof pages 3-5): Matthew N. Bahr, David B. Damon, Simon D. Yates, Alexander S. Chin, J. David Christopher, Samuel Cromer, Nicholas Perrotto, Jorge Quiroz, and Victor Rosso. Collaborative evaluation of commercially available automated powder dispensing platforms for high-throughput experimentation in pharmaceutical applications. Organic Process Research & Development, 22:1500-1508, Oct 2018. URL: https://doi.org/10.1021/acs.oprd.8b00259, doi:10.1021/acs.oprd.8b00259. This article has 62 citations and is from a peer-reviewed journal.

5. (bahr2020recentadvancesin pages 2-3): Matthew N. Bahr, Mark A. Morris, Noah P. Tu, and Aakankschit Nandkeolyar. Recent advances in high-throughput automated powder dispensing platforms for pharmaceutical applications. Organic Process Research & Development, 24:2752-2761, Oct 2020. URL: https://doi.org/10.1021/acs.oprd.0c00411, doi:10.1021/acs.oprd.0c00411. This article has 55 citations and is from a peer-reviewed journal.

6. (bahr2018collaborativeevaluationof pages 5-7): Matthew N. Bahr, David B. Damon, Simon D. Yates, Alexander S. Chin, J. David Christopher, Samuel Cromer, Nicholas Perrotto, Jorge Quiroz, and Victor Rosso. Collaborative evaluation of commercially available automated powder dispensing platforms for high-throughput experimentation in pharmaceutical applications. Organic Process Research & Development, 22:1500-1508, Oct 2018. URL: https://doi.org/10.1021/acs.oprd.8b00259, doi:10.1021/acs.oprd.8b00259. This article has 62 citations and is from a peer-reviewed journal.

7. (bahr2018collaborativeevaluationof pages 7-8): Matthew N. Bahr, David B. Damon, Simon D. Yates, Alexander S. Chin, J. David Christopher, Samuel Cromer, Nicholas Perrotto, Jorge Quiroz, and Victor Rosso. Collaborative evaluation of commercially available automated powder dispensing platforms for high-throughput experimentation in pharmaceutical applications. Organic Process Research & Development, 22:1500-1508, Oct 2018. URL: https://doi.org/10.1021/acs.oprd.8b00259, doi:10.1021/acs.oprd.8b00259. This article has 62 citations and is from a peer-reviewed journal.

8. (carruthers2025amobilerobotic pages 115-119): S Carruthers. A mobile robotic researcher for autonomous solar fuels research. Unknown journal, 2025.

9. (bahr2020recentadvancesin pages 1-2): Matthew N. Bahr, Mark A. Morris, Noah P. Tu, and Aakankschit Nandkeolyar. Recent advances in high-throughput automated powder dispensing platforms for pharmaceutical applications. Organic Process Research & Development, 24:2752-2761, Oct 2020. URL: https://doi.org/10.1021/acs.oprd.0c00411, doi:10.1021/acs.oprd.0c00411. This article has 55 citations and is from a peer-reviewed journal.

10. (szymanski2024automatingthesynthesis pages 78-80): N Szymanski. Automating the synthesis and characterization of inorganic materials. Unknown journal, 2024.

11. (szymanski2023anautonomouslaboratory pages 7-7): Nathan J. Szymanski, Bernardus Rendy, Yuxing Fei, Rishi E. Kumar, Tanjin He, David Milsted, Matthew J. McDermott, Max Gallant, Ekin Dogus Cubuk, Amil Merchant, Haegyeom Kim, Anubhav Jain, Christopher J. Bartel, Kristin Persson, Yan Zeng, and Gerbrand Ceder. An autonomous laboratory for the accelerated synthesis of inorganic materials. Nature, 624:86-91, Nov 2023. URL: https://doi.org/10.1038/s41586-023-06734-w, doi:10.1038/s41586-023-06734-w. This article has 1090 citations and is from a highest quality peer-reviewed journal.

12. (mccalla2023semiautomatedexperimentsto pages 3-4): Eric McCalla. Semiautomated experiments to accelerate the design of advanced battery materials: combining speed, low cost, and adaptability. ACS Engineering Au, 3:391-402, Nov 2023. URL: https://doi.org/10.1021/acsengineeringau.3c00037, doi:10.1021/acsengineeringau.3c00037. This article has 21 citations and is from a peer-reviewed journal.

13. (fei2024alabosapythonbased pages 20-25): Yuxing Fei, Bernardus Rendy, Rishi Kumar, Olympia Dartsi, Hrushikesh P. Sahasrabuddhe, Matthew J. McDermott, Zheren Wang, Nathan J. Szymanski, Lauren N. Walters, David Milsted, Yan Zeng, Anubhav Jain, and Gerbrand Ceder. Alabos: a python-based reconfigurable workflow management framework for autonomous laboratories. ArXiv, May 2024. URL: https://doi.org/10.48550/arxiv.2405.13930, doi:10.48550/arxiv.2405.13930. This article has 41 citations.

14. (jiang2023autonomousbiomimeticsolid pages 2-3): Ying Jiang, Hatem Fakhruldeen, Gabriella Pizzuto, Louis Longley, Ai He, Tianwei Dai, Rob Clowes, Nicola Rankin, and Andrew I. Cooper. Autonomous biomimetic solid dispensing using a dual-arm robotic manipulator. Digital Discovery, 2:1733-1744, Jan 2023. URL: https://doi.org/10.1039/d3dd00075c, doi:10.1039/d3dd00075c. This article has 58 citations and is from a peer-reviewed journal.

15. (jiang2023autonomousbiomimeticsolid pages 1-2): Ying Jiang, Hatem Fakhruldeen, Gabriella Pizzuto, Louis Longley, Ai He, Tianwei Dai, Rob Clowes, Nicola Rankin, and Andrew I. Cooper. Autonomous biomimetic solid dispensing using a dual-arm robotic manipulator. Digital Discovery, 2:1733-1744, Jan 2023. URL: https://doi.org/10.1039/d3dd00075c, doi:10.1039/d3dd00075c. This article has 58 citations and is from a peer-reviewed journal.

16. (jiang2023autonomousbiomimeticsolid pages 8-10): Ying Jiang, Hatem Fakhruldeen, Gabriella Pizzuto, Louis Longley, Ai He, Tianwei Dai, Rob Clowes, Nicola Rankin, and Andrew I. Cooper. Autonomous biomimetic solid dispensing using a dual-arm robotic manipulator. Digital Discovery, 2:1733-1744, Jan 2023. URL: https://doi.org/10.1039/d3dd00075c, doi:10.1039/d3dd00075c. This article has 58 citations and is from a peer-reviewed journal.

17. (jiang2023autonomousbiomimeticsolid pages 10-11): Ying Jiang, Hatem Fakhruldeen, Gabriella Pizzuto, Louis Longley, Ai He, Tianwei Dai, Rob Clowes, Nicola Rankin, and Andrew I. Cooper. Autonomous biomimetic solid dispensing using a dual-arm robotic manipulator. Digital Discovery, 2:1733-1744, Jan 2023. URL: https://doi.org/10.1039/d3dd00075c, doi:10.1039/d3dd00075c. This article has 58 citations and is from a peer-reviewed journal.

18. (lunt2023modularmultirobotintegration pages 1-3): Amy. M. Lunt, Hatem Fakhruldeen, Gabriella Pizzuto, Louis Longley, Alexander White, Nicola Rankin, Rob Clowes, Ben Alston, Lucia Gigli, Graeme M. Day, Andrew I. Cooper, and Sam. Y. Chong. Modular, multi-robot integration of laboratories: an autonomous solid-state workflow for powder x-ray diffraction. Preprint, Jan 2023. URL: https://doi.org/10.48550/arxiv.2309.00544, doi:10.48550/arxiv.2309.00544. This article has 1 citations.

19. (yang2007meteringanddispensing pages 4-6): Shoufeng Yang and Jrg Evans. Metering and dispensing of powder; the quest for new solid freeforming techniques. Powder Technology, 178:56-72, Sep 2007. URL: https://doi.org/10.1016/j.powtec.2007.04.004, doi:10.1016/j.powtec.2007.04.004. This article has 199 citations and is from a domain leading peer-reviewed journal.

20. (yang2007meteringanddispensing pages 10-12): Shoufeng Yang and Jrg Evans. Metering and dispensing of powder; the quest for new solid freeforming techniques. Powder Technology, 178:56-72, Sep 2007. URL: https://doi.org/10.1016/j.powtec.2007.04.004, doi:10.1016/j.powtec.2007.04.004. This article has 199 citations and is from a domain leading peer-reviewed journal.

21. (yang2007meteringanddispensing pages 13-14): Shoufeng Yang and Jrg Evans. Metering and dispensing of powder; the quest for new solid freeforming techniques. Powder Technology, 178:56-72, Sep 2007. URL: https://doi.org/10.1016/j.powtec.2007.04.004, doi:10.1016/j.powtec.2007.04.004. This article has 199 citations and is from a domain leading peer-reviewed journal.

22. (yang2007meteringanddispensing pages 9-10): Shoufeng Yang and Jrg Evans. Metering and dispensing of powder; the quest for new solid freeforming techniques. Powder Technology, 178:56-72, Sep 2007. URL: https://doi.org/10.1016/j.powtec.2007.04.004, doi:10.1016/j.powtec.2007.04.004. This article has 199 citations and is from a domain leading peer-reviewed journal.

23. (yang2007meteringanddispensing pages 7-9): Shoufeng Yang and Jrg Evans. Metering and dispensing of powder; the quest for new solid freeforming techniques. Powder Technology, 178:56-72, Sep 2007. URL: https://doi.org/10.1016/j.powtec.2007.04.004, doi:10.1016/j.powtec.2007.04.004. This article has 199 citations and is from a domain leading peer-reviewed journal.

24. (alsenz2011powderpickinganinexpensive pages 1-2): Jochem Alsenz. Powderpicking: an inexpensive, manual, medium-throughput method for powder dispensing. Powder Technology, 209:152-157, May 2011. URL: https://doi.org/10.1016/j.powtec.2011.02.014, doi:10.1016/j.powtec.2011.02.014. This article has 16 citations and is from a domain leading peer-reviewed journal.

25. (alsenz2011powderpickinganinexpensive pages 3-4): Jochem Alsenz. Powderpicking: an inexpensive, manual, medium-throughput method for powder dispensing. Powder Technology, 209:152-157, May 2011. URL: https://doi.org/10.1016/j.powtec.2011.02.014, doi:10.1016/j.powtec.2011.02.014. This article has 16 citations and is from a domain leading peer-reviewed journal.

26. (alsenz2011powderpickinganinexpensive pages 4-5): Jochem Alsenz. Powderpicking: an inexpensive, manual, medium-throughput method for powder dispensing. Powder Technology, 209:152-157, May 2011. URL: https://doi.org/10.1016/j.powtec.2011.02.014, doi:10.1016/j.powtec.2011.02.014. This article has 16 citations and is from a domain leading peer-reviewed journal.

27. (alsenz2011powderpickinganinexpensive pages 5-6): Jochem Alsenz. Powderpicking: an inexpensive, manual, medium-throughput method for powder dispensing. Powder Technology, 209:152-157, May 2011. URL: https://doi.org/10.1016/j.powtec.2011.02.014, doi:10.1016/j.powtec.2011.02.014. This article has 16 citations and is from a domain leading peer-reviewed journal.

28. (lunt2024aroboticworkflow pages 11-16): Amy Lunt. A robotic workflow to screen crystal forms using powder x-ray diffraction. Text, Jan 2024. URL: https://doi.org/10.17638/03178518, doi:10.17638/03178518. This article has 0 citations and is from a peer-reviewed journal.

29. (yang2007meteringanddispensing pages 6-7): Shoufeng Yang and Jrg Evans. Metering and dispensing of powder; the quest for new solid freeforming techniques. Powder Technology, 178:56-72, Sep 2007. URL: https://doi.org/10.1016/j.powtec.2007.04.004, doi:10.1016/j.powtec.2007.04.004. This article has 199 citations and is from a domain leading peer-reviewed journal.

30. (moravkar2020traditionalandadvanced pages 2-3): K. K. MORAVKAR, S. D. KORDE, B. A. BHAIRAV, S. B. SHINDE, S. V. KAKULADE, and S. S. CHALIKWAR. Traditional and advanced flow characterization techniques: a platform review for development of solid dosage form. Indian Journal of Pharmaceutical Sciences, Jan 2020. URL: https://doi.org/10.36468/pharmaceutical-sciences.726, doi:10.36468/pharmaceutical-sciences.726. This article has 34 citations.

31. (ghoroi2013multifacetedcharacterizationof pages 2-3): Chinmay Ghoroi, Lakxmi Gurumurthy, D.J. McDaniel, Laila J. Jallo, and Rajesh N. Davé. Multi-faceted characterization of pharmaceutical powders to discern the influence of surface modification. Powder Technology, 236:63-74, Feb 2013. URL: https://doi.org/10.1016/j.powtec.2012.05.039, doi:10.1016/j.powtec.2012.05.039. This article has 94 citations and is from a domain leading peer-reviewed journal.

32. (freeman2017characterisingpowderflow pages 2-3): T Freeman and K Brockbank. Characterising powder flow properties–the need for a multivariate approach. Unknown journal, 2017.

33. (moravkar2020traditionalandadvanced pages 9-10): K. K. MORAVKAR, S. D. KORDE, B. A. BHAIRAV, S. B. SHINDE, S. V. KAKULADE, and S. S. CHALIKWAR. Traditional and advanced flow characterization techniques: a platform review for development of solid dosage form. Indian Journal of Pharmaceutical Sciences, Jan 2020. URL: https://doi.org/10.36468/pharmaceutical-sciences.726, doi:10.36468/pharmaceutical-sciences.726. This article has 34 citations.

34. (jiang2023autonomousbiomimeticsolid pages 10-10): Ying Jiang, Hatem Fakhruldeen, Gabriella Pizzuto, Louis Longley, Ai He, Tianwei Dai, Rob Clowes, Nicola Rankin, and Andrew I. Cooper. Autonomous biomimetic solid dispensing using a dual-arm robotic manipulator. Digital Discovery, 2:1733-1744, Jan 2023. URL: https://doi.org/10.1039/d3dd00075c, doi:10.1039/d3dd00075c. This article has 58 citations and is from a peer-reviewed journal.

35. (tom2024selfdrivinglaboratoriesfor pages 5-6): Gary Tom, Stefan P. Schmid, Sterling G. Baird, Yang Cao, Kourosh Darvish, Han Hao, Stanley Lo, Sergio Pablo-García, Ella M. Rajaonson, Marta Skreta, Naruki Yoshikawa, Samantha Corapi, Gun Deniz Akkoc, Felix Strieth-Kalthoff, Martin Seifrid, and Alán Aspuru-Guzik. Self-driving laboratories for chemistry and materials science. Chemical Reviews, 124:9633-9732, Aug 2024. URL: https://doi.org/10.1021/acs.chemrev.4c00055, doi:10.1021/acs.chemrev.4c00055. This article has 638 citations and is from a highest quality peer-reviewed journal.

36. (hernandezdelvalle2024pelletdispensomixerand pages 2-3): Miguel Hernández-del-Valle, Jorge Ilarraza-Zuazo, Enrique Dios-Lázaro, Javier Rubio, Joris Audoux, and Maciej Haranczyk. Pellet dispensomixer and pellet distributor: open hardware for nanocomposite space exploration via automated material compounding. Digital Discovery, Jul 2024. URL: https://doi.org/10.1039/d4dd00198b, doi:10.1039/d4dd00198b. This article has 1 citations and is from a peer-reviewed journal.

37. (doloi2025democratizingselfdrivinglabs pages 18-19): Sayan Doloi, Maloy Das, Yujia Li, Zen Han Cho, Xingchi Xiao, John V. Hanna, Matthew Osvaldo, and Leonard Ng Wei Tat. Democratizing self-driving labs: advances in low-cost 3d printing for laboratory automation. Digital Discovery, 4:1685-1721, Jan 2025. URL: https://doi.org/10.1039/d4dd00411f, doi:10.1039/d4dd00411f. This article has 27 citations and is from a peer-reviewed journal.

```

=== file: scripts/edison_submit.py ===
````py
"""Submit and poll Edison Scientific tasks via the edisonscientific endpoint.

The Edison Platform is reached at ``https://api.platform.edisonscientific.com``
(NOT ``https://api.platform.futurehouse.org`` -- that's the public FutureHouse
endpoint, which is different infrastructure with different access controls).
We re-use the open-source ``futurehouse-client`` SDK because it speaks the
same protocol, but every constructor here pins ``service_uri`` to the Edison
host so we can't accidentally talk to the wrong cluster.

Authentication is via the ``EDISON_API_KEY`` environment variable.

Usage examples (run from the repo root):

    # Submit a fresh literature-deep query (paperqa3-high) for generative-CAD
    python scripts/edison_submit.py submit-cad-litreview

    # Submit one iteration of the analysis feedback cycle bundling the design
    # context (README, manuscript, prior analyses, CAD) inline into the query
    python scripts/edison_submit.py submit-analysis 1

    # Poll a previously-submitted task and dump its formatted answer
    python scripts/edison_submit.py poll <task_id>
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
from pathlib import Path

from futurehouse_client import FutureHouseClient, TaskRequest
from futurehouse_client.models.app import RuntimeConfig

# The Edison Scientific platform endpoint. This is the canonical answer to
# "you're using futurehouse, should be using edisonscientific" -- the SDK
# defaults to FutureHouse PROD, so we override.
EDISON_SERVICE_URI = "https://api.platform.edisonscientific.com"

# Edison job names (the SDK's JobNames enum points at older paperqa2 names;
# Edison exposes the paperqa3 family + the data-analysis-crow-high job).
JOB_LITERATURE_HIGH = "job-futurehouse-paperqa3-high"
JOB_ANALYSIS = "job-futurehouse-data-analysis-crow-high"

REPO_ROOT = Path(__file__).resolve().parent.parent

# Files we embed inline (as fenced text blocks) into every analysis iteration
# so Edison sees the full design context without depending on the chunked
# upload endpoint, which currently 404s on the Edison cluster. Total payload
# is ~135 KB -- well within reasonable query size.
CONTEXT_TEXT_FILES: tuple[Path, ...] = (
    REPO_ROOT / "README.md",
    REPO_ROOT / "docs" / "manuscript" / "main.tex",
    REPO_ROOT / "docs" / "edison" / "analysis-v2-corrected-gondola.md",
    REPO_ROOT / "cad" / "README.md",
    REPO_ROOT / "cad" / "excavator.py",
    REPO_ROOT / "cad" / "dfm.py",
)

# Common framing for every iteration of the analysis feedback cycle. The
# gantry-only constraint (no second axis on the bucket) is the load-bearing
# requirement from PR comment 4166621470.
ANALYSIS_PREAMBLE = """\
You are reviewing the powder-excavator project, an open-source bulk powder
dispenser intended to feed a downstream precision gravimetric dispenser inside
a self-driving lab. **Hard constraint:** the entire dispensing motion must be
achievable on a 3-axis gantry (X, Y, Z) -- *no* second actuator on the bucket
itself. All trough rotation / scoop opening / closing must come from passive
mechanical interaction with fixed external features (cam ramps, routed slots,
fixed posts, compliant flexures, etc.) driven by gantry motion alone.

Target powders are dozens of microns in diameter, often cohesive,
hygroscopic, or triboelectrically charged. Manufacturing target is FDM 3D
printing in PETG / nylon / ESD-safe filament with stock dowel-pin pivots.

The full design context (README, LaTeX manuscript, prior Edison analyses,
and the CadQuery parametric model with its DFM checks) is embedded inline
below as fenced code blocks.
"""

ITERATION_PROMPTS = {
    1: """\
**Iteration 1 of 3 -- gantry-only baseline review.**

Given the gantry-only constraint above, please:

1. Identify every place in the current design where the mechanism implicitly
   assumes a second actuator on the bucket and propose a gantry-only
   substitute (cam, slot, compliant bistable mechanism, OT-2-style tip-eject,
   pipette-displacement-driven suction, etc.).
2. Compare the smooth-cam-ramp variant (Panel D) and the routed-slot variant
   (Panel E) for: kinematic determinism, bidirectional return, robustness to
   powder build-up on the cam/slot, and additive-manufacturing complexity.
3. Critique the bimodal scoop suggestion from PR comment 3134394694
   ("scoop position" vs "hold/don't leak position", potentially actuated by
   OT-2 tip-eject style drop or pipette-suction). Is a single passive
   bistable flexure (compliant mechanism) achievable on a 3-axis gantry, or
   does it always require a second axis?
4. Propose three concrete experimental measurements (mass CV, dose-recovery,
   bridging frequency) that would discriminate between the cam-ramp,
   pin-slot, and bistable variants.
5. Recommend an open, pip-installable feedback-loop toolchain that hooks the
   CadQuery parametric model into a measure-and-re-design loop on a Jubilee
   or OpenTrons rig.
""",
    2: """\
**Iteration 2 of 3 -- refinement based on Iteration 1.**

Building on Iteration 1's gantry-only critique (whose verbatim answer will
be embedded below as `analysis-iter1.md`):

1. Pick the single strongest gantry-only actuation strategy from Iteration 1
   and design it in detail: dimensions, materials, tolerances, expected dose
   range, expected CV, failure modes.
2. Identify the 2-3 highest-risk geometric parameters (e.g. bumper chamfer
   angle, slot waypoint spacing, flexure thickness) and propose a
   one-factor-at-a-time sweep that the CadQuery model + Bayesian optimisation
   loop could run.
3. Specify the closed-loop digital-twin instrumentation needed (load cell,
   camera, encoder feedback) and how each measurement would feed back into
   the next CadQuery parameter update.
""",
    3: """\
**Iteration 3 of 3 -- concrete decision and build plan.**

Building on Iterations 1 and 2 (whose verbatim answers will be embedded
below as `analysis-iter1.md` and `analysis-iter2.md`):

1. Recommend a single design to take to first prototype, with a justification
   that explicitly addresses why each rejected variant was rejected.
2. Provide a 5-step build-and-test plan for that prototype (print, assemble,
   instrument, calibrate, characterise) with go/no-go criteria at each step.
3. List the additions / changes that should be made to the manuscript
   (`docs/manuscript/main.tex`) to reflect the chosen design and to defend
   the gantry-only-no-second-axis claim.
4. List the parameters in `cad/excavator.py::ExcavatorParams` that need to
   change to match the chosen design.
""",
}

CAD_LITREVIEW_QUERY = """\
We are designing the actuation and feedback loop for an open-hardware powder
dispenser ("powder-excavator") that must run on a 3-axis gantry with no
second axis on the bucket. The bucket's tilt schedule is therefore programmed
purely by passive mechanical interaction with fixed external features
(cam ramps, routed slots, compliant flexures, OT-2-style tip-ejection,
pipette-displacement-driven suction, etc.) driven by gantry motion alone.

Please synthesise the state of the art across two linked topics, with a
preference for **open and pip-installable** tools (we are using CadQuery as
the parametric authoring layer) and citing peer-reviewed work where possible:

1. **Generative / computational CAD and systems design for mechanical
   hardware**: parametric / algorithmic CAD ecosystems (CadQuery, build123d,
   OpenSCAD, Rhino + Grasshopper + Rhino.Inside, Onshape FeatureScript, Zoo
   Design Studio / KCL); generative / AI-assisted geometry (nTop, Fusion
   Generative Design, DeepCAD, Text2CAD / CAD-LLM, BrepGen, CAD-Recode,
   Shap-E / TRELLIS); systems-design / requirements-driven approaches (SysML
   v2, OpenMDAO, Bayesian-optimisation design loops); and automated DFM /
   printability checks (slicer-side, DFMPro, Castor). Comparative table where
   tools fight in the same niche.

2. **Automated feedback loops and digital-twin-style evaluation for
   mechanical hardware prototypes**: twin maturity (Kritzinger / Tao /
   Grieves), AM-specific twins (NIST AM-Bench, Eclipse Ditto, ROS2 + Gazebo /
   Ignition), closed-loop design->print->measure->re-design pipelines
   (PowderBot, A-Lab, Ada, Bayesian-optimisation of printed parts), in-situ
   AM monitoring (melt-pool, OCT, PrintWatch / Spaghetti Detective), CV-based
   metrology, and what a credible end-to-end loop would look like for the
   powder-excavator specifically (CadQuery -> print -> Jubilee / OpenTrons
   rig + balance + vision -> Bayesian optimiser -> next params).

End with a concrete recommended toolchain (one pick each for: parametric CAD
authoring, generative exploration, DFM check, prototype-feedback loop, and
the wire-it-together path) for an open-source, pip-installable, no-license-
fee build.
"""


def make_client() -> FutureHouseClient:
    """Build a FutureHouseClient pinned to the Edison Scientific endpoint."""
    api_key = os.environ.get("EDISON_API_KEY")
    if not api_key:
        sys.exit("EDISON_API_KEY env var is not set")
    return FutureHouseClient(service_uri=EDISON_SERVICE_URI, api_key=api_key)


def _fence_for(content: str) -> str:
    """Return a backtick fence longer than any run of backticks in ``content``.

    Markdown fenced code blocks terminate on the first line that starts
    with a fence of equal or greater length than the opener, so to safely
    embed arbitrary content (including content that itself contains
    triple-backtick fences) we pick a fence one longer than the longest
    backtick run in the content (with a floor of 3).
    """
    longest = 0
    run = 0
    for ch in content:
        if ch == "`":
            run += 1
            if run > longest:
                longest = run
        else:
            run = 0
    return "`" * max(3, longest + 1)


def _embed_context() -> str:
    """Return the design-context files joined as fenced text blocks."""
    parts: list[str] = []
    for fp in CONTEXT_TEXT_FILES:
        if not fp.exists():
            continue
        rel = fp.relative_to(REPO_ROOT)
        ext = fp.suffix.lstrip(".") or "text"
        # Read with explicit UTF-8 (avoid locale-dependent decode errors)
        # and pick a fence longer than any backtick run in the file so
        # embedded ``` fences (e.g. inside README.md) can't prematurely
        # terminate the wrapper.
        text = fp.read_text(encoding="utf-8")
        fence = _fence_for(text)
        parts.append(f"\n=== file: {rel} ===\n{fence}{ext}\n{text}\n{fence}")
    return "\n".join(parts)


def submit_analysis(iteration: int) -> str:
    """Submit one iteration of the analysis feedback cycle."""
    if iteration not in ITERATION_PROMPTS:
        sys.exit(f"iteration must be one of {sorted(ITERATION_PROMPTS)}")
    client = make_client()
    query = (
        ANALYSIS_PREAMBLE
        + "\n"
        + ITERATION_PROMPTS[iteration]
        + "\n\n--- Embedded repository context follows ---\n"
        + _embed_context()
    )
    task = client.create_task(TaskRequest(name=JOB_ANALYSIS, query=query))
    print(f"submitted analysis iter {iteration}: task_id={task}")
    return str(task)


# File globs (relative to REPO_ROOT) that we ship to Edison as an *uploaded
# directory* alongside the inline-embedded text context. This is the path used
# by ``submit-analysis-with-files`` and is meant to give the analysis job the
# full design state: parametric source, generated CAD (STEP/STL/manifest),
# rendered figures (SVG/PNG/GIF), the LaTeX manuscript + bib, every prior
# Edison analysis, the brainstorming doc, and the original hand sketches.
UPLOAD_GLOBS: tuple[str, ...] = (
    "README.md",
    "powder-excavator-sketch.jpg",
    "PXL_20260423_231729467.jpg",
    "cad/*.py",
    "cad/README.md",
    "cad/tests/*.py",
    "cad/build/*.step",
    "cad/build/*.stl",
    "cad/build/manifest.json",
    "docs/figures/*.svg",
    "docs/figures/*.png",
    "docs/figures/*.gif",
    "docs/figures/cad/*.svg",
    "docs/figures/cad/*.png",
    "docs/manuscript/main.tex",
    "docs/manuscript/references.bib",
    "docs/edison/*.md",
    "docs/brainstorming-and-literature.md",
    "scripts/edison_submit.py",
)

# Question we ask Edison once the bundle is uploaded.
ANALYSIS_WITH_FILES_QUERY = """\
You are reviewing the **current state** of the powder-excavator project,
an open-hardware bulk powder dispenser intended to feed a downstream
precision gravimetric dispenser inside a self-driving lab.

**Hard constraint:** the entire dispensing motion must be achievable on a
3-axis gantry (X, Y, Z) -- *no* second actuator on the bucket itself. All
trough rotation / scoop opening / closing must come from passive mechanical
interaction with fixed external features (cam ramps, routed slots, fixed
posts, compliant flexures, etc.) driven by gantry motion alone.

The full design state has been uploaded to the job bucket and includes:

- ``README.md``, ``powder-excavator-sketch.jpg``, ``PXL_*.jpg``: design
  intent and the original hand sketch.
- ``cad/excavator.py`` + ``cad/build.py`` + ``cad/dfm.py`` + ``cad/render.py``:
  the CadQuery parametric source, exporter, DFM/feedback checks, and figure
  renderer.
- ``cad/tests/*.py``: the unit + regression tests for the CAD model.
- ``cad/build/*.step``, ``cad/build/*.stl``, ``cad/build/manifest.json``:
  STEP + STL exports of every part and the assembly, plus the parameter
  snapshot used to build them.
- ``docs/figures/*.svg`` + ``*.png`` + ``mechanism.gif``: schematic panels
  A-E of the mechanism.
- ``docs/figures/cad/*.svg`` + ``*.png``: hidden-line renders of the
  parametric model (per-part + assembly + 3 assembly views).
- ``docs/manuscript/main.tex`` + ``references.bib``: the manuscript draft.
- ``docs/edison/*.md``: every prior Edison analysis (analysis-v1 through
  analysis-v3) and the literature-review responses.
- ``docs/brainstorming-and-literature.md``: ideation + lit notes.
- ``scripts/edison_submit.py``: the script being used to submit this query.

Please review the current state end-to-end and provide:

1. A geometry / kinematics / statics critique of the parametric CAD as it
   currently stands (do the dimensions in ``ExcavatorParams``, the pivot
   placement, the cam-ramp rise vs. lever arc, the slot-board path, and
   the strike-off bar geometry actually compose into a working
   gantry-only powder-excavation cycle?). Cross-reference the rendered
   PNGs/SVGs against the schematic panels and call out any place the CAD
   and the schematic disagree.
2. Specific, parameter-level edits to ``ExcavatorParams`` you would make
   next, with justification (cite the figures or STEP/STL files when
   relevant).
3. A ranked list of the 3 highest-impact remaining risks to a successful
   first physical prototype, given the gantry-only constraint, and the
   cheapest experiment to retire each one.
4. A check on whether the DFM rules in ``cad/dfm.py`` cover the failure
   modes you would actually expect on a printed PETG / nylon / ESD-safe
   build -- what's missing? what's over-conservative?
5. Concrete next-iteration recommendations for: (a) the manuscript text,
   (b) the schematic figures (panels A-E + mechanism.gif), (c) the
   parametric model, and (d) the test suite.

Reply in the structure above with section headings 1-5.
"""


def _stage_upload_dir() -> Path:
    """Materialise the upload bundle in a temp directory.

    Resolves :data:`UPLOAD_GLOBS` relative to :data:`REPO_ROOT` and copies
    every match into a fresh temp directory, preserving the relative path
    layout so the analysis job sees a familiar structure. Returns the temp
    directory's path; callers are responsible for cleanup (the analysis
    job uploads the directory before we delete it).
    """
    staged = Path(tempfile.mkdtemp(prefix="excavator-edison-upload-"))
    for pattern in UPLOAD_GLOBS:
        for match in REPO_ROOT.glob(pattern):
            if not match.is_file():
                continue
            rel = match.relative_to(REPO_ROOT)
            dest = staged / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(match, dest)
    return staged


# File suffixes we treat as "text" and embed inline as fenced blocks. Anything
# else (PNG / JPG / GIF / STL / STEP) is referenced by a public GitHub raw URL
# on the current branch instead, because the Edison cluster's chunked upload
# endpoint returns 404 (see comment at the top of this file).
TEXT_SUFFIXES = frozenset({
    ".md", ".py", ".tex", ".bib", ".json", ".svg", ".txt", ".cfg", ".toml",
})

# GitHub repo coordinates for raw URLs. Hardcoded because the script ships
# only with this single repo.
GH_OWNER = "vertical-cloud-lab"
GH_REPO = "powder-excavator"


def _git_branch() -> str:
    """Best-effort current branch name for raw URLs (fallback to ``main``)."""
    try:
        import subprocess
        out = subprocess.check_output(
            ["git", "-C", str(REPO_ROOT), "rev-parse", "--abbrev-ref", "HEAD"],
            text=True,
        ).strip()
        return out or "main"
    except Exception:
        return "main"


def _embed_full_bundle() -> str:
    """Inline-embed every file from :data:`UPLOAD_GLOBS` for the analysis job.

    Text files are embedded as fenced code blocks (with a fence longer than
    any backtick run inside the file, so embedded ``` markers can't break
    out). Binary files are listed under "Binary asset references" with
    GitHub raw URLs on the current branch. This is the inline fallback used
    when the chunked upload endpoint is unavailable.
    """
    branch = _git_branch()
    text_parts: list[str] = []
    binary_lines: list[str] = []
    seen: set[Path] = set()
    for pattern in UPLOAD_GLOBS:
        for match in sorted(REPO_ROOT.glob(pattern)):
            if not match.is_file() or match in seen:
                continue
            seen.add(match)
            rel = match.relative_to(REPO_ROOT)
            if match.suffix.lower() in TEXT_SUFFIXES:
                ext = match.suffix.lstrip(".") or "text"
                try:
                    text = match.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    binary_lines.append(
                        f"- `{rel}` (binary, raw URL: "
                        f"https://github.com/{GH_OWNER}/{GH_REPO}/raw/{branch}/{rel})"
                    )
                    continue
                fence = _fence_for(text)
                text_parts.append(
                    f"\n=== file: {rel} ===\n{fence}{ext}\n{text}\n{fence}"
                )
            else:
                binary_lines.append(
                    f"- `{rel}` (raw URL: "
                    f"https://github.com/{GH_OWNER}/{GH_REPO}/raw/{branch}/{rel})"
                )
    bundle = "\n".join(text_parts)
    if binary_lines:
        bundle += (
            "\n\n=== Binary asset references (fetch from GitHub raw URL) ===\n"
            + "\n".join(binary_lines)
        )
    return bundle


def submit_analysis_with_files() -> str:
    """Submit a fresh analysis task bundling the full design state.

    Tries chunked upload first via ``client.upload_file`` (this is the
    "proper" path and is what the Edison docs describe). If the cluster
    returns the known 404 on ``/upload-chunk``, falls back to embedding
    every text-form file inline and listing binary assets (PNG/JPG/GIF/
    STL/STEP) by public GitHub raw URL on the current branch. Either way
    we end up with a single analysis task referencing the full design
    state; this command does **not** poll for results.
    """
    client = make_client()
    upload_id: str | None = None
    staged = _stage_upload_dir()
    n_files = sum(1 for _ in staged.rglob("*") if _.is_file())
    print(f"staged {n_files} files in {staged} for upload")
    try:
        try:
            upload_id = client.upload_file(
                job_name=JOB_ANALYSIS,
                file_path=str(staged),
            )
            print(f"upload complete: upload_id={upload_id}")
        except Exception as exc:  # noqa: BLE001 -- intentional broad catch + fallback
            print(
                f"chunked upload unavailable ({type(exc).__name__}); "
                "falling back to inline embedding + GitHub raw URLs",
                file=sys.stderr,
            )
    finally:
        shutil.rmtree(staged, ignore_errors=True)

    if upload_id is None:
        query = (
            ANALYSIS_WITH_FILES_QUERY
            + "\n\n--- Embedded repository bundle (inline fallback because the "
            "Edison chunked-upload endpoint is unavailable on this cluster) "
            "---\n"
            + _embed_full_bundle()
        )
        task = client.create_task(
            TaskRequest(name=JOB_ANALYSIS, query=query)
        )
        print(f"submitted analysis-with-files (inline): task_id={task}")
    else:
        task = client.create_task(
            TaskRequest(
                name=JOB_ANALYSIS,
                query=ANALYSIS_WITH_FILES_QUERY,
                runtime_config=RuntimeConfig(upload_id=upload_id),
            )
        )
        print(
            f"submitted analysis-with-files: task_id={task} upload_id={upload_id}"
        )
    return str(task)


def submit_cad_litreview() -> str:
    """Resubmit the generative-CAD literature-deep query at the Edison
    endpoint (the previous submission via FutureHouse was cancelled)."""
    client = make_client()
    task = client.create_task(
        TaskRequest(name=JOB_LITERATURE_HIGH, query=CAD_LITREVIEW_QUERY)
    )
    print(f"submitted CAD lit-review (paperqa3-high): task_id={task}")
    return str(task)


def poll(task_id: str) -> None:
    """Print the status and (if available) the formatted answer for a task."""
    client = make_client()
    resp = client.get_task(task_id)
    print(f"task_id : {task_id}")
    print(f"status  : {getattr(resp, 'status', '?')}")
    print(f"job     : {getattr(resp, 'job_name', '?')}")
    answer = getattr(resp, "formatted_answer", None) or getattr(resp, "answer", None)
    if answer:
        print("\n--- answer ---\n")
        print(answer)
    else:
        print("(no answer body yet)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("submit-cad-litreview")
    sub.add_parser("submit-analysis-with-files")
    p_an = sub.add_parser("submit-analysis")
    p_an.add_argument("iteration", type=int, choices=sorted(ITERATION_PROMPTS))
    p_poll = sub.add_parser("poll")
    p_poll.add_argument("task_id")
    args = parser.parse_args()
    if args.cmd == "submit-cad-litreview":
        submit_cad_litreview()
    elif args.cmd == "submit-analysis-with-files":
        submit_analysis_with_files()
    elif args.cmd == "submit-analysis":
        submit_analysis(args.iteration)
    elif args.cmd == "poll":
        poll(args.task_id)


if __name__ == "__main__":
    main()

````

=== Binary asset references (fetch from GitHub raw URL) ===
- `powder-excavator-sketch.jpg` (raw URL: https://github.com/vertical-cloud-lab/powder-excavator/raw/copilot/initial-prototyping-mini-excavator/powder-excavator-sketch.jpg)
- `PXL_20260423_231729467.jpg` (raw URL: https://github.com/vertical-cloud-lab/powder-excavator/raw/copilot/initial-prototyping-mini-excavator/PXL_20260423_231729467.jpg)
- `cad/build/arm.step` (raw URL: https://github.com/vertical-cloud-lab/powder-excavator/raw/copilot/initial-prototyping-mini-excavator/cad/build/arm.step)
- `cad/build/assembly.step` (raw URL: https://github.com/vertical-cloud-lab/powder-excavator/raw/copilot/initial-prototyping-mini-excavator/cad/build/assembly.step)
- `cad/build/cam_ramp.step` (raw URL: https://github.com/vertical-cloud-lab/powder-excavator/raw/copilot/initial-prototyping-mini-excavator/cad/build/cam_ramp.step)
- `cad/build/pin.step` (raw URL: https://github.com/vertical-cloud-lab/powder-excavator/raw/copilot/initial-prototyping-mini-excavator/cad/build/pin.step)
- `cad/build/slot_board.step` (raw URL: https://github.com/vertical-cloud-lab/powder-excavator/raw/copilot/initial-prototyping-mini-excavator/cad/build/slot_board.step)
- `cad/build/strike_off_bar.step` (raw URL: https://github.com/vertical-cloud-lab/powder-excavator/raw/copilot/initial-prototyping-mini-excavator/cad/build/strike_off_bar.step)
- `cad/build/trough.step` (raw URL: https://github.com/vertical-cloud-lab/powder-excavator/raw/copilot/initial-prototyping-mini-excavator/cad/build/trough.step)
- `cad/build/arm.stl` (raw URL: https://github.com/vertical-cloud-lab/powder-excavator/raw/copilot/initial-prototyping-mini-excavator/cad/build/arm.stl)
- `cad/build/cam_ramp.stl` (raw URL: https://github.com/vertical-cloud-lab/powder-excavator/raw/copilot/initial-prototyping-mini-excavator/cad/build/cam_ramp.stl)
- `cad/build/pin.stl` (raw URL: https://github.com/vertical-cloud-lab/powder-excavator/raw/copilot/initial-prototyping-mini-excavator/cad/build/pin.stl)
- `cad/build/slot_board.stl` (raw URL: https://github.com/vertical-cloud-lab/powder-excavator/raw/copilot/initial-prototyping-mini-excavator/cad/build/slot_board.stl)
- `cad/build/strike_off_bar.stl` (raw URL: https://github.com/vertical-cloud-lab/powder-excavator/raw/copilot/initial-prototyping-mini-excavator/cad/build/strike_off_bar.stl)
- `cad/build/trough.stl` (raw URL: https://github.com/vertical-cloud-lab/powder-excavator/raw/copilot/initial-prototyping-mini-excavator/cad/build/trough.stl)
- `docs/figures/mechanism.gif` (raw URL: https://github.com/vertical-cloud-lab/powder-excavator/raw/copilot/initial-prototyping-mini-excavator/docs/figures/mechanism.gif)
- `docs/figures/cad/assembly-end.png` (raw URL: https://github.com/vertical-cloud-lab/powder-excavator/raw/copilot/initial-prototyping-mini-excavator/docs/figures/cad/assembly-end.png)
- `docs/figures/cad/assembly-side.png` (raw URL: https://github.com/vertical-cloud-lab/powder-excavator/raw/copilot/initial-prototyping-mini-excavator/docs/figures/cad/assembly-side.png)
- `docs/figures/cad/assembly.png` (raw URL: https://github.com/vertical-cloud-lab/powder-excavator/raw/copilot/initial-prototyping-mini-excavator/docs/figures/cad/assembly.png)
```

## Answer

### 1. Geometry / Kinematics / Statics Critique of Current CAD

The parametric CAD model (`cad/excavator.py`) resolves the fundamental errors of previous revisions (the inverted pendulum and cam-ramp singularity are fixed), but introduces a new set of kinematic disconnects and integration ambiguities.

**Statics (Pendulum Stability):** The updated pivot placement ($Y = -4.0$ mm) successfully creates a stable pendulum. My calculations—using the default 1.27 g/cm³ PETG density and 1.0 g/cm³ powder density—place the loaded center of gravity at $Y \approx -6.12$ mm, giving a safe $+2.12$ mm restoring margin. The empty trough is also stable (CG at $Y \approx -7.32$ mm). The reduction of the rim lips to 2×2 mm (from the earlier 6×6 mm) was critical here; the heavy lips would have pulled the CG above the pivot.

**Kinematics (Cam Ramp):** The smooth cam ramp is kinematically sound but operates exactly at its physical limit. The lever arm from the pivot to the lip's outer corner is $17.65$ mm. At the target 45° tilt, the lip corner rises by a maximum of $9.98$ mm. The `cam_ramp_rise` is configured to $10.0$ mm, meaning it asks the lip to lift slightly further than it geometrically can without the gantry pushing the arm into the ramp itself. The sensitivity at 45° is a controllable $7.64$ deg/mm, safely below the 15 deg/mm ceiling and far from the snap-through singularity at ~70°.

**Kinematics (Slot Board vs. Schematic):** There are two major discrepancies between the `slot_path` CAD and Panel E:
1. **Missing Stem Geometry:** Panel E relies on a vertical stem connecting the carriage pivot to the slot peg. To achieve a 45° tilt from an 18 mm $Z$-drop in the slot (from $Z=30$ to $Z=12$), the stem must be exactly ~61.5 mm long (where $\Delta Z = L_{\text{stem}}(1 - \cos 45^\circ)$). The CAD entirely omits this stem and any parameters defining it, making the slot path meaningless in isolation.
2. **Directional Contradiction:** Panel E visually depicts the slot *rising* during the pour phase (SVG $y$-coordinates decrease from 144 to 112). The CAD `slot_path` defines the pour phase as *falling* (board-local $Z$ coordinates drop from 30 to 12). While both can work depending on the stem-mounting orientation, they describe opposite physical motions.

**Integration Ambiguities:** The CAD lacks mounting features. The vertical arms end abruptly without bolt holes or dovetails for the gantry carriage. The dowel pin lacks E-clip grooves or retaining features. The cam ramp and slot board lack lab-frame mounting features. The $Y$-height of the strike-off bar and the cam ramp relative to the gantry coordinate system are undefined.

### 2. Recommended Parameter-Level Edits to `ExcavatorParams`

*   **`cam_ramp_rise = 9.0`** (from 10.0). *Justification:* The maximum geometrically achievable rise for a 45° tilt with this lever arm is 9.98 mm. A 10.0 mm ramp demands impossible kinematics. Dropping it to 9.0 mm provides a 1 mm safety margin against manufacturing tolerances and gantry Z-axis sag.
*   **`pin_clearance = 0.4`** (from 0.3). *Justification:* While 0.3 mm is technically a sliding fit on highly tuned FDM printers, 0.4 mm is a much safer default for consumer printers to prevent the nylon/PETG bosses from binding on the metal dowel during the gravity-return swing.
*   **Add `stem_length = 61.5`** and **`peg_diameter = 4.0`**. *Justification:* The pin-defined-path variant requires a stem to connect the carriage to the slot. A 61.5 mm stem perfectly maps the 18 mm $Z$-drop in the current `slot_path` to the 45° target tilt.
*   **Add `arm_mounting_holes = True`** or similar interface geometry parameters. *Justification:* The arms currently cannot be attached to a real gantry.

### 3. Top 3 Highest-Impact Prototype Risks & Cheapest Experiments

1.  **Risk: The pin-slot kinematics bind or fail to hit the target tilt due to unaccounted stem geometry.**
    *   *Experiment:* Laser-cut or 3D-print a 2D planar mockup of the slot board, carriage pivot, and stem. Drive the "carriage" manually along a straight edge and measure the resulting stem angle to confirm the 61.5 mm stem / 18 mm $Z$-drop math yields a smooth 45° tilt without the peg binding in the slot corners.
2.  **Risk: Cohesive powder retention in the half-cylinder trough.**
    *   *Experiment:* Print just the trough body (with 2×2 mm lips). Manually pack it with a worst-case cohesive powder (e.g., damp flour, TiO₂), manually tilt it exactly 45° sideways over a balance, and measure the retained mass. Vapour-smooth the print and repeat. This isolates the geometric retention issue from gantry kinematics.
3.  **Risk: Triboelectric charging overriding gravity release.**
    *   *Experiment:* Perform the manual tilt test (above) using fine, dry inorganic salts in a standard PETG trough versus a trough lined with grounded copper tape. Measure the mass of powder clinging to the walls to quantify the severity of the electrostatic problem and validate the copper-tape mitigation.

### 4. Evaluation of `cad/dfm.py` Coverage

The DFM checks are a solid foundation but miss critical real-world failure modes for FDM prints:

**What is missing:**
*   **End-cap meat above the pin hole:** The pin hole is 3.3 mm in diameter and centered at $Y = -4.0$ mm. The flat rim is at $Y = 0$. This leaves only 2.35 mm of wall material above the bore. `dfm.py` does not check if this dimension satisfies the `min_wall` requirement.
*   **Kinematic Consistency:** It checks if the slot path fits in the gantry envelope, but it does *not* check if the `slot_path` $Z$-drop, `stem_length`, and `cam_target_tilt_deg` are mathematically consistent.
*   **FDM Print Orientation / Internal Overhangs:** The trough's interior is a half-cylinder. If printed open-side-down, the entire roof is a massive bridging overhang. `dfm.py` checks the cam ramp overhang but ignores the main body.
*   **Integration Checks:** It does not flag the absence of mounting holes or pin-retaining features.

**What is over-conservative:**
*   The warning on `slot X reversal` is conceptually useful but might trigger false positives for complex multi-stage dispensing schedules (e.g., if a "knock" oscillation is explicitly programmed into the slot path).

### 5. Concrete Next-Iteration Recommendations

*   **(a) Manuscript:** Add a subsection explicitly detailing the stem geometry required for the pin-in-slot variant. Acknowledge the discrepancy between the "rising slot" schematic and the "falling Z" CAD coordinates, explaining the coordinate system convention. Explicitly state the margin of safety on the pendulum stability ($+2.12$ mm).
*   **(b) Schematic Figures:** Update Panel E to include a labeled `stem_length` dimension. Reconcile the visual direction of the slot path in Panel E with the CAD model (either flip the SVG to show a descending slot or invert the CAD $Z$-coordinates). In Panel D, add a dimension showing the 9.98 mm max-rise limit to explain the cam ramp sizing.
*   **(c) Parametric Model:** Implement a `build_stem()` function. Add `stem_length` and `peg_diameter` to `ExcavatorParams`. Add bolt holes or dovetail mounts to the top of the arms. Add an E-clip groove to the dowel pin.
*   **(d) Test Suite:** Add a `test_kinematic_consistency()` unit test that asserts `dZ_slot == stem_length * (1 - cos(target_tilt))`. Add a `test_end_cap_wall()` test to ensure the material above the pin bore exceeds `min_wall`. Add a `test_cam_rise_margin()` to ensure `cam_ramp_rise` is strictly less than the maximum geometrically achievable rise.

***

**Discretionary Analytical Decisions:**
*   Evaluated pendulum stability using a composite model of 5 discrete volume elements (shell, endcaps, lips, bosses, powder) with typical densities (PETG = 1.27 g/cm³, Powder = 1.0 g/cm³) rather than relying on CAD-kernel volume integrals.
*   Modelled the powder load as a uniform half-disk extruded along the cavity length, assuming a 0° angle of repose for the initial static stability check.
*   Analysed the stem/slot kinematics assuming a stem-up geometry (peg above carriage pivot) where $\Delta Z = L(1 - \cos\theta)$, derived directly from the schematic's visual layout.
*   Defined the cam singularity as the point where the lip's circular arc tangent becomes strictly vertical ($\theta + \phi_0 = 90^\circ$).
*   Recommended increasing pin clearance to 0.4 mm based on standard consumer FDM tolerances, overriding the previous 0.3 mm recommendation which is often too tight for un-reamed printed bores.
