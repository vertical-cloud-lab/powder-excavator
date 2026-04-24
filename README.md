# powder-excavator

![Design sketch](powder-excavator-sketch.jpg)

## Paper

A bare-bones LaTeX template in the Digital Discovery (RSC) submission style is
available in [`paper/main.tex`](paper/main.tex). A pre-built PDF is committed
alongside it at [`paper/main.pdf`](paper/main.pdf).

To rebuild the PDF locally (requires a TeX Live installation that includes
`latexmk`, `geometry`, `hyperref`, `authblk` and `lipsum`):

```sh
cd paper
latexmk -pdf main.tex
```
