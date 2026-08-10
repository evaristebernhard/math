# ===== Mertens 柱算法攻击套件 · 配置 =====
# 数据目录: 放 Kim-Nguyen Zenodo 包 (record 10775723) 的三个数据文件
DATA_DIR  = "data"     # data/zeroes.txt  data/alpha.txt  data/beta.txt
WORK_DIR  = "work"
ZEROS_ARB = "work/zeros_arb.txt"   # 01 生成的高精度零点

NEV = 20000            # 评估集大小 (Ingham 核 T = gamma_{NEV+1})
ARB_PREC_BITS = 2000   # 01 零点精度 (~602 十进制位; 支撑 y <= 1e590)
NPROC = 14             # 默认使用 14 个物理核，保留 2 核给系统

# 三个作战阶段
#  mH: 重块(进格)零点数   NU: 嵌入精度(比特, 决定 y 量级与对齐深度)
#  zeros: "kn"=用 Zenodo 301位零点 | "arb"=用 01 生成的 600 位零点
#  beta_list: 渐进 BKZ 块大小序列   target: 要超越的纪录
STAGES = {
  "otr1985": dict(mH=80,  NU=400,  NUY=8, beta_list=[20],
                   target=1.061545, zeros="kn",
                   note="复现 1985 Odlyzko-te Riele 阶梯与沙箱 1.1215 记录"),
  "validate": dict(mH=140, NU=900,  NUY=8, beta_list=[20],
                   target=1.30,     zeros="kn",
                   note="复现 KtR-2006 阶梯; 2026-07-26 Arb 认证 1.358053, 旧沙箱浮点 1.3624"),
  "bt2015":   dict(mH=580, NU=780,  NUY=8, beta_list=[20,30,40],
                   target=1.6383,   zeros="kn",
                   note="超越 Best-Trudgian 2015; BKZ 数小时"),
  "hurst":    dict(mH=900, NU=1300, NUY=8, beta_list=[20,30,40],
                   target=1.826054, zeros="arb",
                   note="冲击 Hurst 2016 预印本/2018 发表纪录; 必须用 600 位零点; BKZ 6-48h+"),
}

# s03 的默认吞吐赛马。每条链独占一个物理核，并从独立的行排列 + LLL
# 开始；tuple 为 (mH, NU, 条数)。seed 由 s03 确定性派生。
RACE_PROFILES = {
  "bt2015": [(580, 780, 2), (580, 900, 3), (580, 950, 3),
             (620, 900, 2), (620, 950, 2),
             (650, 900, 1), (650, 950, 1)],
}

# 搜索参数
N_BASES   = 2000    # Babai 扰动基点数
TOP_BASES = 40      # 进入 AP 扫描的基点数
N_MID     = 3000    # 中层评分零点数
AP_J      = 120     # AP 扫描半径 j in [-AP_J, AP_J]
N_DELTA   = 5       # 使用最短 Y-向量条数
FINALISTS = 200     # full 模式全维精算候选数

# s04 模式预算。full 至少检查四百万个二维 AP 网格点。
SEARCH_MODES = {
  "anchor": dict(n_bases=600, top_bases=20, ap_j=0, ap2_seeds=0,
                 finalists=10, min_ap_evals=0),
  "pilot":  dict(n_bases=2500, top_bases=60, ap_j=160, ap2_seeds=80,
                 finalists=40, min_ap_evals=500_000),
  "full":   dict(n_bases=6000, top_bases=100, ap_j=400, ap2_seeds=220,
                 finalists=200, min_ap_evals=4_000_000),
}
