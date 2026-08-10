# ===== 共享工具: 数据解析 / Ingham 核 / KL 账本 =====
import contextlib
import hashlib
import json
import math
import os
import re
import tempfile

# ---------- 数据解析 ----------
# 重要陷阱: alpha/beta 的小数值行是科学计数法, 指数在 300 字符行的末尾。
# 任何截断解析都会丢指数把 1e-5 读成 1.0 —— 必须整行解析!

def read_lines(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read().splitlines()

def parse_arb_line(s):
    """解析 01 生成的零点行: 'k [mid+/-rad]' 或 'k mid' -> (k, mid_str)"""
    k, rest = s.split(None, 1)
    rest = rest.strip()
    if rest.startswith("["):
        rest = rest[1:-1] if rest.endswith("]") else rest[1:]
        mid = rest.split("+/-")[0]
    else:
        mid = rest
    return int(k), mid

def parse_arb_ball_line(s):
    """保留半径地解析 ``k [mid+/-rad]``。

    返回 ``(k, ball_text)``。认证路径必须把 ``ball_text`` 整体交给
    ``flint.arb``；只有构格的中点路径可以调用 :func:`parse_arb_line`。
    """
    k, rest = s.split(None, 1)
    rest = rest.strip()
    if not (rest.startswith("[") and rest.endswith("]") and "+/-" in rest):
        raise ValueError(f"零点 {k} 不是严格 Arb ball: {rest[:80]!r}")
    # 只允许十进制 Arb 的稳定文本格式，拒绝 NaN/inf 和尾随垃圾。
    if not re.fullmatch(
        r"\[[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"
        r"\+/-[+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?\]",
        rest.replace(" ", ""),
    ):
        raise ValueError(f"零点 {k} 的 Arb ball 格式非法")
    return int(k), rest.replace(" ", "")

def validate_arb_rows(lines, lo, hi, require_ball=True):
    """校验 shard 索引、唯一性和 Arb 文本，返回按索引排列的原始行。"""
    rows = {}
    for raw in lines:
        if not raw.strip():
            continue
        if require_ball:
            k, _ = parse_arb_ball_line(raw)
        else:
            k, _ = parse_arb_line(raw)
        if k in rows:
            raise ValueError(f"重复零点索引 {k}")
        if not lo <= k <= hi:
            raise ValueError(f"零点索引 {k} 不在 [{lo},{hi}]")
        rows[k] = raw.rstrip("\n")
    missing = [k for k in range(lo, hi + 1) if k not in rows]
    if missing:
        raise ValueError(f"缺少 {len(missing)} 个零点，首个为 {missing[0]}")
    return [rows[k] for k in range(lo, hi + 1)]

def load_gamma_strings(cfg, stage):
    """按 stage 选择零点源, 返回前 NEV+1 个 gamma 的十进制字符串列表"""
    import config
    if cfg["zeros"] == "kn":
        Z = read_lines(os.path.join(config.DATA_DIR, "zeroes.txt"))
        return [z.strip() for z in Z[:config.NEV + 1]]
    out = {}
    for line in read_lines(config.ZEROS_ARB):
        k, mid = parse_arb_line(line)
        out[k] = mid
    assert all(k in out for k in range(1, config.NEV + 2)), "zeros_arb 不完整, 先跑 01"
    return [out[k] for k in range(1, config.NEV + 2)]

def zeros_digits(gstrs):
    return min(len(s.split(".")[-1]) for s in gstrs[:100])

# ---------- Ingham 核与权重 ----------
def ingham_kernel(u):
    return (1.0 - u) * math.cos(math.pi * u) + math.sin(math.pi * u) / math.pi

def build_weights(gf, af, NEV):
    """w_k = 2*alpha_k*g(gamma_k/T), T=gamma_{NEV+1};  gf/af 为 float 数组"""
    import numpy as np
    T = gf[NEV]
    u = gf[:NEV] / T
    g = (1 - u) * np.cos(math.pi * u) + np.sin(math.pi * u) / math.pi
    return 2 * af[:NEV] * g, T

# ---------- 大偏差账本 ----------
def logI0(x):
    if x < 1e-10: return x * x / 4
    if x < 30:
        t = 1.0; s = 1.0; k = 0; x2 = x * x / 4
        while True:
            k += 1; t *= x2 / (k * k); s += t
            if t < 1e-16 * s or k > 500: break
        return math.log(s)
    return x - 0.5 * math.log(2 * math.pi * x) + math.log(1 + 1 / (8 * x))

def R1(x):
    if x < 1e-10: return x / 2
    h = 1e-6 * max(1, x)
    return (logI0(x + h) - logI0(x - h)) / (2 * h)

def dKL(x):
    return x * R1(x) - logI0(x)

def tilt_prediction(wH, nats):
    """在 nats 预算下重块的倾斜预测: 返回 (lambda, L_H_pred)"""
    lo, hi = 1e-1, 1e7
    for _ in range(60):
        mid = math.sqrt(lo * hi)
        if sum(dKL(mid * x) for x in wH) < nats: lo = mid
        else: hi = mid
    lam = math.sqrt(lo * hi)
    return lam, float(sum(x * R1(lam * x) for x in wH))

# ---------- fplll 矩阵格式 ----------
def write_fplll_matrix(path, rows):
    with atomic_text_writer(path) as f:
        f.write("[")
        for r in rows:
            f.write("[" + " ".join(str(x) for x in r) + "]\n")
        f.write("]\n")

def read_fplll_matrix(path, dim):
    with open(path, encoding="utf-8") as handle:
        txt = handle.read()
    toks = re.findall(r"-?\d+", txt)
    assert len(toks) == dim * dim, f"期望 {dim*dim} 个整数, 读到 {len(toks)}"
    it = iter(toks)
    return [[int(next(it)) for _ in range(dim)] for _ in range(dim)]

def validate_fplll_matrix(path, dim):
    """只有完整的 dim×dim 整数矩阵才可成为 checkpoint。"""
    try:
        rows = read_fplll_matrix(path, dim)
    except (OSError, AssertionError, ValueError):
        return False
    return len(rows) == dim and all(len(row) == dim for row in rows)

@contextlib.contextmanager
def atomic_text_writer(path, encoding="utf-8"):
    """同目录临时文件 + fsync + replace，避免半写 checkpoint。"""
    path = os.fspath(path)
    directory = os.path.dirname(path) or "."
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{os.path.basename(path)}.", suffix=".tmp",
                               dir=directory, text=True)
    try:
        with os.fdopen(fd, "w", encoding=encoding) as handle:
            yield handle
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    except BaseException:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(tmp)
        raise

