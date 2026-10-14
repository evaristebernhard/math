# Seven Limit Cycles in a Periodically Forced Three-Zone Equation

论文研究固定方程

\[
\dot x=-9x+\frac{21}{2}\operatorname{sat}(x)
       +\frac{181363}{100000}\sin t.
\]

主定理：这个方程在相位圆柱上有**至少七个不同的孤立周期轨道**。

作者为 **Chaoyu Hu**（杭州电子科技大学自动化学院）和 **Jizheng Chen**（长安大学数学系）。英文单位、地址和邮箱沿用本仓库其他论文中的作者信息。

## 论文的证明

[paper/main.tex](paper/main.tex) 包含完整论证：

1. 给出三个分区的显式解。
2. 推导带偏置的响应恒等式和四次切换的停留时间导数；通过显式积分、三角展开和 Cramer 消元，得到两个停留时间变量的匹配方程，说明固定参数如何选出。
3. 用有理初值、切换时刻的有理区间和带余项界的有限 Taylor 展开，证明返回位移在三个不相交区间上变号。
4. 排除擦碰，证明返回映射在这些区间上解析，进而得到三个孤立周期轨道。
5. 构造唯一的半周期反对称轨道，并用停留时间界证明它孤立。
6. 半周期反射给出另外三个孤立周期轨道，总共至少七个。

正文包含 9 篇相关文献及响应／停留时间图，给出临界曲线、转折点和有理参数的构造过程。摘要、引言和第 3.3 节说明符号计算在积分、消元和约化中的作用。

附录列出全部有理输入、区间运算规则、严格符号界，并展开 `y=-0.571` 的完整代入算例。读者可按这些公式直接核对证明中的估计。

## 编译

在本目录运行：

    make paper

或进入 `paper`，逐次运行：

    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex

## 辅助核算与研究记录

[proof/rational_bounds.py](proof/rational_bounds.py) 用精确有理数和整数取整核算论文的界，沿用旧脚本的切换结构和有理输入，以 Fraction 实现区间运算。

    python3 proof/rational_bounds.py

[proof/certify_seven.py](proof/certify_seven.py) 保留原有 Decimal 核算；实验代码和数据保留在 `experiments` 与 `paper/figures` 中。它们用于辅助检查和研究。

参数邻域的扩展研究单独保存在 `paper/robustness.tex` 和 `proof/certify_parameter_persistence.py`。

[notes_discovery.md](notes_discovery.md) 记录发现过程；`research` 目录保存数量上界的后续研究。

相关文献：[Bravo et al., arXiv:2507.06705](https://arxiv.org/abs/2507.06705)。

