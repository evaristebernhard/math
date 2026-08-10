from itertools import combinations
from math import floor


def abelian_squares(w: str):
    out = set()
    n = len(w)
    for i in range(n):
        for j in range(i + 2, n + 1, 2):
            u = w[i:j]
            h = len(u) // 2
            if u[:h].count('a') == u[h:].count('a'):
                out.add(u)
    return out


def theta(w: str):
    return len(abelian_squares(w))


def words_with_x_a(n, x):
    for pos in combinations(range(n), x):
        s = ['b'] * n
        for p in pos:
            s[p] = 'a'
        yield ''.join(s)


def M_bruteforce(x, n):
    vals = [(theta(w), w) for w in words_with_x_a(n, x)]
    m = min(v for v, _ in vals)
    return m, {w for v, w in vals if v == m}


def rev_closure(bases):
    out = set()
    for w in bases:
        out.add(w)
        out.add(w[::-1])
    return out


def x4_expected(n):
    if n < 8:
        return None
    r = n % 4
    if r == 0:
        k = n // 4
        bases = ['a' + 'b'*(2*k-1) + 'a'*3 + 'b'*(2*k-3)]
    elif r == 1:
        k = (n-1)//4
        bases = ['a' + 'b'*(2*k-1) + 'a'*3 + 'b'*(2*k-2)]
    elif r == 2:
        k = (n-2)//4
        bases = [
            'a' + 'b'*(2*k-1) + 'a'*3 + 'b'*(2*k-1),
            'a' + 'b'*(2*k+1) + 'a'*3 + 'b'*(2*k-3),
            'b' + 'a' + 'b'*(2*k-1) + 'a'*3 + 'b'*(2*k-2),
            'b'*2 + 'a' + 'b'*(2*k-1) + 'a'*3 + 'b'*(2*k-3),
        ]
    else:
        k = (n-3)//4
        bases = [
            'a' + 'b'*(2*k+1) + 'a'*3 + 'b'*(2*k-2),
            'b'*2 + 'a' + 'b'*(2*k-1) + 'a'*3 + 'b'*(2*k-2),
        ]
    return rev_closure(bases)


def x5_expected(n):
    if n == 5:
        return {'a'*5}
    r = n % 4
    if r == 0:
        k = n//4
        bases = ['a'*2 + 'b'*(2*k-1) + 'a'*3 + 'b'*(2*k-4)]
    elif r == 1:
        k = (n-1)//4
        bases = ['a'*2 + 'b'*(2*k-1) + 'a'*3 + 'b'*(2*k-3)]
    elif r == 2:
        k = (n-2)//4
        bases = ['a'*2 + 'b'*(2*k-1) + 'a'*3 + 'b'*(2*k-2)]
    else:
        k = (n-3)//4
        bases = [
            'a'*2 + 'b'*(2*k-1) + 'a'*3 + 'b'*(2*k-1),
            'b'*(2*k-1) + 'a'*5 + 'b'*(2*k-1),
        ]
        if 2*k-3 >= 0:
            bases.append('a'*2 + 'b'*(2*k+1) + 'a'*3 + 'b'*(2*k-3))
    return rev_closure(bases)


def x4_count_formula(s, q, t):
    B = max(s, q, t)
    u = min(s, q)
    if q == 0:
        A = 0
    elif q % 2:
        A = floor((u+1)/2)
    else:
        A = floor(u/2) + 1
    C = 0 if t < q else min(s, t-q) + 1
    return 1 + floor(B/2) + A + C


def cq(u, q):
    return sum(1 for x in range(u+1) if x % 2 == q % 2)


def x5_count_formula(s, q, t):
    assert q >= 1
    M = max(s, q, t)
    u = min(s, q)
    return floor(M/2) + u + 1 + (q % 2 == 0) + cq(u, q) + (t >= q)


def x5_14_count_formula(s, q, t):
    assert q >= 1
    M = max(s, q, t)
    u = min(s, q)
    A = cq(u, q)
    return floor(M/2) + min(q, t) + A + 2


def test_main_values_and_extremizers():
    for n in range(8, 23):
        m4, e4 = M_bruteforce(4, n)
        assert m4 == 1 + floor((n-2)/4), (n, m4)
        assert e4 == x4_expected(n), (n, e4 ^ x4_expected(n))
    for n in range(6, 23):
        m5, e5 = M_bruteforce(5, n)
        assert m5 == floor((n+1)/4), (n, m5)
        assert e5 == x5_expected(n), (n, e5 ^ x5_expected(n))


def test_x4_exact_count_formula():
    for s in range(7):
        for q in range(7):
            for t in range(7):
                w = 'b'*s + 'a' + 'b'*q + 'a'*3 + 'b'*t
                assert theta(w) == x4_count_formula(s, q, t), (s, q, t, theta(w), x4_count_formula(s,q,t), abelian_squares(w))


def test_x5_23_exact_count_formula():
    for s in range(7):
        for q in range(1, 7):
            for t in range(7):
                w = 'b'*s + 'a'*2 + 'b'*q + 'a'*3 + 'b'*t
                assert theta(w) == x5_count_formula(s, q, t), (s, q, t, theta(w), x5_count_formula(s,q,t), abelian_squares(w))


