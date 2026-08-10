# JAG 投稿审计（准确状态版，2026-08-09）

对象：`paper_submission/main.tex` / 当前编译 PDF。

## 1. 总结

当前稿件包含一组关于八次节点曲面低重量 strict even sets 的已证明结果，并以极值问题
\[
u(8)=168?
\]
作为主要动机。稿件目前**不证明** `u(8) <= 168`，也不应把现有方法表述为一套已经建立的一般理论。

目前正文可以准确概括为：

- 用 8-divisible code、shortening、Griesmer 与 minimal-even-set 输入把高节点假设压到 minimum weight `48/64/72`；
- 排除 minimum-distance `72`；
- 对 strict weight `64` 得到 `CI(4,4,4)` 与 symmetric `2x2` determinant presentation；
- 在 minimum `64` 情形用精确 MacWilliams 计数得到 `A_64 >= 533`，并把全局比较压到 residual `32/36`；
- 对 residual `32` 排除 `k=1` comparison，但 `k=0` 仍开放；
- 对 residual `36` 建立 six-quartic map reduction，并排除 finite normal quadratic target 以及 finite cubic target with isolated singularities；
- 在 minimum `48` 情形得到 first-residual bound、`A_64+21A_48>=533` 与 contact-quadric intersection bound。

这些结果彼此相关，但目前没有证据支持把它们描述为“独立结构理论”“一般方法”或“可广泛迁移的框架”。论文应只陈述已经证明的 octic-specific 结论。

## 2. 当前已闭合结果

以下结果可按正文现有 hypotheses 作为 theorem-level 结论使用：

1. high-node reduction 中 minimum distance 只需考虑 `48,64,72`；
2. minimum-distance `72` branch 不可能；
3. 任意 strict weight-64 even set 是 reduced transverse `CI(4,4,4)`，并有
   \[
   F_8=q_0q_2-q_1^2;
   \]
4. minimum `64` 时 `A_64>=533`；
5. minimum `64` 时可选择 base word 使 first residual distance 为 `32` 或 `36`；
6. residual `32` 的 split-MacWilliams compensation inequalities；
7. residual `32` 的 common-pencil bound 与 `k=1` exclusion；
8. residual `36` disjoint-net 情形的 blow-up / six-quartic map reduction；
9. residual `36` finite normal `(m,e)=(2,9)` target exclusion；
10. residual `36` finite `(m,e)=(3,6)` target 在 target singularities isolated 时的 exclusion；
11. J1/J2 在正文明确 hypotheses 下的 degree-eight statements；
12. coupled degree-0/1 Beilinson--Horrocks obstruction，作为独立局部命题；
13. minimum `48` first residual 的 `24<=d(R)<=48`；
14. `A_64+21A_48>=533`；
15. reduced contact quadrics 无公共平面分量时的 intersection bound。

## 3. 明确仍开放的部分

正文必须继续明确保留：

- residual `32`, `k=0` six-quartic compatibility；
- residual `36` finite cubic target with positive-dimensional singular locus；
- residual `36` nonfinite maps；
- residual `36` nonnormal targets；
- weight `48` 的剩余 pair geometries；
- final `u(8)<=168`。

这些不是“技术细节待补”，而是当前数学上尚未完成的分支。

## 4. 关于论文定位的措辞

不建议使用：

- `a new theory of octic strict even sets`；
- `an independent structural theory`；
- `a general framework`；
- `a broadly applicable method`；
- `a complete structural paper`，如果这句话容易让人误解 residual branches 已闭合；
- 把 `u(8)=168` 写成已基本解决。

更准确的表述是：

> The paper proves several results on low-weight strict even sets of nodes on octic surfaces, combining divisible-code constraints with symmetric determinantal and comparison arguments. The extremal problem `u(8)=168` is the main motivation, but the final upper bound is not proved.

这句话只概括正文实际做了什么，不声称一般性或超出已证明范围的创新层级。

## 5. 正文叙事审计

本轮已把 Introduction 中若干评价性措辞降为事实描述：

