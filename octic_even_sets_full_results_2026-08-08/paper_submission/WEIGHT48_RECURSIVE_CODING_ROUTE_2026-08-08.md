# Weight 48：递归 residual abundance 纯码论路线

日期：2026-08-08

状态：**[Exact certificates verified; research note, not yet promoted to main.tex]**

## 1. 两条低收益路线已经诊断到头

固定一个 weight-48 word `c`，使用正确 octic strict weight set

\[
\{0,48,64,72,80,88,96,104,112,120,128,136,144,152,160,168\}
\]

后：

1. two-block split-MacWilliams + `A64+21 A48>=533` 仍允许 `d(Res(C;c))=48`；
2. 即使加入较高 total-degree split moments，极端 relaxation 仍允许
   \[
   A_{48}=1,\qquad A_{64}=512;
   \]
3. 锚定一个 `(64,64,80)` / 40A 二维子码做四块 split LP，也仍允许 `A48=1` 且不强迫额外 64-triangle。

因此不宜继续在单 anchor / 单二维子码的局部 LP 上堆次数。

---

## 2. 新主线：若 first residual 的最坏值 `d(R)=48`，则 minimum words 爆炸

设

\[
R=\operatorname{Res}(C;c)=[121,18,48],
\]

则 `R` 是 4-divisible。

考虑

\[
P(w)= -\frac{(w-52)(w-60)(w-64)(w-68)(w-72)}{368640}.
\]

其 length-121 Krawtchouk 展开为

\[
P=\frac{953}{40960}K_0+\frac{407}{40960}K_1+
\frac{241}{122880}K_2+\frac{21}{40960}K_3+
\frac{9}{163840}K_4+\frac1{98304}K_5,
\]

所有系数严格正。

并且

\[
P(48)=1,
\]

而对所有其他非零 4-divisible weights `52,56,...,120`，

\[
P(w)\le0.
\]

又

\[
P(0)=2652.
\]

MacWilliams 给

\[
A_{48}(R)\ge 2^{18}\frac{953}{40960}-2652
=\frac{17236}{5}>3447.
\]

因此

\[
\boxed{A_{48}(R)\ge3448.}
\]

这是 exact theorem；验证脚本：

`scripts/verify_weight48_residual48_abundance.py`。

---

## 3. 3448 个 residual minimum words 自动制造第二 residual

取任意 3448 个 weight-48 supports in length 121。
总 incidence 为

\[
3448\cdot48=121\cdot1367+97.
\]

凸性给

\[
\sum_{Y<Z}|Y\cap Z|
\ge24\binom{1367}{2}+97\binom{1368}{2}
=113105580.
\]

而

\[
\frac{113105580}{\binom{3448}{2}}>19.
\]

在 4-divisible code 中两个 weight-48 words 的 intersection 为偶数；minimum 48 又给 intersection `<=24`。故存在 pair 满足

\[
\boxed{|Y\cap Z|\in\{20,22,24\}.}
\]

固定其中一个 minimum word `Y`，第二 residual

\[
S=\operatorname{Res}(R;Y)=[73,17]
\]

为 even code，且两 lift 均至少 48，所以

\[
d(S)\ge24.
\]

上述 pair 给 residual word weight

\[
48-|Y\cap Z|\in\{28,26,24\}.
\]

因此

\[
\boxed{d(S)\in\{24,26,28\}.}
\]

于是最坏 first residual `48` 已经完全由纯码论压成三种 second-residual minima。

---

## 4. 第二层也有 exact trade-off

对任意 even `[73,17]` code with `d>=24`，考虑

\[
Q(w)=\frac{(w-30)(w-36)(w-38)(w-44)(w-46)(w-72)}{2027520}.
\]

其 Krawtchouk 展开为

\[
\begin{aligned}
Q={}&\frac{191}{2816}K_0+\frac{179}{5632}K_1+
\frac{19}{2112}K_2+\frac{1357}{540672}K_3\\
&+\frac{257}{540672}K_4+\frac{47}{540672}K_5+
\frac1{180224}K_6,
\end{aligned}
\]

全部系数严格正。

并且

\[
Q(24)=\frac{21}{2},\qquad
Q(26)=\frac{345}{88},\qquad
Q(28)=1,
\]

而所有 even `w>=30` 上 `Q(w)<=0`。

MacWilliams 整理后得到

\[
\boxed{924A_{24}+345A_{26}+88A_{28}\ge522758.}
\]

因此

\[
\boxed{A_{24}+A_{26}+A_{28}\ge566.}
\]

特别地，若

\[
d(S)=28,
\]

则

\[
\boxed{A_{28}(S)\ge5941.}
\]

验证脚本：

`scripts/verify_weight48_second_residual_tradeoff.py`。

---

## 5. 递归树

当前 purely coding tree 可写为

\[
\boxed{
\begin{array}{c}
d(C)=48\\
\downarrow\\
R=[121,18],\quad24\le d(R)\le48.
\end{array}}
\]

其中最坏 outlet

\[
d(R)=48
\]

不再视为一个孤立 profile，而是

\[
\boxed{
 d(R)=48
 \Longrightarrow A_{48}(R)\ge3448
 \Longrightarrow S=[73,17],\ d(S)\in\{24,26,28\}.
}
\]

且无论 `d(S)` 是哪一个，低三层总量满足

\[
924A_{24}+345A_{26}+88A_{28}\ge522758.
\]

如果 `d(S)=28`，则出现第二次 massive minimum layer：`A28>=5941`。

---

## 6. `d(R)=44` 也有 exact low-weight compression

同一个 length-121 五次多项式满足

\[
P(44)=\frac{14}{3},\qquad P(48)=1,
\]

并在所有 4-divisible `w>=52` 上非正。因此对任意 4-divisible `[121,18,44]` code，

\[
\boxed{70A_{44}+15A_{48}\ge51708.}
\]

于是：

- 若 `A44>=15`，15 个 weight-44 supports 的 incidence 强迫一对交至少 16；其和重落在 `44,48,52,56`；
- 若 `A44<=14`，则
  \[
  \boxed{A_{48}\ge3382},
  \]
  3382 个 weight-48 supports 强迫一对交至少 20；其和重同样落在 `44,48,52,56`。

故

\[
\boxed{d(R)=44\Longrightarrow R\text{ contains a 2D subcode whose three nonzero weights lie in }\{44,48,52,56\}.}
\]

exact verifier：`scripts/verify_weight48_residual44_tradeoff.py`。

---

## 7. 下一步优先级

不进入几何。继续码论：

1. **处理 second residual `d(S)=24/26/28`**：针对三种 minimum 分别做 anchored split / pair-state compression，目标把三支再压到统一的 third-residual 小范围。
2. **特别优先 `d(S)=28`**：已有 `A28>=5941`，应直接做 incidence / 二维子码 split，预计最容易继续收缩。
3. **回头处理 `d(R)=40`**：寻找类似的 low-weight trade-off，把 40/44/48 三个高 residual outlets 统一成少量低维子码 signatures。
4. 最后把 `d(R)=40,44,48` 的纯码论 descendants 统一成少量 3D subcode signatures，再交给几何。

当前判断：48 分支确实适合继续走 coding-first；现在已经出现与原 `A64>=533` 同类型、甚至数值更强的 recursive abundance phenomenon。