"""Connected robust-hosting-capacity admission driver (standard-library only).

This is the *outer cell-cover logic* used by the paper, independent of any
power-flow package. Plug in an oracle that validates nonlinear DistFlow,
Hessian, phasor, and PV capability on a WHOLE (gain, lo, hi) cell.

An oracle's PASS is only as rigorous as its underlying implementation.
A failed cell is UNKNOWN, never a proof of physical insecurity.
"""
from collections import deque
from dataclasses import dataclass
from fractions import Fraction as Q
from typing import Callable, Sequence

@dataclass(frozen=True)
class Cell:
    lo: Q
    hi: Q
    depth: int = 0

@dataclass(frozen=True)
class Certificate:
    passed: bool
    covered: tuple[Cell, ...]
    unresolved: Cell | None
    calls: int

Oracle = Callable[[Sequence[Q], Q, Q], bool]

def cover_prefix(
    gains: Sequence[Q], target: Q, oracle: Oracle, *,
    initial_width: Q = Q(1, 50),
    min_width: Q = Q(1, 4000),
    max_depth: int = 20,
) -> Certificate:
    """PASS iff oracle has passed on gap-free closed cells covering [0,target].

    The exact Fraction endpoints avoid losing coverage due to float rounding.
    The physical credibility of PASS still depends on a *validated oracle*.
    """
    target = Q(target)
    if target < 0 or initial_width <= 0 or min_width <= 0 or max_depth < 0:
        raise ValueError("invalid capacity or refinement controls")
    if target == 0:
        return Certificate(True, (), None, 0)
    todo = deque()
    left = Q(0)
    while left < target:
        right = min(target, left + initial_width)
        todo.append(Cell(left, right))
        left = right
    passed = []
    calls = 0
    while todo:
        cell = todo.popleft()
        calls += 1
        if oracle(gains, cell.lo, cell.hi):
            passed.append(cell)
            continue
        width = cell.hi - cell.lo
        if width <= min_width or cell.depth >= max_depth:
            return Certificate(False, tuple(passed), cell, calls)
        center = (cell.lo + cell.hi) / 2
        todo.appendleft(Cell(center, cell.hi, cell.depth+1))
        todo.appendleft(Cell(cell.lo, center, cell.depth+1))
    passed.sort(key=lambda c: c.lo)
    cursor = Q(0)
    for cell in passed:
        if cell.lo != cursor:
            return Certificate(False, tuple(passed), Cell(cursor,cell.lo), calls)
        cursor = cell.hi
    if cursor != target:
        return Certificate(False, tuple(passed), Cell(cursor,target), calls)
    return Certificate(True, tuple(passed), None, calls)


def choose_tested_gains(
    gains_list: Sequence[Sequence[Q]],
    targets: Sequence[Q],
    oracle: Oracle,
) -> tuple[tuple[Q, ...], Q, Certificate]:
    """Return best PASS among finite tested designs (NOT a global optimum)."""
    best = None
    for gains in gains_list:
        g = tuple(map(Q, gains))
        for target in targets:
            res = cover_prefix(g, Q(target), oracle)
            if res.passed and (best is None or Q(target) > best[1]):
                best = (g, Q(target), res)
    if best is None:
        raise ValueError("no tested candidate achieved PASS")
    return best


def _rational_toy_oracle(gains, a, b):
    """Independent toy: Phi(lambda,w)=(lambda+w)^2 <= (4/5)^2
    for every w in [0,1/10]; exact proof by monotonicity for lambda>=0.
    Gains are intentionally unused in this toy.
    """
    assert a >= 0
    return (b + Q(1,10))**2 <= Q(4,5)**2


def self_test():
    g = (Q(1),)
    assert cover_prefix(g,Q(7,10),_rational_toy_oracle).passed
    r=cover_prefix(g,Q(4,5),_rational_toy_oracle)
    assert not r.passed and r.unresolved is not None
    assert choose_tested_gains([g], [Q(1,2),Q(7,10)],_rational_toy_oracle)[1] == Q(7,10)
    print("Fraction cell-cover / UNKNOWN / gain-selection toy regressions passed.")
    print("This tests the driver, not IEEE33 power-flow safety.")

if __name__ == "__main__":
    self_test()
