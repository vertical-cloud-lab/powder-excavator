# Powder-Excavator — design brainstorming &amp; prior-art notes

This document captures a literature-aware brainstorm for the gantry-mounted
"powder excavator" sketched in `powder-excavator-sketch.jpg` and recreated as
the four labelled subpanels under [`docs/figures/`](figures/). It is
structured roughly like the introduction to a *Digital Discovery* manuscript
on a new powder-handling tool: where does this device sit in the landscape
of automated powder dispensing, what gap is it trying to fill, and what
would we need to measure to defend that claim.

> **Provenance note.** This brainstorm was prompted by feedback on PR #2 to
> "send the idea to Edison for high-effort literature search" and to consider
> the discussion at
> <https://accelerated-discovery.org/t/accurate-powder-dispensing-for-chemistry-and-materials-science-applications/177>.
> The Edison Scientific service was wired in via `edison_client` for the
> follow-up session: a high-effort PaperQA3 literature search and two
> high-effort design-review tasks were run, and their verbatim responses
> are archived under [`docs/edison/`](edison/). The community-thread-
> specific contributions from the linked accelerated-discovery thread
> are summarised in §2.5 below and credited inline; the peer-reviewed
> citations marked with `[ETC]`, `[Tom24]`, `[Yang07]`, `[Bahr18]`,
> `[Bahr20]`, `[Jiang23]`, `[Szym23]`, `[Lunt23]`, `[Lunt24]`,
> `[Carr25]`, `[Fei24]`, `[Cook20]`, `[Alsenz11]`, `[HdV24]`, `[Doloi25]`,
> `[Mor20]`, `[Free17]` are taken directly from the Edison literature
> task and are listed in §6.

> **Geometry note (post-review).** The mechanism description in §3 and §5
> below has been updated to the **longitudinal-pivot / sideways-tilt /
> smooth-cam-ramp** geometry adopted after the Edison design-review tasks
> identified two design-blocking issues with the earlier "ferris-wheel
> gondola" (transverse pivot, end-over-end tilt, sawtooth + hooked-lip)
> revision: a kinematic impossibility in the push-to-tilt mechanism and a
> trapped-volume / bridging problem for cohesive powders. Details and the
> raw review text live in [`docs/edison/`](edison/).

---

## 1. Why powder handling is the pinch point in self-driving labs

Self-driving laboratories (SDLs) for chemistry and materials science have
matured rapidly over the past five years, with closed-loop platforms now
routinely combining robotic execution, automated characterization, and
Bayesian / generative experiment design [1–4, Tom24]. Across nearly
every published SDL, **solids handling — and powder dispensing in
particular — is repeatedly called out as the dominant bottleneck**: it
is the step most likely to be left to a human, the one most sensitive to
material properties (cohesion, hygroscopicity, triboelectric charging),
and the one that most often limits end-to-end autonomy [1, 4, 5, Tom24,
Yang07]. Tom et al.'s 2024 *Chemical Reviews* survey of SDLs makes the
point bluntly: solid-dispensing hardware "remains rare and costly
relative to liquid handling, and many labs simply avoid direct powder
manipulation" wherever pre-dissolved stocks will do [Tom24].

Compared with liquid handling, powder dispensing is hard for three coupled
reasons:

1. **No universal flow regime.** Free-flowing crystalline powders, fluffy
   nanopowders, sticky organics, and hygroscopic salts each demand different
   feeders, hoppers, and tip geometries [5, 6, Yang07].
2. **Dose accuracy scales poorly down.** Sub-milligram gravimetric dosing
   needs a draft-shielded balance, vibration isolation, and feedback control;
   the 17,797-dispense ETC benchmark across four commercial platforms found
   that 2 mg targets exhibited 190–680 % higher %RSD than 50 mg targets, and
   that across the full dataset the % error spanned −10 % to +3,245 %
   (95.3 % of dispenses fell between −25 % and +100 %) [7, Bahr18, Bahr20].
3. **Cross-contamination is expensive.** Reservoirs and end-effectors must
   either be disposable, easily cleaned, or dedicated per material, which
   blows up the part count of a multi-reagent platform [5, Carr25].

## 2. Prior art (representative, not exhaustive)

