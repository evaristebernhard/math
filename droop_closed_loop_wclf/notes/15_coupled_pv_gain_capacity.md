# Capacity-first update: coupled PV P/Q, saturation, and gain selection

Date: 2026-10-13. Status: exact mathematical lemmas + DOUBLE PRECISION experiment. NOT outward-rounded IEEE-33 certification.

## A modeling correction that changes capacity conclusions

If both independent right-half-disc PV injection disturbances (wp,wq) and voltage-droop correction are delivered by the **same PV inverter**, then

\[
P_{\mathrm{PV},j}=0.025+w_{p,j},\quad
Q^{\rm raw}_{\mathrm{PV},j}=w_{q,j}-g_j(V_j-1)
\]

in per-unit on a 10 MVA base, with PV inverter nameplate S=0.1 pu. The physical law is

\[
Q_{\rm PV,j}=\operatorname{clip}(Q^{\rm raw}_{\rm PV,j},
-\sqrt{S_j^2-P_{\rm PV,j}^2},+\sqrt{S_j^2-P_{\rm PV,j}^2}).
\]

The previous check on the droop correction alone was NOT sufficient to certify full PV apparent-power limits. We retain the unsaturated smooth closed-loop DistFlow branch only where a full apparent-power inequality has been certified for all uncertainty sources. For other regimes, use the clipped law; derivatives/Hessians of the unsaturated model must NOT be used across switching surfaces.

## An exact angular formula for correlated PV apparent-power uncertainty

Let w_k=(wp_k,wq_k) range independently over right half-discs Omega(C_k); let the load increment s range over [-h,h]. Given an affine two-dimensional PV output

\[
y_{\rm aff}(w,s)=d+\sum_k T_k w_k+t s,
\]

define e(theta)=(cos(theta),sin(theta)) and hplus(a,b)=sqrt(a*a+b*b) for a>=0, otherwise |b|. Then

\[
\boxed{\max_{w,s}\|y_{\rm aff}(w,s)\|_2=
\max_{\theta\in[0,2\pi]}\left[
e(\theta)^T d+\sum_k C_k hplus(T_k^T e(\theta))
+h |t^Te(\theta)|\right].}
\]

Proof: Euclidean norm is the support function of the Euclidean unit circle. Swap two compact maxima and maximize each independent right-half-disc support block and the scalar load interval. QED.

The angular expression is Lipschitz in theta with a valid constant
K=||d|| + sum C_k ||T_k||_F + h||t||. Taking N equispaced angles, the global max is bounded above by sampled maximum + pi*K/N. Sampling alone is a LOWER bound on the maximum and does not certify safety.

On an unsaturated closed-loop normal branch, expand V_j at a nominal load and zero disturbance. Its Hessian satisfies

\[
D^2V_j=\frac{D^2\nu_j}{2\sqrt{\nu_j}}-
\frac{D\nu_j D\nu_j^T}{4\nu_j^{3/2}},
\]

so if ν_j>=ν_L>0, ||D²ν_j||<=Mnu and ||Dν_j||<=Knu uniformly,
MV <= Mnu/(2sqrt(ν_L)) + Knu²/(4ν_L^(3/2)).
A Taylor remainder of the PV Q output is at most
eta=g_j MV(h²+sum C_k²)/2.
Hence a sufficient full inverter unsaturation condition is

\[
\boxed{J_{\rm grid}+\pi K/N+\eta\le S_j.}
\]

The affine vector uses d=(Ppv0,-g(V0-1)); its active row responds to own wp only; its reactive row responds both to own wq and to the closed-loop voltage sensitivity for all PV sources, and to the flexible-load increment. This retains PV P/Q correlation instead of bounding the P and Q extrema independently.

## Connected hosting: a simpler upper-exclusion lemma

For fixed g and a physical clipped-control normal power-flow branch, define the robustly safe load set C(g) and the connected incremental hosting upper endpoint

\[
\Lambda_{\rm conn}(g)=\sup\{L\ge0:[0,L]\subseteq C(g)\}.
\]

If any **feasible** physical PV disturbance at some load Lu yields overcurrent or an out-of-range bus voltage, then

\[
\boxed{\Lambda_{\rm conn}(g)\le L_u.}
\]

No load derivative sign or exclusion of all greater *pointwise* safe load levels is required. A genuine violated witness obstructs every continuously safe prefix extending across it. This updates the more restrictive monotonicity-focused argument in note 14. The latter is useful only when trying to exclude *all* higher disconnected safe points.

## IEEE-33 preliminary corrected study

Network: MATPOWER case33bw, 32 radial in-service lines, 10 MVA 12.66 kV base; base demand x.65; PV at buses 9,18,24,33, base 0.25MW each, uncertain PV (P,Q) independent half-disc C=0.125MVA; S=1MVA for each inverter; added unity-PF load at bus 18; voltage 0.95–1.05pu; a RESEARCH-ASSUMED common current limit 0.31pu, not real line nameplate data.

The continuous INNER capacity is checked by earlier nonlinear box/block-Hessian method, now with correlated full PV apparent-power envelope above to validate unsaturation. The UPPER obstruction is the first violation among a finite list of feasible disturbance witnesses, solved with the physically clipped Q law. It is not an adversarial global-max computation.

| Uniform g | Candidate continuous safe inner MW | First tested unsafe-witness barrier MW |
|---:|---:|---:|
| 1.50 | 0.89334 | 0.91890 |
| 1.70 | 0.97376 | 1.00280 |
| 1.80 | 1.01309 | 1.04380 |
| 1.85 | 1.03255 | 1.06408 |
| 1.90 | 1.01922 | 1.08421 |
| 2.00 | 0.99748 | 1.12403 |
| 2.20 | 0.95484 | 1.19767 |
| 2.40 | 0.91320 | 1.21002 |
| 2.60 | 0.86000 | 1.22173 |
| 3.00 | 0.78000 | 1.23685 |

At g=1.85 the simplistic independent |wq|+|Qdroop| capability check accepted only about 1.02156MW, while the correlated (P,Q) norm plus nonlinear Hessian remainder brought its connected candidate INNER bound back to 1.03255MW. On [1.02,1.04]MW the worst PV *computed upper bound* of apparent power was about 0.09785pu, below the 0.1pu nameplate; independent nonlinear power-flow boundary-angle search sampled max about 0.09426pu at load 1.03255MW, without proving global maximality.

Among the tested gains, g=1.85 has the highest *inner certificate*; the finite-witness upper obstruction keeps improving up to approximately g=2.9 and becomes overcurrent-limited above roughly 2.9–2.95. This wide and gain-dependent gap is the most important UNSOLVED capacity-control issue. Neither curve proves a global physical optimum.

All numbers are ordinary floating-point computation and only conditional real-arithmetic enclosure checks. The contracted box and derivatives were not calculated with outward rounding, and physical clipped PV branches have not been uniformly certified for every uncertainty/load. Different power-flow roots outside the chosen box are not excluded.

## Next mathematical task

Make a piecewise-smooth, saturation-aware NONLINEAR DistFlow safety enclosure (rather than borrowing an unsaturated Hessian across a clipping kink). Tighten the high-g connected INNER capacity, then compare it with valid fixed-witness barriers for the same gain and loading direction. Only then optimize g. A finite gain grid does not establish a global optimum.
