# Mertens 数论极限提升项目（柱算法 / BKZ 实验平台）

目标: 用可复现、可审计、最终可做 Arb 认证的「重块投影格 + 轻块收割」
柱算法推进 Mertens 振荡的数论极限:
1.061545 (已破, 本仓库认证到 1.1837045609831252) → 1.218 (已破) →
**1.6383 (Best–Trudgian 2015)** →
**1.826054 (Hurst 2016 预印本 / 2018 正式发表)**。

## 已在沙箱验证过的部分 (你拿到的不是纸面设计)

| 组件                       | 验证结果                                                                                 |
| -------------------------- | ---------------------------------------------------------------------------------------- |
| otr1985 (dim 81, BKZ-20)   | **Arb 认证 h_lo=1.1837045609831252 > 1.1215 > 1.061545**                           |
| 数据解析                   | 复现 K–N 发表值 h_StR = −1.007452 @ y=1.9571878850562201959e19                         |
| validate (dim 141, BKZ-20) | **2026-07-26 Arb 认证 h_lo=1.3580532527406444 > 1.218**（旧沙箱浮点记录 1.362365） |
| 维度约化税                 | 已确认理想 `L_H_pred/A_H` 不是实际效率；必须另测 `q(d,β)`                             |
| arb 零点                   | 0.01–0.10 s/零点 @457 位; γ₁ 与 K–N 数据逐位吻合                                     |
| 理想预算账本               | 1.826 的全局大偏差量级约 856 nats；这是理想搜索稀有度，不等于 LLL/BKZ 可兑现的 `B_eff` |
| NU1900 warm 标定           | lift/scorer parity 通过；m460 实测 `eta=0.1493`，当前单-tour 路线 **No-Go**           |

## 一、安装 (WSL2 Ubuntu 内)

```bash
sudo apt update
sudo apt install -y build-essential python3 python3-venv python3-dev \
                    libgmp-dev libmpfr-dev libfplll-dev fplll-tools
python3 -m venv ~/mertens-venv && source ~/mertens-venv/bin/activate
pip install -U pip numpy mpmath python-flint cython cysignals
pip install fpylll        # 若失败: sudo apt install python3-fpylll 并改用系统 python
fplll --version && python3 -c "import fpylll, flint; print('OK')"
```

内存: 16 GB 机器建议 `C:\Users\<你>\.wslconfig` 设 `memory=12GB`,
运行前关掉 Chrome; BKZ 单实例内存 <2 GB, 可 2–3 个种子并行。

## 二、数据放置

```
mertens_kit/
  data/zeroes.txt   data/alpha.txt   data/beta.txt   ← K–N Zenodo 包 (record 10775723)
  work/                                              ← 自动生成
```

⚠️ 解析陷阱: alpha/beta 的小数值行是科学计数法, 指数在 ~300 字符行的**末尾**。
本套件全部整行解析; 你若自写代码, 切勿截断行首解析。

## 三、运行顺序

```bash
cd mertens_kit
python3 s00_probe.py                      # CPU/内存/后端隔离探测
python3 s01_make_zeros.py --jobs 14 --resume
python3 s02_build_lattice.py validate     # 构格 + 倾斜预测
bash    s03_reduce.sh validate 20 --single
python3 s04_search.py validate work/validate_bkz20.txt --mode full --jobs 14
python3 s05_certify.py validate --jobs 14 --resume
```

所有阶段默认 `jobs=14`，所有 BLAS/OpenMP/fplll 内部线程固定为 1。s01 和
s05 的 shard、s03 的矩阵 checkpoint、s04 的结果都采用同目录临时文件
完成校验后再原子提交。

### 后端单-tour 基准

```bash
python3 s00_probe.py \
  --basis work/bt2015_basis.txt --meta work/bt2015_meta.json \
  --beta 20 --timeout 300
```

`dd/qd` 的 unsupported abort 在独立子进程内被捕获。只有输出是完整方阵且
MPFR-384 Babai 可解码时才标为 usable。可选的 workspace-local QD 构建用
`--start-qd-build` 后台启动，安装到 `.opt/fplll-qd`，不会替换系统 fplll。

### 隔离变量短探针（当前默认路线）

```bash
# m=260/360/460；每个 m 只做一次 LLL，BKZ-20/40 均从同一 LLL 分叉
python3 s06_probe.py --jobs 6 --wall-hours 4
```

