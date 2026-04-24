# Bimodal compliant mechanism — secondary design idea

> Tracks issue [#4]; complements the cam-ramp baseline being developed in
> [#2].

## What "bimodal" means here

We use **bimodal** as a synonym for **bistable**: the trough/scoop assembly
has *exactly two* stable equilibria — a "scoop" pose and a "dump" pose —
separated by a finite snap-through energy barrier. The mechanism rests in
either pose with no holding torque from the gantry; transitioning between
them requires the gantry to push past the barrier, after which the mechanism
snaps the rest of the way on its own.

This is attractive for the powder-excavator because:

1. **Repeatability.** The dump pose is set by the geometry of the flexure,
   not by where the gantry happens to stop. Every dump is the same angle.
2. **No external return spring or latch.** The flexure provides both the
   return force and the latching action (no separate ledge / hook to
   register against, and no risk of mis-engagement on approach).
3. **Tactile end-stops.** The snap is sharp, which helps shake loose
   residual cohesive powder — a partial substitute for the ERM vibration
   motor proposed in #3.
4. **Single moving part.** The two flexures and the trough are one printed
   piece. There are no pin joints to wear, bind, or contaminate with
   powder.

## Mechanical concept

The secondary design replaces the pin-and-ledge pivot of the baseline with
a **symmetric pre-compressed pair of flexure beams** — the canonical
*von Mises truss* used throughout the compliant-mechanism literature
(Howell, *Compliant Mechanisms*, Wiley 2001, ch. 6). The two flexures are
fixed to the gantry-mounted frame at their feet and pinned (printed in one
piece, in practice) to the trough's tilt axis at their apex. Because the
flexures are slightly shorter than the as-fabricated chord between their
feet and the apex, they are axially pre-compressed at assembly. That
pre-compression turns the apex-up configuration from a single stable
equilibrium into an unstable saddle with two stable wells either side of
it.

```
     trough  (tilts about the apex)
       \____________/
            /\
   flexure /  \ flexure
          /    \         <-- pre-compressed in their as-built geometry
         /      \
   ====/========\=====   <-- frame mounted to the gantry carriage
```

When the gantry presses one end of the trough downward, the apex moves
laterally past the central instability, the flexures snap from one well to
the other, and the trough flips into the dump pose. Lifting the gantry off
the trough leaves it in the dump pose; touching it from the other side
snaps it back.

## How we test for bimodal compliance

Two independent open-source tools are checked in here:

1. A **closed-form / numerical PRBM model** in
   [`scripts/bimodal_compliance.py`](../scripts/bimodal_compliance.py).
   It implements the Pseudo-Rigid-Body Model of the von Mises truss as two
   axial-spring flexures, samples the strain-energy curve `U(y)` over the
   apex-displacement range, locates every equilibrium with `scipy.optimize`,
   classifies each as stable or unstable from the sign of `d²U/dy²`, and
   measures the snap-through energy barrier and peak actuation force.
   The design is reported as **bimodal** iff there are exactly two stable
   equilibria with a positive barrier between them.

2. A **pytest regression suite** in
   [`tests/test_bimodal_compliance.py`](../tests/test_bimodal_compliance.py).
   It pins the qualitative behaviour we rely on (two stable wells,
   symmetric about the centre, well location matching the closed-form
   `y = ±√(L₀² − b²)`, and loss of bistability when the pre-compression is
   removed) so that future tweaks to the geometry don't silently break it.

Both are wired into a [GitHub Actions
workflow](../.github/workflows/bimodal-compliance.yml) that runs on every
push touching the analyser, so we'll catch a non-bimodal design before it
gets prototyped.

### Why PRBM as the primary tool (and what we did try)

The brief was to *install software that can help run tests to check for
bimodal compliance*. Three open-source FEA tools were evaluated by actually
installing them on a stock Ubuntu 24.04 runner — the dismissive "heavyweight"
table in an earlier draft of this doc was wrong, and the results below
replace it.

| Tool        | Install command                              | Result        | Used here? |
| ----------- | -------------------------------------------- | ------------- | ---------- |
| `numpy`+`scipy` PRBM    | `pip install -r requirements.txt`            | works in seconds, runs in CI | **primary** (`scripts/bimodal_compliance.py`) |
| **SfePy**   | `pip install sfepy`                          | installed cleanly (v 2026.1, ~30 s, pure pip) | available; not yet wired up |
| **CalculiX**| `sudo apt-get install -y calculix-ccx`       | installed cleanly (v 2.21, single deb, ~50 MB) | **cross-check**: `scripts/calculix_crosscheck.py` re-solves the truss with NLGEOM; agrees with PRBM end-to-end ([figure](figures/bimodal-fea-crosscheck.svg)) |
| code_aster  | not packaged for Ubuntu 24.04; no published Docker image on Docker Hub or quay.io that we could pull anonymously; `pip install code_aster` returns nothing | **could not install in this environment** | n/a |

PRBM is still the *primary* tool because (a) it's pure-Python so it runs in
CI on every push without apt, (b) the bistability question is purely
topological in `U(y)` and PRBM captures that exactly for this geometry, and
(c) it returns a clean Python data structure (`AnalysisResult`) the tests
can assert against. CalculiX is now wired in as a one-shot cross-check
(see [`scripts/calculix_crosscheck.py`](../scripts/calculix_crosscheck.py))
so we have an independent FEA confirmation of the snap-through curve, and
we can graduate to it (or to SfePy) the moment we need flexure-bending
stress, fatigue, or buckling results that PRBM can't give.

## Running the check locally

```bash
pip install -r requirements.txt
python scripts/bimodal_compliance.py        # prints summary, writes plot
pytest tests/test_bimodal_compliance.py     # regression test

# optional: regenerate the four-panel figure + snap-through GIF
python -m scripts.visualize_bimodal

# optional: independent CalculiX FEA cross-check
sudo apt-get install -y calculix-ccx        # one-time, ~50 MB
python -m scripts.calculix_crosscheck       # writes docs/figures/bimodal-fea-crosscheck.svg
```

The default parameters give two stable wells at apex displacements of
≈ ±1.9 mm (≈ ±6.5° trough tilt), separated by a snap-through barrier of
≈ 2.9 mJ that requires a peak actuation force of ≈ 2.4 N — comfortably
within what the 3018-PROVer V2 gantry can deliver, and a useful starting
point for sizing the prototype.

## Visualisations

Generated by `scripts/visualize_bimodal.py` and `scripts/calculix_crosscheck.py`
and committed under `docs/figures/`:

| File | Description |
| ---- | ----------- |
| [`bimodal-mechanism.svg`](figures/bimodal-mechanism.svg) / `.png` | Four-panel figure: (A) the mechanism in its two stable poses with powder grains visualised, (B) the double-well energy landscape with stable / unstable equilibria and barrier height annotated, (C) the force-displacement curve including the negative-stiffness snap-through region, (D) trough tilt vs apex displacement. |
| [`bimodal-mechanism.gif`](figures/bimodal-mechanism.gif) | Animation of the trough snapping between the scoop and dump poses, with the corresponding point on the energy curve tracked alongside. |
| [`bimodal-fea-crosscheck.svg`](figures/bimodal-fea-crosscheck.svg) / `.png` | PRBM analytical force-displacement curve overlaid on 64 points from a CalculiX 2.21 NLGEOM truss solve. The two methods agree across the full snap-through range. |
| [`bimodal-fea-crosscheck.json`](figures/bimodal-fea-crosscheck.json) | Raw `(y, F)` points returned by CalculiX, for downstream regression checks. |
| [`bimodal-energy.svg`](figures/bimodal-energy.svg) | Minimal energy/force plot emitted by `scripts/bimodal_compliance.py` itself. |

## 3D-printable prototype

A monolithic, fastener-free, support-free print of this design lives under
[`cad/`](../cad/), with an isometric preview, a sliced-and-ready STL, the
parametric OpenSCAD source, and a full PETG print/test guide:

| File | What it is |
| ---- | ---------- |
| [`cad/bimodal_trough.scad`](../cad/bimodal_trough.scad) | Parametric source — variables mirror `FlexureParams`. |
| [`cad/bimodal-trough.stl`](../cad/bimodal-trough.stl) | 76 × 26 × 20 mm mesh, 1 264 triangles, manifold. ~45 min / ~6 g of PETG. |
| [`cad/bimodal-trough-iso.png`](../cad/bimodal-trough-iso.png) | Render. |
| [`cad/README.md`](../cad/README.md) | Print settings, mounting, and the snap-force / cycle / powder test procedure. |

## Open questions / next steps

- [ ] Sweep `(half_span, initial_rise, pre_compression, thickness)` to find
      a parameter set that puts the dump-pose tilt in the 25–35° range
      called for by the trough-pour kinematics from #2.
- [ ] Add a flexural (PRBM-`γ`/`K_Θ`) correction to capture the bending
      contribution alongside the axial-only von Mises term, so we can size
      the flexures against yield/fatigue rather than just stiffness.
- [ ] Hand off the chosen parameter set to `scripts/generate_figures.py`
      (currently being added in #2) for a Panel-F figure in the manuscript.
- [ ] Compare side-by-side with the smooth cam-ramp baseline (#2) and the
      pin-slot variant currently being added there.
