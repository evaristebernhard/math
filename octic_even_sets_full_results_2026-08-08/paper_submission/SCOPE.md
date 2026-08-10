# 单篇投稿的取舍原则（2026-08-09 投稿审计版）

目标：主稿是一篇关于 nodal octic 低重量 even sets 的结构论文，而不是未完成的 `u(8)\le168` 证明日志。正文只保留无条件结果或假设完全显式的定理。

## 投稿正文主线

1. Beauville--Endraß 维数输入、shortening 与 Griesmer：高节点情形只需考虑 minimum distance
   \[
   48,\ 64,\ 72.
   \]
2. **minimum-distance 72 branch**：由精确五阶 Krawtchouk--MacWilliams certificate 完全排除。该结论只排除 `d(K)=72`，不排除其他 minimum branch 中出现 weight-72 words。
3. **weight 64 universal geometry**：任意 strict weight-64 even set（不要求 global minimum 为64）都给出 reduced transverse
   \[
   CI(4,4,4),\qquad F=q_0q_2-q_1^2.
   \]
4. **minimum 64 coding abundance**：
   \[
   A_{64}\ge533
   \]
   （维数至少20时 `A64>=2353`），并由 incidence convexity 无条件选择 base word 使 first residual distance 为
   \[
   32\quad\text{或}\quad36.
   \]
   因此 local `40A/40B` 不承担全局逻辑。
5. **residual 32 triangle**：
   - common-pencil bound `k<=1` 已证明；
   - 完整重量谱上的 split-MacWilliams compensation 已证明：
     \[
     A_{88}+A_{96}\ge65,\qquad A_{88}+3A_{96}\ge185,
     \]
     并有 mixed-coset / `>=471` dichotomy；
   - plane、quadratic carrier 与全部 `delta=2` candidates 已闭合；
   - 一般 `k=1` 已由 transversality + UFD 完整排除，不再存在 plane--cubic outlet；
   - 因而 residual-32 只剩 `k=0` six-quartic / low-rank compatibility。
6. **residual 36 global map**：若两 determinant nets disjoint，六 quartics 在 `Bl_A P^3`, `|A|=28` 上定义 generically finite map 到 smooth `Q^4`。有
   \[
   D^3=36,\qquad g(D^2)=33,\qquad me=18.
   \]
   normal target 强迫
   \[
   (m,e)=(2,9)\quad\text{or}\quad(3,6).
   \]
   finite normal `(2,9)` 已由 self-adjoint Jordan 四型 + smooth-line degree-9 sheet count 完全排除；最临界的六-plane Jordan 型给出 `2Σn_i<=54`，故至多27张 exceptional planes，与28矛盾。finite `(3,6)` + isolated target singularities 由 K3 hyperplane-section Euler contradiction 排除。因此 finite normal residual-36 target 若存在，只能是 cubic target with singular curve；其余剩余为 nonfinite 或 nonnormal target。
7. **local comparison tools**：J1 canonical-module gluing、J2 degree-8 orientation defect、coupled Beilinson--Horrocks obstruction 保留为独立结构结果；不宣称 Horrocks outlets exhaustively classified。
8. **minimum 48**：无条件 first residual
   \[
   R=[121,18],\qquad24\le d(R)\le48,
   \]
   十个 lift profiles；全局精确 trade-off
   \[
   A_{64}+21A_{48}\ge533;
   \]
   incidence 给出高 `A48` 时 48/48 intersection `16` or `24`，低 `A48` 时强迫 64/64 overlap；两 distinct weight-48 contact quadrics 无 common plane component 时 intersection `<=16`。

## 投稿正文明确不宣称

- 不宣称最终 maximal-node bound `u(8)<=168`。
- 不把 minimum-distance-72 theorem 当作“所有 72-word 都不存在”。
- residual-32 general `k=1` 已完全排除；当前只不宣称 `k=0` 已闭合。
- 不宣称 residual-36 已闭合；finite cubic target with singular curve、nonfinite 与 nonnormal target 仍开放，但 finite normal `(2,9)` 已闭合。
- 不宣称 weight-48 的 B16/B24/A32/A40 atoms 已闭合。
- 不把 weight-48 second/third residual 中依赖额外谱假设的计算当作投稿无条件定理。

## 从投稿 PDF 移出的内容

以下内容保留在研究源码/Markdown，但不进入投稿 PDF 主线：

- conditional QT-lift / normal-nodal Smith-carrier chain；
- Jacobian--defect lattice 的一般理论、Gram circuit 分类、hidden defect；
- Artin--Mumford detector 的失败路线；
- weight-48 B16/B24 最新 contact-factor 分类；
- residual-32 desmic/quadratic-cover 深层研究；
- 依赖额外 `A72=0` 等假设的 second/third residual experiments。

## 验证命令语义

- `npm test`：只验证投稿正文实际使用的静态 TeX 与 exact certificates。
- `npm run test:research`：在投稿测试基础上额外运行未进正文的 weight-48 residual experiments。
- `npm run build`：强制 `latexmk -g` 重建投稿 PDF。

## 当前投稿定位

最合适的叙事是：

> high-node octics force a small low-weight coding spectrum; weight 64 automatically carries symmetric determinant geometry; coding abundance forces many simultaneous presentations; residual 32/36 are then compressed by global comparison geometry; minimum 48 is controlled by an exact 48/64 trade-off and contact-quadric incidence.

这是一篇结构/归约论文，而不是最终 `u(8)` 闭合论文。
