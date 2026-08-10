#!/usr/bin/env bash
# 一键复现 Kotnik–te Riele 2006 的 1.218 阶梯。
set -euo pipefail

PYTHON=${PYTHON:-python3}
mkdir -p work

"$PYTHON" s02_build_lattice.py validate | tee work/validate_build.log
bash s03_reduce.sh validate 20 | tee work/validate_reduce.log
"$PYTHON" s04_search.py validate work/validate_bkz20.txt \
  | tee work/validate_search.log
"$PYTHON" s05_certify.py validate | tee work/validate_certify.log

"$PYTHON" - <<'PY'
import json

result = json.load(open("work/validate_results.json"))
cert = json.load(open("work/validate_certificate.json"))
assert result["y_exact_num"] == cert["y_exact_num"]
assert result["NUY"] == cert["NUY"]
assert abs(result["h"] - cert["h_lo"]) < 1e-12
assert cert["h_lo"] > 1.218
print(f"[REPRO] h_lo={cert['h_lo']:.16f} > 1.218: PASS")
PY
