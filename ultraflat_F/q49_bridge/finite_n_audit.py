#!/usr/bin/env python3
"""Necessary amplitude-resolution check for Section 5's *individual waves*.
Not a no-go theorem for finite real Littlewood polynomials or other designs.
"""
import argparse, math

def report(n: int, h: int, d: int):
    if n < 2 or h < 1 or d < 1:
        raise ValueError("Need N>=2, H>=1, D>=1")
    w_avg = 1.0/(2*d)  # optimistic; w_min cannot exceed average
    scale = n*w_avg/(h*h)
    max_d_threshold = n/(2*h*h)  # limiting scale=1 for equal weights
    return {
        "N":n, "H":h, "D":d,
        "optimistic_Nw_min_over_H_squared":scale,
        "D_threshold_for_all_wave_scale_at_least_one":max_d_threshold,
        "even_N_autocorrelation_epsilon_lower_bound": (
          math.sqrt(1+1/math.sqrt(n))-1 if n%2==0 else None
        ),
        "warning":"A necessary test for termwise stationary-phase asymptotics only."
    }

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--n",type=int,default=200)
    p.add_argument("--h",type=int,default=2)
    p.add_argument("--d",type=int,default=40)
    a=p.parse_args()
    for key,value in report(a.n,a.h,a.d).items():
        print(key,value)
