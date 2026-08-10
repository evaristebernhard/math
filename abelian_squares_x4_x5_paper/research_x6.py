from itertools import combinations
from collections import Counter, defaultdict
from math import floor
import argparse


def abelian_squares(w: str):
    n = len(w)
    pa = [0] * (n + 1)
    for i, ch in enumerate(w):
        pa[i + 1] = pa[i] + (ch == 'a')
    out = set()
    for i in range(n):
        for j in range(i + 2, n + 1, 2):
            h = (j - i) // 2
            if pa[i + h] - pa[i] == pa[j] - pa[i + h]:
                out.add(w[i:j])
    return out


def theta(w: str):
    return len(abelian_squares(w))


def words_with_x_a(n, x=6):
    for pos in combinations(range(n), x):
        s = ['b'] * n
        for p in pos:
            s[p] = 'a'
        yield ''.join(s)


def a_run_composition(w: str):
    runs = []
    i = 0
    n = len(w)
    while i < n:
        if w[i] != 'a':
            i += 1
            continue
        j = i
        while j < n and w[j] == 'a':
            j += 1
        runs.append(j - i)
        i = j
    return tuple(runs)


def b_gap_vector(w: str):
    pos = [i for i, c in enumerate(w) if c == 'a']
    if not pos:
        return (len(w),)
    gaps = [pos[0]]
    for x, y in zip(pos, pos[1:]):
        gaps.append(y - x - 1)
    gaps.append(len(w) - 1 - pos[-1])
    return tuple(gaps)


def canonical_reversal(w: str):
    return min(w, w[::-1])


def fmt_word(w: str):
    # compact run-length display
    out = []
    i = 0
    while i < len(w):
        j = i + 1
        while j < len(w) and w[j] == w[i]:
            j += 1
        r = j - i
        out.append(w[i] if r == 1 else f"{w[i]}^{r}")
        i = j
    return ''.join(out)


def phi6(n):
    return 2 + floor((n - 4) / 4)


def audit_n(n, near=1):
    best = None
    by_value = defaultdict(list)
    for w in words_with_x_a(n, 6):
        t = theta(w)
        if best is None or t < best:
            best = t
            by_value = defaultdict(list)
            by_value[t].append(w)
        elif t <= best + near:
            by_value[t].append(w)
        # if the minimum improved, older near-minimal buckets are irrelevant
        if best is not None:
            for k in list(by_value):
                if k > best + near:
                    del by_value[k]
    ex = by_value[best]
    reps = sorted({canonical_reversal(w) for w in ex})
    run_dist = Counter(len(a_run_composition(w)) for w in ex)
    comp_dist = Counter(a_run_composition(w) for w in ex)
    return best, ex, reps, run_dist, comp_dist, by_value


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--min-n', type=int, default=6)
    ap.add_argument('--max-n', type=int, default=22)
    ap.add_argument('--samples', type=int, default=12)
    ap.add_argument('--near', type=int, default=1)
    args = ap.parse_args()

    print('x=6 exact brute-force audit')
    print('conjectured target: Phi(6,n-6) = 2 + floor((n-4)/4)')
    for n in range(args.min_n, args.max_n + 1):
        best, ex, reps, run_dist, comp_dist, by_value = audit_n(n, args.near)
        target = phi6(n)
        print('\n' + '=' * 72)
        print(f'n={n:2d}  M6={best}  target={target}  match={best==target}  extremizers={len(ex)}  rev-orbits={len(reps)}')
        print('a-run-count distribution:', dict(sorted(run_dist.items())))
        print('a-run-composition distribution:', dict(sorted(comp_dist.items())))
        print('extremal reversal representatives:')
        for w in reps[:args.samples]:
            print(' ', fmt_word(w), ' gaps=', b_gap_vector(w))
        if len(reps) > args.samples:
            print(f'  ... {len(reps)-args.samples} more reversal orbits')
        for d in range(1, args.near + 1):
            vals = by_value.get(best + d, [])
            if vals:
                rc = Counter(len(a_run_composition(w)) for w in vals)
                print(f'near +{d}: count={len(vals)}, a-run-count={dict(sorted(rc.items()))}')


if __name__ == '__main__':
    main()