def test_x5_14_exact_count_formula_and_nonextremality():
    for s in range(7):
        for q in range(1, 7):
            for t in range(7):
                w = 'b'*s + 'a' + 'b'*q + 'a'*4 + 'b'*t
                assert theta(w) == x5_14_count_formula(s, q, t), (s, q, t, theta(w), x5_14_count_formula(s,q,t), abelian_squares(w))
                target = floor((len(w)+1)/4)
                assert theta(w) >= target + 1, (s, q, t, w, theta(w), target)


def test_x5_run_rigidity_finite_audit():
    for n in range(7, 23):
        target = floor((n+1)/4)
        for w in words_with_x_a(n, 5):
            runs = sum(1 for i,c in enumerate(w) if c == 'a' and (i == 0 or w[i-1] != 'a'))
            if runs >= 3:
                assert theta(w) >= target + 1, (n, w, theta(w), target)


def test_x4_central_concentration_finite_audit():
    for n in range(8, 23):
        target = 1 + floor((n-2)/4)
        for w in words_with_x_a(n, 4):
            if theta(w) == target:
                assert 'aaa' in w, (n, w)


def word_from_gaps(gaps):
    return 'b' * gaps[0] + ''.join('a' + 'b' * gaps[i + 1] for i in range(len(gaps) - 1))


def a_run_count(w):
    return sum(c == 'a' and (i == 0 or w[i - 1] != 'a') for i, c in enumerate(w))


def test_wing_escape_and_unique_exception():
    from itertools import product
    failures = []
    for x in (4, 5):
        for gaps in product(range(6), repeat=x + 1):
            w = word_from_gaps(gaps)
            if a_run_count(w) < 3:
                continue
            P = 'b' * gaps[0] + 'a' + 'b' * gaps[1] + 'a' + 'b' * gaps[2]
            escaped = abelian_squares(w) - abelian_squares(P)
            assert escaped, (w, P, gaps)
            two_a_minimum = theta(P) == floor((len(P) - 2) / 2)
            if two_a_minimum and len(escaped) < 2:
                failures.append((w, P, escaped))
    assert failures == [('abababa', 'abab', {'baba'})], failures


def expected_x4_triples(N):
    r, rho = divmod(N, 4)
    if rho == 0:
        return {(0, 2*r + 1, 2*r - 1)}
    if rho == 1:
        return {(0, 2*r + 1, 2*r)}
    if rho == 2:
        return {
            (0, 2*r + 1, 2*r + 1),
            (0, 2*r + 3, 2*r - 1),
            (1, 2*r + 1, 2*r),
            (2, 2*r + 1, 2*r - 1),
        }
    return {(0, 2*r + 3, 2*r), (2, 2*r + 1, 2*r)}


def expected_x5_23_triples(N):
    r, rho = divmod(N, 4)
    if rho == 0:
        return {(0, 2*r + 1, 2*r - 1)}
    if rho == 1:
        return {(0, 2*r + 1, 2*r)}
    if rho == 2:
        out = {(0, 2*r + 1, 2*r + 1)}
        if r >= 1:
            out.add((0, 2*r + 3, 2*r - 1))
        return out
    return {(0, 2*r + 3, 2*r)}


def test_integer_optimisations_to_100():
    for N in range(4, 101):
        target = 1 + floor((N + 2) / 4)
        equality = {
            (s, q, N - s - q)
            for s in range(N + 1)
            for q in range(N - s + 1)
            if x4_count_formula(s, q, N - s - q) == target
        }
        assert equality == expected_x4_triples(N), (N, equality ^ expected_x4_triples(N))

    for N in range(1, 101):
        target = floor((N + 6) / 4)
        equality = {
            (s, q, N - s - q)
            for s in range(N + 1)
            for q in range(1, N - s + 1)
            if x5_count_formula(s, q, N - s - q) == target
        }
        assert equality == expected_x5_23_triples(N), (N, equality ^ expected_x5_23_triples(N))


def two_a_count_formula(i, j, k):
    points = sum(
        1
        for x in range(i + 1)
        for z in range(k + 1)
        if abs(x - z) <= j and (x + z - j) % 2 == 0
    )
    return floor(max(i, j, k) / 2) + points


def test_near_extremal_odd_wing():
    for i in range(1, 25):
        for j in range(25):
            for k in range(1, 25):
                total = i + j + k
                if total % 2 == 0:
                    continue
                q = (total - 1) // 2
                if two_a_count_formula(i, j, k) <= q + 1:
                    assert (i, j, k) == (1, 2*q - 1, 1), (i, j, k, q)


def test_balancing_lemma_small_gaps():
    from itertools import product
    for gaps in product(range(5), repeat=6):
        if sum(gaps[:3]) != sum(gaps[3:]):
            continue
        w = word_from_gaps(gaps)
        assert any(u.count('a') == 4 for u in abelian_squares(w)), (gaps, w)


