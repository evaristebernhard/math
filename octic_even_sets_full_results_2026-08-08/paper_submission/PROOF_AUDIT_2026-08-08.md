# 投稿稿逐证明审计（2026-08-08，历史版本）

> **Superseded:** 当前投稿状态请以 `PROOF_AUDIT_2026-08-09.md` 为准。本文件保留用于追踪历史纠错，其中若与 2026-08-09 审计冲突，以后者为准。

本文件比较 `paper_submission/main.tex` 与 2026-08-05 的 60 页完整技术证明稿，并额外检查逻辑是否真的由当前正文支持。目标不是“删结论”，而是区分：

- **GREEN**：当前数学逻辑闭合，只需补写细节/引用；
- **YELLOW**：原技术稿有证明，但投稿稿压缩过度，必须恢复关键中间步骤；
- **RED**：当前投稿稿存在实际错误、过度宣称或依赖未证明输入，必须改状态。

---

## 1. 统一 shortening：GREEN，但定理少了一个维数条件

当前 lemma 说任意 prescribed subcode `D` 只要 support union ≤104，都能最后选一个 19 维子码包含 `D`。这在 `dim D>19` 时显然不成立。

应改成：

\[
\dim D\le 19,\qquad |\operatorname{supp}(D)|\le 104.
\]

项目里实际需要保留的 low-weight configurations 维数都很小，所以这只是定理陈述修正，不影响应用。

shortening 的维数记账本身正确：进行 \(\nu-169\) 次 shortening，每次维数至多降 1，故
\[
(\nu-150)-(\nu-169)=19.
\]

---

## 2. Weight 72：RED（当前正文过度宣称）

### 原技术稿真正证明的结论

原稿明确从
\[
d(K)=72
\]
出发，得到一个
\[
[169,19,72]
\]
的 8-divisible code，并证明这种 code 不存在。

所以闭合结论是：

\[
\boxed{d(K)\neq 72.}
\]

而不是：

> “任何 \([169,19]\) 8-divisible code 只要含有一个 72-word 就不可能。”

### 为什么当前正文的强版本不成立

residual restriction
\[
C/\langle c\rangle\to \mathbf F_2^{97}
\]
的单射证明使用了：若 kernel representative \(x\subseteq\operatorname{supp}(c)\)，则
\[
72\le \operatorname{wt}(x)\le72.
\]
左侧正是 minimum distance 72 的假设。

如果 code 另有 48- 或 64-word，这一步不成立。

### 必须修正

- Introduction/Theorem 1：改成“minimum-distance-72 branch is impossible”。
- Section weight 72 开头显式假设 \(d(C)=72\)。
- 不得在 weight-48 branch 中把这个 theorem 当成“所有 72-word 都被禁止”。

---

## 3. Weight 64 determinant theorem：YELLOW → 可修成 GREEN

结论本身与完整技术稿一致：在 \(d(K)=64\) 下，每个 weight-64 word 自动给出
\[
F=q_0q_2-q_1^2,
\qquad
W=V(q_0,q_1,q_2)=CI(4,4,4),
\]
且 reduced transverse。

当前投稿稿只用了两段话，丢掉了三个需要展示的关键节点：

1. 设
   \[
   L=\frac{4H-E_W}{2},
   \qquad \chi(L)=4,
   \qquad h^2(L)=h^0(L),
   \]
   因而 \(h^0(L)\ge2\)。
2. Endraß degree-four stability alternative 的 semistable case：fixed part degree 必须是 2，从而产生 contact quadric / weight 48，与 \(d(K)=64\) 冲突。
3. unstable case 中 \(s_0^2,s_0s_1,s_1^2\) 的 quartic lifts 与
   \[
   q_0q_2-q_1^2=\lambda F,
   \quad \lambda\neq0.
   \]

最后的 regular-sequence / length \(4^3=64\) / reduced-transverse argument 是可靠的。

需要补的主要是“文献输入的精确引用 + 中间次数记账”，不是新 gap。

---

## 4. Weight 64 first residual：GREEN，但投稿稿证明太短

固定 \(c\) 后：
\[
R=[105,18],\quad 4\text{-divisible},\quad d(R)\ge32.
\]
这是完整可证的。

五阶 certificate 应把真正的 MacWilliams 矛盾写出来：
\[
\mathbb E_R P_R
=4480+3008A_1(R^\perp)+\cdots+5A_5(R^\perp)
\ge4480,
\]
而若 \(d(R)\ge44\)，则
\[
\mathbb E_RP_R\le \frac{656015360}{2^{18}}=2502.5.
\]
因此
\[
d(R)\in\{32,36,40\}.
\]

