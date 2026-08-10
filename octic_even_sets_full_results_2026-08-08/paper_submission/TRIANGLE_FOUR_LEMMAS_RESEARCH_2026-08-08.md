# Residual triangle 四个旧引理的恢复与重证

日期：2026-08-08

## 0. 结论先行

原先标记的四个接口为：

- **CP**: `common-pencil`，即 `k = dim(V_AB ∩ V_AC) <= 1`；
- **HV**: cubic `t=16` 中 common 32-block 的 h-vector 中项 `11` 与 `CI(3,4,4)` 的 `10` 冲突；
- **CD**: cubic `t=0` 中三个 contact cubics 的公共正维 locus 如何严格返回低次数；
- **PH**: primitive case 中 `I_A(4)=W`, `dim W=5`。

本轮结果：

1. **CP 可以从头严格证明，不需要旧 common-pencil 文档。**
2. **HV 与 PH 的旧来源已恢复：它们是 quartic defect `d=2`、`k=1` 的两个有限 Hilbert/liaison 候选 A/B。** 这两个数值结论可直接重证。
3. **CD 可以得到一个比旧稿更干净的证明**：对 `t=0` 的公共 28 点块做 `CI(3,4,5)` liaison，得到 `dim I_D(3)=2`, `dim I_D(4)=7`；两个独立 cubic 若互素，其线性倍数在 degree 4 已给 8 维，矛盾，因此必有一次或二次公因子。
4. 真正剩余的问题不应再表述为 “HV/PH 本身缺证明”，而是：**为什么相关几何分支最终只需处理 quartic defect `d=2`；或者如何直接排除 `d>=3` 的剩余候选。**

---

# 1. Triangle liaison 的统一 h-vector 对称

设

```text
Z_AB=A∪B,   Z_AC=A∪C,   Z_BC=B∪C,
|A|=|B|=|C|=32,
```

且三个 pair 都是 transverse `CI(4,4,4)`。

`CI(4,4,4)` 的 Artinian h-vector 为

\[
c=(1,3,6,10,12,12,10,6,3,1),
\]

socle degree 为 9。

对 `A` 与 `B` 的直接 liaison，标准 h-vector 公式为

\[
h_B(i)=c_i-h_A(9-i).
\]

同理

\[
h_C(i)=c_i-h_A(9-i),
\]

故 `h_B=h_C`。再对 `B,C` 的 link 使用同一公式：

\[
h_C(i)=c_i-h_B(9-i).
\]

于是

\[
h_B(i)+h_B(9-i)=c_i.
\]

再代回 `A-B` link 得

\[
\boxed{h_A=h_B=h_C=:h},
\]

且

\[
\boxed{h_i+h_{9-i}=c_i.}\tag{H}
\]

这是 residual triangle 的基本数值对称，不需要任何 common-pencil 输入。

---

# 2. Quartic defect 与 `(k,d)` 关系

定义

\[
d:=h^1(\mathcal I_A(4))=32-H_A(4).
\]

由

\[
0\to I_A(4)\to S_4\to H^0(O_A)\to H^1(I_A(4))\to0
\]

以及 `dim S_4=35`, `|A|=32`，得到

\[
\boxed{\dim I_A(4)=3+d.}\tag{D1}
\]

令

\[
U=V_{AB},\qquad V=V_{AC},\qquad
k:=\dim(U\cap V),\qquad W=U+V.
\]

两 net 都是 3 维，因此

\[
\dim W=6-k.
\]

而 `W⊂I_A(4)`，故

\[
6-k\le3+d,
\]

即

\[
\boxed{k+d\ge3.}\tag{D2}
\]

旧 `RESULTS.md` 中所谓的有限 `(d,k)` 枚举正是以 (H)、Macaulay O-sequence 条件和 (D2) 为核心数值约束。

---

# 3. CP：common-pencil lemma 的新完整证明

## 定理 CP

在 residual triangle setup 中，若 `U=V_AB`, `V=V_AC` 是两套不同的 transverse determinant nets，则

\[
\boxed{\dim(U\cap V)\le1.}
\]

## 证明

若 `dim(U∩V)=3`，则 `U=V`，两者 base locus 相同，迫使

\[
A\cup B=A\cup C,
\]

从而 `B=C`，矛盾。因此只需排除

\[
k=2.
\]

此时

\[
\dim W=\dim(U+V)=4.
\]

吹起公共 32 点：

\[
Y=Bl_A\mathbf P^3,
\qquad
D=4H-\sum_{a\in A}E_a.
\]

### (a) `W` 在 `Y` 上无基点

- 在 `B` 上，`U` 全消失，但 `V` 的 base locus 是 `A∪C`，故 `V` 不会全消失；
- 在 `C` 上同理；
- 在其它点，两 net 各自的 base locus 已知；
- 在每个 `E_a≅P^2` 上，任一 transverse `CI(4,4,4)` net 的三个一阶 jet 是三个独立线性式，因此没有共同 projective zero。

故 `W` 给出 morphism

