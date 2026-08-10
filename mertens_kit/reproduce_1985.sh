#!/usr/bin/env bash
# 一键复现 1985 Odlyzko–te Riele 阶梯与旧沙箱 1.1215 记录。
set -euo pipefail

PYTHON=${PYTHON:-python3}
mkdir -p work

"$PYTHON" s02_build_lattice.py otr1985 | tee work/otr1985_build.log
bash s03_reduce.sh otr1985 20 | tee work/otr1985_reduce.log
"$PYTHON" s04_search.py otr1985 work/otr1985_bkz20.txt \
  | tee work/otr1985_search.log
"$PYTHON" s05_certify.py otr1985 | tee work/otr1985_certify.log

"$PYTHON" - <<'PY'
import json

cert = json.load(open("work/otr1985_certificate.json"))
h = cert["h_lo"]
assert h > 1.1215, (h, "没有复现旧沙箱 1.1215")
assert h > 1.061545, (h, "没有超越 Odlyzko–te Riele 1985")
print(f"[REPRO] h_lo={h:.16f} > 1.1215 > 1.061545: PASS")
PY
