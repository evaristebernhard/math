# Seven Limit Cycles in a Periodically Forced Three-Zone Equation

论文研究固定方程

\[
\dot x=-9x+\frac{21}{2}\operatorname{sat}(x)
       +\frac{181363}{100000}\sin t.
\]

主定理：这个方程在相位圆柱上有**至少七个不同的孤立周期轨道**。
稳定性推论：其中可以选出四个局部渐近稳定的吸引环和三个排斥环，中央反对称环是双曲排斥环。该结论由严格位移变号、标量序和半周期映射直接推出。

作者为 **Chaoyu Hu**（杭州电子科技大学自动化学院）和 **Jizheng Chen**（长安大学数学系）。英文单位、地址和邮箱沿用本仓库其他论文中的作者信息。

## 论文的证明

[paper/main.tex](paper/main.tex) 包含完整论证：

1. 给出三个分区的显式解。
2. 推导带偏置的响应恒等式、四次切换的停留时间导数和四段匹配条件，说明停留时间竞争、擦碰与固定参数的选择。
3. 用有理初值、切换时刻的有理区间和带余项界的有限 Taylor 展开，证明返回位移在三个不相交区间上变号。
4. 排除擦碰，证明返回映射在这些区间上解析，进而得到三个孤立周期轨道。
5. 构造唯一的半周期反对称轨道，并用停留时间界证明它孤立。
6. 半周期反射给出另外三个孤立周期轨道，总共至少七个。

论文面向 Qualitative Theory of Dynamical Systems，按常微分方程定性理论与动力系统方向组织，主要内容是极限环数量与稳定性、返回映射、停留时间竞争、擦碰和半周期对称性。正文给出临界曲线、转折点、有理参数的构造过程及响应／停留时间图。参考文献表收录 14 篇已发表文献，两篇预印本在正文署名并提供链接。

摘要按期刊的 150--250 词要求调整；注明通讯作者 Chaoyu Hu，文末包含资助、利益冲突、作者贡献、数据可用性和 AI 使用声明。两位作者共同参与构造、证明检验及修改；本研究无专项资助和利益冲突。

正文说明本模型与原文献的参数对应为 a=-A, b=B，并按预印本所述将五环猜想归于 Carmona、Freire、Ponce 和 Torres（2003）的工作。掠碰命题区分局部消失的停留时间与总停留时间；带偏置周期响应的点态序、均值坐标及中央轨道的首次切换均给出论证。半周期映射的共轭关系同时用于孤立性和稳定性。

第二轮复核明确了停留时间在整个射击区间上的定义，以及标量返回映射没有高周期点的理由。掠碰命题展开差商的变常数公式，区分状态流的 C1 参数依赖与外区访问时长的平方根律。新增文献涉及 Massera 的周期解存在理论、Mawhin 的多重性结果、两分区方程任意多环的构造、分段线性系统的结构分类、Abel 方程的环数问题、掠碰正规形和 Schwarzian 返回映射方法；各篇均在相关正文位置引用。

附录列出全部有理输入、区间运算规则、严格符号界，并展开 `y=-0.571` 的完整代入算例。读者可按这些公式直接核对证明中的估计。

## 编译

在本目录运行：

    make paper

或进入 `paper`，逐次运行：

    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex

## 辅助核算与研究记录

[experiments/matching_response.py](experiments/matching_response.py) 按正文的显式仿射匹配方程重新生成图的采样数据，并核对临界停留时间、振幅及近似周期轨道。图中的采样值为近似值；七环证明使用附录的有理估计。

[proof/rational_bounds.py](proof/rational_bounds.py) 用精确有理数和整数取整核算论文的界，沿用旧脚本的切换结构和有理输入，以 Fraction 实现区间运算。

    python3 proof/rational_bounds.py

[proof/certify_seven.py](proof/certify_seven.py) 保留原有 Decimal 核算；实验代码和数据保留在 `experiments` 与 `paper/figures` 中。它们用于辅助检查和研究。

参数邻域的扩展研究单独保存在 `paper/robustness.tex` 和 `proof/certify_parameter_persistence.py`。

[notes_discovery.md](notes_discovery.md) 记录发现过程；`research` 目录保存数量上界的后续研究。

相关文献：[Bravo et al., arXiv:2507.06705](https://arxiv.org/abs/2507.06705)。

