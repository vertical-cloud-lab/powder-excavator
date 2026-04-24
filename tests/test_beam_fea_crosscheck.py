"""Tests for the higher-end B32-beam FEA cross-check.

The CalculiX integration test runs the full sweep at reduced fidelity (so it
fits in CI time) and only when ``ccx`` is installed; the closed-form bending
estimate and the equilibrium-locator helper are tested unconditionally.
"""

from __future__ import annotations

import shutil

import numpy as np
import pytest

from scripts.beam_fea_crosscheck import (
    BeamSweepResult,
    _equilibria_from_curve,
    bending_force,
    report,
    run_sweep,
)
from scripts.bimodal_compliance import FlexureParams


def test_bending_force_is_linear_and_restoring() -> None:
    """The closed-form bending estimate is a linear restoring force in ``y``."""
    p = FlexureParams()
    y = np.linspace(-2e-3, 2e-3, 5)
    F = np.asarray(bending_force(y, p))
    # Restoring (sign opposite to y) and exactly anti-symmetric.
    assert np.all(F[y > 0] < 0)
    assert np.all(F[y < 0] > 0)
    assert np.allclose(F, -F[::-1], atol=1e-12)
    # Linear in y → F/y is constant where y != 0.
    nz = y != 0
    ratios = F[nz] / y[nz]
    assert np.allclose(ratios, ratios[0], rtol=1e-12)


def test_bending_stiffness_scales_as_thickness_cubed() -> None:
    """k_bend ∝ t³ — the dominant manufacturing-tolerance lever."""
    base = FlexureParams()
    # F at y = 1 mm gives the linear stiffness sign-flipped.
    k_base = -float(bending_force(1.0e-3, base))
    thicker = FlexureParams(thickness=base.thickness * 2.0)
    k_thicker = -float(bending_force(1.0e-3, thicker))
    assert k_thicker / k_base == pytest.approx(8.0, rel=1e-9)


def test_equilibria_locator_finds_known_zeros() -> None:
    """A clean cubic with three real zeros at y = -1, 0, +1 (in mm)."""
    y = np.linspace(-2.0, 2.0, 401) * 1e-3
    # F(y) = -y * (y-1e-3) * (y+1e-3): stable at ±1mm, unstable at 0
    F = -y * (y - 1e-3) * (y + 1e-3) * 1e9
    eqs = _equilibria_from_curve(y, F)
    kinds = {round(y_eq * 1e3, 3): kind for y_eq, kind in eqs}
    assert kinds.get(-1.0) == "stable"
    assert kinds.get(0.0) == "unstable"
    assert kinds.get(1.0) == "stable"


def test_report_handles_empty_sweep() -> None:
    text = report([], FlexureParams())
    assert "no converged" in text.lower()


def test_report_warns_when_fea_loses_bistability() -> None:
    """If the FEA only finds one well, the human-readable report must warn."""
    # A monotonic-ish synthetic curve with a single zero (one stable well).
    ys = np.linspace(-3e-3, 3e-3, 7)
    Fs = -ys * 1000.0  # strictly restoring → single equilibrium at y = 0
    results = [BeamSweepResult(y=float(y), force=float(F)) for y, F in zip(ys, Fs)]
    text = report(results, FlexureParams())
    assert "warning" in text.lower()


@pytest.mark.skipif(shutil.which("ccx") is None,
                    reason="CalculiX (ccx) not installed; skipping integration test")
def test_b32_sweep_runs_and_produces_points() -> None:
    """Smoke-test the full pipeline at reduced fidelity to keep CI fast."""
    # 9 displacement points × 6 elements per half ≈ 10 s on a stock runner.
    results = run_sweep(FlexureParams(), n_steps=9, n_seg_per_half=6)
    assert len(results) == 9
    ys = np.array([r.y for r in results])
    Fs = np.array([r.force for r in results])
    # Sweep covers both wells worth of range.
    assert ys.min() < -1e-3 and ys.max() > 1e-3
    # FEA gives finite forces, with restoring sign in the deep-displacement
    # regime (push the apex well below the feet line, force pushes it back up).
    assert np.all(np.isfinite(Fs))
    assert Fs[ys.argmin()] > 0.0
