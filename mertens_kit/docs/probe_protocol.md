# q(d,β) 隔离变量标定协议

本项目的目标是提升可严格认证的数论极限，不是追逐未审计的浮点峰值。

`L_H_pred/A_H` 是理想倾斜天花板；实际候选必须报告：

- `q_eff = h_H/A_H`（直接实际效率）；
- `q_ideal = h_H/L_H_pred`（理想预算兑现率）；
- 二次损失、真实余弦损失及 `rho`；
- checkpoint SHA-256 与精确 `c_y/2^NUY`；
- 100/160 位 canonical scorer parity。

标定固定 `mH=260,360,460`、`NU=900`、一个 seed。每个 m 只做一次
LLL；BKZ-20 和 BKZ-40 各自直接读取同一个 LLL checkpoint，均为单 tour。
同父 LLL 差分不混入累计 tour，但固定 NU 的 q 不能跨 NU 外推。正式模型
使用 `L_H^ideal(B_eff)=h_H^real`，并比较 `ΔB_eff/Δβ`。

```bash
python3 s06_probe.py --jobs 6 --wall-hours 4
```

只有预测可过线的 1–2 组才允许后续长跑。BT2015 14 链与 BKZ-50 派生
分别要求显式 `--campaign bt2015-14` 和
`--campaign bkz50-escalation`。

`1.37223054` 目前只按确定性搜索观察处理；仓库没有与它对应的严格 Arb
证书。相同 seed 重现并完成 Arb 认证之前，不标记为认证结果。现有
checkpoint/result/certificate 只读保留，新标定产物写入 `work/probes/`。

## 2026-07-26 首轮结果

| mH | dim | q20 | q40 | Δq/10β |
|---:|---:|---:|---:|---:|
| 260 | 261 | 0.852494 | 0.852952 | +0.000229 |
| 360 | 361 | 0.791505 | 0.811143 | +0.009819 |
| 460 | 461 | 0.755869 | 0.787624 | +0.015877 |

全部 checkpoint 完整提交，原始行序 MPFR-384 Babai 的 100/160 位
canonical scorer parity 全部通过。它们确认 NU=900 No-Go；后续
NU=1900 campaign 以 m460/BKZ-20 测量 `η=ΔB_eff/ΔB`。

## 2026-07-27 NU1900 结果与协议修正

历史设计曾写成“只有 `eta>=0.90` 才进入 m800”。这个条件可以作为停止
gate，但把 0.90 当成可预期性能是不合理的：它隐含
`B_eff(1900)>=780.956`，运行前没有数据支持。现保留参数只为重现实验，
不再把它写成算法会达到的预测。

精确 lift 与 scorer 均通过：

```text
NU900 -> NU1900: det(U)=1
exact division remainders=0
source/target reconstruction differences=0
MPFR-384 Babai + 100/160 dps scorer parity=VERIFIED
```

实测：

| checkpoint | `h_H` | `B_eff` | `rho` | `kappa=rho^2` |
|---|---:|---:|---:|---:|
| m460/NU900/BKZ-20 | 1.312456 | 157.124 | 2.446 | 5.985 |
| m460/NU1900/wrapper | 1.479092 | 280.799 | 8.373 | 70.107 |
| m460/NU1900/BKZ-20 | 1.458237 | 260.594 | 8.706 | 75.790 |

以 BKZ-20 口径得到 `eta=0.149276`，campaign 状态为
`eta_gate_no_go`，m800 未启动。以后跨 NU 的门控顺序改为：

1. 先验证 lift 与双精度 scorer parity；
2. 报告 `D_ideal`、`D_observed`、`kappa`、`B_eff`，不只报告 `q`；
3. 只有小维标定已达到主实例所需的 `rho/kappa` 数量级，才放大维度；
4. 单个 Babai 分数不假定随 BKZ 单调，至少报告 checkpoint 本身和候选
   生成策略；
5. MPFR 精度升级只处理数值失败，不能当成增加搜索强度；
6. Hurst m800 当前保持停止，直到新 primitive 在 m460 显著降低
   `kappa`。

完整推导、时间复杂度包络和 artifact SHA-256 见
`docs/archive/hurst1900_postmortem.md`。
