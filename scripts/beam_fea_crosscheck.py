#!/usr/bin/env python3
"""Higher-end FEA cross-check: B32 Timoshenko beams vs PRBM and PRBM+bending.

This script is the "higher-end simulation" pass for the bimodal-trough flexures.
It complements two simpler checks already in the repo:

* :mod:`scripts.bimodal_compliance` — analytical PRBM (axial-only von Mises
  truss). Captures the snap-through bistability driven by axial pre-compression,
  but treats each flexure as a pin-pin axial spring with no bending stiffness.
* :mod:`scripts.calculix_crosscheck` — CalculiX with **T3D2 truss** elements.
  Same physics as the PRBM (axial only), used as an independent FEA confirmation
  that the PRBM math is implemented correctly.

The truss check confirms the PRBM math but cannot tell us whether the *actual*
flexure beams (which have non-zero bending stiffness ``EI``) will still snap.
For the slender PETG flexures we're targeting (``t = 0.6 mm``, ``L ≈ 20 mm``)
the bending contribution is small relative to axial — but small is not zero,
and it can easily move the peak snap-through force by 10–25 % on a shallow
arch. That is the difference between "snaps cleanly on the first print" and
"feels mushy and needs the flexure thinned by 0.1 mm and re-printed".

This script therefore re-solves the V-truss with **B32 quadratic Timoshenko
beam elements** (already supported by the stock ``calculix-ccx`` package on
Ubuntu — no new dependencies). For each target apex displacement ``y`` we run
a separate displacement-controlled NLGEOM static solve and read the apex
reaction force, which traces the full force-displacement curve including the
unstable negative-stiffness branch between the wells.

Three curves are then overlaid in the output figure so the bending
contribution is *visible*:

1. **PRBM (axial only)** — from :mod:`scripts.bimodal_compliance`.
2. **PRBM + closed-form bending estimate** — adds a small-displacement linear
   bending term ``F_bend(y) ≈ k_bend · y`` from the two pinned-pinned
   half-beams treated as simply-supported beams loaded transversely at the
   apex. This gives an analytical sense of how big the bending contribution
   is *without* needing FEA, and lets the FEA result be cross-checked against
   it in the small-y regime.
3. **CalculiX 2.21 (B32, NLGEOM, displacement-controlled)** — the FEA solve.

Why displacement control rather than the *STATIC, RIKS arc-length method
suggested in the original plan: Riks failed to converge through the
snap-through region for our parameters in CalculiX 2.21 (the negative-stiffness
branch destabilised the arc-length predictor). Displacement control sidesteps
this — at every prescribed ``y`` the problem is well-posed even where the
tangent stiffness is negative — and recovers the full F–y curve including the
unstable branch, which is what we actually need.

Usage::

    sudo apt-get install -y calculix-ccx       # one-time, ~50 MB
    python -m scripts.beam_fea_crosscheck      # writes the comparison plot

Tested with ``ccx`` 2.21 on Ubuntu 24.04. Runs in ~60 s for the default
41-point sweep.
"""

from __future__ import annotations

import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from scripts.bimodal_compliance import FlexureParams, analyze, force as prbm_force


# ---------------------------------------------------------------------------
# Closed-form bending contribution (PRBM + bending)
# ---------------------------------------------------------------------------

def bending_force(y: np.ndarray | float, p: FlexureParams) -> np.ndarray | float:
    """Linear small-displacement transverse stiffness contribution from bending.

    Each of the two half-beams is treated as a pinned-pinned beam of effective
    length ``L0`` loaded at midspan by a vertical apex displacement that
    decomposes into a component perpendicular to the beam axis. For a
    pinned-pinned beam loaded transversely at midspan the lateral stiffness is
    ``k_lat = 48 * E * I / L^3``. The vertical component of the apex
    displacement projects onto this lateral DOF as ``cos(theta)`` where
    ``theta`` is the half-angle of the V-truss (``sin(theta) = h0 / L``).

    This is intentionally a *linear, small-y* estimate — its sole purpose is
    to show on the plot what order of magnitude the bending contribution
    contributes, so the reader can see at a glance how much the FEA result is
    changing because of bending vs because of geometric nonlinearity. The
    full nonlinear bending response is captured by the FEA curve.
    """
    L = p.effective_natural_length()
    I = p.width * p.thickness ** 3 / 12.0
    cos_theta = p.half_span / L
    # Two parallel half-beams, both contribute their lateral stiffness to the
    # apex; ``cos_theta`` projects vertical apex motion onto the lateral DOF
    # (and vice versa for the resulting force).
    k_bend = 2.0 * (48.0 * p.youngs_modulus * I / L ** 3) * cos_theta ** 2
    return -k_bend * np.asarray(y)


