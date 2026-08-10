# [RETRACTED] Weight 48：错误禁重假设下的探索

日期：2026-08-08

> **审计撤回：** 本笔记误读了 Endraß Cor. 1.11 的表格列。对 degree 8，strictly-even 禁重只有 56；88,96,104,112 属于 degree 10。因此下文基于删除 88,96,104,112 得出的 `d(R)<=44`、`A48>=24` 和全局 `24/32` reduction **均不是 octic 定理**。保留本文仅用于记录失败路线，不得引用为投稿结果。


## 0. 结论先行

在 minimum-weight-48 分支，Endraß 的 strict-even 禁重输入会显著加强当前稿件。

设 shortening 后

\[
C\subset \mathbf F_2^{169},\qquad \dim C=19,\qquad d(C)=48.
\]

则本轮得到：

1. strict octic 全局允许重量实际上是
   \[
   \boxed{\mathcal W=\{0,48,64,72,80,120,128,136,144,152,160,168\}};
   \]
   当前 `main.tex` 中仍允许 88,96 的 first-residual 表需要修正。
2. 固定 48-word 后
   \[
   R=\operatorname{Res}(C;c)=[121,18],\qquad 24\le d(R)\le44,
   \]
   改进旧的 `<=48`。
3. local minimum lift profiles 从十个缩为六个：
   \[
   \begin{array}{c|c|c}
   r&a&(\operatorname{wt}x,\operatorname{wt}(x+c))\\\hline
   24&24&(48,48)\\
   32&16&(48,64)\\
   36&12&(48,72)\\
   40&8&(48,80)\\
   40&24&(64,64)\\
   44&20&(64,72).
   \end{array}
   \]
4. 以任一 48-word 为 base 做两块 split-MacWilliams，exact dual certificate 给
   \[
   \boxed{A_{48}\ge24}.
   \]
5. 24 个 minimum words 的 incidence 强迫一对交 16 或 24；因此可以选 base 使
   \[
   \boxed{d(\operatorname{Res}(C;c))\in\{24,32\}}.
   \]

所以 48 分支出现了与 `A64>=533 + incidence` 同型的全局机制：数值没有 533 那么大，但足够把 first-residual 的 `36/40/44` 全部从全局主分支树中绕开。

---

## 1. 文献输入

Endraß, *Minimal even sets of nodes*, Theorem 1.10 与 Corollary 1.11 对 degree 8 给：

- nonzero strict even set 的最小重量是 48；
- 48 当且仅当由 quadric surface cut out；
- strict weights 56, 88, 96, 104, 112 不出现。

结合 8-divisibility，在 minimum-48 branch 的长度 169 shortened strict code 中，全部允许重量为

\[
\boxed{0,48,64,72,80,120,128,136,144,152,160,168}.
\]

shortening 只取原 strict code 的子码，因此这些禁重完整继承。

---

## 2. 固定一个 48-word 后的完整 residual weight spectrum

固定 `c`, `wt(c)=48`。对一个 `H=<c>` coset 取代表 `x`，令

- `r` = `x` 在 `supp(c)^c` 上的重量；
- `a<=24` = `x` 在 `supp(c)` 上的重量（必要时以 `x+c` 替换）。

两 lifts 的全局重量为

\[
u=r+a,\qquad v=r+48-a.
\]

所以

\[
r=\frac{u+v-48}{2},\qquad a=\frac{u-v+48}{2}.
\]

把 `u,v` 限制在上面的 Endraß 允许集合，精确枚举得到 residual 可能重量

\[
\boxed{0,24,32,36,40,44,48,52,56,72,76,80,96,100,104,108,112,116,120}.
\]

注意出现大 gap：

\[
60,64,68,84,88,92
\]

全部不可能。

---

## 3. 新的 first-residual 上界 `d(R)<=44`

考虑 length 121 的 Krawtchouk polynomial

\[
\boxed{
P=19923960K_0+127704K_3+31905K_4+4835K_5.
}
\]

所有 Krawtchouk coefficients 非负。

若 `d(R)>=48`，非零 residual weights 只能取

\[
48,52,56,72,76,80,96,100,104,108,112,116,120.
\]

精确评价为：

- `P(48)=P(56)=P(76)=0`；
- 其余上述重量上严格负。

而

\[
P(0)=1,269,004,369,920,
\]

同时 MacWilliams 平均至少为 K0 coefficient

\[
19,923,960,
\]

即总和至少

\[
19,923,960\cdot2^{18}=5,222,946,570,240,
\]

但 sign pattern 给总和至多 `P(0)`，矛盾。

故

\[
\boxed{24\le d(R)\le44}.
\]

这使 local first-residual minimum profiles 精确缩到六个。

---

## 4. Split-MacWilliams 强迫 `A48>=24`

这里普通一变量 weight-enumerator LP 不够强：如果只要求 `A48>=1`，实 LP 可以允许 `A48=1`。所以不能复制 `A64>=533` 的一变量证书。

