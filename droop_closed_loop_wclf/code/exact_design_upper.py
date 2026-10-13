"""Self-contained exact-rational all-gain hosting upper bound for IEEE 33.

No numpy/scipy required. Does not compute a safe inner bound or optimize gains.
The common 0.31pu thermal limit is an assumed study value.
Run: python3 code/exact_design_upper.py
"""
from fractions import Fraction as F

# From, to, r_ohm, x_ohm, loadP_kW, loadQ_kVAr; buses 2..33.
ROWS = """\
1 2 0.0922 0.047 100 60
2 3 0.493 0.2511 90 40
3 4 0.366 0.1864 120 80
4 5 0.3811 0.1941 60 30
5 6 0.819 0.707 60 20
6 7 0.1872 0.6188 200 100
7 8 0.7114 0.2351 200 100
8 9 1.03 0.74 60 20
9 10 1.044 0.74 60 20
10 11 0.1966 0.065 45 30
11 12 0.3744 0.1238 60 35
12 13 1.468 1.155 60 35
13 14 0.5416 0.7129 120 80
14 15 0.591 0.526 60 10
15 16 0.7463 0.545 60 20
16 17 1.289 1.721 60 20
17 18 0.732 0.574 90 40
2 19 0.164 0.1565 90 40
19 20 1.5042 1.3554 90 40
20 21 0.4095 0.4784 90 40
21 22 0.7089 0.9373 90 40
3 23 0.4512 0.3083 90 50
23 24 0.898 0.7091 420 200
24 25 0.896 0.7011 420 200
6 26 0.203 0.1034 60 25
26 27 0.2842 0.1447 60 25
27 28 1.059 0.9337 60 20
28 29 0.8042 0.7006 120 70
29 30 0.5075 0.2585 200 600
30 31 0.9744 0.963 150 70
31 32 0.3105 0.3619 210 100
32 33 0.341 0.5302 60 40
""".strip().splitlines()
rows = [line.split() for line in ROWS]
n = 32
assert len(rows) == n
parent = [int(row[0])-2 for row in rows]
assert all(int(row[1]) == i+2 for i,row in enumerate(rows))
zbase=F('12.66')**2/F('10')
r = [F(row[2])/zbase for row in rows]
x = [F(row[3])/zbase for row in rows]
base_p = [F(row[4])*F('.65')/10000 for row in rows]
base_q = [F(row[5])*F('.65')/10000 for row in rows]
PV=(7,16,22,31)
V_MAX=F('1.05')
I_MAX=F('.31')
qcap_up=F('.096825')
assert qcap_up*qcap_up>F('.1')**2-F('.025')**2
D=[[0]*n for _ in range(n)]
for j in range(n):
    k=j
    while k>=0:
        D[k][j]=1
        k=parent[k]
assert sum(D[0]) == n

def downstream(lam):
    out=[base_p[j] - (F('.025') if j in PV else 0) + (lam/10 if j==16 else 0) for j in range(n)]
    for j in reversed(range(n)):
        if parent[j]>=0:out[parent[j]]+=out[j]
    return out

row=16
R=[sum((F(D[k][row]*D[k][j])*r[k] for k in range(n)),F(0)) for j in range(n)]
X=[sum((F(D[k][row]*D[k][j])*x[k] for k in range(n)),F(0)) for j in range(n)]
M=[]
for j in range(n):
    M.append(sum((F(D[k][row]*(int(k==j)-2*D[k][j]))*(r[k]*r[j]+x[k]*x[j]) for k in range(n)),F(0)))
assert all(z>=0 for z in R+X)
assert all(z<=0 for z in M)

def necessary_voltage_upper(lam):
    p=[-base_p[j]+(F('.025') if j in PV else 0)-(lam/10 if j==16 else 0) for j in range(n)]
    q=[-base_q[j]+(qcap_up if j in PV else 0) for j in range(n)]
    sub=downstream(lam)
    ell_min=[max(F(0),t)**2/V_MAX**2 for t in sub]
    return 1 +2*sum((R[j]*p[j]+X[j]*q[j] for j in range(n)),F(0))+sum((M[j]*ell_min[j] for j in range(n)),F(0))

def necessary_source_lower(lam):
    sub=downstream(lam)
    loss_min=sum((r[j]*max(F(0),sub[j])**2/V_MAX**2 for j in range(n)),F(0))
    return sub[0]+loss_min

def upper_at_six_decimals():
    lo,hi=F(0),F(3)
    assert necessary_voltage_upper(lo)>F('.95')**2>necessary_voltage_upper(hi)
    for _ in range(75):
        md=(lo+hi)/2
        if necessary_voltage_upper(md)>F('.95')**2:lo=md
        else:hi=md
    up=F((hi*1000000).__ceil__(),1000000)
    assert necessary_voltage_upper(up)<F('.95')**2
    assert necessary_source_lower(F('1.506628'))>I_MAX
    return up

if __name__=='__main__':
    cap=upper_at_six_decimals()
    print('All-gain true robust connected hosting upper <=',float(cap),'MW')
    print('Bus18 squared-V upper at bound',float(necessary_voltage_upper(cap)))
    print('Threshold squared-V',float(F('.95')**2))
    print('Exact positive gap',F('.95')**2-necessary_voltage_upper(cap))
    print('Weaker independent source-current outer <=1.506628 MW')
