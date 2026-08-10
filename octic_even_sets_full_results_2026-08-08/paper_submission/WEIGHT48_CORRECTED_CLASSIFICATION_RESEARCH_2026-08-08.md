# Weight 48：纠正 Endraß 表格后的分类研究

日期：2026-08-08

## 0. Endraß 输入的纠正

重新核对 `Minimal even sets of nodes`, Cor. 1.11 原 PDF 表格：

- degree 8, strictly even：禁重只有 `56`；
- degree 10, strictly even：禁重 `88,96,104,112`；
- degree 8, weakly even：禁重 `32,36,...,56`；
- degree 8 的 strict minimum 是 48，且 weight 48 当且仅当由 quadric surface cut out；
- degree 8 的 weak minimum 是 28，且 weight 28 当且仅当由 plane cut out。

因此 minimum-48 strict code 的正确允许重量必须保留

\[
88,96,104,112.
\]

旧的删除这四个重量后得到的 `d(R)<=44`、`A48>=24`、global `24/32` reduction 全部撤回。

---

## 1. 当前无条件 first residual

固定 strict weight-48 word `c`：

\[
R=\operatorname{Res}(C;c)=[121,18],\qquad R\text{ 4-divisible},
\]

且已有 exact fifth-degree MacWilliams certificate 给

\[
\boxed{24\le d(R)\le48}.
\]

正确的十个 minimum lift profiles 为

\[
\begin{array}{c|c|c}
r&a&(\operatorname{wt}x,\operatorname{wt}(x+c))\\\hline
24&24&(48,48)\\
32&16&(48,64)\\
36&12&(48,72)\\
40&8&(48,80)\\
40&24&(64,64)\\
44&4&(48,88)\\
44&20&(64,72)\\
48&0&(48,96)\\
48&16&(64,80)\\
48&24&(72,72).
\end{array}
\]

---

## 2. 是否存在 `A64>=533` 的 weight-48 analogue？

### [Experimental LP diagnostic]

用正确 strict octic weight set

\[
\{0,48,64,72,80,88,96,104,112,120,128,136,144,152,160,168\}
\]

做两层诊断：

1. ordinary MacWilliams/Delsarte LP for `[169,19]`；
2. 固定一个 weight-48 word 后，把坐标分成 `121+48` 两块，对全部 canonical `H=<c>` coset states 使用 split-MacWilliams moments。

正确 weight set 给出 72 个 canonical two-block states（错误删除 `88..112` 时只有 30 个）。在 full split-LP relaxation 中，目标 `A48` 仍可取

\[
\boxed{A_{48}=1}.
\]

因此：

> 当前 ordinary / two-block split MacWilliams constraints **不能**推出任何 `A48>1`，更不用说类似 `A64>=533` 的大量 minimum words。

这是 LP 可行性诊断，不表示真实几何 code 一定存在 `A48=1`；只说明 533 型低阶 LP 证书路线本身不够。

同样，把 extended even code 的 weak coset 加入、使用 Endraß 的 weak gap `32,...,56`，标准/split LP relaxation 仍允许 strict `A48=1`，所以单纯再加 weak weight spectrum 也没有立刻产生 abundance theorem。

---

## 3. 十个 profiles 应按两类几何组织，而不是逐十个打

### Family I：存在第二个 weight-48 word

六个 profiles：

\[
\begin{array}{c|c|c}
r&|W\cap W'|&\operatorname{wt}(W+W')\\\hline
24&24&48\\
32&16&64\\
36&12&72\\
40&8&80\\
44&4&88\\
48&0&96.
\end{array}
\]

Endraß strict gap 56 正好排除了 intersection 20。因此任意两个 distinct weight-48 words 的交集只能是

\[
\boxed{0,4,8,12,16,24}.
\]

已有 contact-quadric theorem 又给：若两个 unique reduced contact quadrics 无公共 plane component，则

\[
|W\cap W'|\le16.
\]

