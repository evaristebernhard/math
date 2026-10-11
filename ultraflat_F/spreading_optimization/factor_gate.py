#!/usr/bin/env python3
"""Necessary feasibility certificate on the Fourier-magnitude obstruction.
For fixed h and B the optimal (among equal-magnitude-coefficient factors)
L2 mismatch squared is exactly sum_{u in B}(|I_u|-1/sqrt(L))**2
+ sum_{u not in B}|I_u|**2. Finite FFT approximates I_u; not rigorous
until coefficient integrals are interval-certified.
"""
import argparse, json
import numpy as np

def cutoff(z,edge=.025):
    a=np.abs(z);t=(a-(.5-edge))/edge
    out=np.ones_like(a)
    m=(t>0)&(t<1)
    v=t[m];l=np.exp(-1/v);r=np.exp(-1/(1-v));out[m]=r/(l+r)
    out[a>=.5]=0.
    return out

def report(T,mesh=131072,edge=.025,beta=1.0):
    z=np.arange(mesh)/mesh-.5
    g=cutoff(z,edge)
    h=g*np.exp(1j*np.pi*T*beta*z*z)
    Ihat=np.fft.fft(h)/mesh  # Fourier coefficients, grid sampled at x=z+1/2
    u=np.fft.fftfreq(mesh,d=1/mesh).astype(np.int64)
    Ihat*=np.where(u%2==0,1.0,-1.0) # back to centered z basis, sign irrelevant for modulus
    L=2*int(T*abs(beta)/2)+1
    B=np.abs(u)<= (L-1)//2
    mags=np.abs(Ihat[B]);target=1/np.sqrt(L)
    l2_inside=np.sum((mags-target)**2)
    l2_outside=np.sum(np.abs(Ihat[~B])**2)
    ideal_phase=np.zeros(mesh,complex)
    # phases of real Fourier coefficients corrected for center shift
    good=np.abs(Ihat[B])>1e-14
    ph=np.ones(B.sum(),complex)
    ph[good]=Ihat[B][good]/np.abs(Ihat[B][good])
    ideal_phase[B]=ph*target
    # Centered-z coefficients require factor (-1)^u to evaluate at x=z+1/2.
    ideal_phase_x=np.zeros(mesh,complex)
    ideal_phase_x[B]=ph*target*np.where(u[B]%2==0,1.0,-1.0)
    f=np.fft.ifft(ideal_phase_x)*mesh
    return {'T':T,'L':L,'mesh':mesh,'edge':edge,'energy_h':float(np.mean(g*g)),
            'best_possible_L2_error':float(np.sqrt(l2_inside+l2_outside)),
            'min_L2_error_inside':float(np.sqrt(l2_inside)),
            'tail_L2':float(np.sqrt(l2_outside)),
            'phase_projection_sup_grid':float(np.max(np.abs(f-h))),
            'phase_projection_maxmod_grid':float(np.max(np.abs(f)))}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--T',type=int,nargs='+',default=[63,127,255,511,1023]);p.add_argument('--edge',type=float,default=.025)
    a=p.parse_args();print(json.dumps([report(T,edge=a.edge) for T in a.T],indent=2))
