# Weight 48：48/64 trade-off 与无条件 weight-64 determinant theorem

日期：2026-08-08

状态：**[新审计通过；暂未并入 main.tex]**

本文只记录在当前 shortened `[169,19]` high-node framework 中已经逐接口核对通过的结论。它替代“试图直接证明 `A48` 很大”的旧路线。

---

## 1. 核心变化：533 的正确 weight-48 analogue 是 trade-off

沿用 minimum-64 分支中已经精确验证的五阶 Krawtchouk–MacWilliams 多项式

\[
P(w)=\lambda+\sum_{j=1}^5\mu_j\frac{K_j^{(169)}(w)}{\binom{169}{j}},
\]

其中

\[
\lambda=\frac{455}{131072},
\]

且所有 \(\mu_j>0\)。直接精确计算得

\[
\begin{array}{c|rrrrrrrrrrrrrrrr}
w&0&48&64&72&80&88&96&104&112&120&128&136&144&152&160&168\\\hline
P(w)&1287&21&1&0&0&0&0&0&-1&-6&-21&-56&-126&-252&-462&-792.
\end{array}
\]

对任意当前的 binary `[169,19]` strict octic code，MacWilliams 恒等式给

\[
\sum_{c\in C}P(\operatorname{wt}c)
=2^{19}\lambda
+2^{19}\sum_{j=1}^5
\mu_j\frac{A_j^\perp}{\binom{169}{j}}.
\]

因为

\[
2^{19}\lambda=1820,
\]

故得到精确恒等式

\[
\boxed{
\begin{aligned}
A_{64}+21A_{48}
={}&533+A_{112}+6A_{120}+21A_{128}+56A_{136}\\
&+126A_{144}+252A_{152}+462A_{160}+792A_{168}\\
&+2^{19}\sum_{j=1}^5
\mu_j\frac{A_j^\perp}{\binom{169}{j}}.
\end{aligned}}
\]

因此无条件有

\[
\boxed{A_{64}+21A_{48}\ge533.}
\]

这不是 LP relaxation 的经验现象，而是 exact MacWilliams identity。

---

## 2. 新定理：weight-64 determinant structure 不需要 `d(K)=64`

### 定理

设 \(X=V(F_8)\subset\mathbf P^3\) 是仅有 ordinary double points 的八次曲面。设 \(Z\) 是任意 strict even set，且

\[
|Z|=64.
\]

则存在 quartics \(q_0,q_1,q_2\) 使

\[
\boxed{F_8=q_0q_2-q_1^2}
\]

（允许对其中一个 \(q_i\) 作非零常数缩放），并且

\[
\boxed{Z=V(q_0,q_1,q_2)}
\]

scheme-theoretically。特别地，\(Z\) 是 reduced transverse \(CI(4,4,4)\)。

### Proof audit

令 \(\pi:\widetilde X\to X\) 为节点解消，\(E_Z\) 为 \(Z\) 上 exceptional curves 之和，并令

\[
L_Z:=\frac{4H-E_Z}{2}.
\]

#### Step 1. RR 强迫至少两个 sections

Endraß 的 RR 公式（degree \(s=8\)，strict，\(v=4\)）给

\[
\chi(L_Z)
=\frac{8\cdot4}{8}(4-16+8)+\binom73+1-\frac{64}{4}
=4.
\]

由 Serre duality 与 Endraß Lemma 4.1，

\[
h^2(L_Z)=h^0(L_Z).
\]

故

\[
4=2h^0(L_Z)-h^1(L_Z),
\]

于是

\[
\boxed{h^0(L_Z)\ge2.}
\]

由 Endraß Prop. 3.3(i)，\(Z\) 在 degree 4 不可能 stable。

#### Step 2. semistable 也不可能

若 \(Z\) 在 degree 4 semistable，则由 Endraß Prop. 3.3(ii)：

- reduced fixed part \(B_Z\) cuts out \(Z\)；
- moving quadratic system \(F_Z\) contains a square。

由于并非 stable，\(F_Z\neq\varnothing\)。square 的 degree 必为正偶数。又 \(B_Z\) 必非空（否则不可能 cut out 非空 \(Z\)），所以在总 degree 4 下只能有

\[
\deg F_Z=2,\qquad \deg B_Z=2.
\]

因此一个 **reduced quadric** \(B_Z\) cut out \(Z\)。但 Endraß Prop. 3.8(ii) 对 even \(s=8\) 明确给

\[
|Z|=s(s-2)=8\cdot6=48,
\]

与 \(|Z|=64\) 矛盾。

故 \(Z\) 在 degree 4 必为 unstable。

#### Step 3. unstable 在 `v=s/2=4` 直接给 determinant

Endraß Prop. 3.6 对 unstable word 给 quartics \(q_0,q_1,q_2\) 与 degree

