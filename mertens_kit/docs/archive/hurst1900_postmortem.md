# NU=1900 warm-start 标定复盘（2026-07-27）

## 结论

这次运行验证了 **跨 NU 的格提升实现正确**，但否定了“增加 NU 后，固定
block size 的 LLL/BKZ 会按原比例兑现搜索预算”这一性能模型。

- `[PARITY VERIFIED]`：NU900 → NU1900 的整数变换、重构、行列式以及
  100/160 位 scorer 均通过。
- `[PARITY BROKEN]`：原先以 `eta >= 0.90` 预测有效预算增长的模型与实测
  不符；实测 `eta=0.149276`。
- 当前的 **单核、12 小时、LLL + 单-tour BKZ-20/40 + 单个 Babai**
  路线不应继续启动 m800。它不是数学上的“不可能性证明”，而是对当前
  算法和资源约束的 No-Go 结论。

完整机器可读记录：

- `work/probes/hurst1900_warm_seed20260726/campaign.json`
- `work/probes/hurst1900_warm_seed20260726/m460_n1900/lift000.json`
- `work/probes/hurst1900_warm_seed20260726/m460_n1900/cleanup000.json`

## 1. 运行证据

### 1.1 精确 warm lift

源格为 m460/NU900 的原始 basis 和 LLL checkpoint，目标格为相同 active
set 的 m460/NU1900 basis。恢复出的整数变换 `U` 满足：

```text
exact_division_remainders       = 0
source_reconstruction_differences = 0
target_reconstruction_differences = 0
det(U)                          = 1
U * B900                        = R900
warm basis                      = U * B1900
```

关键 SHA-256：

```text
NU900 LLL parent  48ee6e1ec76772a6e2c9e1e94874d4f5d7244aa8519211d105900a10aba535fb
warm basis        e4b2202afd26a5ab7716ef95f81b7d768c03611e19357e904b410fae917095b7
wrapper LLL       69f8c1572084f2726e3f3ff947a59b6daae5ec7211ea9045f3eca38e8eb6030b
BKZ-20            00c7341c40302f0937a8dadc5cdb6e6ee9883b4ff4e029f76a56e35a6a9b1f93
```

因此结果差不能归因于错格、错 active set、非幺模变换或 scorer 精度。

### 1.2 墙钟和 fallback

| 阶段 | 结果 | 墙钟 | 峰值 RSS |
|---|---|---:|---:|
| 冷启动 wrapper baseline | 1245 秒时无完整矩阵 | 1245.160 s | 91.8 MiB |
| warm heuristic/longdouble | `infinite loop in babai`，保留完整输出作为下一父本 | 521.322 s | 51.7 MiB |
| warm heuristic/MPFR-256 | timeout，无矩阵 | 600.070 s | 105.1 MiB |
| warm wrapper | 完成 | 1107.531 s | 183.8 MiB |
| warm cleanup 合计 | 完成 | 2228.923 s | 183.8 MiB |
| BKZ-20/DPE | `infinite loop in babai` | 17.744 s | 56.5 MiB |
| BKZ-20/longdouble | `infinite loop in babai` | 30.974 s | 57.7 MiB |
| BKZ-20/MPFR-256 | 单 tour，按 loop limit 正常提交 | 100.289 s | 109.3 MiB |

warm-start 的价值是取得了一个可验证的完整 checkpoint；它没有证明比
cold-start 更快，因为 cold baseline 本身没有完成，不能形成完成时间比值。

### 1.3 得分和有效预算

同一 m460 active set：

| checkpoint | `h_H` | raw budget | `B_eff` | budget tax | `rho` | `kappa=rho^2` |
|---|---:|---:|---:|---:|---:|---:|
| NU900/BKZ-20 | 1.312456 | 612.742 | 157.124 | 455.619 | 2.446 | 5.985 |
| NU1900/wrapper | 1.479092 | 1305.889 | 280.799 | 1025.090 | 8.373 | 70.107 |
| NU1900/BKZ-20 | 1.458237 | 1305.889 | 260.594 | 1045.295 | 8.706 | 75.790 |

两份 NU1900 checkpoint 的 MPFR-384 Babai 与 100/160 位 canonical scorer
均为 `VERIFIED`，`h_H` 差分别约为 `3.69e-100` 和 `1.61e-100`。

BKZ-20 的这个单一 Babai 候选还低于 wrapper 候选。这不表示 BKZ
“数学上变差”，而是说明“基更强”并不保证固定 target、固定行序、只取一个
Babai 输出时的非齐次候选分数单调。

## 2. 为什么增加 1000 bit 只得到很少收益

令 `n=mH`，`c_y` 为格中的整数 y 坐标。忽略取整常数后，嵌入的 CVP
目标可写成

```text
||v-t||^2 ~= c_y^2 + 2^(2 NU) * sum_j w_j theta_j(c_y)^2,
```

归一化为

```text
F_NU(c_y) = 2^(-2 NU) c_y^2 + sum_j w_j theta_j(c_y)^2.
```

若能够在约 `C` 个近独立候选中真正找到最好的一个，同时逼近误差按
`C^(-2/n)` 缩小，则平衡两项得到

```text
C_opt   ~ 2^(NU*n/(n+1)),
D_ideal ~ 2^(-2*NU/(n+1)).
```

对 `n=460`，NU900 → NU1900 的理想余弦损失为：

```text
D_ideal(900)  = 0.07083233895
D_ideal(1900) = 0.003669589283
理想改善倍数 = 19.3025
```

这与倾斜/KL 理想模型一致。问题不在“NU 没有提供原始搜索范围”，而在当前
约化算法没有把这段范围变成相同数量级的可用候选。

