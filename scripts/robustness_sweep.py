#!/usr/bin/env python3
"""Robustness (uncertainty-quantification) sweep for the bimodal-trough.

The closed-form PRBM analyzer in :mod:`scripts.bimodal_compliance` gives the
nominal force-displacement curve, and the higher-end B32-beam FEA in
:mod:`scripts.beam_fea_crosscheck` checks that bending physics doesn't kill
the snap-through. Neither of those tells us how forgiving the design is to
the things we *can't* control on a small FDM printer:

* ``flexure_thick`` (``±0.05 mm``, ~8 %) — first-layer squish, nozzle wear.
  The dominant lever, because flexure stiffness scales with ``t³``.
* ``youngs_modulus`` (``±15 %``) — PETG batch + drybox / humidity history.
* ``initial_rise`` (``±0.1 mm``) — cooling distortion of the as-printed arch.
* ``pre_compression`` (``±0.3 %``) — assembly tolerance, only relevant if the
  flexures are not printed monolithically (default design *is* monolithic, so
  this enters via residual stress rather than assembly slop).

This script wraps the PRBM analyzer in a Latin-hypercube sweep over those
four inputs (using ``scipy.stats.qmc`` — already in ``requirements.txt``)
and reports:

* ``P(bistable)`` — fraction of samples that have two stable wells with a
  positive snap-through barrier.
* 5th / 50th / 95th-percentile peak snap-through force across the bistable
  samples — the realistic spread the print/test rig will see.
* First-order sensitivity (squared Pearson correlation of each input with
  the peak snap force across bistable samples) — a cheap proxy for Sobol
  indices that needs no extra solves.
* A *robust* parameter recommendation: scan a 2-D grid over
  ``(flexure_thick, initial_rise)`` (the two design knobs you actually
  control on the print bed) and pick the cell with the highest
  ``P(bistable)`` after re-sampling the other two inputs over their
  manufacturing spreads.

Run as a module from the repo root::

    python -m scripts.robustness_sweep                 # 256-sample default
    python -m scripts.robustness_sweep --samples 64    # quick CI-friendly run
    python -m scripts.robustness_sweep --grid-only     # skip MC, just heatmap

Outputs:

* ``docs/figures/bimodal-robustness-violin.{svg,png}`` — peak snap-through
  force distribution as a violin, broken out by which input dominates.
* ``docs/figures/bimodal-robustness-heatmap.{svg,png}`` — 2-D heatmap of
  ``P(bistable)`` over ``(flexure_thick, initial_rise)``.
* ``docs/figures/bimodal-robustness-summary.json`` — machine-readable summary
  (percentiles, sensitivities, recommended parameter set).

Why PRBM and not the B32 FEA in the loop: PRBM solves in milliseconds, so
256 (or 1 024) samples take seconds. The B32 FEA takes ~60 s per sample,
which would push the sweep to multiple hours and out of CI scope. PRBM
captures the bistability *topology* (whether two wells exist at all)
exactly, which is what dominates the print/no-print decision; the absolute
peak force the sweep reports is the PRBM number, and the user can apply the
B32-FEA bending correction from the cross-check figure to scale it. Future
work: cache B32 results and use them as the sweep model for the hot-spot
region the heatmap identifies.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.stats import qmc

from scripts.bimodal_compliance import AnalysisResult, FlexureParams, analyze


# ---------------------------------------------------------------------------
# Manufacturing-tolerance ranges
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class InputRanges:
    """±-half-widths for each manufacturing input around its nominal value.

    The default values reflect realistic FDM-PETG print-to-print variation
    measured on small-nozzle (0.4 mm) prints and are used as the sweep's
    manufacturing-tolerance ranges.
    """

    thick_tol: float = 0.05e-3       # m, half-width
    youngs_tol_frac: float = 0.15    # fractional, ±15 %
    rise_tol: float = 0.10e-3        # m, half-width
    pre_compression_tol: float = 0.003  # absolute, ±0.3 percentage points


def _bounds(p: FlexureParams, r: InputRanges) -> np.ndarray:
    """Return the ``(low, high)`` bounds for the four sampled inputs.

    Pre-compression is clamped at zero on the low side — a negative
    pre-compression would mean the as-built flexure is *longer* than its
    natural length, which is a different regime (taut, not bistable) and
    isn't a realistic manufacturing outcome.
    """
    return np.array([
        [p.thickness - r.thick_tol, p.thickness + r.thick_tol],
        [p.youngs_modulus * (1 - r.youngs_tol_frac),
         p.youngs_modulus * (1 + r.youngs_tol_frac)],
        [p.initial_rise - r.rise_tol, p.initial_rise + r.rise_tol],
        [max(0.0, p.pre_compression - r.pre_compression_tol),
         p.pre_compression + r.pre_compression_tol],
    ])


# ---------------------------------------------------------------------------
# Sweep core
# ---------------------------------------------------------------------------

@dataclass
class Sample:
    thickness: float
    youngs_modulus: float
    initial_rise: float
    pre_compression: float
    is_bimodal: bool
    peak_force: float       # peak |F| between wells [N], 0 if not bimodal
    barrier_height: float   # snap-through energy barrier [J], 0 if not bimodal
    well_separation: float  # separation between the two stable wells [m], 0 if not


def _evaluate(thickness: float, youngs_modulus: float,
              initial_rise: float, pre_compression: float,
              base: FlexureParams) -> Sample:
    """Run the PRBM analyzer for one sampled parameter set."""
    p = FlexureParams(
        half_span=base.half_span,
        initial_rise=initial_rise,
        natural_length=None,
        youngs_modulus=youngs_modulus,
        width=base.width,
        thickness=thickness,
        tilt_per_y=base.tilt_per_y,
        pre_compression=pre_compression,
    )
    result: AnalysisResult = analyze(p)
    wells = sorted(result.stable_wells)
    sep = wells[-1] - wells[0] if len(wells) >= 2 else 0.0
    return Sample(
        thickness=thickness,
        youngs_modulus=youngs_modulus,
        initial_rise=initial_rise,
        pre_compression=pre_compression,
        is_bimodal=result.is_bimodal,
        peak_force=result.snap_through_force if result.is_bimodal else 0.0,
        barrier_height=result.barrier_height if result.is_bimodal else 0.0,
        well_separation=sep,
    )


def lhs_sweep(n_samples: int, base: FlexureParams, ranges: InputRanges,
              seed: int = 20240424) -> list[Sample]:
    """Latin-hypercube sample the four inputs and evaluate the PRBM at each."""
    bounds = _bounds(base, ranges)
    sampler = qmc.LatinHypercube(d=4, seed=seed)
    unit = sampler.random(n=n_samples)
    scaled = qmc.scale(unit, bounds[:, 0], bounds[:, 1])
    return [_evaluate(*row, base=base) for row in scaled]


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

INPUT_LABELS = (
    "flexure thickness  [mm]",
    "Young's modulus  [GPa]",
    "initial rise  [mm]",
    "pre-compression  [%]",
)
INPUT_SCALE = (1e3, 1e-9, 1e3, 1e2)
INPUT_KEYS = ("thickness", "youngs_modulus", "initial_rise", "pre_compression")


def first_order_sensitivities(samples: list[Sample]) -> dict[str, float]:
    """Squared Pearson correlation between each input and the peak snap force.

    A cheap, no-extra-solve proxy for Sobol first-order indices. Computed
    only over bistable samples (the peak force is undefined elsewhere). The
    returned values are normalised to sum to 1 so they read as "fraction of
    explained variance attributable to this input".
    """
    bistable = [s for s in samples if s.is_bimodal]
    if len(bistable) < 4:
        return {k: float("nan") for k in INPUT_KEYS}
    F = np.array([s.peak_force for s in bistable])
    raw: dict[str, float] = {}
    for key in INPUT_KEYS:
        x = np.array([getattr(s, key) for s in bistable])
        if x.std() == 0.0 or F.std() == 0.0:
            raw[key] = 0.0
            continue
        c = float(np.corrcoef(x, F)[0, 1])
        raw[key] = c * c
    total = sum(raw.values())
    if total == 0.0:
        return {k: 0.0 for k in INPUT_KEYS}
    return {k: v / total for k, v in raw.items()}


def summarise(samples: list[Sample]) -> dict[str, object]:
    """Build a JSON-serialisable summary of the sweep."""
    n = len(samples)
    bistable = [s for s in samples if s.is_bimodal]
    p_bistable = len(bistable) / n if n else 0.0
    if bistable:
        F = np.array([s.peak_force for s in bistable])
        pcts = np.percentile(F, [5, 50, 95])
        peak_summary = {
            "p05_N": float(pcts[0]),
            "p50_N": float(pcts[1]),
            "p95_N": float(pcts[2]),
            "mean_N": float(F.mean()),
            "std_N": float(F.std()),
        }
    else:
        peak_summary = {k: 0.0 for k in ("p05_N", "p50_N", "p95_N",
                                         "mean_N", "std_N")}
    return {
        "n_samples": n,
        "n_bistable": len(bistable),
        "p_bistable": p_bistable,
        "peak_snap_force": peak_summary,
        "sensitivities_norm_explained_var": first_order_sensitivities(samples),
    }


def report(summary: dict[str, object]) -> str:
    """Human-readable rendering of :func:`summarise`."""
    lines = ["Robustness sweep — PRBM under FDM print tolerances"]
    lines.append("-" * len(lines[0]))
    lines.append(f"  samples drawn:        {summary['n_samples']}")
    lines.append(f"  bimodal samples:      {summary['n_bistable']}")
    lines.append(f"  P(bistable):          {float(summary['p_bistable']):.3f}")
    pf = summary["peak_snap_force"]
    lines.append(f"  peak snap force [N]:  "
                 f"p05={pf['p05_N']:.3f}  p50={pf['p50_N']:.3f}  p95={pf['p95_N']:.3f}  "
                 f"(mean={pf['mean_N']:.3f}, sd={pf['std_N']:.3f})")
    lines.append("  first-order sensitivity (frac. explained variance):")
    for k, v in summary["sensitivities_norm_explained_var"].items():
        lines.append(f"    {k:18s}  {v:.3f}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Robust-design recommendation: scan (thickness, initial_rise) grid
# ---------------------------------------------------------------------------

@dataclass
class GridResult:
    thickness_grid: np.ndarray   # 1D, m
    rise_grid: np.ndarray        # 1D, m
    p_bistable: np.ndarray       # 2D, len(rise) x len(thickness)
    median_peak_force: np.ndarray  # 2D, N (NaN where no bistable samples)


def grid_scan(base: FlexureParams, ranges: InputRanges,
              n_thick: int = 11, n_rise: int = 11,
              n_inner: int = 64, seed: int = 20240424) -> GridResult:
    """For each ``(thickness, initial_rise)`` cell, MC over the other inputs.

    The outer grid lives in design space (variables you set when you slice
    the print). At each grid cell we draw ``n_inner`` Latin-hypercube samples
    over the *remaining* manufacturing tolerances (Young's modulus + the
    residual thickness/rise scatter that the printer adds on top of the cell
    centre, scaled to one-third of the full tolerance to avoid double
    counting), and report the fraction that come out bimodal plus the
    median peak snap force across the bimodal subset.
    """
    bounds = _bounds(base, ranges)
    thick_grid = np.linspace(bounds[0, 0], bounds[0, 1], n_thick)
    rise_grid = np.linspace(bounds[2, 0], bounds[2, 1], n_rise)

    # Inner LHS draws over Young's modulus and pre-compression at each cell.
    inner_bounds = np.array([bounds[1], bounds[3]])
    sampler = qmc.LatinHypercube(d=2, seed=seed)
    inner_unit = sampler.random(n=n_inner)
    inner_scaled = qmc.scale(inner_unit, inner_bounds[:, 0], inner_bounds[:, 1])

    # Residual print scatter inside one grid cell, in m: each cell is one
    # tolerance step wide, so the within-cell scatter is comfortably less
    # than that. Use a third for both thickness and rise.
    if n_thick > 1:
        cell_thick = (thick_grid[1] - thick_grid[0]) / 3.0
    else:
        cell_thick = 0.0
    if n_rise > 1:
        cell_rise = (rise_grid[1] - rise_grid[0]) / 3.0
    else:
        cell_rise = 0.0
    rng = np.random.default_rng(seed)
    thick_jitter = rng.uniform(-cell_thick, cell_thick, n_inner)
    rise_jitter = rng.uniform(-cell_rise, cell_rise, n_inner)

    p_bist = np.zeros((n_rise, n_thick))
    median_F = np.full((n_rise, n_thick), np.nan)
    for i, h0 in enumerate(rise_grid):
        for j, t in enumerate(thick_grid):
            forces: list[float] = []
            n_bist = 0
            for k in range(n_inner):
                E = inner_scaled[k, 0]
                pre = inner_scaled[k, 1]
                s = _evaluate(
                    thickness=max(0.05e-3, t + thick_jitter[k]),
                    youngs_modulus=E,
                    initial_rise=max(0.5e-3, h0 + rise_jitter[k]),
                    pre_compression=pre,
                    base=base,
                )
                if s.is_bimodal:
                    n_bist += 1
                    forces.append(s.peak_force)
            p_bist[i, j] = n_bist / n_inner
            if forces:
                median_F[i, j] = float(np.median(forces))

    return GridResult(thickness_grid=thick_grid, rise_grid=rise_grid,
                      p_bistable=p_bist, median_peak_force=median_F)


def recommend_robust(grid: GridResult, base: FlexureParams) -> dict[str, float]:
    """Pick the grid cell that maximises ``P(bistable)`` (ties → closest to nominal)."""
    p = grid.p_bistable
    # Argmax with tie-break toward the cell closest to (base.thickness, base.initial_rise)
    max_p = p.max()
    candidates = np.argwhere(p >= max_p - 1e-9)
    nominal_t = base.thickness
    nominal_h = base.initial_rise

    def dist(idx: np.ndarray) -> float:
        i, j = int(idx[0]), int(idx[1])
        return math.hypot((grid.thickness_grid[j] - nominal_t) / max(nominal_t, 1e-9),
                          (grid.rise_grid[i] - nominal_h) / max(nominal_h, 1e-9))

    best = min(candidates, key=dist)
    i, j = int(best[0]), int(best[1])
    return {
        "thickness_m": float(grid.thickness_grid[j]),
        "initial_rise_m": float(grid.rise_grid[i]),
        "p_bistable": float(p[i, j]),
        "median_peak_force_N": float(grid.median_peak_force[i, j])
            if not math.isnan(grid.median_peak_force[i, j]) else 0.0,
    }


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def render_violin(samples: list[Sample], out_path: Path) -> Path:
    """Violin of peak snap-force distribution, broken out by input quartile."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    bistable = [s for s in samples if s.is_bimodal]
    if not bistable:
        # Still emit an empty figure so the CI artifact is always present.
        fig, ax = plt.subplots(figsize=(7.0, 4.0))
        ax.text(0.5, 0.5, "No bistable samples — design is not robust.",
                ha="center", va="center", transform=ax.transAxes, fontsize=12)
        ax.set_axis_off()
    else:
        F = np.array([s.peak_force for s in bistable])
        fig, axes = plt.subplots(1, 4, figsize=(13.0, 4.4), sharey=True)
        for ax, key, label in zip(axes, INPUT_KEYS, INPUT_LABELS):
            x = np.array([getattr(s, key) for s in bistable])
            qs = np.quantile(x, [0.25, 0.5, 0.75])
            buckets = [F[x < qs[0]],
                       F[(x >= qs[0]) & (x < qs[1])],
                       F[(x >= qs[1]) & (x < qs[2])],
                       F[x >= qs[2]]]
            buckets = [b for b in buckets if b.size]
            if buckets:
                parts = ax.violinplot(buckets, showmedians=True)
                for pc in parts["bodies"]:
                    pc.set_alpha(0.55)
            ax.set_xticks(range(1, len(buckets) + 1))
            ax.set_xticklabels(["Q1", "Q2", "Q3", "Q4"][: len(buckets)])
            ax.set_xlabel(label)
            ax.grid(True, alpha=0.3)
        axes[0].set_ylabel("peak snap-through force  [N]")
        fig.suptitle(
            f"Peak snap force across {len(samples)} LHS samples "
            f"({len(bistable)} bistable, {len(samples) - len(bistable)} mono-stable)",
            fontsize=11,
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path)
    fig.savefig(out_path.with_suffix(".png"), dpi=120)
    plt.close(fig)
    return out_path


