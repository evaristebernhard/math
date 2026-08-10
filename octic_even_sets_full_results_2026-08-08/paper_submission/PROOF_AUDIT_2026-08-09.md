# 投稿稿整篇证明审计（2026-08-09）

本文件 **取代 `PROOF_AUDIT_2026-08-08.md` 作为当前投稿状态的权威审计**。旧审计保留为历史记录，但其中关于 Endraß 禁重、residual-32 split-MacWilliams closure、general `k=1` closure 等后来被纠正的判断不得继续作为当前依据。

状态约定：

- **GREEN**：当前 `main.tex` 的 theorem statement 与 proof 已匹配，可作为投稿结果；
- **YELLOW**：有实质归约，但仍保留显式 outlet，正文不得写成 closure；
- **SUPPLEMENTARY**：研究证明保留，但已从投稿 PDF 主线移出；
- **REVOKED**：旧版本中过度宣称或依赖错误输入的路线，当前不得引用为无条件结论。

---

## 1. Uniform shortening 与 low-weight trichotomy — GREEN

当前 shortening lemma 已包含必要条件
\[
\dim D\le19,
\qquad
|\operatorname{supp}(D)|\le104.
\]
由 Beauville--Endraß 维数输入、shortening 与 Griesmer，hypothetical high-node octic 的 strict minimum distance 只需考虑
\[
48,\quad64,\quad72.
\]
正文现统一在复数域上工作，避免把 Endraß / topological inputs 误写成任意特征 `!=2` 的结论。

## 2. Minimum-distance 72 branch — GREEN

当前 theorem 只声称
\[
\boxed{d(K)\ne72},
\]
即排除 minimum-distance-72 branch；不声称所有其他 branch 中的 weight-72 words 不存在。

Residual injection、61-state exact certificate 与 MacWilliams average 均在正文完整给出，有限整数表在 appendix。

## 3. Universal weight-64 determinant presentation — GREEN

正文已恢复 Riemann--Roch / stability / instability 的关键步骤，并证明任意 strict weight-64 even set（不要求 global minimum 为64）都是 reduced transverse
\[
CI(4,4,4),
\qquad
F=q_0q_2-q_1^2.
\]
该 theorem 是论文最强的几何输入之一。

## 4. Minimum-64 first residual — GREEN

对固定 weight-64 minimum word：
\[
R=[105,18],\qquad R\text{ is 4-divisible},\qquad d(R)\in\{32,36,40\}.
\]
正文完整给出 degree-5 Krawtchouk certificate 与四个 local lift profiles `32/36/40A/40B`。

40A/40B 只作为 local profiles；不再承担全局分支逻辑。

## 5. `A64>=533`、incidence 与 global 32/36 reduction — GREEN

精确 LP identity 给
\[
A_{64}\ge533
\]
（dimension at least 20 时 `A64>=2353`）。Incidence convexity 的整数计算完整在正文中，强迫可选择一个 base word 使
\[
\boxed{d(\operatorname{Res}(C;c))\in\{32,36\}}.
\]
该归约不依赖旧 residual-intersection strengthening。

## 6. Residual-32 split compensation — GREEN，closure — NO

完整 octic weight spectrum 下的 exact split-MacWilliams certificates 已验证：
\[
A_{88}+A_{96}\ge65,
\qquad
A_{88}+3A_{96}\ge185.
\]
若无一个 nonzero `H`-coset 同时混合 weight64 与 weight88/96，则
\[
A_{88}+A_{96}\ge471.
\]
这些是无条件 compensation theorems，但 **不排除 residual triangle**。

## 7. Residual-32 geometry — mixed GREEN/YELLOW

### GREEN

- common-pencil bound
  \[
  k=\dim(V_{AB}\cap V_{AC})\le1;
  \]
- plane carrier exclusion；
- quadratic carrier exclusion；
- 全部 quartic defect `delta=2` cubic / primitive candidates closed；
- associated Hilbert/liaison calculations are reproduced by submission tests.

### GREEN: general `k=1` completely excluded

2026-08-09 的进一步 transversality/UFD 审计闭合了此前残留的 plane--cubic 与 nonreduced outlets。当前正文 Proposition `Exclusion of the k=1 comparison` 处理全部三种 isotropy type：

- both non-isotropic：rank bound 先给 product equality；UFD 写成
  \[
  u_1=ab,\quad u_2=cd,\quad v_1=ac,\quad v_2=bd.
  \]
  Transversality 强迫两个 carrier pieces 不相交并分别为 reduced complete intersections，故
  \[
  32\ge4(\alpha^2+\beta^2),\qquad \alpha+\beta=4,
  \]
  只可能 \(\alpha=\beta=2\)。随后四个 quadratic factors 都是 contact quadrics；reduced 情形产生 forbidden strict weight48，全部 double-plane 情形则由 weak-28 symmetric difference / net-dimension collapse 排除；
