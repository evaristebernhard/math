"""Independent half-disc affine PV apparent-power upper bound.

For y = d + sum_j T_j*w_j + t*s + e, where wj in right half-disc of
radius Cj, |s|<=h and ||e||<=eta, return an exact-real mathematical
upper bound on sup ||y||_2. Requires angular Lipschitz allowance.
Uses ordinary float (NOT outward-rounded machine proof).
"""
from math import cos, sin, hypot, sqrt, pi


def support(a,b,radius):
    if radius < 0: raise ValueError("radius must be >=0")
    return radius*(hypot(a,b) if a>=0 else abs(b))


def apparent_power_upper(d,blocks,radii,load_vec=(0.,0.),
                         half_width=0.,remainder=0.,angles=4096):
    if len(blocks)!=len(radii) or angles<8 or half_width<0 or remainder<0:
        raise ValueError("bad arguments")
    K=hypot(*d)+half_width*hypot(*load_vec)
    for A,c in zip(blocks,radii):
        if c < 0: raise ValueError("negative radius")
        K+=c*sqrt(sum(x*x for row in A for x in row))
    sampled=float("-inf")
    for k in range(angles):
        sx,sy=cos(2*pi*k/angles),sin(2*pi*k/angles)
        phi=sx*d[0]+sy*d[1]+half_width*abs(sx*load_vec[0]+sy*load_vec[1])
        for A,c in zip(blocks,radii):
            wp=sx*A[0][0]+sy*A[1][0]
            wq=sx*A[0][1]+sy*A[1][1]
            phi+=support(wp,wq,c)
        sampled=max(sampled,phi)
    return dict(sampled_lower=sampled,angular_allowance=pi*K/angles,
                nonlinear_allowance=remainder,total_upper=sampled+pi*K/angles+remainder)


def main():
    import random
    rng=random.Random(41)
    d=(.025,.081);t=(0.,.02)
    blocks=[((1.,0.),(-.3,.8)),((0.,0.),(.25,-.15))]
    C=(.0125,.009);h=.01;eta=.0005
    b=apparent_power_upper(d,blocks,C,t,h,eta,angles=2048)
    for _ in range(4000):
        ws=[]
        for c in C:
            ang=rng.uniform(-pi/2,pi/2);r=sqrt(rng.random())*c
            ws.append((r*cos(ang),r*sin(ang)))
        s=rng.uniform(-h,h)
        y=[d[0],d[1]]
        for i in (0,1):
            y[i]+=t[i]*s+sum(A[i][0]*w[0]+A[i][1]*w[1]
                              for A,w in zip(blocks,ws))
        assert hypot(*y)+eta<=b['total_upper']+1e-12
    print('Illustrative PV apparent-power upper:',round(b['total_upper'],8))
    print('Passed finite-sample checks, NOT a directed-rounding proof.')


if __name__=='__main__':main()