- `Our strongest geometric input` 改为 `A geometric input used repeatedly below`；
- `three different levels of rigidity` 改为 `three minimum-weight branches are treated by different mechanisms`；
- `isolate the remaining outlets after proving structural reductions` 改为 `records the proved reductions and keeps unresolved cases explicit`；
- `rigid geometric form` 改为 `specific geometric form`。

Abstract 当前也只列结果与开放状态，没有声称建立新理论。

## 6. Endraß 调用链

weight-64 determinant theorem 目前按原文逻辑拆开：

- Riemann--Roch 给 `chi(L)=4`；
- Serre duality + Endraß Lemma 4.1 给 `h^2(L)=h^0(L)`；
- Endraß Definition 3.1 / Proposition 3.3 使用的是 quadratic contact system 的 stable/semistable/unstable terminology；
- semistable degree-4 alternative 会强迫 reduced contact quadric，从 Proposition 3.8 得 weight 48，与 weight 64 矛盾；
- unstable case 使用 Proposition 3.6 的构造，在 `v=4,s=8` 时 `2v-s=0`，得到 nonzero constant coefficient 和 determinant identity。

因此正文不再把 Proposition 3.6 说成比原文更强的直接 statement。

## 7. residual-36 与 J2 的 proof-presentation 状态

此前两个压缩过快的位置已经补成正文可检查的证明：

- rank-three self-adjoint Jordan types 与 invariant Lagrangian counts 已独立 lemma 化；
- J2 中 `J_E(p)=epsilon_p lambda J_Z(p)` 的 global scalar / local signs 已由同一节点 quadratic tangent cone 的 Hessian determinant comparison 推出。

这减少了 exposition gap，但不改变 residual-36 尚未整体闭合的事实。

## 8. 计算证书

当前 submission-level verifier 使用 exact integer / rational arithmetic，并通过：

- weight-72 certificate；
- weight-64 residual certificate；
- `A_64>=533` 与 incidence arithmetic；
- `48/64` trade-off；
- residual-32 三个 split-MacWilliams certificates；
- residual-triangle Hilbert / liaison finite checks。

正式投稿仍应真正提供 machine-readable certificates 与 verifier scripts；不能只在正文里声称存在。

## 9. 参考文献与作者信息

当前 bibliography 已补充与正文实际使用相关的 Beauville、Catanese、Casnati--Catanese、Catanese--Tonoli、Endraß、Jaffe--Ruberman、MacWilliams--Sloane、Migliore、Miyaoka、Stanley 等来源，并按 alphabetical--chronological 顺序整理。

作者单位当前按作者提供的信息写为：

- Jizheng Chen — Department of Mathematics, Chang'an University；
- Chaoyu Hu — School of Automation, Hangzhou Dianzi University。

地址采用两校官网可核对的校址。作者本人仍需在投稿前确认最终出版时希望采用的英文单位名称。

## 10. JAG 投稿状态

当前已有：

- AMS-LaTeX / `amsart`；
- abstract < 300 words；
- MSC 2020；
- keywords；
- full postal affiliations / emails；
- alphabetical--chronological bibliography；
- non-acknowledgment author footnote 已删除；
- computational supplement statement。

尚需作者本人决定或确认：

- funding / grant 信息；
- corresponding-author metadata；
- supplementary certificate package 的实际上传或稳定存档；
- cover letter 的最终措辞。

## 11. 对 JAG 的现实判断

JAG 是否接收不能仅由格式或内部审计判断。当前主题与代数几何期刊范围相符，但稿件没有解决 `u(8)=168`，且 residual `32/36/48` 都仍有开放部分。因此投稿价值应由**已经闭合的具体定理本身**来承担，而不能依赖把未完成的极值问题包装成近乎解决，也不能依赖声称方法具有尚未证明的一般性。

较稳妥的投稿策略是：准确列出 theorem-level results，明确剩余分支，让编辑和 referee 自行判断这些结果是否达到 JAG 的 significance threshold。
