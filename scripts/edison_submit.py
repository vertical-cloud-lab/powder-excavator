"""Submit and poll Edison Scientific tasks via the edisonscientific endpoint.

The Edison Platform is reached at ``https://api.platform.edisonscientific.com``
(NOT ``https://api.platform.futurehouse.org`` -- that's the public FutureHouse
endpoint, which is different infrastructure with different access controls).
We re-use the open-source ``futurehouse-client`` SDK because it speaks the
same protocol, but every constructor here pins ``service_uri`` to the Edison
host so we can't accidentally talk to the wrong cluster.

Authentication is via the ``EDISON_API_KEY`` environment variable.

Usage examples (run from the repo root):

    # Submit a fresh literature-deep query (paperqa3-high) for generative-CAD
    python scripts/edison_submit.py submit-cad-litreview

    # Submit one iteration of the analysis feedback cycle bundling the design
    # context (README, manuscript, prior analyses, CAD) inline into the query
    python scripts/edison_submit.py submit-analysis 1

    # Poll a previously-submitted task and dump its formatted answer
    python scripts/edison_submit.py poll <task_id>
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from futurehouse_client import FutureHouseClient, TaskRequest

# The Edison Scientific platform endpoint. This is the canonical answer to
# "you're using futurehouse, should be using edisonscientific" -- the SDK
# defaults to FutureHouse PROD, so we override.
EDISON_SERVICE_URI = "https://api.platform.edisonscientific.com"

# Edison job names (the SDK's JobNames enum points at older paperqa2 names;
# Edison exposes the paperqa3 family + the data-analysis-crow-high job).
JOB_LITERATURE_HIGH = "job-futurehouse-paperqa3-high"
JOB_ANALYSIS = "job-futurehouse-data-analysis-crow-high"

REPO_ROOT = Path(__file__).resolve().parent.parent

# Files we embed inline (as fenced text blocks) into every analysis iteration
# so Edison sees the full design context without depending on the chunked
# upload endpoint, which currently 404s on the Edison cluster. Total payload
# is ~135 KB -- well within reasonable query size.
CONTEXT_TEXT_FILES: tuple[Path, ...] = (
    REPO_ROOT / "README.md",
    REPO_ROOT / "docs" / "manuscript" / "main.tex",
    REPO_ROOT / "docs" / "edison" / "analysis-v2-corrected-gondola.md",
    REPO_ROOT / "cad" / "README.md",
    REPO_ROOT / "cad" / "excavator.py",
    REPO_ROOT / "cad" / "dfm.py",
)

# Common framing for every iteration of the analysis feedback cycle. The
# gantry-only constraint (no second axis on the bucket) is the load-bearing
# requirement from PR comment 4166621470.
ANALYSIS_PREAMBLE = """\
You are reviewing the powder-excavator project, an open-source bulk powder
dispenser intended to feed a downstream precision gravimetric dispenser inside
a self-driving lab. **Hard constraint:** the entire dispensing motion must be
achievable on a 3-axis gantry (X, Y, Z) -- *no* second actuator on the bucket
itself. All trough rotation / scoop opening / closing must come from passive
mechanical interaction with fixed external features (cam ramps, routed slots,
fixed posts, compliant flexures, etc.) driven by gantry motion alone.

Target powders are dozens of microns in diameter, often cohesive,
hygroscopic, or triboelectrically charged. Manufacturing target is FDM 3D
printing in PETG / nylon / ESD-safe filament with stock dowel-pin pivots.

The full design context (README, LaTeX manuscript, prior Edison analyses,
and the CadQuery parametric model with its DFM checks) is embedded inline
below as fenced code blocks.
"""

ITERATION_PROMPTS = {
    1: """\
**Iteration 1 of 3 -- gantry-only baseline review.**

Given the gantry-only constraint above, please:

1. Identify every place in the current design where the mechanism implicitly
   assumes a second actuator on the bucket and propose a gantry-only
   substitute (cam, slot, compliant bistable mechanism, OT-2-style tip-eject,
   pipette-displacement-driven suction, etc.).
