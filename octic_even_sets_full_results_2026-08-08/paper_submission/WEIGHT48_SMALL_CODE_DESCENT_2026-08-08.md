# Weight 48：第三层小码继续下降的纯码论结果

日期：2026-08-08

## 1. 从第二 residual 统一进入长度 45/47/49

对此前的 even `[73,17]` second residual `S`，已有 exact trade-off

\[
924A_{24}+345A_{26}+88A_{28}\ge522758.
\]

所以
\[
A_{24}+A_{26}+A_{28}\ge566.
\]
至少有一种重量 `w in {24,26,28}` 出现至少 189 次。对 189 个同重 supports 做 incidence：

- `w=24`：强迫交至少 8；
- `w=26`：强迫交至少 10；
- `w=28`：强迫交至少 11。

因此 residualize 其中一个 word 后得到维数 16 的第三 residual `T`，其参数属于

\[
[49,16],\quad [47,16],\quad [45,16],
\]

并且统一有

\[
\boxed{10\le d(T)\le16.}
\]

更精确地：

- anchor 24：`[49,16]`, `12<=d<=16`；
- anchor 26：`[47,16]`, `11<=d<=16`；
- anchor 28：`[45,16]`, `10<=d<=16`，其中 `d>=17` 已由 Griesmer 排除。

## 2. length 45 的 `d=14/15/16` 可统一压缩

在 `d(S)=28` 分支中，第三 residual 为 `[45,16]` 且 `14<=d<=16`。无需分别处理三个 minimum。考虑
\[
P(w)=-\frac{(w-17)(w-21)(w-22)(w-27)(w-28)(w-33)(w-34)}{11618880}.
\]
其 length-45 Krawtchouk 展开系数为
\[
\frac{73161}{3872960},\frac{275}{29792},\frac{57089}{15491840},
\frac{4143}{3098368},\frac{409}{968240},\frac{89}{774592},
\frac3{126464},\frac3{885248},
\]
全部严格正。并且
\[
P(14)=1,\qquad P(15)=\frac{27}{70},\qquad
P(16)=\frac{5049}{48412},
\]
而 `P(w)<=0` 对所有 `17<=w<=45`。MacWilliams 给
\[
A_{14}+A_{15}+A_{16}\ge
\left\lceil\frac{32175099}{48412}\right\rceil=665.
\]
所以至少一种重量出现至少 222 次。incidence 在 length 45 上分别强迫：

- 222 个 weight-14 words 中有一对交至少 5；
- 222 个 weight-15 words 中有一对交至少 5；
- 222 个 weight-16 words 中有一对交至少 6。

