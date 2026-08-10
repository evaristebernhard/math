# Residual triangle：higher-defect cubic candidates 的系统压缩

日期：2026-08-08

## 0. 状态说明

这份笔记继续 `TRIANGLE_FOUR_LEMMAS_RESEARCH_2026-08-08.md`。

旧数值枚举给出：在 residual triangle 的 half-`CI(4,4,4)` 对称、Macaulay O-sequence 与 common-pencil `k<=1` 之后，仍有 31 个 h-vector：

- 8 quadratic；
- 18 cubic；
- 5 primitive quartic。

本轮只处理 **18 个 cubic candidates**。

需要严格区分：

- **[旧数值事实]**：来自早期 `RESULTS.md/T16_RESULT.md` 的有限 Hilbert 枚举；
- **[旧结构输入]**：J3 conductor-sign / six-quartic map 已在 residual 36/40A comparison 中证明的通用部分；
- **[本轮新证明]**：下面的 `CI(3,3,4)` filter、unique-cubic filter、以及 `|A|=32` 的 six-quartic/J3 迁移。

---

# 1. 18 个 cubic h-vectors 的精确参数表

记

\[
\delta=h^1(I_A(4))=32-H_A(4),
\qquad
m_3=h^0(I_A(3)).
\]

由于 `I_A(2)=0`，有

\[
m_3=20-H_A(3)=10-h_3,
\qquad
h^0(I_A(4))=3+\delta.
\]

18 个 cubic candidates 的 `(delta,m_3)` 恰为

\[
\begin{array}{c|l}
\delta&m_3\\\hline
2&1\\
3&1\\
4&1,2\\
5&1,2\\
6&1,2,3\\
7&1,2,3\\
8&2,3\\
9&3,4\\
10&4\\
11&5.
\end{array}
\]

完整列表由 `scripts/verify_triangle_cubic_reduction.mjs` 精确生成。

---

# 2. 一个统一的 `CI(3,3,4)` filter

## 定理 2.1 [本轮新证明]

假设

\[
m_3\ge2
\]

且 cubic linear system `I_A(3)` **没有固定曲面因子**，即其全部成员的 polynomial gcd 为 1。

则除一个候选外，所有 cubic h-vectors 都不可能；唯一数值幸存者是

\[
\boxed{\delta=7,\quad m_3=2,}
\]

\[
\boxed{h_A=(1,3,6,8,7,5,2,0,0,0).}
\]

### 证明

取一般

\[
p_1,p_2\in I_A(3).
\]

由于 linear system 无固定 divisor，一般 pair 可取为 coprime。因此

\[
C=V(p_1,p_2)
\]

是 degree-9 complete-intersection curve（允许 reducible，但无 surface component）。

另一方面，两套 determinant nets 的和

\[
W=V_{AB}+V_{AC}\subset I_A(4)
\]

在吹起 `A` 后无基点，故 `I_A(4)` 的 projective base locus 本身至多为 `A`；特别地，没有 `C` 的 irreducible component 被所有 quartics through `A` 所包含。

因此可取

\[
q\in I_A(4)
\]

使

\[
Z=V(p_1,p_2,q)=CI(3,3,4)
\]

是零维 complete intersection，且

\[
A\subset Z,\qquad |Z|=36.
\]

记 residual scheme 为

\[
E=Z:A,\qquad |E|=4.
\]

`CI(3,3,4)` 的 h-vector 是

\[
h_{334}=(1,3,6,8,8,6,3,1),
\]

socle degree 7。因此 direct liaison 给

\[
h_E(i)=h_{334}(i)-h_A(7-i).
\]

对全部 `m_3>=2` 的 12 个 cubic candidates 逐个代入。合法 residual 必须是 length-4 O-sequence。精确检查表明：

- 11 个候选产生负项或违反 Macaulay growth；
- 唯一合法的是
  \[
  (\delta,m_3)=(7,2),
  \]
  且
  \[
  \boxed{h_E=(1,1,1,1).}
  \]

证毕。

---

