# Weight 48：纯码论 recursive residual cascade（2026-08-08）

## 1. 第一 residual 的统一低重量 trade-off

固定一个 strict weight-48 word 后得到
\[
R=[121,18],\qquad R\text{ 4-divisible},\qquad d(R)\ge24.
\]
在正确 octic strict weight spectrum 下，first residual 的低重量只可能是
\[
24,32,36,40,44,48.
\]

沿用此前处理 `d(R)=48` 的五次多项式
\[
P(w)=-\frac{(w-52)(w-60)(w-64)(w-68)(w-72)}{368640}.
\]
其 length-121 Krawtchouk 展开系数全部严格正，并且
\[
P(24)=231,\quad P(32)=70,\quad P(36)=\frac{168}{5},\quad
P(40)=14,\quad P(44)=\frac{14}{3},\quad P(48)=1,
\]
而所有允许的 4-divisible weight `w>=52` 上 `P(w)<=0`。因此 MacWilliams 给统一 exact inequality
\[
\boxed{
3465A_{24}+1050A_{32}+504A_{36}+210A_{40}+70A_{44}+15A_{48}\ge51708.
}
\]

这比逐个处理 `d(R)=40,44,48` 更自然：它实际上把所有 first-residual outlets 放进同一个低重量 budget。

## 2. 统一二维低重量子码

对 length 121 上同重 supports 做凸性 incidence。由于 `R` 4-divisible，任意两个 codewords 的交数为偶数。下面这些阈值足以强迫一对同重 words 的和重不超过 56：

\[
\begin{array}{c|cccccc}
w&24&32&36&40&44&48\\\hline
\text{threshold }A_w&2&5&6&10&15&29\\
\text{forced }|X\cap Y|\ge&0&4&8&12&16&20.
\end{array}
\]

若所有阈值都未达到，则统一 inequality 左端最多为
\[
3465\cdot1+1050\cdot4+504\cdot5+210\cdot9+70\cdot14+15\cdot28
=13475<51708,
\]
矛盾。

故得到纯码论结论：

> **Master 2D compression.** 任意当前 first residual `R` 中都存在两个 distinct equal-weight words `x,y`，其重量属于 `24,32,36,40,44,48`，并满足
> \[
> \operatorname{wt}(x+y)\le56.
> \]
> 因而 `R` 含有一个二维子码，其三个非零重量都落在很低的 residual spectrum 中。

这一步完全不使用 contact quadric 或 determinant geometry。

## 3. 最坏递归支 `48 -> 28 -> 16 -> 8 -> 4`

此前已经 exact 验证：若
\[
R=[121,18,48],
\]
则
\[
A_{48}(R)\ge3448,
\]
incidence 强迫第二 residual
\[
S=[73,17],\qquad d(S)\in\{24,26,28\}.
\]

若取最难的 `d(S)=28`，则已有
\[
A_{28}(S)\ge5941.
\]
这些 weight-28 supports 在 length 73 上强迫一对交至少 11。固定其中一个 28-word residualize，得到
\[
T=[45,16],\qquad 14\le d(T)\le17.
\]
Griesmer 已排除 `d(T)>=17`，故
\[
\boxed{d(T)\in\{14,15,16\}}.
\]

### 3.1 若 `d(T)=16`

新找到一个 exact degree-7 Krawtchouk certificate。其归一化多项式满足
\[
P_{45}(16)=1,\qquad P_{45}(w)\le0\quad(17\le w\le45),
\]
且全部 Krawtchouk coefficients 严格正。MacWilliams 给
\[
A_{16}(T)\ge \frac{6144498}{935}>6571,
\]
因此
\[
\boxed{A_{16}(T)\ge6572}.
\]

6572 个 weight-16 supports 在 length 45 上的平均 pair intersection 大于 5，因此存在一对交至少 6。再 residualize 一个 weight-16 word：
\[
U=[29,15],\qquad d(U)\ge8,
\]
并由该邻居得到一个 weight `<=10` word。Griesmer 对 `[29,15,9]` 给所需长度 30，因此 `d(U)>=9` 不可能，故
\[
\boxed{U=[29,15,8]}.
\]

### 3.2 `d(T)=16` 实际已经矛盾

上一步纯码论推出：若 `T=[45,16,16]`，则必产生一个 binary
\[
U=[29,15,8].
\]
David Jaffe 对长度不超过 30 的最优 binary linear codes 的分类证明了 `[29,15,8]` 不存在。因此
\[
\boxed{[45,16,16]\text{ 不存在于该递归分支}.}
\]

此前进一步对假想 `[29,15,8]` 构造的 degree-8 abundance certificate 与 `[21,14,4]` descent 仍可保留为独立的 conditional arithmetic check，但不再作为实际主线；主线在 `[29,15,8]` 处已经闭合。

所以最坏 high-distance cascade 应准确写成
\[
\boxed{
[121,18,48]
\to[73,17,28]
\to[45,16,d],\qquad d\le15.
}
\]

这说明每当 residual minimum 取到当前参数允许的高端值时，massive minimum-word abundance 会把它推入更短码，随后可由已知小参数码的非存在性直接截断。

## 4. 当前意义

这说明 weight-48 分支不应直接进入几何分类。更自然的策略是：

1. 用 master trade-off 把 first residual 全部压进低重量二维子码；
2. 对高 minimum outlet 递归 residual；
3. 每次若 residual minimum 仍接近最大值，就用 exact Krawtchouk certificate 制造大量 minimum words；
4. incidence 再次 residual；
5. 最后把得到的 residual flag 重新解释成原 code 中一个低维（约 4--6 维）刚性 subcode signature，再做 multi-split MacWilliams / Terwilliger，而不是几何枚举。

下一步最值得做的是把 `d(S)=24,26` 和 `d(T)=14,15` 也做成类似的 trade-off/flag compression；若能统一，则 48 分支有希望先被纯码论压成极少数 4D/5D signatures。

Exact verifier：

`scripts/verify_weight48_recursive_cascade.py`