| Class | Example systems | Typical accuracy / scale | Strengths | Limits relevant to us |
|---|---|---|---|---|
| **Gravimetric, vibratory-head dispensers** | Mettler-Toledo Quantos QX1/QX5, Chemspeed SWING / Powdernium / FLEX GDU-Pfd, Unchained Labs Freeslate/Junior | ETC benchmark: 2–50 mg, 17,797 dispenses, %RSD strongly mass-dependent; Quantos best overall % error/%RSD/time balance; Chemspeed SWING fastest (13–65 s) [Bahr18, Bahr20] | High precision on dense free-flowing powders; closed-loop weight feedback; integrated workflow software | Per-reagent consumable cartridges/heads; abrasive solids damage Quantos heads; hygroscopic / deliquescent powders clog them; Chemspeed SWING and one Unchained system **failed outright** on fumed silica [Bahr18, Carr25] |
| **Auger / screw feeders on robot arms** | Custom rigs in Berlinguette &amp; MacLeod's "Ada" thin-film SDL [3], Aspuru-Guzik group platforms; Chemspeed FLEX GDU-Pfd hopper/auger module [Bahr20] | mg–g, application-dependent; GDU-Pfd ±10 % tolerance setting | Robust to mildly cohesive powders; metered dosing | Mechanical complexity; cleaning between materials non-trivial; the Lunt et al. modular-workflow paper notes "grinding, mixing and recovering solids remains an unsolved challenge in commercial automation" [Lunt23, Lunt24] |
| **Spatula-mimicking dual-arm robots** | Cooper group's PowderBot (Liverpool) [Jiang23] | 20 mg–1 g; ~0.07 % error at 200 mg for non-challenging solids; Al₂O₃ at 1000 mg = −0.02 ± 0.05 % | Versatile across material classes; comparable failure rate to commercial systems (23.1 % vs. 26.9 % vs. 26.5 %) at lower hardware cost | Slow throughput due to manipulator motions and corrective restarts; struggles with compressible powders (CaCO₃) and highly hygroscopic materials [Jiang23] |
| **Slurry-conversion workflows** | Ceder group A-Lab (Berkeley) — Quantos doses precursors into vials, ball-milled with ethanol into pumpable slurry [Szym23, Fei24] | 50–100 g precursor bottles; 36 novel compounds in 17 days; target throughput 100–200 samples/day | Sidesteps last-mile dry-transfer issues; well-characterised end-to-end workflow | Adds ethanol handling, drying, and a dedicated `RecoverPowder` regrinding task downstream; upstream powder loading is still manual [Szym23, Fei24] |
| **Capsule / cartridge "drop a pre-weighed slug"** | Pre-weighed vials/sachets fed by pick-and-place arms | Limited by pre-weighing step | Eliminates real-time dosing error | Needs upstream weighing; brittle to inventory mistakes; Quantos cartridge ecosystem in particular criticised for high cost, single-vendor procurement, RFID-locked reuse, and clogging on hygroscopic powders [Carr25] |
| **Acoustic / ultrasonic non-contact transfer** | Echo-style platforms adapted for solid dispersions; ultrasonic capillaries (~14–16 µg through 0.2 mm nozzles) [Yang07] | µg–low mg, narrow material window | Non-contact, no cross-contamination, very high throughput | Currently limited to specific particle sizes / suspensions; mostly demonstrated in solid-freeforming/AM contexts, not chemistry SDLs [Yang07] |
| **Vacuum / electrostatic pickup** | DryPette (vacuum, 2–700 mg, SD <5 % above 50 mg), Electronic Spatula (charged tip, down to 0.2 mg), automated electrostatic pipettes [Alsenz11, Yang07] | ~mg | Gentle on the powder; good for fragile crystals; 0.3 mg-class doses possible | Hard to release a clean dose; **exquisitely** sensitive to humidity, charge decay, and powder conductivity [Yang07] |
| **Positive-displacement "PowderPicking"** | Standard Gilson MICROMAN pipettes with disposable capillary-piston tips (Alsenz) [Alsenz11, Cook20] | 0.6–25 mg; mean CV ≈ 6 % across 10 powders; worst-case ≈ 10 % | Cheap (standard pipettes + disposable tips); handles electrostatic / sticky powders; disposable tips eliminate carryover | Manual / medium throughput; depends on complete homogeneous filling of the probe cylinder; tip clogging with adhesive powders, particle dropout with coarse granules [Alsenz11] |
| **Bulk "scoop and dump" mechanical scoops** | This project (`powder-excavator`) and various lab-built rigs; closest commercial analogue is the MTI PF-A glass dispenser referenced in the community thread | 0.1–10 g (estimated, to be measured) | Cheap, mechanically simple, no actuators on the end-effector, easy to clean; the present design has **no consumable** at all | Not a precision dosing tool; dose CV likely 5–20 % depending on whether a strike-off bar is used; not for sub-mg work |

