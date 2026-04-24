# Commercial Powder Dispensing Solutions — Landscape

This document collects the commercial company / product landscape for powder
dispensing solutions, motivating the design of `powder-excavator`.

## Status

Five Edison Scientific literature queries have been submitted to gather a
comprehensive, citation-backed landscape. Per the originating issue
("Send several Edison queries. Don't wait. Fetch next session.") the results
are intentionally **not** awaited in this session. Task IDs and the original
prompts are recorded in [`edison_queries.json`](./edison_queries.json) and
should be fetched (via `EdisonClient.get_task`) in a follow-up session, then
synthesized into the sections below.

## Outline (to be filled in once Edison results are fetched)

1. Bench-top / laboratory automated powder dispensers
   - Mettler Toledo Quantos (QX1, QX2)
   - Chemspeed (SWING, FLEX, Crystal, Powdernium / GDU heads)
   - Unchained Labs / Freeslate (Core Module powder dispensing)
   - Zinsser Analytic (Lissy)
   - Hamilton (STAR with powder head), Analytik Jena CyBio
   - Sartorius, Gilson, Anton Paar accessories
2. Micro- / milligram-scale precision dispensers
   - Acoustic and piezo-based micro-powder dispensers
   - Tapping / vibratory micro-dose modules
3. Industrial bulk powder feeders and dispensing
   - Coperion K-Tron, Schenck Process, Brabender Technologie
   - Gericke, Acrison, Hapman, AZO
   - GEA, Glatt, Powder Systems Limited (PSL)
   - Matcon (IBC), Hosokawa Micron, MTI Mixers
4. Dispensing technologies compared
   - Gravimetric loss-in-weight, volumetric screw/auger, vibratory,
     acoustic, micro-dosing heads, tapping, robotic spatula/scoop.
   - Accuracy, minimum dose, cohesive vs free-flowing powder
     suitability, contamination risk, throughput, automation/API.
5. Gaps and opportunities for `powder-excavator`

## Submitted Edison queries

See [`edison_queries.json`](./edison_queries.json) for the full prompts and
task IDs. Brief tags:

| Tag | Focus |
| --- | --- |
| `commercial-powder-dispensers-overview` | Cross-cutting landscape (lab + industrial) |
| `lab-automated-powder-dispensing-companies` | Lab vendors and model names |
| `powder-dosing-technology-comparison` | Technology comparison table |
| `industrial-powder-feeders-bulk-handling` | Industrial / bulk vendors |
| `micro-dose-mg-precision-dispensers` | mg / sub-mg precision instruments |

## Fetching results next session

```python
import json, os
from edison_client import EdisonClient

client = EdisonClient(api_key=os.environ["EDISON_API_KEY"])
with open("research/edison_queries.json") as f:
    records = json.load(f)

for r in records:
    task = client.get_task(r["task_id"])
    # Inspect task.status / task.answer / task.formatted_answer
    print(r["tag"], getattr(task, "status", None))
```