2. Compare the smooth-cam-ramp variant (Panel D) and the routed-slot variant
   (Panel E) for: kinematic determinism, bidirectional return, robustness to
   powder build-up on the cam/slot, and additive-manufacturing complexity.
3. Critique the bimodal scoop suggestion from PR comment 3134394694
   ("scoop position" vs "hold/don't leak position", potentially actuated by
   OT-2 tip-eject style drop or pipette-suction). Is a single passive
   bistable flexure (compliant mechanism) achievable on a 3-axis gantry, or
   does it always require a second axis?
4. Propose three concrete experimental measurements (mass CV, dose-recovery,
   bridging frequency) that would discriminate between the cam-ramp,
   pin-slot, and bistable variants.
5. Recommend an open, pip-installable feedback-loop toolchain that hooks the
   CadQuery parametric model into a measure-and-re-design loop on a Jubilee
   or OpenTrons rig.
""",
    2: """\
**Iteration 2 of 3 -- refinement based on Iteration 1.**

Building on Iteration 1's gantry-only critique (whose verbatim answer will
be embedded below as `analysis-iter1.md`):

1. Pick the single strongest gantry-only actuation strategy from Iteration 1
   and design it in detail: dimensions, materials, tolerances, expected dose
   range, expected CV, failure modes.
2. Identify the 2-3 highest-risk geometric parameters (e.g. bumper chamfer
   angle, slot waypoint spacing, flexure thickness) and propose a
   one-factor-at-a-time sweep that the CadQuery model + Bayesian optimisation
   loop could run.
3. Specify the closed-loop digital-twin instrumentation needed (load cell,
   camera, encoder feedback) and how each measurement would feed back into
   the next CadQuery parameter update.
""",
    3: """\
**Iteration 3 of 3 -- concrete decision and build plan.**

Building on Iterations 1 and 2 (whose verbatim answers will be embedded
below as `analysis-iter1.md` and `analysis-iter2.md`):

1. Recommend a single design to take to first prototype, with a justification
   that explicitly addresses why each rejected variant was rejected.
2. Provide a 5-step build-and-test plan for that prototype (print, assemble,
   instrument, calibrate, characterise) with go/no-go criteria at each step.
3. List the additions / changes that should be made to the manuscript
   (`docs/manuscript/main.tex`) to reflect the chosen design and to defend
   the gantry-only-no-second-axis claim.
4. List the parameters in `cad/excavator.py::ExcavatorParams` that need to
   change to match the chosen design.
""",
}

CAD_LITREVIEW_QUERY = """\
We are designing the actuation and feedback loop for an open-hardware powder
dispenser ("powder-excavator") that must run on a 3-axis gantry with no
second axis on the bucket. The bucket's tilt schedule is therefore programmed
purely by passive mechanical interaction with fixed external features
(cam ramps, routed slots, compliant flexures, OT-2-style tip-ejection,
pipette-displacement-driven suction, etc.) driven by gantry motion alone.

Please synthesise the state of the art across two linked topics, with a
preference for **open and pip-installable** tools (we are using CadQuery as
the parametric authoring layer) and citing peer-reviewed work where possible:

1. **Generative / computational CAD and systems design for mechanical
   hardware**: parametric / algorithmic CAD ecosystems (CadQuery, build123d,
   OpenSCAD, Rhino + Grasshopper + Rhino.Inside, Onshape FeatureScript, Zoo
   Design Studio / KCL); generative / AI-assisted geometry (nTop, Fusion
   Generative Design, DeepCAD, Text2CAD / CAD-LLM, BrepGen, CAD-Recode,
   Shap-E / TRELLIS); systems-design / requirements-driven approaches (SysML
   v2, OpenMDAO, Bayesian-optimisation design loops); and automated DFM /
   printability checks (slicer-side, DFMPro, Castor). Comparative table where
   tools fight in the same niche.

