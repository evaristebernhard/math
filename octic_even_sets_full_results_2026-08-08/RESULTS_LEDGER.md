# 八次节点曲面低重量偶集项目：完整成果账本

日期：2026-08-09（投稿状态同步）

本文件的目的不是筛选“最适合单篇投稿的少数结论”，而是**完整保存目前已经得到、并经过历次审计确认的数学成果**。任何结论即使暂时不能闭合最终的 \(u(8)\le168\) / 最大节点数问题，只要本身已经证明、有限枚举闭合、或在明确上游输入下成为完整条件定理，都保留在这里。投稿状态以 `paper_submission/PROOF_AUDIT_2026-08-09.md` 为准。

状态标签：

- **[T]**：在列明设定下无条件闭合的数学定理。
- **[L]**：经典文献输入；项目不从第一性原理重证。
- **[C]**：由精确有限枚举/计算证书闭合。
- **[CT]**：上游输入明确后，下游蕴含完全闭合。
- **[OPEN]**：真正仍未闭合的接口；不是“失败定理”。

---

## A. 统一编码入口

1. **[L→T] Beauville–Endraß 维数入口**  
   对假想高节点八次曲面，严格偶节点码满足
   \[
   \dim K\ge \nu-150.
   \]
   因而在 \(169\le \nu\le174\) 时，可以在保留指定低重配置的前提下 shortening 到长度 169，并取得包含该配置的 19 维子码。

2. **[T] 保留指定低重配置的 shortening lemma**  
   当指定配置的支撑并集大小不超过 104 时，有足够多的外部坐标完成最多 5 次 shortening；最终得到
   \[
   C\subseteq \mathbf F_2^{169},\qquad \dim C=19.
   \]

3. **[T/Audit correction] 完整允许重量谱复核 + Endraß 表格纠错**  
   对一般以及 strict-octic 的 minimum-64 shortened code，必须允许
   \[
   \{0,64,72,80,88,96,104,112,120,128,136,144,152,160,168\}.
   \]
   Endraß《Minimal even sets of nodes》Cor. 1.11 的表格曾因文本抽取错列被误读：degree \(8\) 的 strictly-even gap 只有 weight \(56\)；\(88,96,104,112\) 属于 degree \(10\)。因此删除这四个重量的旧证书只能作为额外假设下的 conditional certificate，不能用于八次曲面的无条件主线。

---

## B. Weight 72：完整闭合

4. **[T+C] Weight-72 residual reduction**  
   固定 72-word 后得到
   \[
   R=\operatorname{Res}(C;c)=[97,18].
   \]

5. **[C] 修正后的五阶 Krawtchouk 证书**  
   lift-pair 必须使用 Krawtchouk 值的“和”而不是“差”。60 个非零允许状态全部满足证书多项式非正，而零状态给出精确正值。

6. **[T+C] Weight 72 排除定理**  
   MacWilliams 平均下界为 7280，而有限状态证书给出上界 5148，矛盾。因此不存在含 72-word 的 8-divisible \([169,19,72]\) 码；在假想高节点范围内
   \[
   d(K)\ne72.
   \]

**投稿价值：很高。** 这是完全独立、可复核的 coding obstruction，不依赖后面的复杂几何比较。

---

## C. Weight 64：determinant、residual 分类、40B、全局多表示结构

7. **[L→T] Weight-64 symmetric determinant theorem**  
   任一 strict weight-64 严格偶集 \(W\)（不要求 global minimum 为 64，也允许同一 code 中存在 48-word）自动给出
   \[
   F_8=q_0q_2-q_1^2,
   \qquad
   W=V(q_0,q_1,q_2)=CI(4,4,4),
   \]
   且该完全交 reduced、transverse。  
   这不是额外“标准假设”，而是从 Endraß 的 degree-four stability alternative 推出的结构定理。

8. **[T] 第一 residual 参数**  
   固定 weight-64 word 后
   \[
   R=[105,18],\qquad R\text{ 为 4-divisible},\qquad d(R)\ge32.
   \]