故 intersection 24 是唯一立即进入 reducible/shared-plane geometry 的 pair type。

### Family II：minimum residual coset 不含第二个 weight-48 word

四个 profiles：

\[
(64,64),\quad(64,72),\quad(64,80),\quad(72,72),
\]

分别出现在 `r=40,44,48,48`。

若真的存在 `A48=1` 的几何 code，那么所有 first-residual minimum words 必须落在这一 family。因而与其追求一个目前不存在的 abundance theorem，更现实的替代目标是：

> 研究 “isolated weight-48 word” 是否能由 contact-quadric geometry / weak-even coset 排除。

---

## 4. Intersection 24 的强结构：weak-plane triangle

设两个 weight-48 sets `W,W'` 交 24。contact-quadric intersection theorem 迫使其 contact quadrics 共享 plane：

\[
Q=P_0\cup P_1,\qquad Q'=P_0\cup P_2.
\]

因为每个 plane component 本身都是 contact plane，Endraß Theorem 1.10 给三个 weakly even plane words

\[
U_0,U_1,U_2,\qquad |U_i|=28.
\]

并且

\[
W=U_0+U_1,\qquad W'=U_0+U_2.
\]

由 `|W|=|W'|=48`：

\[
|U_0\cap U_1|=|U_0\cap U_2|=4.
\]

又 `|W\cap W'|=24` 等价于 `wt(W+W')=48`，而

\[
W+W'=U_1+U_2,
\]

故

\[
|U_1\cap U_2|=4.
\]

因此 `r=24` profile 自动归约为

\[
\boxed{\text{三个 contact planes 的 weak-28 words，两两交 4}.}
\]

这是比一般 residual classification 更具体的几何模型。

---

## 5. Intersection 16：equality case

`r=32` 对应两个 weight-48 words 交 16，和为 strict weight64。

若 contact quadrics `q,q'` 无公共 plane，则这是 16-point theorem 的 equality case。若进一步假设

\[
C=V(q,q')
\]

integral，则从

\[
F=A^2+qB=A'^2+q'B'
\]

在 `C` 上得到 `A'^2=A^2`，故整体选符号后

\[
A'-A\in(q,q').
\]

完成平方可写成

\[
\boxed{F=Q_4^2+qq'H_4}.
\]

所以 equality case 自然产生一个 degree-4 contact carrier；这与 symmetric difference 的 weight64 相匹配。它目前是结构归约，不是 contradiction。

---

## 6. Endraß weak gap 的真正潜力

对 octic，weakly even 的强 gap 是

\[
\boxed{32,36,40,44,48,52,56\text{ 全部不存在}},
\]

而 minimum weak word 是 28，由 plane cut out。

因此未来若能从某个 strict weight-48 configuration **制造一个 low-weight weak word**，就会比试图删除 strict `88..112` 有力得多。

例如若 `U` 是 weak-28 plane word、`W` 是 strict-48 word，则 `U+W` 仍 weak，

\[
\operatorname{wt}(U+W)=76-2|U\cap W|.
\]

weak gap 立即给

\[
|U\cap W|\in\{0,2,4,6,8,24\}.
\]

所以 reducible contact-quadric / contact-plane 分支中存在很强的 discrete incidence restrictions。

---

## 7. 当前建议

48 分支不宜继续按十个 profile 机械推进。更好的分类树是：

1. **Pair-of-48 family**：按 pair intersection `24 / 16 / 12 / 8 / 4 / 0`，优先处理
   - 24：weak-plane triangle；
   - 16：contact-quadric equality case。
2. **Isolated-48 family**：四种 minimum residual lift `(64,64),(64,72),(64,80),(72,72)`，尝试用 extended weak code / contact quadric geometry 排除。
3. 不再期待仅靠 ordinary MacWilliams 得到 533 型 `A48` abundance；若要有类似效果，需要更高阶 geometry-aware constraints（weak coset、Terwilliger、contact-plane incidence）。
