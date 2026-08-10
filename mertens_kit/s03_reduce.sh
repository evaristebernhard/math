#!/usr/bin/env bash
# 兼容入口；实现位于可测试的 Python 调度器。
set -euo pipefail
exec "${PYTHON:-python3}" "$(dirname "$0")/s03_reduce.py" "$@"