输出位于 `work/probes/qcal_seed20260726/`，包含每个 checkpoint 的
SHA-256、原始行序 MPFR-384 Babai、100/160 位 scorer parity、
`h_H/A_H`、`h_H/L_H_pred`、`rho`、直接 `Δq/Δβ`、拟合残差和推荐参数。
DPE 失败才转 longdouble，再失败转 MPFR-256；截断矩阵从不提交。

本机首轮同父 LLL / 单-tour 实测：

| mH (dim) | q20=hH/AH | q40=hH/AH | Δq/10β |
| ---: | ---: | ---: | ---: |
| 260 (261) | 0.852494 | 0.852952 | +0.000229 |
| 360 (361) | 0.791505 | 0.811143 | +0.009819 |
| 460 (461) | 0.755869 | 0.787624 | +0.015877 |

六个 100/160 位 scorer parity 均为 `VERIFIED`。这些结果只证明
`NU=900` 下为 No-Go；不能把固定 NU 的 `q` 乘法拟合外推到高预算。

当前模型反解 `L_H^ideal(B_eff)=h_H^real`，报告原始预算、有效预算和
预算税。NU=900 的 BKZ-20 三点预算税约 443–456 nats，说明原先所谓
“维度 q 税”主要混入了每维预算变化。

### NU=1900 Hurst warm campaign：已完成标定，当前 No-Go

```bash
# 只用于查看或复现任务图；不要据此启动 m800
python3 s08_hurst1900_campaign.py --dry-run

# 已完成运行的只读审计
python3 -m json.tool \
  work/probes/hurst1900_warm_seed20260726/campaign.json | less
```

实测 m460/NU900 → NU1900 的精确 lift、完整 wrapper LLL 和
100/160 位 scorer parity 均通过，但 wrapper/BKZ-20 只得到
`B_eff=280.799/260.594`，相对 NU900/BKZ-20 的
`eta=0.1784/0.1493`；历史 gate `eta>=0.90` 被实测否定，m800 未启动。
原参数只保留作结果复现，不能再视为合理的性能假设。

数学推导、复杂度包络、运行时间、SHA-256 与 m800 可行性边界见
[`docs/archive/hurst1900_postmortem.md`](docs/archive/hurst1900_postmortem.md)。

不寻找具体巨大 `y` 的替代路线——极值正三角多项式、有限独立性、
内部 SVP、外部批量 CVP 与对偶过滤原型——见
[`docs/extremal_independence_program.md`](docs/extremal_independence_program.md)。
小规模真实零点原型入口为 `s09_dual_filter_prototype.py`；当前权重下的
`T,m,N_i` 最佳点规划扫描入口为 `s10_extremal_design_scan.py`。

### 显式长跑 campaign（默认关闭）

```bash
# 只有显式 campaign 才展开 BT2015 14 链：
bash s03_reduce.sh bt2015 20 30 40 --campaign bt2015-14 --jobs 14

# BKZ-50 派生还需第二个显式 campaign：
bash s03_reduce.sh bt2015 20 30 40 \
  --campaign bt2015-14 --campaign bkz50-escalation --jobs 14
```

14 链、BKZ-50 escalation、多 seed full search 均不再默认启动。

s04 的 `full` 模式至少扫描 4,000,000 个二维 AP 网格点、精算 200 个
finalists，并以 100/160 位独立重算写出 `parity=VERIFIED|UNVERIFIED`。
s05 优先直接解析 s01 保存的完整 Arb ball（不丢半径），缺失或精度不足的
区间才调用 `acb.zeta_zeros` 重算；parent 只按区间顺序相加局部严格球。

只复现 1985 年 Odlyzko–te Riele 的 `1.061545` 阶梯以及旧沙箱的
`1.1215` 超越记录，可运行较小的 81 维 stage：

```bash
python3 s02_build_lattice.py otr1985
bash    s03_reduce.sh otr1985 20
python3 s04_search.py otr1985 work/otr1985_bkz20.txt
python3 s05_certify.py otr1985
```

本环境 2026-07-26 的一手运行（重新构格、BKZ-20、搜索、20,000 零点
Arb 重算）得到严格球算术下界
`h_lo = 1.1837045609831252 > 1.1215 > 1.061545`；精确候选保存在
`work/otr1985_results.json`，认证包围保存在
`work/otr1985_certificate.json`。

