# powder-excavator

![Design sketch](powder-excavator-sketch.jpg)

## Secondary design idea — bimodal (bistable) compliant mechanism

A second design direction is being explored alongside the cam-ramp baseline:
a single-piece printed trough suspended by a pre-compressed flexure pair
that snaps between a "scoop" pose and a "dump" pose with no pin joints,
spring, or external latch. See
[`docs/bimodal-compliant-mechanism.md`](docs/bimodal-compliant-mechanism.md)
for the design rationale.

To check that a candidate flexure geometry is actually bimodal (two stable
equilibria with a positive snap-through barrier), install the open-source
analysis stack and run the analyzer + tests:

```bash
pip install -r requirements.txt
python scripts/bimodal_compliance.py        # summary report + energy plot
pytest tests/test_bimodal_compliance.py     # bistability regression tests
```

The same checks run automatically in CI via
[`.github/workflows/bimodal-compliance.yml`](.github/workflows/bimodal-compliance.yml).