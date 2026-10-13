# Structure-aware robust hosting-capacity algorithm — manuscript

**Purpose:** an algorithm paper, not a global optimality paper. The main contribution is a complete-load-interval feasibility oracle combining nonlinear DistFlow implicit derivatives, separated Hessian blocks for voltage, half-disc support functions, complex-power phasor geometry for thermal constraints, and joint PV apparent-power capability. Heterogeneous inverter gains are a light outer design variable.

## Research logic
1. For a candidate gain vector and load cell, enclose the nonlinear normal branch and compute its first/second derivatives.
2. Use blockwise Hessian bounds and exact right-half-disc supports to bound each signed voltage violation over the *entire* cell.
3. Use affine complex-power angular supports (plus grid and nonlinear-remainder allowances) to bound each line current.
4. Require the full correlated PV $(P,Q)$ circle test throughout the cell. If raw Q clips, return UNKNOWN rather than reusing unsaturated derivatives.
5. Recursively subdivide failed cells. Accept capacity L **only if every cell of [0,L] passes**.
6. As an optional design layer, search gain vectors and retain the one with the largest passing connected capacity.

## Contents
- `paper/main.tex`: English manuscript with problem formulation, two core algorithms, conditional theorem/proof, numerical comparison and limitations.
- `results/ieee33_design_trials.csv`: reported experimental design candidates (FLOAT, not outward-rounded safety proofs).
- `paper/REPRODUCIBILITY.md`: exact distinction between mathematical theorem, exploratory IEEE33 inner candidates and interval-certified fixed-disturbance *unsafe* witnesses.

## Study benchmark
case33bw active 32 lines; base loads ×0.65; PVs at buses 9,18,24,33, 0.25 MW nominal each; each has a 0.125 MVA right-half-disc uncertainty and 1 MVA rating; additional unity-PF load at bus18; V limits [0.95,1.05] pu; **common 0.31 pu line current is a research-assumed limit**, not official branch ratings.

| Gains (buses 9/18/24/33) | FLOAT passed complete-prefix target |
|---|---:|
| (1.92,1.92,1.92,1.92) | 1.0586 MW |
| (3.70,1.92,2.12,2.52) | 1.1363 MW |
| (3.80105,1.89598,2.39520,4.00) | 1.1500 MW |

The 8.63% improvement is in a *conservative computed inner capacity*, not a rigorously proved physical improvement or a global optimum.

**Source status:** Full IEEE33 runnable numerical dependency set still resides in the previous experiment ZIP, not in this GitHub branch. Existing math proofs and standalone exact outer-bound code are in sibling `droop_closed_loop_wclf/` on this same PR branch. Do not claim standalone IEEE33 code reproducibility from the paper folder yet.

Build manuscript when pdflatex is installed:
```bash
cd distribution_capacity_algorithm/paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