- mixed isotropic/non-isotropic：difference relation rank5，矛盾；
- both isotropic：由
  \[
  (v-v')(v+v')=q(u'-u)
  \]
  先用 transverse \(CI(q,u,v)\) 证明 \(q\) squarefree；若 \(q\) 的 irreducible factors 分配到等式左侧两个因子的两边，则在交曲线上 \(dq=0\)，再取 \(u=0\) 的点得到 first-jet rank 至多2，矛盾；若全部 factors 落在同一边，则 degree4 强迫 \(q\mid v\pm v'\)，进而两个 determinant nets 相同，矛盾。

因此
\[
\boxed{k=1\text{ impossible}},
\qquad
\boxed{V_{AB}\cap V_{AC}=0}.
\]
Residual-32 triangle 现只剩 \(k=0\) six-quartic comparison。

### YELLOW: `k=0`

Six-quartic / low-rank quadric-pencil / relative-contact compatibility remains open.  The desmic/quadratic-cover analysis remains research material, not a submission theorem.

## 8. Residual-36 global six-quartic theorem — GREEN with explicit hypotheses

2026-08-09 新增正式 theorem：若 residual-36 的两个 determinant nets disjoint，则在
\[
Y=\operatorname{Bl}_A\mathbf P^3,
\qquad |A|=28,
\qquad D=4H-\sum E_a
\]
上六 quartics 定义 generically finite map 到 smooth quadric fourfold。正文证明
\[
D^3=36,
\qquad
K_YD^2=-8,
\qquad
g(D^2)=33,
\qquad
me=18.
\]
Normal target 情形由 Riemann--Hurwitz 强迫
\[
\boxed{(m,e)=(2,9)\text{ or }(3,6)}.
\]

### finite normal `(2,9)` target — GREEN, completely excluded

在 normal finite quadratic-target 情形，28 个 exceptional planes 迫使 quadric pencil 出现 rank \(\le4\) member。这里特别撤回早期对 rank3 singular conic 直接使用 degree-9 特殊 fibre bound 的做法：finite map 在 codimension-two singular locus 上未必 flat。当前正文改用 self-adjoint Jordan classification，并且所有 sheet count 都只放在 target 的 generic-smooth plane/line 上。rank3 的五种可能型为 `(2,1,1)+(2)`, `(2,1,1)+(1,1)`, `(4,1,1)`, `(3,2,1)`, `(2,2,2)`；前四型由 invariant-Lagrangian 数量/两条 smooth-line pairing 排除，最后一型给 codimension-one singular plane，违反 normality。rank4 时先得到 radical line \(L\subset X'\)。进一步令 \(T=B_0^{-1}B_1\)，并利用 \(L\subset Q_0\) 得到二维 eigenspace \(K\) 对 \(B_0\) 完全 isotropic。Self-adjoint primary decomposition 将 rank4 可能 Jordan 型压到四种：
\[
(J_2,J_2)_\lambda+(J_2)_\mu,\quad
(J_2,J_2)_\lambda+(J_1,J_1)_\mu,\quad
(J_2,J_4)_\lambda,\quad
(J_3,J_3)_\lambda.
\]
四型的 invariant Lagrangian planes 均可显式列出。若两张 common planes 沿 generic-smooth line 相交，则在该 line 的 generic point target local ring regular、source Cohen--Macaulay，finite map 因而 flat of rank9；故对应 exceptional-plane multiplicities 满足
\[
n_i+n_j\le9.
\]
前三/第四型分别给总数上界18、27、18、18；最临界的六-plane 型恰有
\[
2\sum n_i\le54\Longrightarrow\sum n_i\le27<28.
\]
因此
\[
\boxed{(m,e)=(2,9),\ X'\text{ normal},\ \phi\text{ finite}\Longrightarrow\bot}.
\]
该证明不依赖 clean `(1,3)/(2,2)` carrier 假设。

### finite `(3,6)` + isolated target singularities — GREEN

Finite-map canonical formula + effectiveness + `H^2` degree argument给出
\[
R_\phi=\sum_{a\in A}E_a.
\]
General hyperplane section target 是 smooth `(2,3)` K3，Euler number24；source 是 quartic K3 blow-up 28 points，Euler number52。Simple ramification stratification would give
\[
6\cdot24-28\cdot2=88,
\]
contradiction。正文已补充 branch-line 交点时 fiber defects additive 的说明。

### Remaining residual-36 outlets — YELLOW

- normal finite cubic target with positive-dimensional singular locus；
- nonfinite maps / divisorial contractions；
- nonnormal targets。

所以 finite normal quadratic branch 已真正闭合；residual-36 仍未整体闭合。

## 9. J1/J2 canonical-module / orientation defect — GREEN

J1 exact sequences and Ext/Matlis argument are in正文；J2 explicitly assumes the residual degree-8 relation and only concludes
\[
(Q_A)_8\ne0.
\]
It is correctly warned that this does **not** imply automatic defect in degree `<=3`.

## 10. Coupled Beilinson--Horrocks obstruction — GREEN as standalone theorem

正文只声称 genuinely coupled degree-0/1 Horrocks block impossible。它不再被描述为 exhaustive regular comparison closure。

## 11. QT / Smith chain — SUPPLEMENTARY

Full source is preserved inside `main.tex` under `\iffalse...\fi`, so it is omitted from compiled submission PDF without deleting the research proof.

Current status is recorded in
`SUPPLEMENTARY_QT_SMITH_STATUS_2026-08-09.md`.

It must not be cited as unconditional residual-36 closure.

## 12. Minimum-distance 48 first residual — GREEN

正文无条件证明
\[
R=[121,18],
\qquad
24\le d(R)\le48,
\]
and lists the ten correct lift profiles allowing weight72 and the full strict octic spectrum.

## 13. `48/64` global trade-off and pair thresholds — GREEN

Exact identity gives
\[
\boxed{A_{64}+21A_{48}\ge533}.
\]
Incidence consequences currently in正文 are supported by exact arithmetic:

- `A48>=22` -> two weight48 words meet in16 or24；
- `18<=A48<=21` -> two weight64 words meet in24/28/32/40；
- `A48<=17` -> two weight64 words meet in28/32/40。

Every appearing weight64 word has the universal determinant structure.

## 14. Contact-quadric intersection theorem — GREEN

For two distinct strict weight48 sets with reduced contact quadrics having no common plane component,
\[
|W\cap W'|\le16.
\]
The proof correctly uses quartic root `A` on ordinary components and sextic residual `B` on repeated components; the earlier erroneous cubic count is absent.

## 15. Weight48 B16/B24/A32/A40 atoms — YELLOW / research only

The recent atom compression and contact-factor normal forms are mathematically useful but do not yet eliminate the core atoms.  They remain outside submission `main.tex`.

Likewise weight48 second/third residual experiments are separated into `npm run test:research` and are not submission theorem inputs.

## 16. REVOKED / forbidden claims

The following must not re-enter the paper:

1. `A88=A96=A104=A112=0` as an octic Endraß input；
2. unconditional residual-32 closure from the legacy split certificate；
3. “minimum-distance 72 excluded” interpreted as “all weight72 words excluded”；
4. the obsolete claim that general residual-32 `k=1` has a surviving plane--cubic outlet；the new transversality/UFD proof closes `k=1` completely；
5. residual-36 full closure；
6. weight48 second/third residual claims that depend on hidden spectrum assumptions；
7. final maximal-node theorem `u(8)<=168`。

## 17. Submission organization audit

The compiled submission now omits the long conditional QT/Smith section and the historical `Audit boundaries` appendix.  Internal project-management language was removed from Abstract/Introduction/Remaining outlets.  `SCOPE.md` has been rewritten to the 2026-08-09 status.

Author metadata is now:

- **Jizheng Chen**, Chang'an University, Xi'an, China — `1253183582@qq.com`
- **Chaoyu Hu**, Hangzhou Dianzi University, Hangzhou, China — `evaristebernhardwiener@gmail.com`
- **Corresponding author:** Chaoyu Hu

## 18. Verification status

Submission test semantics were separated:

- `npm test` = submission-relevant static and exact certificates；
- `npm run test:research` = submission tests plus additional research-only weight48 residual experiments；
- `npm run build` = forced `latexmk -g` rebuild。

After the later proof-presentation and submission edits, the submission tests and forced LaTeX build were rerun successfully.  The current page count should be read from the latest build rather than this historical audit entry.

## Final assessment

The current manuscript proves the following submission-level results; it does not prove `u(8)<=168` and no claim of a general structural theory is intended:

\[
\boxed{
\begin{array}{l}
\text{minimum-distance 72 excluded};\\
\text{universal strict-64 symmetric }CI(4,4,4);\\
A_{64}\ge533\text{ and global residual }32/36;\\
\text{residual-32 compensation and complete }k=1\text{ exclusion};\\
\text{residual-36 six-quartic reduction, complete finite-normal }(2,9)\text{ exclusion, and cubic-target obstruction};\\
A_{64}+21A_{48}\ge533\text{ and contact-quadric incidence control}.
\end{array}}
\]

The remaining gaps are stated explicitly rather than hidden in theorem language.
