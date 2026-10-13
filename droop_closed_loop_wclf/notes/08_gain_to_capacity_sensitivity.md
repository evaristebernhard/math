# From worst-case-current certificates to optimizing inverter gain for hosting capacity

This note deliberately keeps **hosting-capacity control** as the primary objective. Gain derivatives are not novel by themselves; their purpose is to offer a mathematically grounded way to choose which inverter to adjust and how much.

## 1. Closed-loop gain sensitivity

Fix the flexible-load size lambda, disturbance w and a differentiable unsaturated Q/V droop branch. The steady-state residual F(z,w,lambda,g)=0 is defined in note 06, with
$$q=q^0-\lambda e+w_q-\operatorname{diag}(g)(\sqrt\nu-V^{ref}).$$
At fixed z, differentiating with respect to one gain g_j gives
$$
\frac{\partial q}{\partial g_j}=-(\sqrt{\nu_j}-V_j^{ref})e_j.
$$
Using F_1=nu-nu_s*1-2Rp-2Xq-Mell and F_2=ell-(a^2+b^2)/nu with b=Dq-H_x ell,
$$
\boxed{
F_{g_j}=
2(\sqrt{\nu_j}-V_j^{ref})
\begin{bmatrix}
X_{:,j}\\
\operatorname{diag}(b/\nu)D_{:,j}
\end{bmatrix}.
}
$$
The full steady-state sensitivity is
$$
\boxed{z_{g_j}=-F_z^{-1}F_{g_j}.}
$$
This includes the implicit change of current losses and all other nodal voltages. A numeric example on a one-line feeder with R=.05, X=.03, g=2 and load lambda=.05 gives d(nu,ell)/dg approximately (+0.00045697,-0.00076229). Centered finite differences agree to the displayed precision.

## 2. Envelope theorem for worst-case thermal margins

Let for line l
$$
m_l(\lambda,g)=\max_{w\in\mathcal U}\ell_l(\lambda,g,w)
$$
and thermal safety condition m_l<=ell_l^rated. Under compact uncertainty set, continuous normal-branch solutions, and a **unique interior/suitable constrained** maximizing disturbance w_l* at the considered lambda,g, the value function is differentiable (assuming standard regularity), with
$$
\partial_\lambda m_l=\partial_\lambda\ell_l(\lambda,g,w_l^*),
\quad
\partial_{g_j}m_l=\partial_{g_j}\ell_l(\lambda,g,w_l^*).
$$
Derivatives on the right follow from -F_z^{-1}F_lambda and -F_z^{-1}F_gj. If the maximizer is not unique, use directional-derivative/Danskin active-maximizer sets rather than treating a single gradient as exact.

## 3. Which inverter best releases capacity?

Suppose a unique limiting constraint is \psi(\lambda,g)=m_l(\lambda,g)-ell_l^rated=0 at a locally active capacity limit lambda*(g). If \partial_lambda\psi>0 and all other constraints have slack, the implicit function theorem gives
$$
\boxed{
\frac{\partial\lambda^*}{\partial g_j}
=-\frac{\partial_{g_j}m_l}{\partial_\lambda m_l}.
}
$$
Positive derivative predicts increasing gain g_j may free hosting capacity locally; negative predicts it may reduce hosting capacity.

For a *binding undervoltage* constraint define
$$\psi_i^{low}=\nu_i^{min}-\min_w\nu_i,$$
and for overvoltage
$$\psi_i^{high}=\max_w\nu_i-\nu_i^{max}.$$
The same local sensitivity formula applies to whichever unique constraint is active, with correct minimum/maximum envelope derivatives.

These sensitivities are **local**: multiple active limits, discrete controller modes, saturation, nonunique worst-case disturbances, and disconnected feasible capacity sets can invalidate a smooth global capacity derivative. In those cases use certified envelopes and a nonsmooth/interval method.

## 4. What is the actual research objective?

Rather than minimizing the width of a worst-case current bound as an isolated benchmark, target
$$
\max_{\lambda,g}\ \lambda\quad
\text{subject to robust voltage, line thermal, inverter reserve and (eventually) dynamic constraints}.
$$
Use the certified current/voltage enclosures from notes 02, 06, and 07 as a feasibility oracle. The Hessian bound M from note 06 is needed to quantify how accurate the first-order worst-case predictor is, so that a candidate gain update cannot silently violate thermal/current limits.

Before proving global hosting optimality, establish: (i) a certified feasible lower bound in (lambda,g); (ii) upper exclusion certificates for other parameter regions; (iii) a sound search or a clearly labeled local optimizer. Merely grid-searching 10 gains is not a proof.

## 5. Research separation

- Established: symbolic formula for gain derivative under smooth unsaturated branch; conditional active-constraint sensitivity identity; explicit Hessian algebra and a two-node numerical consistency test.
- Not established: a globally optimal gain, verified IEEE-33-bus Hessian bounds, robust inverter saturation behavior, or continuous-time closed-loop safety during load ramps.
