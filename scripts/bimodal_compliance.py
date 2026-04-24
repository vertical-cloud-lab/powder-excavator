"""Bimodal-compliance analyzer for the powder-excavator secondary design.

This module implements a small, self-contained numerical check for whether a
candidate compliant trough/scoop mechanism is *bimodal* — i.e. has exactly two
stable equilibria (the "scoop" pose and the "dump" pose) separated by a
finite snap-through energy barrier.

The mechanism we evaluate here is the classical *von Mises truss*
(a.k.a. shallow inverted-V truss) used as the canonical bistable compliant
primitive in the compliant-mechanism literature (see Howell, *Compliant
Mechanisms*, Wiley 2001, Ch. 6). Two symmetric prismatic flexures are pinned
to a moving carrier (the trough's tilt axis) at their apex and to ground at
their feet. The carrier moves vertically by ``y``; for small angles the tilt
of the trough is proportional to ``y``. With the flexures slightly
pre-compressed so the apex starts above the dead-centre line, the elastic
strain energy ``U(y)`` is a double well in ``y`` and the design is bimodal.

Running this file as a script prints a human-readable report and writes a
plot of the energy and force curves to ``docs/figures/bimodal-energy.svg``.
The :func:`analyze` function is also imported by the test-suite.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from scipy.optimize import brentq


# ---------------------------------------------------------------------------
# Mechanism parameters
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class FlexureParams:
    """Parameters of one symmetric pair of pre-compressed flexure beams.

    Units are SI (metres, newtons, pascals). Defaults correspond to a small
    PETG flexure pair sized for a benchtop powder-excavator trough that snaps
    between a "scoop" pose and a "dump" pose.
    """

    # Geometry of the inverted-V truss in its as-fabricated (unloaded) state.
    half_span: float = 20.0e-3        # b: horizontal distance from apex to foot [m]
    initial_rise: float = 4.0e-3      # h0: initial vertical rise of apex above feet [m]
    natural_length: float | None = None  # L0: natural (stress-free) flexure length [m]

    # Material / cross-section (rectangular flexure beam).
    youngs_modulus: float = 2.0e9     # E (PETG) [Pa]
    width: float = 6.0e-3             # b_x (in-plane width)  [m]
    thickness: float = 0.6e-3         # t   (out-of-plane thickness, bending direction) [m]

    # Trough kinematics: tilt angle (rad) per metre of apex travel ``y``.
    # For the powder-excavator the trough rocks about a longitudinal pivot
    # driven by the apex; this is set so a full snap from one well to the
    # other corresponds to roughly a 30 deg trough tilt.
    tilt_per_y: float = 60.0          # [rad / m]

    # Fractional axial pre-compression applied at assembly when
    # ``natural_length`` is left as None. 0.015 = 1.5%, comfortably above the
    # snap-through threshold for the default geometry.
    pre_compression: float = 0.015

    def axial_stiffness(self) -> float:
        """Axial (k = EA/L0) stiffness of one flexure beam [N/m]."""
        area = self.width * self.thickness
        return self.youngs_modulus * area / self.effective_natural_length()

    def effective_natural_length(self) -> float:
        """Stress-free flexure length L0.

        If ``natural_length`` is supplied it is returned verbatim. Otherwise
        L0 is set shorter than the as-fabricated chord by ``pre_compression``
        so the truss is axially pre-compressed when assembled — the standard
        recipe for obtaining bistability from a shallow inverted-V truss.
        """
        if self.natural_length is not None:
            return self.natural_length
        as_built = float(np.hypot(self.half_span, self.initial_rise))
        return as_built * (1.0 - self.pre_compression)


@dataclass
class AnalysisResult:
    """Result of :func:`analyze`."""

    y: np.ndarray
    energy: np.ndarray            # U(y) [J]
    force: np.ndarray             # -dU/dy [N]
    equilibria: list[tuple[float, str]] = field(default_factory=list)
    stable_wells: list[float] = field(default_factory=list)
    barrier_height: float = 0.0   # [J]
    snap_through_force: float = 0.0  # peak |F| between wells [N]
    params: "FlexureParams | None" = None

    @property
    def is_bimodal(self) -> bool:
        """True iff exactly two stable equilibria exist with a positive barrier."""
        return len(self.stable_wells) == 2 and self.barrier_height > 0.0

    def summary(self) -> str:
        tilt_per_y = self.params.tilt_per_y if self.params is not None else 60.0
        lines = ["Bimodal-compliance analysis"]
        lines.append("-" * len(lines[0]))
        for y_eq, kind in self.equilibria:
            tilt_deg = np.degrees(y_eq * tilt_per_y)
            lines.append(
                f"  equilibrium at y = {y_eq*1e3:+7.3f} mm "
                f"(tilt ~ {tilt_deg:+6.2f} deg) -> {kind}"
            )
        lines.append(f"  stable wells: {len(self.stable_wells)}")
        lines.append(f"  snap-through energy barrier: {self.barrier_height*1e3:.4f} mJ")
        lines.append(f"  peak snap-through force:    {self.snap_through_force:.3f} N")
        lines.append(f"  bimodal: {self.is_bimodal}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Energy model (von Mises truss with two symmetric axial-spring flexures)
# ---------------------------------------------------------------------------

ArrayLike = np.ndarray | float


def strain_energy(y: ArrayLike, p: FlexureParams) -> ArrayLike:
    """Total elastic strain energy of the symmetric flexure pair.

    The apex is at height ``y`` above the line of the feet; each flexure has
    deformed length ``L(y) = sqrt(b^2 + y^2)`` and natural length ``L0``.
    Two flexures contribute, hence the factor of 2 absorbed below.
    """
    k = p.axial_stiffness()
    L0 = p.effective_natural_length()
    L = np.hypot(p.half_span, y)
    return k * (L - L0) ** 2  # 2 * (1/2) * k * (L - L0)^2


def force(y: ArrayLike, p: FlexureParams, dy: float = 1e-7) -> ArrayLike:
    """Generalised force on the apex, F = -dU/dy, by central differences."""
    y_arr = np.asarray(y, dtype=float)
    return -(strain_energy(y_arr + dy, p) - strain_energy(y_arr - dy, p)) / (2.0 * dy)


def _find_roots(y: np.ndarray, f: np.ndarray, fn) -> list[float]:
    roots: list[float] = []
    for i in range(len(y) - 1):
        if f[i] == 0.0:
            roots.append(float(y[i]))
        elif f[i] * f[i + 1] < 0.0:
            try:
                roots.append(float(brentq(fn, y[i], y[i + 1])))
            except ValueError:
                continue
    out: list[float] = []
    for r in roots:
        if not out or abs(r - out[-1]) > 1e-9:
            out.append(r)
    return out


def analyze(p: FlexureParams | None = None,
            y_range: tuple[float, float] | None = None,
            n_samples: int = 4001) -> AnalysisResult:
    """Sample ``U(y)`` and ``F(y)``, locate equilibria, classify them, and
    measure the snap-through barrier between stable wells.
    """
    if p is None:
        p = FlexureParams()
    if y_range is None:
        margin = 1.5 * max(p.initial_rise, 1e-3)
        y_range = (-margin, +margin)

    y = np.linspace(y_range[0], y_range[1], n_samples)
    U = np.asarray(strain_energy(y, p))
    F = np.asarray(force(y, p))

    fn = lambda yy: float(force(yy, p))
    eq_points = _find_roots(y, F, fn)

    classified: list[tuple[float, str]] = []
    stable_wells: list[float] = []
    h = 1e-6
    for y_eq in eq_points:
        d2U = (float(strain_energy(y_eq + h, p))
               - 2.0 * float(strain_energy(y_eq, p))
               + float(strain_energy(y_eq - h, p))) / h ** 2
        if d2U > 0.0:
            classified.append((y_eq, "stable"))
            stable_wells.append(y_eq)
        elif d2U < 0.0:
            classified.append((y_eq, "unstable"))
        else:
            classified.append((y_eq, "neutral"))

    barrier = 0.0
    snap_force = 0.0
    if len(stable_wells) >= 2:
        wells_sorted = sorted(stable_wells)
        y_lo, y_hi = wells_sorted[0], wells_sorted[-1]
        mask = (y >= y_lo) & (y <= y_hi)
        U_well = min(float(strain_energy(y_lo, p)), float(strain_energy(y_hi, p)))
        barrier = float(U[mask].max() - U_well)
        snap_force = float(np.abs(F[mask]).max())

    return AnalysisResult(
        y=y,
        energy=U,
        force=F,
        equilibria=classified,
        stable_wells=stable_wells,
        barrier_height=barrier,
        snap_through_force=snap_force,
        params=p,
    )


# ---------------------------------------------------------------------------
# CLI / plotting
# ---------------------------------------------------------------------------

def _plot(result: AnalysisResult, out_path: Path) -> None:  # pragma: no cover - I/O
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    p = result.params or FlexureParams()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.4, 5.0), sharex=True)
    ax1.plot(result.y * 1e3, result.energy * 1e3, color="tab:blue")
    ax1.set_ylabel("strain energy U  [mJ]")
    ax1.set_title("Bimodal compliant mechanism — energy landscape")
    ax1.grid(True, alpha=0.3)

    ax2.plot(result.y * 1e3, result.force, color="tab:orange")
    ax2.axhline(0.0, color="black", lw=0.5)
    ax2.set_xlabel("apex displacement y  [mm]")
    ax2.set_ylabel("restoring force F  [N]")
    ax2.grid(True, alpha=0.3)

    for y_eq, kind in result.equilibria:
        marker = "o" if kind == "stable" else "x"
        ax1.plot(y_eq * 1e3, float(strain_energy(y_eq, p)) * 1e3,
                 marker=marker, color="black")
        ax2.plot(y_eq * 1e3, 0.0, marker=marker, color="black")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def main() -> int:  # pragma: no cover - CLI entry-point
    params = FlexureParams()
    result = analyze(params)
    print(result.summary())

    out = Path(__file__).resolve().parent.parent / "docs" / "figures" / "bimodal-energy.svg"
    _plot(result, out)
    print(f"\nWrote energy/force plot to {out}")
    return 0 if result.is_bimodal else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
