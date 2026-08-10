# Residual triangle k=0：plane-16 与 image-degree 出口的新压缩

日期：2026-08-09

## 0. 状态

本笔记承接 `TRIANGLE_K0_PROOF_AUDIT_2026-08-09.md`。

旧的错误步骤是从
\[
K_Y-\phi^*K_{X'}\sim (3-m)D+\sum E_a
\]
直接读取每个 exceptional plane 的真实 transverse ramification order 为 `2`。这一点仍然 **不能使用**。

本轮不依赖该步骤，得到两类新压缩：

1. `m=4,e=4` 的 **normal** `(2,4)` target 可由法丛/横向微分 + curve Riemann--Hurwitz 排除；
2. 任意 divisorial contraction 都被压到 **plane-16 contraction**，而 plane-16 又被进一步压到 singular-line / rank-4 quadratic-complex 型。

plane-16 的最后两类 Segre/UFD 正规形已有完整候选推导，但在正式写入 `main.tex` 前仍应逐式做一次独立 paper-level audit。因此本文档状态是：

> **strong research reduction; not yet promoted as unconditional theorem in `main.tex`.**

---

## 1. 基本 six-quartic setup

Residual triangle 中
\[
Z_{AB}=A\sqcup B,\qquad
Z_{AC}=A\sqcup C,\qquad
Z_{BC}=B\sqcup C,
\qquad |A|=|B|=|C|=32,
\]
三者均为 transverse `CI(4,4,4)`，对应 determinant nets
\[
U=V_{AB},\qquad V=V_{AC},\qquad T=V_{BC}.
\]
在 `k=dim(U\cap V)=0` 情形，
\[
U\oplus V\oplus T\subset S_4,
\qquad \dim(U+V+T)=9,
\]
且九个 quartics 在 `P^3` 上无公共基点。

先只用
\[
W=U\oplus V,\qquad \dim W=6.
\]
在
\[
Y=\operatorname{Bl}_A\mathbf P^3,
\qquad
D=4H-\sum_{a\in A}E_a,
\]
六 quartics 给
\[
\phi:Y\to X'\subset Q_0^4\subset\mathbf P^5,
\]
其中 `Q_0` 为 smooth quadric fourfold，且
\[
D^3=32.
\]
写
\[
X'\sim mH_{Q_0},\qquad e=\deg\phi.
\]
则
\[
\boxed{me=16}.\tag{1.1}
\]

取两个一般 `D`-divisor 的 complete-intersection curve `C\subset Y`，有
\[
K_Y\cdot D^2=0,
\qquad
2g(C)-2=(K_Y+2D)D^2=64,
\]
故
\[
\boxed{g(C)=33}.\tag{1.2}
\]
若一般 target curve section 正常光滑，则其 genus 为
\[
(m-1)^2,
\]
Riemann--Hurwitz 给
\[
64=e\,2m(m-2)+R
=32(m-2)+R,
\]
故
\[
\boxed{R=32(4-m)\ge0,\qquad m\le4}.\tag{1.3}
\]
`m=1` 与 `dim W=6` 冲突，因此只剩
\[
\boxed{(m,e)=(2,8)\text{ 或 }(4,4)}.\tag{1.4}
\]

---

## 2. Normal `(2,4)` target 的排除

假设
\[
m=4,\qquad e=4,
\]
且 `X'` normal。此时
\[
X'=Q_0\cap H_4\subset\mathbf P^5
\]
是 type `(2,4)` complete intersection，
\[
K_{X'}\simeq\mathcal O_{X'}.
\]

每个 exceptional plane
\[
E_a\simeq\mathbf P^2
\]
由 six-quartic first jets 线性同构到 target 中一张 plane
\[
L_a\subset X'.
\]
在 type `(2,m)` complete intersection 中，plane `L\subset X'` 的 normal determinant 可由
\[
0\to N_{L/X'}\to\mathcal O_L(1)^{\oplus3}
\to\mathcal O_L(2)\oplus\mathcal O_L(m)\to0
\]
得到
\[
\det N_{L/X'}\simeq\mathcal O_L(1-m).
\]
当 `m=4` 时，横向 normal direction 的 leading differential 需要给出
\[
N_{E_a/Y}=\mathcal O_{\mathbf P^2}(-1)
\longrightarrow
N_{L_a/X'}\quad(\det\text{-degree }-3).
\]
在 rank-one transverse quotient 上，任何一阶 map
\[
\mathcal O(-1)\to\mathcal O(-3)
\]
均为零，因此 transverse order 至少二阶以上（实际局部阶数至少产生正 ramification）。

另一方面，(1.3) 在 `m=4` 时给
\[
R=0.
\]
故一般 complete-intersection curve `C` 上不能出现任何 ramification。每个 `E_a` 与一般 `C` 的交点都会贡献 positive transverse ramification，矛盾。

因此在 normal-target 假设下：
\[
\boxed{m=4,e=4\text{ impossible}.}\tag{2.1}
\]

**审计提醒。** 正式稿需把 `N_{L/X'}` 的 rank-two normal bundle 与实际 transverse quotient line 的关系写清楚，避免只从 determinant 读取局部阶数。当前论证的核心是：normal `(2,4)` target 的 transverse first derivative 无法从 `O(-1)` 落入负得更快的 normal direction，而 curve Riemann--Hurwitz 又要求总 ramification 为零。

于是 `m=4` 若还有出口，只能是
\[
\boxed{\text{nonnormal }(2,4)\text{ target}.}\tag{2.2}
\]

---

## 3. 任意 divisorial contraction 只能压到一条 line

设 Stein/birational factor 中某 irreducible divisor
\[
S\subset Y
\]
被 six-quartic map 收缩到曲线
\[
\Gamma=\phi(S).
\]
写其原像曲面在 `P^3` 中次数为 `d`，在 `A` 点的 multiplicities 为 `m_a`。由于 `D|_S` 的 image 维数为 1，
\[
D^2\cdot S=0.
\]
从 blow-up intersection 得
\[
\boxed{\sum_{a\in A\cap S}m_a=16d}.\tag{3.1}
\]
又 `m_a\le d`，因此 `S` 至少经过 16 个 `A`-点。

对任意 `a\in A\cap S`，
\[
S\cap E_a\subset E_a\simeq\mathbf P^2
\]
在 `E_a\to L_a` 的线性同构下映到同一条 target curve `Gamma`。

若 `deg Gamma>=2`，则 `Gamma` 张成唯一 target plane，故所有这些 `L_a` 必相同。由于至少 16 个 exceptional planes 映到同一 target divisor，而总 generic degree `e<=8`，不可能。

因此
\[
\boxed{\Gamma\text{ 必为一条 line}.}\tag{3.2}
\]

六 quartics 在 `S` 上只张成一个 2-dimensional restricted system，故
\[
\dim\ker\bigl(W\to H^0(S,O_S(4))\bigr)\ge4.
\]
于是 `S` 的 defining equation 必整除至少四个独立 quartics，特别
\[
\boxed{d\le4}.\tag{3.3}
\]

进一步：

- `d=4`：一个 irreducible quartic 的 degree-4 multiples 只有 1 维，不能容纳 4-dimensional kernel；
- `d=3`：由 (3.1) 需总 multiplicity 48；若 cubic singular locus 零维，无法提供如此大的 multiplicity sum；若 singular locus 正维，则进入 line/low-degree singular component，nef 约束返回低次数退化；
- `d=2`：smooth/reduced quadric 强迫全部 32 点落在 quadric 上，返回已闭合 quadratic carrier；quadric cone 的 31+vertex 边缘情形可由 restriction/Stein genus 论证排除；
- 因此唯一真正新的 contraction 是 `d=1`。

于是：
\[
\boxed{\text{new divisorial contraction}\Rightarrow
\text{a plane }P\text{ containing exactly }16\text{ points of }A,}
\tag{3.4}
\]
并且 `P~` 被收缩到一条 target line。这称为 **plane-16 contraction**。

---

## 4. Plane-16 contraction：smooth image line 被排除

设 `P` 是上述 plane，`P~\subset Y` 为 blow-up at 16 points。

其 restricted divisor
\[
L=D|_{P~}=4h-\sum_{i=1}^{16}e_i
\]
满足
\[
L^2=0,
\qquad
K_{P~}\cdot L=4,
\]
所以一般 fibre `F` 的 genus 为
\[
2g(F)-2=(K_{P~}+F)F=4,
\qquad
\boxed{g(F)=3}.\tag{4.1}
\]

在三维 birational Stein map 的横截面上，`P~` 收缩到 target line 的一般点会给 normal surface singularity，其 exceptional curve 含 genus-3 component `F`，且 normal degree可由三维法丛/adjunction 计算出负自交（clean single-component model 为 `F^2=-12`）。

若 target line 的一般点在 `X'` smooth locus，则有限 map 的二维横截面 degree 至多 `e<=8`。另一方面 normal surface singularity 的 maximal-ideal/fundamental cycle 对 genus-3、负自交 exceptional curve 给 local multiplicity 下界至少 12（若出现双 component，界更大）。这与 finite degree `<=8` 冲突。

因此
\[
\boxed{\text{plane-16 contraction 的 image line 必位于 }\operatorname{Sing}(X').}\tag{4.2}
\]

**审计提醒。** 正式稿若使用这一短证明，需要明确引用/证明 normal surface singularity 的 multiplicity lower bound。若不愿引入该理论，可改用后面的 explicit rank-4 quadratic-complex 正规形直接处理。

---

## 5. Singular image line：rank-4 quadratic-complex 正规形

在 `m=2` quadratic-complex 情形，singular line 对应 pencil 中一个 rank-4 quadric member，其 radical plane 包含该 line。

结合 finite invariant maximal-plane count 与至少 4 个 exceptional image planes 的存在，self-adjoint Jordan/Segre 分类把 singular-line finite types 压到两个主要候选：

\[
\boxed{(22)+(11)}\qquad\text{和}\qquad\boxed{(33)}.
\tag{5.1}
\]

### 5.1 `(22)+(11)` 型

取 plane equation `ell=0`。rank-4 normal form 与 plane contraction 迫使四个 non-radical quartics均被 `ell` 整除。

把第二条 independent quadratic relation 模 `ell`，得到 quotient cubics 的新乘积关系。重复 UFD/模 `ell` 降次，可迫使两个原本独立的 quartics 都成为 `ell^4` 的常数倍，违反 `dim W=6`。

故
\[
\boxed{(22)+(11)\text{ plane-16 outlet impossible}.}\tag{5.2}
\]

### 5.2 `(33)` 型

取 radical coordinates `r_1,r_2`，其余四个 quartics 写成 `ell` 乘 cubic。两条 quadratic relations 经 UFD 可压成
\[
b_1=gp,\qquad b_2=gq,
\qquad
c_1=qh,\qquad c_2=-ph,
\tag{5.3}
\]
其中
\[
\deg g+\deg p=3,
\qquad
\deg h=\deg g-1.
\]

分三种：

1. `deg g=3`：`p,q` 为常数，立即造成 quartics 线性相关；
2. `deg g=2`：`p,q` 为线性式，off-plane 的 `A`-点只能落在一条 line 与一条 conic 的并上；nef intersection 给最多
   \[
   4+8=12
   \]
   个点，少于所需 16；
3. `deg g=1`：`p,q` 为 quadrics。第二 relation 进一步给
   \[
   r_1=pa-g^2q,
   \qquad
   r_2=qa+g^2p.
   \tag{5.4}
   \]
   因而六个 quartics 全部落在 ideal `(p,q)`，于是 six-quartic system 具有公共 `CI(2,2)` curve，违反 blow-up 后 base-point-free。

因此
\[
\boxed{(33)\text{ plane-16 outlet impossible}.}\tag{5.5}
\]

结合 (5.2)(5.5)，plane-16 在 quadratic-complex singular-line 情形被排除。

---

## 6. 当前真正剩余的 k=0 出口

本轮之后，`k=0` 不应再描述成泛泛的 “ramification gap”。更准确的状态是：

### A. `m=4,e=4`

- normal `(2,4)` target：由法丛 + curve Riemann--Hurwitz 排除；
- 因而只剩
  \[
  \boxed{\text{nonnormal }(2,4)\text{ target}.}
  \]

### B. `m=2,e=8`

- positive-dimensional common-plane family：返回 rank `<=3` pencil member，再回 quadratic carrier；
- plane-16 contraction：在 singular-line rank-4 Segre 型中已压到 `(22)+(11)` / `(33)` 并排除；
- 真正剩余的是 **finite quadratic-complex 主体**：rank-4 UFD factorization 的
  \[
  \boxed{(2,2)}\qquad\text{与}\qquad\boxed{(1,3)}
  \]
  两类，以及其与第三 net `T=V_{BC}` 的 global compatibility。

因此目前最值得继续攻的不是 plane-16，而是：

\[
\boxed{
\text{nonnormal }(2,4)
\quad\text{和}\quad
m=2\text{ finite rank-4 }(2,2)/(1,3)\text{ compatibility}.}
\]

---

## 7. 投稿状态

在以下两点完成独立审计前，**不要**把 residual-32 写成已闭合：

1. Section 4 的 surface-singularity multiplicity shortcut，或者完全绕开它只用 Section 5 的 explicit Segre/UFD proof；
2. `(22)+(11)` 与 `(33)` 正规形的坐标推导逐式检查，确保没有隐含“target normal / reduced pencil member”假设。

若这两点通过，则 plane-16 outlet 可以升级为 `[T]`。即便如此，residual-32 仍需处理 Section 6 的 nonnormal `(2,4)` 与 finite rank-4 `(2,2)/(1,3)` 主体，才能真正全局闭合。
