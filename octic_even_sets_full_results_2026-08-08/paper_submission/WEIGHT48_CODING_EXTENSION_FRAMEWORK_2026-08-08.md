# Weight 48：从 residual cascade 到 restricted-weight extension

日期：2026-08-08

## 1. 为什么不应直接进入几何分类

当前 minimum-48 分支已经有纯码论的第一层统一压缩：固定 weight-48 word `c` 后，
\[
R=\operatorname{Res}(C;c)=[121,18]
\]
是 4-divisible，并满足
\[
3465A_{24}+1050A_{32}+504A_{36}+210A_{40}+70A_{44}+15A_{48}\ge51708.
\]
因此 `R` 总能找到两个同重 words `y,z`，其 residual weight 属于
\[
24,32,36,40,44,48
\]
且
\[
\operatorname{wt}(y+z)\le56.
\]

这说明正确的第一对象不是 contact-quadric 的几何 pair type，而是由 `c,y,z` lift 回原码产生的低维 subcode。

## 2. 3D signature 是有限的

令
\[
H=\langle c,x_1,x_2\rangle\subset C,
\]
其中 `x_1,x_2` lift 上述两个 residual words。对 `H\cong F_2^3` 的七个非零 words 记其重量为 `w(v)`。每个坐标对应一个 column type
\[
\alpha\in F_2^3,
\]
其 multiplicity `m_alpha` 由 Walsh inversion 唯一恢复：
\[
\boxed{
 m_\alpha=\frac18\sum_{v\in F_2^3}(169-2w(v))(-1)^{\alpha\cdot v}.
}
\]

把所有 canonical first-residual lift profiles、所有允许的 `y+z` residual weights `<=56`、以及所有 lift orientations 代入后，非负整数 multiplicity 条件只留下：

- 697 个 labeled realizations；
- 对固定 `c` 的基变换稳定子取轨道后，仅 165 个 3D signatures；
- 七个非零重量全部落在
  \[
  \boxed{48,64,72,80,88,96};
  \]
- `H` 的 support size 只在
  \[
  \boxed{84\le |\operatorname{supp}H|\le124}.
  \]

因此 48 分支已经可以从“连续几何分类”替换为一个 165-state 的纯整数 extension 问题。

Exact enumerator：

`scripts/enumerate_weight48_3d_signatures.py`.

## 3. 8-divisibility 给出的 quadratic-form compatibility

把坐标分为
\[
A=\operatorname{supp}(c),\quad |A|=48,
\qquad B=A^c,\quad |B|=121.
\]
对 `x in C` 写
\[
x=(d,y),\qquad d=x|_A,\quad y=x|_B\in R.
\]
因为 `C` 是 8-divisible，`R` 是 4-divisible，而且
\[
\operatorname{wt}(d)+\operatorname{wt}(y)\equiv0\pmod8.
\]
特别地 `D`, 即所有 restrictions `d` 的线性像，是一个 4-divisible binary code。

在任意 4-divisible binary code 上定义
\[
q(u)=\frac{\operatorname{wt}(u)}4\pmod2.
\]
则
\[
\boxed{q_D(d)=q_R(y).}
\]
由于两个 lifts 相差 `1_A`，而 `1_A` 是 isotropic radical vector，故上述关系在 quotient `D/<1_A>` 上良定义。

因此 reconstruction of `C` from `R` 不是任意 split extension，而是一个保持 quadratic form 的 linear extension problem。其 kernel 必须是 `R` 中的 totally singular subcode；特别地 kernel 中 words 自动具有 weight divisible by 8。

这提供了比普通 two-block split MacWilliams 更强、又比几何分类更代数化的约束层。

## 4. 与 Kurz 的 nodal-surface coding 路线的关系

Kurz 在 sextic nodal-surface code 的处理里使用了同型策略：

1. 先用 MacWilliams / Pless moments 强迫某个低重量 word；
2. residualize，把 divisibility 从 8 降到 4；
3. 对 residual 的 restricted weight set 做有限分类；
4. 再通过 code extension 枚举恢复原码。

其后续算法框架把 restricted-weight linear-code classification 写成 lattice-point enumeration / integer linear programming。这说明当前 octic weight-48 分支最自然的下一步不是逐几何类型，而是：

\[
\boxed{
165\text{ 个 3D signatures}
\longrightarrow
\text{restricted-weight extensions to dimension }4,5,\ldots
}
\]

并在每次 extension 时加入：

- 全局允许重量集；
- 8-divisibility / Ward intersection congruences；
- quadratic-form compatibility；
- MacWilliams positivity；
- 必要时才加入 8-block split moments。

## 5. 当前递归小码结果

另一条互补的纯码论 descent 已把最坏 residual outlet 压到
\[
[121,18,48]\to[73,17,\le28]\to[45/47/49,16,\le16]\to[n\le33,15,\le8].
\]
其中 `[45,16,16]` 会进一步产生 `[29,15,8]`；Jaffe 的分类结果表明 binary `[29,15,8]` 不存在，所以这一最坏子支实际上已经被排除。

因此下一阶段应优先研究 restricted-weight extension / 3D-to-4D augmentation，而不是再增加几何 case distinctions。
