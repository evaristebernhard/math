# High-Filling Bose--Hubbard / Rotor Paper

This folder contains the submission-style LaTeX manuscript organized from the audited document `High_Filling_Bose_Hubbard_Rotor_Audited_Manuscript_2026-08-07(1).docx`.

## Authors

- Jizheng Chen — Department of Mathematics, Chang'an University — equal contribution
- Tianrun Yu — College of Control Science and Engineering, Zhejiang University — equal contribution
- Chaoyu Hu — School of Automation, Hangzhou Dianzi University — corresponding author

Corresponding email: `evaristebernhardwiener@gmail.com`.

## Files

- `main.tex` — complete manuscript
- `references.bib` — bibliography
- `SUBMISSION_NOTES.md` — editorial and mathematical-scope notes retained from the audited source

## Build

A standard BibTeX workflow is sufficient:

```text
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

The manuscript deliberately preserves the source document's scope limitations. In particular, it does not claim a thermodynamic BEC theorem, volume-uniform Gaussian domination for the full amplitude model, removal of the finite-window hypothesis from the second-order operator-norm expansion, or a complete fourth-order quantum effective Hamiltonian.
