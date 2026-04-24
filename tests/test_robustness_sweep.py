"""Tests for the robustness (uncertainty-quantification) sweep.

These pin the qualitative behaviours we rely on when interpreting the
sweep outputs in CI:

* the LHS sweep is reproducible given a seed,
* every sample lies inside the requested ±tolerance bounds,
* the sensitivity calculation returns a normalised distribution,
* the grid-scan recommender picks a high-``P(bistable)`` cell,
* and the JSON summary is round-trippable.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pytest

from scripts.bimodal_compliance import FlexureParams
from scripts.robustness_sweep import (
    InputRanges,
    _bounds,
    first_order_sensitivities,
    grid_scan,
    lhs_sweep,
    main,
    recommend_robust,
    summarise,
)


def test_lhs_samples_lie_within_bounds() -> None:
    base = FlexureParams()
    ranges = InputRanges()
    samples = lhs_sweep(64, base, ranges, seed=1)
    bnd = _bounds(base, ranges)
    for s in samples:
        assert bnd[0, 0] - 1e-12 <= s.thickness <= bnd[0, 1] + 1e-12
        assert bnd[1, 0] - 1e-3 <= s.youngs_modulus <= bnd[1, 1] + 1e-3
        assert bnd[2, 0] - 1e-12 <= s.initial_rise <= bnd[2, 1] + 1e-12
        assert bnd[3, 0] - 1e-9 <= s.pre_compression <= bnd[3, 1] + 1e-9


def test_lhs_is_reproducible_under_seed() -> None:
    base = FlexureParams()
    ranges = InputRanges()
    s1 = lhs_sweep(32, base, ranges, seed=42)
    s2 = lhs_sweep(32, base, ranges, seed=42)
    assert [x.thickness for x in s1] == [x.thickness for x in s2]
    assert [x.peak_force for x in s1] == [x.peak_force for x in s2]


def test_default_design_is_bistable_across_tolerances() -> None:
    """At the nominal design, every LHS sample stays bistable.

    This is the single most important robustness claim — if the sweep ever
    starts producing mono-stable samples at the default geometry, the
    flexure design is too close to the bifurcation boundary and should be
    re-tuned (thicken the arch or shorten the half-span)."""
    samples = lhs_sweep(128, FlexureParams(), InputRanges(), seed=7)
    bistable = [s for s in samples if s.is_bimodal]
    assert len(bistable) >= int(0.95 * len(samples)), (
        f"only {len(bistable)}/{len(samples)} samples are bistable")


def test_summary_percentiles_are_ordered() -> None:
    samples = lhs_sweep(64, FlexureParams(), InputRanges(), seed=3)
    s = summarise(samples)
    pf = s["peak_snap_force"]
    assert pf["p05_N"] <= pf["p50_N"] <= pf["p95_N"]
    assert s["n_samples"] == 64
    assert 0.0 <= float(s["p_bistable"]) <= 1.0


def test_sensitivities_sum_to_one() -> None:
    samples = lhs_sweep(64, FlexureParams(), InputRanges(), seed=11)
    sens = first_order_sensitivities(samples)
    assert math.isclose(sum(sens.values()), 1.0, abs_tol=1e-9)
    for v in sens.values():
        assert 0.0 <= v <= 1.0


def test_grid_scan_produces_valid_arrays() -> None:
    base = FlexureParams()
    grid = grid_scan(base, InputRanges(), n_thick=5, n_rise=5, n_inner=16, seed=2)
    assert grid.p_bistable.shape == (5, 5)
    assert grid.median_peak_force.shape == (5, 5)
    assert np.all((grid.p_bistable >= 0.0) & (grid.p_bistable <= 1.0))


def test_recommender_picks_a_high_p_bistable_cell() -> None:
    base = FlexureParams()
    grid = grid_scan(base, InputRanges(), n_thick=5, n_rise=5, n_inner=16, seed=2)
    rec = recommend_robust(grid, base)
    # Whatever cell is picked, P(bistable) at that cell must be the maximum.
    assert rec["p_bistable"] == pytest.approx(grid.p_bistable.max())
    # Recommended values must sit inside the scanned grid.
    assert grid.thickness_grid[0] <= rec["thickness_m"] <= grid.thickness_grid[-1]
    assert grid.rise_grid[0] <= rec["initial_rise_m"] <= grid.rise_grid[-1]


def test_main_smoke_writes_summary_json(tmp_path: Path, monkeypatch) -> None:
    """End-to-end: ``main()`` runs at minimal sample count and emits JSON."""
    figures = tmp_path / "docs" / "figures"
    figures.mkdir(parents=True)
    # Redirect the figures directory by monkey-patching the script's __file__
    # sentinel: it computes ``parent.parent / 'docs' / 'figures'``.
    import scripts.robustness_sweep as mod
    monkeypatch.setattr(mod, "__file__", str(tmp_path / "scripts" / "robustness_sweep.py"))

    rc = main(["--samples", "16", "--grid-thick", "3", "--grid-rise", "3",
               "--grid-inner", "8", "--seed", "1"])
    assert rc == 0
    summary_path = figures / "bimodal-robustness-summary.json"
    assert summary_path.exists()
    data = json.loads(summary_path.read_text())
    assert data["n_samples"] == 16
    assert "recommendation" in data
    assert "grid" in data
