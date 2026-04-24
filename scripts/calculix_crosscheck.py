#!/usr/bin/env python3
"""CalculiX cross-check of the bimodal-compliance PRBM model.

This script complements ``scripts/bimodal_compliance.py`` (analytical
Pseudo-Rigid-Body Model) by re-solving the same von Mises truss problem with
the open-source CalculiX FEA solver. It serves two purposes:

1. **Independent verification.** It confirms that the PRBM force-displacement
   curve agrees with a geometrically-nonlinear truss FEA solve.
2. **Demonstrate that the FEA path is viable.** Earlier design-doc text
   dismissed CalculiX/SfePy as "heavyweight"; this script shows the
   CalculiX route works fine for this small problem on a stock Ubuntu
   runner with ``sudo apt-get install -y calculix-ccx``. We keep PRBM as
   the primary tool because it's instant and CI-friendly, but CalculiX
   remains available as soon as we want flexure stress / fatigue results
   that PRBM can't give.

Usage::

    sudo apt-get install -y calculix-ccx       # one-time, ~50 MB
    python scripts/calculix_crosscheck.py      # writes the comparison plot

Tested with ``ccx`` 2.21 on Ubuntu 24.04.
"""

from __future__ import annotations

import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

from scripts.bimodal_compliance import FlexureParams, analyze


def _build_inp(b: float, h0: float, E: float, A: float, alpha: float,
               dT: float, y_target: float) -> str:
    """Build a CalculiX input deck for one displacement target.

    Pre-compression is baked in via thermal contraction (``alpha * dT``)
    rather than ``*INITIAL CONDITIONS, TYPE=STRESS`` because the latter
    requires per-integration-point stress records that CalculiX 2.21's
    truss elements don't accept cleanly.
    """
    return f"""*HEADING
von Mises truss snap-through (PRBM cross-check)
*NODE, NSET=NALL
1, {-b:.6e}, 0.0, 0.0
2,  0.0,    {h0:.6e}, 0.0
3, {+b:.6e}, 0.0, 0.0
*NSET, NSET=NAPEX
2
*ELEMENT, TYPE=T3D2, ELSET=ETRUSS
1, 1, 2
2, 2, 3
*MATERIAL, NAME=PETG
*ELASTIC
 {E:.3e}, 0.30
*EXPANSION
 {alpha:.3e}
*SOLID SECTION, ELSET=ETRUSS, MATERIAL=PETG
 {A:.3e}
*BOUNDARY
1, 1, 3
3, 1, 3
2, 1, 1
2, 3, 3
*INITIAL CONDITIONS, TYPE=TEMPERATURE
NALL, 0.0
*STEP, NLGEOM, INC=400
*STATIC
 0.05, 1.0
*TEMPERATURE
NALL, {dT:.3e}
*BOUNDARY
 2, 2, 2, {y_target - h0:.6e}
*NODE PRINT, NSET=NAPEX, FREQUENCY=1000
 RF
*END STEP
"""


def run_sweep(p: FlexureParams = FlexureParams(),
              n_steps: int = 64,
              y_max_factor: float = 1.6) -> tuple[list[float], list[float]]:
    """Sweep apex displacement and return ``(positions, forces)`` from CalculiX."""
    if shutil.which("ccx") is None:
        raise RuntimeError(
            "CalculiX (`ccx`) not found in PATH. Install with "
            "`sudo apt-get install -y calculix-ccx`."
        )

    L_built = math.hypot(p.half_span, p.initial_rise)
    L0 = p.effective_natural_length()
    pre = (L_built - L0) / L_built
    alpha = 1.0e-3
    dT = -pre / alpha  # axial strain = alpha*dT, want strain = -pre
    A = p.width * p.thickness

    y_targets = [
        p.initial_rise * (y_max_factor - 2.0 * y_max_factor * i / (n_steps - 1))
        for i in range(n_steps)
    ]
    positions: list[float] = []
    forces: list[float] = []

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        inp_path = tmp_path / "truss.inp"
        dat_path = tmp_path / "truss.dat"
        for k, y in enumerate(y_targets):
            inp_path.write_text(_build_inp(p.half_span, p.initial_rise,
                                           p.youngs_modulus, A, alpha, dT, y))
            r = subprocess.run(
                ["ccx", "truss"], cwd=tmp_path,
                capture_output=True, text=True, timeout=30,
            )
            if r.returncode != 0 or not dat_path.exists():
                continue
            dat = dat_path.read_text()
            blocks = list(re.finditer(
                r"forces.*?\n\s*2\s+([-\dEe.+]+)\s+([-\dEe.+]+)\s+([-\dEe.+]+)",
                dat, re.DOTALL,
            ))
            if not blocks:
                continue
            fy = float(blocks[-1].group(2))
            # *NODE PRINT RF gives reaction; flip sign so positive F means
            # restoring force opposing positive y, matching the PRBM convention.
            positions.append(y)
            forces.append(-fy)

    return positions, forces


def render_comparison(positions: list[float], forces: list[float],
                      out_path: Path,
                      p: FlexureParams = FlexureParams()) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    result = analyze(p, y_range=(-7e-3, 7e-3), n_samples=2001)
    y_ccx = np.array(positions)
    F_ccx = np.array(forces)

    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    ax.plot(result.y * 1e3, result.force, "b-", lw=2,
            label="PRBM (scripts/bimodal_compliance.py)")
    ax.plot(y_ccx * 1e3, F_ccx, "rs", ms=6, mfc="none", mew=1.5,
            label="CalculiX 2.21 (NLGEOM truss, disp.-controlled)")
    ax.axhline(0.0, color="black", lw=0.5)

    for y_eq, kind in result.equilibria:
        color = "tab:green" if kind == "stable" else "tab:red"
        marker = "o" if kind == "stable" else "X"
        ax.plot(y_eq * 1e3, 0.0, marker=marker, color=color, ms=11, zorder=5)

    ax.set_xlabel("apex displacement  $y$  [mm]")
    ax.set_ylabel("restoring force  $F$  [N]")
    ax.set_title("Snap-through cross-check: PRBM vs CalculiX FEA")
    ax.set_ylim(-220, 220)
    ax.set_xlim(-7, 7)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", fontsize=9)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path)
    fig.savefig(out_path.with_suffix(".png"), dpi=120)
    plt.close(fig)
    return out_path


def main() -> int:
    print("Running CalculiX sweep (this takes ~30 s)…")
    positions, forces = run_sweep()
    print(f"  captured {len(positions)} converged FEA points")
    if not positions:
        print("ERROR: no CalculiX results captured.", file=sys.stderr)
        return 1

    figures = Path(__file__).resolve().parent.parent / "docs" / "figures"
    out = figures / "bimodal-fea-crosscheck.svg"
    render_comparison(positions, forces, out)
    json_out = figures / "bimodal-fea-crosscheck.json"
    json_out.write_text(json.dumps({"y_m": positions, "Fy_N": forces}, indent=2))
    print(f"  wrote {out} and {json_out}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