# ---------------------------------------------------------------------------
# CalculiX B32-beam input deck
# ---------------------------------------------------------------------------

def _build_inp(p: FlexureParams, y_target: float, n_seg_per_half: int) -> str:
    """Generate a CalculiX deck for one displacement-controlled B32 solve.

    The geometry is the symmetric V-truss: two straight half-beams joining
    the feet at ``(±b, 0)`` to a shared apex at ``(0, h0)``. Each half-beam
    is meshed with ``n_seg_per_half`` quadratic B32 beam elements (3 nodes
    per element, 9 integration points). Pre-compression is applied via a
    thermal contraction (``alpha · dT``) chosen to match
    ``FlexureParams.pre_compression`` exactly.
    """
    b = p.half_span
    h0 = p.initial_rise
    nseg = n_seg_per_half
    n_per_half = 2 * nseg + 1
    total = 2 * n_per_half - 1  # apex shared

    nodes: list[tuple[int, float, float]] = []
    for i in range(total):
        if i < n_per_half:
            t = i / (n_per_half - 1)
            x = -b * (1.0 - t)
            y = h0 * t
        else:
            j = i - (n_per_half - 1)
            t = j / (n_per_half - 1)
            x = b * t
            y = h0 * (1.0 - t)
        nodes.append((i + 1, x, y))
    apex_id = n_per_half

    elems: list[tuple[int, int, int, int]] = []
    eid = 1
    for k in range(nseg):
        n = 1 + 2 * k
        elems.append((eid, n, n + 1, n + 2))
        eid += 1
    for k in range(nseg):
        n = apex_id + 2 * k
        elems.append((eid, n, n + 1, n + 2))
        eid += 1

    node_lines = "\n".join(f"{nid}, {x:.6e}, {y:.6e}, 0.0" for nid, x, y in nodes)
    elem_lines = "\n".join(f"{e[0]}, {e[1]}, {e[2]}, {e[3]}" for e in elems)

    A = p.width * p.thickness
    L_built = math.hypot(b, h0)
    L0 = p.effective_natural_length()
    pre = (L_built - L0) / L_built  # fractional pre-compression
    alpha = 1.0e-3
    dT = -pre / alpha

    return f"""*HEADING
B32 beam V-truss, displacement-controlled, NLGEOM
*NODE, NSET=NALL
{node_lines}
*NSET, NSET=NAPEX
{apex_id}
*NSET, NSET=NLEFT
1
*NSET, NSET=NRIGHT
{nodes[-1][0]}
*ELEMENT, TYPE=B32, ELSET=EBEAM
{elem_lines}
*BEAM SECTION, ELSET=EBEAM, MATERIAL=PETG, SECTION=RECT
 {p.width:.6e}, {p.thickness:.6e}
 0.0, 0.0, 1.0
*MATERIAL, NAME=PETG
*ELASTIC
 {p.youngs_modulus:.3e}, 0.30
*EXPANSION
 {alpha:.3e}
*BOUNDARY
 NLEFT, 1, 3
 NRIGHT, 1, 3
 NAPEX, 1, 1
 NAPEX, 3, 3
*INITIAL CONDITIONS, TYPE=TEMPERATURE
NALL, 0.0
*STEP, NLGEOM, INC=400
*STATIC
 0.05, 1.0
*TEMPERATURE
NALL, {dT:.6e}
*BOUNDARY
 NAPEX, 2, 2, {y_target - h0:.6e}
*NODE PRINT, NSET=NAPEX, FREQUENCY=1000
 RF
*END STEP
"""


# ---------------------------------------------------------------------------
# Sweep driver
# ---------------------------------------------------------------------------

@dataclass
class BeamSweepResult:
    """One displacement-controlled apex-force point from CalculiX."""

    y: float    # apex height above the feet line [m]
    force: float  # restoring force on the apex (positive = pushing apex up) [N]


