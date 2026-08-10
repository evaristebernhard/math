#!/usr/bin/env bash
# Build fplll 5.4.5 with LLL/Babai/GSO counters on a private prefix.
# Set FPLLL_SRC to an unpacked 5.4.5 source tree before running.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
SRC="${FPLLL_SRC:-$ROOT/.build/fplll-5.4.5}"
PREFIX="${FPLLL_PREFIX:-$ROOT/.opt/fplll-instrumented}"
PATCH_DIR="$ROOT/.build/fplll-instrumentation"
mkdir -p "$PATCH_DIR"
if [[ ! -f "$SRC/fplll/lll.cpp" || ! -f "$SRC/fplll/lll.h" ]]; then
  echo "FPLLL_SRC must point to an unpacked fplll 5.4.5 source tree" >&2
  exit 2
fi
rm -rf "$PATCH_DIR/source"
mkdir -p "$PATCH_DIR/source"
cp -a "$SRC/." "$PATCH_DIR/source/"
patch -d "$PATCH_DIR/source" -p1 < "$ROOT/fplll_lll_instrumentation.h.patch"
patch -d "$PATCH_DIR/source" -p1 < "$ROOT/fplll_lll_instrumentation.cpp.patch"
cd "$PATCH_DIR/source"
if [[ ! -x ./configure ]]; then
  ./autogen.sh
fi
./configure --prefix="$PREFIX" --disable-shared --enable-static
make -j"${MERTENS_BUILD_JOBS:-2}"
make install
"$PREFIX/bin/fplll" --version
