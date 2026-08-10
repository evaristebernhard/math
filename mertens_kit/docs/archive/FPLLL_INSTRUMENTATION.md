# fplll LLL instrumentation

## Current status

`[PARITY UNVERIFIED]`：补丁已经按 Ubuntu Noble fplll 5.4.5 源码准备，
但尚未完成私有 binary 的编译、基准对照和 instrumented 运行。下面描述的
是预期接口，不是已经取得的运行时内层计数。只重新编译而未设置
`FPLLL_INSTRUMENT`，也不会比现有 watchdog 多出进度信息。

The installed `/usr/bin/fplll` is Ubuntu Noble `5.4.5`.  The patch pair
`fplll_lll_instrumentation.h.patch` and
`fplll_lll_instrumentation.cpp.patch` targets that exact source version.
It instruments the actual `LLLReduction` implementation, not the Python
watchdog:

- outer LLL `iteration`
- Lovasz `swap_count`
- `babai_count`
- `gso_refresh_count`
- non-zero Babai `size_reduction_count`
- `kappa` and `elapsed`

The counters are disabled unless `FPLLL_INSTRUMENT` is set.  The report
interval is controlled by `FPLLL_INSTRUMENT_INTERVAL` (default `1000`).
Reports are emitted on `stderr`, so the existing campaign sidecars preserve
them in `stderr_tail` and the Python heartbeat continues to report CPU/RSS.

Build with `build_fplll_instrumented.sh` after unpacking the matching 5.4.5
source and providing autotools.  Do not replace the system binary; prepend the
private prefix to `PATH` only for the diagnostic run.
