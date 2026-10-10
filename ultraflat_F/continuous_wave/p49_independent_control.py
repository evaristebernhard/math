#!/usr/bin/env python3
"""p49 proxy independent-sign negative control, not a q49 Fourier constructor."""
import json
import numpy as np

def run(n=200,seed=20261010):
    rng=np.random.default_rng(seed)
    Y=rng.uniform(0,1,(n,49))
    x=np.cos(2*np.pi*Y[:,0])
    for j in range(1,49):
        t=1-x*x
        x=x+(.5*t+.125*t*t)*np.cos(2*np.pi*Y[:,j])
    s=np.where(x>=0,1,-1)
    correlations=np.array([np.dot(s[:-r],s[r:]) for r in range(1,n)],float)
    J=2*np.sum(correlations*correlations)/n**2
    amp=abs(np.fft.fft(s,n=65536))/np.sqrt(n)
    return {'n':n,'seed':seed,'p49_energy_sample':float(np.mean(x*x)),
            'teacher_is_q49':False,'C4_autocorrelation':float(J),
            'C4_Rademacher_expected':(n-1)/n,
            'grid_min_modulus':float(amp.min()),
            'grid_max_modulus':float(amp.max()),
            'note':'Sample diagnostics only.'}

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
