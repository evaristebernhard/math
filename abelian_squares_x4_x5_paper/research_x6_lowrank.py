from itertools import combinations
from math import floor


def words_with_x_a(n, x=6):
    for pos in combinations(range(n), x):
        s = ['b'] * n
        for p in pos:
            s[p] = 'a'
        yield ''.join(s)


def abelian_squares(w):
    n = len(w)
    pa = [0]*(n+1)
    for i,c in enumerate(w):
        pa[i+1] = pa[i] + (c == 'a')
    out = set()
    for i in range(n):
        for j in range(i+2,n+1,2):
            h=(j-i)//2
            if pa[i+h]-pa[i] == pa[j]-pa[i+h]:
                out.add(w[i:j])
    return out


def target(n):
    return 2 + floor((n-4)/4)


def low_family(u):
    ac = u.count('a')
    bc = len(u)-ac
    trivial = (ac == 0 or bc == 0)
    return trivial or ac in (2, 4)


def main():
    for n in range(10,25):
        best_low = 10**9
        witness = None
        total_counter = 0
        worst_gap = 0
        for w in words_with_x_a(n):
            A = abelian_squares(w)
            low = sum(1 for u in A if low_family(u))
            if low < best_low:
                best_low = low
                witness = w
            if low < target(n):
                total_counter += 1
                worst_gap = max(worst_gap, target(n)-low)
        print(n, 'target',target(n),'min_low',best_low,'counterexamples',total_counter,'worst_deficit',worst_gap,'witness',witness)

if __name__=='__main__':
    main()
