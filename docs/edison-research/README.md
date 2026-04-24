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

## Reproducing

```python
import os
from edison_client import EdisonClient
client = EdisonClient(api_key=os.environ['EDISON_API_KEY'])
task = client.get_task(task_id='<trajectory-id-from-table>')
print(task.formatted_answer or task.answer)
```