9. **[C→T] 五阶 residual 证书**  
   精确 MacWilliams/Krawtchouk 证书给出
   \[
   d(R)\le40.
   \]
   因而
   \[
   d(R)\in\{32,36,40\}.
   \]

10. **[T] lift-profile 四分支**  
    最小 residual 的 lift pair 唯一导致：
    - \(d(R)=32\): \((64,64,64)\) triangle；公共块 32，四块大小 \((73,32,32,32)\)。
    - \(d(R)=36\): lift weights \(64,72\)；公共块 28，四块大小 \((69,36,36,28)\)。
    - \(40A\): lift weights \(64,80\)；公共块 24，四块大小 \((65,40,40,24)\)。
    - \(40B\): lift weights \(72,72\)。

11. **[Geometric input retained] Pairwise residual-intersection strengthening**  
    在每个 64-word 都来自 reduced transverse determinant presentation 的几何情形，若有第二个 64-word，可选择一对公共块至少 24；因此 two-presentation 分支落入 32/36/40A，40B 可视为“唯一 weight-64 word”的出口。

12. **[CT+C] 旧 40B/unique-minimum-word 证书**  
    若额外输入把 40B 识别为“所选 code 中恰有一个 weight-64 word”的出口，则完整允许重量谱的 lift-pair 证书给出 MacWilliams 平均下界 7280、有限状态上界 5152，因而该 unique-word outlet 不存在。**注意：纯码论的 40B 只表示某个最小 residual word 的两 lifts 为 \((72,72)\)，不能在没有 residual-intersection strengthening 的情况下自动解释成全局 unique weight-64 word。** 当前投稿主线已用 \(A_{64}\ge533\)+incidence 直接压到 residual 32/36，不再依赖此输入。

13. **[T] 全局最小字下界**  
    对 \([169,19,64]\) 分支，精确 LP 身份给出
    \[
    A_{64}\ge533.
    \]
    若 \(\dim C\ge20\)，同一证书给出
    \[
    A_{64}\ge2353.
    \]

14. **[T] 粗 incidence 定理**  
    在 533 个 weight-64 words 中：
    - 必有一对交集至少 28；
    - 若不存在交集 32 的 pair，则交集恰为 28 的无序 pair 至少
      \[
      e_{28}\ge5743;
      \]
    - 因而至少一个 64-word 有至少 22 个交集 28 的邻居。

14a. **[T] 新的全局 residual 32/36 归约（2026-08-08 审计提炼）**  
    由上条可选两个 weight-64 words 满足交集 \(28\) 或 \(32\)。固定其中一个 \(c\)，另一个在 \(\operatorname{supp}(c)^c\) 上给出 residual word，重量为
    \[
    64-28=36\quad\text{或}\quad64-32=32.
    \]
    又任意 weight-64 residual code 都有 \(d(R)\ge32\)，故可以选择一个 minimum word 使
    \[
    \boxed{d(\operatorname{Res}(C;c))\in\{32,36\}}.
    \]
    这是纯 coding + incidence 的无条件归约，**不需要**旧的 pairwise residual-intersection strengthening。

14b. **[Audit correction] 不能把 32/36 再纯码论压成 36**  
    旧尝试用 Cor. 1.11 删除 \(88,96,104,112\) 并调用 split-MacWilliams 排除 residual 32；这是对 Endraß 表格的错列误读。正确状态仍是
    \[
    \boxed{d(\operatorname{Res}(C;c))\in\{32,36\}}.
    \]
    40A/40B 已由 14a 绕开；32 是真实 residual-triangle 几何分支，36 暂缓完整闭合。

**重要解释：** 假想反例不是只有一两个 determinant presentation，而是携带数百套；“many-presentations”本身就是一个强全局结构结论。

---

## D. Residual triangle（\(d(R)=32\)）

15. **[C | conditional] residual triangle 的 legacy split-MacWilliams certificate**  
    若额外假设
    \[
    A_{88}=A_{96}=A_{104}=A_{112}=0,
    \]
    则四块 \((73,32,32,32)\) 的 122 个非零 coset states 上存在 27 项非负 split-Krawtchouk contradiction。该整数 certificate 本身正确，但额外禁重**不是**八次曲面的 Endraß 输入，因此不能排除实际 octic residual triangle。脚本保留作 conditional audit，不进入无条件测试链。

