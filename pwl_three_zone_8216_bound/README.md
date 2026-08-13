# Sparse toric PWL limit-cycle bounds

This directory contains the manuscript for a sparse toric counting method for constant-slope scalar periodic piecewise-linear equations, together with its three-zone saturation application and exact certificate.  The general fixed-itinerary theorem gives

\[
N_X(k,M)\le \Theta_k\,k!(4M)^k\mathsf L_{2k},
\]

while the three-zone application proves

\[
N_{\mathrm{reg},3z}^{+}\le 8216,
\qquad
L^*\le 16437.
\]

## Files

- `main.tex` - article manuscript.
- `general_toric_unconditional_graph.tex` - strong unconditional graph-structured fixed-itinerary theorem included by `main.tex`.
- `general_toric_unconditional.tex` - coarser all-loose backup formulation.
- `SPARSE_TORIC_GENERALIZATION.md` - proof-status and scope audit for the general method.
- `SHARP_BOUND_RESEARCH.md` - separate research ledger for the conjectural
  sharp bound $L^*\le5$; it is not used by the proved manuscript.
- `references.bib` - cited bibliography.
- `Makefile` - standard build/verification entry points.
- `supplementary_certificate.tex` - stand-alone explanation and exact volume tables.
- `verification/verify_certificate.py` - deterministic symbolic and polyhedral verifier.
- `verification/mixed_volume_certificate.json` - complete exponent, vertex, and Minkowski-volume data.

## Reproduce the certificate

The verifier requires Python 3 and SciPy:

```bash
python3 verification/verify_certificate.py \
  --check verification/mixed_volume_certificate.json
```

It verifies support/vertex counts

```text
F=36/16, G=265/24, H2=1154/52,
H1_tilde=12360/54, P_epsilon=13/8, Hc_tilde=2692/74
```

and normalized polarization sums and mixed volumes

```text
163392/24=6808, 37632/24=1568, 29952/24=1248.
```

## Build

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary_certificate.tex
```