lift profiles 32/36/40A/40B 的数值推导也正确。

---

## 5. 40B：RED as stated；但可以完全绕开这个接口

当前正文把 “40B” 直接说成 unique weight-64 outlet，然后用 certificate 排除。

问题是：

> “如果存在第二个 weight-64 word，就能选择公共块至少 24 的 pair”

在 60 页母稿中被明确标为 **Residual-intersection input**，并没有在该稿中独立证明。

所以：

- 纯码论的 40B 只表示一个 minimum residual word 的 two lifts 是 \((72,72)\)；
- “40B = 整个 code 只有一个 64-word”需要额外几何输入；
- 当前投稿稿不能把 40B 无条件排除写成完整 theorem。

### 更好的主线：完全不需要这个 input

已经证明
\[
A_{64}\ge533.
\]
incidence convexity 又证明存在两个 weight-64 words 满足
\[
|W_1\cap W_2|\ge28.
\]
对不同 64-words，交集不可能超过 32，因此可选一对使
\[
|W_1\cap W_2|=28\quad\text{或}\quad32.
\]
固定 \(W_1\) 取 residual，则 \(W_2\) 给出 residual word
\[
r=64-|W_1\cap W_2|=36\quad\text{或}\quad32.
\]
由于总有 \(d(R)\ge32\)，于是对一个适当选择的 minimum word：
\[
\boxed{d(R)\in\{32,36\}.}
\]

这是**纯 coding + incidence 的无条件全局 reduction**，比旧的 residual-intersection input 更强、更干净。

因此单篇投稿建议：

- 40A/40B 留作“local residual profile”或 appendix；
- 主线在证明 \(A_{64}\ge533\) 后直接全局压到 residual 32/36；
- 不让未重证的 pairwise residual-intersection input 承担主逻辑。

---

## 6. \(A_{64}\ge533\) 与 incidence：GREEN，但必须恢复精确算术

LP polynomial 的完整系数和 weight table 已在母稿中给出，应该至少放 appendix。

对 incidence，当前正文只有一句“convexity gives...”，投稿不够。

令 \(N=533\)，每个 block 大小 64，坐标数 169，令 \(m_p\) 为经过坐标 \(p\) 的 minimum words 数。则
\[
\sum_p m_p=533\cdot64=34112=169\cdot201+143.
\]
凸性给
\[
\sum_p\binom{m_p}{2}
\ge 26\binom{201}{2}+143\binom{202}{2}
=3,425,643.
\]
另一方面
\[
\sum_p\binom{m_p}{2}
=\sum_{\{x,y\}}|x\cap y|.
\]
总 pair 数为
\[
\binom{533}{2}=141,778.
\]
如果所有交集 \(\le24\)，右边最多
\[
24\cdot141,778=3,402,672<3,425,643,
\]
矛盾，所以有交集至少 28。

若无 32-intersection pair，则
\[
3,425,643\le24\binom{533}{2}+4e_{28},
\]
所以
\[
e_{28}\ge \left\lceil\frac{22,971}{4}\right\rceil=5743.
\]
平均 degree 为
\[
\frac{2e_{28}}{533}>21.5,
\]
故某顶点 degree 至少 22。

这是一段很漂亮、很短但完整的证明，应放正文。

---

## 7. Residual triangle：YELLOW / CT，不应假装完全无条件

母稿的 quadratic LD 部分实际上非常详细而且有价值，当前正文压成了 15 行，远远不够。

至少应恢复：

- blow-up
  \[
  Y=\operatorname{Bl}_A\mathbf P^3,
  \qquad D=4H-\sum_{a\in A}E_a,
  \]
  和
  \[
  D^2\cdot\widetilde P_e=16e-32;
  \]
- quadric restriction \(L^2=0\)、Stein factorization、image 是直线；
- \(\dim(W\cap qS_2)=3\)；
- 每个 determinant net 与 kernel 恰交一维；
- normal form 与 \(CI(2,2,4)\sqcup CI(2,2,4)\) 的 \(16+16\) splitting；
- quadratic compatibility 产生 contact quadric；
- cubic \(t=16\) 的 liaison h-vector contradiction；
- cubic \(t=0\) 的三 cubic common-component argument；
- primitive rank-4/rank-3 factorization 降回 degree ≤2。

### Residual triangle 仍是无条件几何分支

母稿自己写的是：

> “公共 pencil 引理给出 ...”

后续审计已经重证 common-pencil、defect-two cubic/primitive 等多个接口，并进一步压缩 higher-defect candidates；但 residual triangle 的完整无条件闭合仍需几何 comparison。

