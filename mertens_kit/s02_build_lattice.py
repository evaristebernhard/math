#!/usr/bin/env python3
"""步骤 02: 柱算法格构造 (重块投影格 + 目标向量)。"""
import argparse
import sys, os, json, math, time
import numpy as np
import mpmath as mp
import config, util

parser = argparse.ArgumentParser()
parser.add_argument("stage", choices=sorted(config.STAGES))
parser.add_argument("--mH", type=int, help="覆盖重块维度（赛马链使用）")
parser.add_argument("--nu", type=int, help="覆盖嵌入精度（赛马链使用）")
parser.add_argument("--output-prefix", help="不含 _basis.txt/_meta.json 的输出前缀")
args = parser.parse_args()
stage = args.stage
cfg = dict(config.STAGES[stage])
mH = args.mH if args.mH is not None else cfg["mH"]
NU = args.nu if args.nu is not None else cfg["NU"]
NUY, NEV = cfg["NUY"], config.NEV
prefix = args.output_prefix or f"{config.WORK_DIR}/{stage}"
os.makedirs(config.WORK_DIR, exist_ok=True)
t0 = time.time()

# ---- 数据 ----
gstr = util.load_gamma_strings(cfg, stage)                    # NEV+1 个 gamma 字符串
A = util.read_lines(os.path.join(config.DATA_DIR, "alpha.txt"))
Bt = util.read_lines(os.path.join(config.DATA_DIR, "beta.txt"))
gf = np.array([float(s) for s in gstr])
af = np.array([float(s) for s in A[:NEV + 1]])
bf = np.array([float(s) for s in Bt[:NEV + 1]])               # psi 只需 float 精度
w, T = util.build_weights(gf, af, NEV)

# ---- 精度守卫 ----
digs = util.zeros_digits(gstr)
need = NU * math.log10(2) + 10
assert digs >= need, f"零点精度不足: 有 {digs} 位, NU={NU} 需要 {need:.0f} 位 (hurst 阶段请用 zeros=arb)"

# ---- KL 账本选主动集 (= 按核加权振幅取前 mH) + 倾斜预测 ----
order = np.argsort(-w)
H = np.sort(order[:mH])
AH = float(w[H].sum())
nats = (NU - 16) * math.log(2)
lam, LH = util.tilt_prediction([float(w[k]) for k in H], nats)
print(f"[02] stage={stage} mH={mH} NEV={NEV} T={T:.1f}")
print(f"[02] A_H={AH:.4f}  B_full={w.sum():.4f}  nats={nats:.0f}  tilt: lam={lam:.0f} L_H_pred={LH:.4f} ({LH/AH*100:.1f}%)")

# ---- 整数格 (与沙箱验证版逐行一致) ----
mp.mp.dps = int(NU * 0.302) + 40
two = mp.mpf(2)
S  = [mp.sqrt(mp.mpf(float(w[k]))) for k in H]
gH = [mp.mpf(gstr[k]) for k in H]
pH = [mp.mpf(float(bf[k])) for k in H]
def IR(x): return int(mp.floor(x + mp.mpf('0.5')))
n = mH
rows = [[IR(S[j] * gH[j] * two**(NU - NUY)) for j in range(n)] + [1]]
for j in range(n):
    r = [0] * (n + 1); r[j] = IR(S[j] * 2 * mp.pi * two**NU); rows.append(r)
tvec = [IR(S[j] * (pH[j] % (2 * mp.pi)) * two**NU) for j in range(n)] + [0]

util.write_fplll_matrix(f"{prefix}_basis.txt", rows)
util.atomic_write_json(
    f"{prefix}_meta.json",
    dict(stage=stage, mH=mH, NU=NU, NUY=NUY, NEV=NEV, T=T,
         H=[int(k) for k in H], AH=AH, LH_pred=LH,
         tvec=[str(x) for x in tvec]),
)
print(f"[02] wrote {prefix}_basis.txt (dim {n+1}) + {prefix}_meta.json  ({time.time()-t0:.0f}s)")
print(f"[02] 下一步:  bash s03_reduce.sh {stage}")
