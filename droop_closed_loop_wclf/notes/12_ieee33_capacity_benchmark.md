# IEEE 33-bus capacity-control benchmark — 2026-10-13

This experiment restores the project's main engineering objective: **how much added flexible load may be hosted, where the binding robust safety limit lies, and how fast that load may safely ramp with inverter dynamics?**

## 1. Feeder and operating assumptions

Use the active 32 radial branches from the MATPOWER case33bw system, 12.66 kV and 10 MVA base. Scale base P,Q demand by 0.65. Four PV inverters at buses 9,18,24,33 inject 0.25 MW base active power each with *independent right-half-disc* uncertainty radius 0.125 MVA each. Each inverter has S=1 MVA; for the unsaturated Q/V control, enforce reactive reserve based on the worst possible active PV power (0.375 MW). Add unity-power-factor flexible load lambda MW at bus 18.

Assumed network voltage limits [0.95,1.05] pu and **research-assumed** common current limit 0.31 pu. This 0.31 pu is not a MATPOWER line-by-line thermal nameplate.

Take all active inverter voltage-magnitude gains equal to g in {1,1.5,1.85,2,3}.

## 2. What was actually checked

The baseline uses a conventional finite-radius fixed-point enclosure for the nonlinear radial DistFlow *algebraic droop feedback*. A second baseline applies the signed-interval plus half-disc/geometric current contractor **at each load point**. The new fixed-g study uses a simultaneous state/parameter enclosure over a load subinterval [lo,hi], then an implicit-function Hessian matrix majorant with variable ordering

$$t=(\lambda,w_{p,9},w_{q,9},w_{p,18},w_{q,18},w_{p,24},w_{q,24},w_{p,33},w_{q,33}).$$

For the full parameter Jacobian J=F_z and P=J0^-1, use componentwise |J-J0|<=E. In **real arithmetic**, if rho(|P|E)<1, then

$$
|J^{-1}|\le (I-|P|E)^{-1}|P|.
$$

Apply this inverse majorant to the complete second-order residual from notes 06 and 09 to enclose each Hessian entry for every squared-voltage and squared-line-current safety constraint. A small addition to the PV half-disc at bus 18 conservatively encloses the load **interval** without pretending intermediate levels have been checked pointwise.

Two Taylor inner bounds are compared:
- **isotropic**: one full joint operator-Hessian norm M for (lambda,w);
- **block**: separate B_lambda-lambda, B_lambda-w, B_w-w upper norms, retaining the lambda/w structure (note 10).

Voltage, line-square-current and active-power-dependent inverter Q reserve constraints are all included. PV Q capacity is handled as an equivalent squared-voltage inequality on the unsaturated branch, rather than rejecting a region only because a broad auxiliary state box crosses the Q limit.

Important: these are **ordinary floating-point checks** of conditions that would certify the result under exact arithmetic. No outward rounding was used, so these numbers are **not formal computer-assisted safety proofs**.

## 3. Measured capacity results (MW)

Each continuous-inner method covers real values in its accepted subinterval, not merely 0.02 MW grid points. 'Continuous' below means the linked union of accepted subintervals starting at lambda=0; a gap interrupts the continuous feasible path.

| Gain g | Isotropic Hessian connected prefix | Block Hessian connected prefix | Largest passing *point* on contractor's 0.02 MW grid |
|---:|---:|---:|---:|
|1.00|0.677886|0.678910|0.68|
|1.50|0.893239|0.893341|0.90|
|1.85|0.999800|1.032555|1.04|
|2.00|0.960000|0.992980|1.00|
|3.00|0.739580|0.780000|0.84|

At g=1.85 the isotropic Hessian leaves two gaps between nearby individually certified segments, while the block Hessian covers the full [0,1.032555] MW interval in the numerical certificate. At g=2, the improvement of connected coverage is about 3.4%; at g=3 about 5.5%.

At g=1.85 the *limiting certificate near maximal continuously safe load* is undervoltage at bus 18. At g=2 it is inverter reactive-power headroom at bus 18. At g=3 the most limiting near the disconnected highest safe inner segment is overcurrent on the first feeder line; do **not** conflate the highest isolated safe point with a contiguous safe load ramp.

Crucially: this new local quadratic certificate **did not exceed** the best previously tested pointwise nonlinear geometric interval contractor in maximal capacity. Its observed advantage is continuous-interval coverage.

Random perturbation power-flow sampling (400 fixed-load scenarios per gain) found no violating solution at 0.005 MW below the highest reported block safe **point**. Such sampling is not a global optimization or rigorous proof.

## 4. A dynamic surprise

For a separate **quasi-static power-flow plus first-order inverter response** model
$$
\tau_i\dot q_i=-q_i+g_i(1-V_i),\quad\tau_i=10{\rm s},
$$
simulate bus-18 loading from 0 to 1.03 MW under one *fixed* PV disturbance at all four inverters: delta p_i=0, delta q_i=-0.125 MVA. Use Euler time step 0.5 s and solve the nonlinear radial power flow with actual physical q_i at every step.

| Load ramp duration | Minimum voltage through response | Observed voltage below 0.95? |
|---:|---:|:---:|
| step (0 s) | 0.906914 | yes |
| 10 s | 0.933334 | yes |
| 60 s | 0.947836 | yes |
| 180 s | 0.950141 | no |
| 300 s | 0.950607 | no |

Results at Euler dt=0.1 s agree within 2.4e-4 pu for 10 s, ~3e-6 pu for 60 s and ~3e-7 pu for 180 s. The 300 s case is only an **observed safe trajectory for one fixed disturbance** and not an all-time robust certificate. This demonstrates why quasi-static connected hosting intervals must **not** be advertised as dynamically safe ramps.

## 5. Interpretation and next proof

1. A practical mathematical improvement exists: structured Hessian preserves connected coverage, and the common-gain optimum over tested values is near g=1.85.
2. We do not yet know that 1.032555 MW is physically maximal or formally machine-certified. Do not confuse inability to certify with true unsafe operation.
3. The next relevant theorem is a *joint* capacity/rate certificate: an interval-verified steady hosting region plus a forward-invariant inverter reactive-state tube, yielding a safe ramp-speed formula. Notes 11 provides conditional theory; verifying its constants on IEEE 33 is still open.
4. To improve absolute capacity, preserve half-disc geometry in the **joint load interval** instead of the current enlarged-half-disc superset; use rowwise rather than global operator Hessian bounds.
5. Need formal outward rounding, actual PV Q/P coupling, and line-specific thermal ratings before engineering deployment or publication claims.

## 6. Reproducibility

The full research-session numerical source package (including the prior interval prototype, 33-bus input, block-Hessian computation, 5-gain benchmark, random derivative checks, and the time-domain demonstrator) has been generated as a downloadable conversation artifact. The main GitHub PR includes the mathematical framework and this benchmark record; the complete session dependency scripts require an additional import and independent CI run before being treated as repository-verified regression tests.

MATPOWER reference case: https://github.com/MATPOWER/matpower/blob/master/data/case33bw.m
