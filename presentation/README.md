# Project wrap-up presentation

Marp slides for the `powder-excavator` project (issue #17, PR #18).

## Build

```bash
cd presentation
npm install
npx marp --html --allow-local-files slides.md -o slides.html
npx marp --pdf  --html --allow-local-files slides.md -o slides.pdf
```

## Files

- [`slides.md`](slides.md) — source (Marp Markdown)
- [`slides.html`](slides.html) — built HTML deck (renders the embedded video)
- [`slides.pdf`](slides.pdf) — built PDF (static; video shows poster frame)
- [`assets/`](assets) — images and the print video referenced by the slides

## Design principles

Slides follow Jean-luc Doumont's principles:

- The **title area is the message area** — every slide title is a complete
  sentence stating the message of the slide.
- **Maximize signal-to-noise** — one image or one short list per slide; no
  decorative chrome; chartjunk avoided.
- Build-up ordering: problem → first attempt → pushback → fix → result →
  generalization → next steps.
