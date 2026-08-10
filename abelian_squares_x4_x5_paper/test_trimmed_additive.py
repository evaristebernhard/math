from itertools import product

from research_trimmed_additive import (
    F,
    abelian_square_factors,
    additive_square_factors,
    encode,
    enumerate_additive_square_free,
)


def test_strict_additive_square_maps_to_binary_abelian_square():
    checked = 0
    for n in range(1, 8):
        for g in product(range(1, 4), repeat=n):
            g = tuple(g)
            bas = abelian_square_factors(encode(g))
            for q in additive_square_factors(g):
                assert encode(q) in bas
            checked += 1
    print(f"strict-injection audit passed for {checked} gap words over {{1,2,3}}, length <= 7")


def test_additive_square_free_fmms_margins():
    levels = enumerate_additive_square_free(3, 12)
    print("\nlen  AS-free  min(theta-Phi)  examples")
    for n in range(1, 13):
        words = levels.get(n, [])
        if not words:
            print(f"{n:>3}  {0:>7}  -  -")
            break
        best = None
        examples = []
        for g in words:
            w = encode(g)
            theta = len(abelian_square_factors(w))
            phi = F(len(g)) + F(sum(g))
            margin = theta - phi
            if best is None or margin < best:
                best = margin
                examples = [g]
            elif margin == best and len(examples) < 4:
                examples.append(g)
        print(f"{n:>3}  {len(words):>7}  {best:>14}  {examples}")
        assert best is not None