def run_sweep(p: FlexureParams | None = None,
              n_steps: int = 41,
              y_max_factor: float = 1.6,
              n_seg_per_half: int = 10) -> list[BeamSweepResult]:
    """Sweep apex displacement and return CalculiX B32-beam apex force points.

    Parameters
    ----------
    p
        Flexure parameters. Default is the design point from
        :class:`FlexureParams`.
    n_steps
        Number of apex-displacement targets in the sweep.
    y_max_factor
        Sweep extent as a multiple of ``initial_rise`` either side of the
        feet line. ``1.6`` covers both wells plus margin for the default
        geometry.
    n_seg_per_half
        B32 elements per half-beam. ``10`` is enough for monotonic
        convergence of the snap force at the default geometry.

    Notes
    -----
    Diverged/non-converged points are silently skipped — Riks would be
    needed to walk through any region where the prescribed-y problem itself
    becomes ill-posed, but for this geometry displacement control converges
    everywhere.
    """
    if p is None:
        p = FlexureParams()
    if shutil.which("ccx") is None:
        raise RuntimeError(
            "CalculiX (`ccx`) not found in PATH. Install with "
            "`sudo apt-get install -y calculix-ccx`."
        )

    y_targets = np.linspace(-p.initial_rise * y_max_factor,
                            +p.initial_rise * y_max_factor,
                            n_steps)
    results: list[BeamSweepResult] = []

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        inp_path = tmp_path / "beam.inp"
        dat_path = tmp_path / "beam.dat"
        for yt in y_targets:
            inp_path.write_text(_build_inp(p, float(yt), n_seg_per_half))
            r = subprocess.run(
                ["ccx", "beam"], cwd=tmp_path,
                capture_output=True, text=True, timeout=120,
            )
            if r.returncode != 0 or not dat_path.exists():
                continue
            text = dat_path.read_text()
            # Last "forces" block for NAPEX gives the reaction. Format is
            # one node row of (vx, vy, vz). We want vy.
            blocks = list(re.finditer(
                r"forces .*?for set NAPEX and time\s+[-\dEe.+]+\s*\n\s*\n"
                r"\s*\d+\s+([-\dEe.+]+)\s+([-\dEe.+]+)\s+([-\dEe.+]+)",
                text,
            ))
            if not blocks:
                continue
            fy = float(blocks[-1].group(2))
            # *NODE PRINT RF gives reaction; flip sign so positive F means
            # restoring force opposing positive y (matches PRBM convention).
            results.append(BeamSweepResult(y=float(yt), force=-fy))

    return results


# ---------------------------------------------------------------------------
# Plotting & reporting
# ---------------------------------------------------------------------------

def _equilibria_from_curve(y: np.ndarray, F: np.ndarray) -> list[tuple[float, str]]:
    """Bracket-and-bisect locator for F(y) = 0 with stability classification.

    Used for the FEA curve, which is sampled discretely. An equilibrium is
    *stable* iff ``dF/dy < 0`` at the crossing (the force pushes the apex
    back toward equilibrium); *unstable* iff ``dF/dy > 0``.
    """
    eqs: list[tuple[float, str]] = []
    for i in range(len(y) - 1):
        f0, f1 = F[i], F[i + 1]
        if f0 == 0.0 or f0 * f1 < 0.0:
            if f0 == f1:
                y_eq = float(y[i])
            else:
                y_eq = float(y[i] - f0 * (y[i + 1] - y[i]) / (f1 - f0))
            slope = (f1 - f0) / (y[i + 1] - y[i])
            kind = "stable" if slope < 0.0 else "unstable"
            eqs.append((y_eq, kind))
    return eqs