一个 legacy split-MacWilliams certificate 在附加假设
\[
A_{88}=A_{96}=A_{104}=A_{112}=0
\]
下确实给出 122-state exact contradiction；然而重新核对 Endraß 原 PDF 后确认，Cor. 1.11 的 degree-8 strictly-even gap 只有 weight \(56\)，而 \(88,96,104,112\) 位于 degree-10 列。因此该 certificate 只能保留为 conditional audit，不能用于 octic 主线。正确全局状态仍是
\[
\boxed{d(\operatorname{Res}(C;c))\in\{32,36\}},
\]
其中 32 是 residual-triangle 几何分支，36 暂缓完整闭合。

---

## 8. J1/J2：GREEN theorem，YELLOW exposition

J1 的完整证明应恢复两条 exact sequences：
\[
0\to R_U\to R_Z\oplus R_E\to S/J\to0,
\]
\[
0\to Q_A\to S/J\to R_A\to0,
\]
再 apply \(\operatorname{Ext}_S^\bullet(-,S(-4))\)，使用 1-dimensional CM vanishing 与 Matlis duality。

J2 也应写出
\[
\operatorname{Rel}_{D_0}(8)
=\ker(\operatorname{Rel}_U(8)\to k^A)
\]
以及
\[
J_E(p)=\varepsilon_p\lambda J_Z(p).
\]
这样 orientation coherence 与
\[
\langle\lambda_Z,\lambda_E\rangle\cap\operatorname{Rel}_{D_0}(8)\neq0
\]
的等价才是可检查的。

结论只到 degree 8，不能自动下沉到 degree ≤3；这一 audit correction 当前正文写对了。

---

## 9. Regular comparison：RED if called “closed”; GREEN only for the coupled-block theorem

母稿真正完整写出的新 theorem 是：genuinely coupled degree-0/1 Horrocks block 不可能。

必须恢复两个数值式：
\[
\sum_a x_an_a+8n_0+5n_1=4,
\]
\[
\sum_a x_a^3n_a+44n_0+5n_1=
\begin{cases}
10,&w=72,\\
4,&w=80.
\end{cases}
\]
由 minimality 排除 \(a\ge7\)，得到
\[
n_6=n_2+6n_0-1\quad(w=72),
\]
\[
n_6=n_2+6n_0\quad(w=80),
\]
故 \(n_6>3n_0\)。

filtration
\[
0\to\Omega^1(-1)^{n_1}\to\mathcal H_\mu\to\Omega^1{}^{n_0}\to0
\]
再给 \(n_6\le3n_0\)，矛盾。

### 真正的问题

母稿说：

> “此前 split、central \(\Omega^1(-2)\)、single \(\Omega^1(-1)\)、single \(\Omega^1\)、null-correlation outlets 已处理。”

但这些证明并没有包含在当前 60 页稿，也没有进入投稿稿。

所以当前论文最多能声称：

\[
\boxed{\text{the final genuinely coupled Horrocks block is impossible}.}
\]

不能仅凭现在的正文声称“regular comparison fully closed”。

如果旧笔记里能把那些 outlet proofs 找回来，就补入 appendix；找不回来则在论文里降格为明确输入。

---

## 10. QT-lift：YELLOW，且 theorem 需要补一个 carrier 假设

核心 argument 很漂亮，而且在 residual-36 normal-nodal 应用下基本闭合。

但当前 QT theorem 的 statement 没写 \(T=(\tau=0)\) irreducible，而消去常数误差 \(H\) 的证明用了：

> “一个二次式在不可约四次面 \(T\) 上恒为零，因此只能为零。”

所以当前证明至少需要
\[
\tau\text{ irreducible}
\]
（或者另外证明一个适用于 reduced/reducible carrier 的更强版本）。

在本文唯一实际使用 QT 的 normal-nodal Smith outlet 中，\(T\) 本来就是 irreducible normal quartic，所以最简单的修法是：**把 QT theorem 限制到这个实际应用所需的 irreducible carrier 情形。**

此外应显式解释：为什么 \(Q\) 提升同一个 sheaf morphism 后
\[
Q^tN^{-1}Q-c\tau M^{-1}\in\operatorname{Mat}_2(S),
\]
而不只是直接写成“there is a constant H”。

---

## 11. Normal-nodal Smith carrier：YELLOW，当前投稿稿压缩得太严重

当前正文把母稿约 8 页证明压成两段，这种程度不能投稿。

必须恢复至少以下数据：