def atomic_write_json(path, value):
    with atomic_text_writer(path) as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")

def sha256_file(path, block_size=1 << 20):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(block_size), b""):
            digest.update(block)
    return digest.hexdigest()

def physical_cpu_ids(reserve=2):
    """从 sysfs/lscpu 等价信息选每个物理核的首个逻辑 CPU。"""
    selected = []
    seen = set()
    cpu_root = "/sys/devices/system/cpu"
    for name in sorted(os.listdir(cpu_root), key=lambda s: int(s[3:]) if s[3:].isdigit() else 10**9):
        if not re.fullmatch(r"cpu\d+", name):
            continue
        cpu = int(name[3:])
        topology = os.path.join(cpu_root, name, "topology")
        try:
            with open(os.path.join(topology, "core_id"), encoding="ascii") as handle:
                core = int(handle.read())
            with open(os.path.join(topology, "physical_package_id"),
                      encoding="ascii") as handle:
                package = int(handle.read())
            online_path = os.path.join(cpu_root, name, "online")
            if os.path.exists(online_path):
                with open(online_path, encoding="ascii") as handle:
                    online = handle.read().strip() == "1"
            else:
                online = True
        except OSError:
            continue
        if online and (package, core) not in seen:
            seen.add((package, core))
            selected.append(cpu)
    if not selected:
        selected = list(range(os.cpu_count() or 1))
    keep = max(1, len(selected) - max(0, reserve))
    return selected[:keep]
