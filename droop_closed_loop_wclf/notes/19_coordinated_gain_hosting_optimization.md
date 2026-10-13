# Capacity control through coordinated inverter gains: first IEEE-33 experiment

Research note, 2026-10-13. This is **the B extension of A's existing capacity certification**, not a replacement for the implicit Jacobian, block Hessian, right-half-disc support, or phasor line-current bounds. Mathematical and numerical status are deliberately separated.

## 1. Model and actual control decision

The network, data normalization, voltage/current assumptions, PV active/reactive uncertainty sets, and flexible load at bus 18 remain **identical** to notes 12–18. The only added decision is the vector of four inverter Volt/VAR droop gains

\[
\mathbf g=(g_9,g_{18},g_{24},g_{33})\in[0,4]^4.
\]

The range [0,4] is an explicit **research-study constraint**, not a demonstrated hardware or dynamic-stability admissible interval. With physically active-power-dependent reactive clipping,

\[
Q_j=\operatorname{clip}\left(w_{q,j}-g_j(V_j-1),
-\sqrt{S_j^2-P_j^2},\sqrt{S_j^2-P_j^2}\right).
\]

For an uncertainty set \(\mathcal U\) made of four independent right half-discs, the steady connected robust hosting capacity is

\[
\Lambda_{\rm conn}(\mathbf g)=
\sup\{L\ge0:\ [0,L]\times\mathcal U\text{ satisfies every power-flow, voltage,
current, and inverter-capability constraint on the selected normal branch}\}.
\]

The **physical** capacity-oriented coordinated control problem is
\[
\boxed{\max_{\mathbf g\in[0,4]^4}\Lambda_{\rm conn}(\mathbf g).}
\]

This is an **offline gain-design problem**. It is not real-time charge scheduling, small-signal/dynamic stability synthesis, or a claim of all-time disturbance rejection.

## 2. What A actually provides for this optimization

On an interval \(I=[a,b]\) with no inverter Q saturation *for every input* in that cell, use the already developed **nonlinear closed-loop state inclusion**, the separated load/uncertainty **block-Hessian voltage bound**, and the analytic **phasor geometric line-current upper bound**. Enforce the **correlated total PV apparent-power cap** \(P_j^2+Q_j^2\le S_j^2\) on the entire original cell, not merely a favorable midpoint. Taking the connected union of all accepted load subintervals from zero gives \(C_H(\mathbf g)\), a **conservative candidate inner capacity**.

The mathematical implication \(C_H(\mathbf g)\le \Lambda_{\rm conn}(\mathbf g)\) is valid when **all state/derivative/phasor majorants used by A are rigorously enclosed**. The present 33-bus implementation evaluates most of them in **ordinary double precision**, so its reported numerical \(C_H\) values are not yet validated rigorous lower bounds. Additionally, \(C_H\) may be smaller than physical hosting capacity when the Q capability constraint clips.

Thus the practical first experiment is **maximize the computed inner candidate \(C_H\)** and separately test the physical clipped-controller outputs. This is NOT the same as establishing the globally optimal \(\mathbf g\) for the physical problem.

## 3. Numerical observation: coordination improves the inner capacity by 7.34%

Everything except four gains is held fixed: MATPOWER case33bw 32 in-service lines; 10 MVA/12.66 kV bases; base loads multiplied by 0.65; four PVs at buses 9,18,24,33, each with \(P_0=0.25\) MW, independent right-half-disc \((w_p,w_q)\) of radius 0.125 MVA, apparent power limit \(S=1\) MVA; increment of unity-power-factor load at bus 18. Study security: \(0.95\le V\le1.05\) pu and common \(I\le0.31\) pu. That current threshold is **research-assumed, not actual line-specific ratings**.

| PV gains (9,18,24,33) | Connected inner \(C_H\), FLOAT MW | First tested physically clipped unsafe crossing, FLOAT MW |
|---|---:|---:|
| (1.92,1.92,1.92,1.92) | 1.0586 | 1.0922197 |
| (3.50,1.92,1.92,1.92) | 1.1229 | 1.1635709 |
| **(3.70,1.92,2.12,2.52)** | **1.1363** | **1.1780523** |

Observed improvement in **candidate inner capacity**, not proven true optimal hosting capacity:
\[
1.1363-1.0586=0.0777\ {\rm MW}=77.7\ {\rm kW},
\qquad \frac{0.0777}{1.0586}\approx7.34\%.
\]

The design was found by a modest local coordinate/gain sweep, NOT global optimization. Uniform scalar gains of 1.92 still match exactly between the new four-vector code path and old scalar code path in finite-precision regression. 140 sampled nonlinear physical clipped-controller power flows around load 1.10–1.105 MW were safe under the coordinated setting; these samples do **not** replace the all-uncertainty upper-envelope calculation.

