"""Tests for the bimodal-compliance analyzer.

These tests check the qualitative behaviour we rely on when designing the
bistable compliant trough: with the default parameters the mechanism must be
bimodal (exactly two stable equilibria, one unstable equilibrium between
them, and a positive snap-through energy barrier); and the analyzer must
correctly classify obvious mono-stable configurations as *not* bimodal.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from scripts.bimodal_compliance import (
    AnalysisResult,
    FlexureParams,
    analyze,
    force,
    strain_energy,
)


def test_default_design_is_bimodal() -> None:
    result = analyze()
    assert result.is_bimodal, result.summary()
    assert len(result.stable_wells) == 2
    assert result.barrier_height > 0.0
    assert result.snap_through_force > 0.0


def test_default_design_has_symmetric_wells() -> None:
    result = analyze()
    y_lo, y_hi = sorted(result.stable_wells)
    assert math.isclose(y_lo, -y_hi, rel_tol=1e-3, abs_tol=1e-6)
    # the unstable equilibrium between the wells sits at y = 0
    unstable = [y for y, k in result.equilibria if k == "unstable"]
    assert len(unstable) == 1
    assert abs(unstable[0]) < 1e-6


def test_well_locations_match_closed_form() -> None:
    """Closed-form well location for the von Mises truss:
    ``y_well = sqrt(L0**2 - b**2)`` where L0 is the natural length and b is
    the half-span."""
    p = FlexureParams()
    expected = math.sqrt(p.effective_natural_length() ** 2 - p.half_span ** 2)
    measured = max(abs(y) for y in analyze(p).stable_wells)
    assert math.isclose(measured, expected, rel_tol=1e-3, abs_tol=1e-6)


def test_force_is_zero_at_each_equilibrium() -> None:
    p = FlexureParams()
    result = analyze(p)
    for y_eq, _kind in result.equilibria:
        assert abs(float(force(y_eq, p))) < 1e-3  # newtons


def test_taut_truss_is_not_bimodal() -> None:
    """Closed-form bistability condition for a symmetric von Mises truss:
    ``L0 > b`` (natural length exceeds the half-span). If we instead choose
    ``L0 <= b`` the truss is always taut, the only equilibrium is at y = 0,
    and the design is *not* bimodal."""
    p_built = FlexureParams()
    p = FlexureParams(natural_length=p_built.half_span)  # L0 = b
    result = analyze(p)
    assert not result.is_bimodal
    assert len(result.stable_wells) <= 1


def test_strain_energy_is_nonnegative_and_minimum_at_wells() -> None:
    p = FlexureParams()
    result = analyze(p)
    assert np.all(result.energy >= -1e-15)
    for y_well in result.stable_wells:
        # energy at a stable well is no greater than the central barrier value
        U_well = float(strain_energy(y_well, p))
        U_center = float(strain_energy(0.0, p))
        assert U_well <= U_center + 1e-12


def test_result_summary_contains_key_fields() -> None:
    result: AnalysisResult = analyze()
    text = result.summary()
    assert "bimodal" in text.lower()
    assert "snap-through" in text.lower()
    assert "stable wells" in text.lower()


@pytest.mark.parametrize("rise_mm", [4.0, 5.0, 6.0])
def test_bimodality_robust_to_initial_rise(rise_mm: float) -> None:
    """Bistability should be preserved across a range of as-built rises,
    provided the rise is large enough that ``L0 > b`` after pre-compression
    (closed-form: ``h0 > b * sqrt(2 * pre_compression)`` for small
    pre-compression). For the default 1.5% pre-compression and 20 mm
    half-span, that threshold is ~3.46 mm; the rises chosen here all clear
    it comfortably."""
    p = FlexureParams(initial_rise=rise_mm * 1e-3)
    assert analyze(p).is_bimodal
