# d(R)=32 residual triangle：直接的 k=1 / k=0 路线

日期：2026-08-08

## 0. 目的

本笔记刻意停止 quartic defect \(\delta\) 的逐候选枚举，回到 d(R)=32 分支本身的三角结构：

\[
Z_{AB}=A\sqcup B,
\qquad
Z_{AC}=A\sqcup C,
\qquad
Z_{BC}=B\sqcup C,
\qquad |A|=|B|=|C|=32,
\]

三者都是 reduced transverse \(CI(4,4,4)\)，并分别有三维 determinant nets

\[
U:=V_{AB},\qquad V:=V_{AC},\qquad T:=V_{BC}.
\]

令

\[
k:=\dim(U\cap V).
\]

已证明 common-pencil bound \(k\le1\)。因此只需处理 \(k=1\) 与 \(k=0\)。

本轮结论：

1. \(k=1\) 有一个不依赖 Hilbert defect 的短证明，直接排除；
2. \(k=0\) 可迁移 J3 conductor/degree 论证到一个 \((2,2)\subset P^5\) 的 target；
3. target 的 common-plane 数量强迫 quadric pencil 出现 corank \(\ge2\)；
4. 若继续分类 pencil，hard case 是三个 2-dimensional eigenspaces 的 toric eight-plane model；它的 polynomial factorization 已经把问题压到 degree \(\le2\) Smith/contact compatibility。

因此 d(R)=32 的真正问题不应再写成 31 个 h-vector，而是一个单一的 k=0 low-rank compatibility lemma。

---

# 1. 三个 net 的基本直接和结构

因为

\[
I_{A\cup B}(4)=U,
\qquad
I_{A\cup C}(4)=V,
\qquad
I_{B\cup C}(4)=T,
\]

且三个 64 点集都是 \(CI(4,4,4)\)，每个 degree-4 ideal piece 恰为对应的三维 net。

若

\[
u+v+t=0,
\qquad u\in U,\ v\in V,\ t\in T,
\]

限制到 A 得 \(t|_A=0\)。由于 \(t\) 本来就在 \(I_{B\cup C}(4)\)，所以

\[
t\in I_{A\cup B\cup C}(4)
=U\cap T.
\]

在 k=0 情形，pairwise symmetry 给三个 pairwise intersections 都为 0，因此 \(t=0\)，继而 \(u=v=0\)。故

\[
\boxed{U\oplus V\oplus T\subset S_4,\qquad \dim(U+V+T)=9.}
\]

而三个 net 的 base loci 的三重交为空：

\[
(A\cup B)\cap(A\cup C)\cap(B\cup C)=\varnothing.
\]

所以九个 quartics 在 \(P^3\) 上构成 base-point-free system。这是 k=0 独有的全局额外结构。

---

# 2. k=1 的短证明：完全不需要 quartic defect

假设

\[
U\cap V=\langle q\rangle,
\qquad \deg q=4.
\]

令

\[
W=U+V,\qquad \dim W=5.
\]

在

\[
Y=Bl_A P^3,
\qquad
D=4H-\sum_{a\in A}E_a,
\]

W 无基点，且每个 exceptional plane \(E_a\simeq P^2\) 由 first jets 线性同构到 \(P(W^*)\) 中的一张 plane。

两套 determinant identities 给两个 rank-3 ternary quadratic forms

\[
F=Q_U=Q_V.
\]

所以

\[
R:=Q_U-Q_V
\]

是 W 上的非零 quadratic relation。它的零 quadric包含 \(\phi(E_a)\simeq P^2\)。smooth quadric threefold \(Q^3\subset P^4\) 不含 plane，因此

\[
\boxed{\operatorname{rank}R\le4.}
\]

下面只看 common line \(\langle q\rangle\) 对两个 ternary forms 是 isotropic 还是 non-isotropic。

## 2.1 q 对两边都 non-isotropic

完成平方并把 binary residual forms 分解后可写

\[
F=\lambda q^2+u_1u_2
=\mu q^2+v_1v_2,
\]

