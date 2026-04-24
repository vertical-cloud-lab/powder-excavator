# powder-excavator

![Design sketch](powder-excavator-sketch.jpg)

## Paper

A bare-bones LaTeX template in the Digital Discovery (Royal Society of
Chemistry) submission style is available in [`paper/`](paper). It is built on
the official RSC "Paper" article template (two-column, 8.5pt Times,
`natbib`/`rsc.bst` bibliography, RSC running headers/footers) and uses
`lipsum` placeholder text. A pre-built PDF is committed alongside it at
[`paper/main.pdf`](paper/main.pdf).

To rebuild the PDF locally (requires a TeX Live installation that includes
`latexmk` and standard packages such as `natbib`, `mhchem`, `times`,
`mathptmx`, `lastpage`, `lipsum` and `url`; the RSC class assets — `rsc.bst`,
`rsc.bib`, `headers/`, `mhchem.sty`, `balance.sty`, `caption.sty`,
`caption3.sty`, `fancyhdr.sty`, `secsty.sty` — are vendored in `paper/`):

```sh
cd paper
latexmk -pdf main.tex
```
