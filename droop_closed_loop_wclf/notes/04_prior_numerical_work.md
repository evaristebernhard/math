# Previous numerical prototypes — historical, not recertified here

The earlier conversation developed several double-precision Python prototypes for:

- 3-bus Q/V feedback changing the sign of a bus-voltage response to another bus's active injection;
- an explicit Jacobian-deviation matrix L for a nonlinear closed-loop DistFlow residual;
- direct geometric bounds for line squared current using a half-disc/rectangle outer approximation;
- asymmetric interval refinements and affine complex-power sensitivity;
- a support-function reduction of the worst-case affine complex-power norm to one angular maximization.

### Selected previously reported observations

- In a 3-node radial toy model, the linearized sensitivity dV_1/dp_2 became negative under large local reactive droop gain.
- On a custom 33-node case derived from case33bw, one float-based state-box envelope reported max line current around 0.20831 pu; the affine complex-power bound reported around 0.16267 pu.
- An earlier custom hosting-capacity sweep reported improvement under tighter state bounds, but this was a one-direction, numerically searched, **algorithm-certified** capacity, not a proof of globally maximum hosting capacity.
- Independent random perturbations were used as cross-checks. Random samples do not prove absence of violations.

These results came from exploratory prototypes with specific custom gains and capacities. They are **not reproduced or independently verified by this commit**. In particular, neither directed-rounding interval arithmetic nor all inverter saturation regimes were implemented. Avoid using these numerical claims as certified theorem evidence.

The new dependency-free demonstration in code/cubic_demo.py serves a narrower purpose: test the cubic *rate* predicted by the conditional proposition on an explicit smooth nonzero-baseline polynomial. It is not an IEEE network test.

Original numerical prototype artifacts should only be imported in a later commit together with exact dependencies, source references, executable commands, and a test run; an incomplete script without its imported modules would be misleading.