实测损失：

```text
D_obs(NU900/BKZ20)    = 0.4238980762
D_obs(NU1900/wrapper) = 0.2572627663   改善 1.6477 倍
D_obs(NU1900/BKZ20)   = 0.2781173788   改善 1.5242 倍
```

定义算法近似罚：

```text
kappa = D_observed / D_ideal = rho^2.
```

wrapper 路径的 `kappa` 从 `5.985` 增至 `70.107`，恶化 `11.71` 倍，
抵消了大部分理想收益。在小损失近似下：

```text
B_eff ~= B_raw - (n/2) log(kappa).
```

由 `kappa` 增长预测的额外预算税为

```text
(460/2) * log(70.107/5.985) = 565.99 nats,
```

而实测 budget tax 增量为 `1025.090-455.619=569.47 nats`。二者接近，
说明主要问题是 **算法近似因子随 NU/条件数恶化**，不是 scorer 或 lift
实现错误。

### 几何原因

NU 增加时，前 `mH` 个相位坐标约放大 `2^DeltaNU`，最后的 `c_y`
坐标不按同一比例放大。格因此变得更各向异性，而不是整体均匀缩放。
提高 MPFR 位数只让 GSO/Babai 更可靠、代价更高；它不会自动增加枚举的
候选数量。固定维度下的 LLL、固定 `beta` 的单-tour BKZ、再取一个 Babai，
不能等价地遍历 NU 新增的指数级候选熵。

## 3. 原 eta gate 为什么不合理

原 gate 定义：

```text
eta = Delta B_eff / Delta B_raw
```

并要求 `eta >= 0.90`。它隐含预测：

```text
B_eff(1900) >= 157.124 + 0.90*(1000 ln 2) = 780.956 nats.
```

这个数恰好接近 m800 过线所需的 `771.015 nats`，但在运行前没有独立证据
支持。等价地，它要求 m460 的损失至少改善

```text
exp(2*0.90*1000*ln(2)/460) = 15.064 倍。
```

实测 wrapper 只改善 `1.648` 倍，BKZ-20 只改善 `1.524` 倍，因此
`eta=0.149276`。以后 `eta` 只能作为观测量，不能把 `0.90` 当成从
NU900 可外推的默认性能假设。命令行中保留该参数仅用于复现实验。

## 4. 复杂度与时间应该怎样估

LLL 的位复杂度是维度和输入 bit-length 的多项式，但 fplll 的实际墙钟还
取决于 swap 数、Babai 次数、GSO 刷新、精度升级和输入基质量。单写一个
大 O 不能给出可靠完成时间；必须同时给经验包络和运行时计数。

NU900 wrapper 的同机样本：

| dimension | 时间 |
|---:|---:|
| 261 | 60.405 s |
| 361 | 94.496 s |
| 461 | 148.267 s |

同 NU 的经验拟合为 `T ~= 0.00964*d^1.568`。再用 bit-length 指数
`p=2,3,4` 给 NU900 → NU1900 包络：

| 任务 | p=2 | p=3 | p=4 | 实测 |
|---|---:|---:|---:|---:|
| m460 warm LLL | 661 s | 1395 s | 2945 s | wrapper 1108 s |
| m800 warm LLL | 1533 s | 3237 s | 6834 s | 未运行 |

该表只估 LLL 完成时间，不估结果质量，也不包含 parent LLL、fallback、
BKZ 和搜索。m460 实测落在包络内，说明“27 分钟还没结束”本身不异常；
真正否定路线的是完成后的 `kappa/eta`，不是单纯运行慢。

如需可解释的中途 ETA，必须给 fplll 内层增加并持久化：

```text
iteration, swap_count, babai_count, gso_refresh_count, elapsed
```

只重新编译未插桩的同一份 fplll 不会产生这些信息。当前仓库的
instrumentation patch 尚未完成编译和运行验证，因此其状态是
`[PARITY UNVERIFIED]`，不能拿它宣称已获得算法内部进度。

## 5. m800 的可行性边界

m800/NU1900 的理想模型本身可以越过目标：

```text
A_H                         = 1.9464180118
ideal heavy score           = 1.9047115877
Meff=1000 q10 tail harvest  = 0.0242611975
ideal total                 = 1.9289727852 > 1.826054
```

所以这不是数学不可能性。但实际过线至少需要：

```text
required h_H    = 1.8017928025
required B_eff  = 771.0151972 nats
required rho    < 1.8621751
required kappa  < 3.4676962
```

当前 m460 wrapper 已是 `rho=8.373, kappa=70.107`。在维度从 461 增至
801 的同时，还要求 `kappa` 改善约 `20.2` 倍（`rho` 改善约 `4.5`
倍），这与固定-beta 单-tour 路线的观测趋势相反。

若把当前可兑现预算直接代入 m800 理想反解：

| 假设 `B_eff` | heavy | heavy + q10 tail |
|---:|---:|---:|
| 260.594 | 1.486830 | 1.511092 |
| 280.799 | 1.510017 | 1.534279 |
| 350 | 1.577915 | 1.602176 |
| 500 | 1.684479 | 1.708740 |
| 700 | 1.777346 | 1.801607 |
| 771.015 | 1.801793 | 1.826054 |

因此当前决定是：**停止 m800 campaign，不再靠提高 MPFR 精度或重复相同
单-tour 期待跨越缺口。** 重新开放路线前，必须先出现能显著降低
`kappa` 或产生大量有效独立候选的新 primitive，例如更强的 CVP/enumeration、
多候选解码、重新缩放/预条件，或在可负担维度上的显著更强 BKZ；并先在
m460 做可复现的小规模门控。
