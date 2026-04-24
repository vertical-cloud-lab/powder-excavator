"""Render the parametric CAD model to SVG views of the actual 3D geometry.

Where ``scripts/generate_figures.py`` draws hand-laid-out *schematic* figures
that explain the design intent, this module produces *honest renders* of the
geometry returned by :mod:`cad.excavator` — i.e.\\ what the part will
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

* The same isometric projection direction is used for every part so they
  all read as views of the same coordinate system.

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

# Shared SVG exporter options. Picked so every part renders into the same
# isometric viewpoint with hidden-line dashes turned on, which is what a
# reader expects from a "CAD render" — a clean orthographic-style line
# drawing rather than a shaded raster.
_BASE_OPT: dict[str, Any] = {
    "width": 720,
    "height": 540,
    "marginLeft": 20,
    "marginTop": 20,
    "showAxes": False,
    "projectionDir": (1.0, -1.0, 0.6),  # iso-ish: looks down +Z, from +X / -Y
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

    # Full assembly — collapse to a single Compound so the SVG exporter can
    # project it. ``toCompound`` preserves the per-instance placements.
    asm = build_assembly(p)
    out = _render(asm.toCompound(), "assembly", width=900, height=600)
    print(f"wrote {out.relative_to(REPO_ROOT)}")


if __name__ == "__main__":  # pragma: no cover
    main()
