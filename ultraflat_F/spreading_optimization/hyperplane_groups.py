#!/usr/bin/env python3
"""Rigorous linear-algebraic grouping of original D spreading factors.
For 3D support, pair i,j if the plane span(s_i,s_j) contains no
other support representative. Build a maximum matching in this graph;
each matched pair can share one first-order-vanishing W_j^0.
For each group of size 1 or 2, the linear first-order value equations
have a solution if the group vectors are linearly independent.
"""
import json
import numpy as np
import networkx as nx
from seed_fourier import generate

def group_p3():
    c=generate(3)
    # canonical sign: first nonzero coordinate positive
    s=sorted([a for a in c if next(x for x in a if x)>0]);n=len(s)
    G=nx.Graph();G.add_nodes_from(range(n));pairs=[]
    for i in range(n):
        for j in range(i+1,n):
            cross=np.cross(s[i],s[j]);
            if np.all(cross==0):continue
            vanish=[k for k in range(n) if np.dot(cross,s[k])==0]
            if vanish==[i,j]:
                G.add_edge(i,j);pairs.append((i,j))
    matched=nx.algorithms.matching.max_weight_matching(G,maxcardinality=True)
    groups=[sorted(pair) for pair in matched]
    used=set(i for group in groups for i in group)
    groups.extend([[i] for i in range(n) if i not in used])
    # Verify every pair W_j^0 annihilates precisely the intended support group
    assert sum(len(g) for g in groups)==n
    return {'d':3,'D':n,'groups':len(groups),'paired_groups':len(matched),
            'admissible_edges':len(pairs),'group_frequencies':[[list(s[i]) for i in group] for group in groups],
            'explanation':'Generic one-factor-per-support-sign-pair construction reduces to one factor per matched hyperplane group, preserving first-order product fitting; magnitude-control factor lemma still needed.'}

if __name__=='__main__':
 r=group_p3();print(json.dumps({k:v for k,v in r.items() if k!='group_frequencies'},indent=2))
 open('/mnt/data/spreading_optimization/p3_groups.json','w').write(json.dumps(r,indent=2))

def construct_p3(tau=1e-7):
    from fractions import Fraction
    import itertools, math
    from sympy import Matrix, Rational
    c=generate(3)
    supp=sorted([a for a in c if next(x for x in a if x)>0]);D=len(supp)
    grouping=group_p3()
    groups=[[supp.index(tuple(a)) for a in group] for group in grouping['group_frequencies']]
    W0=[]
    for gr in groups:
        if len(gr)==2:
            a,b=[Matrix(supp[i]) for i in gr];w=a.cross(b)
        else:
            a=Matrix(supp[gr[0]]);w=None
            for vec in itertools.product(range(-2,3),repeat=3):
                if vec==(0,0,0):continue
                t=a.cross(Matrix(vec))
                if t!=Matrix([0,0,0]) and all(t.dot(Matrix(supp[k]))!=0 for k in range(D) if k not in gr):
                    w=t;break
            if w is None:raise ValueError('failed singleton')
        gcd=math.gcd(*(abs(int(z)) for z in w))
        w=w/gcd
        assert all(w.dot(Matrix(supp[i]))==0 for i in gr)
        assert all(w.dot(Matrix(supp[i]))!=0 for i in range(D) if i not in gr)
        W0.append(w)
    gamma=Matrix([Rational(1),Rational(13),Rational(169)])
    rho=[abs(Matrix(s).dot(gamma)) for s in supp]
    assert all(x for x in rho)
    W1=[]
    for j,gr in enumerate(groups):
        vals=[]
        for i in gr:
            b=c[supp[i]]
            product=Rational(1)
            for k,w in enumerate(W0):
                if k!=j:product*=abs(Matrix(supp[i]).dot(w))
            vals.append(Rational(b.numerator*b.numerator,b.denominator*b.denominator)/(rho[i]*product))
        mat=Matrix([supp[i] for i in gr])
        vec=Matrix(vals)
        # minimum norm rational solution: mat.T*(mat*mat.T)^-1 * val
        W1.append(mat.T*(mat*mat.T).inv()*vec)
        assert mat*W1[-1]==vec
    tau=Rational(str(tau))
    W=[a+tau*b for a,b in zip(W0,W1)]
    betas=[[abs(Matrix(s).dot(w)) for w in W] for s in supp]
    rel=[]
    for i,s in enumerate(supp):
        P=Rational(1)
        for v in betas[i]:P*=v
        target=tau*Rational(c[s].numerator*c[s].numerator,c[s].denominator*c[s].denominator)/rho[i]
        rel.append(abs(P/target-1))
    minbeta=min(map(float,(a for row in betas for a in row)))
    minimum_per_factor=[min(float(betas[i][j]) for i in range(D)) for j in range(len(W))]
    rcount=len(W)
    t_j=[100./x for x in minimum_per_factor]
    uniform_T=100./minbeta
    log10_spread_costs=[sum(__import__('math').log10(t_j[j]*float(betas[i][j])) for j in range(rcount)) for i in range(D)]
    result={'tau':str(tau),'D':D,'r':len(W0),
       'log10_uniform_T_product':rcount*__import__('math').log10(uniform_T),
       'log10_anisotropic_T_product':sum(__import__('math').log10(x) for x in t_j),
       'log10_max_individual_box_size_anisotropic':max(log10_spread_costs),
       'log10_min_individual_box_size_anisotropic':min(log10_spread_costs),
       'factorwise_min_beta':minimum_per_factor,
       'max_relative_product_error':max(map(float,rel)),
       'smallest_projection_beta':minbeta,
       'T_for_min_spreading_width_100':100/minbeta,
       'max_w0_coordinate':max(abs(int(x)) for w in W0 for x in w)}
    return result
