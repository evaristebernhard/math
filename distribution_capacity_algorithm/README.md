# 配电网鲁棒安全接入容量算法

本目录为**中文配电网算法论文**，研究问题是：在光伏注入不确定、逆变器视在功率受限的情况下，给出配电网能够连续、安全接入的新增负荷容量。

论文的主体是**安全容量计算与协调增益设计的一体化算法**：非线性 DistFlow、隐函数 Jacobian、负荷与光伏扰动分块 Hessian、半圆支撑函数、复功率几何电流界、光伏有功--无功联合容量约束、自适应区间覆盖。根据各节点电压、电流和逆变器功率约束，增益协调在每轮容量计算后更新设计变量。

## 这版论文的定位

**核心问题：** 给定光伏不确定范围和逆变器运行范围，通过非线性 DistFlow 数值求解、结构化 Hessian/复功率边界和逆变器增益协调，共同计算新增负荷的安全接入容量。

正文已有 **4 张可由 LaTeX 源码复现的矢量图**：IEEE 33 节点实际接线、容量算法流程、三组增益容量对比、固定光伏扰动下的非线性潮流电压响应。4 幅图位于 `paper/figures/`，并直接编入主文。

`algorithm/ieee33_solver_demo.py` 是能够运行的非线性 DistFlow + 实际逆变器无功限幅潮流求解脚本，从兄弟研究目录的 `exact_design_upper.py` 读取 IEEE 33 节点参数，使用 SciPy 求解并重算图中电压曲线。其原始绘图数据收录在 `results/ieee33_fixed_disturbance_voltage.csv`。

运行：

```bash
python3 -m pip install numpy scipy
python3 distribution_capacity_algorithm/algorithm/ieee33_solver_demo.py
make -C distribution_capacity_algorithm/paper paper
```

工程数值论文采用收敛的非线性潮流求解、约束裕度与同条件对比来评价算法；形式化区间算术证明不是本论文的必要前提。但**固定扰动的潮流曲线不能冒充全光伏扰动集的最坏情况结果**。

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

## 新增同模型消融实验

`results/ieee33_method_ablation.csv` 保存 IEEE 33 节点在**同一物理模型、同一光伏半圆扰动和同一逆变器完整视在功率约束**下四种算法的容量判定与运行时间。整体 Hessian、分块 Hessian + 标量电流、分块 Hessian + 复功率电流、两种电流界取较紧者进行逐项对比。2048 个角度，初始容量单元 0.02 MW，最小 0.00025 MW。协调增益方案下标量电流界约 0.83 MW 起停止接受，复功率界完整通过 1.15 MW。对 0.80 MW 运行时间单独重复 3 次，结果见实验章节。