15a. **[C→T] 完整重量谱上的 high-weight compensation theorem（2026-08-08）**  
    保留完整允许重量
    \[
    \{0,64,72,80,88,96,104,112,120,128,136,144,152,160,168\}
    \]
    后共有 1594 个非零 \(H\)-coset split states。total split degree \(\le8\) 的 exact rational dual certificates 给出
    \[
    \boxed{A_{88}+A_{96}\ge65},
    \qquad
    \boxed{A_{88}+3A_{96}\ge185}.
    \]
    因而
    \[
    \max\{A_{88},A_{96}\}\ge47,
    \qquad
    A_{96}\ge41\ \text{or}\ A_{88}\ge65.
    \]
    进一步，若不存在一个非零 \(H\)-coset 同时含 weight 64 与 weight 88/96，则删去 199 个 mixed states 后的 1395-state exact certificate 给出
    \[
    \boxed{A_{88}+A_{96}\ge471}.
    \]
    三张证书已加入投稿目录 `npm test`，均只使用 Python integer arithmetic。它们不排除 triangle，但把其 coding obstruction 变成“mixed 3D 小配置 / 极大量高重量字”的无条件二分。

16. **[T within stated setup] Blow-up nef 四分法**  
    对公共 32 点 blow-up 后，低次数 carrier 被分为：plane / quadratic / cubic / primitive quartic。

17. **[T] Plane carrier 排除**。

18. **[T] Quadratic LD 的 restriction-image 直线定理**  
    若 reduced quadric 包含公共 32 点，限制线性系统的像只能是一条直线。

19. **[T] 每个 determinant net 与 quadratic kernel 恰交一维**；若交维过大会产生 contact quadric，从而产生 weight 48，与 \(d(K)=64\) 冲突。

20. **[T] Quadratic normal form 与 \(16+16\) splitting**。

21. **[T] Quadratic compatibility 最终闭合**  
    所有非零 reduced pencil member 均被迫成为 contact quadric；再由 minimal weak set/对称差排除退化可能。

22. **[T] Cubic-contact defect-two 分支完整闭合**：\(t=16\) 支由 contact plane + liaison / Hilbert-function contradiction 排除；\(t=0\) 支现由 direct Hilbert calculation 闭合：公共 residual 28 点满足 \(\dim I_D(3)=2\)、\(\dim I_D(4)=7\)，两 independent contact cubics 若互素会产生 8 个 independent quartics，矛盾，因此必有 degree 1 或 2 common factor，返回已排除低次数 carrier。

23. **[T under the residual-triangle setup] Primitive five-quartic 分支降回 quadratic LD**。