但固定一个 48-word `c` 后，按

\[
\operatorname{supp}(c)^c\sqcup\operatorname{supp}(c)
\]

做两块 split weight enumerator，Endraß 允许重量只留下 **30 个 canonical `H=<c>` coset states**。

对 split Krawtchouk moments

\[
(i,j)=(0,2),(0,4),(0,6),(1,4),(1,6),(3,2),(4,2),(6,0),(7,0)
\]

构造 exact nonnegative dual certificate。若 `c_48(s)` 表示一个 coset state 中 weight-48 representatives 的数目，则逐 30 个 state 精确验证

\[
c_{48}(s)\ge
\alpha+\beta\mathbf 1_{s=0}
+\sum_m\lambda_m\Phi_m(s),
\qquad \lambda_m\ge0.
\]

求和并用 split-MacWilliams positivity 得到

\[
A_{48}\ge
\alpha2^{18}+\beta
=
\frac{53180410117026702938}{2252682009742045275}
\approx23.60759747.
\]

由于 `A48` 是整数，

\[
\boxed{A_{48}\ge24}.
\]

完整有理系数放在

`paper_submission/scripts/verify_weight48_global_reduction.py`

中，避免正文出现无意义的大分数。

---

## 5. 24 个 minimum words 已足够做 incidence

任取两个不同 weight-48 words `c,x`，令交集大小为 `t`。则

\[
\operatorname{wt}(c+x)=96-2t.
\]

因为 `c+x` 是非零 strict word，且不超过 96；Endraß 后允许的重量只有

\[
48,64,72,80.
\]

因此

\[
\boxed{t\in\{24,16,12,8\}}.
\]

现在至少有 24 个 48-words，总 coordinate-incidence 是

\[
24\cdot48=1152.
\]

把 1152 尽量均匀分到 169 coordinates，凸性给 pair-incidence 下界

\[
138\binom72+31\binom62
=3363.
\]

若所有 pair intersection 都至多 12，则上界只有

\[
12\binom{24}{2}=3312,
\]

矛盾。

所以存在一对 48-words 满足

\[
\boxed{t=16\quad\text{或}\quad24}.
\]

固定其中一个 `c`，另一个在 complement 上给 residual word 重量

\[
48-t=32\quad\text{或}\quad24.
\]

而 residual minimum 至少 24，且完整 spectrum 中没有 28，所以

\[
\boxed{d(\operatorname{Res}(C;c))\in\{24,32\}}.
\]

这就是 weight-48 版本的 `many minimum words + incidence` global reduction。

---

## 6. 两个真正剩余的几何分支

### 6.1 `d(R)=24`

minimum profile 必为

\[
(48,48),\qquad |W_1\cap W_2|=24.
\]

于是

\[
W_3=W_1+W_2
\]

也有 weight 48，三非零 words 全是 48；四块为

\[
\boxed{(97,24,24,24)}.
\]

由 contact-quadric intersection theorem，任意两对应 reduced contact quadrics 必共享 plane component。故三套 minimal contact quadrics 全部 reducible。

进一步，每个 plane component 本身是 contact plane，因而切出 weight-28 weakly even set。因一个 reducible contact quadric由两个 contact planes组成，48-word 可视为两个 weak-28 plane words 的和；两 plane words 的交集大小必须为 4。

因此 `d=24` 的自然几何模型不是一般 residual，而是一个 **contact-plane triangle**。这比旧 second-residual 暴力枚举更值得优先研究。

目前没有仅靠低阶 split-MacWilliams 找到对 `(97,24,24,24)` triangle 的直接 contradiction；所以这一分支暂不标记闭合。

### 6.2 `d(R)=32`

minimum profile 唯一为

\[
(48,64),\qquad |W_{48}\cap W'_{48}|=16,
\]

其中两 48-words 的和是 weight 64。

如果两个 contact quadrics 无公共 plane，这正好达到 16-point theorem 的等号情形；因此可改为研究 **equality case of the contact-quadric intersection theorem**，而不是一般 residual classification。

四块对二维子码 `H=<c_1,c_2>`（weights `48,48,64`）为

\[
\boxed{(89,32,32,16)}.
\]

低阶 split-MacWilliams LP 没有直接排掉这一 block type，因此目前也不应称其 code-theoretically closed。

---

## 7. 当前最优路线

weight 48 不再应该按旧的十个 first-residual profiles 往下逐类处理。

新的主树是

\[
\boxed{
\text{minimum }48
\Longrightarrow A_{48}\ge24
\Longrightarrow d(R)=24\text{ or }32.
}
\]

然后分别研究：

1. `d=24`：三套 weight-48 / 三个 reducible contact quadrics / contact-plane triangle；
2. `d=32`：两个 contact quadrics 的 16-point equality case + 一个 weight-64 sum。

这两类都比原来的 `24,32,36,40,44,48` 六个距离、十个 profile 小得多。