其中

\[
U=\langle q,u_1,u_2\rangle,
\qquad
V=\langle q,v_1,v_2\rangle.
\]

若 \(\lambda\ne\mu\)，relation

\[
(\lambda-\mu)q^2+u_1u_2-v_1v_2=0
\]

在五个独立 coordinates 上 rank 5，与 rank \(\le4\) 矛盾。因此

\[
\lambda=\mu
\]

且

\[
\boxed{u_1u_2=v_1v_2.}
\]

由于任一 determinant net 的 base locus 是 zero-dimensional CI，\(u_1,u_2\) 及 \(v_1,v_2\) 均无公共曲线因子。UFD 因而给

\[
u_1=ab,
\qquad
u_2=cd,
\qquad
v_1=ac,
\qquad
v_2=bd,
\]

并有

\[
\deg a=\deg d=\alpha,
\qquad
\deg b=\deg c=\beta,
\qquad
\alpha+\beta=4.
\]

\(\alpha,\beta\ne0\)，否则 U=V 或出现 base surface。

共同 base A 是

\[
A=V(q,a,d)\cup V(q,b,c)
\]

（clean case；若出现 common components，则已经是更低次数 degeneration）。两个 pieces 的 complete-intersection lengths 为

\[
4\alpha^2,
\qquad
4\beta^2.
\]

若 \(\{\alpha,\beta\}=\{1,3\}\)，这两个 lengths 是 4 与 36；它们的 overlap 在由两个 linear factors 决定的 line 上最多为 3，除非产生 positive-dimensional base locus。因此 union 长度至少 37，与 \(|A|=32\) 矛盾。

故

\[
\boxed{\alpha=\beta=2.}
\]

于是 a,b,c,d 都是 quadrics，并且

\[
F=\lambda q^2+abcd.
\]

在 \(a=0\) 上

\[
F=\lambda q^2.
\]

\(\lambda=0\) 会使 F reducible，所以 \(\lambda\ne0\)。因此 \(a=0\) 是 contact quadric。若 reduced，Endraß contact-quadric theorem 给 weight-48 strict even set，与 minimum weight64 矛盾；reducible/nonreduced cases进入既有 contact-plane/double-plane compatibility。

所以 non-isotropic case 排除。

## 2.2 mixed isotropic / non-isotropic

一边可正规化为

\[
qu+v^2,
\]

另一边为

\[
\lambda q^2+xy.
\]

两者之差在五维 W 上 rank 5，与 rank \(\le4\) 矛盾。

## 2.3 q 对两边都 isotropic

可写

\[
F=qu+v^2=qu'+(v')^2.
\]

故

