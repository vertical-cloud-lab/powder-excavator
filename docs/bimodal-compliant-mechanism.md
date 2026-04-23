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

### Why PRBM and not full FEA

The brief was to *install software that can help run tests to check for
bimodal compliance*. Two paths were considered:

| Tool                | Install cost | Fits in CI | Sufficient for bistability check? |
| ------------------- | ------------ | ---------- | --------------------------------- |
| `numpy`/`scipy` PRBM (this PR)             | `pip install` (seconds) | yes  | yes — bistability is a topological property of `U(θ)`, captured exactly by PRBM |
| `SfePy` / `FEniCSx` (continuum FEA)        | minutes, native deps    | awkward | overkill at this stage |
| `CalculiX` / `code_aster` (commercial-grade FEA) | system packages, CAD pre-processing | no | overkill at this stage |

PRBM is the standard first-pass tool for compliant-mechanism design and
gives an exact answer to the bistability question for this geometry; we
should only graduate to continuum FEA once we are sizing the flexure
cross-section against fatigue and snap-through stress, which is out of
scope for this issue.

## Running the check locally

```bash
pip install -r requirements.txt
python scripts/bimodal_compliance.py        # prints summary, writes plot
pytest tests/test_bimodal_compliance.py     # regression test
```

The default parameters give two stable wells at apex displacements of
≈ ±1.9 mm (≈ ±6.5° trough tilt), separated by a snap-through barrier of
≈ 2.9 mJ that requires a peak actuation force of ≈ 2.4 N — comfortably
within what the 3018-PROVer V2 gantry can deliver, and a useful starting
point for sizing the prototype.

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
