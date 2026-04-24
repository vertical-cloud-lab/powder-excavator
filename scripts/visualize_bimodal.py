"""Visualisations for the bimodal compliant mechanism.

Generates two artefacts under ``docs/figures/``:

* ``bimodal-mechanism.svg`` — a four-panel static figure showing
  (A) the mechanism in its two stable poses, (B) the strain-energy
  landscape with both wells and the snap-through saddle marked,
  (C) the force-displacement curve including the negative-stiffness
  region characteristic of a snap-through bistable, and (D) the trough
  tilt as a function of apex displacement.
* ``bimodal-mechanism.gif`` — an animation of the trough snapping between
  the scoop pose and the dump pose, with the corresponding point on the
  energy curve tracked alongside.

Run from the repository root::

    python scripts/visualize_bimodal.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # noqa: E402
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyArrowPatch, Polygon, Rectangle

from scripts.bimodal_compliance import (
    AnalysisResult,
    FlexureParams,
    analyze,
    strain_energy,
)


# Fixed parameters used throughout this module — kept in sync with
# scripts.bimodal_compliance.FlexureParams() defaults.
PARAMS = FlexureParams()
TROUGH_HALF_LENGTH = 30.0e-3   # [m] visual half-length of the trough
TROUGH_HEIGHT = 6.0e-3         # [m] visual height of the trough body
ANIMATION_FRAMES = 90


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def _frame_color() -> str:
    return "#4d4d4d"


def _flexure_color(strain: float) -> str:
    """Map axial strain (compression positive) to a colour for visual feedback."""
    s = float(np.clip(abs(strain) / 0.04, 0.0, 1.0))
    # interpolate from neutral grey to a warm red for highly strained
    return matplotlib.colors.to_hex((0.85, 0.30 + 0.4 * (1.0 - s), 0.30 + 0.4 * (1.0 - s)))


def _draw_mechanism(ax: plt.Axes, y: float, p: FlexureParams = PARAMS,
                    show_axes: bool = False, label: "str | None" = None) -> None:
    """Draw the bistable trough mechanism with its apex at height ``y``."""
    b = p.half_span
    L0 = p.effective_natural_length()
    deformed = np.hypot(b, y)
    strain = (deformed - L0) / L0  # tension positive

    # Frame: ground feet
    foot_w = 4.0e-3
    foot_h = 2.0e-3
    ax.add_patch(Rectangle((-b - foot_w / 2, -foot_h), foot_w, foot_h,
                           facecolor=_frame_color(), edgecolor="black"))
    ax.add_patch(Rectangle((+b - foot_w / 2, -foot_h), foot_w, foot_h,
                           facecolor=_frame_color(), edgecolor="black"))
    # hatched ground line
    gx = np.linspace(-b - 8e-3, b + 8e-3, 2)
    ax.plot(gx, [-foot_h, -foot_h], color="black", lw=1.2)
    for x0 in np.linspace(-b - 8e-3, b + 8e-3, 18):
        ax.plot([x0, x0 - 1.5e-3], [-foot_h, -foot_h - 2.0e-3],
                color="black", lw=0.6)

    # Two flexure beams from feet to the apex at (0, y)
    flex_color = _flexure_color(strain)
    for foot_x in (-b, +b):
        ax.plot([foot_x, 0.0], [0.0, y], color=flex_color, lw=3.5,
                solid_capstyle="round")

    # Tilt of the trough is proportional to apex displacement.
    tilt = y * p.tilt_per_y  # rad
    cos_t, sin_t = np.cos(tilt), np.sin(tilt)
    # Trough as a rectangle pivoting about (0, y), drawn as an open trough
    half = TROUGH_HALF_LENGTH
    h = TROUGH_HEIGHT
    # corners in trough-local coords (x-along, y-up): bottom rectangle
    body_local = np.array([
        [-half, 0.0],
        [+half, 0.0],
        [+half, +h],
        [-half, +h],
    ])
    R = np.array([[cos_t, -sin_t], [sin_t, cos_t]])
    body_world = body_local @ R.T + np.array([0.0, y + 1.5e-3])
    ax.add_patch(Polygon(body_world, closed=True, facecolor="#dedede",
                         edgecolor="black", lw=1.2))

    # A few "powder grains" sitting in the trough that fall out when tilted
    rng = np.random.default_rng(0)
    n_grains = 18
    grains_local = np.column_stack([
        rng.uniform(-0.85 * half, 0.85 * half, n_grains),
        rng.uniform(0.5e-3, 0.9 * h, n_grains),
    ])
    keep = np.ones(n_grains, dtype=bool)
    if abs(tilt) > np.radians(3.0):
        # grains slide out of the low side once tilted past ~3 degrees
        keep = grains_local[:, 0] * np.sign(tilt) < 0.4 * half * (1.0 - abs(tilt) / np.radians(8.0))
    grains_world = grains_local[keep] @ R.T + np.array([0.0, y + 1.5e-3])
    ax.scatter(grains_world[:, 0], grains_world[:, 1], s=8,
               color="#8a5a2b", edgecolor="none", zorder=5)

    # Apex pivot dot
    ax.plot(0.0, y, marker="o", markersize=6, color="black", zorder=6)

    if label is not None:
        ax.text(0.0, -foot_h - 6.5e-3, label, ha="center", va="top",
                fontsize=10, fontweight="bold")

    ax.set_xlim(-b - 1.2e-2, b + 1.2e-2)
    ax.set_ylim(-1.0e-2, +2.5e-2)
    ax.set_aspect("equal")
    if not show_axes:
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)


# ---------------------------------------------------------------------------
# Static four-panel figure
# ---------------------------------------------------------------------------

def render_static(out_path: Path, result: AnalysisResult | None = None) -> Path:
    if result is None:
        result = analyze(PARAMS)
    wells = sorted(result.stable_wells)
    y_lo, y_hi = wells[0], wells[-1]
    unstable = [y for y, kind in result.equilibria if kind == "unstable"]

    fig = plt.figure(figsize=(10.5, 7.0))
    gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.25)

    # Panel A: mechanism in its two stable poses
    axA = fig.add_subplot(gs[0, 0])
    axA.set_title("(A) Two stable poses of the bimodal trough", fontsize=11)
    # draw both poses as a side-by-side composite by overlaying with alpha
    # — easier to read if we use two stacked sub-axes within Panel A.
    axA.axis("off")
    inner = gs[0, 0].subgridspec(1, 2, wspace=0.05)
    axA1 = fig.add_subplot(inner[0, 0])
    axA2 = fig.add_subplot(inner[0, 1])
    _draw_mechanism(axA1, y_lo, label=f"scoop pose\n(y = {y_lo*1e3:+.2f} mm)")
    _draw_mechanism(axA2, y_hi, label=f"dump pose\n(y = {y_hi*1e3:+.2f} mm)")

    # Panel B: energy landscape
    axB = fig.add_subplot(gs[0, 1])
    axB.plot(result.y * 1e3, result.energy * 1e3, color="tab:blue", lw=2.0)
    for y_eq, kind in result.equilibria:
        U_eq = float(strain_energy(y_eq, PARAMS)) * 1e3
        if kind == "stable":
            axB.plot(y_eq * 1e3, U_eq, "o", color="tab:green",
                     markersize=9, label="stable" if y_eq == y_lo else None)
        else:
            axB.plot(y_eq * 1e3, U_eq, "X", color="tab:red",
                     markersize=10, label="unstable")
    # annotate barrier height
    if result.barrier_height > 0 and unstable:
        y_u = unstable[0]
        U_top = float(strain_energy(y_u, PARAMS)) * 1e3
        U_well = float(strain_energy(y_lo, PARAMS)) * 1e3
        axB.annotate("", xy=(y_u * 1e3, U_top), xytext=(y_u * 1e3, U_well),
                     arrowprops=dict(arrowstyle="<->", color="black"))
        axB.text(y_u * 1e3 + 0.25, 0.5 * (U_top + U_well),
                 f"$\\Delta U$ = {result.barrier_height*1e3:.2f} mJ",
                 fontsize=9, va="center")
    axB.set_xlabel("apex displacement  $y$  [mm]")
    axB.set_ylabel("strain energy  $U$  [mJ]")
    axB.set_title("(B) Double-well energy landscape", fontsize=11)
    axB.grid(True, alpha=0.3)
    axB.legend(loc="upper right", fontsize=9, frameon=False, ncols=1)
    # zoom in on the double well so it's clearly visible (the steep outer
    # walls extend to ~200 mJ which would otherwise hide the 2.9 mJ barrier)
    if unstable:
        U_top = float(strain_energy(unstable[0], PARAMS)) * 1e3
        axB.set_ylim(-0.2 * U_top, 3.5 * U_top + 1.0)
    axB.set_xlim(-1.6 * abs(y_lo) * 1e3, +1.6 * abs(y_hi) * 1e3)

    # Panel C: force vs displacement
    axC = fig.add_subplot(gs[1, 0])
    axC.plot(result.y * 1e3, result.force, color="tab:orange", lw=2.0)
    axC.axhline(0.0, color="black", lw=0.5)
    # shade the negative-stiffness (snap-through) region
    mask = (result.y >= y_lo) & (result.y <= y_hi)
    axC.fill_between(result.y[mask] * 1e3, 0, result.force[mask],
                     where=result.force[mask] > 0, color="tab:orange", alpha=0.15)
    axC.fill_between(result.y[mask] * 1e3, 0, result.force[mask],
                     where=result.force[mask] < 0, color="tab:orange", alpha=0.15)
    for y_eq, kind in result.equilibria:
        marker = "o" if kind == "stable" else "X"
        color = "tab:green" if kind == "stable" else "tab:red"
        axC.plot(y_eq * 1e3, 0.0, marker=marker, color=color, markersize=9)
    axC.text(0.05, 0.95,
             f"peak snap-through force\n$F_{{\\max}}$ = {result.snap_through_force:.2f} N",
             transform=axC.transAxes, fontsize=9, va="top",
             bbox=dict(boxstyle="round", fc="white", ec="0.7"))
    axC.set_xlabel("apex displacement  $y$  [mm]")
    axC.set_ylabel(r"restoring force  $F = -\,dU/dy$  [N]")
    axC.set_title("(C) Force-displacement (snap-through region)", fontsize=11)
    axC.grid(True, alpha=0.3)
    # zoom around the bistable region
    F_max = result.snap_through_force
    axC.set_ylim(-3.5 * F_max, 3.5 * F_max)
    axC.set_xlim(-1.6 * abs(y_lo) * 1e3, +1.6 * abs(y_hi) * 1e3)

    # Panel D: trough tilt vs apex displacement
    axD = fig.add_subplot(gs[1, 1])
    tilt_deg = np.degrees(result.y * PARAMS.tilt_per_y)
    axD.plot(result.y * 1e3, tilt_deg, color="tab:purple", lw=2.0)
    for y_eq, kind in result.equilibria:
        marker = "o" if kind == "stable" else "X"
        color = "tab:green" if kind == "stable" else "tab:red"
        axD.plot(y_eq * 1e3, np.degrees(y_eq * PARAMS.tilt_per_y),
                 marker=marker, color=color, markersize=9)
    axD.set_xlabel("apex displacement  $y$  [mm]")
    axD.set_ylabel("trough tilt  [deg]")
    axD.set_title("(D) Trough tilt vs apex displacement", fontsize=11)
    axD.grid(True, alpha=0.3)

    fig.suptitle(
        f"Bimodal compliant mechanism — von Mises truss flexure pair  "
        f"(bistable: {result.is_bimodal})",
        fontsize=12, y=1.02,
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    return out_path


# ---------------------------------------------------------------------------
# Animated snap-through GIF
# ---------------------------------------------------------------------------

def _snap_trajectory(result: AnalysisResult,
                     n_frames: int = ANIMATION_FRAMES) -> np.ndarray:
    """A smooth back-and-forth y(t) that visits both wells via the saddle."""
    wells = sorted(result.stable_wells)
    y_lo, y_hi = wells[0], wells[-1]
    # half cycle: lo -> hi via raised cosine, then mirror
    t = np.linspace(0.0, 1.0, n_frames // 2, endpoint=False)
    half = y_lo + (y_hi - y_lo) * 0.5 * (1.0 - np.cos(np.pi * t))
    return np.concatenate([half, half[::-1]])


def render_animation(out_path: Path, result: AnalysisResult | None = None,
                     fps: int = 18) -> Path:
    if result is None:
        result = analyze(PARAMS)
    ys = _snap_trajectory(result)

    fig = plt.figure(figsize=(8.5, 4.0))
    gs = GridSpec(1, 2, figure=fig, width_ratios=[1.1, 1.0], wspace=0.25)
    ax_mech = fig.add_subplot(gs[0, 0])
    ax_eng = fig.add_subplot(gs[0, 1])

    ax_eng.plot(result.y * 1e3, result.energy * 1e3, color="tab:blue", lw=2.0)
    for y_eq, kind in result.equilibria:
        marker = "o" if kind == "stable" else "X"
        color = "tab:green" if kind == "stable" else "tab:red"
        ax_eng.plot(y_eq * 1e3, float(strain_energy(y_eq, PARAMS)) * 1e3,
                    marker=marker, color=color, markersize=9)
    cursor, = ax_eng.plot([], [], marker="o", color="black",
                          markersize=10, markerfacecolor="white", zorder=6)
    ax_eng.set_xlabel("apex displacement  $y$  [mm]")
    ax_eng.set_ylabel("strain energy  $U$  [mJ]")
    ax_eng.set_title("energy landscape")
    ax_eng.grid(True, alpha=0.3)

    def init():
        return (cursor,)

    def update(i):
        ax_mech.clear()
        y = float(ys[i])
        _draw_mechanism(ax_mech, y, label=f"y = {y*1e3:+.2f} mm")
        ax_mech.set_title("snap-through animation")
        cursor.set_data([y * 1e3], [float(strain_energy(y, PARAMS)) * 1e3])
        return (cursor,)

    anim = FuncAnimation(fig, update, init_func=init,
                         frames=len(ys), interval=1000 // fps, blit=False)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    anim.save(out_path, writer=PillowWriter(fps=fps))
    plt.close(fig)
    return out_path


def main() -> int:
    figures = Path(__file__).resolve().parent.parent / "docs" / "figures"
    result = analyze(PARAMS)
    print(result.summary())
    static = render_static(figures / "bimodal-mechanism.svg", result)
    print(f"Wrote static figure  to {static}")
    static_png = render_static(figures / "bimodal-mechanism.png", result)
    print(f"Wrote static figure  to {static_png}")
    gif = render_animation(figures / "bimodal-mechanism.gif", result)
    print(f"Wrote animation       to {gif}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
