# Gantry-Only Baseline Review Of Powder Excavator

- **Trajectory ID:** `d6e32c46-2774-4477-a060-9993ef51ab10`
- **Crow / job:** `job-futurehouse-data-analysis-crow-high` (analysis (Crow, high))
- **Source:** Edison Scientific (`api.platform.edisonscientific.com`)

## Prompt

```
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


--- Embedded repository context follows ---

=== file: README.md ===
```md
# powder-excavator

A pure-mechanical, gantry-mounted "ladle / trough" for picking up loose
powder from a bed and depositing it at a target location. The trough is
suspended between two vertical arms that grip its **two short end caps**;
a single **longitudinal pivot pin** runs through both end caps along the
trough's long axis L. There are no actuators on the bucket itself — the
gantry's existing X / Z motion plus a fixed wall-/post-mounted **smooth
inclined cam ramp** does all the work.

> **Geometry note (post-review).** An earlier revision of this design used
> a **transverse** pivot pin (running across the trough's width D) and
> tipped the trough **end-over-end** against a **sawtooth** ledge. Both
> choices were retired after a high-effort review by Edison Scientific
> identified (i) a kinematic impossibility — a fixed sawtooth tooth
> cannot engage a fixed-radius hook on a horizontally-translating pivot
> without the lip plunging through the tooth — and (ii) a severe trapped-
> volume / arching problem when cohesive powders are forced to bottleneck
> through the narrow ~13 mm spill point of an end-over-end half-cylinder.
> The current design uses a **longitudinal** pivot pin and **sideways
> tilt** so powder pours over the full 80 mm long edge, and replaces the
> sawtooth with a **smooth cam ramp** that the trough's chamfered bumper
> slides up. A follow-on hand sketch
> ([`PXL_20260423_231729467.jpg`](PXL_20260423_231729467.jpg)) refines the
> cam ramp into a **pin-defined-path** (peg-in-routed-slot) variant in
> which a peg on a stem hanging from the gantry is captured in a slot
> routed into a fixed external board, so the slot path deterministically
> programs the trough's tilt schedule. The full review and the verbatim
> Edison answers live in [`docs/edison/`](docs/edison/); the
> literature-aware brainstorming doc has been ported to a LaTeX manuscript
> with a proper BibTeX bibliography (see
> [`docs/manuscript/main.tex`](docs/manuscript/main.tex) and
> [`docs/manuscript/refs.bib`](docs/manuscript/refs.bib); build with
> `cd docs/manuscript && make`).

## Original concept sketch

![Design sketch](powder-excavator-sketch.jpg)

## Cleaned-up design diagram

The sketch above has been recreated as four labelled subpanels. Each is a
self-contained SVG with its own caption. All four are produced (along with
the mechanism animation below) by a single reproducible script,
[`scripts/generate_figures.py`](scripts/generate_figures.py).

### Panel A — Orthographic views (end / side / top)

![Panel A — orthographic](docs/figures/panel-A-orthographic.svg)

### Panel B — End-cap pivot detail

![Panel B — pivot detail](docs/figures/panel-B-pivot-detail.svg)

### Panel C — 3D / isometric view of trough on gantry

![Panel C — isometric](docs/figures/panel-C-isometric.svg)

### Panel D — Mechanism of action (4 steps)

![Panel D — mechanism of action](docs/figures/panel-D-mechanism.svg)

### Panel E — Pin-defined-path actuation variant

A follow-on hand sketch
([`PXL_20260423_231729467.jpg`](PXL_20260423_231729467.jpg)) refines the
smooth cam ramp into a peg-in-routed-slot mechanism. A vertical stem hangs
from the gantry carriage on a pin pivot; a transverse peg at the top of the
stem rides in a slot routed into a fixed external board. The slot's shape
over `X` deterministically programs the trough's tilt schedule, with the peg
captive in the slot for the entire stroke (no approach-and-contact
ambiguity, and bidirectional return without relying on gravity). See
[`docs/manuscript/main.tex`](docs/manuscript/main.tex) §"Pin-defined-path
actuation" for the full trade-off discussion.

![Panel E — pin-defined-path actuation](docs/figures/panel-E-pin-slot.svg)

### Animation — cam-engagement and sideways tilt

![Mechanism animation — trough rolls sideways about its longitudinal pin as its bumper rides up the cam ramp](docs/figures/mechanism.gif)

The full literature-aware design discussion — framed roughly as the
introduction to a *Digital Discovery* manuscript on a new powder
dispenser, with references to recent SDL / powder-handling literature —
is now a LaTeX manuscript with a proper BibTeX bibliography:
[`docs/manuscript/main.tex`](docs/manuscript/main.tex),
[`docs/manuscript/refs.bib`](docs/manuscript/refs.bib). Build with
`cd docs/manuscript && make` (requires `pdflatex`, `bibtex`, and
`cairosvg`).

## Parametric CAD pipeline ([`cad/`](cad/))

The same dimensions used in the figures and the manuscript also drive an
**open, scriptable parametric CAD model** built on
[CadQuery](https://github.com/CadQuery/cadquery), so the design can be
iterated as plain Python source and exported to STEP / STL for any
open-source slicer. A small `cad/dfm.py` runs design-for-manufacturing and
**gantry-only kinematics** checks (the explicit constraint from PR comment
4166621470 — "we have a gantry system and would like to avoid installing a
second axis"), so a parameter regression is caught the next time anyone
edits `ExcavatorParams`. See [`cad/README.md`](cad/README.md) for the
rationale (why CadQuery over Rhino / Grasshopper / Fusion / nTop) and the
full feedback-loop description.

```bash
pip install cadquery
python -m cad.build      # writes STEP + STL + manifest into cad/build/
python -m cad.dfm        # design-for-manufacturing + gantry-only kinematics checks
python -m unittest discover cad/tests -v
```


## Design brainstorming

### Core idea

The bucket is an **elongated half-cylinder trough** (think: a long,
narrow ladle with a semicircular cross-section and an open top). It is
suspended between **two parallel vertical arms** that hang from the
gantry carriage and grip the trough on its **two short end caps**. A
**single horizontal pivot pin** runs from one arm, through a printed
boss in the first end cap, lengthwise along L through the trough, out
through a matching boss in the second end cap, and into the second arm
(panels B and C). The pivot axis is therefore **parallel to the
trough's long axis L** — the trough rolls about that axis like a
spit-roast rotating about its skewer.

- The two arms are rigidly bolted to the carriage and **always stay
  vertical** during operation.
- The trough is the **only** part that ever rotates, and only about the
  longitudinal pin — rolling **sideways** when its rim-mounted bumper
  catches the cam ramp. Powder pours over the **full 80 mm long edge**,
  not through a narrow end-cap point.
- The pin sits a few millimetres above the loaded trough's centre of
  mass, so gravity returns the trough to "open-up" once the dump cam is
  cleared (a stable pendulum / gondola-style pivot).

Picking shape matters:

- A **half-cylinder** maximises retained volume per unit "scoop depth"
  while presenting a long flat top edge that pours uniformly along its
  whole length.
- An **elongated** trough (length L ≈ 3 × diameter D) gives the spill
  edge a large area (≈ L × few-mm depth) so cohesive powders cannot
  arch across it, eliminating the bottleneck/bridging failure mode of
  an end-over-end tilt of the same trough (Edison v2 §3).
- **No moving lid / hinge in the baseline design** — powder is held in
  by gravity alone, which keeps the part count and the failure modes to
  a minimum.

### Mechanism of action (4 steps — see Panel D)

1. **J-curve plunge into the bed.** The gantry lowers the carriage
   (Z↓) so the trough enters the powder bed, then translates a few
   millimetres in X while continuing down — a shallow J-curve rather
   than a pure Z-plunge. A blunt flat half-cylinder driven straight
   down compresses the bed underneath it instead of flowing in (Edison
   v1 §2); the J-curve lets powder spill into the open top as the
   bucket sweeps forward.
2. **Lift past the strike-off bar.** The carriage rises (Z↑) along an
   X-coordinate that takes the rim of the trough **under a fixed bed-
   edge strike-off bar**. The bar wipes the heaped powder back into the
   bed and leaves a defined fill volume. Without this step, dose CV
   sits in the 15–30 % range across powder classes (Edison v2 §4); with
   it, ≈10 % CV is realistic on cohesive inorganics — comparable to the
   positive-displacement-pipette baseline reported by Alsenz (see
   [`docs/manuscript/main.tex`](docs/manuscript/main.tex)).
3. **Transport to the deposit X.** The carriage translates in X over to
   the deposit station. Arms still vertical; trough still open-up,
   level under gravity.
4. **Sideways tilt against the cam → deposit.** The gantry pushes the
   trough in X into a fixed, wall-/post-mounted **smooth inclined cam
   ramp** at end-cap-rim height. The chamfered bumper on the trough's
   long-side rim **slides up the cam's hypotenuse**; because the cam
   surface is a continuous incline rather than a fixed point, pure-X
   gantry travel is geometrically compatible with the resulting roll of
   the trough about its longitudinal pin (Edison v2 §1). Continued
   X-push rolls the trough sideways and powder pours over the **full
   long edge**. Backing the carriage off lets gravity right the trough
   under its pendulum action.

The "push against a cam to dump" trick is what makes this fully
mechanical — no servo / solenoid is needed on the bucket itself.

### What is the cam ramp?

A **fixed, wall- or post-mounted inclined block** at roughly trough-
end-cap-rim height (see Panel D, Step 4, and the GIF above). Its top
surface is a **smooth ramp** (a chamfered, ideally polished
hypotenuse), *not* a comb of teeth. It is *not* on the floor of the
powder bed and is *not* part of the moving assembly. The trough's rim
bumper rides up the ramp as the gantry pushes the carriage in X; the
height the bumper reaches up the ramp (set by how far in X the gantry
pushes) determines the tilt angle and therefore how much powder is
poured.

Why a smooth ramp and not a sawtooth?

- **Kinematic compatibility.** A fixed sawtooth tooth cannot engage a
  fixed-radius hook on a horizontally-translating pivot pin without the
  lip having to plunge through the tooth — the pin-to-tooth distance
  must change as the pivot moves in X, but the hook's radius is fixed.
  An inclined cam removes the constraint entirely: the contact point
  slides continuously along the cam surface as the gantry travels
  (Edison v2 §1).
- **Continuous tilt control.** With a smooth ramp, the tilt angle is a
  continuous function of gantry X position, so pour rate and final
  dose can be modulated in software without changing hardware.
- **No catch-and-skip failure mode.** A printed sawtooth tooth and a
  printed hook can mis-engage, snag, or skip; a chamfered bumper on a
  smooth incline cannot.

### Optional: knock-to-de-bridge

Because the bumper is in continuous frictional contact with the cam
during the tilt, the gantry can be driven to **rapidly oscillate ±2 mm
in X** while the bumper is engaged. This momentarily slams the trough
against the cam and acts as a free pneumatic-knocker analogue to break
up bridges of cohesive powder that would otherwise refuse to pour
(Edison v1 §6). It is a software-only feature — the same hardware that
performs the tilt also performs the knock.

### Open questions / things to prototype

- **Manufacturing.** Target is a **3D-printable** trough + arms + end-
  cap pivot bosses (PETG / nylon for the prototype, with a glued-in
  brass sleeve for the pin holes if wear becomes an issue). The pivot
  pin itself is a stock dowel pin or shoulder bolt, ideally **metal**
  so it can also serve as the ground path for an optional conductive
  trough lining (e.g. interior copper tape) that mitigates triboelectric
  charging on fine dry inorganics (Edison v1 §2). The cam ramp can be
  printed too. A machined-aluminium revision would only be needed if
  the printed parts wear or charge problematically.
- **Target powders are dozens-of-microns in diameter** — catalysts,
  ceramics, salts. Many are cohesive, hygroscopic, and/or
  triboelectrically charged; some clump and resist removal from a
  scoop. This drives several of the open questions below.
- **Trough geometry sweep.** Pure semicircle vs. a slightly deeper "U"
  vs. a V-bottom — which retains powder best while still pouring
  cleanly when rolled? A 3D-printed bake-off across our worst-case
  cohesive powders is cheap.
- **Cam-ramp angle sweep.** Cam slope, length, and surface finish are
  the three knobs most likely to dominate dose CV. Steeper slopes give
  more aggressive tilts per unit gantry travel but risk bumper slip;
  shallower slopes give finer control but a longer dump stroke.
- **Strike-off bar profile.** Square cross-section vs. a chamfered or
  rounded leading edge — which leaves the cleanest fill at the rim
  without flicking powder away? Worth varying.
- **Bumper profile.** Chamfer angle and surface finish on the rim
  bumper directly affect cam engagement; too sharp and it digs in,
  too rounded and it slips. Print + sand a small set and characterise.
- **Bed depletion.** Repeated scoops from the same X, Y in a static
  bed will form a crater and the dose will decay (Edison v1 §3). The
  gantry must raster the plunge X, Y across the bed, or a separate
  "bed-stir" cycle must be added.
- **Cleaning / cross-contamination.** For multi-material campaigns the
  pivot pin is the natural quick-release point — pull the pin, swap the
  trough, re-insert. For very sticky powders a **per-material
  consumable trough** (snap-in printed liner) may be cheaper than
  cleaning.
- **Use-environment caveat.** A bulk-transfer scoop unavoidably
  exposes the powder to ambient air during transport and leaves an
  open crater in the stock bed. For hygroscopic salts this is a real
  limitation; the device's intended envelope is **bulk transfer in
  ambient or globally-controlled environments (e.g. inside a glovebox
  or on a benchtop with a desiccated stock container)**, not as a
  direct loader for highly moisture-sensitive workflows.

### Possible variations (all still pure-mechanical)

- **Reversible tilt** — cam ramps on both sides of the work area let
  the same bucket dump left or right by which way it's pushed.
- **Two troughs back-to-back** — one fills while the other is being
  dumped, doubling throughput with no extra actuators.
- **Auger / screw inside the trough** — adds one rotary actuator but
  gives controlled metered dosing instead of "tilt and pour all".
- **Passive flap lid for fine powders.** A lightweight flap hinged on
  the trough's long upper edge that gravity holds *closed* over the
  mouth while the trough hangs open-up (so fluffy powder is not shed
  during X-travel). When the trough rolls against the cam ramp in
  step 4, a small projection on the flap strikes a separate fixed tang
  on the same cam assembly, swinging the flap clear so powder can
  pour out. Returns to closed under gravity once the trough returns
  upright. Still purely mechanical — no actuator on the bucket.

### Acknowledgements

The design changes between PR #2 and the present revision were prompted
by a high-effort design review from [Edison Scientific](https://edisonscientific.com/),
plus a literature search via the same service. Verbatim responses are
archived under [`docs/edison/`](docs/edison/) for traceability.

```

=== file: docs/manuscript/main.tex ===
```tex
% !TEX program = pdflatex
% Powder-Excavator design brainstorming and prior-art review.
%
% Build:
%   cd docs/manuscript
%   pdflatex main
%   bibtex   main
%   pdflatex main
%   pdflatex main
%
% Or use the Makefile in this directory: ``make``.

\documentclass[11pt,a4paper]{article}

\usepackage[margin=1in]{geometry}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{microtype}
\usepackage{textcomp}
\usepackage[hyphens]{url}
\usepackage{xcolor}
\usepackage{hyperref}
\hypersetup{
  colorlinks=true,
  linkcolor=blue!50!black,
  citecolor=blue!50!black,
  urlcolor=blue!50!black,
  pdftitle={Powder-Excavator: design brainstorming and prior-art notes},
  pdfauthor={vertical-cloud-lab},
}
\usepackage{enumitem}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{longtable}
\usepackage{caption}
\usepackage{siunitx}

\sisetup{
  range-units = single,
  per-mode    = symbol,
}

\title{Powder-Excavator: design brainstorming and prior-art notes}
\author{vertical-cloud-lab}
\date{April 2026}

\begin{document}
\maketitle

\begin{abstract}
\noindent
This document captures a literature-aware brainstorm for the gantry-mounted
``powder excavator'' sketched in \texttt{powder-excavator-sketch.jpg} and
recreated as the labelled subpanels under \texttt{docs/figures/}. It is
structured roughly like the introduction to a \emph{Digital Discovery}
manuscript on a new powder-handling tool: where does this device sit in the
landscape of automated powder dispensing, what gap is it trying to fill, and
what would we need to measure to defend that claim. The current revision
adopts the corrected \emph{longitudinal-pivot, sideways-tilt} geometry
identified by the Edison Scientific design-review tasks~\cite{edisonscientific},
and adds a cam-slot / pin-defined-path actuation variant (Sec.~\ref{sec:pinslot})
based on a follow-on hand sketch.
\end{abstract}

\paragraph{Provenance.}
This brainstorm was prompted by feedback on PR~\#2 to ``send the idea to
Edison for a high-effort literature search'' and to consider the discussion
at the Accelerated Discovery
thread~\cite{accdiscthread}. The Edison Scientific service was wired in via
\texttt{edison\_client} for a follow-up session: a high-effort PaperQA3
literature search and two high-effort design-review tasks were
run~\cite{edisonscientific}, and their verbatim responses are archived under
\texttt{docs/edison/}. Peer-reviewed citations marked
\cite{tom2024selfdrivinglaboratoriesfor,yang2007meteringanddispensing,bahr2018collaborativeevaluationof,bahr2020recentadvancesin,jiang2023autonomousbiomimeticsolid,szymanski2023anautonomouslaboratory,szymanski2024automatingthesynthesis,fei2024alabosapythonbased,lunt2023modularmultirobotintegration,lunt2024aroboticworkflow,carruthers2025amobilerobotic,alsenz2011powderpickinganinexpensive,hernandezdelvalle2024pelletdispensomixerand,doloi2025democratizingselfdrivinglabs,moravkar2020traditionalandadvanced,freeman2017characterisingpowderflow,ghoroi2013multifacetedcharacterizationof,mccalla2023semiautomatedexperimentsto}
are taken directly from the Edison literature task and are listed in the
\hyperref[sec:references]{References} section.

\paragraph{Geometry note (post-review).}
The mechanism described in Sec.~\ref{sec:fits} and Sec.~\ref{sec:variations}
has been updated to the \textbf{longitudinal-pivot, sideways-tilt,
smooth-cam-ramp} geometry adopted after the Edison design-review tasks
identified two design-blocking issues with the earlier ``ferris-wheel
gondola'' (transverse pivot, end-over-end tilt, sawtooth and hooked-lip)
revision: a kinematic impossibility in the push-to-tilt mechanism and a
trapped-volume / bridging problem for cohesive powders. Section~\ref{sec:pinslot}
adds a \emph{pin-defined-path} actuation variant in which a peg on a stem
descending from the gantry rides in a routed slot in a fixed external board;
this captures the cam-ramp idea in a fully constrained ``peg in slot'' form
that removes the approach/contact ambiguity of a free cam follower.

% --------------------------------------------------------------------------
\section{Why powder handling is the pinch point in self-driving labs}
\label{sec:why}

Self-driving laboratories (SDLs) for chemistry and materials science have
matured rapidly over the past five years, with closed-loop platforms now
routinely combining robotic execution, automated characterization, and
Bayesian or generative experiment design~\cite{tom2024selfdrivinglaboratoriesfor,szymanski2023anautonomouslaboratory,fei2024alabosapythonbased,mccalla2023semiautomatedexperimentsto}.
Across nearly every published SDL, \textbf{solids handling --- and powder
dispensing in particular --- is repeatedly called out as the dominant
bottleneck}: it is the step most likely to be left to a human, the one most
sensitive to material properties (cohesion, hygroscopicity, triboelectric
charging), and the one that most often limits end-to-end
autonomy~\cite{tom2024selfdrivinglaboratoriesfor,yang2007meteringanddispensing,carruthers2025amobilerobotic,jiang2023autonomousbiomimeticsolid}.
Tom et al.'s 2024 \emph{Chemical Reviews} survey of SDLs makes the point
bluntly: solid-dispensing hardware ``remains rare and costly relative to
liquid handling, and many labs simply avoid direct powder
manipulation'' wherever pre-dissolved stocks will
do~\cite{tom2024selfdrivinglaboratoriesfor}.

Compared with liquid handling, powder dispensing is hard for three coupled
reasons:

\begin{enumerate}[leftmargin=*]
  \item \textbf{No universal flow regime.} Free-flowing crystalline powders,
    fluffy nanopowders, sticky organics, and hygroscopic salts each demand
    different feeders, hoppers, and tip
    geometries~\cite{yang2007meteringanddispensing,bahr2018collaborativeevaluationof,carruthers2025amobilerobotic}.
  \item \textbf{Dose accuracy scales poorly down.} Sub-milligram gravimetric
    dosing needs a draft-shielded balance, vibration isolation, and feedback
    control; the 17{,}797-dispense ETC benchmark across four commercial
    platforms found that \SI{2}{\milli\gram} targets exhibited
    \SIrange{190}{680}{\percent} higher \%RSD than \SI{50}{\milli\gram}
    targets, and that across the full dataset the percent error spanned
    \SI{-10}{\percent} to \SI{+3245}{\percent} (\SI{95.3}{\percent} of
    dispenses fell between \SI{-25}{\percent} and
    \SI{+100}{\percent})~\cite{bahr2018collaborativeevaluationof,bahr2020recentadvancesin}.
  \item \textbf{Cross-contamination is expensive.} Reservoirs and
    end-effectors must either be disposable, easily cleaned, or dedicated
    per material, which blows up the part count of a multi-reagent
    platform~\cite{tom2024selfdrivinglaboratoriesfor,carruthers2025amobilerobotic}.
\end{enumerate}

% --------------------------------------------------------------------------
\section{Prior art (representative, not exhaustive)}
\label{sec:priorart}

Table~\ref{tab:priorart} summarises the device classes that any new
powder-handling tool has to position itself against. The rows are not
intended as a complete vendor list; they are the classes of mechanism that
recur across the SDL literature
\cite{tom2024selfdrivinglaboratoriesfor,yang2007meteringanddispensing,bahr2018collaborativeevaluationof,bahr2020recentadvancesin,jiang2023autonomousbiomimeticsolid,szymanski2023anautonomouslaboratory,fei2024alabosapythonbased,lunt2023modularmultirobotintegration,lunt2024aroboticworkflow,carruthers2025amobilerobotic,alsenz2011powderpickinganinexpensive}.

\begin{small}
\begin{longtable}{@{}p{0.21\linewidth}p{0.36\linewidth}p{0.36\linewidth}@{}}
\caption{Prior-art device classes for automated powder handling. Quantitative
claims in the ``Strengths'' and ``Limits'' columns are taken from the cited
sources.}
\label{tab:priorart}\\
\toprule
\textbf{Class} & \textbf{Strengths} & \textbf{Limits relevant to us} \\
\midrule
\endfirsthead
\multicolumn{3}{c}{\tablename\ \thetable{} -- continued from previous page}\\
\toprule
\textbf{Class} & \textbf{Strengths} & \textbf{Limits relevant to us} \\
\midrule
\endhead
\midrule
\multicolumn{3}{r}{\emph{continued on next page}}\\
\endfoot
\bottomrule
\endlastfoot
Gravimetric vibratory-head dispensers (Quantos QX1/QX5, Chemspeed SWING /
Powdernium / FLEX GDU-Pfd, Unchained Labs Freeslate/Junior) &
High precision on dense free-flowing powders; closed-loop weight feedback;
integrated workflow software; ETC benchmark established Quantos as the best
overall \% error / \%RSD / time balance and Chemspeed SWING as the fastest
(\SIrange{13}{65}{\second})~\cite{bahr2018collaborativeevaluationof,bahr2020recentadvancesin} &
Per-reagent consumable cartridges/heads; abrasive solids damage Quantos
heads; hygroscopic powders clog them; Chemspeed SWING and one Unchained
system \emph{failed outright} on fumed silica in the ETC
benchmark~\cite{bahr2018collaborativeevaluationof,carruthers2025amobilerobotic} \\
\addlinespace
Auger / screw feeders on robot arms (Berlinguette \& MacLeod ``Ada''
thin-film SDL; Aspuru-Guzik group platforms; Chemspeed FLEX GDU-Pfd
hopper/auger module) &
Robust to mildly cohesive powders; metered dosing; \SI{\pm10}{\percent}
tolerance setting on GDU-Pfd~\cite{bahr2020recentadvancesin} &
Mechanical complexity; cleaning between materials non-trivial; the Lunt
modular-workflow paper notes ``grinding, mixing and recovering solids
remains an unsolved challenge in commercial
automation''~\cite{lunt2023modularmultirobotintegration,lunt2024aroboticworkflow} \\
\addlinespace
Spatula-mimicking dual-arm robots (Cooper group's
PowderBot~\cite{jiang2023autonomousbiomimeticsolid}) &
Versatile across material classes; \(\sim\)\SI{0.07}{\percent} error at
\SI{200}{\milli\gram} for non-challenging solids; comparable failure rate
to commercial systems (\SI{23.1}{\percent} vs.\ \SI{26.9}{\percent} vs.\
\SI{26.5}{\percent}) at lower hardware
cost~\cite{jiang2023autonomousbiomimeticsolid} &
Slow throughput due to manipulator motions and corrective restarts;
struggles with compressible powders (CaCO\textsubscript{3}) and highly
hygroscopic materials~\cite{jiang2023autonomousbiomimeticsolid} \\
\addlinespace
Slurry-conversion workflows (Ceder group A-Lab: Quantos doses precursors
into vials, ball-milled with ethanol into pumpable
slurry)~\cite{szymanski2023anautonomouslaboratory,szymanski2024automatingthesynthesis,fei2024alabosapythonbased} &
Sidesteps last-mile dry-transfer issues; well-characterised end-to-end
workflow; 36 novel compounds in 17 days &
Adds ethanol handling, drying, and a dedicated \texttt{RecoverPowder}
regrinding task downstream; upstream powder loading is still
manual~\cite{szymanski2024automatingthesynthesis} \\
\addlinespace
Capsule / cartridge ``drop a pre-weighed slug'' &
Eliminates real-time dosing error &
Needs upstream weighing; Quantos cartridge ecosystem in particular
criticised for high cost, single-vendor procurement, RFID-locked reuse,
and clogging on hygroscopic
powders~\cite{carruthers2025amobilerobotic} \\
\addlinespace
Acoustic / ultrasonic non-contact transfer (Echo-style platforms; ultrasonic
capillaries, \SIrange{14}{16}{\micro\gram} through \SI{0.2}{\milli\meter}
nozzles)~\cite{yang2007meteringanddispensing} &
Non-contact, no cross-contamination, very high throughput &
Limited to specific particle sizes / suspensions; mostly demonstrated in
solid-freeforming / additive-manufacturing contexts, not chemistry SDLs \\
\addlinespace
Vacuum / electrostatic pickup (DryPette, Electronic Spatula, automated
electrostatic pipettes)~\cite{yang2007meteringanddispensing,alsenz2011powderpickinganinexpensive} &
Gentle on the powder; good for fragile crystals; \SI{0.3}{\milli\gram}-class
doses possible &
Hard to release a clean dose; \emph{exquisitely} sensitive to humidity,
charge decay, and powder conductivity~\cite{yang2007meteringanddispensing} \\
\addlinespace
Positive-displacement ``PowderPicking'' (standard Gilson MICROMAN pipettes
with disposable capillary-piston tips,
Alsenz)~\cite{alsenz2011powderpickinganinexpensive,cook2021guideto} &
Cheap; \SIrange{0.6}{25}{\milli\gram} range; mean CV \(\sim\)\SI{6}{\percent}
across 10 powders; disposable tips eliminate carryover &
Manual / medium throughput; depends on complete homogeneous filling of the
probe cylinder; tip clogging with adhesive
powders~\cite{alsenz2011powderpickinganinexpensive} \\
\addlinespace
Bulk ``scoop and dump'' mechanical scoops (\textbf{this project}; closest
commercial analogue: MTI PF-A glass dispenser referenced in the community
thread)~\cite{mtipfaglassdispenser} &
Cheap, mechanically simple, no actuators on the end-effector, easy to clean;
the present design has \emph{no consumable} at all &
Not a precision dosing tool; dose CV likely \SIrange{5}{20}{\percent}
depending on whether a strike-off bar is used; not for sub-mg work \\
\end{longtable}
\end{small}

Two recent overviews are particularly relevant for situating a new device
in this landscape: Tom et al.'s 2024 \emph{Chemical Reviews}
survey~\cite{tom2024selfdrivinglaboratoriesfor} and Lunt et al.'s
solid-state-workflow papers~\cite{lunt2023modularmultirobotintegration,lunt2024aroboticworkflow}.
Both flag \emph{bulk powder transfer from stock containers into a precision
dispenser} as a step that is still almost universally manual. On the
frugal-hardware side, recent open-hardware platforms have demonstrated cost
reductions of up to \SI{94}{\percent} relative to commercial analogues for
adjacent dispensing problems (pellet dispensers, 3D-printed
autosamplers)~\cite{hernandezdelvalle2024pelletdispensomixerand,doloi2025democratizingselfdrivinglabs},
albeit for liquid or pellet handling rather than fine inorganic powders.

\subsection{Community prior art from the Accelerated Discovery thread}
\label{sec:thread}

The Accelerated Discovery thread ``Accurate powder dispensing for chemistry
and materials science applications''~\cite{accdiscthread} is a useful,
opinionated cross-section of what practitioners have actually tried. The
points most relevant to our design:

\begin{itemize}[leftmargin=*]
  \item \textbf{Framing (sgbaird, post 1).} Accurate powder dispensing is
    ``around an order of magnitude more complex and more expensive than
    liquid handling.''  This matches the SDL
    surveys~\cite{tom2024selfdrivinglaboratoriesfor} and is the gap we are
    trying to chip away at on the cheap, mechanical end of the design space.
  \item \textbf{3D-printed calibrated spatulas (post 2, after Cook
    et al.~\cite{cook2021guideto}).} Sets of spatulas with known volumes
    give a calibration curve from volume to mass; decent accuracy in
    isolation, but degraded by static in gloveboxes and by lighter powders.
    Two takeaways for us: (i) \textbf{a strike-off bar is essentially
    required} (``just manually tapped the spatula until each scoop is level
    \dots\ it doesn't seem too difficult to physically level it by passing
    something against the top of the scoop'') --- directly endorses the
    strike-off bar variant in Sec.~\ref{sec:variations}; (ii) per-material
    calibration is realistic if the trough is geometrically well-defined.
  \item \textbf{Positive-displacement-pipette method (post 3,
    Alsenz~\cite{alsenz2011powderpickinganinexpensive}).} Packs a pipette
    tip into the powder; spans \SIrange{0.6}{20}{\milli\gram} with
    \(\sim\)\SI{10}{\percent} CV across tip sizes. The
    \SI{10}{\percent} CV is a \textbf{useful baseline target} for our scoop
    on cohesive powders.
  \item \textbf{Auger / screw-feed builds (loppe35, post 4).} Cheap (jewelry-
    scale load cell \(\approx\) USD 25, stepper + control board) but ``leaky
    when dispensing vertically'' and needs hopper flow aids. Reinforces
    keeping the excavator's bucket \emph{un-augered} in the baseline design;
    the auger is positioned in Sec.~\ref{sec:variations} as an optional
    add-on, not the core mechanism.
  \item \textbf{The ``pick it back up'' problem (muon, posts 5/7/14).}
    Dispensing is only half the workflow; recovering powder \emph{after}
    an operation (ball-milling, acoustic mixing, weighing) is at least as
    hard, and a vacuum/pipette approach is awkward when the milled powder
    is fine and multi-precursor cross-contamination matters.
  \item \textbf{Autotrickler v4 + A\&D FX-120i (sgbaird, post 6).}
    \SI{\pm1}{\milli\gram}, fast-response scale, BLE-controllable from a
    Pico W; community-validated reference for the ``scale + metered feed''
    downstream of a bulk-transfer device. Suggests a concrete integration
    target: excavator $\rightarrow$ tared Autotrickler-style
    trickler/scale.
  \item \textbf{PowderBot (Cooper group)~\cite{jiang2023autonomousbiomimeticsolid}
    and A-Lab (Ceder
    group)~\cite{szymanski2023anautonomouslaboratory,fei2024alabosapythonbased}.}
    Two published end-to-end SDLs that \emph{did} solve solids handling, but
    with workflow-specific workarounds (typically involving milling).
  \item \textbf{Manual MTI PF-A glass dispenser (sgbaird, post~24 --- the
    specific post linked in the review feedback)~\cite{mtipfaglassdispenser}.}
    A \SI{250}{\milli\litre} hand dispenser whose geometry is reminiscent
    of Owen Melville's earlier scoop. The closest existing artifact to our
    bucket and effectively a manual ancestor of the excavator's scoop motion.
\end{itemize}

% --------------------------------------------------------------------------
\section{Where the powder-excavator fits}
\label{sec:fits}

The proposed mini excavator is \textbf{not} competing with Quantos-class
precision dispensers. It is aimed at the \textbf{upstream, bulk-transfer
step}: moving a relatively coarse aliquot of powder from a stock bed (e.g.\
a tray, jar, or hopper) to a downstream station --- which might itself be
a precision dispenser, a sieve, a press, a crucible, a dissolution vial,
or simply a weigh boat for a human-in-the-loop workflow. In that niche, the
design choices shown in Fig.~\ref{fig:panels} (post-review) make sense:

\begin{itemize}[leftmargin=*]
  \item \textbf{Half-cylinder ladle suspended on a longitudinal pivot pin.}
    The pin runs along the trough's long axis $L$, through the two short
    end caps, with the two arms gripping those end caps. The trough rolls
    \emph{sideways} about the pin to pour, dispensing over the
    \emph{full long edge} rather than through a narrow end-cap point. This
    eliminates the trapped-volume / arching failure mode that an end-over-
    end tilt of a half-cylinder would have for cohesive powders (Edison v2
    \S3, archived in \texttt{docs/edison/}).
  \item \textbf{Pure mechanical actuation via a fixed smooth inclined cam
    ramp.} Removes the servo and its wiring/maintenance burden; the deposit
    angle is set by how far up the cam the trough's chamfered bumper has
    ridden (i.e.\ by gantry $X$ position), not by a torque setpoint. A
    smooth ramp --- rather than a sawtooth tooth --- is required because a
    fixed point engaging a fixed-radius hook on a horizontally-translating
    pivot is geometrically impossible (Edison v2 \S1).
    Sec.~\ref{sec:pinslot} below describes a stricter ``peg in routed slot''
    refinement of this idea.
  \item \textbf{Mandatory bed-edge strike-off bar.} Promoted from
    ``optional variation'' to a baseline-required part: without a
    level-defining strike-off, dose CV will sit in the
    \SIrange{15}{30}{\percent} range across powder classes, which would
    put the device below the \(\approx\) \SI{10}{\percent} CV baseline
    achievable with Alsenz's positive-displacement-pipette
    method~\cite{alsenz2011powderpickinganinexpensive} and below the
    Cooper PowderBot's \SI{0.07}{\percent} at
    \SI{200}{\milli\gram}~\cite{jiang2023autonomousbiomimeticsolid}.
  \item \textbf{Open top with no lid.} Trades some retention loss for
    radically simpler cleaning --- which, per
    \cite{tom2024selfdrivinglaboratoriesfor,carruthers2025amobilerobotic},
    is the single biggest hidden cost in multi-material SDLs.
  \item \textbf{Optional grounded conductive lining.} Because the pivot
    pin is a metal dowel, it can double as the ground path for an
    inexpensive copper-tape lining of the trough interior. This is the
    prototype-friendly equivalent of using ESD-safe filament and
    dramatically reduces triboelectric charging on fine inorganics
    (Edison v1 \S2).
\end{itemize}

A reasonable framing for a write-up: \emph{``A purely mechanical,
gantry-mounted ladle for bulk powder transfer in self-driving materials
labs, designed to bridge stock containers and precision dispensers without
adding servo count or cleaning burden, and to take over the upstream-loading
and post-process recovery roles flagged as unsolved by Lunt
et al.''}~\cite{lunt2023modularmultirobotintegration,lunt2024aroboticworkflow}.

The design intentionally makes \textbf{no claim} of being a precision
dispenser, and tempers the ``bidirectional dispense + recover'' claim made
in earlier framing: a half-cylinder cannot scoop cleanly out of a flat bed
without leaving a trail of retained powder, so recovery is a meaningful but
lossy operation rather than a complete one (Edison v2 \S7).

% --------------------------------------------------------------------------
\section{Pin-defined-path actuation: a routed-slot refinement}
\label{sec:pinslot}

A hand-sketch (\texttt{PXL\_20260423\_231729467.jpg}) suggests an actuation
refinement that fully resolves the ``approach-and-contact'' ambiguity of
the smooth cam ramp described in Sec.~\ref{sec:fits}. Rather than a free
cam follower that approaches a fixed inclined surface and slides up it, the
trough is suspended from the gantry carriage by a short \emph{stem} that
carries a transverse \emph{peg} at its top end. This peg rides in a
\emph{routed slot} cut into a fixed external board mounted at fixed height
in the work area (Fig.~\ref{fig:pinslot}). The carriage--stem joint is a
pin pivot; the peg is captured in the slot for the entire stroke. Pure-$X$
gantry travel therefore drives a deterministic tilt-vs.-$X$ schedule given
by the slot's routed path: where the slot is straight and horizontal the
trough holds level (scoop, transport); where it deviates, the difference
between the carriage's straight-line path and the slot's routed path forces
the stem (and the trough rigidly attached to it) to rotate about the
carriage pivot.

This is mechanically the same idea as the cam paths used in coin-op
mechanisms, player pianos, and Geneva-style indexing devices, applied to
the gantry geometry of a self-driving lab. Compared with the smooth
inclined cam ramp of Sec.~\ref{sec:fits}, the pin-in-slot refinement has
several concrete advantages:

\begin{itemize}[leftmargin=*]
  \item \textbf{No engagement event.} The peg never has to ``find'' the
    cam; it is captive in the slot from the moment the trough is mounted.
    There is no lift-off direction in which the contact can lose registration.
  \item \textbf{Bidirectional and reversible.} The slot path constrains
    motion in both $+X$ and $-X$ directions, so the trough can be tipped,
    held, and \emph{returned to level} purely by gantry motion. The smooth
    cam ramp relies on gravity for the return.
  \item \textbf{Programmable schedule.} The slot is the program. Different
    routed slots --- straight-then-rising, multi-stage with a hold detent,
    a small ``knock'' wiggle to dislodge bridges (Edison v1 \S6) ---
    implement different dispensing schedules without any change to the
    trough or carriage. The strike-off bar sweep can be encoded as a small
    detent in the slot near the bed-edge $X$ coordinate.
  \item \textbf{Deterministic tilt at deposit.} Because the peg is captured
    on both sides of the slot wall, the deposit angle is set by slot
    geometry to the tolerance of the routing operation, not by friction at
    a sliding cam interface.
  \item \textbf{Simpler statics analysis.} The slot wall provides both the
    tilt-up reaction force and (on the return stroke) the tilt-down force.
    The smooth cam ramp only provides the former; the latter relies on
    gravity, which fails for very light troughs or when the trough is empty.
\end{itemize}

\paragraph{Caveats.} The slot must be cut to the same accuracy as the
finished tilt schedule requires; a cleanly milled slot in acrylic or
aluminium is straightforward, but FDM-printed slots will have layer-line
ripples that the peg will feel as a low-amplitude tilt jitter. The peg
should be a hardened dowel pin with a low-friction sleeve (PTFE or oil-
impregnated bronze) to minimise stick-slip, and the slot should be slightly
oversized in the direction perpendicular to the desired motion to allow
thermal play without binding. The board itself becomes a second
\emph{registered} fixture in the work area --- it must be mounted in a
known relationship to the gantry's $X$ axis, which is the same registration
problem the bed and the deposit station already face, and so does not
introduce a new class of failure.

% Place the four-panel layout figure environment up here so it floats
% sensibly relative to the references that point at it.
\begin{figure}[ht]
  \centering
  \includegraphics[width=0.95\linewidth]{../figures/panel-A-orthographic}
  \caption{Orthographic views of the half-cylinder trough with the
    longitudinal pivot pin, end-cap pivot bosses, and the chamfered bumper
    that engages the cam ramp. Generated by
    \texttt{scripts/generate\_figures.py}.}
  \label{fig:panels}
\end{figure}

\begin{figure}[ht]
  \centering
  \includegraphics[width=0.85\linewidth]{../figures/panel-E-pin-slot}
  \caption{Pin-defined-path actuation variant (Sec.~\ref{sec:pinslot}). A
    vertical stem hangs from the gantry carriage on a pivot; a transverse
    peg at the top of the stem rides in a routed slot cut into a fixed
    external board. The slot's shape over $X$ is the program for the
    trough's tilt schedule. Generated by
    \texttt{scripts/generate\_figures.py}.}
  \label{fig:pinslot}
\end{figure}

% --------------------------------------------------------------------------
\section{Open questions and what we'd actually need to measure}
\label{sec:measure}

To defend the design in a manuscript-style argument we would need at
minimum:

\begin{itemize}[leftmargin=*]
  \item \textbf{Dose statistics across powder classes.} Mean and CV of
    delivered mass for at least three archetypal powders (e.g.\
    free-flowing crystalline like NaCl, cohesive metal-oxide nanopowder
    like TiO\textsubscript{2}, hygroscopic salt like LiCl) across at least
    30 scoops each. Following Cooper-group
    practice~\cite{jiang2023autonomousbiomimeticsolid}, this should also
    include the known ``hard'' cases --- fumed silica (which broke the
    Chemspeed SWING and one Unchained system in the ETC
    benchmark~\cite{bahr2018collaborativeevaluationof}) and CaCO\textsubscript{3}
    (which broke the PowderBot~\cite{jiang2023autonomousbiomimeticsolid}).
  \item \textbf{Standardised flowability descriptors per powder.} Report
    Carr's compressibility index (CI $\le$ \SI{10}{\percent} = excellent;
    \SIrange{21}{25}{\percent} = passable; $>$\SI{35}{\percent} = very poor)
    and the Hausner ratio (HR \numrange{1.00}{1.11} = excellent;
    \numrange{1.26}{1.34} = passable; $>$\num{1.45} = poor) for every test
    powder, plus Freeman FT4 basic flow energy (BFE) and specific energy
    (SE) where
    available~\cite{moravkar2020traditionalandadvanced,freeman2017characterisingpowderflow,ghoroi2013multifacetedcharacterizationof}.
  \item \textbf{Carryover / cross-contamination.} Mass remaining in the
    trough after a ``tip and pour'' event vs.\ after a programmed cleaning
    cycle (knock-oscillation against the cam, inverted shake, brush, or
    air blast), stratified by powder class, following the approach
    Carruthers used to expose Quantos-cartridge
    limitations~\cite{carruthers2025amobilerobotic}.
  \item \textbf{Sensitivity to bed depletion.} How much does the dose
    change as the powder bed depletes / gets cratered? Run 30 consecutive
    scoops from the same $X,Y$ location and plot dispensed mass vs.\ scoop
    number (Edison v1 \S3). The expected steep decay curve will set the
    requirement that the gantry must raster across the bed.
  \item \textbf{Coupling to a downstream balance.} Demonstrate that the
    excavator $\rightarrow$ balance $\rightarrow$ vibratory-head pipeline
    reduces total wall-clock time per dispensed dose vs.\ a one-stage
    precision dispenser doing both bulk and fine work --- i.e.\ directly
    attack the upstream-loading bottleneck flagged
    by~\cite{tom2024selfdrivinglaboratoriesfor,lunt2023modularmultirobotintegration,lunt2024aroboticworkflow,carruthers2025amobilerobotic}.
  \item \textbf{Mandatory benchmark experiments (Edison v2 \S6).}
    \begin{enumerate}
      \item \textbf{Cam-engagement test.} 3D print the trough, the
        chamfered bumper, and the inclined cam track. Drive the gantry
        purely in $X$ and verify the bumper rides up the cam without
        binding, skipping, or requiring coordinated $Z$ motion.
      \item \textbf{Pin-slot equivalence test.} Repeat the same dispense
        schedule with the cam ramp of Sec.~\ref{sec:fits} and the routed
        slot of Sec.~\ref{sec:pinslot}; compare tilt-angle repeatability
        and dose CV.
      \item \textbf{Trapped-volume bake-off.} Compare retained mass of a
        cohesive test powder (TiO\textsubscript{2} or flour) for a sideways
        tilt vs.\ a hypothetical end-over-end tilt of the same trough. The
        expected \SIrange{7}{26}{\percent} retention penalty of the
        end-over-end case (Edison v2 \S3) is the empirical justification
        for the longitudinal-pivot geometry.
      \item \textbf{Strike-off efficacy.} Measure the dose mass of 30
        consecutive scoops with and without the bed-edge strike-off bar.
        The expected $2$--$3\times$ CV improvement is the empirical
        justification for keeping the strike-off bar in the baseline.
    \end{enumerate}
  \item \textbf{Cam-ramp / strike-off / bumper geometry sweep.} Cam slope,
    ramp length, strike-off cross-section, and rim-bumper chamfer angle are
    the four knobs most likely to dominate dose CV; small parameter sweeps
    are cheap with 3D-printed parts. For the pin-slot variant, the
    equivalent sweep is over slot path shape, peg diameter, and peg sleeve
    material.
\end{itemize}

% --------------------------------------------------------------------------
\section{Design variations worth prototyping (still pure-mechanical)}
\label{sec:variations}

Carrying over from the original brainstorming, with the literature in mind:

\begin{itemize}[leftmargin=*]
  \item \textbf{Pin-defined-path actuation (Sec.~\ref{sec:pinslot}).}
    Replaces or augments the smooth cam ramp; the slot board is the new
    fixed-fixture part. Worth prototyping side-by-side with the cam ramp
    to compare schedule programmability and dose CV.
  \item \textbf{Dual cam ramps (or dual slot boards), left and right} ---
    for two-output workflows (e.g.\ one for ``real'' deposit, one for
    ``purge / waste'' to clear residual material between materials).
  \item \textbf{Strike-off bar variants} --- a square cross-section vs.\ a
    chamfered blade vs.\ a thin compliant flap, scored for fill
    repeatability and for how cleanly the bar sweeps the rim of cohesive
    powders without flicking material away.
  \item \textbf{Twin troughs back-to-back} --- fill one while dumping the
    other for doubled throughput at the cost of one extra carriage stop.
  \item \textbf{Replaceable, snap-in trough liners} --- a thin,
    single-material liner (e.g.\ ESD-safe filament or copper-tape-lined
    PETG) that snaps into the printed trough body. Lets us treat the
    trough as consumable per-material and bypass the cleaning problem
    entirely; this is the prototype-friendly analogue of Quantos
    cartridges~\cite{carruthers2025amobilerobotic} without the RFID
    lock-in.
  \item \textbf{Spring-loaded passive flap lid actuated by the same cam or
    slot} --- closes during transport (curing the fine-powder retention
    problem) and opens at the same instant the cam (or slot detent)
    engages, with no extra actuator.
  \item \textbf{Internal auger as an \emph{option}} --- adds one rotary
    actuator but converts the device from ``tilt and pour all'' to a
    coarse metered dispenser, which would squarely overlap with mid-range
    commercial systems~\cite{bahr2020recentadvancesin}.
\end{itemize}

% --------------------------------------------------------------------------
\section{Open parametric CAD pipeline and design-for-manufacturing feedback}
\label{sec:cad-pipeline}

A central pragmatic constraint placed on this design by the project's
requirements is that the dispenser must run on an \emph{existing} gantry
(X / Y / Z) without any additional actuator on the bucket --- a ``no second
axis'' constraint. To make this constraint enforceable as the design
iterates, the same dimensions that drive Figures~\ref{fig:panels} and~\ref{fig:pinslot} and
the prior-art arguments above also drive a small open-source parametric
CAD pipeline shipped with this manuscript under \texttt{cad/} in the
project repository.

The choice of authoring tool was deliberately restricted to \emph{open,
pip-installable} options so that anyone re-running this pipeline pays only
the price of \texttt{pip install cadquery}. CadQuery
(\url{https://github.com/CadQuery/cadquery}) was chosen over the
commercial parametric / generative-CAD ecosystems (Rhino + Grasshopper,
Fusion 360 Generative Design, nTop, Onshape FeatureScript) because it is
pure Python, runs unattended on a CI runner, and emits standards-compliant
STEP and STL output that any open-source slicer (PrusaSlicer, OrcaSlicer,
Cura) can consume. Sister tools (\texttt{build123d} and OpenSCAD) fit the
same niche and remain candidates as the design matures; a separate
high-effort literature task on generative / computational CAD for
mechanical hardware is in flight and will be folded into a future revision.

The pipeline has three stages, all driven by a single
\texttt{ExcavatorParams} dataclass that holds every dimension in
millimetres:

\begin{enumerate}
  \item \textbf{Authoring} (\texttt{cad/excavator.py}). Each part --- the
    half-cylinder trough with its closed end caps and pivot bosses, the
    two vertical arms, the dowel pin, the bed-edge strike-off bar, the
    smooth inclined cam ramp, and the routed slot board for the
    pin-defined-path variant of \S\ref{sec:pinslot} --- is a plain Python
    function that takes \texttt{ExcavatorParams} and returns a CadQuery
    solid. Because every dimension lives in the dataclass, a design
    iteration is a \texttt{git diff} on a single file.
  \item \textbf{Build} (\texttt{cad/build.py}). Exports STEP and STL for
    every part plus a STEP for the full assembly into \texttt{cad/build/}
    (gitignored), along with a JSON manifest containing the parameter
    snapshot used.
  \item \textbf{Feedback} (\texttt{cad/dfm.py}). Runs an automated battery
    of design-for-manufacturing and gantry-only-kinematics checks against
    the current parameter set and exits non-zero on failure --- making it
    suitable to drop into CI. Categories of checks include FDM
    printability (minimum wall thickness, FDM overhang angle on the
    cam-ramp underside, bumper chamfer presence, dowel-pin clearance);
    cam-ramp kinematics (bumper engagement, ramp fits inside the gantry's
    X travel, ramp angle in a 15--45\textdegree band); and, most
    importantly for the no-second-axis constraint, slot-path kinematics
    (every waypoint inside the routed board, the slot's X and Z spans
    fitting inside the gantry's travel, and a flag on any X-direction
    reversal in the slot path so that bidirectional gantry motion is
    surfaced explicitly to the designer).
\end{enumerate}

Three small unit tests (\texttt{cad/tests/test\_excavator.py}) exercise (i)
that every part builds at default parameters, (ii) that the DFM check
passes at default parameters, and (iii) that two deliberate parameter
regressions --- a sub-minimum trough wall and a slot path routed off the
board --- are correctly caught by the DFM check. This is the start of a
closed-loop generative-CAD workflow rather than the finished product;
near-term extensions are to add a \emph{slicer-side} check
(e.g.\ delegating support volume estimation to PrusaSlicer's CLI) and a
\emph{print-then-measure} loop in which a successful print of the trough
is photographed and analysed with classical CV to extract its as-built
inner radius and wall thickness, closing the loop on the parametric
inputs.

% --------------------------------------------------------------------------
\bibliographystyle{plainurl}
\bibliography{refs}
\label{sec:references}

\end{document}

```

=== file: docs/edison/analysis-v2-corrected-gondola.md ===
```md
The "ferris-wheel gondola" redesign solves the major issues of the previous axis-of-rotation error, creating a mechanically sound baseline with stable pendulum action. However, the proposed pure-X actuation for end-over-end tipping contains a fatal kinematic flaw, and the behavior of cohesive powders inside a long, narrow semicircular channel necessitates a fundamental re-evaluation of both geometry and framing.

### 1. The Fatal Flaw: Kinematic impossibility of the push-to-tilt mechanism
The most critical issue with the current design is that step 3 ("Tip end-over-end -> deposit") **is kinematically impossible as drawn.**

*   The pivot pin translates purely horizontally (constant Z).
*   The sawtooth ledge is fixed in space (constant X, Z).
*   The hooked end-lip is at a fixed radius ($r_p \approx 40$ mm for $L=80$ mm) from the pivot pin.

For a fixed tooth to engage a point-like hook on the lip while the pivot translates purely in X, the distance from the pivot to the tooth must equal the constant radius $r_p$. However, pure horizontal translation necessarily changes this distance. As the gantry pushes forward, the distance drops below $r_p$, meaning the lip must physically plunge *through* the solid tooth/ledge. 

**The fix:** To achieve rotation without an actuator, the gantry *must* coordinate X and Z motion (moving the carriage in a circular arc centered on the engaged tooth), OR the "tooth" cannot be a fixed point but rather an inclined cam track that the lip slides up, OR the arm must be a telescopic/sprung compliant member. 

### 2. Mechanical Soundness of the Gondola
Assuming the kinematic issue is patched, the gondola arrangement itself is excellent.
*   **Stability:** The geometric center of mass of a semicircular cross-section is $4r/3\pi$, or 5.66 mm below the flat rim for a 26.7 mm diameter trough. Placing the pivot pin 2-4 mm above the loaded centroid ensures gravity strongly rights the trough ($>0.003$ Nm restoring moment), returning it to open-up without actuators.
*   **Structural Loads:** For an 80 mm long, 22.3 mL trough holding $\sim$22 g of powder (bulk density 1000 kg/m$^3$), the vertical force per 3D-printed PETG arm is just $\sim$0.11 N. The resulting bending moment at the carriage root is a negligible $\sim$0.003 Nm, producing $<0.2$ MPa of stress (well within PETG's 50 MPa yield strength).

### 3. Powder-Handling Realism
The geometry presents severe powder retention risks for dozens-of-microns cohesive powders (where wall friction angles $\phi_w$ routinely exceed 45° and unconfined yield strengths $\sigma_c$ exceed 100-500 Pa):
*   **The "Trapped Volume" problem:** When tilted end-over-end to 45°, the semicircular channel and the vertical end-cap form a 90° V-pocket. By integrating the enclosed volume, a perfectly fluid powder at 45° tilt still leaves 7.1% (1.58 mL) trapped below the spill lip. For a cohesive powder with a 30° angle of repose, the *effective* tilt at 45° is only 15°, trapping 26.4% (5.9 mL) of the dose.
*   **Bridging & Flow:** To pour, the powder must flow down a narrow 26.7 mm wide half-pipe. Cohesive powders will bridge across this small diameter and slump as a single solid plug, or stick entirely.
*   **Mitigation:** An ESD-safe filament is insufficient here. You will need a significant geometry change: either (a) eliminate the end-cap entirely, making it an open chute (but sacrificing transport capacity), or (b) abandon the end-over-end tilt in favor of tilting sideways (axis parallel to L), which pours over a massive 80 mm long edge where arching is impossible.

### 4. Repeatability & Dose CV
Volumetric scooping into cohesive powders is notoriously variable. Without a leveling step, dose CV will likely sit between 15-30% due to variable mounding and bridging. 
*   **Strike-off bar:** Implementing the strike-off bar (§5) is mandatory to hit the 10% CV baseline established by Alsenz's positive-displacement method.
*   **End-over-end vs. sideways pour:** A sideways tilt drops the entire dose uniformly over the long 80 mm edge. The current end-over-end tilt forces 22 mL of powder to bottleneck through a $\sim$13 mm radius spill point, massively increasing the likelihood of rat-holing and chugging (flow-stop-flow behavior).

### 5. Sawtooth Engagement
Given the kinematic impossibility outlined in §1, a printed end-lip + tooth will simply snap or stall the gantry. The sawtooth ledge must be converted into a smooth, inclined cam profile. A chamfered lip sliding along a polished/lubricated cam track will tilt the bucket repeatably without jamming.

### 6. Suggested Benchmark Experiments
1.  **Kinematic Cam Profile Test:** 3D print the trough and a passive inclined cam track. Drive the gantry purely in X to verify the bucket tilts without binding or requiring Z-coordination.
2.  **The "Trapped Volume" Bake-off:** Compare the retained mass of a cohesive test powder (e.g., TiO2 or flour) dumped from an end-over-end tilt versus a sideways tilt.
3.  **Strike-off Efficacy:** Measure the dose mass of 30 consecutive scoops with and without a fixed bed-leveling blade.

### 7. Framing Pushback: The "Bulk-Transfer" Position
Your positioning in the literature section is highly defensible and smartly avoids competing with Quantos-class systems. Claiming the "bulk transfer feeds precision dispenser" niche directly answers the unsolved automation bottleneck cited by *Materials Horizons* and *ChemRxiv*. However, the "dispense AND recover" (bidirectional) feature highlighted from the community thread is compromised by the trapped volume problem—an open half-pipe simply cannot scoop cleanly out of a flat bed without leaving a trail.

**Discretionary Analytical Decisions:**
*   Assumed a standard gantry translating purely in X and Z axes without rotary or coordinated multi-axis interpolation during the dump phase.
*   Estimated trough volume ($\sim$22.3 mL) and dimensions based on the $L \approx 3D$ and $L \approx 80$ mm constraints provided in the prompt.
*   Calculated structural loads assuming standard 3D printed PETG mechanical properties and typical inorganic powder bulk densities ($800-1600$ kg/m$^3$).
*   Assessed powder flow assuming typical cohesive unconfined yield strengths ($>100$ Pa) and high wall friction angles ($>40^\circ$) characteristic of dozens-of-microns ceramic/catalyst powders.
*   Trapped volume integral modeled the powder as fluid with definable angles of repose to establish the geometric bounds of the end-cap spill problem.

```

=== file: cad/README.md ===
```md
# Parametric CAD pipeline

This directory holds the **scripted, open-source parametric CAD model** for
the powder-excavator design discussed in `docs/manuscript/main.tex` and
`README.md`. It is the start of a feedback-loop-friendly hardware design
pipeline:

```
ExcavatorParams (single source of truth, mm)
        │
        ├──► excavator.py  ──► CadQuery solids (trough, arms, pin, …)
        │                          │
        │                          ├──► build.py  ──► STEP + STL + manifest.json
        │                          │
        │                          └──► (open in CQ-editor / FreeCAD / KiCAD-AS-PCB / …)
        │
        └──► dfm.py  ──► automated checks
                            • FDM printability (min wall, overhang)
                            • gantry-only kinematics (no second axis on the bucket)
                            • cam-ramp and pin-slot reachability
```

## Why CadQuery (instead of Rhino/Grasshopper, Fusion, nTop, …)?

Per PR #2 the user asked for **something open that you can install and run**.
Rhino + Grasshopper, Fusion 360 (and its Generative Design module), nTop, and
Onshape FeatureScript are all powerful but commercial — they don't survive
the "freshly-cloned repo on a CI runner" test.

[CadQuery](https://github.com/CadQuery/cadquery) is a pip-installable, pure-
Python parametric kernel built on top of OCCT (the same kernel FreeCAD uses).
That makes it a natural fit for this repo:

* `pip install cadquery` is the only setup step.
* The model is plain Python source code, so a "design iteration" is a
  `git diff` plus a `python -m cad.build` re-run.
* Outputs are STEP and STL — every open-source slicer (PrusaSlicer,
  OrcaSlicer, Cura) and every CAD viewer (FreeCAD, OCC's CAD Assistant,
  KiCAD's 3D viewer) can read them.

Sister tools that fit the same niche and are worth considering as the design
matures are [`build123d`](https://github.com/gumyr/build123d) (a re-imagined
CadQuery API by the same community) and
[OpenSCAD](https://openscad.org/) (a constructive solid geometry DSL).
The Edison Scientific generative-CAD literature task (`task_id`
`524e7e92-a326-440a-b6fd-f6eb220d9019`, still pending at the time of this
commit) is intended to widen this comparison.

## Files

| File | What it is |
|---|---|
| [`excavator.py`](excavator.py) | Parametric model. `ExcavatorParams` dataclass + `build_*` functions for the trough, arms, pivot pin, strike-off bar, smooth cam ramp, and the pin-slot board (Panel E variant). |
| [`build.py`](build.py) | Exporter — writes STEP + STL for every part and a STEP for the assembly into `cad/build/`, plus a `manifest.json` with the parameter snapshot. |
| [`dfm.py`](dfm.py) | **Feedback mechanism.** Runs FDM-printability and gantry-only kinematics checks against the current parameter set; non-zero exit code on failure (CI-friendly). |
| [`tests/test_excavator.py`](tests/test_excavator.py) | Unit tests: parts build at default parameters, DFM passes at defaults, deliberate regressions (sub-min-wall trough, off-board slot path) are caught. |

## Usage

From the repo root:

```bash
# install (one-time)
pip install cadquery

# generate STEP/STL for every part + assembly + the manifest
python -m cad.build

# run the design-for-manufacturing + gantry-kinematics feedback
python -m cad.dfm

# run the unit tests
python -m unittest discover cad/tests -v
```

The default parameter set in `ExcavatorParams` matches the dimensions called
out in `docs/manuscript/main.tex` (trough length L = 80 mm, L ≈ 3 D, etc.).
Iterate by editing `excavator.py` (or constructing a modified
`ExcavatorParams` with `dataclasses.replace(...)` from a notebook) and
re-running `python -m cad.dfm` — that is the feedback loop.

## What `dfm.py` actually checks

Categories of checks (each prints `[OK]` / `[WARN]` / `[FAIL]`):

* **`sanity.*`** — every dimension must be positive.
* **`fdm.*`** — printability for FDM (min wall thickness ≥ `min_wall`,
  cam-ramp underside overhang ≤ `max_overhang_deg`, bumper chamfer present,
  pin clearance positive).
* **`kinematics.cam.*`** — bumper engages the smooth cam ramp; ramp fits
  inside the gantry's X travel; ramp angle is in the 15–45° band.
* **`kinematics.slot.*`** — the **gantry-only constraint** from PR comment
  4166621470 ("we have a gantry system and would like to avoid installing
  a second axis"): every slot waypoint lies inside the board, the slot's X
  span fits inside `gantry_x_travel`, and the slot's Z span fits inside
  `gantry_z_travel`. Reversals in the slot's X direction are flagged as
  warnings (legal — the gantry just reverses — but worth surfacing).

The exit code is `0` if every error-severity check passes (warnings do not
fail the run), so `python -m cad.dfm` is suitable to drop into CI as a
guardrail for future parameter changes.

```

=== file: cad/excavator.py ===
```py
"""Parametric CAD model of the powder-excavator (CadQuery / open-source).

This is the start of a **feedback-loop friendly** CAD pipeline for the
powder-excavator design described in ``docs/manuscript/main.tex``. CadQuery
was chosen over closed-source authoring tools (Rhino + Grasshopper, Fusion
Generative Design, nTop, Onshape FeatureScript) because it is

* pure Python and pip-installable on every major OS,
* fully scripted (no GUI required for parametric updates), so a design
  iteration is just a ``git diff`` and a re-run, and
* produces standards-compliant STEP and STL output that any open-source
  slicer (PrusaSlicer, OrcaSlicer, Cura) can consume.

The single source of truth for every dimension is :class:`ExcavatorParams`.
Changing one number there propagates through every part.

Usage
-----

Build all parts and the assembly to ``cad/build/`` (run from the repo root)::

    python -m cad.build

Run the design-for-manufacturing checks (per-part wall thickness, FDM
overhang angles, gantry-only kinematics)::

    python -m cad.dfm

Both modules import :func:`build_assembly` from this file, so the same
parametric model drives both the export and the feedback checks.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

import cadquery as cq

# Type alias for cadquery objects we hand back to the caller.
CQObject = Any


# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ExcavatorParams:
    """All design parameters for the powder-excavator, in millimetres.

    Defaults match the dimensions called out in the README and
    ``docs/manuscript/main.tex`` for the longitudinal-pivot, sideways-tilt
    geometry (trough length L = 80 mm, L ~ 3 D, etc.). Mutating values is
    forbidden so the model is reproducible: build a new instance instead.
    """

    # ----- trough (the half-cylinder ladle, open at the top) -----
    trough_length: float = 80.0           # L, along the long pivot axis
    trough_radius: float = 13.0           # inner radius of the half-cylinder
    trough_wall: float = 1.6              # printed wall thickness
    end_cap_thickness: float = 2.0        # closed end caps at +/- L/2

    # ----- pivot (a metal dowel pin running along L through both end caps) -
    pin_diameter: float = 3.0
    pin_clearance: float = 0.2            # diametral clearance, sliding fit
    pivot_boss_diameter: float = 8.0      # local boss around the pin hole
    pivot_boss_thickness: float = 4.0

    # ----- arms (two parallel verticals dropping from the gantry) -----
    arm_thickness: float = 4.0            # in X (gantry-travel direction)
    arm_width: float = 8.0                # in Y, must clear pivot boss
    arm_length: float = 60.0              # vertical drop from carriage
    arm_gap: float = 1.0                  # gap between arm inside face and trough end cap

    # ----- chamfered bumper on the trough (engages the cam ramp) -----
    bumper_height: float = 6.0            # how far the bumper protrudes radially
    bumper_chamfer: float = 2.0
    bumper_width: float = 6.0             # along L

    # ----- fixed bed-edge strike-off bar -----
    strike_off_length: float = 100.0      # spans the bed edge
    strike_off_section: float = 4.0       # square cross-section side

    # ----- smooth inclined cam ramp (baseline tilt actuator) -----
    cam_ramp_length: float = 40.0         # along gantry X
    cam_ramp_rise: float = 20.0           # vertical rise across the ramp
    cam_ramp_width: float = 10.0          # along gantry Y
    cam_ramp_thickness: float = 8.0       # below the running surface

    # ----- pin-slot variant (per PXL_20260423_231729467.jpg, manuscript Sec. ``Pin-defined-path actuation'') -----
    slot_board_length: float = 220.0      # along gantry X
    slot_board_height: float = 60.0       # along gantry Z
    slot_board_thickness: float = 6.0     # along gantry Y
    slot_width: float = 4.2               # peg diameter + clearance
    slot_depth: float = 5.0               # routed depth into the board
    # Polyline of (X, Z) waypoints describing the slot path on the board, in
    # the board's local frame (origin at the bottom-left corner of the board).
    # Default is the same path baked into ``panel-E-pin-slot.svg``: flat for
    # the scoop+transport stretch, rising over the deposit station.
    slot_path: tuple[tuple[float, float], ...] = (
        (10.0, 30.0),
        (140.0, 30.0),
        (170.0, 24.0),
        (200.0, 12.0),
        (210.0, 12.0),
    )

    # ----- gantry working envelope (used by dfm.py's kinematic checks) -----
    gantry_x_travel: float = 250.0
    gantry_z_travel: float = 80.0

    # ----- FDM-printability targets (used by dfm.py's printability checks) -
    min_wall: float = 0.8                 # absolute minimum FDM wall (4-perimeter @ 0.2 mm)
    max_overhang_deg: float = 50.0        # measured from vertical; >50 needs supports

    # Optional metadata (e.g. the git SHA of the design used). Excluded from
    # geometry but useful when the build script writes a manifest.
    metadata: dict[str, str] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Individual parts
# ---------------------------------------------------------------------------


def _half_disk_solid(radius: float) -> cq.Workplane:
    return (
        cq.Workplane("XY")
        .moveTo(-radius, 0)
        .lineTo(radius, 0)
        .threePointArc((0, -radius), (-radius, 0))
        .close()
    )


def build_trough(p: ExcavatorParams) -> CQObject:
    """The open-top half-cylinder ladle with closed end caps and pivot bosses.

    The trough is built lying along the +Z axis (length L along Z), with its
    open top facing +Y, so that the longitudinal pivot pin runs through the
    centre of the two end caps along Z.
    """
    # Outer solid (full length, full outer radius)
    outer = _half_disk_solid(p.trough_radius + p.trough_wall).extrude(p.trough_length)
    # Inner cavity (full outer minus end caps -> length L - 2 * cap)
    cavity_len = p.trough_length - 2 * p.end_cap_thickness
    cavity = (
        _half_disk_solid(p.trough_radius)
        .extrude(cavity_len)
        .translate((0, 0, p.end_cap_thickness))
    )
    body = outer.cut(cavity)

    # Pivot bosses sit on the OUTSIDE of each end cap. Their axis is along
    # Z. We place them on the longitudinal centre line of the half-cylinder,
    # which (since the half-disk hangs into -Y from the flat edge at Y=0)
    # is at (X=0, Y=-radius/2) -- approximately the centroid.
    pivot_centre_y = -p.trough_radius / 2
    boss = (
        cq.Workplane("XY")
        .center(0, pivot_centre_y)
        .circle(p.pivot_boss_diameter / 2)
        .extrude(p.pivot_boss_thickness)
    )
    boss0 = boss.translate((0, 0, -p.pivot_boss_thickness))
    boss1 = boss.translate((0, 0, p.trough_length))

    # Drill the pin clearance hole through caps + bosses (one pass along Z).
    pin_hole_len = p.trough_length + 2 * p.pivot_boss_thickness + 2.0
    pin_hole = (
        cq.Workplane("XY")
        .center(0, pivot_centre_y)
        .circle((p.pin_diameter + p.pin_clearance) / 2)
        .extrude(pin_hole_len)
        .translate((0, 0, -p.pivot_boss_thickness - 1.0))
    )

    # Chamfered bumper on the rim's outside, near mid-length.
    bumper_z_centre = p.trough_length / 2
    bumper = (
        cq.Workplane("XY")
        .center(0, p.trough_radius + p.trough_wall + p.bumper_height / 2)
        .box(
            p.bumper_width,        # X
            p.bumper_height,       # Y
            p.bumper_width,        # Z
            centered=(True, True, True),
        )
        .translate((0, 0, bumper_z_centre))
        .edges("|Z").chamfer(p.bumper_chamfer)
    )

    return body.union(boss0).union(boss1).union(bumper).cut(pin_hole)


def build_arm(p: ExcavatorParams) -> CQObject:
    """One vertical arm.

    Two of these are mirrored about z = L/2 to grip the trough's two end
    caps. The arm hangs from a carriage above it (not modelled here) and has
    a clearance hole for the pivot pin near its bottom.
    """
    arm = (
        cq.Workplane("XY")
        .box(p.arm_thickness, p.arm_width, p.arm_length, centered=(True, True, False))
    )
    pin_hole = (
        cq.Workplane("YZ")
        .circle((p.pin_diameter + p.pin_clearance) / 2)
        .extrude(p.arm_thickness * 2, both=True)
        .translate((0, 0, p.arm_thickness / 2))
    )
    return arm.cut(pin_hole)


def build_pin(p: ExcavatorParams) -> CQObject:
    """Stock metal dowel pin (the pivot)."""
    total_length = (
        p.trough_length
        + 2 * p.pivot_boss_thickness
        + 2 * (p.arm_gap + p.arm_thickness)
    )
    return (
        cq.Workplane("XY")
        .circle(p.pin_diameter / 2)
        .extrude(total_length)
    )


def build_strike_off_bar(p: ExcavatorParams) -> CQObject:
    """The fixed bed-edge strike-off bar (square cross-section)."""
    return (
        cq.Workplane("XY")
        .box(p.strike_off_section, p.strike_off_length, p.strike_off_section)
    )


def build_cam_ramp(p: ExcavatorParams) -> CQObject:
    """The fixed smooth inclined cam ramp the bumper rides up.

    Built as a triangular prism plus a flat mounting base.
    """
    triangle = (
        cq.Workplane("XZ")
        .moveTo(0, 0)
        .lineTo(p.cam_ramp_length, 0)
        .lineTo(p.cam_ramp_length, p.cam_ramp_rise)
        .close()
    )
    ramp = triangle.extrude(p.cam_ramp_width)
    base = (
        cq.Workplane("XY")
        .box(
            p.cam_ramp_length,
            p.cam_ramp_width,
            p.cam_ramp_thickness,
            centered=(False, False, False),
        )
        .translate((0, 0, -p.cam_ramp_thickness))
    )
    return ramp.union(base)


def build_slot_board(p: ExcavatorParams) -> CQObject:
    """Routed slot board for the pin-defined-path actuation variant.

    The board is a rectangular slab with a slot routed along the polyline
    given by ``params.slot_path``. The slot is a fixed-width channel; the peg
    on the trough's stem rides inside it.
    """
    board = (
        cq.Workplane("XZ")
        .box(p.slot_board_length, p.slot_board_height, p.slot_board_thickness)
    )
    # Build the slot as the union of "fat segments" (one per polyline edge),
    # avoiding CadQuery's arbitrary-path sweep which is brittle across
    # versions.
    slot_solid: CQObject = None
    for (x0, z0), (x1, z1) in zip(p.slot_path, p.slot_path[1:]):
        wx0 = x0 - p.slot_board_length / 2
        wz0 = z0 - p.slot_board_height / 2
        wx1 = x1 - p.slot_board_length / 2
        wz1 = z1 - p.slot_board_height / 2
        seg_len = math.hypot(wx1 - wx0, wz1 - wz0)
        if seg_len <= 0:
            continue
        ang_deg = math.degrees(math.atan2(wz1 - wz0, wx1 - wx0))
        seg = (
            cq.Workplane("XZ")
            .box(
                seg_len + p.slot_width,
                p.slot_width,
                p.slot_depth * 2,
                centered=(True, True, True),
            )
        )
        seg = seg.rotate((0, 0, 0), (0, 1, 0), -ang_deg)
        seg = seg.translate(((wx0 + wx1) / 2, 0, (wz0 + wz1) / 2))
        slot_solid = seg if slot_solid is None else slot_solid.union(seg)
    if slot_solid is not None:
        board = board.cut(slot_solid)
    return board


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------


def build_assembly(p: ExcavatorParams | None = None) -> cq.Assembly:
    """Build the full assembly (trough + two arms + pin)."""
    p = p or ExcavatorParams()
    trough = build_trough(p)
    arm = build_arm(p)
    pin = build_pin(p)

    asm = cq.Assembly(name="powder_excavator")
    asm.add(trough, name="trough", color=cq.Color(0.7, 0.7, 0.75))

    pivot_centre_y = -p.trough_radius / 2
    arm_outer_z0 = -p.pivot_boss_thickness - p.arm_gap - p.arm_thickness / 2
    arm_outer_z1 = (
        p.trough_length + p.pivot_boss_thickness + p.arm_gap + p.arm_thickness / 2
    )
    asm.add(
        arm,
        name="arm_left",
        loc=cq.Location(cq.Vector(0, pivot_centre_y, arm_outer_z0)),
        color=cq.Color(0.4, 0.4, 0.45),
    )
    asm.add(
        arm,
        name="arm_right",
        loc=cq.Location(cq.Vector(0, pivot_centre_y, arm_outer_z1)),
        color=cq.Color(0.4, 0.4, 0.45),
    )
    asm.add(
        pin,
        name="pin",
        loc=cq.Location(cq.Vector(
            0, pivot_centre_y,
            -(p.pivot_boss_thickness + p.arm_gap + p.arm_thickness),
        )),
        color=cq.Color(0.85, 0.2, 0.2),
    )

    return asm


__all__ = [
    "ExcavatorParams",
    "build_arm",
    "build_assembly",
    "build_cam_ramp",
    "build_pin",
    "build_slot_board",
    "build_strike_off_bar",
    "build_trough",
]

```

=== file: cad/dfm.py ===
```py
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

```
```

## Answer

The biggest result from this baseline review: the current design is already mostly gantry-only, but the safe baseline under your hard constraint is not the smooth cam alone. Panel E's captive peg-in-slot path is the stronger primary mechanism because it gives deterministic tilt and deterministic return using gantry motion alone. Panel D's smooth cam is still useful, but more as the simpler fallback when powder contamination of a routed slot becomes the dominant problem.

1. Places where the current design still leans on an implicit second actuator, and gantry-only substitutes

A. Return from dump to level in Panel D implicitly assumes gravity is "good enough"
- Current assumption: after the trough rides up the smooth cam, backing off in X lets gravity right the trough.
- Why this is an implicit actuator assumption: if the trough is nearly empty, lightly loaded, sticky with residue, or the pivot friction rises, there is no positive return force. The mechanism only has one-sided constraint during tilt-up.
- Gantry-only substitute: Panel E routed-slot follower. The slot wall supplies both tilt-up and tilt-down reactions, so the gantry's reverse X motion forces return to level.
- Alternative substitute: dual opposed cams, one for tilt-up and one for forced de-tilt, but that is less clean than a captive slot.

B. Cam engagement in Panel D assumes reliable contact registration without active follower preload
- Current assumption: the bumper will find and stay on the cam surface.
- Why this matters: the cam is a unilateral constraint. If contact is lost during approach, knock oscillation, or return, the tilt schedule is no longer deterministic.
- Gantry-only substitute: captive peg-in-slot board, as already proposed in Panel E.
- Alternative substitute: forked yoke follower or V-groove track with a dowel follower, still passive and gantry-driven.

C. Optional passive flap lid assumes timed opening without an actuator
- Current assumption in README: a projection on the flap hits a fixed tang on the cam assembly and opens during dump.
- This is gantry-only feasible, but the timing is implicit and underconstrained in the current baseline.
- Gantry-only substitute: a second passive cam/tang surface dedicated to the flap, or better, a second shallow slot path for a flap follower so lid timing is programmed by fixture geometry, not by incidental collision.

D. "Hold/don't leak" transport behavior from the PR bimodal-scoop suggestion implies a discrete state change not present in the baseline
- Current baseline has only one stable transport state: gravity-open-up.
- If you want a second stable non-leak state, that state change must come from an external fixture because you disallow a bucket actuator.
- Gantry-only substitutes:
  - fixed-post snap-through of a compliant bistable flexure
  - OT-2 tip-eject-style push feature that toggles a latch/flexure with X or Z motion against a fixed edge
  - slot-programmed partial inward tilt during transport, which may eliminate the need for a separate latch entirely
  - passive flap lid, which is simpler than a full bistable trough

E. Pipette-displacement-driven suction / "PowderPicking"-style aspiration would require a pressure source if interpreted literally
- I cannot recommend true suction-based pickup as a direct substitute for the trough without adding a new actuation or pneumatic subsystem, because the provided design context does not include a compliant sealed chamber or existing pipette plunger coupling on the bucket.
- A gantry-only reinterpretation is possible only if the gantry pushes the bucket against a fixed plunger or fixed pneumatic displacement feature, analogous to OT-2 tip eject. That would be a new mechanism, not a minor tweak to the current trough.
- For this project, that path looks overcomplicated relative to slot-driven tilt or a passive flap.

2. Panel D smooth cam ramp vs Panel E routed slot

Quantitative grounding from the embedded CAD defaults:
- Cam ramp length = 40 mm
- Cam rise = 20 mm
- Ramp angle = arctan(20/40) = 26.6°
- DFM check band in cad/dfm.py is 15-45°, so the default cam angle passes that criterion.
- Using the default geometry, bumper-to-pivot distance is about 24.1 mm, giving a nominal initial tilt sensitivity of about 1.19° per mm of gantry X at first contact.
- Default slot path spans X = 10 to 210 mm, so slot X span = 200 mm; this fits inside the default gantry_x_travel = 250 mm.
- Default slot Z span = 18 mm; this fits inside gantry_z_travel = 80 mm.
- The default slot path is monotonic in X, so it is compatible with gantry-only traversal under the current DFM logic.

Kinematic determinism
- Cam ramp: only deterministic while contact is maintained. It is a unilateral constraint.
- Slot: deterministic by construction because the peg is captive in the path.
- Winner: routed slot.

Bidirectional return
- Cam ramp: depends on gravity for return. The Edison review estimated restoring moment above 0.003 N·m for the pendulum geometry, which is enough in principle but still leaves return friction-sensitive and load-dependent.
- Slot: return is forced by reverse gantry motion, loaded or unloaded.
- Winner: routed slot.

Robustness to powder build-up
- Cam ramp: better. It is exposed and easier to wipe; loose powder is more likely to fall off an open inclined surface.
- Slot: worse. A recessed routed channel is a powder trap. Fine cohesive powder can pack into the slot and increase follower friction or jam the peg.
- Winner: cam ramp.

Additive-manufacturing complexity
- Cam ramp: geometrically simpler, but the current DFM logic flags the default underside overhang as 63.4°, above the 50° warning threshold in cad/dfm.py, so naive FDM orientation needs support or reorientation.
- Slot board: as a flat board, it is easier to print as a gross shape, but the slot itself needs tighter tolerance and smoother walls than FDM naturally gives. The manuscript is right that CNC routing in acrylic/HDPE/aluminum is the better fabrication route for the slot variant.
- Winner: if pure FDM only, slight edge to cam for simplicity of concept, but the default DFM warning narrows that gap. If simple subtractive machining is allowed, edge to slot.

My decision for iteration 1:
- Baseline mechanism: routed slot.
- Backup mechanism for dirty environments: smooth cam ramp.
- If you stay FDM-only for all fixtures, prototype both side-by-side because manufacturability may dominate the nominal kinematic advantage of the slot.

3. Critique of the bimodal scoop suggestion: can a passive bistable flexure work on a 3-axis gantry?

Short answer: yes, a passive bistable mechanism is possible on a 3-axis gantry. No, it does not inherently require a second actuator. But it does require a fixed external feature to toggle the state, and it is probably not the best baseline here.

Why it can work gantry-only
- A bistable flexure has two energy minima.
- The gantry can drive the scoop into a fixed post, ramp, or edge that supplies the snap-through force.
- That is mechanically the same logic as OT-2 tip-eject: a translational motion against a stationary feature changes mechanism state without any actuator on the end-effector.

Why it is not automatically the right answer here
- You already have a simpler way to create a "hold" state: use the slot path to command a transport-safe partial inward tilt.
- If leakage during transport is the real concern, a passive flap lid is simpler and easier to replace than a printed bistable trough structure.
- FDM bistable flexures are fatigue-limited. Their life depends strongly on print orientation, strain amplitude, and humidity; PETG and nylon are not magic here.
- A bistable scoop also makes the dump less continuously tunable. One nice feature of the cam/slot concepts is that dump angle can be a continuous function of gantry position.

Bottom line on the PR suggestion
- A single passive bistable flexure is achievable on a 3-axis gantry if toggled by fixed posts/ramps in the workspace.
- It does not always require a second axis.
- But for this project, I would treat it as a later variant, not the baseline. The slot plus optional passive flap gives most of the benefit with less fatigue risk and better tunability.

4. Three experimental measurements that will actually discriminate among cam-ramp, pin-slot, and bistable variants

A. Delivered-mass repeatability
- Metric: mass CV (%) across repeated scoops.
- Suggested protocol: at least 30 dispenses per powder per mechanism, preferably 50 if time allows.
- Powders: one free-flowing crystalline powder, one cohesive oxide like TiO2, one hygroscopic salt.
- Report: mean, SD, CV, and 95% CI for CV by bootstrap.
- Statistical analysis: compare variances with Brown-Forsythe/Levene-type tests; if comparing means too, use Welch ANOVA or Kruskal-Wallis depending on assumption checks.
- Why it discriminates: slot should reduce variance from engagement uncertainty; bistable may reduce transport loss but could add snap-through variability.

B. Dose-recovery fraction / retained mass after dump
- Metric: recovery = discharged mass / loaded mass, plus residual mass left in trough.
- Protocol: weigh trough before loading, after loading, after dump; compute loaded mass and residual mass directly.
- Add a knock/no-knock factor because the README explicitly proposes knock-to-de-bridge.
- Statistical analysis: two-factor model for mechanism × knock condition; if assumptions fail, use aligned-rank or permutation alternatives.
- Why it discriminates: slot should help reach and hold full dump angle; cam may underperform if contact is lost; bistable depends heavily on its dump-state geometry.

C. Bridging / flow-stoppage frequency during dump
- Metric: proportion of dumps with no stoppage, transient stoppage, or major stoppage requiring intervention.
- Protocol: video-score each dump, or instrument with simple timing and post-dump residual mass threshold.
- Powders: include a deliberately ugly cohesive case such as fumed silica or similarly problematic fine powder, because the whole point is to stress the mechanism.
- Statistical analysis: contingency-table analysis with chi-square or Fisher's exact test; optionally model with ordinal logistic regression if enough runs are available.
- Why it discriminates: the slot should make programmed knock motion more repeatable than the cam; a bistable snap may provide one strong impulse but no sustained oscillatory de-bridging.

Those three are the right first set because they map to the three practical questions: how repeatable is the scoop, how completely does it empty, and how often does the powder misbehave.

5. Recommended open, pip-installable feedback-loop toolchain

Best practical stack for this repo:
- CadQuery for parametric geometry generation
- existing cad/dfm.py as a hard feasibility gate
- pyserial for direct serial control of gantry and balance where needed
- duet or direct G-code for Jubilee-class Duet-controlled motion systems
- opentrons Python API if you test on OT-2
- NumPy/SciPy/pandas for measurement handling
- scikit-optimize or Ax for closed-loop parameter search
- optional OpenCV for simple vision checks on printed geometry or powder-bed state

Concrete recommendation
- Geometry and constraints: cadquery
- Motion control on Jubilee: pyserial plus Duet HTTP/serial interface
- Motion control on OT-2: opentrons
- Data analysis/optimization: numpy, scipy, pandas, scikit-optimize
- Print orchestration if desired: OctoPrint client

A sane loop is:
1. edit ExcavatorParams
2. run cad.dfm and reject infeasible parameter sets automatically
3. export STL/STEP
4. print fixture/part
5. run scripted scoop experiment on Jubilee or OT-2
6. collect mass/recovery/bridging metrics
7. feed scores into Bayesian optimization or simple grid search
8. update parameters and repeat

What I would do next, concretely
- Prototype Panel E first, but orient the slot so gravity helps clear it, not fill it.
- Keep Panel D in parallel as the contamination-tolerant control.
- Do not make bistability the first branch. First test whether a slot-programmed transport-safe angle or a passive flap already solves leakage.
- Add one new DFM rule: flag recessed slot geometries whose opening orientation makes powder accumulation likely. Right now cad/dfm.py checks travel and bounds, not fouling risk.

Limitations
- I cannot verify the exact text of PR comment 3134394694 because only its paraphrase is present in the embedded context, not the full comment body.
- I did not fabricate any performance data. The numeric comparisons above are kinematic/geometry-derived from the embedded CAD defaults and from the archived Edison review text.
- I did not validate external package APIs live; the package recommendations are based on the open Python toolchains described in the repo context and widely used control/optimization stacks.

Decision: for the gantry-only baseline, make the routed-slot mechanism the lead design, retain the smooth cam as the contamination-tolerant backup, and defer the bistable scoop to a later branch unless transport leakage proves severe enough that slot-programmed hold or a passive flap cannot solve it.

- Used the embedded default CAD parameters (cam_ramp_length 40 mm, cam_ramp_rise 20 mm, slot path 10→210 mm in X, 30→12 mm in Z) as the quantitative basis for kinematic comparisons.
- Treated the routed-slot variant as a bilateral kinematic constraint and the smooth cam as a unilateral contact constraint for the determinism comparison.
- Used the Edison archived restoring-moment estimate (>0.003 N·m) qualitatively for gravity-return critique rather than inventing new dynamic simulations.
- Assumed alpha = 0.05 for proposed discrimination experiments and suggested bootstrap CIs for CV because CV sampling distributions are often non-normal.
- Recommended Brown-Forsythe/Levene-type variance tests, Welch/Kruskal-Wallis mean tests, and chi-square/Fisher tests depending on assumption checks.
- Recommended the pin-slot as the iteration-1 baseline despite its fouling risk because kinematic determinism and forced return are more central to the no-second-actuator requirement.
- Recommended CNC-routed slot fixtures over FDM slot fixtures when possible because the manuscript itself notes FDM layer-line jitter in the slot.
- Treated the bistable concept as feasible only when toggled by fixed external posts/ramps, not as a free self-toggling feature.