def render_heatmap(grid: GridResult, recommendation: dict[str, float],
                   base: FlexureParams, out_path: Path) -> Path:
    """2-D ``P(bistable)`` heatmap with the recommended cell highlighted."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.0, 4.6))
    extent = (grid.thickness_grid[0] * 1e3, grid.thickness_grid[-1] * 1e3,
              grid.rise_grid[0] * 1e3, grid.rise_grid[-1] * 1e3)

    im = axL.imshow(grid.p_bistable, extent=extent, origin="lower",
                    aspect="auto", vmin=0.0, vmax=1.0, cmap="viridis")
    fig.colorbar(im, ax=axL, label="P(bistable)")
    axL.scatter(base.thickness * 1e3, base.initial_rise * 1e3,
                marker="*", color="white", edgecolor="black", s=180,
                label=f"nominal ({base.thickness*1e3:.2f}, {base.initial_rise*1e3:.2f})")
    axL.scatter(recommendation["thickness_m"] * 1e3,
                recommendation["initial_rise_m"] * 1e3,
                marker="X", color="red", edgecolor="black", s=160,
                label=f"recommended ({recommendation['thickness_m']*1e3:.2f}, "
                      f"{recommendation['initial_rise_m']*1e3:.2f})")
    axL.set_xlabel("flexure thickness  [mm]")
    axL.set_ylabel("initial rise  [mm]")
    axL.set_title("P(bistable) over print-tolerance MC")
    axL.legend(loc="lower right", fontsize=8)

    F = grid.median_peak_force
    im2 = axR.imshow(F, extent=extent, origin="lower", aspect="auto",
                     cmap="magma")
    fig.colorbar(im2, ax=axR, label="median peak snap-through force  [N]")
    axR.scatter(base.thickness * 1e3, base.initial_rise * 1e3,
                marker="*", color="white", edgecolor="black", s=180)
    axR.scatter(recommendation["thickness_m"] * 1e3,
                recommendation["initial_rise_m"] * 1e3,
                marker="X", color="cyan", edgecolor="black", s=160)
    axR.set_xlabel("flexure thickness  [mm]")
    axR.set_ylabel("initial rise  [mm]")
    axR.set_title("Median peak snap force across bistable samples")

    fig.suptitle("Robust-design grid scan over print tolerances", fontsize=11)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path)
    fig.savefig(out_path.with_suffix(".png"), dpi=120)
    plt.close(fig)
    return out_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--samples", type=int, default=256,
                    help="number of LHS samples for the global sweep (default 256)")
    ap.add_argument("--grid-thick", type=int, default=11,
                    help="number of thickness grid points (default 11)")
    ap.add_argument("--grid-rise", type=int, default=11,
                    help="number of rise grid points (default 11)")
    ap.add_argument("--grid-inner", type=int, default=64,
                    help="inner-loop MC samples per grid cell (default 64)")
    ap.add_argument("--seed", type=int, default=20240424,
                    help="RNG seed (default 20240424)")
    ap.add_argument("--grid-only", action="store_true",
                    help="skip the global LHS sweep and only emit the heatmap")
    ap.add_argument("--no-figures", action="store_true",
                    help="skip writing matplotlib figures (just write JSON)")
    return ap.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    base = FlexureParams()
    ranges = InputRanges()

    figures = Path(__file__).resolve().parent.parent / "docs" / "figures"
    figures.mkdir(parents=True, exist_ok=True)

    summary: dict[str, object] = {}
    samples: list[Sample] = []
    if not args.grid_only:
        print(f"Drawing {args.samples} Latin-hypercube samples…")
        samples = lhs_sweep(args.samples, base, ranges, seed=args.seed)
        summary = summarise(samples)
        print(report(summary))

        if not args.no_figures:
            violin_path = figures / "bimodal-robustness-violin.svg"
            render_violin(samples, violin_path)
            print(f"  wrote {violin_path}")

    print(f"\nGrid scan: {args.grid_thick} × {args.grid_rise} cells, "
          f"{args.grid_inner} inner samples each "
          f"({args.grid_thick * args.grid_rise * args.grid_inner} total PRBM solves)…")
    grid = grid_scan(base, ranges,
                     n_thick=args.grid_thick, n_rise=args.grid_rise,
                     n_inner=args.grid_inner, seed=args.seed)
    rec = recommend_robust(grid, base)
    print(f"  recommended robust parameters:")
    print(f"    thickness    = {rec['thickness_m']*1e3:.3f} mm  "
          f"(nominal {base.thickness*1e3:.3f} mm)")
    print(f"    initial_rise = {rec['initial_rise_m']*1e3:.3f} mm  "
          f"(nominal {base.initial_rise*1e3:.3f} mm)")
    print(f"    P(bistable) at this cell = {rec['p_bistable']:.3f}")
    print(f"    median peak snap force   = {rec['median_peak_force_N']:.3f} N")

    if not args.no_figures:
        heatmap_path = figures / "bimodal-robustness-heatmap.svg"
        render_heatmap(grid, rec, base, heatmap_path)
        print(f"  wrote {heatmap_path}")

    summary["recommendation"] = rec
    summary["grid"] = {
        "thickness_mm": (grid.thickness_grid * 1e3).tolist(),
        "rise_mm": (grid.rise_grid * 1e3).tolist(),
        "p_bistable": grid.p_bistable.tolist(),
    }
    json_path = figures / "bimodal-robustness-summary.json"
    json_path.write_text(json.dumps(summary, indent=2))
    print(f"  wrote {json_path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