1. 写
   \[
   M=\begin{pmatrix}x&y\\y&z\end{pmatrix},
   \qquad
   Q=\begin{pmatrix}a&b\\b&c\end{pmatrix},
   \qquad \tau=ac-b^2.
   \]
2. 2×2 identity
   \[
   QMQ+\tau\operatorname{adj}(M)=\operatorname{tr}(QM)Q.
   \]
3. 从 QT 推出唯一 quadratic \(h\)：
   \[
   ax+2by+cz=h\tau,
   \qquad
   N=hQ-\operatorname{adj}(M).
   \]
4. \(h\neq0\)。
5. Smith-border 需要明确提供 \(\Delta=V(a,b,c)\) 是 reduced transverse 8-point scheme（母稿在节点分离证明中用了 \(da,db,dc\) independent）。当前 theorem statement 没写这个 hypothesis。
6. 证明
   \[
   \Delta\cap R=\varnothing,
   \qquad
   \Delta\cap\operatorname{Sing}X=\varnothing.
   \]
7. 公共 28 点满足
   \[
   W_M\cap H=A=W_N\cap H
   \]
   scheme-theoretically，且两 nets 在 \(H\) 上相同。
8. smooth quadric：
   \[
   c_1(\mathcal K)=(-4,-4),\quad c_2(\mathcal K)=4,
   \]
   discriminant \(-16\)，destabilizing type 只能 \((1,0,0)\) 或 \((0,1,0)\)，进而 trace syzygy 有公共因子。
9. two planes / double plane：恢复 \(c_2=16-r\) 与矛盾。
10. cone：在 \(\mathbb F_2\) 上分 vertex outside/inside A 两种，恢复 \(c_2=4\) / \(3\) 的计算。

结论本身仍然可以保留为 **[CT]**，但证明必须恢复到这个颗粒度。

---

## 12. Weight 48 first residual：GREEN，但需要写完整 MacWilliams proof

当前正文只说 polynomial 有 nonnegative expansion，却没给 expansion：
\[
P_{48}(r)
=9885K_0+4635K_1+1079K_2+225K_3+\frac{129}{4}K_4+\frac{15}{4}K_5.
\]
若 \(d(R)\ge52\)，
\[
\mathbb E_RP_{48}\ge9885,
\]
但
\[
\mathbb E_RP_{48}\le\frac{1,092,648,960}{2^{18}}=4168.125,
\]
矛盾。

这一段可以完整写在正文，只有十几行。

---

## 13. Weight 48 contact-quadric 16-point theorem：RED in current text；结论本身 GREEN

当前投稿稿写成：重复分量上的节点由“cubic”切出，贡献 \(3e_\Gamma\)。这是错误的。