\[
\phi_W:Y\to\mathbf P(W^*)\simeq\mathbf P^3,
\qquad
D=\phi_W^*O(1).
\]

并且

\[
D^3=4^3-32=32>0.
\]

因此 `phi_W(Y)` 必为三维。

### (b) 两个 determinant expressions 给出非零 quadratic relation

每套 determinant net 在自身 3 维空间上给出 rank-3 ternary quadratic form：

\[
F=Q_U(U)=Q_V(V),
\]

其中标准形为 `q0 q2-q1^2`。

把 `Q_U,Q_V` 看成 `W` 上的 quadratic forms。若

\[
Q_U=Q_V
\]

作为 `Sym^2 W` 中的形式，则这个 rank-3 quadratic form 的唯一 1 维 radical 同时等于 `U^⊥` 与 `V^⊥`，故 `U=V`，矛盾。

所以

\[
R:=Q_U-Q_V\ne0.
\]

但 substitution 后

\[
R(W)=F-F=0.
\]

故 `phi_W(Y)` 落在 `P^3` 中一个非零 quadric surface 上，因此

\[
\dim\phi_W(Y)\le2,
\]

与 `D^3=32>0` 矛盾。

因此 `k=2` 不可能，CP 得证。

---

# 4. 恢复旧有限枚举：`d=2` 恰有两个 h-vector

由 CP 与 (D2)：

\[
k\le1,
\qquad
k+d\ge3,
\]

所以

\[
d\ge2.
\]

当 `d=2` 时，必有

\[
k=1,
\qquad
\dim W=5,
\qquad
\dim I_A(4)=3+d=5,
\]

因此

\[
\boxed{W=I_A(4).}\tag{D3}
\]

结合半-CI 对称 (H)，`d=2` 只有两个与 “无 quadric” 相容的类型。

## Candidate A：唯一 cubic

若 `dim I_A(3)=1`，则

\[
H_A(3)=20-1=19,
\]

故

\[
h_3=19-(1+3+6)=9.
\]

由 (H)，`h_6=1`, `h_7=h_8=h_9=0`。

又

\[
d=32-H_A(4)=h_5+h_6=2,
\]

故 `h_5=1`；再由 `h_4+h_5=12`，得到

\[
\boxed{h_A=(1,3,6,9,11,1,1,0,0,0).}\tag{A}
\]

同时

\[
\dim I_A(4)=5.
\]

设唯一 cubic 为 `p`，则 `pS_1` 是 4 维，因此

\[
I_A(4)=pS_1+\langle q\rangle.
\]

这正是旧 `T16_RESULT.md` 中 `11` 的来源。

## Candidate B：无 cubic

若 `I_A(3)=0`，则

\[
h_0,h_1,h_2,h_3=(1,3,6,10).
\]

由 (H) 得 `h_6=h_7=h_8=h_9=0`。

又 `d=2`，所以 `h_5=2`，继而 `h_4=10`：

\[
\boxed{h_A=(1,3,6,10,10,2,0,0,0,0).}\tag{B}
\]

并且由 (D3)

\[
\boxed{I_A(4)=W,\qquad \dim W=5.}
\]

这就是旧文档所谓 “five primitive quartics”。

因此：**HV 与 PH 在 `d=2` 层面已经完全恢复，不再是无来源断言。**

---

# 5. HV：`t=16` 的 `11>10` liaison contradiction

Candidate A 中

\[
h_A=(1,3,6,9,11,1,1).
\]

`t=16` 的 cubic/plane contact comparison 给出

\[
F=Q^2+(p\ell)B_4,
\]

并得到包含 `A` 的

\[
Z_p=V(p,Q,B_4)=CI(3,4,4),
\qquad |Z_p|=48.
\]

`CI(3,4,4)` 的 h-vector 是

\[
h_{344}=(1,3,6,9,10,9,6,3,1),
\]

socle degree 为 8。

若 `T` 是 `A` 在 `Z_p` 中的 residual 16 点 scheme，则 liaison 公式给出

\[
h_T(i)=h_{344}(i)-h_A(8-i).
\]

取中间次数 `i=4`：

\[
h_T(4)=10-11=-1,
\]

不可能。

故 transverse `t=16` 分支不存在；退化/符号不一致情形仍按旧证明产生一次或二次因子。

---

# 6. CD：`t=0` 的新 Hilbert-factor 证明

这一步可以比旧稿 “三个 cubics 有公共曲线，所以返回 LD” 更严格。

Candidate A 中仍取

\[
h_A=(1,3,6,9,11,1,1).
\]

`t=0` 给出三个 weak-60 contact sets

\[
\Omega_A=A\sqcup D,
\quad
\Omega_B=B\sqcup D,
\quad
\Omega_C=C\sqcup D,
\qquad |D|=28,
\]

且每个 transverse contact cubic scheme 是

\[
CI(3,4,5).
\]

`CI(3,4,5)` 的 h-vector 为

\[
h_{345}=(1,3,6,9,11,11,9,6,3,1).
\]

由 `A` 与 `D` 在 `Omega_A` 中 liaison，socle degree 9，