def positive_gap_word(gaps):
    return ''.join('a' + 'b' * g for g in gaps)


def F_fixed(t):
    return floor((t + 2) / 4)


def test_weakly_monotone_gap_theorem_finite_audit():
    from itertools import combinations_with_replacement
    for m in range(1, 8):
        for inc in combinations_with_replacement(range(1, 5), m):
            for gaps in (inc, tuple(reversed(inc))):
                w = positive_gap_word(gaps)
                assert theta(w) >= floor(len(w) / 2) - 1, (gaps, theta(w), len(w))
                if m >= 3:
                    target = F_fixed(m) + F_fixed(sum(gaps))
                    assert theta(w) >= target, (gaps, theta(w), target)


def window_has_square_by_occurrence(gaps, start, k):
    w = positive_gap_word(gaps)
    apos = [i for i, c in enumerate(w) if c == 'a']
    left = 0 if start == 0 else apos[start - 1] + 1
    right = len(w) if start + 2 * k == len(apos) else apos[start + 2 * k]
    first_a = apos[start]
    last_a = apos[start + 2 * k - 1]
    for s in range(left, first_a + 1):
        for e in range(last_a + 1, right + 1):
            u = w[s:e]
            if len(u) % 2:
                continue
            h = len(u) // 2
            if u[:h].count('a') == k and u[h:].count('a') == k:
                return True
    return False


def test_positive_gap_rank_window_criterion_small():
    from itertools import product
    for m in range(2, 7):
        for gaps in product(range(1, 4), repeat=m):
            for k in range(1, m // 2 + 1):
                for start in range(0, m - 2 * k + 1):
                    p = 0 if start == 0 else gaps[start - 1]
                    c = gaps[start + k - 1]
                    q = gaps[start + 2 * k - 1]
                    delta = sum(gaps[start:start + k]) - sum(gaps[start + k:start + 2 * k])
                    predicted = -(p + q) <= delta <= 2 * c
                    actual = window_has_square_by_occurrence(gaps, start, k)
                    assert actual == predicted, (gaps, start, k, delta, p, c, q, actual, predicted)


def test_periodic_block_count_small():
    for h in range(1, 8):
        C = ((h + 1) * (h + 1) + 1) // 2
        B = floor(h / 2) + 1
        for L in range(1, 9):
            w = ('a' + 'b' * h) * L
            mixed = {u for u in abelian_squares(w) if 'a' in u}
            lower = C * floor((L - 1) / 2) + (B if L % 2 == 0 else 0)
            assert len(mixed) >= lower, (h, L, len(mixed), lower)


def test_rank_two_free_compensation_finite_audit():
    # Exhaust small positive-gap words and then test genuinely superadditive
    # descending/ascending families where rank two is absent for structural reasons.
    from itertools import product

    for m in range(4, 7):
        for gaps in product(range(1, 5), repeat=m):
            w = positive_gap_word(gaps)
            if any(u.count('a') == 4 for u in abelian_squares(w)):
                continue
            target = F_fixed(m) + F_fixed(sum(gaps))
            assert theta(w) >= target, (gaps, theta(w), target)

    for m in range(6, 10):
        for tail in ((1, 1, 1), (1, 2, 1), (2, 1, 3)):
            desc = [0] * m
            desc[-3:] = tail
            for i in range(m - 4, -1, -1):
                desc[i] = desc[i + 1] + desc[i + 2] + desc[i + 3] + 1
            w = positive_gap_word(tuple(desc))
            assert not any(u.count('a') == 4 for u in abelian_squares(w)), tuple(desc)
            assert theta(w) >= F_fixed(m) + F_fixed(sum(desc)), tuple(desc)

        for first in ((1, 1), (1, 2), (2, 1)):
            for last in (1, 3, 10):
                asc = [0] * m
                asc[0], asc[1] = first
                for i in range(0, m - 3):
                    left = 0 if i == 0 else asc[i - 1]
                    asc[i + 2] = left + asc[i] + asc[i + 1] + 1
                asc[-1] = last
                w = positive_gap_word(tuple(asc))
                assert not any(u.count('a') == 4 for u in abelian_squares(w)), tuple(asc)
                assert theta(w) >= F_fixed(m) + F_fixed(sum(asc)), tuple(asc)


if __name__ == '__main__':
    tests = [
        test_main_values_and_extremizers,
        test_x4_exact_count_formula,
        test_x5_23_exact_count_formula,
        test_x5_14_exact_count_formula_and_nonextremality,
        test_x5_run_rigidity_finite_audit,
        test_x4_central_concentration_finite_audit,
        test_wing_escape_and_unique_exception,
        test_integer_optimisations_to_100,
        test_near_extremal_odd_wing,
        test_balancing_lemma_small_gaps,
        test_positive_gap_rank_window_criterion_small,
        test_periodic_block_count_small,
        test_weakly_monotone_gap_theorem_finite_audit,
        test_rank_two_free_compensation_finite_audit,
    ]
    for fn in tests:
        fn()
        print(f'PASS {fn.__name__}')
