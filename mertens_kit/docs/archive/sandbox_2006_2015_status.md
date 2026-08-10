# 沙箱批次状态（更新至 2026-07-27）

启动时间：2026-07-26（Asia/Shanghai）

## Kotnik–te Riele 2006

- stage: `validate`
- historical target: `1.218`
- internal acceptance target: `1.30`
- basis: dim `141`, `mH=140`, `NU=900`
- baseline:
  - `A_H=1.3008`
  - `B_full=2.7307`
  - `nats=613`
  - `lambda=486735`
  - `L_H_pred=1.3007 (100.0%)`
- runtime observation:
  - LLL + BKZ-20 completed
  - search `h=1.358053`
  - `h_H=1.2961 / A_H=1.3008 = 99.6%`
  - harvest `+0.0619`
  - exceeds both `1.218` and internal acceptance threshold `1.30`
  - Arb certification completed in `626s`
  - certified enclosure:
    `h(y,T) in [1.358053253, 1.358053253]`
  - certificate lower bound: `1.3580532527406444`
  - `[PARITY VERIFIED]` against the independent 360-dps recomputation

## Best–Trudgian 2015

- stage: `bt2015`
- target: `1.6383`
- basis: dim `581`, `mH=580`, `NU=780`
- baseline:
  - `T=18047.1`
  - `A_H=1.8232`
  - `B_full=2.7307`
  - `nats=530`
  - `lambda=2138`
  - `L_H_pred=1.6689 (91.5%)`
- runtime observation:
  - basis built successfully
  - LLL completed
  - BKZ-20 completed
  - BKZ-20 checkpoint search:
    - `h=1.309021`
    - `h_H=1.3069 / A_H=1.8232 = 71.7%`
    - harvest `+0.0021`
    - target `1.6383`: not reached
  - `[PARITY BROKEN]` relative to the predicted heavy efficiency `91.5%`;
    this checkpoint is not sufficient evidence for the 2015 record
  - BKZ-30 的 dpe 路径触发 `infinite loop in babai`，MPFR fallback 后完成
  - BKZ-40 也已产生完整 checkpoint；当前没有活动的 fplll 进程
  - 三个 checkpoint 的联合搜索最好为 `h=1.3360130419583878`
    (`h_H=1.3245658920614527`)，仍未达到 `1.6383`
- checkpoints: `work/bt2015_bkz20.txt`, `...bkz30.txt`, `...bkz40.txt`

## Hurst 2016 preprint / 2018 publication：NU1900 follow-up

- stage: `hurst`
- target: `1.826054`
- zero source: `work/zeros_arb.txt`
- zero production:
  - `20,001` zeros
  - `2000` bits
  - `49` chunks / `12` processes
  - completed in `215s`
  - K–N `gamma_1` self-check: `OK`
- 旧快照：
  - dim `901`, `mH=900`, `NU=1300` basis 已构建，但约化停止；
  - 该静态理想预测不能用于声称 NU1900 会达到目标。
- 2026-07-27 标定：
  - 采用 `mH=460`, `NU=1900`，从相同 active set 的 NU900 LLL 精确提升；
  - `det(U)=1`，全部精确除法余数和重构差异均为零；
  - warm wrapper LLL 在 `1107.531s` 完成，完整 cleanup 为 `2228.923s`；
  - wrapper: `h_H=1.4790917535`, `B_eff=280.799`, `rho=8.373`;
  - BKZ-20: `h_H=1.4582371410`, `B_eff=260.594`, `rho=8.706`;
  - 两个 checkpoint 的 MPFR-384 Babai 与 100/160 位 scorer parity
    均为 `[PARITY VERIFIED]`；
  - BKZ-20 口径 `eta=0.149276 < 0.90`，campaign 正确停止，
    m800 未构建/未约化。
- 当前判断：
  - `[PARITY BROKEN]` 的是旧性能模型，不是 lattice lift 或 scorer；
  - 单核 12 小时、固定-beta 单-tour + 单 Babai 路线为 No-Go；
  - 不再建议直接运行旧的 `hurst` cold LLL/BKZ 命令。
- 审计：
  - `work/probes/hurst1900_warm_seed20260726/campaign.json`
  - `docs/archive/hurst1900_postmortem.md`

## Search after checkpoint

```bash
python3 s04_search.py bt2015 work/bt2015_bkz20.txt
```

Only run `s05_certify.py` after a search candidate exceeds its target.