Two recent overviews are particularly relevant for situating a new device
in this landscape: Tom et al.'s 2024 *Chemical Reviews* survey of SDL
hardware [Tom24] and the *ChemRxiv* / Digital Synthesis &amp; Catalysis
Lab review of SDL hardware for chemistry and materials [4]. Both flag
*bulk powder transfer from stock containers into a precision dispenser*
as a step that is still almost universally manual, and the Lunt et al.
modular-workflow paper makes the same point about post-processing
recovery [Lunt23, Lunt24]. On the frugal-hardware side, recent
open-hardware platforms have demonstrated cost reductions of up to 94 %
relative to commercial analogues for adjacent dispensing problems
(pellet dispensers, 3D-printed autosamplers) [HdV24, Doloi25], albeit
for liquid or pellet handling rather than fine inorganic powders.

### 2.5 Community prior art from the Accelerated Discovery thread

The
[Accelerated Discovery thread "Accurate powder dispensing for chemistry
and materials science applications"](https://accelerated-discovery.org/t/accurate-powder-dispensing-for-chemistry-and-materials-science-applications/177)
[8] is a useful, opinionated cross-section of what practitioners have
actually tried. The points most relevant to our design:

- **Framing (sgbaird, post 1).** Accurate powder dispensing is "around an
  order of magnitude more complex and more expensive than liquid handling."
  This matches the SDL reviews [1, 4] and is the gap we are trying to chip
  away at on the cheap, mechanical end of the design space.
- **3D-printed calibrated spatulas (post 2, after Cook et al. 2020 [9]).**
  Sets of spatulas with known volumes give a calibration curve from volume
  → mass; decent accuracy in isolation, but degraded by static in
  gloveboxes and by lighter powders. Two takeaways for us: (i) **a
  strike-off bar is essentially required** ("just manually tapped the
  spatula until each scoop is level… it doesn't seem too difficult to
  physically level it by passing something against the top of the scoop")
  — directly endorses the strike-off bar variant in §5; (ii) per-material
  calibration is realistic if the trough is geometrically well-defined.
- **Positive-displacement-pipette method (post 3, Alsenz [10]).** Packs a
  pipette tip into the powder; spans ~0.6–20 mg with ~10 % CV across tip
  sizes. The 10 % CV is a **useful baseline target** for our scoop on
  cohesive powders.
- **Auger / screw-feed builds (loppe35 post 4; later post with stepper +
  3D-printed adapter).** Cheap (jewelry-scale load cell ≈ USD 25, stepper
  + control board), but "leaky when dispensing vertically" and needs hopper
  flow aids. Reinforces our decision to keep the excavator's bucket
  *un-augered* in the baseline design — the auger is positioned in §5 as
  an optional add-on, not the core mechanism.
- **The "pick it back up" problem (muon, posts 5/7/14).** Dispensing is
  only half the workflow; recovering powder *after* an operation
  (ball-milling, acoustic mixing, weighing) is at least as hard, and a
  vacuum/pipette approach is awkward when the milled powder is fine and
  multi-precursor cross-contamination matters. The excavator's open-top
  ladle is in principle a recovery tool too — worth calling out as an
  underexplored capability.
- **Autotrickler v4 + A&D FX-120i (sgbaird, post 6).** ±1 mg, fast-response
  scale, BLE-controllable from a Pico W; community-validated reference for
  the "scale + metered feed" downstream of a bulk-transfer device.
  Suggests a concrete integration target: excavator → tared
  Autotrickler-style trickler/scale.
- **PowderBot (Cooper group, [11]) and ALab (Ceder group, [12]).** Two
  published end-to-end SDLs that *did* solve solids handling, but with
  workflow-specific workarounds (typically involving milling). Useful
  honest comparators; the excavator is aimed at being more general at the
  cost of precision.
- **Powder-bed AM cross-pollination (kthchow, post 16).** Insstek's
  "clogged vibration mechanism" / blow-disk approach from directed-energy-
  deposition AM, and the pharmaceutical SDL community at CMAC, both have
  mature solutions for sticky / triboelectrically charged powders that
  could be borrowed wholesale rather than re-invented.
- **Low-cost dispensing platforms (mreish video, post 15; Tourlomousis
  ~USD 100 dispenser for biopolymers, post 18).** Demonstrate a market for
  the same "good-enough, cheap, hackable" niche the excavator targets.
- **Ceramics-robot survey (Maruyama, post 19).** Explicitly enumerates the
  commercial vendor list a real lab is currently choosing among
  (Trajan/Mettler-Toledo, Chemspeed, Unchained Labs, Hamilton,
  ThermoFisher), confirming the prior-art rows in §2.
- **Manual MTI PF-A glass dispenser (sgbaird, post 24 — the specific post
  linked in the review feedback [13]).** A 250 mL hand dispenser whose
  geometry is reminiscent of Owen Melville's earlier scoop. Worth
  inspecting the video for the exact lip / tilt geometry it uses; that is
  effectively a manual ancestor of the excavator's scoop motion and is the
  closest existing artifact to our bucket.

The thread is also a *de facto* community wishlist: cheap, integrable with
an existing gantry/robot, tolerant of cohesive and statically-charged
powders, ideally bidirectional (dispense *and* recover). The excavator
hits the first three at the cost of precision; the fourth is a free
side-benefit worth claiming in a writeup.

## 3. Where the powder-excavator fits

The proposed mini excavator is **not** competing with Quantos-class precision
dispensers. It is aimed at the **upstream, bulk-transfer step**: moving a
relatively coarse aliquot of powder from a stock bed (e.g., a tray, jar, or
hopper) to a downstream station — which might itself be a precision
dispenser, a sieve, a press, a crucible, a dissolution vial, or simply a
weigh boat for a human-in-the-loop workflow. In that niche, the design
choices in `powder-excavator-sketch.jpg` (as updated post-review) make
sense:

- **Half-cylinder ladle suspended on a longitudinal pivot pin.** The pin
  runs along the trough's long axis L, through the two short end caps,
  with the two arms gripping those end caps. The trough rolls
  **sideways** about the pin to pour, dispensing over the **full long
  edge** rather than through a narrow end-cap point. This eliminates
  the trapped-volume / arching failure mode that an end-over-end tilt of
  a half-cylinder would have for cohesive powders (Edison v2 §3, archived
  in [`docs/edison/`](edison/)).
- **Pure mechanical actuation via a fixed smooth inclined cam ramp.**
  Removes the servo and its wiring/maintenance burden; the deposit
  angle is set by how far up the cam the trough's chamfered bumper has
  ridden (i.e. by gantry X position), not by a torque setpoint. A
  smooth ramp — rather than a sawtooth tooth — is required because a
  fixed point engaging a fixed-radius hook on a horizontally-translating
  pivot is geometrically impossible (Edison v2 §1). The cam is the same
  philosophy as a passive cam in classic mechanical assembly lines.
- **Mandatory bed-edge strike-off bar.** Promoted from "optional
  variation" to a baseline-required part: without a level-defining
  strike-off, dose CV will sit in the 15–30 % range across powder
  classes, which would put the device below the ≈10 % CV baseline
  achievable with Alsenz's positive-displacement-pipette method
  [Alsenz11] and below the Cooper PowderBot's 0.07 % at 200 mg [Jiang23].
- **Open top with no lid.** Trades some retention loss for radically
  simpler cleaning — which, per [Tom24, Carr25], is the single biggest
  hidden cost in multi-material SDLs.
- **Optional grounded conductive lining.** Because the pivot pin is a
  metal dowel, it can double as the ground path for an inexpensive
  copper-tape lining of the trough interior. This is the prototype-
  friendly equivalent of using ESD-safe filament and dramatically
  reduces triboelectric charging on fine inorganics (Edison v1 §2).

A reasonable framing for a write-up would be: *"A purely mechanical,
gantry-mounted ladle for bulk powder transfer in self-driving materials
labs, designed to bridge stock containers and precision dispensers
without adding servo count or cleaning burden, and to take over the
upstream-loading and post-process recovery roles flagged as unsolved by
Lunt et al. [Lunt23, Lunt24]."*

The design intentionally makes **no claim** of being a precision
dispenser, and tempers the "bidirectional dispense + recover" claim
made in earlier framing: a half-cylinder cannot scoop cleanly out of a
flat bed without leaving a trail of retained powder, so recovery is a
meaningful but lossy operation rather than a complete one (Edison v2 §7).

## 4. Open questions and what we'd actually need to measure

To defend the design in a manuscript-style argument we would need at minimum:

- **Dose statistics across powder classes.** Mean &amp; CV of delivered mass
  for ≥3 archetypal powders (e.g., free-flowing crystalline like NaCl,
  cohesive metal-oxide nanopowder like TiO₂, hygroscopic salt like LiCl)
  across ≥30 scoops each. Following Cooper-group practice [Jiang23], this
  should also include known "hard" cases — fumed silica (which broke the
  Chemspeed SWING and one Unchained system in the ETC benchmark [Bahr18])
  and CaCO₃ (which broke the PowderBot [Jiang23]).
- **Standardised flowability descriptors per powder.** Report Carr's
  compressibility index (CI ≤ 10 % = excellent; 21–25 % = passable;
  >35 % = very poor) and the Hausner ratio (HR 1.00–1.11 = excellent;
  1.26–1.34 = passable; >1.45 = poor) for every test powder, plus
  Freeman FT4 basic flow energy (BFE) and specific energy (SE) where
  available [Mor20, Free17]. These are cheap, published, comparable
  across studies, and currently absent from most powder-dispenser
  evaluations.
- **Carryover / cross-contamination.** Mass remaining in the trough after a
  "tip and pour" event, vs. after a programmed cleaning cycle (knock-
  oscillation against the cam, inverted shake, brush, or air blast).
  Carryover should be reported as a fraction of the nominal dose and
  stratified by powder class, following the approach Carruthers used to
  expose Quantos-cartridge limitations [Carr25].
- **Sensitivity to bed depletion.** How much does the dose change as
  the powder bed depletes / gets cratered? Run 30 consecutive scoops
  from the same X, Y location and plot dispensed mass vs. scoop number
  (Edison v1 §3). The expected steep decay curve will set the
  requirement that the gantry must raster across the bed.
- **Coupling to a downstream balance.** Demonstrate that the
  excavator → balance → vibratory-head pipeline reduces total wall-clock
  time per dispensed dose vs. a one-stage precision dispenser doing both
  bulk and fine work — i.e. directly attack the upstream-loading
  bottleneck flagged by [Tom24, Lunt23, Lunt24, Carr25].
- **Mandatory benchmark experiments (Edison v2 §6).**
  1. **Cam-engagement test.** 3D print the trough, the chamfered bumper,
     and the inclined cam track. Drive the gantry purely in X and verify
     the bumper rides up the cam without binding, skipping, or requiring
     coordinated Z motion — i.e. that the kinematic problem of the old
     sawtooth design has been resolved.
  2. **Trapped-volume bake-off** (sanity-check on the geometry change).
     Compare retained mass of a cohesive test powder (TiO₂ or flour) for
     a sideways tilt vs. a hypothetical end-over-end tilt of the same
     trough. The expected ~7–26 % retention penalty of the end-over-end
     case (Edison v2 §3) is the empirical justification for the
     longitudinal-pivot geometry.
  3. **Strike-off efficacy.** Measure the dose mass of 30 consecutive
     scoops with and without the bed-edge strike-off bar. The expected
     2–3× CV improvement is the empirical justification for keeping the
     strike-off bar in the baseline.
- **Cam-ramp / strike-off / bumper geometry sweep.** Cam slope, ramp
  length, strike-off cross-section, and rim-bumper chamfer angle are
  the four knobs most likely to dominate dose CV; small parameter
  sweeps are cheap with 3D-printed parts.

## 5. Design variations worth prototyping (still pure-mechanical)

Carrying over from the README brainstorming, with the literature in mind:

- **Dual cam ramps, left and right** — for two-output workflows (e.g.,
  one for "real" deposit, one for "purge/waste" to clear residual
  material between materials).
- **Strike-off bar variants** — a square cross-section vs. a chamfered
  blade vs. a thin compliant flap, scored for fill repeatability and
  for how cleanly the bar sweeps the rim of cohesive powders without
  flicking material away.
- **Twin troughs back-to-back** — fill one while dumping the other for
  doubled throughput at the cost of one extra carriage stop.
- **Replaceable, snap-in trough liners** — a thin, single-material liner
  (e.g. ESD-safe filament or copper-tape-lined PETG) that snaps into the
  printed trough body. Lets us treat the trough as consumable per-
  material and bypass the cleaning problem entirely; this is the
  prototype-friendly analogue of Quantos cartridges [Carr25] without
  the RFID lock-in.
- **Spring-loaded passive flap lid actuated by the same cam** — closes
  during transport (curing the fine-powder retention problem) and
  opens at the same instant the bumper engages the cam, with no extra
  actuator.
- **Internal auger as an *option*** — adds one rotary actuator but
  converts the device from "tilt and pour all" to a coarse metered
  dispenser, which would squarely overlap with mid-range commercial
  systems [Bahr20].

## 6. References

Citations marked `[abbrev]` in the body above are the verbatim Edison
PaperQA3 results from `docs/edison/literature-high-powder-dispensing.md`,
restated here as a numbered bibliography. The original numeric citations
[1]–[13] from the previous revision are retained at the end for
backward compatibility with earlier discussion threads.

- **[Tom24]** G. Tom *et al.*, *Self-driving laboratories for chemistry and
  materials science.* Chemical Reviews 124, 9633–9732 (Aug 2024).
  <https://doi.org/10.1021/acs.chemrev.4c00055>
- **[Yang07]** S. Yang and J. Evans, *Metering and dispensing of powder; the
  quest for new solid freeforming techniques.* Powder Technology 178, 56–72
  (Sep 2007). <https://doi.org/10.1016/j.powtec.2007.04.004>
- **[Bahr18]** M. N. Bahr *et al.*, *Collaborative evaluation of commercially
  available automated powder dispensing platforms for high-throughput
  experimentation in pharmaceutical applications.* Organic Process Research
  &amp; Development 22, 1500–1508 (Oct 2018).
  <https://doi.org/10.1021/acs.oprd.8b00259>
  (the "ETC benchmark"; 17,797 dispenses, four platforms, seven powders.)
- **[Bahr20]** M. N. Bahr *et al.*, *Recent advances in high-throughput
  automated powder dispensing platforms for pharmaceutical applications.*
  Organic Process Research &amp; Development 24, 2752–2761 (Oct 2020).
  <https://doi.org/10.1021/acs.oprd.0c00411>
- **[Jiang23]** Y. Jiang *et al.* (Cooper group), *Autonomous biomimetic solid
  dispensing using a dual-arm robotic manipulator* ("PowderBot"). Digital
  Discovery 2, 1733–1744 (2023). <https://doi.org/10.1039/d3dd00075c>
- **[Szym23]** N. J. Szymanski *et al.* (Ceder group), *An autonomous
  laboratory for the accelerated synthesis of inorganic materials* ("A-Lab").
  Nature 624, 86–91 (Nov 2023). <https://doi.org/10.1038/s41586-023-06734-w>
- **[Fei24]** Y. Fei *et al.*, *AlabOS: a Python-based reconfigurable
  workflow management framework for autonomous laboratories.* arXiv:2405.13930
  (May 2024). <https://doi.org/10.48550/arxiv.2405.13930>
- **[Lunt23]** A. M. Lunt *et al.*, *Modular, multi-robot integration of
  laboratories: an autonomous solid-state workflow for powder X-ray
  diffraction.* arXiv:2309.00544 (Jan 2023).
  <https://doi.org/10.48550/arxiv.2309.00544>
- **[Lunt24]** A. M. Lunt *et al.*, *A robotic workflow for the discovery
  and recovery of solids in autonomous chemistry.* (cited via Edison; see
  `docs/edison/literature-high-powder-dispensing.md` for full bibliographic
  metadata.)
- **[Carr25]** S. Carruthers, *A mobile robotic researcher for autonomous
  solar fuels research.* Doctoral thesis, 2025. (Cited via Edison; documents
  practical Quantos cartridge frustrations — high cost, single-vendor
  procurement, embedded ID chips limiting reuse, hygroscopic clogging,
  fragile internals.)
- **[Alsenz11]** J. Alsenz, *PowderPicking — an inexpensive method for
  powder dispensing using positive-displacement pipettes.* Powder
  Technology, 2011.
  <https://www.sciencedirect.com/science/article/abs/pii/S0032591011000696>
  (≈6 % mean CV across 10 powders for 0.6–25 mg doses.)
- **[Cook20]** C. J. Cook *et al.*, *A guide to the inert-atmosphere
  processing of sol–gel reactions.* Nature Protocols 16, 365–388 (2021)
  — solid dispensing into 8×30 mm vials with calibrated spatulas.
  <https://www.nature.com/articles/s41596-020-00452-7>
- **[HdV24]** J. Hernandez del Valle *et al.*, *Pellet
  dispensomixer-and-…* (frugal open-hardware pellet dispenser; up to 94 %
  cost reduction relative to commercial analogues). Cited via Edison; full
  bibliographic metadata in `docs/edison/literature-high-powder-dispensing.md`.
- **[Doloi25]** Doloi *et al.*, *Democratizing self-driving labs.* (Cited via
  Edison; argues for low-cost / open-hardware SDL components.)
- **[Mor20]** S. K. Moravkar *et al.*, *Traditional and advanced flow
  characterisation methods for pharmaceutical powders* (Carr index,
  Hausner ratio, FT4). Cited via Edison.
- **[Free17]** T. Freeman, *Characterising powder flow.* Cited via Edison;
  Freeman Technology overview at <https://www.freemantech.co.uk/about-powder-flow>.
- **[McC23]** E. McCalla, *Semi-automated experiments to accelerate the
  design of advanced battery materials.* ACS Engineering Au 3, 391–402
  (Nov 2023). <https://doi.org/10.1021/acsengineeringau.3c00037>

The community-thread URL credited inline in §2.5 is also retained:
8. Accelerated Discovery community thread, *Accurate powder dispensing for
   chemistry and materials science applications.*
   <https://accelerated-discovery.org/t/accurate-powder-dispensing-for-chemistry-and-materials-science-applications/177>

The earlier numeric references [1]–[7], [13] from the original brainstorm
remain useful as in-thread reading list:

1. *Toward self-driving laboratory 2.0 for chemistry and materials discovery.*
   Materials Horizons, 2026.
   <https://pubs.rsc.org/en/content/articlehtml/2026/mh/d5mh01984b>
2. *Science acceleration and accessibility with self-driving labs.* Nature
   Communications, 2025.
   <https://www.nature.com/articles/s41467-025-59231-1>
3. *Autonomous "self-driving" laboratories: a review of technology and policy
   implications.* Royal Society Open Science, 2025.
   <https://royalsocietypublishing.org/rsos/article/12/7/250646>
4. *Self-Driving Laboratories for Chemistry and Materials Science.* ChemRxiv
   preprint, 2024.
   <https://chemrxiv.org/doi/pdf/10.26434/chemrxiv-2024-rj946>
5. T. Freeman, *Measuring Powder Flowability: Challenges and Solutions.*
   Powder Technology, 2017. See also Freeman Technology's overview at
   <https://www.freemantech.co.uk/about-powder-flow>.
6. *Performance metrics to unleash the power of self-driving labs in
   chemistry and materials science.* (PMC10866889)
   <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10866889/>
7. Mettler-Toledo Quantos automated powder dispensing — vendor
   specifications: lower limit ≈ 0.1 mg dose, repeatability on the order of
   ±0.01–0.02 mg for ≤10 mg doses on the QX-series.
8. Accelerated Discovery community thread, *Accurate powder dispensing for
   chemistry and materials science applications.*
   <https://accelerated-discovery.org/t/accurate-powder-dispensing-for-chemistry-and-materials-science-applications/177>
   Posts referenced individually in §2.5.
9. C. J. Cook *et al.*, *A guide to the inert-atmosphere processing of
   sol–gel reactions.* Nature Protocols 16, 365–388 (2021) — solid
   dispensing into 8×30 mm vials with calibrated spatulas.
   <https://www.nature.com/articles/s41596-020-00452-7>
10. J. Alsenz, *Powder dispensing using positive-displacement pipettes for
    small-scale solubility/formulation work.* Powder Technology, 2011.
    <https://www.sciencedirect.com/science/article/abs/pii/S0032591011000696>
11. *PowderBot: An automated robotic platform for handling solids* (Cooper
    group), arXiv:2309.00544.
    <https://arxiv.org/abs/2309.00544>
12. N. J. Szymanski *et al.*, *An autonomous laboratory for the accelerated
    synthesis of novel materials* ("A-Lab", Ceder group). Nature 624,
    86–91 (2023).
    <https://www.nature.com/articles/s41586-023-06734-w>
13. MTI Corporation, *Manual dispenser of 250 mL made of glass for solid
    powder, model PF-A* — referenced in the Accelerated Discovery thread,
    post 24 (the specific URL called out in the review feedback).
    Demo video: <https://www.youtube.com/watch?v=Ur7GZV2PaPQ>

