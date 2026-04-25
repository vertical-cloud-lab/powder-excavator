# Project wrap-up presentation

Marp slides for the `powder-excavator` project (issue #17, PR #18).

## Build

```bash
cd presentation
npm install
npx marp --html --allow-local-files slides.md -o slides.html
npx marp --pdf  --html --allow-local-files slides.md -o slides.pdf
```

## How to present (with the videos playing)

The embedded `<video>` only plays in the **HTML** build, not the PDF. Three
ways to drive the live deck:

1. **Browser, fullscreen** *(recommended)* — open `slides.html` in
   Chrome/Firefox, press <kbd>F11</kbd> for fullscreen, then arrow keys to
   advance. The video on slide 10 autoplays muted and loops; click it for
   audio. This is the most reliable path on a presenter laptop.
2. **Marp watch/server mode** — for editing while presenting, run

   ```bash
   npx marp --html --allow-local-files --server .
   ```

   then open <http://localhost:8080/slides.html>. Edits to `slides.md` reload
   live.
3. **Marp Preview / VS Code Marp extension** — opens the deck in a
   presenter-style window with speaker notes; `<video>` plays here too.

Slide 11 is the **GIF** version of the same moment, so the **PDF** export
still carries the motion (e.g. when sharing the deck after the talk).

## Files

- [`slides.md`](slides.md) — source (Marp Markdown)
- [`slides.html`](slides.html) — built HTML deck (renders the embedded video)
- [`slides.pdf`](slides.pdf) — built PDF (the GIF slide preserves the motion)
- [`assets/`](assets) — images, GIFs, and the print video referenced by the slides

## Design principles

Slides follow Jean-luc Doumont's principles:

- The **title area is the message area** — every slide title is a complete
  sentence stating the message of the slide.
- **Maximize signal-to-noise** — one image or one short list per slide; no
  decorative chrome; chartjunk avoided.
- Build-up ordering: problem → first attempt → pushback → fix → result →
  generalization → next steps.
