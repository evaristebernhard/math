#!/usr/bin/env python3
"""Finite experiments for additive squares versus binary Abelian squares.

For a positive integer gap word g=(g_1,...,g_m), encode
    E(g) = a b^{g_1} a b^{g_2} ... a b^{g_m}.

The program compares strict additive-square factors of g with distinct Abelian
square factors of E(g), and measures the FMMS margin
    theta(E(g)) - (F(|E(g)|_a)+F(|E(g)|_b)),
where F(t)=floor((t+2)/4).

Finite computation is used only for audit/conjecture generation, never as proof.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import product


def F(t: int) -> int:
    return (t + 2) // 4


def encode(g: tuple[int, ...]) -> str:
    return "".join("a" + "b" * x for x in g)


def is_abelian_square(s: str) -> bool:
    if len(s) % 2:
        return False
    h = len(s) // 2
    return Counter(s[:h]) == Counter(s[h:])


def abelian_square_factors(w: str) -> set[str]:
    out: set[str] = set()
    n = len(w)
    for i in range(n):
        for j in range(i + 2, n + 1, 2):
            s = w[i:j]
            if is_abelian_square(s):
                out.add(s)
    return out


def additive_square_factors(g: tuple[int, ...]) -> set[tuple[int, ...]]:
    out: set[tuple[int, ...]] = set()
    n = len(g)
    for i in range(n):
        for k in range(1, (n - i) // 2 + 1):
            if sum(g[i : i + k]) == sum(g[i + k : i + 2 * k]):
                out.add(g[i : i + 2 * k])
    return out


def has_additive_square_suffix(g: tuple[int, ...]) -> bool:
    n = len(g)
    for k in range(1, n // 2 + 1):
        if sum(g[n - 2 * k : n - k]) == sum(g[n - k : n]):
            return True
    return False


def enumerate_additive_square_free(K: int, max_len: int):
    levels: dict[int, list[tuple[int, ...]]] = {0: [()]}
    for n in range(1, max_len + 1):
        cur: list[tuple[int, ...]] = []
        for prefix in levels[n - 1]:
            for x in range(1, K + 1):
                cand = prefix + (x,)
                if not has_additive_square_suffix(cand):
                    cur.append(cand)
        levels[n] = cur
        if not cur:
            break
    return levels


def audit(K: int, max_len: int) -> None:
    levels = enumerate_additive_square_free(K, max_len)
    print(f"alphabet=1..{K}")
    print("len  AS-free  min(theta-Phi)  examples attaining min")
    print("---  -------  --------------  ----------------------")
    for n in range(1, max_len + 1):
        words = levels.get(n, [])
        if not words:
            print(f"{n:>3}  {0:>7}  {'-':>14}  -")
            break
        best = None
        examples: list[tuple[int, ...]] = []
        for g in words:
            w = encode(g)
            theta = len(abelian_square_factors(w))
            phi = F(w.count('a')) + F(w.count('b'))
            margin = theta - phi
            if best is None or margin < best:
                best = margin
                examples = [g]
            elif margin == best and len(examples) < 3:
                examples.append(g)
        print(f"{n:>3}  {len(words):>7}  {best:>14}  {examples}")


def verify_strict_injection(K: int, max_len: int) -> None:
    checked = 0
    for n in range(1, max_len + 1):
        for g0 in product(range(1, K + 1), repeat=n):
            g = tuple(g0)
            bas = abelian_square_factors(encode(g))
            for q in additive_square_factors(g):
                if encode(q) not in bas:
                    raise AssertionError((g, q, encode(q)))
            checked += 1
    print(f"strict-injection audit passed for {checked} words over 1..{K}, length <= {max_len}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--K", type=int, default=3)
    p.add_argument("--max-len", type=int, default=12)
    p.add_argument("--verify-injection", action="store_true")
    args = p.parse_args()
    audit(args.K, args.max_len)
    if args.verify_injection:
        verify_strict_injection(args.K, min(args.max_len, 7))


if __name__ == "__main__":
    main()
