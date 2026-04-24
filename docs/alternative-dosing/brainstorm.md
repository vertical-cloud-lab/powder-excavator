# Alternative powder-dosing styles for the Genmitsu 3018-Pro V2

Issue [#12](https://github.com/vertical-cloud-lab/powder-excavator/issues/12)
asks us to think beyond the two designs already on the table — the
pivoting scoop / ladle in PR
[#2](https://github.com/vertical-cloud-lab/powder-excavator/pull/2) and the
bimodal compliant trough in PR
[#5](https://github.com/vertical-cloud-lab/powder-excavator/pull/5) — and
to propose alternative dosing styles that:

- bolt onto the **Genmitsu 3018-Pro V2** spindle/gantry mount,
- are realistically buildable in **one workshop day** (3D printing fine,
  electronics/motors are allowed but each added active component is a
  schedule risk),
- and address the gaps surfaced by the commercial-landscape sweep in
  PR [#11](https://github.com/vertical-cloud-lab/powder-excavator/pull/11)
  — chiefly the **sub-10 mg cohesive-powder dispensing gap**, the absence
  of an *open* powder head, and the dominance of gravimetric Quantos /
  positive-displacement SWILE as the only well-evidenced sub-mg paths.

The approach we take throughout: **let the gantry itself be the actuator**
wherever possible (the 3018 already has fast, repeatable XYZ motion under
GRBL control, so any dosing primitive that can be triggered by a
contact / press / tap / scrape against a fixed feature on the bed is
essentially "free" from a build-risk perspective).

## Design constraints recap

| Constraint | Source | Implication for alternatives |
| --- | --- | --- |
| Must mount on Genmitsu 3018-Pro V2 spindle clamp | issue #12 | Tool envelope ≤ ~Ø45 mm clamp, ≤ ~3 kg, ≤ ~300 × 180 × 45 mm work area |
| One workshop day left | issue #12 | Prefer purely-mechanical or single-discrete-component electronic designs |
| 3D printing OK; electronics/motors OK but risky | issue #12 | Rank passive > single-component-active > full electromechanical |
| Sub-10 mg, cohesive powder is unsolved at the open-source level | PR #11 §5 / §6 | Aim for designs that *attack* this regime, not that copy the > 50 mg gravimetric heads |
| Gravity / hopper feeds clog on cohesive powders | PR #11 §1, §4 | Prefer designs where powder is **mechanically liberated each cycle** (tap, scrape, displace) rather than relying on gravity flow |
| Avoid duplicating the scoop (#2) and bistable trough (#5) | issue #12 | Concepts below explicitly do not pivot a bucket and do not rely on a snap-through flexure |

## Candidate alternatives

The list below is ordered by **risk-adjusted feasibility for a one-day
build**: passive / fully gantry-driven first, then designs that need a
single small active component, then ones that meaningfully add
electromechanical complexity.

### A. Tap-driven sieve cup (passive, gantry-as-actuator) ⭐

A printed cup (~10–20 mL) with a calibrated **mesh** or laser-precise
slot pattern in its base is mounted to the spindle clamp. The cup is
pre-loaded with powder. Cohesive powders **do not flow through the mesh
under gravity**, but each tap shakes some loose. The 3018 dispenses by
descending until the cup strikes a fixed printed anvil on the bed at a
controlled feedrate; one G-code "peck" = one tap = a near-constant micro-
dose. Total dose is metered by **tap count** (open-loop) or by an
external balance underneath (closed-loop), as recommended in
[issue #3](https://github.com/vertical-cloud-lab/powder-excavator/issues/3).

- *Mechanism in the PR #11 taxonomy*: vibratory / sieve micro-feeder,
  but **driven by gantry-impulse instead of a piezo or ERM motor** —
  removes the only active component a SWILE-class sieve dispenser would
  normally need.
- *Why it's interesting*: directly attacks the cohesive-powder regime
  (taps overcome surface forces; gravity alone cannot), keeps the
  electronics count at zero, and the only printed parts are a
  bottom-mesh cup and an anvil.
- *Risks*: tap-energy repeatability depends on Z-axis acceleration
  consistency; mesh size has to be matched to particle size (one printed
  cup per powder); needs an external balance for sub-mg accuracy.
- *Build day*: print cup + anvil (~3 h), hand-cut steel mesh insert
  (~30 min), G-code peck routine (~1 h), characterise on a 0.1 mg balance
  (~3 h).

### B. Pez-style positive-displacement chamber strip ⭐

A printed cartridge holds a row of small (e.g. 5–50 µL) **fixed-volume
chambers** in series. Each chamber is pre-loaded once, off-line, by
slot-filling and striking off the top with a flat blade (so each chamber
holds a metrologically-flat constant volume — the "loss-on-strike" idea
already used by powder-fill machines at industrial scale). To dose, the
gantry advances the cartridge one chamber-pitch using a fixed pawl on
the bed (rack-and-ratchet), bringing the next loaded chamber over the
target. A spring-loaded ejector or a fixed pin pushes the chamber's
contents downward into the vial.

- *Mechanism in the PR #11 taxonomy*: positive-displacement / volumetric
  micro-dispenser, conceptually closest to **Chemspeed SWILE** — the
  best-evidenced sub-mg head in the literature — but built from PLA and
  TPU rather than glass capillaries and pneumatics.
- *Why it's interesting*: per-dispense mass is set by chamber geometry
  (printable to ~0.05 mm with FDM, finer with resin), so once the
  packing density of a powder is calibrated, mass is repeatable without
  any feedback. Cross-contamination is bounded (each chamber is
  used once and discarded with the strip).
- *Risks*: cohesive powders may bridge over chamber openings during
  fill; open-strike accuracy is fundamentally limited by powder
  packing variance (PR #11 §4 cites < 1 % under "ideal conditions",
  much worse for cohesive solids); strip needs to be re-loaded between
  runs.
- *Build day*: design + print strip + cartridge holder + ratchet pawl
  (~4 h), print fill jig + striker bar (~1 h), characterise (~3 h).

### C. Capillary dip + fixed wiper (a printable mini-SWILE) ⭐

A short, fine-bore printed (or commercial PEEK / PTFE) **straw** is held
by the spindle clamp. The gantry dips it into a powder reservoir; the
straw fills by a combination of jamming and capillary forces. The gantry
then traverses to the dispense site and drives the straw past a fixed
**wiper / scraper** on the bed (a printed knife-edge), shearing off the
powder column into the receiving vial.

- *Mechanism in the PR #11 taxonomy*: directly the **Chemspeed SWILE**
  principle — piston-and-glass-capillary positive displacement, the
  only sub-mg head that has been benchmarked from 0.1 mg upward in
  the published evidence (PR #11 §1, §2). Replicating it in
  printable / off-the-shelf parts is exactly the "open SWILE
  alternative" gap called out in PR #11 §5.
- *Why it's interesting*: smallest doses of any concept here; entirely
  passive on the dispense side (the wiper is bolted to the bed, the
  straw is bolted to the spindle, the gantry does the rest).
- *Risks*: "fill" repeatability of an unmodulated dip is the SWILE's
  Achilles heel even in the commercial product; very fine bores will
  clog with cohesive powders; printed bores may not be smooth enough
  without a PTFE-spray finish.
- *Build day*: print straw holder + wiper + reservoir (~2 h), source
  straws / PEEK tubing from the makerspace (~1 h), characterise
  (~4 h).

### D. Brush / swab pickup + comb knock-off

A natural-bristle brush or static-dissipative microfibre swab is
clamped to the spindle. The gantry dips the brush into a powder dish;
particles adhere to the bristles by van der Waals + electrostatic
attraction (the same surface forces that make cohesive powders hard to
dose by gravity become the *mechanism* here). The gantry transports the
loaded brush to the dispense site and drags it across a fixed printed
**comb** that mechanically knocks particles off into the target vial.

- *Mechanism in the PR #11 taxonomy*: not directly represented in the
  commercial landscape — closest analogue is the dual-arm spatula
  dispenser of Jiang et al. 2023 (PR #11 §6), but at a much smaller
  pickup mass.
- *Why it's interesting*: turns the cohesive-powder failure mode into
  the design principle; absolutely minimal hardware; very small mean
  doses (likely sub-mg).
- *Risks*: highly powder-dependent; mass per stroke probably has high
  RSD; needs external balance / weighing for any usable accuracy.
- *Build day*: print brush holder + comb + reservoir (~2 h),
  characterise (~4 h).

### E. Salt-shaker oscillation dispenser

A printed cup with a calibrated bottom slot/mesh is moved by the gantry
in a fast sinusoidal X-Y "shake" pattern over the target. Total dose is
proportional to (shake amplitude × frequency × duration). No tap
required — the side-to-side acceleration substitutes for the vertical
tap of concept A.

- *Mechanism*: gantry-driven analogue of a vibratory sieve feeder (PR
  #11 §4 cites commercial equivalents from 0.36 to 1440 g/h).
- *Why it's interesting*: smooth, continuous control of dose by time
  rather than discrete taps; no impacts on the gantry frame.
- *Risks*: GRBL feedrate / acceleration limits cap how "vibratory" the
  motion really is — the 3018 is not a piezo. Minimum stable dose may
  be tens of mg.
- *Build day*: print cup (~1 h), tune G-code shake pattern (~3 h),
  characterise (~3 h).

### F. Passive auger via rack-and-pinion against a fixed pin

A short Archimedes screw inside a printed tube is geared (printed
rack + pinion or one-way clutch) to a small linear stage on the
spindle. As the gantry pushes the stage past a fixed pin on the bed, the
pinion ratchets the screw forward by a fixed angle, positively
displacing one auger-thread of powder out of the tube tip into the
target vial.

- *Mechanism in the PR #11 taxonomy*: volumetric screw / auger feeder,
  the dominant industrial principle (Coperion K-Tron, Acrison, Schenck;
  PR #11 §3) — but here all rotation comes from gantry push, no motor.
- *Why it's interesting*: continuous and repeatable in principle; gives
  per-stroke dose set by pitch × thread cross-section.
- *Risks*: small printed augers are leaky / fragile; tolerances on
  printed gear teeth are marginal at this size; cohesive powders pack
  against the auger root; build complexity is the highest of the
  passive options.
- *Build day*: high — design and print auger + clutch + stage (~6 h),
  iterate, characterise. Risk of not finishing in one day.

### G. Add a single ERM coin motor to concept A

Identical to concept A (tap-driven sieve cup) but augmented with a
~$2 ERM "phone haptic" coin motor glued to the side of the cup, run
from a 3 V coin cell via a SPST switch (no microcontroller). The motor
provides higher-frequency vibration than the gantry tap can supply,
extending the lower bound of dose-rate and improving repeatability.

- *Why it's interesting*: best-evidence, lowest-risk way of attacking
  the cohesive-powder regime if a single active component is acceptable
  (matches the strategy already proposed in
  [issue #3 Challenge 2](https://github.com/vertical-cloud-lab/powder-excavator/issues/3#issue-anti-adhesion)).
- *Risks*: introduces one battery / motor / switch — the smallest
  possible deviation from "fully passive". Vibration amplitude is
  fixed; closed-loop control requires either a relay or an MCU.

### H. Solenoid-tapped sieve (closed-loop tap)

Concept A but with a 5 V push-pull solenoid replacing the gantry tap,
fired by a microcontroller against an external balance reading. This is
the most accurate path here but also the most "electronics-heavy", and
duplicates much of what a Quantos already does — likely not worth the
build-day risk on day-of-workshop.

## Ranking summary

| Rank | Concept | Active components | Expected dose floor | Risk |
| ---- | ------- | ----------------- | ------------------- | ---- |
| 1 | A. Tap-driven sieve cup | 0 | ~1–10 mg / tap | Low |
| 2 | B. Pez-style chamber strip | 0 | ~1–20 mg / chamber | Low |
| 3 | C. Capillary dip + wiper | 0 | ~0.1–5 mg / stroke | Med |
| 4 | E. Salt-shaker oscillation | 0 | ~10 mg / s | Med |
| 5 | D. Brush pickup + comb | 0 | ~0.05–5 mg / stroke | Med |
| 6 | G. ERM-augmented sieve | 1 (ERM motor) | ~0.5–5 mg / sec | Low–Med |
| 7 | F. Passive auger | 0 | ~5–50 mg / stroke | High (build) |
| 8 | H. Solenoid + balance | 2+ (solenoid, MCU) | ~0.1 mg (closed-loop) | High (build + tuning) |

**Recommended for the one-day build:** concept **A** as the headline
design (lowest risk, most differentiated from #2 and #5, attacks the
cohesive-powder regime exactly where PR #11 says the field has the
biggest open gap), with concept **B** (Pez strip) as a parallel-track
fallback because it can be characterised on a benchtop balance even if
the gantry isn't available.

## Edison feedback query

A single Edison **literature** query was submitted for outside feedback
on the eight concepts above (don't-wait policy, per the issue). The
task ID and the full prompt are persisted in
[`edison_query.json`](./edison_query.json); the answer will be fetched
in the next session and incorporated into a follow-up update to this
document.