正确 contact presentation 是
\[
F=A^2+qB=A'^2+q'B',
\qquad \deg A=4,\quad \deg B=6.
\]
对 \(C=Q\cap Q'\) 的 irreducible component \(\Gamma\)：

- 若 \(A|_\Gamma\not\equiv0\)，公共节点由 quartic \(A\) 切出，至多 \(4e_\Gamma\)；
- 若 \(A|_\Gamma\equiv0\)，则 \(\Gamma\subset X\)，并且 repeated intersection forces \(m_\Gamma\ge2\)；节点由 sextic \(B|_\Gamma=0\) 控制，至多 \(6e_\Gamma\)。

令 \(E_1,E_2\) 为两类 reduced total degrees，则
\[
E_1+2E_2\le4,
\]
所以
\[
|W\cap W'|
\le4E_1+6E_2
=4(E_1+2E_2)-2E_2
\le16.
\]

因此 **16-point theorem 的结论没坏，但当前投稿稿 proof 中的 3 必须改成 6。**

---

## 14. Weight 48 second/third residual certificates：RED as unconditional statements

这是本轮审计发现的另一个重要问题，来自母稿本身而不只是投稿压缩。

`verify_octic_weight48_second_residual.py` 中写的是：

```python
STRICT = {0, 48, 64, *range(80, 169, 8)}  # weight 72 already excluded
```

但前面的 weight-72 theorem 只证明
\[
d(K)\neq72,
\]
即排除 minimum-distance-72 branch；它**没有证明在 \(d(K)=48\) 的 code 里不存在 72-word**。

事实上 weight-64 residual-36 分支本身就自然产生 72-word，所以“weight 72 already excluded globally”显然不是已证明事实。

因此：

- second residual 的 `d=18 none` 等依赖上述 `STRICT` 集合的 statement，目前只能标为
  \[
  \boxed{\text{conditional on the additional hypothesis }A_{72}=0};
  \]
- factor-graph / d=28 third residual 若继承同一 weight set，也必须同步检查并降格；
- 这些结果不能以无条件 [C] 身份放进投稿正文或 appendix。

第一 residual 的十个 profiles **没有这个问题**，因为它明确允许了 weights 72。

---

# 本轮建议后的“单篇投稿安全主线”

最干净的无条件/明确条件结构应改为：

1. 文献输入 + shortening + Griesmer：minimum branch 只需考虑 48/64/72。
2. **minimum-distance 72 branch** 完整排除。
3. minimum 64 ⇒ 每个 64-word 自动 symmetric transverse \(CI(4,4,4)\)。
4. \(A_{64}\ge533\) + exact incidence theorem。
5. 由 incidence **无额外几何 input** 选择一对 intersection 28 或 32，得到一个 fixed minimum word 的 residual distance 32 或 36。
6. residual 32 不能由旧 split-MacWilliams 无条件排除：其额外删除的 \(88,96,104,112\) 并非 Endraß 的 octic 禁重。故全局 minimum-64 主线准确停在
   \[
   \boxed{d(R)\in\{32,36\}}.
   \]
   其中 32 继续走 residual-triangle 几何；36 暂不继续完整闭合。
7. residual 36：J1/J2、coupled Horrocks block、QT/Smith 等已完成内容保留为 partial structural results；不宣称 outlets 完备，也不把这些局部结果串成未经证明的 closure。
8. minimum 48：无条件 first residual 仍为 \(24\le d(R)\le48\)，共有十个 local profiles；16-point contact-quadric theorem 保留。误删 \(88,96,104,112\) 后得到的 \(A_{48}\ge24\) 与 \(24/32\) global reduction 已撤回。
9. second/third residual finite enumeration 暂从“无条件投稿结果”中撤下，保存在成果库并标记额外假设 \(A_{72}=0\)。

这样论文反而会更强：它不再依赖未重证的 pairwise residual-intersection strengthening 来进入 32/36，而是由已经完全闭合的 \(A_{64}\) incidence 直接进入。

---

## 15. Residual triangle 的二次审计：母稿还隐藏了三个独立接口

把 2026-08-05 母稿的 triangle 章节逐句对照后，除了早先已经识别的 common-pencil lemma，还发现三处没有在母稿中展开证明的步骤：

1. **(HV) liaison Hilbert-vector input**：在 cubic \(t=16\) 分支，母稿直接使用“cubic candidate 的中间 \(h\)-vector entry 为 11，而 \(CI(3,4,4)\) 为 10”。后者可由
   \[
   (1+t+t^2)(1+t+t^2+t^3)^2
   \]
   直接计算，但 candidate 的 11 没有在母稿中推导。正式稿需要给出该 Hilbert-function calculation。
2. **(CD) cubic-degeneration input**：在 cubic \(t=0\) 分支，可严格推出三个 contact cubics 必有正维公共 locus；母稿随后一句“进入同一退化路线”就结束。需要独立证明该公共 locus 确实强迫 degree \(\le2\) carrier 或 nonprimitive cubic reduction。
3. **(PH) primitive Hilbert input**：primitive quartic 分支直接写
   \[
   W=I_A(4),\qquad \dim W=5.
   \]
   从两个 3-dimensional nets 与 common-pencil bound 只能立即得到 \(\dim W\ge5\)；等号以及 \(W=I_A(4)\) 需要额外 Hilbert-function / liaison argument。

因此，**若只看这条几何路线本身**，准确状态仍是
\[
\mathrm{CP}+\mathrm{HV}+\mathrm{CD}+\mathrm{PH}\Longrightarrow d(R)=32\text{ excluded}.
\]
plane、quadratic LD、rank-3/4 primitive factorization 等下游论证本身仍然保留且已在投稿稿中详细重写。不过本节的这些接口已被前述 Endraß 禁重 + split-MacWilliams 证书在逻辑上旁路：整个 \(d(R)=32\) 分支现已独立闭合。

## 16. 源码静态审计

在 `paper_submission/scripts/check_tex.mjs` 中加入了静态检查，并通过 `npm test` 运行；同一测试链现已加入 `verify_dR32_split_certificate.py`。当前结果包括：

```text
TeX static audit OK: 72 labels, 54 references, 36 explicit tags.
d(R)=32 exact split-MacWilliams certificate
  nonzero H-coset states : 122
  maximum certificate    : -597428248
  certificate at H       : 117963660093832
  constant * 2^17        : 131072000000000
All exact checks passed.
```

检查覆盖 duplicate labels、undefined `ref/eqref`、environment nesting、brace balance 与 duplicate explicit tags；32 分支证书则完全使用 Python integers，无浮点运算。