24. **[T + OPEN] residual triangle 的准确剩余状态（2026-08-09 最新）**。  
    当前已无条件证明 common-pencil
    \[
    k=\dim(V_{AB}\cap V_{AC})\le1,
    \]
    并闭合 plane、quadratic carrier 与全部 quartic-defect \(\delta=2\) candidates。进一步的 transversality/UFD 证明现已**完全排除 general \(k=1\)**：
    - both non-isotropic 由 product-UFD、两个 carrier pieces 的横截长度与 contact-quadric 低重矛盾排除；
    - mixed isotropic/non-isotropic 由 rank5 difference 排除；
    - both isotropic 中先由 transverse \(CI(q,u,v)\) 证明 common quartic \(q\) squarefree，再按其 irreducible factors 在 \((v-v')(v+v')=q(u'-u)\) 两边的分配，用 \(dq=0\) 的交曲线 first-jet 矛盾排除 split assignment；same-side assignment 则强迫两 determinant nets 相同。
    因而
    \[
    \boxed{k=1\text{ impossible}},\qquad \boxed{U\cap V=0}.
    \]

    对 \(k=0\)，six-quartic map 的稳定数值归约仍为
    \[
    me=16,\qquad m\le4,
    \qquad (m,e)=(2,8)\text{ or }(4,4),
    \]
    但 deeper plane-16 / desmic / quadratic-cover 分析仍属于研究笔记，未升级为投稿定理。第 15a 条的 split-MacWilliams theorem 继续提供“mixed 3D 小配置 / 至少 471 个 weight-88/96 words”的无条件二分。**因此 residual-32 现在只剩 \(k=0\) 一个真正几何出口。**

---

## E. J1–J2 与 regular comparison

25. **[T] J1 canonical-module gluing exact sequence**  
    对两个 \(CI(4,4,4)\) 表示的公共/并集，得到自然 canonical-module 正合列；degree-eight relation space 可由局部对偶与 Jacobian residue 描述。

26. **[T] J2 orientation noncoherence ⇒ degree-eight saturation defect**  
    在公共块对八次式施加独立条件且 residual union 有 degree-eight defect 的输入下，Jacobian orientation 不相容会产生 degree-eight saturation defect。

27. **[Audit correction] J1–J2 只保证 degree-eight defect**  
    一般 local duality **不能**自动把 defect 下沉到次数 \(\le3\)。旧的“次数 \(\le3\) saturation 自动闭合”不能再当普遍定理使用。

28. **[T] Regular comparison：Smith–Cartan divisor 余维一可逆时产生 residual degree-eight defect**。

29. **[T] Coupled degree-0/1 Beilinson–Horrocks capacity theorem (Thm 21.5)**  
    genuinely coupled degree-0/1 Horrocks monad 不能出现在相应 corank-two length 的非零 symmetric octic representation 中，除非已出现 degree \(\le1\) line summand，因而返回低次数 saturation 路线。

30. **[Audit correction] 当前独立材料不足以声称整个 regular comparison outlet 闭合**。  
    当前稿独立重证的是 genuinely coupled degree-0/1 Horrocks block 的不可能性；投稿稿只把它作为 standalone obstruction，不再要求 Horrocks outlets exhaustive。

30a. **[T, disjoint-net normal-target setup] Residual-36 global six-quartic reduction（2026-08-09）**  
    对公共块 \(|A|=28\) 的两套 weight-64 determinant nets，若两 nets disjoint，则六 quartics 在
    \[
    Y=\operatorname{Bl}_A\mathbf P^3,\qquad D=4H-\sum E_a
    \]
    上定义 generically finite map 到 smooth quadric fourfold。精确数值为
    \[
    D^3=36,\qquad K_YD^2=-8,\qquad g(D^2)=33,\qquad me=18.
    \]
    若 target normal，则 general curve-section Riemann--Hurwitz 强迫
    \[
    \boxed{(m,e)=(2,9)\text{ or }(3,6)}.
    \]

30b. **[T] Finite normal \((2,9)\) 完整排除**  
    在 normal finite quadratic-target 情形，28 个 exceptional planes 首先强迫 pencil 出现 rank \(\le4\) member。旧的 rank3 singular-conic 特殊 fibre count 已撤回：finite 在 codimension-two singular locus 上不保证 flat。当前证明统一使用 self-adjoint Jordan classification，并且所有 degree-9 sheet bounds 都只在 generic-smooth target plane/line 上使用。rank3 的五型 `(2,1,1)+(2)`, `(2,1,1)+(1,1)`, `(4,1,1)`, `(3,2,1)`, `(2,2,2)` 已由 invariant-Lagrangian 数量、smooth-line pairings 或 codimension-one singular-plane contradiction 全部排除。rank4 时 radical line \(L\subset X'\)，并令 \(T=B_0^{-1}B_1\)。二维 eigenspace \(K\) 对 \(B_0\) 完全 isotropic，self-adjoint primary decomposition 只留下
    \[
    (J_2,J_2)_\lambda+(J_2)_\mu,\quad
    (J_2,J_2)_\lambda+(J_1,J_1)_\mu,\quad
    (J_2,J_4)_\lambda,\quad
    (J_3,J_3)_\lambda.
    \]
    四型的 invariant Lagrangian planes 可显式列出。若两张 common planes 沿 generic-smooth line 相交，则 finite map 在该 line 的 generic point flat of rank9，故对应 multiplicities 满足 \(n_i+n_j\le9\)。四型总容量依次至多18、27、18、18；最临界型满足
    \[
    2\sum n_i\le54\Longrightarrow\sum n_i\le27<28.
    \]
    因此
    \[
    \boxed{(2,9),\ X'\text{ normal},\ \phi\text{ finite}\Longrightarrow\bot}.
    \]
    这条排除不依赖旧 clean \((1,3)/(2,2)\) carrier 分类。

30c. **[T] Finite \((3,6)\) + isolated target singularities 排除**  
    Finite-map canonical formula 给出实际 ramification divisor
    \[
    R_\phi=\sum_{a\in A}E_a.
    \]
    General hyperplane section target 是 Euler number 24 的 smooth \((2,3)\) K3；source 是 quartic K3 blow-up 28 points，Euler number 52。Simple ramification stratification 则强迫 Euler number
    \[
    6\cdot24-28\cdot2=88,
    \]
    矛盾。故 finite cubic-target / isolated-singularity outlet 不存在。

30d. **[T consequence + OPEN] Residual-36 的真正剩余出口**  
    结合 30b 与 30c：finite normal quadratic target 已完全排除；finite cubic target 若 singularities isolated 也已排除。因此 normal finite survivor 若存在，只可能是
    \[
    \boxed{(m,e)=(3,6)\text{ with positive-dimensional singular locus}.}
    \]
    当前真正剩余为：normal finite cubic target with singular curve、nonfinite/divisorial-contraction，以及 nonnormal target。旧 clean rank-four \((1,3)/(2,2)\) 分类不再承担 finite quadratic branch 的逻辑。

---

## F. Jacobian residue 与 free-defect lattice

31. **[T] Hessian–Jacobian identity 与 \(0,\pm1\) residue vectors**。

32. **[T] Double-solid anti-invariant contact class construction**。

33. **[T] Jacobian–defect lattice pairing theorem**  
    在实际 globally split contact presentations 产生的 free defect classes 上，Jacobian residue vectors 与 integral defect classes 的实线性拟阵一致；Hodge–Riemann 给出相应负定性。

34. **[T] 额外整除性**  
    involution 对称性进一步压缩 residue-vector 内积的允许集合。

35. **[T] 三项 Jacobian circuit ⇔ residual triangle**  
    最小三项依赖强迫三个支撑形成三个 pairwise-only 32 点块，因此正是 residual triangle；若 triangle 已排除，则不存在三项 Jacobian circuit。

36. **[T] 四项 circuit 系数正规化**  
    最小四项实线性依赖可在符号归一后化成刚性系数形式。

37. **[T] 唯一四项 Gram 型**  
    支撑交数、八整除内积、正定性与无三项子 circuit 把候选压缩为唯一 Gram 类型；相应三维子格的 norm-minimal vectors 只有有限刚性集合。

38. **[T] 四项范数恒等式**  
    compatible quartic contact surfaces 给出 double cover 上线性等价，从而得到一个八次/四次多项式恒等式；这是旧 Cartan/双锥路线中可独立保留的代数成果。

39. **[T] Quartic carrier 的六条 edge curves**  
    同一 quartic carrier 同时承载六条异号交曲线；一对 opposite edges 的次数与其余四条不同，并且每个顶点附近的 edge degree sum 被严格确定。

40. **[T] Opposite-edge 2-torsion relation**  
    quartic carrier 的 Weil divisor class group 中，三对 opposite edges 的类差等于同一二挠类；若 carrier 光滑（quartic K3），Picard 无挠，故该二挠类必须消失。

**这整组结果不应因最终 \(u(8)\) 尚未闭合而删除。** 它们可单独发展为“Jacobian residues / defect lattice / short circuits”方法论文。

---

## G. Hidden defect、Jacobian saturation 与二阶变形

41. **[T] Relation-space 的局部–整体插值重写**  
    hidden relation 问题等价于：节点函数若在每个 weight-64 complete intersection 上局部来自八次式，是否全局来自一个八次式。

42. **[T] Hidden defect space 的线性代数定义与维数公式**。

43. **[T] 多集合版 J1 + clean gluing tree 充分判据**  
    若逐步加入 weight-64 sets 时公共块、saturation defect 与最终 relation 条件满足 clean tree 假设，则全局 gluing relation 完全由局部 ones 生成。

44. **[T] Defect-lattice 子格与 hidden defect rank relation**。

45. **[Audit correction] mod-2 annihilator 不会自动成为 weak-even word**  
    必须控制 defect lattice 判别群的 2-primary 部分；早期“缺失的一维就是 weak word”结论撤回。

46. **[T] Jacobian saturation excess 结构公式**  
    saturation excess 与 hidden defect 是两个不同量，不得混淆。

47. **[T] Equisingular second fundamental form**  
    determinant presentation 的 Jacobian relation 消灭相应二阶 equisingular obstruction；由此得到明确的二次映射约束。反向蕴含一般不成立。

---

## H. Weight 48：residual + contact quadric + 深层计算证书

48. **[L] Weight 48 是极小严格偶集**  
    Endraß：weight 48 当且仅当由 reduced contact quadric 切出；该 contact quadric 唯一。

49. **[T] 第一 residual**  
    固定 48-word 后
    \[
    R=[121,18],\qquad R\text{ 为 4-divisible},\qquad d(R)\ge24.
    \]

50. **[C→T] 五阶 MacWilliams 证书：\(d(R)\le48\)**  
    使用
    \[
    P_{48}(r)=-(r-52)(r-60)(r-64)(r-72)(r-76)
    \]
    及其非负 Krawtchouk expansion，排除 \(d(R)\ge52\)。因此
    \[
    \boxed{24\le d(R)\le48}.
    \]

51. **[T+C] 第一层 lift profiles 完整枚举**  
    Endraß 对 octic strictly-even 只额外禁止 weight \(56\)；\(88,96,104,112\) 必须保留。因此最小 residual 只可能出现在 \(r\in\{24,32,36,40,44,48\}\)，共有十个 lift profiles（含 \((48,88)\) 与 \((48,96)\)）。

51a. **[RETRACTED] 错误的 \(A_{48}\ge24\) 尝试**  
    曾因误读 Cor. 1.11 删除 \(88,96,104,112\)，得到 30-state split LP 与 \(A_{48}\ge24\)。该假设对 octic 不成立，结论撤回。使用正确重量集不能强迫单独的 \(A_{48}\) abundance。

51b. **[T+C] 正确的 global \(48/64\) trade-off（2026-08-08/09）**  
    在完整 strict octic spectrum 上，同一个 degree-five LP polynomial 给出精确恒等式并推出
    \[
    \boxed{A_{64}+21A_{48}\ge533}.
    \]
    因而：
    - 若 \(A_{48}\ge22\)，存在两 weight-48 words 交集 16 或 24；
    - 若 \(18\le A_{48}\le21\)，存在两 weight-64 words 交集 24/28/32/40；
    - 若 \(A_{48}\le17\)，存在两 weight-64 words 交集 28/32/40。
    这不是单独的 minimum-word abundance theorem，而是把 contact-quadric family 与 weight-64 determinant family 绑定起来的全局 trade-off。

52. **[T] 两个 contact quadrics 无公共平面时的 16 点交集上界**  
    若两个不同 weight-48 sets 的 contact quadrics 没有公共平面分量，则
    \[
    |W\cap W'|\le16.
    \]
    因而交集 24 强迫公共平面分量。该证明不要求 \(Q\cap Q'\) reduced。

53. **[C | conditional on \(A_{72}=0\)] d=24 weight-48 triangle 的第二 residual 精确枚举**  
    原脚本使用
    `STRICT = {0,48,64,*range(80,169,8)}`，即额外假设整个 minimum-distance-48 code 中不存在 weight-72 word。**前面的 weight-72 定理只排除了 \(d(K)=72\) branch，并没有推出 \(A_{72}=0\)；因此这一额外条件目前没有由主线证明。** 在该附加假设下，第二 residual 的首批可行距离为
    \[
    0,12,16,20,22,24,28,30,32,34,36,38,\ldots,
    \]
    \(d=12\) 只有 \((48,48,48,48)\)，\(d=16\) 只有 \((48,48,48,64)\) 的置换，且 \(d=18\) 不存在。

54. **[C | conditional on \(A_{72}=0\) + factor-graph rules] Factor-graph 过滤证书**  
    在上述额外 weight-set 限制以及 contact-plane factor-graph 规则输入下：
    - \(d=12,22,30\)：无 surviving profile；
    - \(d=20\)：仅 \((48,48,48,80)\)；
    - \(d=24\)：仅 \((48,64,64,64)\)；
    - \(d=28\)：仅 \((64,64,64,64)\)；
    - 其它距离的 surviving profiles 由脚本完整列出。

55. **[C | inheritance of the same extra weight-set hypothesis must be checked] d=28 四面体第三 residual 证书**  
    在原枚举所使用的 weight-set/filter 输入下：
    - 第二 residual 唯一 Venn 解 \((12,12,12;28)\)；
    - 七个非零列型 multiplicities 为 \(28,12,12,12,12,12,12\)；
    - kernel 恰有两个 profile；
    - third residual 不可能取 1,5,13；
    - 所有 \(d\le12\) 的可行 profile 都含 weight-48 lift；
    - 第一个 pure profile 是 \(d=14\) 的 \(64^8\)。
    投稿前应重跑“允许 72”的版本，确认哪些句子仍无条件成立。

---

## I. QT-lift 与 Smith-border comparison

56. **[T] Symmetric presentation 的 canonical quadratic/linking form**  
    对 \(2\times2\) symmetric determinant presentation 的 rank-one reflexive cokernel，adjugate 给出无分母 quadratic pairing，并唯一延拓到正常曲面。

57. **[T] Half-section square ⇒ self-dual similitude**  
    若 relative reflexive sheaf 的 half-section \(s\) 满足
    \[
    2\operatorname{div}(s)=\operatorname{div}(\tau|_X),
    \]
    则 linking-form compatibility 不是额外假设，而是自动推出的形式后果。

58. **[T in the irreducible-carrier setup] 常数同伦误差必须消失**  
    从 quadratic lift \(Q\) 与 \(\det Q=\tau\) 得到的常数 symmetric error matrix \(H\) 必为 0；当前证明关键使用 \(T=(\tau=0)\) **不可约**：quadratic vector \(Qk\) 在不可约 quartic 上恒消失而次数 \(2<4\)，故只能全局为零。若要推广到 reducible carrier，需要另证。

59. **[CT, irreducible quartic carrier] QT-lift 定理**  
    在 Smith-border/comparison 已经给出 global half-section、divisor-square relation 与 quadratic lift \(Q\)，并且 quartic carrier 不可约的设定下，经过整体符号归一，有严格多项式恒等式
    \[
    \boxed{\tau N=QMQ^t},
    \qquad
    \boxed{QM=N\operatorname{adj}(Q)^t}.
    \]
    因而旧的“linking-form compatibility GAP”已消失；真正上游只剩 Smith-border identification 本身。

---

## J. QT 下 normal-nodal quartic Smith carrier 排除

60. **[CT] 2×2 identity ⇒ auxiliary quadric**  
    QT 恒等式推出唯一二次式 \(h\)，并定义辅助 quadric \(H=(h=0)\)。

61. **[CT] Carrier nodes 与 octic nodes 分离**  
    quartic carrier 的节点集不与相关 corank-two scheme / octic node set 发生禁止的交叠。

62. **[CT] 公共 28 点 scheme-theoretically 落在 auxiliary quadric 上**，且两套 quartic nets 在该 quadric 上完全相同。

63. **[CT] Smooth auxiliary quadric 排除**  
    restricted quartic net 的 kernel bundle 有负判别式；destabilizing line subbundle + trace syzygy 强迫 carrier 沿曲线奇异。

64. **[CT] Reducible quadric / double plane 排除**。

65. **[CT] Quadric cone 排除**  
    无论顶点是否属于公共 28 点，都由 pullback kernel bundle 的极小 \(c_2\) 与 trace syzygy 得到非正常矛盾。

66. **[CT] Normal-nodal quartic Smith outlet 条件排除定理**  
    对 residual-36 comparison：若 nonregular comparison 的 quartic Smith carrier 不可约、正常、仅含普通节点，并且 Smith-border 输入成立，则该配置不存在。

**注意：** 此结果不覆盖 reducible / nonnormal / multi-component / embedded Smith divisor，也不证明 residual 36 出口完备性。

---

## K. 两个重要“负结果/纠错”也必须保留

67. **[T] Orientation flip 不是逐点可加的 Chern length**  
    单节点 Jacobian orientation flip 可由常数 congruence 实现，而 matrix factorization 仍同构；不存在“每个 mismatch 点固定贡献 comparison-cone 长度”的普遍公式。这个反例直接否定旧路线的一种错误局部化解释。

68. **[T] Residue Gram lattice 不能检测全部 Artin–Mumford torsion**  
    free-defect lattice / primitive closure 不能一般性恢复 double solid 全部 2-torsion；十节点 quartic symmetroid 给出反例。因此 Jacobian–defect pairing 的正确适用范围是 free integral defect lattice，而不是普遍 torsion detector。

---

## L. 真正未闭合的边界（保留，不与“已完成成果”混淆）

69. **[OPEN]** Smith-border identification 对 reducible / nonnormal / embedded carriers 的独立完整审计。
70. **[OPEN]** PC：长度 5 Artin scheme 集中于高阶 cubic singularity 的局部分类。
71. **[OPEN]** TC：10+18 标准形的 many-presentations 全局兼容性。
72. **[OPEN after stronger reduction]** residual 36 尚未完整闭合，但 disjoint-net normal-target 情形已压到 \((2,9)/(3,6)\)。Finite normal \((2,9)\) 已由 self-adjoint Jordan / invariant-plane sheet count 完全排除；finite \((3,6)\)+isolated target singularities 也已排除。因此 normal finite survivor 若存在，只能是 cubic target with singular curve。真正剩余是 finite cubic target with positive-dimensional singular locus、nonfinite/divisorial，以及 nonnormal target；QT/Smith 保留为这些退化出口的 supplementary 工具。
73. **[OPEN, non-global]** residual 40A nonregular comparison。该 local profile 已被 \(A_{64}\ge533\)+incidence 从 minimum-64 的全局主分支中绕开，无需 residual-32 exclusion。
74. **[OPEN after global trade-off]** weight 48 的 first-residual 主分类仍为 \(r\in\{24,32,36,40,44,48\}\) 的十个 profiles，但已由
    \[
    A_{64}+21A_{48}\ge533
    \]
    获得全局 pair compression；几何上 contact-quadric 交集 24 强迫公共平面，而无公共平面时交集至多16。B16/B24/A32/A40 atom 的进一步 contact-factor 分类仍属研究阶段，未形成批量排除。
75. **[OPEN]** 最终全局极值结论（本成果库不宣称 \(u(8)\le168\)）。

---

# 建议的论文拆分（不要再“为了投稿”丢结果）

### Paper A — Divisible codes and low-weight even sets on nodal octics
保留 A–C + H 的无条件部分：weight 72 排除、weight 64 determinant/residual/40B、\(A_{64}\) 与 incidence、weight 48 residual、16 点 contact-quadric 交集上界、计算证书。

### Paper B — Jacobian residues and defect lattices for symmetric contact presentations
保留 E–G：J1/J2、regular comparison、Jacobian–defect pairing、short circuits、four-term Gram/carrier、hidden defect、saturation excess、second fundamental form。即使不能解决最终 octic node bound，这组方法本身有独立价值。

### Paper C / companion — QT comparison and quartic Smith carriers
保留 I–J：canonical quadratic form、half-section square、QT-lift、normal-nodal carrier 的 auxiliary-quadric/syzygy 排除。上游 Smith-border identification 要单独审计。

### Research appendix / computational companion
保留 weight-48 second/third residual 全部有限证书以及 factor-graph profile tables。

**原则：投稿主文可以拆，但成果库不删。**