\[
2v-s=8-8=0
\]

的 polynomial \(\alpha\)，满足

\[
\alpha F_8=q_0q_2-q_1^2.
\]

这里 \(\alpha\) 为非零常数（Endraß Cor. 3.7(i) 的 `v=s/2` 情形中辅助 surface \(W\) 正是空集）。重标度后

\[
\boxed{F_8=q_0q_2-q_1^2.}
\]

注意：Endraß Cor. 3.7(i) 同时给 unstable degree \(s/2\) 的 weight 必为

\[
\frac{s^3}{8}=64,
\]

与此完全一致。

#### Step 4. base scheme 自动是 reduced `CI(4,4,4)`

由构造，三个 quartics 都在 \(Z\) 上消失，所以

\[
Z\subseteq V(q_0,q_1,q_2).
\]

若公共零点集含曲线 \(\Gamma\)，则在 \(\Gamma\) 上

\[
q_0=q_1=q_2=0,
\]

从

\[
F_8=q_0q_2-q_1^2
\]

立即有

\[
dF_8=q_2dq_0+q_0dq_2-2q_1dq_1=0
\]

沿 \(\Gamma\) 恒成立。因此 \(\Gamma\subset\operatorname{Sing}X\)，与 \(X\) 只有孤立节点矛盾。

故三 quartics 的 ideal 高度为 3；在 \(\mathbf P^3\) 中它们形成 regular sequence。因此

\[
\operatorname{length}V(q_0,q_1,q_2)=4^3=64.
\]

这个零维 scheme 已包含 \(Z\) 的 64 个不同 reduced points，所以长度已经耗尽：

\[
\boxed{V(q_0,q_1,q_2)=Z}
\]

scheme-theoretically。于是该 complete intersection 自动 reduced/transverse。

### 审计结论

旧正文把这一定理放在 `d(K)=64` 假设下，是不必要的。证明实际只需要：

1. octic nodal surface；
2. strict even set；
3. weight exactly 64。

因此它可以在 `d(K)=48` 分支中无条件调用。

---

## 3. 48-word pair 的 incidence dichotomy

令

\[
M:=A_{48}.
\]

