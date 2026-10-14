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
2. 用有理初值、切换时刻的有理区间和带余项界的有限 Taylor 展开，证明返回位移在三个不相交区间上变号。
3. 排除擦碰，证明返回映射在这些区间上解析，进而得到三个孤立周期轨道。
4. 构造唯一的半周期反对称轨道，并用停留时间界证明它孤立。
5. 半周期反射给出另外三个孤立周期轨道，总共至少七个。

附录列出全部有理输入、区间运算规则、严格符号界，并展开 `y=-0.571` 的完整代入算例。论文中的证明不要求读者运行 Python，也不把程序输出作为证明前提。

本稿只陈述这组固定参数的存在性结果。“至少七个”不等于“恰好七个”；后者还需要排除其他周期轨道。

## 编译

在本目录运行：

    make paper

或进入 `paper`，逐次运行：

    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex

## 辅助核算与研究记录

[proof/rational_bounds.py](proof/rational_bounds.py) 用精确有理数和整数取整核算论文的界；浮点数只用于显示结果。它与旧脚本共用切换结构和有理输入，因此不是独立的轨道结构证明。

    python3 proof/rational_bounds.py

[proof/certify_seven.py](proof/certify_seven.py) 保留原有 Decimal 核算；实验代码和数据保留在 `experiments` 与 `paper/figures` 中。它们用于辅助检查和研究。

`paper/robustness.tex` 及 `proof/certify_parameter_persistence.py` 保留此前参数邻域的扩展研究，**不再纳入本稿**。主定理的证明不依赖这部分内容。

[notes_discovery.md](notes_discovery.md) 记录发现过程；`research` 目录保存数量上界的后续研究。

相关文献：[Bravo et al., arXiv:2507.06705](https://arxiv.org/abs/2507.06705)。

