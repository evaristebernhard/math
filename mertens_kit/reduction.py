"""fplll 子进程、checkpoint 分类与原子提交的共享实现。"""
from __future__ import annotations

import json
import os
import signal
import subprocess
import tempfile
import time
from dataclasses import asdict, dataclass

import util


THREAD_ENV = {
    "OMP_NUM_THREADS": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "BLIS_NUM_THREADS": "1",
    "VECLIB_MAXIMUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1",
}


@dataclass
class RunResult:
    command: list[str]
    returncode: int
    status: str
    accepted: bool
    seconds: float
    peak_rss_kib: int
    output_valid: bool
    stderr_tail: str
    output: str | None = None
    retained_valid_failure: bool = False


def _rss_kib(pid: int) -> int:
    try:
        with open(f"/proc/{pid}/status", encoding="utf-8") as handle:
            for line in handle:
                if line.startswith("VmRSS:"):
                    return int(line.split()[1])
    except OSError:
        pass
    return 0


def _cpu_seconds(pid: int) -> float:
    try:
        fields = open(f"/proc/{pid}/stat", encoding="ascii").read().split()
        ticks = os.sysconf("SC_CLK_TCK")
        return (int(fields[13])+int(fields[14]))/ticks
    except (OSError, ValueError, IndexError):
        return 0.0


def classify_run(returncode: int, stderr: str, output_valid: bool,
                 timed_out: bool = False) -> tuple[str, bool]:
    lower = stderr.lower()
    if timed_out:
        return "timeout", False
    if "infinite loop in babai" in lower:
        return "infinite_loop_in_babai", False
    loop_limit = ("loops limit exceeded" in lower
                  or "loop limit exceeded" in lower
                  or "maximal number of loops" in lower)
    if loop_limit and output_valid:
        return "completed_by_limit", True
    if returncode == 0 and output_valid:
        return "completed", True
    if not output_valid:
        return "truncated_or_invalid_matrix", False
    if returncode < 0:
        return f"crash_signal_{-returncode}", False
    return f"failed_rc_{returncode}", False


def run_fplll(command: list[str], input_path: str, output_path: str, dim: int,
              timeout: float | None = None, cpu: int | None = None,
              metadata: dict | None = None,
              retain_valid_failure: bool = False,
              progress_interval: float | None = None,
              progress_label: str | None = None) -> RunResult:
    """运行一次 fplll；只有已分类为可接受的完整矩阵才原子提交。"""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    fd, temporary = tempfile.mkstemp(
        prefix=f".{os.path.basename(output_path)}.", suffix=".tmp",
        dir=os.path.dirname(output_path) or ".",
    )
    os.close(fd)
    error_path = temporary + ".err"
    env = os.environ.copy()
    env.update(THREAD_ENV)

    def child_setup():
        os.setsid()
        if cpu is not None:
            try:
                os.sched_setaffinity(0, {cpu})
            except (AttributeError, OSError):
                pass

    started = time.monotonic()
    timed_out = False
    peak_rss = 0
    progress_path = output_path+".progress.jsonl"
    progress_handle = None

    def emit_progress(event, pid=None):
        elapsed = time.monotonic()-started
        payload = {
            "event": event, "elapsed_seconds": elapsed,
            "timeout_seconds": timeout,
            "timeout_fraction": elapsed/timeout if timeout else None,
            "peak_rss_kib": peak_rss,
            "stdout_bytes": (
                os.path.getsize(temporary) if os.path.exists(temporary) else 0
            ),
            "stderr_bytes": (
                os.path.getsize(error_path) if os.path.exists(error_path) else 0
            ),
            "cpu_seconds": _cpu_seconds(pid) if pid else None,
        }
        if progress_handle is not None:
            progress_handle.write(json.dumps(payload, sort_keys=True)+"\n")
            progress_handle.flush()
        if progress_interval:
            label = progress_label or os.path.basename(output_path)
            cpu_text = (
                f"{payload['cpu_seconds']:.1f}s"
                if payload["cpu_seconds"] is not None else "n/a"
            )
            budget_text = (
                f"{100*payload['timeout_fraction']:.1f}%"
                if payload["timeout_fraction"] is not None else "unbounded"
            )
            print(
                f"[FPLLL] {label} {event} elapsed={elapsed:.1f}s "
                f"budget={budget_text} cpu={cpu_text} "
                f"rss={peak_rss/1024:.1f}MiB "
                f"stdout={payload['stdout_bytes']}B "
                f"stderr={payload['stderr_bytes']}B",
                flush=True,
            )

    try:
        if progress_interval:
            progress_handle = open(progress_path, "a", encoding="utf-8")
            emit_progress("started")
        with open(input_path, "rb") as source, open(temporary, "wb") as sink, \
                open(error_path, "wb") as errors:
            process = subprocess.Popen(
                command,
                stdin=source,
                stdout=sink,
                stderr=errors,
                env=env,
                preexec_fn=child_setup,
            )
            next_progress = time.monotonic()+(progress_interval or 10**30)
            while process.poll() is None:
                peak_rss = max(peak_rss, _rss_kib(process.pid))
                if progress_interval and time.monotonic() >= next_progress:
                    emit_progress("running", process.pid)
                    next_progress = time.monotonic()+progress_interval
                if timeout and time.monotonic() - started > timeout:
                    timed_out = True
                    os.killpg(process.pid, signal.SIGTERM)
                    try:
                        process.wait(5)
                    except subprocess.TimeoutExpired:
                        os.killpg(process.pid, signal.SIGKILL)
                time.sleep(0.05)
            returncode = process.returncode
        with open(error_path, encoding="utf-8", errors="replace") as handle:
            stderr = handle.read()
        output_valid = util.validate_fplll_matrix(temporary, dim)
        status, accepted = classify_run(returncode, stderr, output_valid, timed_out)
        retained = bool(
            not accepted and retain_valid_failure and output_valid
        )
        if accepted or retained:
            os.replace(temporary, output_path)
            committed = output_path
        else:
            os.unlink(temporary)
            committed = None
        result = RunResult(
            command=command,
            returncode=returncode,
            status=status,
            accepted=accepted,
            seconds=time.monotonic() - started,
            peak_rss_kib=peak_rss,
            output_valid=output_valid,
            stderr_tail=stderr[-4000:],
            output=committed,
            retained_valid_failure=retained,
        )
        sidecar = output_path + ".run.json"
        payload = asdict(result)
        if metadata:
            payload["metadata"] = metadata
        util.atomic_write_json(sidecar, payload)
        emit_progress("completed")
        return result
    finally:
        if progress_handle is not None:
            progress_handle.close()
        for path in (temporary, error_path):
            try:
                os.unlink(path)
            except FileNotFoundError:
                pass


def mpfr_decode_check(path: str, dim: int, target=None, bits: int = 384) -> dict:
    """解析矩阵并用 MPFR GSO/Babai 做后端输出的独立有效性检查。"""
    try:
        from fpylll import FPLLL, GSO, IntegerMatrix

        rows = util.read_fplll_matrix(path, dim)
        FPLLL.set_precision(bits)
        matrix = IntegerMatrix.from_matrix(rows)
        gso = GSO.Mat(matrix, float_type="mpfr")
        ok = bool(gso.update_gso())
        decoded = None
        if target is not None:
            decoded = [int(x) for x in gso.babai(tuple(int(x) for x in target))]
            ok = ok and len(decoded) == dim
        return {"available": True, "valid": ok, "coefficients": decoded}
    except Exception as exc:
        return {"available": False, "valid": False,
                "error": f"{type(exc).__name__}: {exc}"}
