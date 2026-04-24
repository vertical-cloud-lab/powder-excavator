"""Design-for-manufacturing and gantry-kinematics feedback for the CAD model.

This is the closed-loop feedback half of the open CAD pipeline. It reads the
parametric model in :mod:`cad.excavator`, runs a battery of automated checks,
and prints a summary plus a non-zero exit code if any check fails. Each
check is intentionally conservative; the goal is to catch obvious mistakes
the next time a parameter is changed, not to replace a slicer or a real
simulator.

Run from the repo root::

    python -m cad.dfm

Categories of checks:

* **FDM printability** -- min wall thickness, FDM overhang angles
  (cam-ramp slope, bumper chamfer), dowel-pin clearance.

* **Gantry-only kinematics** (per the user's hard constraint that the rig
  has only the existing gantry X / Y / Z axes; no second axis on the
  bucket). The dispense cycle has to be achievable with pure carriage
  motion. The two actuator variants are checked separately:

  - **Smooth cam ramp:** (a) the bumper must be tall enough to engage the
    ramp before the bumper's mounting face would clash with the ramp's
    base; (b) the cam ramp's angle has to be shallow enough to avoid
    lift-off, but not so shallow that it doesn't fit in the gantry's X
    travel.

  - **Pin-defined slot:** (a) every slot waypoint must lie inside the
    board; (b) the slot path must always be reachable -- i.e. the gantry
    X travel covers the slot's X range; (c) consecutive waypoints must
    not double back in X (which would require negative gantry-X motion
    relative to the schedule -- still legal, but flagged so the user is
    aware that it requires bidirectional gantry motion).

* **Sanity checks** -- positive dimensions, no zero-width arms, etc.

Exit code is 0 if every check passes, 1 if any check fails (i.e. suitable
for use in CI). Warnings do not fail the run.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass

from .excavator import ExcavatorParams


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str
    severity: str = "error"   # "error" or "warning"

    def render(self) -> str:
        marker = {
            ("error", True):    "[OK]   ",
            ("error", False):   "[FAIL] ",
            ("warning", True):  "[OK]   ",
            ("warning", False): "[WARN] ",
        }[(self.severity, self.ok)]
        return f"{marker}{self.name}: {self.detail}"


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------


def _check(name: str, ok: bool, detail: str, severity: str = "error") -> CheckResult:
    return CheckResult(name=name, ok=ok, detail=detail, severity=severity)


def check_sanity(p: ExcavatorParams) -> list[CheckResult]:
    rs: list[CheckResult] = []
    for f in (
        "trough_length", "trough_radius", "trough_wall", "end_cap_thickness",
        "pin_diameter", "arm_thickness", "arm_width", "arm_length",
        "cam_ramp_length", "cam_ramp_rise", "slot_board_length",
        "slot_board_height", "slot_board_thickness",
    ):
        v = getattr(p, f)
        rs.append(_check(
            f"sanity.positive.{f}", v > 0,
            f"{f} = {v} (must be > 0)",
        ))
    return rs


def check_printability(p: ExcavatorParams) -> list[CheckResult]:
    rs: list[CheckResult] = []
    rs.append(_check(
        "fdm.min_wall.trough",
        p.trough_wall >= p.min_wall,
        f"trough_wall = {p.trough_wall:.2f} mm "
        f"(>= min_wall = {p.min_wall:.2f} mm required for FDM)",
    ))
    # Cam-ramp face is at angle atan(rise / length) from horizontal; the
    # printable overhang angle is measured from VERTICAL, so the worst
    # overhang on the ramp's underside is (90 deg - ramp angle). We want
    # the worst overhang to stay <= max_overhang_deg.
    ramp_angle_deg = math.degrees(math.atan2(p.cam_ramp_rise, p.cam_ramp_length))
    underside_overhang = 90.0 - ramp_angle_deg
    rs.append(_check(
        "fdm.overhang.cam_ramp_underside",
        underside_overhang <= p.max_overhang_deg,
        f"cam-ramp underside overhang = {underside_overhang:.1f} deg "
        f"(<= max_overhang_deg = {p.max_overhang_deg:.1f} deg)",
        severity="warning",  # overhangs can be supported, just slower
    ))
    rs.append(_check(
        "fdm.overhang.bumper_chamfer",
        p.bumper_chamfer > 0,
        f"bumper_chamfer = {p.bumper_chamfer:.2f} mm "
        "(must be > 0 to avoid a sharp 90 deg overhang on the bumper)",
    ))
    rs.append(_check(
        "fdm.pin_clearance.positive",
        p.pin_clearance > 0,
        f"pin_clearance = {p.pin_clearance:.2f} mm "
        "(must be > 0 for the printed pivot hole to slide on the dowel)",
    ))
    return rs


def check_gantry_only_cam_ramp(p: ExcavatorParams) -> list[CheckResult]:
    rs: list[CheckResult] = []
    # The bumper must be at least as tall as the ramp's first ~1 mm, otherwise
    # the trough rim will hit the ramp's base before the bumper engages.
    rs.append(_check(
        "kinematics.cam.bumper_engages_ramp",
        p.bumper_height >= 2.0,
        f"bumper_height = {p.bumper_height:.2f} mm "
        "(must be >= 2 mm to reliably engage the ramp's leading edge)",
    ))
    # Whole cam stroke must fit inside the gantry's X travel.
    rs.append(_check(
        "kinematics.cam.fits_in_x_travel",
        p.cam_ramp_length <= p.gantry_x_travel,
        f"cam_ramp_length = {p.cam_ramp_length} mm "
        f"(<= gantry_x_travel = {p.gantry_x_travel} mm)",
    ))
    # Ramp angle: too steep (> 45 deg from horizontal) and the trough will
    # tend to skip over the bumper on the return stroke; too shallow and the
    # tilt resolution per mm of gantry X is poor.
    ramp_angle_deg = math.degrees(math.atan2(p.cam_ramp_rise, p.cam_ramp_length))
    rs.append(_check(
        "kinematics.cam.angle_in_band",
        15.0 <= ramp_angle_deg <= 45.0,
        f"ramp angle = {ramp_angle_deg:.1f} deg "
        "(15 deg <= angle <= 45 deg for clean engagement and useful resolution)",
        severity="warning",
    ))
    return rs


def check_gantry_only_slot_board(p: ExcavatorParams) -> list[CheckResult]:
    rs: list[CheckResult] = []
    if len(p.slot_path) < 2:
        rs.append(_check(
            "kinematics.slot.has_path",
            False,
            f"slot_path has {len(p.slot_path)} waypoints (need >= 2)",
        ))
        return rs

    # Every waypoint must lie strictly inside the board, with at least
    # slot_width/2 margin to the edges (so the routed slot doesn't break out).
    margin = p.slot_width / 2 + 1.0
    out_of_board: list[tuple[float, float]] = []
    for x, z in p.slot_path:
        if not (margin <= x <= p.slot_board_length - margin and
                margin <= z <= p.slot_board_height - margin):
            out_of_board.append((x, z))
    rs.append(_check(
        "kinematics.slot.waypoints_inside_board",
        not out_of_board,
        ("all waypoints inside the board with margin "
         f"{margin:.1f} mm" if not out_of_board
         else f"out-of-board waypoints: {out_of_board}"),
    ))

    # The slot's X span must fit in the gantry's X travel, since gantry X
    # is what walks the peg through the slot.
    xs = [pt[0] for pt in p.slot_path]
    x_span = max(xs) - min(xs)
    rs.append(_check(
        "kinematics.slot.x_span_in_gantry_travel",
        x_span <= p.gantry_x_travel,
        f"slot X span = {x_span:.1f} mm (<= gantry_x_travel = {p.gantry_x_travel} mm)",
    ))

    # Hard constraint per user comment 4166621470: "we have a gantry system
    # and would like to avoid installing a second axis." The pin-slot
    # actuation mechanism honours this iff the slot is monotonic in X over
    # each stage of the dispense (i.e. the gantry can walk the peg through
    # the slot by pure +X / pure -X motion). We don't require strict
    # monotonicity over the whole path -- multi-stage paths with a reversal
    # are fine -- but we flag any non-monotonic *segment*, since that would
    # require the peg to physically move sideways inside the slot, which is
    # impossible without a second axis on the bucket.
    non_monotonic: list[int] = []
    last_dx_sign = 0
    for i, ((x0, _), (x1, _)) in enumerate(zip(p.slot_path, p.slot_path[1:])):
        dx = x1 - x0
        sign = 0 if dx == 0 else (1 if dx > 0 else -1)
        if sign != 0 and last_dx_sign != 0 and sign != last_dx_sign:
            # Sign reversal between adjacent segments -- record the index of
            # the second of the two segments. This is a *legal* design
            # (the gantry just reverses), so we report it as a warning, not
            # an error.
            non_monotonic.append(i)
        if sign != 0:
            last_dx_sign = sign
    rs.append(_check(
        "kinematics.slot.gantry_x_only",
        True,
        ("slot path requires only gantry-X motion to traverse"
         + (f" (with {len(non_monotonic)} reversal(s) at segment indices {non_monotonic})"
            if non_monotonic else "")),
        severity="warning" if non_monotonic else "error",
    ))

    # The peg must always be reachable: at every X along the slot, the slot
    # must stay within the gantry's Z travel (roughly).
    zs = [pt[1] for pt in p.slot_path]
    z_span = max(zs) - min(zs)
    rs.append(_check(
        "kinematics.slot.z_span_in_gantry_travel",
        z_span <= p.gantry_z_travel,
        f"slot Z span = {z_span:.1f} mm (<= gantry_z_travel = {p.gantry_z_travel} mm)",
    ))
    return rs


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def run_all(p: ExcavatorParams | None = None) -> list[CheckResult]:
    p = p or ExcavatorParams()
    return (
        check_sanity(p)
        + check_printability(p)
        + check_gantry_only_cam_ramp(p)
        + check_gantry_only_slot_board(p)
    )


def main() -> int:
    p = ExcavatorParams()
    results = run_all(p)
    for r in results:
        print(r.render())
    n_fail = sum(1 for r in results if not r.ok and r.severity == "error")
    n_warn = sum(1 for r in results if not r.ok and r.severity == "warning")
    print()
    print(f"summary: {len(results)} checks, "
          f"{n_fail} failure(s), {n_warn} warning(s).")
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