validate 通过（本批次认证 h ≥ 1.358053；旧沙箱浮点记录 1.3624±）后:

```bash
python3 s02_build_lattice.py bt2015
nohup bash s03_reduce.sh bt2015 20 30 40 > work/bt2015_bkz.log 2>&1 &
python3 s04_search.py bt2015 work/bt2015_bkz40.txt && python3 s05_certify.py bt2015

# Hurst 当前没有推荐的长跑命令；先阅读 NU1900 标定复盘。
```

## 四、阶段参数与预期 (16C/32T, 单实例 BKZ)

| 阶段              | 维度 | NU(bits) | 零点源                  | BKZ 墙钟                     | 预期 h      | 超越                      |
| ----------------- | ---- | -------- | ----------------------- | ---------------------------- | ----------- | ------------------------- |
| validate          | 141  | 900      | K–N 301位              | 分钟级                       | ~1.36       | 1.218 ✓                  |
| bt2015            | 581  | 780      | K–N 301位              | 已暂停                       | 不作承诺    | 等待 `q(d,β)` 标定         |
| hurst1900 标定 | 461 | 1900 | **2000-bit Arb balls** | wrapper 1108s；全 cleanup 2229s | `eta=0.1493` | **No-Go，m800 未启动** |

提示:

- BKZ 每完成一个块大小就有 checkpoint (`work/<stage>_bkz<b>.txt`), 可先用 bkz20/30 的基跑 s04 看趋势。
- 多 seed full search 当前暂停；先完成隔离变量探针。
- s04 中 fpylll CVP 枚举失败会自动回退 Babai+扰动 (已验证路径), 不影响运行。

## 五、判读 s04 输出

- `h_H/A_H` 只是观测；跨 NU 比较必须反解 `B_eff`，不得外推固定 q。
- `harvest`: 轻块+尾部收割, 正常 +0.03–0.10。
- 认证以 s05 的 **h_lo** 为准 (球算术保证下界)。

## 当前沙箱批次（2026-07-26）

| 目标                          | 已完成的 baseline                                                       | 当前长任务                                                                                                        |
| ----------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Kotnik–te Riele 2006 / 1.218 | dim 141; A_H=1.3008; nats=613; L_H_pred=1.3007 (100.0%)                 | **Arb 认证 h_lo=1.3580532527406444**                                                                        |
| Best–Trudgian 2015 / 1.6383  | dim 581; A_H=1.8232; nats=530; L_H_pred=1.6689 (91.5%)                  | BKZ-20 仅 h=1.309021 / 重块效率 71.7%；BKZ-30 的 dpe 路径触发`infinite loop in babai`，已自动切换 MPFR-300 继续 |
| Hurst 2016/2018 / 1.826054    | 20,001 个 2000-bit Arb 零点；m460 NU900→1900 精确 warm lift 与 scorer parity 通过 | wrapper/BKZ-20 `B_eff=280.799/260.594`，`eta=0.1493`；当前算法路线停止，m800 未启动 |

现场记录见 `docs/archive/sandbox_2006_2015_status.md` 和
`docs/archive/hurst1900_postmortem.md`；每完成一个块大小会产生
`work/<stage>_bkz<b>.txt`，它是下一次搜索和断点续跑的依据。

## 六、证书等级 (诚实声明)

s05 输出 = 严格球算术枚举证书: γ 为 arb 严格球, y 精确, cos/求和全程区间。
**发表级**还需: ① 核对 Ingham 定理原文核形式与常数 (本套件用 OtR-1985 核
g(u)=(1−u)cos(πu)+sin(πu)/π); ② alpha/beta 换成独立重算的严格球;
③ 引用 Kim–Nguyễn Zenodo 数据集 (10.5281/zenodo.10775723) 与 Hurst 2018。

## 七、下一战 (改 x_min 上界)

同一管线把权重换成 Pintz/Saouter 有效核 (alpha*=alpha·exp(−3e−9γ²), 见
Evaluation-h.c), 目标改为 |h|>1 且最小化 y, 加 ν_y 约束 — 即 K–N 的
x_min < exp(1.96e19) 战场。柱算法 + 你的 16 核在这里同样适用。
