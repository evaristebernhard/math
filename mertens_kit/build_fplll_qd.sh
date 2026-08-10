#!/usr/bin/env bash
# 后台可选构建：只安装到 workspace/.opt，不替换系统 fplll。
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
SRC="$ROOT/.build"
PREFIX="$ROOT/.opt/fplll-qd"
JOBS="${MERTENS_BUILD_JOBS:-2}"
mkdir -p "$SRC" "$PREFIX"

if [[ ! -x "$PREFIX/qd/bin/qd-config" ]]; then
  [[ -d "$SRC/qd/.git" ]] || git clone --depth 1 https://github.com/scibuilder/QD.git "$SRC/qd"
  cd "$SRC/qd"
  ./autogen.sh
  ./configure --prefix="$PREFIX/qd" --enable-shared=yes
  make -j"$JOBS"
  make install
fi

if [[ ! -d "$SRC/fplll/.git" ]]; then
  git clone --depth 1 https://github.com/fplll/fplll.git "$SRC/fplll"
fi
cd "$SRC/fplll"
./autogen.sh
PKG_CONFIG_PATH="$PREFIX/qd/lib/pkgconfig:${PKG_CONFIG_PATH:-}" \
CPPFLAGS="-I$PREFIX/qd/include ${CPPFLAGS:-}" \
LDFLAGS="-L$PREFIX/qd/lib -Wl,-rpath,$PREFIX/qd/lib ${LDFLAGS:-}" \
  ./configure --prefix="$PREFIX"
make -j"$JOBS"
make install
"$PREFIX/bin/fplll" --version
