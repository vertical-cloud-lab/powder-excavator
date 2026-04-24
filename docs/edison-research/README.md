# Edison Scientific research notes

Curated outputs from FutureHouse / Edison Scientific agents that informed the design
and review of the powder-excavator mechanism. Each file contains the original prompt
and the verbatim agent answer. Fetched via `edison_client` against the public API.

Use these as reviewer context for the bimodal compliant-mechanism PR — they capture
the prior-art search, the gantry-only kinematics critique that drove the design
toward a passive bistable trough, and the Edison-recommended bench-test plan.

| # | File | Crow | Trajectory ID |
| - | ---- | ---- | ------------- |
| 01 | [`01-gantry-scoop-feasibility-literature.md`](01-gantry-scoop-feasibility-literature.md) — Automated Powder Dispensing Gantry Scoop Feasibility | literature (PaperQA3, high) | `86968176-9927-43b4-aa09-e7e4f86855be` |
| 02 | [`02-low-cost-dispenser-design-review.md`](02-low-cost-dispenser-design-review.md) — Low-Cost Mechanical Powder Dispenser Design Review | analysis (Crow, high) | `faeecd89-ea28-403b-94f3-c8402a79e78a` |
| 03 | [`03-second-analysis-pass.md`](03-second-analysis-pass.md) — Second Analysis Pass on Powder-Excavator Mechanism | analysis (Crow, high) | `844f6123-36b7-4e61-a0f6-c2e357f804b0` |
| 04 | [`04-gantry-only-baseline-review.md`](04-gantry-only-baseline-review.md) — Gantry-Only Baseline Review Of Powder Excavator | analysis (Crow, high) | `d6e32c46-2774-4477-a060-9993ef51ab10` |
| 05 | [`05-gantry-only-mechanism-feedback.md`](05-gantry-only-mechanism-feedback.md) — Gantry-Only Powder Excavator Mechanism Feedback | analysis (Crow, high) | `7f85494a-ce97-4ebf-bea9-6ac2359014dd` |
| 06 | [`06-low-cost-gantry-dispenser-litreview.md`](06-low-cost-gantry-dispenser-litreview.md) — Low Cost Gantry Mounted Powder Dispenser Literature Review | literature (PaperQA3, high) | `ae836203-2acd-491c-b6a2-4c349245523b` |
| 07 | [`07-generative-cad-and-feedback-loops.md`](07-generative-cad-and-feedback-loops.md) — Generative CAD and Automated Feedback for Open Hardware | literature (PaperQA3, high) | `f5a27ed3-8530-4102-9e31-5af9bbe9b0e0` |
| 08 | [`08-end-to-end-cad-review-v3.md`](08-end-to-end-cad-review-v3.md) — End-to-End Review of Gantry-Only Powder Excavator CAD | analysis (Crow, high) | `ac68bc56-557c-4009-a03d-dc4cb9774691` |
| 09 | [`09-open-source-robotic-powder-dispensers.md`](09-open-source-robotic-powder-dispensers.md) — Survey of Open Source Robotic Powder Dispensing Systems | literature (PaperQA3) | `7b5e41fa-f5a9-4dba-bd79-75eaaca83ca3` |
| 10 | [`10-microdispenser-evidence.md`](10-microdispenser-evidence.md) — Datasheet and Paper Evidence for Dry-Powder Dispensers and Modules | literature (PaperQA3) | `78d179da-e724-4999-bb74-98a175944d6b` |
| 11 | [`11-liquid-handler-solid-modules.md`](11-liquid-handler-solid-modules.md) — Solid-Dispensing Modules For Liquid-Handling Platforms | literature (PaperQA3) | `d2f50d5d-4448-4ed7-80e9-8bb28ed60313` |
| 12 | [`12-industrial-bulk-vendor-specs.md`](12-industrial-bulk-vendor-specs.md) — Vendor-Specific Model Level Specifications For Industrial Powder Handling Equipment | literature (PaperQA3) | `a61e05d3-46bd-4439-a599-1a143995adcd` |
| 13 | [`13-mti-mixers-survey.md`](13-mti-mixers-survey.md) — MTI Mixers and MTI Group Equipment Survey | literature (PaperQA3) | `e2919d20-86cc-44eb-a1f0-d2fc5b2db4f3` |
| 14 | [`14-mti-corporation-catalog.md`](14-mti-corporation-catalog.md) — MTI Powder Handling Equipment Catalog | literature (PaperQA3) | `ab9e026e-946d-4918-a0b6-49e09d7bc962` |

## Reproducing

```python
import os
from edison_client import EdisonClient
client = EdisonClient(api_key=os.environ['EDISON_API_KEY'])
task = client.get_task(task_id='<trajectory-id-from-table>')
print(task.formatted_answer or task.answer)
```