\[
(v-v')(v+v')=q(u'-u).
\]

若 quartic q irreducible，则 q 必整除 \(v-v'\) 或 \(v+v'\)。因双方 degree4，得到

\[
v'=\pm v+cq
\]

进而 \(u'\in\langle q,u,v\rangle\)，所以 U=V，矛盾。

因此 q reducible。任一 reducible quartic 有 degree1 或2 的因子 r。限制到 \(r=0\)：

\[
F=v^2.
\]

故 r 是 contact plane 或 contact quadric，返回已排除低重量 geometry。

结论：

\[
\boxed{k=1\text{ 无条件排除（在既有 contact-plane/quadric literature input 下）}.}
\]

---

# 3. k=0：six-quartic map

现在

\[
U\cap V=0,
\qquad
W_A:=U\oplus V,
\qquad \dim W_A=6.
\]

两个 determinant forms 的差

\[
Q_0:=Q_U-Q_V
\]

在 U 与 V 两个 complementary 3-spaces 上分别 nondegenerate，故

\[
\operatorname{rank}Q_0=6.
\]

于是

\[
Q_0^4=(Q_0=0)\subset P^5
\]

是 smooth quadric fourfold。

在

\[
Y_A=Bl_A P^3,
\qquad
D=4H-\sum_AE,
\]

六 quartics 给 morphism

\[
\phi_A:Y_A\to X_A'\subset Q_0^4.
\]

因为

\[
D^3=64-32=32>0,
\]

map generically finite。

写

\[
X_A'\sim mH_Q,
\qquad
\deg\phi_A=e.
\]

则

\[
2me=D^3=32,
\qquad me=16.
\]

J3 conductor-sign 计算只依赖 blow-up canonical formula，不依赖 common block 是 28 还是 32：

\[
K_{Y_A}-\phi_A^*K_{X_A'}=(3-m)D+\sum_AE_a. \tag{K0.1}
\]

这里必须把 `D` 理解为一般 hyperplane pullback 的实际 divisor，而不能把线性等价类 `D=4H-\sum E_a` 展开后读取 exceptional coefficient。一般 hyperplane 不包含 image plane `L_a`，所以其 pullback `D` 不包含 `E_a`；因此 (K0.1) 沿每个 `E_a` 的真实 coefficient 确实是

\[
\boxed{+1}.
\]

若 `E_a` 支配 normalization conductor，局部 canonical coefficient 为 `(r-1)-rc\le-1`，矛盾。因此 `E_a` 的一般像点位于 normal smooth locus，并且横向 ramification index满足

\[
r_a-1=1,
\qquad
\boxed{r_a=2}. \tag{K0.2}
\]

又有

\[
N_{E_a/Y_A}=O_{P^2}(-1),
\qquad
N_{L_a/X_A'}=O_{P^2}(1-m).
\]

leading transverse jet 给 nonzero map

\[
O_{P^2}(-2)\longrightarrow O_{P^2}(1-m),
\]

故

\[
\boxed{m\le3}. \tag{K0.3}
\]

与 `me=16` 联立，仅有

\[
(m,e)=(1,16),(2,8).
\]

`m=1` 意味 image 落在 hyperplane section，等价于六 quartics 有线性关系，与 `U\oplus V` 矛盾。因此

\[
\boxed{m=2,\quad e=8,\quad X_A'=Q_0\cap Q_1\subset P^5.} \tag{K0.4}
\]

---

# 4. 至少八张 common planes

每个 `E_a` 线性同构到 `Q_0` 中 maximal plane `L_a`，并且 `L_a\subset X_A'`。不同 `E_a` 未必给不同 `L_a`；但 generic cover degree 是 8，而每个 `E_a` 沿 `L_a` 的 transverse local degree 是 2。因此若 `t` 张 exceptional planes 映到同一 `L`，则

\[
2t\le8,
\qquad t\le4.
\]

32 张 `E_a` 因而给至少八张不同 common maximal planes：

\[
\boxed{\#\{L_a\}\ge8.} \tag{K0.5}
\]

令

\[
T=Q_0^{-1}Q_1
\]

为 `Q_0`-self-adjoint operator。common maximal planes 正好对应 `T`-invariant maximal isotropic 3-spaces。

若每个 pencil member corank至多1，则每个 eigenvalue 的 geometric multiplicity至多1；primary block为 cyclic。一个 cyclic self-adjoint primary block在给定维数上至多有一个 invariant subspace，而 maximal isotropic half-space若存在也唯一。因此整个 operator至多有一个 invariant maximal isotropic 3-space，与 (K0.5) 矛盾。

所以 pencil 必出现

\[
\boxed{\operatorname{corank}(Q_1-\lambda Q_0)\ge2.} \tag{K0.6}
\]

---

# 5. clean finite rank-4 case：eight-plane toric model 直接矛盾

先处理 pencil 的 finite-plane clean case：没有 rank\(\le3\) member，也没有 positive-dimensional family of common planes。为了拥有至少8张 invariant maximal isotropic planes，self-adjoint primary decomposition只能达到 extremal pattern

\[
V=V_1\oplus V_2\oplus V_3,
\qquad \dim V_i=2,
\]

三个 block 对应三个不同 eigenvalues；每个 hyperbolic 2-space有两条 isotropic eigenlines，因此恰有

\[
2^3=8
\]

张 common maximal planes。取 isotropic coordinates后，intersection具有 toric normal form

\[
x_1y_1=x_2y_2=x_3y_3. \tag{K0.7}
\]

pullback 到 `P^3` 后，六 quartics满足

\[
X_1Y_1=X_2Y_2=X_3Y_3. \tag{K0.8}
\]

对共同 degree-8 product 做 UFD。每个 irreducible factor按照它在三组 factorization 中落入 `X_i` 还是 `Y_i`，得到 cube atoms

\[
G_\varepsilon,\qquad \varepsilon\in\{0,1\}^3.
\]

对 coordinate plane `L_\varepsilon`，其三个 defining coordinates 的 gcd 正是 `G_\varepsilon`。若 `G_\varepsilon` 非常数，则 divisor `(G_\varepsilon=0)` 被 `\phi_A` 映入 `L_\varepsilon`；在 clean finite 情形它给一个非exceptional divisor dominating该 plane，因此对 generic fibre over `L_\varepsilon` 贡献正的额外 degree。

但 (K0.5) 与“总共只有8张 common planes”一起迫使：

- 八张 plane 全部都是 exceptional image planes；
- 32 张 `E_a` 必须平均且实际上恰好四张映到每一 `L_\varepsilon`；
- 每张 plane 的 generic degree 已由 exceptional sheets 完全用满：
  \[
  4\times2=8=e.
  \]

因此任何 nonconstant atom 都不可能存在。

另一方面 (K0.8) 的共同 product有 degree8，不可能所有 atoms均为常数。矛盾。

故

\[
\boxed{\text{clean finite rank-4 }k=0\text{ case is impossible}.} \tag{K0.9}
\]

这个矛盾比先把 atom 识别成 Smith/contact divisor更直接。

---

# 6. 剩余只是真正的 low-degree degeneration

因此 `k=0` 不再有一般 six-quartic 主分支。剩下的只有上述 clean finite classification 的退化边界：

1. pencil 出现 rank\(\le3\) member；
2. common maximal planes形成 positive-dimensional family；
3. 某个 atom divisor不 dominant，而被 map 收缩到 curve/point；
4. toric factorization出现 nonreduced/common-component degeneration。

rank\(\le3\) 时 quadratic relation 的 UFD normal form 是

\[
f_1f_2=f_3^2,
\qquad
f_1=ha^2,\ f_2=hb^2,\ f_3=hab,
\]

所以立即出现 quadric factor、`CI(2,2)` curve，或更低次数 common component。若 degree-1/2 factor的 divisor仍二维映到 target plane，则前面的 covering-degree记账把它送入 low-degree relative-factor 情形；若其像降维，则在相应 plane/quadric strict transform 上 restricted quartic system发生 contraction，正是旧 d(R)=32 专属的 low-degree degeneration 接口。

因此当前真正需要补严的已经不是 31 个 Hilbert candidates，而是一个很小的统一返回句：

> **K0-LD return.** 上述 rank\(\le3\)、positive-family、non-dominant atom 或 nonreduced degeneration，必返回已闭合的 plane/quadric carrier、contact plane/quadric，或 determinant net 的 positive-dimensional base locus。

这正是旧审计稿用一句“返回 low-degree degeneration”压掉的部分；现在至少 clean finite 主分支已经完全独立闭合。

---

# 7. 审计结论

- 旧 split-MacWilliams closure 仍然不能无条件使用，因为它错误删除 octic allowed weights 88,96,104,112；
- 但“32 分支原来不难”的几何直觉基本正确：
  - `k=1` 有短的 rank-4/UFD/contact-quadric proof；
  - `k=0` 的 clean finite主分支由 conductor + eight-plane count + toric degree saturation直接排除；
  - 只剩 low-degree degeneration 的统一返回接口，而不是 higher-defect Hilbert 分支树。
- 最终论文应按 `k=1/k=0` 写主证明，Hilbert枚举仅保留为审计附录。