residualize 相应的一个 word 后得到 dimension 15、length 31/30/29 的码，并由邻居得到 minimum upper bound 9/10/10。结合 `n_2(15,10)=35` 以及 odd-distance parity extension，可统一得到
\[
\boxed{[45,16,d],\ 14\le d\le16\Longrightarrow
[n,15,d'],\ 29\le n\le31,\ d'\le8.}
\]
若走 weight-16 子支，则 Jaffe 的 `[29,15,8]` 非存在性进一步给 `d'<=7`。而在原先的极端 `d=16` 情形，已有更强的 `A16>=6572` 证书直接强迫 `[29,15,8]`，从而整个 `d=16` outlet 被排除。

## 3. 第三层 `d=16` 的 abundance（旧的更强极端证书）

### length 45

已有 exact certificate：
\[
A_{16}\ge6572.
\]
从而 residual 到 `[29,15,8]`，再由 `A_8>=188` residual 到 `[21,14,4]`。

### length 47

存在 exact degree-7 Krawtchouk polynomial，全部系数非负，满足

\[
P(16)=1,\qquad P(17)=\frac5{13},\qquad P(18)=\frac{2375}{22932},
\]
且 `P(w)<=0` 对所有 `w>=19`。MacWilliams 给

\[
\boxed{A_{16}+A_{17}+A_{18}\ge2736.}
\]

因此至少一种重量出现 912 次。incidence 给：

- 16-word pair 交至少 6；
- 17-word pair 交至少 7；
- 18-word pair 交至少 7。

再 residual 后得到 `[31,15]`, `[30,15]`, 或 `[29,15]`。
结合 Griesmer 以及下面的两个小码非存在性，最终这些分支都满足

\[
\boxed{d\le8.}
\]

### length 49

另有 exact degree-7 certificate：
\[
P(16)=1,\qquad P(17)=\frac{11}{27},\qquad P(18)=\frac{847}{7176},
\]
且 `P(w)<=0` 对所有 `w>=19`。得到

\[
\boxed{A_{16}+A_{17}+A_{18}\ge881.}
\]

故至少一种重量出现 294 次。incidence 后：

- 若主导重量 16，得到 `[33,15]` 且 `8<=d<=10`；
- 若主导重量 17，得到 `[32,15]` 且 `d<=9`；
- 若主导重量 18，得到 `[31,15]` 且 `d<=8`。

原本唯一仍相对高的 outlet 是 `[33,15,10]`。但 Bouyukliev--Jakobsson 对 binary distance-10 codes 的精确结果给出 `n_2(15,10)=35`。因此 `[33,15,10]` 不存在。进一步，若 `[n,15,9]` 存在，则加 overall parity coordinate 得到 `[n+1,15,10]`；故对 `n<=33`，distance 9 也不可能。于是本递归中所有 length `<=33`, dimension `15` 的出口统一满足
\[
\boxed{d\le8.}
\]

## 3. 两个非常短的小码非存在性

### 3.1 不存在 binary `[31,15,10]`

Griesmer bound 对 `[31,15,10]` 取等号。取 minimum weight-10 word residualize，得到

\[
[21,14,d']\qquad d'\ge5.
\]

但 radius-2 Hamming ball 的体积
\[
1+21+\binom{21}{2}=232
\]
大于 syndrome space 大小
\[
2^{21-14}=128.
\]
因此 `[21,14,5]` 不存在，故 `[31,15,10]` 不存在。

同理 `[30,15,9]` 也不存在，因为 residual 一个 weight-9 word 同样给 `[21,14,>=5]`。

### 3.2 不存在 binary `[22,14,5]`

若存在 `[22,14,5]`，取一个 rank-8 parity-check matrix，令其 22 个非零、互异列构成
\[
A\subset \mathbf F_2^8,\qquad |A|=22.
\]

距离至少 5 表示任意四列线性无关，故所有 unordered pair sums
\[
a_i+a_j\quad(i<j)
\]
彼此不同，且都不属于 `A`。于是 231 个 pair sums 占据
\[
\mathbf F_2^8\setminus(\{0\}\cup A)
\]
的 233 个元素中的 231 个，只剩两个不同元素 `b,c`。

令
\[
S=\bigoplus_{a\in A}a.
\]
因为每个 `a in A` 在全部 pair sums 中出现 `21` 次，
\[
\bigoplus_{i<j}(a_i+a_j)=S.
\]
另一方面，`F_2^8` 全体元素 xor 为 0，所以 complement 的 xor 也是 `S`。但 complement 等于 pair sums 加上 `{b,c}`，故
\[
S=S+b+c,
\]
从而 `b=c`，矛盾。

因此
\[
\boxed{[22,14,5]\text{ 不存在}.}
\]

于是：

- `[32,15,10]` 不存在（residual weight 10 -> `[22,14,>=5]`）；
- `[31,15,9]` 不存在（residual weight 9 -> `[22,14,>=5]`）。

## 4. 当前 coding-first 图景

最坏的 high-distance outlets 现在形成明显的自动下降：

\[
[121,18,48]
\to [73,17,\le28]
\to [45/47/49,16,\le16]
\to [29\text{--}33,15,\le10],
\]

而长度 29--32 的若干最高距离 outlet 已被 Griesmer/Hamming/Sidon 直接排除。

这条路线的目标不应是立即得到最终 contradiction，而是把原始 octic code 先压成一个非常短的 residual flag / 低维 subcode signature，再对该 signature 使用 multi-split MacWilliams 或 Terwilliger positivity。这样几何最多只需要处理最终极少数 surviving signatures。