2. **Automated feedback loops and digital-twin-style evaluation for
   mechanical hardware prototypes**: twin maturity (Kritzinger / Tao /
   Grieves), AM-specific twins (NIST AM-Bench, Eclipse Ditto, ROS2 + Gazebo /
   Ignition), closed-loop design->print->measure->re-design pipelines
   (PowderBot, A-Lab, Ada, Bayesian-optimisation of printed parts), in-situ
   AM monitoring (melt-pool, OCT, PrintWatch / Spaghetti Detective), CV-based
   metrology, and what a credible end-to-end loop would look like for the
   powder-excavator specifically (CadQuery -> print -> Jubilee / OpenTrons
   rig + balance + vision -> Bayesian optimiser -> next params).

End with a concrete recommended toolchain (one pick each for: parametric CAD
authoring, generative exploration, DFM check, prototype-feedback loop, and
the wire-it-together path) for an open-source, pip-installable, no-license-
fee build.
"""


def make_client() -> FutureHouseClient:
    """Build a FutureHouseClient pinned to the Edison Scientific endpoint."""
    api_key = os.environ.get("EDISON_API_KEY")
    if not api_key:
        sys.exit("EDISON_API_KEY env var is not set")
    return FutureHouseClient(service_uri=EDISON_SERVICE_URI, api_key=api_key)


def _embed_context() -> str:
    """Return the design-context files joined as fenced text blocks."""
    parts: list[str] = []
    for fp in CONTEXT_TEXT_FILES:
        if not fp.exists():
            continue
        rel = fp.relative_to(REPO_ROOT)
        ext = fp.suffix.lstrip(".") or "text"
        parts.append(f"\n=== file: {rel} ===\n```{ext}\n{fp.read_text()}\n```")
    return "\n".join(parts)


def submit_analysis(iteration: int) -> str:
    """Submit one iteration of the analysis feedback cycle."""
    if iteration not in ITERATION_PROMPTS:
        sys.exit(f"iteration must be one of {sorted(ITERATION_PROMPTS)}")
    client = make_client()
    query = (
        ANALYSIS_PREAMBLE
        + "\n"
        + ITERATION_PROMPTS[iteration]
        + "\n\n--- Embedded repository context follows ---\n"
        + _embed_context()
    )
    task = client.create_task(TaskRequest(name=JOB_ANALYSIS, query=query))
    print(f"submitted analysis iter {iteration}: task_id={task}")
    return str(task)


def submit_cad_litreview() -> str:
    """Resubmit the generative-CAD literature-deep query at the Edison
    endpoint (the previous submission via FutureHouse was cancelled)."""
    client = make_client()
    task = client.create_task(
        TaskRequest(name=JOB_LITERATURE_HIGH, query=CAD_LITREVIEW_QUERY)
    )
    print(f"submitted CAD lit-review (paperqa3-high): task_id={task}")
    return str(task)


def poll(task_id: str) -> None:
    """Print the status and (if available) the formatted answer for a task."""
    client = make_client()
    resp = client.get_task(task_id)
    print(f"task_id : {task_id}")
    print(f"status  : {getattr(resp, 'status', '?')}")
    print(f"job     : {getattr(resp, 'job_name', '?')}")
    answer = getattr(resp, "formatted_answer", None) or getattr(resp, "answer", None)
    if answer:
        print("\n--- answer ---\n")
        print(answer)
    else:
        print("(no answer body yet)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("submit-cad-litreview")
    p_an = sub.add_parser("submit-analysis")
    p_an.add_argument("iteration", type=int, choices=sorted(ITERATION_PROMPTS))
    p_poll = sub.add_parser("poll")
    p_poll.add_argument("task_id")
    args = parser.parse_args()
    if args.cmd == "submit-cad-litreview":
        submit_cad_litreview()
    elif args.cmd == "submit-analysis":
        submit_analysis(args.iteration)
    elif args.cmd == "poll":
        poll(args.task_id)


if __name__ == "__main__":
    main()
