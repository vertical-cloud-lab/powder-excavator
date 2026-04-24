# Commercial Powder Dispensing Solutions — Landscape

This document collects the commercial company / product landscape for powder
dispensing solutions, motivating the design of `powder-excavator`.

## Status

Five Edison Scientific literature queries were submitted in a prior session
and have now been fetched. The full citation-backed answers are stored
verbatim under [`edison_results/`](./edison_results/) — one Markdown file
per query, plus the raw JSON response. The synthesis below references those
files and pulls out the most useful evidence-backed findings; consult the
per-query files for full tables and citations.

A **second batch of six follow-up queries** has now been submitted (not
yet awaited; to be fetched in a follow-up session) to fill the gaps
identified in the first synthesis — in particular **MTI** (both MTI
Corporation lab equipment and MTI Mixers industrial), Acrison / Hapman /
AZO / PSL / Matcon, mainstream liquid-handler powder modules (Hamilton,
Tecan, Zinsser, Gilson, Sartorius, CyBio, Anton Paar), acoustic / piezo
dry-powder microdispensers and the specific Quantos QX1/QX2 and Chemspeed
Powdernium product lines, and academic / open-source robotic dispensers.
See the [Submitted Edison queries](#submitted-edison-queries) section for
the full list and task IDs.

| Tag (file) | Focus |
| --- | --- |
| [`commercial-powder-dispensers-overview`](./edison_results/commercial-powder-dispensers-overview.md) | Cross-cutting landscape (lab + industrial) |
| [`lab-automated-powder-dispensing-companies`](./edison_results/lab-automated-powder-dispensing-companies.md) | Lab vendors and model names |
| [`powder-dosing-technology-comparison`](./edison_results/powder-dosing-technology-comparison.md) | Technology-by-technology comparison |
| [`industrial-powder-feeders-bulk-handling`](./edison_results/industrial-powder-feeders-bulk-handling.md) | Industrial / bulk vendors |
| [`micro-dose-mg-precision-dispensers`](./edison_results/micro-dose-mg-precision-dispensers.md) | mg / sub-mg precision instruments |

## Synthesis

> All numeric specs, model names and limitations below come from the
> retrieved Edison answers. Where a vendor or product was named in the
> original prompt but no datasheet evidence was returned, that is called
> out explicitly so the gap is visible rather than fabricated.

### 1. Bench-top / laboratory automated powder dispensers

The two best-evidenced commercial benchtop platforms for HTE-grade solid
dispensing are **Mettler Toledo Quantos** and **Chemspeed**:

- **Mettler Toledo Quantos** (e.g. QB5 with QH012-LNMP head; QX96 carousel
  on an XPE206 balance). Gravimetric dosing with a combined rotary +
  tapping action and an RFID-tagged dosing head that supports parameter
  learning. Comparative benchmarking exercised it at 2, 10, 50 and 20 mg
  targets; performance is balanced across many pharmaceutical powders but
  RSD degrades sharply below ~10 mg, and over-dispensing on coarse
  powders or timeouts on poor-flowing solids (e.g. potassium acetate,
  molecular sieves, ammonium acetate) are known failure modes. The
  CHRONECT integration adds a 32-position dosing-head rack with a 6-axis
  robotic arm; reported average dispense time ≈138 s.
- **Chemspeed** (SWING / FLEX / Crystal platforms, with the **GDU-S
  SWILE** piston-and-glass-capillary head and the **GDU-Pfd** hopper /
  auger / crescent-valve head). SWILE was demonstrated effective from
  **0.1 mg to 50 mg** and is favoured for sub- to low-mg dispensing of a
  wider powder range (including sticky/oily solids); GDU-Pfd uses a
  30 mL container with a typical ±10% tolerance setting and was tested
  down to 0.5 mg. Average dispense time ≈103 s; at a 2 mg target it
  beat CHRONECT/Quantos on speed (54 vs 141 s).
- **Unchained Labs / Freeslate**: present in HTE comparisons as an
  earlier-generation automated solid + liquid dispensing platform; cited
  per-dispense times >250 s, slower than current Mettler / Chemspeed
  systems. **Symyx** is identified as a classic combinatorial supplier
  but no model-level numeric specs were retrieved.
- **Zinsser Analytic Lissy, Gilson, Hamilton STAR, Sartorius, Analytik
  Jena CyBio, Anton Paar, Retsch / Verder, Plasmatreat, AutoDose**: named
  in the prompt but **no quantitative solid-dispensing datasheet
  evidence was returned**. They appear in the literature mostly as
  generic robotic-platform / liquid-handling vendors; product-specific
  brochures will be needed to fill these in.

### 2. Micro- / milligram-scale precision dispensers

- Among gravimetric dispensers, **Quantos** is well evidenced down to
  20 mg (with mean errors growing for many powders, e.g. Al₂O₃
  −6.00 ± 0.93 %, NaNO₂ −3.96 ± 2.40 %, pectin −5.87 ± 1.37 % at 20 mg;
  near-zero mean error for most powders at 200–1000 mg).
- **Chemspeed GDU-S SWILE** is the strongest evidenced low-/sub-mg
  performer (0.1–50 mg study range).
- A field-wide observation across several reviews is that **single-shot
  dispensing below ~10 mg is broadly difficult** for any commercial
  gravimetric / hopper system; SWILE-style positive-displacement and
  acoustic / piezo approaches are the main paths beyond that limit.
- Specific user-named products **Quantos QX1 / QX2**, **Chemspeed
  "Powdernium"**, and a **"Hamilton STAR powder head"** were *not*
  substantiated in the retrieved evidence — they may be marketing-only
  names or otherwise underdocumented in the literature.
- True acoustic / piezo dry-powder micro-dispensers were not found with
  vendor specs in the Edison evidence set (Labcyte Echo / Scienion
  systems are predominantly liquid-only); EDC Biosystems is the only
  vendor commonly cited for ng-scale dry-powder dosing of engineered
  particles.
- The Hou (2024) micro-feeder thesis provides a useful comparison row
  set: **MG2 Microdose** vibratory sieve at 0.36–0.54 g/h, **3P
  Innovation** piezo-vibration feeder at 3.6–1440 g/h, **LCI Circle
  Feeder MD-120** rotating-vane >32 g/h, **DEC µPTS** pressure-transfer
  at 3.6–450 g/h handling sub-µm/cohesive/wet powders, and **Vibra-Flow**
  <3.6 g/h.

### 3. Industrial bulk powder feeders and dispensing

The strongest evidence is for continuous **gravimetric loss-in-weight
(LIW) screw feeders**:

- **Coperion K-Tron** — KT16 (24 kg scale), KT20 / KT35 (90 kg scale);
  pharma study targets <3 % RSD and 99–101 % feeding accuracy;
  MT-12 / MT-20 micro feeders at 32–3540 g/h. Used in the **Lilly
  continuous direct-compression** platform.
- **Schenck Process / AccuRate**, **Brabender Technologie** — appear in
  the LIW comparison literature; specific model/capacity claims for
  these are sparser in the retrieved set.
- **GEA / Buck** — split-butterfly / containment valves for contained
  charging/discharging.
- **Glatt** — appears as a containment valve patentee.
- **Gericke** — GAC232 (tool size 8) at 160–3200 L/h; integrated with
  continuous mixing equipment.
- **Hosokawa Micron** — discussed for FIBC/IBC filling, discharge and
  contained transfer at concept level.
- **Acrison, Hapman, AZO, Powder Systems Limited (PSL), Matcon, MTI
  Mixers**: no primary model/capacity sources were retrieved; treat
  claims about these vendors as unconfirmed pending vendor datasheets.

### 4. Dispensing technologies compared

From `powder-dosing-technology-comparison.md`:

- **Gravimetric LIW feeders** — direct mass-flow control via load cells;
  a feeder-performance article cites achievable **±0.2 % of set rate
  over a 20:1 turndown**; main disturbances are refill events,
  cohesion, electrostatics and under-filled screws at high speed.
  Inherently automation-friendly because mass flow is already digitised.
- **Volumetric screw / auger feeders** — open-loop, no self-correction;
  reviews note rotating-groove volumetric devices can show **<1 %
  variation** under ideal conditions and reach 3–11 g/s, but accuracy
  degrades with bulk-density change, packing, humidity, electrostatics
  and headload variation.
- **Vibratory / piezo micro-feeders** — practical for some micro-feeding
  but limited at low rates with cohesive powders; commercial examples
  cover roughly 0.36–1440 g/h.
- **Acoustic / pneumatic micro-dispensers** — aspirate-and-dispense
  examples deliver 0.5–10 mg with ~1–2 mm tube diameters and ~2–10 kPa
  partial vacuum; few vendor specs were retrievable for true acoustic
  dry-powder ejection.
- **Quantos-style micro-dosing heads with tapping** — best evidenced
  from ~10 mg upward; powder/head matching matters more than nominal
  tolerance.
- **Robotic spatula / scoop systems** — represented by recent academic
  work (e.g. Jiang et al. 2023, dual-arm biomimetic dispensing); flexible
  on cohesive powders and powder variety, but slower per dispense than
  dedicated heads.

### 5. Gaps and opportunities for `powder-excavator`

The Edison-backed evidence highlights a consistent set of gaps in
commercial offerings that motivate this project:

1. **Sub-10 mg single-shot dispensing of cohesive powders** is poorly
   served by existing gravimetric heads; SWILE is the main credible
   option and is locked into the Chemspeed platform.
2. **Vendor-lock-in**: the well-evidenced lab platforms (Quantos,
   Chemspeed) are tightly coupled to proprietary balances, dosing heads
   and software; there is no widely-cited *open* hardware/software
   stack for HTE-grade solid dispensing.
3. **Cohesive / sticky / electrostatic / wet powders** repeatedly appear
   as failure modes across vendors. Closed-loop adaptive strategies
   (e.g. flow-aware dosing as in FLIP-style ML approaches) are mostly
   research prototypes today.
4. **Throughput gap between lab and industrial scales**: lab heads
   operate at mg/dispense × ~100 s/dispense; industrial LIW feeders
   start in the kg/h range. The g/min "kilo-lab" middle ground is
   under-served.
5. **Cross-platform integration**: most vendors expose limited APIs and
   few publish protocols suitable for autonomous / self-driving-lab
   orchestration; new entrants have a clear opening on
   automation-friendly integration.

## Submitted Edison queries

See [`edison_queries.json`](./edison_queries.json) for the full prompts and
task IDs, and [`edison_results/`](./edison_results/) for the fetched
answers (Markdown + JSON, one pair per tag).

**First batch** (fetched, in `edison_results/`):

| Tag | Focus |
| --- | --- |
| `commercial-powder-dispensers-overview` | Cross-cutting landscape (lab + industrial) |
| `lab-automated-powder-dispensing-companies` | Lab vendors and model names |
| `powder-dosing-technology-comparison` | Technology comparison table |
| `industrial-powder-feeders-bulk-handling` | Industrial / bulk vendors |
| `micro-dose-mg-precision-dispensers` | mg / sub-mg precision instruments |

**Second batch** (submitted, *not* yet fetched — pull in next session):

| Tag | Focus |
| --- | --- |
| `mti-corporation-lab-powder-equipment` | MTI Corporation (mtixtl.com) lab/materials-research powder equipment |
| `mti-mixers-industrial-powder-handling` | MTI Mixers / MTI Group industrial powder mixing & handling |
| `industrial-bulk-vendors-acrison-hapman-azo-psl-matcon` | Acrison, Hapman, AZO, PSL, Matcon model-level specs |
| `lab-liquid-handlers-with-powder-modules` | Hamilton, Tecan, Zinsser, Gilson, Sartorius, CyBio, Anton Paar solid-dispensing modules |
| `acoustic-piezo-capacitive-microdose-and-quantos-qx-chemspeed-powdernium` | Acoustic/piezo dry-powder dispensers + Quantos QX1/QX2 + Chemspeed Powdernium / GDU specifics |
| `academic-and-open-source-powder-dispensing-robots` | Academic / open-source / self-driving-lab powder dispensing robots |

## Reproducing the fetch

All five tasks completed with `status=success`. They were re-fetched with:

```python
import json, os
from edison_client import EdisonClient

client = EdisonClient(api_key=os.environ["EDISON_API_KEY"])
with open("research/edison_queries.json") as f:
    records = json.load(f)

for r in records:
    task = client.get_task(r["task_id"])
    # task.formatted_answer holds the citation-backed Markdown answer
    print(r["tag"], task.status)
```