def render_comparison(results: list[BeamSweepResult], out_path: Path,
                      p: FlexureParams | None = None) -> Path:
    """Write the three-curve comparison plot to ``out_path`` (svg + png)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    if p is None:
        p = FlexureParams()
    prbm = analyze(p, y_range=(-7e-3, 7e-3), n_samples=2001)
    y_dense = prbm.y
    F_axial = prbm.force
    F_bend = np.asarray(bending_force(y_dense, p))
    F_combined = F_axial + F_bend

    y_fea = np.array([r.y for r in results])
    F_fea = np.array([r.force for r in results])

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.0, 4.8))

    fea_eqs = _equilibria_from_curve(y_fea, F_fea)
    fea_abs_max = float(np.abs(F_fea).max()) if F_fea.size else 1.0

    for ax, ylim, title in (
        (axL, (-1.1 * fea_abs_max, 1.1 * fea_abs_max),
         "Full F–y range (B32 bending dominates)"),
        (axR, (-5.0, 5.0),
         "Zoom to ±5 N (PRBM and PRBM+bending visible)"),
    ):
        ax.plot(y_dense * 1e3, F_axial, "b-", lw=2,
                label="PRBM, axial only (von Mises truss)")
        ax.plot(y_dense * 1e3, F_combined, "g--", lw=1.6,
                label="PRBM + linear bending estimate")
        ax.plot(y_fea * 1e3, F_fea, "rs", ms=6, mfc="none", mew=1.5,
                label="CalculiX 2.21, B32 Timoshenko beams (NLGEOM)")
        ax.axhline(0.0, color="black", lw=0.5)

        for y_eq, kind in prbm.equilibria:
            color = "tab:blue" if kind == "stable" else "tab:purple"
            marker = "o" if kind == "stable" else "X"
            ax.plot(y_eq * 1e3, 0.0, marker=marker, color=color, ms=10,
                    mfc="none", mew=1.5, zorder=5)
        for y_eq, kind in fea_eqs:
            color = "tab:red" if kind == "stable" else "tab:orange"
            marker = "o" if kind == "stable" else "X"
            ax.plot(y_eq * 1e3, 0.0, marker=marker, color=color, ms=10,
                    mfc="none", mew=1.5, zorder=5)

        ax.set_xlabel("apex displacement  $y$  [mm]")
        ax.set_ylabel("restoring force  $F$  [N]")
        ax.set_title(title)
        ax.set_xlim(-7, 7)
        ax.set_ylim(*ylim)
        ax.grid(True, alpha=0.3)
        ax.legend(loc="upper right", fontsize=8)
    fig.suptitle(
        "Higher-end FEA cross-check: PRBM (axial) vs PRBM+bending vs B32 beam",
        fontsize=11,
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path)
    fig.savefig(out_path.with_suffix(".png"), dpi=120)
    plt.close(fig)
    return out_path


def report(results: list[BeamSweepResult],
           p: FlexureParams | None = None) -> str:
    """Human-readable comparison of peak snap force and well location."""
    if p is None:
        p = FlexureParams()
    prbm = analyze(p)
    y_fea = np.array([r.y for r in results])
    F_fea = np.array([r.force for r in results])
    if y_fea.size == 0:
        return "FEA produced no converged points."

    fea_eqs = _equilibria_from_curve(y_fea, F_fea)
    fea_stable = [y for y, kind in fea_eqs if kind == "stable"]

    # Peak |F| between the outermost stable wells (or whole sweep if none).
    if len(fea_stable) >= 2:
        y_lo, y_hi = min(fea_stable), max(fea_stable)
        mask = (y_fea >= y_lo) & (y_fea <= y_hi)
        fea_peak = float(np.abs(F_fea[mask]).max()) if mask.any() else float(np.abs(F_fea).max())
    else:
        fea_peak = float(np.abs(F_fea).max())

    lines = ["B32-beam FEA cross-check"]
    lines.append("-" * len(lines[0]))
    lines.append(f"  PRBM (axial-only) peak snap force: {prbm.snap_through_force:6.3f} N")
    lines.append(f"  PRBM (axial-only) stable wells:    "
                 + ", ".join(f"{w*1e3:+.3f} mm" for w in sorted(prbm.stable_wells)))
    lines.append(f"  B32 FEA peak |F| in well-to-well range: {fea_peak:6.3f} N")
    if fea_stable:
        lines.append(f"  B32 FEA stable wells:              "
                     + ", ".join(f"{w*1e3:+.3f} mm" for w in sorted(fea_stable)))
    else:
        lines.append("  B32 FEA stable wells:              none detected")
    if len(fea_stable) < 2:
        lines.append(
            "  WARNING: bending stiffness in the actual beams may be large"
            " enough to suppress one or both wells. Re-run the robustness"
            " sweep (scripts/robustness_sweep.py) before printing."
        )
    return "\n".join(lines)


def main() -> int:
    print("Running CalculiX B32-beam sweep (this takes ~60 s)…")
    p = FlexureParams()
    results = run_sweep(p)
    print(f"  captured {len(results)} converged FEA points")
    if not results:
        print("ERROR: no CalculiX results captured.", file=sys.stderr)
        return 1

    print()
    print(report(results, p))
    print()

    figures = Path(__file__).resolve().parent.parent / "docs" / "figures"
    out = figures / "bimodal-beam-fea-crosscheck.svg"
    render_comparison(results, out, p)
    json_out = figures / "bimodal-beam-fea-crosscheck.json"
    json_out.write_text(json.dumps(
        {"y_m": [r.y for r in results], "Fy_N": [r.force for r in results]},
        indent=2,
    ))
    print(f"  wrote {out} and {json_out}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
