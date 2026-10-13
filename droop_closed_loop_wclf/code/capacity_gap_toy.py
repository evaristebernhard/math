"""Simple exact hosting-capacity-gap example.

This script checks an elementary mathematical theorem on a *toy* fixed-voltage
line. It is not a nonlinear DistFlow / IEEE-33 certification.
Run: python3 code/capacity_gap_toy.py
"""
from math import sqrt

PV = 0.30
UNCERTAINTY = 0.05
CURRENT_LIMIT = 0.20
OUTER_GAP = 0.001  # squared-current pu, NOT MW


def worst_squared_current(load):
    a = load - PV
    if a < 0:
        return (a - UNCERTAINTY)**2
    return a*a + UNCERTAINTY**2


def main():
    upper_true = PV + sqrt(CURRENT_LIMIT**2-UNCERTAINTY**2)
    upper_cert = PV + sqrt(CURRENT_LIMIT**2-UNCERTAINTY**2-OUTER_GAP)
    lower_true = PV + UNCERTAINTY - CURRENT_LIMIT
    m = 2*(0.45-PV)  # derivative infimum on the upper boundary neighborhood
    loss = upper_true-upper_cert
    assert abs(lower_true-0.15)<1e-12
    assert worst_squared_current(0) > CURRENT_LIMIT**2
    assert abs(worst_squared_current(upper_true)-CURRENT_LIMIT**2)<1e-12
    assert abs(worst_squared_current(upper_cert)+OUTER_GAP-CURRENT_LIMIT**2)<1e-12
    assert upper_true-OUTER_GAP/m>=0.45
    assert loss<=OUTER_GAP/m
    print("True robust upper capacity (pu):",upper_true)
    print("Certified outer-bound upper capacity (pu):",upper_cert)
    print("Lost hosting capacity (pu):",loss)
    print("Theorem upper bound on capacity loss (pu):",OUTER_GAP/m)


if __name__=="__main__":
    main()
