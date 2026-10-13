# 配电网鲁棒安全接入容量算法

本目录为**中文算法论文**，研究问题是：在光伏注入不确定、逆变器视在功率受限的情况下，给出配电网能够连续、安全接入的新增负荷容量。

**不要求证明增益全局最优。** 论文的主体是安全容量判定算法：非线性 DistFlow、隐函数 Jacobian、负荷与光伏扰动分块 Hessian、半圆支撑函数、复功率几何电流界、光伏有功--无功联合容量约束、自适应区间覆盖。外层增益协调仅作为提高算法输出容量的应用。

## 目录

- `paper/main.tex`：中文论文主文件；正文分为 `paper/sections/01_problem.tex` 至 `04_experiments.tex`。
- `paper/REPRODUCIBILITY.md`：数值结果的证据等级、尚缺实验与验证任务。
- `results/ieee33_design_trials.csv`：IEEE 33 节点三组增益及其双精度候选容量。
- `algorithm/connected_prefix.py`：独立可运行的完整负荷区间覆盖算法驱动器。它需要外部接入实际的 DistFlow/Hessian/复功率/PV 安全判定器，不等于 IEEE 33 潮流求解器。
- `algorithm/tests/test_connected_prefix.py`：测试完整覆盖、未知区间和有限候选增益选择。

## IEEE 33 节点实验参数

基于 MATPOWER case33bw 的 32 条有效径向支路，原始负荷缩放 0.65。9、18、24、33 号节点分别设置 0.25 MW 标称光伏、0.125 MVA 右半圆扰动与 1 MVA 逆变器。18 号节点新增单位功率因数负荷。电压限值 0.95--1.05 pu，线路电流统一限值 0.31 pu **仅为研究设定，不是真实线路额定值**。

| 增益（9、18、24、33） | 全负荷区间双精度候选容量 |
|---|---:|
| (1.92,1.92,1.92,1.92) | 1.0586 MW |
| (3.70,1.92,2.12,2.52) | 1.1363 MW |
| (3.80105,1.89598,2.39520,4.0) | 1.1500 MW |

以上是**普通浮点计算得到的安全内界候选**，不能称为已经严格证明的全扰动安全容量。增益协调带来的 8.63% 提升也是计算目标的改善，尚非可证明的物理容量提升。

## 编译与检查

安装 XeLaTeX、中文宏包及 Noto CJK 字体后：

```bash
make -C distribution_capacity_algorithm/paper paper
cd distribution_capacity_algorithm
python3 algorithm/connected_prefix.py
python3 -m unittest discover -s algorithm/tests -v
```

GitHub Actions 会构建中文 PDF 并上传为工作流产物。上一个研究目录 `droop_closed_loop_wclf/` 保留了原始数学分析与部分代码；没有丢弃 Hessian 工作。

**待完成的核心内容：** 将 IEEE 33 完整实验依赖合入仓库；以严格向外包络重新验证整个安全负荷前缀；进行完整的同模型消融、运行时间和其他馈线实验。
