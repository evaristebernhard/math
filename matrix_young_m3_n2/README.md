# Matrix Young m=3, n=2 working manuscript

This folder contains the audited LaTeX research notes for the three-factor, two-dimensional Matrix Young problem.

## Build

```bash
make
```

or

```bash
latexmk -pdf main.tex
```

## Status labels

- `[L]` established literature result
- `[R]` rigorous derivation retained in the manuscript
- `[W]` working lemma / proof chain still requiring independent audit
- `[N]` numerical evidence only
- `[F]` falsified or withdrawn route

The source deliberately does **not** promote the tentative equal-weight `j=1` dimension-free norm inequality to a theorem until its missing bridge has been independently closed.
