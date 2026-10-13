"""Simple regression tests; they are NOT formal directed-rounding proofs."""
import math
import unittest

from half_disc_support import (
    support, candidate_and_lambda, affine_phasor_norm_angle_bounds
)


class HalfDiscTests(unittest.TestCase):
    def test_support_formula_against_sampled_boundary(self):
        c = 1.7
        for a,b in ((1,2),(-1,2),(2,0),(-2,0),(0,-4),(0,0)):
            opt = support(a,b,c)
            observed = max(
                a*(c*math.cos(t)) + b*(c*math.sin(t))
                for t in (-math.pi/2 + k*math.pi/8000 for k in range(8001))
            )
            # Include the origin for the a<0,b=0 case.
            observed = max(0,observed)
            self.assertLessEqual(observed,opt+1e-12)
            self.assertLessEqual(opt-observed,0.002)

    def test_curvature_certificate(self):
        c=1.3
        for g in ((1,2),(2,0),(-1,3),(-3,-1),(0,4)):
            star,lam=candidate_and_lambda(*g,c)
            kap=lam/(2*c)
            self.assertGreater(kap,0)
            for k in range(801):
                t=-math.pi/2+k*math.pi/800
                u=(c*math.cos(t),c*math.sin(t))
                gap=g[0]*(star[0]-u[0])+g[1]*(star[1]-u[1])
                dist2=(star[0]-u[0])**2+(star[1]-u[1])**2
                self.assertGreaterEqual(gap+1e-10,kap*dist2)

    def test_degenerate_case(self):
        _, lam=candidate_and_lambda(-1.0,0.0,1.0)
        self.assertEqual(lam,0)

    def test_affine_phasor_grid_enclosure(self):
        base=(0.3, -0.1)
        blocks=[((1.1,0.2),(-0.4,0.6)),((0.1,-0.5),(0.8,0.2))]
        radii=[0.4,0.2]
        lo,hi=affine_phasor_norm_angle_bounds(base,blocks,radii,grid_size=2048)
        self.assertLessEqual(lo,hi)
        for t in range(201):
            a=-math.pi/2+math.pi*t/200
            w1=(radii[0]*math.cos(a),radii[0]*math.sin(a))
            w2=(0.0,radii[1])
            value=[
                base[k]+sum(blocks[j][k][0]*w[0]+blocks[j][k][1]*w[1]
                            for j,w in enumerate((w1,w2)))
                for k in range(2)
            ]
            self.assertLessEqual(math.hypot(*value),hi+1e-12)


class SaturationCapacityTests(unittest.TestCase):
    def test_exact_rational_saturation_capacity_bracket(self):
        from saturation_vi_toy import test as saturation_capacity_test
        saturation_capacity_test()


if __name__ == "__main__":
    unittest.main()