任意两个 distinct weight-48 words \(W,W'\) 的和重为

\[
96-2|W\cap W'|.
\]

在当前 strict octic spectrum 与 minimum 48 下，允许的和重只有

\[
48,64,72,80,88,96,
\]

故

\[
\boxed{|W\cap W'|\in\{0,4,8,12,16,24\}.}
\]

若 \(M\ge22\)，总 point-word incidence 为 \(22\cdot48=1056\)。在 169 个坐标上按凸性最均匀分配：42 个坐标 incidence 7，127 个 incidence 6，因此

\[
\sum_{W<W'}|W\cap W'|
\ge42\binom72+127\binom62
=2787.
\]

若所有 pair 交数至多 12，则右边至多

\[
12\binom{22}{2}=2772,
\]

矛盾。故

\[
\boxed{M\ge22\Longrightarrow\exists W\ne W':\ |W\cap W'|\in\{16,24\}.}
\]

这把 large-`A48` 分支压到两个 contact-quadric pair geometries：

- intersection 16：若两 unique reduced contact quadrics 无公共 plane component，则为已有 16-point theorem 的 equality case；
- intersection 24：由已有 contact-quadric theorem 强迫 shared-plane / weak-plane triangle geometry。

注意：intersection 16 的 shared-component 子支仍需单独保留，不应无条件写成 coprime equality case。

---

## 4. `A48` 小时，64-word abundance 自动接管

由 trade-off，

\[
A_{64}\ge533-21M.
\]

### 4.1 `M<=21`

此时

\[
A_{64}\ge92.
\]

取任意 92 个 weight-64 supports。总 incidence

\[
92\cdot64=5888=27\cdot34+142\cdot35.
\]

故凸性给

\[
\sum_{Z<Z'}|Z\cap Z'|
\ge27\binom{34}{2}+142\binom{35}{2}
=99637.
\]

若所有 pair 交数至多 20，则最多

\[
20\binom{92}{2}=83720,
\]

矛盾。因此有 pair 交数至少 24。

两个 distinct weight-64 words 的和重为

\[
128-2|Z\cap Z'|.
\]

minimum 48 + strict octic spectrum 给允许交数

\[
0,4,8,12,16,20,24,28,32,40
\]

（36 对应 forbidden strict weight 56）。所以

\[
\boxed{M\le21\Longrightarrow
\exists Z\ne Z':\ |Z\cap Z'|\in\{24,28,32,40\}.}
\]

对应四种熟悉 block profiles：

\[
\begin{array}{c|c|c}
|Z\cap Z'|&\operatorname{wt}(Z+Z')&\text{profile}\\\hline
24&80&(24,40,40,65)\quad(40A)\\
28&72&(28,36,36,69)\\
32&64&(32,32,32,73)\quad(32\text{-triangle})\\
40&48&(40,24,24,81).
\end{array}
\]

而由第 2 节新定理，**这里每个 weight-64 word 都自动带 symmetric determinant / reduced `CI(4,4,4)` presentation**，即使全局 minimum 是 48。

### 4.2 `M<=17`

此时

\[
A_{64}\ge533-21\cdot17=176.
\]

176 个 weight-64 supports 的最小 pair-incidence 是

\[
59\binom{66}{2}+110\binom{67}{2}=369765,
\]

而

\[
24\binom{176}{2}=369600.
\]

因此平均 pair intersection 严格大于 24，故至少一对交数 \(>24\)。由离散允许谱，

\[
\boxed{M\le17\Longrightarrow
\exists Z\ne Z':\ |Z\cap Z'|\in\{28,32,40\}.}
\]

即只剩 sum weights

\[
\boxed{72,64,48.}
\]

### 4.3 isolated weight-48 极端

若

\[
A_{48}=1,
\]

则

\[
\boxed{A_{64}\ge512.}
\]

对 512 个 weight-64 supports，凸性最小 pair-incidence 为

\[
3160375.
\]

以 intersection 24 为 baseline：

\[
24\binom{512}{2}=3139584,
\]

excess 为

\[
20791.
\]

任意一对 intersection \(\ge28\) 相对 baseline 24 最多贡献 \(40-24=16\) 的 excess。因此至少有

\[
\left\lceil\frac{20791}{16}\right\rceil=1300
\]

对满足

\[
|Z\cap Z'|\ge28.
\]

故至少一个 weight-64 determinant word 有

\[
\left\lceil\frac{2\cdot1300}{512}\right\rceil=6
\]

个这样的近邻。

所以

\[
\boxed{
A_{48}=1
\Longrightarrow
A_{64}\ge512,
\quad
\#\{\{Z,Z'\}:|Z\cap Z'|\ge28\}\ge1300.
}
\]

这说明“isolated 48-word”并不是无结构出口，反而强迫极大量 determinant weight-64 presentations。

---

## 5. 推荐的新 weight-48 主分类树

不再把十个 first-residual profiles 作为第一层。建议主线改为

\[
\boxed{
\begin{array}{c}
d(K)=48,\quad A_{64}+21A_{48}\ge533\\[1mm]
\downarrow\\
\begin{cases}
A_{48}\ge22
&\Rightarrow (48,48)\text{ pair intersection }16\text{ or }24,\\[1mm]
18\le A_{48}\le21
&\Rightarrow (64,64)\text{ pair intersection }24,28,32\text{ or }40,\\[1mm]
A_{48}\le17
&\Rightarrow (64,64)\text{ pair intersection }28,32\text{ or }40.
\end{cases}
\end{array}}
\]

其中所有出现的 weight-64 words 都无条件是 symmetric determinant `CI(4,4,4)` presentations。

因此 weight-48 分支已经从“十个 local residual profiles”提升为：

> **many contact quadrics versus many symmetric determinant presentations 的全局二分。**

---

## 6. 当前未闭合点

这份笔记没有声称排除 `d(K)=48`。剩余真正任务是：

1. `A48>=22`：处理 intersection 16 的 shared-component 子支，并进一步闭合 16/24 两种 contact-quadric geometry；
2. `18<=A48<=21`：处理 determinant pair 的 24/28/32/40 四种相容性；
3. `A48<=17`：只需处理 28/32/40，其中 32 与 36 已和 minimum-64 项目的 residual geometry 重合，40 直接产生新的 weight-48 word；
4. 研究是否可以把 `40 -> weight48` 反过来与 `M` 的计数结合，进一步提升 incidence trade-off；
5. 在升级到 `main.tex` 前，给新 exact identity 增加独立 verifier，并同步 RESULTS_LEDGER / PROOF_AUDIT。

---

## 7. Endraß 接口（已逐项核对）

使用 `Minimal even sets of nodes`：

- RR formula in §1；
- Proposition 3.3：stable / semistable / unstable characterization；
- Proposition 3.6：unstable degree-v quadratic system 与 `alpha F = g00 g11 - g01^2`，其中 `deg alpha=2v-s`；
- Corollary 3.7(i)：unstable in degree `s/2` implies weight `s^3/8`；
- Proposition 3.8(ii)：reduced quadric on even degree-s surface cuts out strict weight `s(s-2)`；
- Lemma 4.1：`+Ew` 与 `-Ew` 的 cohomology symmetry。

这些接口在 `s=8,v=4,|Z|=64` 下相互完全兼容，没有使用 `d(K)=64`。