# 3. 唯一 coprime-pencil survivor 的几何正规形

现在假设

\[
\delta=7,\quad m_3=2,\quad
h_A=(1,3,6,8,7,5,2).
\]

取 coprime cubics `p_1,p_2` 与 quartic `q` 如上。Residual `E` 有 h-vector `(1,1,1,1)`，故 `E` 是一条 line `L` 上的 length-4 scheme。

因为 `p_i|_L` 是 degree-3 section，而在 length 4 scheme `E` 上为零，所以

\[
p_1|_L=p_2|_L=0.
\]

于是

\[
L\subset V(p_1,p_2).
\]

令

\[
C'=V(p_1,p_2):L.
\]

则

\[
\deg C'=8.
\]

由 `(3,3)` liaison 的 genus formula，

\[
p_a(C')=7.
\]

并且 `q` 在原 `CI(3,3)` 上切出

\[
E\sqcup A,
\]

其中 `q|_L` 的零 scheme 正是 `E`，所以

\[
\boxed{A=C'\cap(q=0),\qquad \deg A=4\deg C'=32.}
\]

进一步，把 `L=(x=y=0)`，写

\[
p_1=xa+yb,
\qquad
p_2=xc+yd,
\]

其中 `a,b,c,d` 为 quadrics。则 residual degree-8 curve 的 Hilbert--Burch generator 是

\[
r_4=ad-bc,
\]

且

\[
I_{C'}=(p_1,p_2,r_4).
\]

在 degree 4，

\[
\dim I_{C'}(4)=8+1=9,
\]

而

\[
\dim I_A(4)=3+\delta=10.
\]

故

\[
I_A(4)/I_{C'}(4)
\]

恰为一维，由 `q` 的 class 生成。

对任意 determinant net `U\subset I_A(4)`，

\[
\dim(U\cap I_{C'}(4))\ge2.
\]

若为 3，则整个 net vanishes on `C'`，与其 base locus 为零维 `CI(4,4,4)` 矛盾；因此恰为 2。

所以这个唯一数值幸存者已经被压成非常具体的模型：

> degree-8 genus-7 ACM curve `C'`，由 `(3,3)` complete intersection residual to a line 得到；`A` 是 `C'` 上的 quartic divisor；每个 weight-64 determinant net 有二维子空间在 `C'` 上恒为零。

在 `C'` 上 determinant relation 退化为一元 quadratic：

- 若该一元 quadratic coefficient 非零，则
  \[
  F|_{C'}=c\,q^2,
  \]
  即 `X∩C'=2A`；
- 若 coefficient 为零，则
  \[
  C'\subset X.
  \]

因此这个 survivor 最终只剩一个 **degree-8 contact/contained-curve outlet**。

---

# 4. Unique cubic candidates 的 `CI(3,4,4)` filter

现在 `m_3=1`，令唯一 cubic 为

\[
p=0.
\]

由于

\[
\dim I_A(4)=3+\delta,
\qquad
\dim pS_1=4,
\]

quotient

\[
I_A(4)/pS_1
\]

的维数为

\[
\delta-1.
\]

当 `delta>=3` 时，可以取两个 mod-`pS_1` independent quartics `s,t`，且利用 `I_A(4)` 的有限 base locus取到

\[
CI(3,4,4)=V(p,s,t)
\]

包含 `A`。其 residual length 为 16。

`CI(3,4,4)` 的 h-vector 为

\[
h_{344}=(1,3,6,9,10,9,6,3,1).
\]

逐 candidate liaison 计算得到：

\[
\begin{array}{c|c|c}
\delta&h_T&\text{O-sequence?}\\\hline
3&(1,3,5,7)&\text{yes}\\
4&(1,3,5,6,1)&\text{yes}\\
5&(1,3,5,5,2)&\text{yes}\\
6&(1,3,5,4,3)&\text{yes}\\
7&(1,3,5,3,4)&\text{no}.
\end{array}
\]

因此

\[
\boxed{m_3=1,\ \delta=7\text{ impossible}.}
\]

`delta=2` 早已由 defect-two analysis 排除。

故 unique-cubic higher-defect candidates 只剩

\[
\boxed{\delta=3,4,5,6.}
\]

## 4.1 `delta=4,5,6` 的二级 residual

对 `delta=4,5,6`，上面的 residual 16-point scheme `T` 都满足

\[
\dim I_T(2)=1.
\]

令唯一 quadric 为 `h=0`。在 `p` 不含 `h` 且可选 quartic `q` 使 `(h,p,q)` 为 regular sequence 的 clean 情形，取

\[
CI(2,3,4)=V(h,p,q)
\]

包含 `T`，其 residual `R` 长度为 8。精确 liaison 给：

\[
\begin{array}{c|c}
\delta&h_R\\\hline
4&(1,3,4)\\
5&(1,3,3,1)\\
6&(1,3,2,2).
\end{array}
\]

其中

\[
\boxed{\delta=5:\quad h_R=(1,3,3,1)=h_{CI(2,2,2)}.}
\]

所以 `delta=5` 被压到一个非常刚性的 eight-point `CI(2,2,2)` residual。

对 `delta=6`，`R` 有至少两个独立 quadrics。若可取第二 quadric `h'` 与 `h`、某 cubic 构成 `CI(2,2,3)`，则 residual length-4 scheme 的 h-vector 被迫为

\[
(1,1,2),
\]

违反 Macaulay growth。因此

\[
\boxed{\delta=6\text{ 的 clean generic quadratic system 不可能};}
\]

剩余只能是 quadrics 有固定 component / nonregular low-degree outlet。

这些数值由 `scripts/verify_triangle_unique_cubic_nested.mjs` 精确验证。

---

# 5. `delta=3`, unique cubic：non-contact subcase 与 contact subcase

这是一个额外的本轮新证明。

当

\[
\delta=3,\qquad m_3=1,
\]

有

\[
\dim I_A(4)=6,
\qquad
\dim I_A(4)/pS_1=2.
\]

任一 determinant net `U` 不可能含两个 independent `pS_1` elements：否则两 quartics 均含 factor `p`，与第三 quartic 共同产生正维 base locus。因此

\[
\dim(U\cap pS_1)=1,
\]

且 `U` 映满二维 quotient。第二个 net `V` 同理。

若 kernel line 对 ternary determinant quadratic form 是 **non-isotropic**，则在共同 quotient basis `s,t` 下，两 nets 可正规化为

\[
U=\langle s+pa,\ pb,\ t+pc\rangle,
\]

\[
V=\langle s+pa',\ pb',\ t+pc'\rangle,
\]

其中 `a,b,c,a',b',c'` 为 linear forms，且

\[
F=(s+pa)(t+pc)-(pb)^2
 =(s+pa')(t+pc')-(pb')^2.
\]

相减并除以 `p`：

\[
(a-a')t+(c-c')s
+p(ac-b^2-a'c'+b'^2)=0. \tag{5.1}
\]

`(p,s,t)` 是 `(3,4,4)` regular sequence；否则在 `p=0` 上 `s=t=0` 的 curve 会成为 determinant net 的 base curve。

而 (5.1) 是 total degree 5 的 syzygy，其 coefficient degrees 为 `(2,1,1)`。Koszul syzygies of a `(3,4,4)` regular sequence start in total degrees 7,7,8。因此不存在非零 degree-5 syzygy。故

\[
a=a',\qquad c=c',\qquad b'=\pm b,
\]

于是两 nets 相同，矛盾。

所以：

\[
\boxed{\delta=3,m_3=1\text{ 的 non-contact subcase 不存在}.}
\]

### 剩余 isotropic/contact subcase

若 kernel line 是 isotropic，则在 `p=0` 上 binary determinant drops to rank one：

\[
F|_{p=0}=q_4^2.
\]

即 `p` 是 contact cubic。由于 `F mod p` 是同一个 intrinsic binary form，两个 nets 同时处于该 subcase。

因此 non-contact subcase 已排，只需分析 contact cubic 的 `t=0/16`。

## 5.1 Contact `t=16`

此时 residual 16-point scheme `T` 的 h-vector 为

\[
h_T=(1,3,5,7).
\]

故

\[
\dim I_T(2)=10-(1+3+5)=1.
\]

令唯一 quadric 为 `h=0`。又

\[
H_T(3)=16,
\qquad
\dim I_T(3)=20-16=4.
\]

而 `hS_1` 已是 4 维，因此

\[
\boxed{I_T(3)=hS_1.}
\]

原 contact cubic `p` 经过 `T`，所以

\[
p=h\ell
\]

对某 linear form `ell`。由 contact equation

\[
F=q^2+pG_5
\]

可知在 `h=0` 上

\[
F=q^2.
\]

因此 `h=0` 是 contact quadric。若 `h` reduced，则 Endraß contact-quadric theorem 给 weight 48 strict even set，与 `d(K)=64` 矛盾。若 `h` reducible/nonreduced，则进入 contact-plane / double-plane 的低次退化，需要使用既有 weak-even compatibility 处理。

所以 `t=16` 的 clean reduced 情形闭合。

## 5.2 Contact `t=0`

公共 28 点块 `D` 由 `CI(3,4,5)` liaison 得到

\[
h_D=(1,3,6,8,9,1,0,\ldots).
\]

于是

\[
\dim I_D(3)=2,
\qquad
\dim I_D(4)=8.
\]

取两个 independent contact cubics `p_1,p_2`。在 clean 情形假设

\[
C=V(p_1,p_2)
\]

是 integral `(3,3)` curve。写两套 contact equations

\[
F=q_1^2+p_1g_1=q_2^2+p_2g_2.
\]

限制到 `C` 有

\[
q_1^2=q_2^2.
\]

由于 `C` integral，可整体选择一个符号，使

\[
q_1-q_2\in I_C(4).
\]

而 `(p_1,p_2)` 是 regular sequence，所以

\[
I_C(4)=p_1S_1+p_2S_1.
\]

故存在 linear forms `a,b` 使

\[
q_1-q_2=p_1a+p_2b.
\]

令

\[
Q=q_1-p_1a=q_2+p_2b.
\]

则 `F-Q^2` 同时被 `p_1,p_2` 整除；互素性给

\[
\boxed{F=Q^2+p_1p_2h_2}
\]

对某 quadric `h_2`。若 `h_2=0`，则 `F` 是平方，排除；故 `h_2` 非零，并且在 `h_2=0` 上 `F=Q^2`。于是又得到 contact quadric。

因此 `t=0` 的 integral/coprime clean 情形也返回 weight-48 contradiction；reducible `C`、componentwise sign-changing 与 nonreduced quadric 是明确的剩余低次退化。

综上：

\[
\boxed{\delta=3,m_3=1\text{ 的 clean/reduced 情形全部闭合}.}
\]

---

# 6. Cubic system 有固定 divisor 时的初步压缩

前面的 `CI(3,3,4)` theorem 假设 `gcd I_A(3)=1`。若有 fixed divisor，因 degree 3，只可能是 plane / quadric / cubic。

- cubic fixed divisor就是 `m_3=1` unique-cubic case；
- fixed quadric：`I_A(3)=q\cdot L`，`L\subset S_1`；
- fixed plane：`I_A(3)=\ell\cdot V_2`。

## 6.1 Fixed quadric

若 `dim L=m_3`：

- `m_3=4` 时 `L=S_1`，所以全部 `A` 都在 `q=0`，回到 quadratic carrier，已排；
- `m_3=3` 时，除至多一个点外全部 `A` 在 `q=0`。

在后者若恰有一个点不在 `q`，则 quadric contains 31 points of `A`。在 quadric strict transform 上

\[
L_Q=4H-\sum_{31}E_i,
\qquad
L_Q^2=32-31=1.
\]

`W=V_{AB}+V_{AC}` 在吹起 `A` 后 base-point free，所以其 restriction 定义 morphism。由于 `L_Q^2=1`，image 必为 degree-one surface and map degree one，即 birational to a plane。可是

\[
K\cdot L_Q=-16+31=15,
\]

从而一般 member 的 arithmetic genus

\[
p_a=1+\frac{L_Q^2+K\cdot L_Q}{2}=9,
\]

不可能是 plane line 的 birational transform。故该 case 也不发生。

因此 fixed-quadric 情形只需继续审计 `m_3=2`（以及 reducible/singular quadric variants）。

## 6.2 Fixed plane

若所有 cubics 有 common plane factor `ell`，则 off-plane points lie in the common zero locus of a system of quadrics。由 plane strict transform 的 nef intersection，任一 plane 最多含 16 个 `A` points，因此至少 16 点位于 residual quadric base locus。这个 outlet 目前尚需单独 Hilbert/liaison 分类，不能直接称为已闭合 plane-LD。

---

# 7. `k=0` six-quartic outlet：J3 在 `|A|=32` 的新迁移

这是本轮最重要的结构归约之一。

设

\[
k=\dim(V_{AB}\cap V_{AC})=0.
\]

则

\[
W=V_{AB}\oplus V_{AC},\qquad \dim W=6.
\]

两个 ternary determinant quadratics 都 rank 3，且作用在 complementary 3-spaces。因此它们的差

\[
Q_0=Q_{AB}-Q_{AC}
\]

在 `W` 上 rank 6，定义 smooth

\[
Q^4=(Q_0=0)\subset P^5.
\]

六 quartics 给 morphism

\[
\phi:Y=Bl_A P^3\to X'\subset Q^4,
\qquad D=4H-\sum_{a\in A}E_a.
\]

因为

\[
D^3=64-32=32>0,
\]

image 三维，`phi` generically finite。

## 7.1 Degree equation

写

\[
X'\sim mH_Q,
\qquad \deg(\phi)=e.
\]

则

\[
\boxed{2me=D^3=32,\qquad me=16.} \tag{7.1}
\]

## 7.2 Conductor-sign bound `m<=3`

旧 J3 的 canonical formula 对任意 `|A|` 都保持同样形式：

\[
K_Y-\phi^*K_{X'}=(3-m)D+\sum E_a. \tag{7.2}
\]

每个 exceptional plane coefficient 恰为 `+1`。

沿 normalization conductor，若 `E_a` 支配 conductor divisor，canonical coefficient 应为

\[
(e_T-1)-e_Tc_T\le-1,
\]

与 `+1` 矛盾。因此 exceptional planes 不支配 conductor，generic point of every image plane lies in the normal smooth locus of `X'`。

横向 ramification index由 coefficient `+1` 给

\[
r_a=2.
\]

而

\[
N_{L_a/Y}\sim O(-1),
\qquad
N_{L_a/X'}\simeq O_{P^2}(1-m),
\]

leading transverse jet 给 nonzero map

\[
O(-2)\to O(1-m).
\]

故

\[
\boxed{m\le3.} \tag{7.3}
\]

结合 `me=16`，只有

\[
(m,e)=(1,16),\quad(2,8).
\]

但 `m=1` 意味 image contained in a hyperplane section of `Q^4`，即六个 sections有线性关系，与 `dim W=6` 矛盾。因此

\[
\boxed{m=2,\qquad e=8.} \tag{7.4}
\]

所以

\[
\boxed{X'=Q_0\cap Q_1\subset P^5}
\]

是两个 quadrics 的 intersection。

---

# 8. 32 exceptional planes 强迫 quadratic pencil 有 corank >=2 成员

每个 exceptional plane `E_a` 线性同构到一个 maximal plane

\[
L_a\subset Q_0^4.
\]

而 `L_a\subset X'`，所以第二个 quadric `Q_1` 也在 `L_a` 上恒为零。

令 `b_0,b_1` 为相应 symmetric bilinear forms，定义

\[
T=b_0^{-1}b_1.
\]

因为 `L_a` 对 `b_0` maximal isotropic，

\[
L_a=L_a^{\perp_{b_0}}.
\]

又 `b_1|_{L_a}=0`，故

\[
b_0(Tx,y)=0\quad(x,y\in L_a),
\]

所以

\[
\boxed{T(L_a)\subset L_a.}
\]

即每个 exceptional plane 都对应一个 `T`-invariant 3-dimensional subspace。

先注意不同 exceptional divisors 未必映到不同 plane。这里可以用覆盖次数控制 multiplicity。由 (7.4)，`phi` 的 generic degree 是 8；而每个 exceptional plane 横向 ramification index 是 2。若有 `t` 个 exceptional planes 映到同一个 image plane `L`，则在 `L` 的一般点上它们对 generic fibre degree 至少贡献 `2t`，故

\[
2t\le8,
\qquad t\le4.
\]

因此 32 个 exceptional divisors 至少产生

\[
\boxed{8\text{ 个不同的 maximal planes }L_a\subset X'.} \tag{8.0}
\]

## Lemma 8.1 [本轮新线性代数引理]

若 pencil

\[
Q_1-\lambda Q_0
\]

的每个成员 corank 至多 1，则 `T` 每个 eigenvalue 的 geometric multiplicity 至多 1。因此每个 generalized eigenspace `V_\lambda` 是单个 Jordan block。不同 `V_\lambda` 因 `T` self-adjoint 而彼此 `b_0`-正交，并且各自的限制配对非退化。

设 `L` 是一个 `T`-invariant maximal `b_0`-isotropic 3-space。Primary decomposition 给

\[
L=\bigoplus_\lambda L_\lambda,
\qquad L_\lambda=L\cap V_\lambda.
\]

在单个 Jordan block `V_\lambda` 中，每个维数至多只有一个 invariant subspace；若 `L_\lambda` isotropic，则

\[
\dim L_\lambda\le\frac12\dim V_\lambda.
\]

求和并使用

\[
\dim L=3=\frac12\dim V
\]

可知每个不等式都必须取等号。因此所有 primary block 都必须为偶维，而且每个 `L_\lambda` 都是该 block 中唯一的 half-dimensional invariant subspace。于是

\[
\boxed{\text{regular self-adjoint }T\text{ 至多有一个 invariant maximal isotropic 3-space}.}
\]

但 (8.0) 给出至少 8 个不同的这种 planes，矛盾。

故 pencil 中存在

\[
\boxed{\operatorname{corank}Q_\lambda\ge2,}
\]

也就是

\[
\boxed{\operatorname{rank}Q_\lambda\le4.} \tag{8.1}
\]

这把整个 `k=0` six-quartic outlet 统一压到一个 **rank<=4 quadratic relation among six quartics**。

## 8.2 Rank 4 / rank 3 正规形

rank 1 或 2 的 quadratic relation 在代数闭域上分解为一个平方或两个线性形式之积；代入六个线性无关 quartics 后，在整环 `S` 中会强迫一个非零线性组合恒为零，与 `dim W=6` 矛盾。因此只需 rank 3 或 4。

### Rank 4

经 `GL(W)` 变换可写

\[
f_1f_2=f_3f_4,
\]

另外两坐标 `f_5,f_6` 位于 radical directions。UFD 分解给

\[
f_1=ab,\qquad f_3=ac,\qquad f_2=cd,\qquad f_4=bd,
\]

其中

\[
\deg a=\deg d=\alpha,
\qquad
\deg b=\deg c=\beta,
\qquad
\alpha+\beta=4.
\]

若 `alpha=0` 或 `4`，上述四个 quartics 中出现成比例 pair，违反线性无关性；故

\[
\boxed{\{\alpha,\beta\}=\{1,3\}\quad\text{或}\quad\{2,2\}.}
\]

前四个 quartics 的公共零 locus 是

\[
V(a,d)\cup V(b,c).
\]

因此：

- `(2,2)` 型给两条 `CI(2,2)` degree-4 curves；
- `(1,3)` 型给一条 line `V(a,d)` 与一条 `CI(3,3)` degree-9 curve。

真正的 32 点 base scheme 还要再与 `f_5=f_6=0` 相交，所以不能像 five-quartic case 那样直接写出 `32=4(alpha^2+beta^2)`；这里需要研究 `f_5,f_6` 在上述两条曲线上的共同零 divisor。这个 distinction 很重要。

### Rank 3

正规形为

\[
f_1f_2=f_3^2.
\]

UFD 给

\[
f_1=ha^2,\qquad f_3=hab,\qquad f_2=hb^2.
\]

因三式均为 quartic，

\[
\deg h+2\deg a=4,
\]

所以只有：

1. `deg h=0`, `deg a=deg b=2`：前三个 quartics 在 `CI(2,2)` curve `V(a,b)` 上全消失；
2. `deg h=2`, `deg a=deg b=1`：前三个 quartics 共享一个 quadric surface `h=0`，并另有一条 line `V(a,b)`；
3. `deg h=4` 会使 `a,b` 为常数，三 quartics 只张成一维，排除。

故 rank-3 outlet 已经明确返回 quadratic curve / quadric-surface geometry。

因此 `k=0` 的真正新内容集中在 rank-4 的 `(1,3)` 与 `(2,2)` 两个 factorization 类型，以及 radical quartics `f_5,f_6` 的 compatibility；这比原来的抽象 six-quartic outlet 明显更窄。

---

# 9. 当前 18 个 cubic candidates 已压成什么？

经过本轮，可把原 18 个 cubic h-vectors 压成以下真正的几何 outlets。

### A. Unique cubic

数值上只剩 `delta=3,4,5,6`，但结构已经进一步压缩：

- `delta=3`：non-contact 已排；contact `t=0/16` 的 clean/reduced 情形也返回 contact quadric，因此只剩 reducible/sign-changing/nonreduced 低次退化；
- `delta=4`：二级 residual 是 length-8 scheme `h=(1,3,4)`；
- `delta=5`：二级 residual 精确为 `CI(2,2,2)`；
- `delta=6`：generic `CI(2,2,3)` continuation 产生非法 `(1,1,2)`，所以只剩 quadratic system 有 fixed component 的退化。

因此 unique-cubic 真正值得继续研究的主模型主要是 `delta=4,5`，加上 `delta=6` 的 fixed-component 分类。

### B. Cubic pencil with no fixed divisor

唯一可能：

\[
\boxed{\delta=7,m_3=2,}
\]

且强制为 degree-8 genus-7 residual curve model。

### C. Fixed low-degree divisor in cubic system

只剩：

- fixed plane；
- fixed quadric 的 `m_3=2` / singular-reducible variants。

### D. `k=0` six-quartic comparison

无论 h-vector，统一归约到

\[
\boxed{rank\le4\text{ quadratic relation}.}
\]

这说明原来“18 个 higher-defect cubic candidates”不是 18 个独立问题；真正值得继续攻的是上述 4 类结构。

---

# 10. 下一步最优入口

优先级建议：

1. **rank<=4 six-quartic relation + base length 32**：利用 UFD factorization 与两个 determinant 3-planes 的特殊 block structure，尝试证明只可能回到已闭合 `16+16 quadratic compatibility` 或 degree-8 residual-curve model。
2. **unique cubic delta=4,5,6**：利用 `CI(3,4,4)` residual 16-point schemes，它们全部落在唯一 quadric 上，继续做 quadric-surface Hilbert/Stein analysis。
3. **delta=3 contact t=0/16**：重新用本轮恢复的 h-vectors，而不是 defect-two 的 `11 vs 10`，分析 residual 16/28 schemes。
4. **fixed-plane/fixed-quadric cubic systems**：作为低次 fixed-divisor outlet 单独分类，避免再与“A 整体落在 plane/quadric”混为一谈。

当前不应再把 residual triangle 的 gap 描述成 `CP/HV/CD/PH`；更准确的是上面四个 higher-defect geometric outlets。
