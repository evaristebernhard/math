# A two-segment closed-loop sensitivity sign reversal

Consider the linearized radial feeder 0--1--2 with positive segment resistances r1,r2 and reactances x1,x2. Write the nominal voltage-magnitude sensitivity as

$$
\Delta V=R\Delta p+X\Delta q,\quad
R=\begin{bmatrix}r_1&r_1\\r_1&r_1+r_2\end{bmatrix},\quad
X=\begin{bmatrix}x_1&x_1\\x_1&x_1+x_2\end{bmatrix}.
$$

Suppose only node 2 has unsaturated reactive droop \Delta q_2=-g\Delta V_2, g>=0. Then

$$
\Delta V=(I+X\operatorname{diag}(0,g))^{-1}R\Delta p,
$$

and direct inversion gives

$$
\boxed{\frac{\partial V_1}{\partial p_2}
=\frac{r_1+g(r_1x_2-x_1r_2)}
{1+g(x_1+x_2)}.}
$$

If x1*r2>r1*x2, the derivative changes sign when
$$g>g_{\rm crit}:=\frac{r_1}{x_1r_2-r_1x_2}.$$

For r1=.01, x1=.08, r2=.08, x2=.02, g=8, the derivative is -0.022, with g_crit approximately 1.6129. The negative sign means increasing node-2 net active injection can decrease node-1 voltage in this local linearized closed loop. Hence an open-loop voltage monotonicity endpoint rule must not be transferred blindly to droop feedback.

This is an elementary illustrative calculation, **not** a claim of novelty or a nonlinear all-network theorem. See code/feedback_sign_reversal.py for arithmetic reproduction.