\[
h_D(i)=h_{345}(i)-h_A(9-i).
\]

直接得到

\[
\boxed{h_D=(1,3,6,8,10,0,0,0,0,0).}
\]

于是

\[
H_D(3)=18,
\qquad
H_D(4)=28,
\]

所以

\[
\boxed{\dim I_D(3)=20-18=2,}
\]

\[
\boxed{\dim I_D(4)=35-28=7.}\tag{CD1}
\]

三个 contact cubic equations 都属于 `I_D(3)`。

- 若它们只张成 1 维，则三者共享同一个 cubic divisor，正是 nonprimitive cubic reduction；
- 否则取两个独立 cubic `p_1,p_2`。由 `dim I_D(3)=2`，它们生成整个 `I_D(3)`。

若 `gcd(p_1,p_2)=1`，则 degree-4 中

\[
p_1S_1+p_2S_1
\]

维数为 8：任何线性 syzygy

\[
\ell_1p_1+\ell_2p_2=0
\]

在互素条件下迫使 `p_1|ell_2`，次数不可能，故 `ell_1=ell_2=0`。

于是

\[
8=\dim(p_1S_1+p_2S_1)
\le\dim I_D(4)=7,
\]

矛盾。

故

\[
\gcd(p_1,p_2)\ne1.
\]

两个独立 cubic 的公因子次数不可能为 3，因此只能是 1 或 2：

\[
\boxed{\deg\gcd(p_1,p_2)\in\{1,2\}.}
\]

即严格得到公共 plane 或 quadric factor，返回已闭合的低次数分支。

所以 **CD 在 Candidate A / `d=2` 情形已经完整闭合**，而且无需模糊的 “positive-dimensional common locus ⇒ LD” 句子。

---

# 7. PH 后面的 primitive factorization

Candidate B 给出

\[
W=I_A(4),\qquad\dim W=5.
\]

`W` 在 `Y=Bl_A P^3` 上无基点，并定义

\[
\phi:Y\to P^4.
\]

两套 determinant expressions 的差给出一个非零 quadratic relation，因此像包含于 quadric threefold `Q^3`。

每个 exceptional plane `E_a≅P^2` 由 quartic 一阶 jets 线性映成一张 plane。光滑 `Q^3⊂P^4` 不含 plane，因此 quadratic relation 必奇异，rank 至多 4。

- rank 4：正规形
  \[
  f_1f_2=f_3f_4.
  \]
  UFD 分解为
  \[
  f_1=ab,\quad f_3=ac,\quad f_2=cd,\quad f_4=bd,
  \]
  且
  \[
  \deg a=\deg d=\alpha,
  \quad
  \deg b=\deg c=\beta,
  \quad
  \alpha+\beta=4.
  \]
  base locus 的 vertex 部分由 `V(a,d)` 与 `V(b,c)` 控制；clean transverse length 给
  \[
  32=4(\alpha^2+\beta^2),
  \]
  故 `alpha=beta=2`，返回 `16+16` quadratic splitting。

- rank 3：
  \[
  f_1f_2=f_3^2,
  \]
  UFD 给
  \[
  f_1=ha^2,\quad f_3=hab,\quad f_2=hb^2.
  \]
  若 `deg h=2`，显式出现 quadratic factor；若 `h` 为单位，则 `a,b` 为 quadrics，也回到 quadratic branch。

故 Candidate B 闭合。

---

# 8. 真正剩余的审计问题：不是四个 lemma，而是 `d>=3`

本轮恢复说明旧稿的问题比 “CP/HV/CD/PH 四个断言无证明” 更精确：

- CP 已重新证明；
- HV/PH 是旧有限 `d=2,k=1` 枚举的两个候选，可以重证；
- CD 在 Candidate A 下可新证。

但 triangle liaison + Macaulay 的基础枚举在 CP 后仍有 **31 个数值 h-vector**：

- 8 个 quadratic 类型；
- 18 个 cubic 类型；
- 5 个 primitive quartic 类型。

`d=2` 只对应其中两个：Candidate A 与 B。

因此正式投稿若想无条件写 “residual triangle fully excluded”，还必须说明：

\[
\boxed{\text{所有 }d\ge3\text{ 候选为何被低次数几何/primitive factorization 覆盖。}}
\]

已有 quadratic LD 确实统一处理所有 minimum-degree-2 候选；但 cubic `d>=3` 与 primitive `k=0` 六四次式情形需要逐项重新审计，不能仅用旧稿一句 “四分法闭合” 代替。

特别地：

- primitive 且 `k=1` 时，`W` 已是 5 维，rank-3/4 quadric factorization 不需要 `W=I_A(4)`，所以可直接沿上述路线处理；
- primitive 且 `k=0` 时，`W` 是 6 维，进入 `P^5` 中 quadric-fourfold / six-quartic comparison，这才是一个真实需要单独处理的 outlet；
- cubic `d>=3` 也应利用 `CI(3,4,4)` / `CI(3,4,5)` liaison 继续逐候选压缩。

这应当作为下一轮 residual-triangle 审计的真正目标。