Why it helped: raising the bus-9 gain reduces the robust full-PV apparent-power upper bound required at the heavily loaded bus 18, relieving a bottleneck, but very high bus-9 gain eventually triggers another capability bottleneck. Different gains at 24 and 33 help the coordination. The numerical inner objective is not monotone in any of the gains.

## 4. Interval-verified physical unsafe upper obstruction for the new setting

For the exact finite-decimal model, fix
\[
\mathbf g=(3.70,1.92,2.12,2.52),\quad
\lambda=1.1795\ {\rm MW},\quad
(w_{p,j},w_{q,j})=(0,-0.0125)\ \text{pu}\quad(j=9,18,24,33).
\]
These are all feasible right-half-disc disturbances. The independent script \`verify_joint_witness_interval.py\` constructs a 64-dimensional closed state box with radius \(10^{-6}\), verifies the **physical** Q clip mode (all four strictly **unsaturated** throughout that specific box), and uses 60-decimal-digit interval evaluations with exact rational comparisons of interval endpoints to check the preconditioned Banach self-mapping and contraction bounds:

\[
\rho_\infty < 1.956\cdot10^{-4}<1,\qquad
\|PF(\widehat z)\|_\infty+\rho_\infty10^{-6}<10^{-6}.
\]

It then proves the **actual box-contained root** violates the bus-18 lower voltage bound:
\[
0.9499459222948 < V_{18} < 0.9499469749858<0.95.
\]

This gives the correct non-strict upper obstruction
\[
\Lambda_{\rm conn}(\mathbf g_{\rm new})\le1.1795\ {\rm MW}
\]
for the intended normal-operation branch. It proves local existence/uniqueness within the box, not uniqueness of every possible physical AC power-flow root or robust infeasibility of every larger isolated load.

## 5. Key next proof: certify a positive PHYSICAL gain, not only optimize conservative margins

Prior note 18 interval-verified that \(\mathbf g_{\rm old}=(1.92,1.92,1.92,1.92)\) has a physically feasible voltage-violating disturbance at \(1.09322\) MW, so

\[
\Lambda_{\rm conn}(\mathbf g_{\rm old})\le1.09322\ {\rm MW}.
\]

The new **float** safe-inner candidate reaches 1.1363 MW, above that *rigorous* old upper obstruction. A rigorous **all-uncertainty safe-prefix inclusion only through 1.10 MW** for the new gains would already give

\[
\Lambda_{\rm conn}(\mathbf g_{\rm new})\ge1.10>
1.09322\ge\Lambda_{\rm conn}(\mathbf g_{\rm old}),
\]

thus proving a physical control improvement of at least 6.78 kW. Certifying the entire candidate 1.1363 MW would raise that provable improvement to at least 43.08 kW.

**At present neither lower-side statement has been formally proved.** They are concrete next proof targets, not current results. Instead of proposing fresh mathematics, prioritize outward-rounded state inclusion, block-Hessian/phasor/PV envelope and connected safety for \([0,1.10]\times\mathcal U\) at the candidate gains.

## 6. Code and limitations

The independently runnable experiment archive (with the old 33-bus Python dependency closure) contains:
- Modified \`safe_load_capacity.py\` to accept scalar or buswise 4-vector gains.
- Modified \`hessian_phasor_capacity.py\` to use each bus's own gain in the *existing* full PV capability envelope.
- Modified \`saturated_capacity_witnesses.py\` to use the physical clipped law with bus-specific gains.
- \`optimize_individual_gains.py\` for a transparent, **finite set** of gain choices, connected capacity evaluation from zero, and five feasible-disturbance physical witness probes.
- \`test_joint_gain.py\` backward compatibility and physical-solve sample regression.
- \`verify_joint_witness_interval.py\` interval certificate for the explicit selected upper witness.
- \`coordinated_gain_optimization_results.json\` and \`joint_witness_interval.log\`.

The source archive is downloadable in the conversation, but the restored experiment dependency tree is **not yet in this GitHub PR**. Hence these numerical experiments are not currently independently runnable solely by cloning this PR. The PR remains a mathematical research record and must not be presented as self-contained validated IEEE33 code.

Next tasks: **(1)** import full source dependency tree to PR; **(2)** outward-rounded all-input safe inner through 1.10 MW; **(3)** then decide whether to tighten the final 1.1363–1.1795 MW bracket or attempt global gain optimality. Dynamic inverter stability, actual thermal ratings, and hardware implementation are outside this steady-only study.
