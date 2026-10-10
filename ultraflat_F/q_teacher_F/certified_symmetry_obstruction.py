#!/usr/bin/env python3
"""Exact arithmetic obstruction to direct coefficient balancing of q49.
Uses only modes e1, (2,1) and (2,-1). The frequency modes survive
all later quartic martingale steps; positive Jackson kernels only damp them.
For J_L=(Fejer_L)^2 / integral(Fejer_L)^2, exact Fourier multipliers:
 j_L(1)=1-3/(2L^2+1)
 j_L(2)=1-(12-9/L)/(2L^2+1), for L>=2.
"""
from fractions import Fraction as Q
from math import sqrt
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'q49_F_bridge'))
from certified_jackson_cutoffs import ceil_sqrt_fraction

def jackson_cutoff(i,depth=49):
    V=(Q(1,2) if i==1 else Q(25,128))*Q(3,2)**(depth-i)
    return max(2,ceil_sqrt_fraction(Q(3*depth)*V/Q(1,200)))

def alpha(L,h):
    if h==1:return Q(1)-Q(3,2*L*L+1)
    if h==2:return Q(1)-(Q(12)-Q(9,L))/Q(2*L*L+1)
    raise NotImplementedError(h)

def run():
    L1,L2=jackson_cutoff(1),jackson_cutoff(2)
    A=Q(1,2)*alpha(L1,1)
    B=Q(5,64)*alpha(L1,2)*alpha(L2,1)
    # Suppose relative squared balancing: |c_a|² / |a.v| in [1-eta,1+eta]
    # on e1, 2e1+e2, 2e1-e2. Necessarily
    #    2A²/(1+eta) <= B²/(1-eta)
    eta=(2*A*A-B*B)/(2*A*A+B*B)
    # If all 3 frequencies included and exact balanced, any L2-distance
    # between F and q >= (sqrt(2)*A-B)/(sqrt(2)+1) by triangle inequality.
    L2_floor=(sqrt(2)*float(A)-float(B))/(sqrt(2)+1)
    return {'L1':L1,'L2':L2,'jackson_hat1_at_e1':float(alpha(L1,1)),
        'teacher_coeff_e1':float(A),'teacher_coeff_2e1_plus_e2':-float(B),
        'teacher_coeff_2e1_minus_e2':-float(B),
        'necessary_relative_squared_balance_error_eta':float(eta),
        'minimal_L2_distance_if_exact_balanced_and_three_modes_kept':L2_floor,
        'source_coefficients_exact_unfiltered':['1/2','-5/64','-5/64'],
        'note':'Results exact except displayed decimal values; L2 distance uses floating sqrt(2). Applies only to retaining all three original frequencies; does NOT rule out spreading into new variables.'}

if __name__=='__main__':
    r=run();print(json.dumps(r,indent=2));import argparse
    p=argparse.ArgumentParser();p.add_argument('--out',default='');a=p.parse_args();
    if a.out:open(a.out,'w').write(json.dumps(r,indent=2))
