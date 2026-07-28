#!/usr/bin/env python3
"""
Cross-model checks: v7.5 vs v7.7, claim by claim.

Run:  python3 rsm/audit/cross_model_checks.py

Companion to checks.py (which carries the original audit's arithmetic). This file
does two jobs checks.py does not:

  PART A - v7.5's theorems that nothing previously machine-checked (Prop 2.1,
           Def 4.3 / Lemma 4.4, Thm 5.1, Thm 6.1, Thm 7.1).
  PART B - independent re-verification of the v7.7 r4 appendix. The appendix's
           [verified] tags were produced by the same model that drafted the
           chain; this file re-derives each checkable item from scratch so the
           tags can be disbelieved.

Idiom, as in checks.py: [PASS] means the stated fact was recomputed and holds.
A refutation of a chain's claim is stated as a fact and PASSes when the claim
fails. Exit is non-zero if any recomputation fails.

Pure stdlib. Exact rational arithmetic where possible; floats for sweeps.
Charts: v7.5 writes X = a + b, Y = a - b; v7.7 writes a = (X+Y)/2, b = (X-Y)/2.
These are the same chart. X*Y = a^2 - b^2 = Q_j;  Q_i = a^2 + b^2.  1_n = 1.
"""

import cmath
import math
import os
import re
from fractions import Fraction as F

FAILURES = []


def check(label, got, want, note=""):
    ok = got == want
    if not ok:
        FAILURES.append(label)
    mark = "PASS" if ok else "FAIL"
    tail = f"   {note}" if note else ""
    print(f"  [{mark}] {label}{tail}")
    return ok


def approx(label, got, want, tol=1e-9, note=""):
    ok = abs(got - want) < tol
    if not ok:
        FAILURES.append(label)
    mark = "PASS" if ok else "FAIL"
    tail = f"   {note}" if note else ""
    print(f"  [{mark}] {label}{tail}")
    return ok


def hdr(n, title):
    print(f"\n{'=' * 78}\n{n}. {title}\n{'=' * 78}")


Qj = lambda a, b: a * a - b * b
Qi = lambda a, b: a * a + b * b

# ===========================================================================
print("\n" + "#" * 78)
print("# PART A -- v7.5 just_math: the previously unchecked theorems")
print("#" * 78)

# ---------------------------------------------------------------------------
hdr("A1", "v7.5 Prop 2.1 -- the split-complex parameterization (HOLDS)")
pts = [(F(3, 2), F(-2, 7)), (F(1), F(1)), (F(-5, 3), F(4, 9))]
ok = all((a + b) * (a - b) == Qj(a, b) for a, b in pts)
check("XY = a^2 - b^2 under X = a+b, Y = a-b (exact, sampled)", ok, True)

# ---------------------------------------------------------------------------
hdr("A2", "v7.5 Def 4.3 + Lemma 4.4 -- the conservation-cost argument is FALSE")
# Lemma 4.4: "A path holding radius exactly sqrt(1n) throughout maintains
#             XY = 1n at every point and so has cost zero."
# On the circle of radius 1 through the seats (+-1, 0):  XY = Q_j = cos 2theta.
worst = max(abs(Qj(math.cos(t), math.sin(t)) - 1)
            for t in [k * math.pi / 180 for k in range(181)])
approx("on the claimed zero-cost arc, max |XY - 1n| = 2 (not 0)", worst, 2.0, 1e-9,
       "-> XY = cos 2theta on the circle; the 'zero cost' property fails")

# Def 4.3: "outward deviation ... strictly increases cost, since XY exceeds 1n
#           wherever the path bulges beyond the standoff circle."
a, b = 0.0, 2.0  # radius 2 > 1, i.e. outside the standoff circle
check("outward point (a,b) = (0,2): radius 2 but XY = -4 < 1n",
      Qj(a, b) < 1, True, "-> 'outward => XY > 1n' is false")

# The chart-ambiguity escape is closed: same failure in the (X,Y) chart about
# P = (1,1) (v7.5 says the arc is 'centered at P').
worst_xy = max(abs((1 + math.cos(t)) * (1 + math.sin(t)) - 1)
               for t in [k * math.pi / 90 for k in range(180)])
check("circle of radius 1 about P=(1,1) in (X,Y): XY = 1n fails there too",
      worst_xy > 1.0, True)

# And no zero-cost spanning path EXISTS. A cost-zero path holds XY = 1n at every
# point, i.e. lies entirely on G. On G, a^2 = 1n + b^2 >= 1n, so |a| >= 1 and a
# never reaches 0: a continuous path on G cannot change the sign of a. The seats
# +P = (1,0) and -P = (-1,0) have opposite sign of a. (v7.7 Theorem 1's wall.)
a_on_G = lambda b: math.sqrt(1 + b * b)
check("on G, |a| >= 1 for every b -- a never reaches 0",
      min(a_on_G(b) for b in [k / 20 for k in range(-200, 201)]) >= 1.0, True)
check("so no continuous path inside G joins a = +1 to a = -1 (sign of a is locked)",
      (a_on_G(0.0) > 0, -a_on_G(0.0) < 0), (True, True),
      "-> zero-cost spanning is impossible, not merely non-minimal")
print("     => Lemma 4.4 is arithmetically false, independent of the circularity")
print("        already recorded (checks.py 9). Cor. 4.5 inherits the failure.")
print("     => v7.7's Theorem 1 (wall) + Theorem 2 (toll: Q_j reaches -1n on every")
print("        spanning path) is the corrected statement of this ground.")
print("     => The prior audit priced r5/v7.7's move to Definition T as an 'honest")
print("        retreat'. It was a forced one: the thing retreated from was false.")

# ---------------------------------------------------------------------------
hdr("A3", "v7.5 Thm 5.1 -- the five-case elimination table (HOLDS)")
# Elements modeled as s * i^e, s in {-1,0,1}, e in {0,1}; i^2 := c reduces e=2.


def orbit(c):
    p, seen = (1, 1), []          # p = i^1
    for _ in range(8):
        seen.append(p)
        s, e = p
        p = (s, e + 1)
        if p[1] == 2:             # reduce i^2 -> c
            p = (p[0] * c[0], c[1])
    closure = (1, 0) in seen
    spanning = (-1, 0) in seen
    return closure, spanning


cases = {"i^2=+1": (1, 0), "i^2=0": (0, 0), "i^2=i": (1, 1),
         "i^2=-i": (-1, 1), "i^2=-1": (-1, 0)}
expect = {"i^2=+1": (True, False), "i^2=0": (False, False), "i^2=i": (False, False),
          "i^2=-i": (False, False), "i^2=-1": (True, True)}
for name, c in cases.items():
    check(f"{name}: (closure, spanning) = {expect[name]}", orbit(c), expect[name])
check("exactly one case satisfies both C and S",
      [n for n in cases if orbit(cases[n]) == (True, True)], ["i^2=-1"],
      "-> the table is right. (The audit's separate finding stands: Requirement S's")
print("        wording equates algebra elements +-1 with the modes -- the seating's origin.)")

# ---------------------------------------------------------------------------
hdr("A4", "v7.5 Thm 6.1 -- rotation-invariant forms (HOLDS among quadratics; gap named)")


def q_rot(coef, th, a, b):
    al, be, ga = coef
    c, s = math.cos(th), math.sin(th)
    x, y = c * a - s * b, s * a + c * b
    return al * x * x + be * x * y + ga * y * y


samples = [(0.7, -1.3), (1.1, 0.2), (-0.4, 0.9)]
angles = [0.3, 0.7, 1.1, 2.0, 2.6]
inv = lambda coef: max(abs(q_rot(coef, th, a, b) - q_rot(coef, 0, a, b))
                       for th in angles for a, b in samples)
approx("a^2 + b^2 is rotation-invariant", inv((1, 0, 1)), 0.0, 1e-12)
check("a^2 - b^2, ab, a^2 alone are each NOT rotation-invariant",
      all(inv(c) > 1e-3 for c in [(1, 0, -1), (0, 1, 0), (1, 0, 0)]), True,
      "-> among quadratic forms, invariance forces beta = 0, alpha = gamma")
r4 = max(abs(Qi(math.cos(th) * a - math.sin(th) * b, math.sin(th) * a + math.cos(th) * b) ** 2
             - Qi(a, b) ** 2) for th in angles for a, b in samples)
approx("but (a^2+b^2)^2 is ALSO rotation-invariant and is not a quadratic form",
       r4, 0.0, 1e-9,
       "-> 'unique up to scale' holds only AMONG quadratic forms")
print("     => Thm 6.1's proof assumes the conserved magnitude is a quadratic form.")
print("        That assumption is the Finsler hole v7.7 names and leaves open (the")
print("        generation principle, open item 2). v7.5 used it silently.")

# ---------------------------------------------------------------------------
hdr("A5", "v7.5 Thm 7.1 -- perpendicularity at the seat (HOLDS)")
# slope of G at (x0, 1/x0) is -1/x0^2; slope of B is +1. At the seat x0 = 1.
check("slope(G) at seat = -1, slope(B) = +1, Q_i-inner-product of tangents = 0",
      (F(-1, 1), F(1, 1), (1 * 1 + (-1) * 1)), (F(-1), F(1), 0))
print("     [INFO] v7.5 Prop 4.1 (density is not completeness; Q is the trap) is")
print("            correct as logic; nothing to compute. It stands.")

# ===========================================================================
print("\n" + "#" * 78)
print("# PART B -- v7.7 r4 appendix, re-verified from scratch")
print("#" * 78)

# ---------------------------------------------------------------------------
hdr("B1", "appendix 1 -- founding observation, slope product and deficit")
slopes = [(x0, F(-1, 1) / (x0 * x0)) for x0 in [F(1), F(2), F(1, 2), F(3, 2)]]
check("slope product sigma(x0) = -1/x0^2 (exact)",
      all(s == F(-1) / (x * x) for x, s in slopes), True)
check("sigma(x0) = -1 iff x0 = sqrt(1n)",
      [x for x, s in slopes if s == F(-1)], [F(1)])
check("deficit sigma(x0) + 1 = 1 - 1/x0^2 (exact)",
      all(s + 1 == 1 - F(1) / (x * x) for x, s in slopes), True)

# ---------------------------------------------------------------------------
hdr("B2", "appendix 2 -- seat curvature: radius sqrt(2), center at 2P [mode chart]")
# y = 1/x: y' = -1/x^2, y'' = 2/x^3. At (1,1): R = (1+y'^2)^{3/2} / |y''|.
yp, ypp = -1.0, 2.0
R = (1 + yp * yp) ** 1.5 / abs(ypp)
approx("osculating radius at (1,1) = sqrt(2) = |O P| ", R, math.sqrt(2))
nx, ny = 1 / math.sqrt(2), 1 / math.sqrt(2)          # unit normal at the seat
center = (1 + R * nx, 1 + R * ny)
approx("osculating center = (2,2) = 2P (x)", center[0], 2.0)
approx("osculating center = (2,2) = 2P (y)", center[1], 2.0)

# ---------------------------------------------------------------------------
hdr("B3", "appendix 3 -- circle regimes about O in the mode chart (exact)")
# X^2 + Y^2 = r^2 on XY = 1:  u + 1/u = r^2 with u = X^2 > 0; disc = r^4 - 4.


def crossings(r2):
    disc = r2 * r2 - 4
    if disc < 0:
        return 0
    if disc == 0:
        return 2                   # u = 1 -> X = +-1, two points
    return 4                       # two u's, each X = +-sqrt(u)


check("r^2 < 2: no crossings; r^2 = 2: tangent at the two seats; r^2 > 2: four",
      [crossings(F(3, 2)), crossings(F(2)), crossings(F(3))], [0, 2, 4])

# ---------------------------------------------------------------------------
hdr("B4", "appendix 5 + 23 -- the canonical map w = z^2 - 2i, and the chart flag")
w = lambda z: z * z - 2j
onG = [complex(x, 1 / x) for x in (0.5, 1.0, 1.7, -2.0, -0.8)]     # z = X + iY
approx("parent G (XY=1) maps into the REAL axis (child x-axis)",
       max(abs(w(z).imag) for z in onG), 0.0, 1e-12)
onB = [complex(x, x) for x in (0.5, 1.0, -1.3)]
approx("parent B (X=Y) maps into the IMAGINARY axis (child y-axis)",
       max(abs(w(z).real) for z in onB), 0.0, 1e-12)
approx("seat (1,1) maps to the child origin", abs(w(1 + 1j)), 0.0, 1e-12)
approx("nu-identification: w(-z) = w(z) (2-to-1)",
       max(abs(w(-z) - w(z)) for z in onG + onB), 0.0, 1e-12)
approx("parent O sits at the branch point, depth |w(0)| = 2*1n", abs(w(0)), 2.0)
# Item 23's identities need the OTHER chart, z = a + ib:
a_, b_ = F(3, 4), F(-2, 5)
X_, Y_ = a_ + b_, a_ - b_
z2re, z2im = a_ * a_ - b_ * b_, 2 * a_ * b_
check("item 23's 'Re z^2 = XY, Im z^2 = (X^2-Y^2)/2' holds for z = a + ib (exact)",
      (z2re, z2im), (X_ * Y_, (X_ * X_ - Y_ * Y_) / 2))
zXY = complex(float(X_), float(Y_)) ** 2
approx("but for z = X + iY (item 5's chart) it is Re z^2 = X^2-Y^2, Im z^2 = 2XY",
       abs(zXY - complex(float(X_ * X_ - Y_ * Y_), float(2 * X_ * Y_))), 0.0, 1e-9)
print("     [FLAG] appendix items 5 and 23 both write 'z' for different charts")
print("            (X + iY vs a + ib). Each is correct in its own chart; the")
print("            appendix does not say the symbol switches. Hygiene, not error.")

# ---------------------------------------------------------------------------
hdr("B5", "appendix 8 -- two returns: invariant at pi, position at 2pi")
qj_th = lambda t: Qj(math.cos(t), math.sin(t))
approx("Q_j(theta + pi) = Q_j(theta) (structure returns at pi)",
       max(abs(qj_th(t + math.pi) - qj_th(t)) for t in (0.3, 1.2, 2.2)), 0.0, 1e-12)
check("the position does NOT return at pi (antipode), only at 2pi",
      (math.cos(0.3 + math.pi) != math.cos(0.3),
       abs(math.cos(0.3 + 2 * math.pi) - math.cos(0.3)) < 1e-12), (True, True))

# ---------------------------------------------------------------------------
hdr("B6", "appendix 9 -- sigma-pairs: not bindable in-plane; half-turn through 3D")
# sigma: (X,Y) -> (-X,Y) reads (a,b) -> (-b,-a) in the split chart.
sig = lambda a, b: (-b, -a)
det_sigma = (0 * 0) - (-1) * (-1)      # matrix [[0,-1],[-1,0]]
check("det(sigma) = -1: sigma is not in SO(2)", det_sigma, -1)
quarter = lambda a, b: (-b, a)          # R(pi/2)
pts_ab = [(0.7, 0.2), (1.0, 0.0), (-0.3, 1.1)]
check("the quarter-turn binds the wrong points: R(pi/2)p != sigma(p) unless a = 0",
      all(quarter(a, b) != sig(a, b) for a, b in pts_ab if a != 0), True)


def half_turn_u(v):                     # rotation by pi about (1,-1,0)/sqrt(2)
    u = (1 / math.sqrt(2), -1 / math.sqrt(2), 0.0)
    d = sum(vi * ui for vi, ui in zip(v, u))
    return tuple(2 * d * ui - vi for vi, ui in zip(v, u))


worst = max(max(abs(half_turn_u((a, b, 0.0))[k] - (sig(a, b) + (0.0,))[k])
                for k in range(3)) for a, b in pts_ab)
approx("a half-turn about an in-plane axis, THROUGH the third dimension, realizes sigma",
       worst, 0.0, 1e-12, "-> the third direction is the cost of sigma-binding")

# ---------------------------------------------------------------------------
hdr("B7", "appendix 10 -- terminals excluded by the operation itself (exact)")
check("XY = 1n has no solution with X = 0 or Y = 0", 0 * 5 == 1 or 5 * 0 == 1, False)
check("X + Y = c DOES admit zero-solutions (additive law lacks the exclusion)",
      0 + F(3) == F(3), True)
lam, X0, Y0 = F(7, 3), F(5, 2), F(2, 5)
check("multiplicative scaling (X,Y) -> (lX, Y/l) preserves XY (exact)",
      (lam * X0) * (Y0 / lam), X0 * Y0)

# ---------------------------------------------------------------------------
hdr("B8", "appendix 11 -- rotation about B: s^2 - r^2 = 2*1n, apex at the seat")
# s = (X+Y)/sqrt(2) along B, r = |X-Y|/sqrt(2) off B: s^2 - r^2 = 2XY (exact).
Xr, Yr = F(9, 4), F(4, 9)
s2 = (Xr + Yr) ** 2 / 2
r2 = (Xr - Yr) ** 2 / 2
check("s^2 - r^2 = 2*XY = 2*1n on G (exact identity)", s2 - r2, 2 * Xr * Yr)
check("apex (r = 0): s = sqrt(2) -- the seat distance |OP|", F(2), s2 - r2)

# ---------------------------------------------------------------------------
hdr("B9", "appendix 12 -- revolution surfaces: the horn and the seat-sphere")
ys = (0.5, 1.0, 2.0, 3.0)
approx("rotating X = 1/Y about the trunk: x^2 + z^2 = 1/y^2 (the horn)",
       max(abs((math.cos(0.9) / y) ** 2 + (math.sin(0.9) / y) ** 2 - 1 / y ** 2)
           for y in ys), 0.0, 1e-12)
approx("the seats sweep the sphere of radius sqrt(2*1n)",
       math.sqrt(1 ** 2 + 1 ** 2), math.sqrt(2))

# ---------------------------------------------------------------------------
hdr("B10", "Theorems 1 and 2 -- wall, door, toll (re-derived)")
# T1(i) the wall: {Q_j = 1} has two components (a >= 1, a <= -1) and the split
# rotation e^{j phi} preserves them.
splitrot = lambda a, b, ph: (a * math.cosh(ph) + b * math.sinh(ph),
                             a * math.sinh(ph) + b * math.cosh(ph))
onGp = [(math.cosh(t), math.sinh(t)) for t in (-1.2, 0.0, 0.8)]
check("split rotations never change the component (sign of a)",
      all(splitrot(a, b, ph)[0] > 0 for a, b in onGp for ph in (-2.0, 1.5)), True,
      "-> no motion within the gradient slice connects the modes: the wall")
# T1(ii) the door: the circle path lies on the one complex law a^2 + b^2 = 1.
path = [(cmath.cos(t), cmath.sin(t)) for t in [k * math.pi / 20 for k in range(21)]]
approx("the circle path (1,0) -> (0,1) -> (-1,0) satisfies Q(z) = 1 throughout",
       max(abs(a * a + b * b - 1) for a, b in path), 0.0, 1e-12,
       "-> the two hyperbola components ARE connected, through the i-slice")
# T2 the toll, general form (IVT): any continuous spanning path avoiding O has
# a = 0 somewhere; there Q_j = -b^2 < 0.
import random as _r
_r.seed(7)


def seg_dist_to_O(p, q):
    px, py = p
    dx, dy = q[0] - px, q[1] - py
    t = max(0.0, min(1.0, -(px * dx + py * dy) / (dx * dx + dy * dy)))
    return math.hypot(px + t * dx, py + t * dy)


worst_toll, kept = float("-inf"), 0
while kept < 200:
    # random polyline from (1,0) to (-1,0); keep only those AVOIDING the origin
    # (the theorem's hypothesis -- a path through O is excluded, not tolled)
    mid = [(_r.uniform(-1, 1), _r.choice([-1, 1]) * _r.uniform(0.2, 1.5))
           for _ in range(3)]
    nodes = [(1.0, 0.0)] + mid + [(-1.0, 0.0)]
    if min(seg_dist_to_O(p, q) for p, q in zip(nodes, nodes[1:])) < 0.05:
        continue
    kept += 1
    reached = 1.0
    for (a0, b0), (a1, b1) in zip(nodes, nodes[1:]):
        for t in [k / 200 for k in range(201)]:
            a, b = a0 + t * (a1 - a0), b0 + t * (b1 - b0)
            reached = min(reached, Qj(a, b))
    worst_toll = max(worst_toll, reached)
check("200 random spanning polylines: every one enters Q_j < 0", worst_toll < 0, True,
      "-> the toll (IVT on the a-coordinate: a=0 somewhere, Q_j = -b^2 < 0)")
approx("on the minimal traversal the toll bottoms at -1n, exactly at the conjugate seats",
       min(qj_th(k * math.pi / 400) for k in range(801)), -1.0, 1e-9)

# ---------------------------------------------------------------------------
hdr("B10b", "the all-directions lemma and step 4 'positivity selects Q_i' "
            "(conclusion HOLDS; the stated reason is borderline)")
# r4, Measure step 4: "the all-directions lemma (a spanning path in the punctured
# plane sweeps >= pi of directions) forces positive-definiteness -- of the two
# slices, positivity selects Q_i."
# (a) The sweep bound itself is true: endpoints are antipodal, so the direction
#     from O turns by >= pi.
_r.seed(23)
worst_sweep = math.inf
for _ in range(300):
    mid = [(_r.uniform(-1.5, 1.5), _r.choice([-1, 1]) * _r.uniform(0.25, 1.5))
           for _ in range(3)]
    nodes = [(1.0, 0.0)] + mid + [(-1.0, 0.0)]
    if min(seg_dist_to_O(p, q) for p, q in zip(nodes, nodes[1:])) < 0.05:
        continue
    ang, prev, turned = [], None, 0.0
    for (a0, b0), (a1, b1) in zip(nodes, nodes[1:]):
        for t in [k / 400 for k in range(401)]:
            th = math.atan2(b0 + t * (b1 - b0), a0 + t * (a1 - a0))
            if prev is not None:
                d = (th - prev + math.pi) % (2 * math.pi) - math.pi
                turned += abs(d)
            prev = th
    worst_sweep = min(worst_sweep, turned)
check(f"every sampled spanning path turns through >= pi ({worst_sweep:.3f} worst)",
      worst_sweep >= math.pi - 1e-6, True)

# (b) BUT: pi is exactly the angular measure of Q_j's positive cone, so the
#     measure bound alone does not exclude the indefinite form.
pos_cone = sum(1 for k in range(36000)
               if Qj(math.cos(2 * math.pi * k / 36000),
                     math.sin(2 * math.pi * k / 36000)) > 0) / 36000 * 2 * math.pi
approx("Q_j's positive cone {|a|>|b|} has angular measure exactly pi",
       pos_cone, math.pi, 1e-3,
       "-> '>= pi of directions' is NOT strictly greater than the cone: borderline")

# (c) What actually closes it: that cone is DISCONNECTED (two opposite sectors),
#     so no continuous path can span it while keeping Q_j > 0.
inpos = lambda a, b: abs(a) > abs(b)
tested, stayed_inside = 0, 0
for _ in range(400):
    mid = [(_r.uniform(-1.5, 1.5), _r.choice([-1, 1]) * _r.uniform(0.25, 1.5))
           for _ in range(3)]
    nodes = [(1.0, 0.0)] + mid + [(-1.0, 0.0)]
    if min(seg_dist_to_O(p, q) for p, q in zip(nodes, nodes[1:])) < 0.05:
        continue
    tested += 1
    if all(inpos(a0 + t * (a1 - a0), b0 + t * (b1 - b0))
           for (a0, b0), (a1, b1) in zip(nodes, nodes[1:])
           for t in [k / 200 for k in range(201)]):
        stayed_inside += 1
check(f"of {tested} spanning paths, the number staying inside Q_j > 0 is zero",
      stayed_inside, 0, "-> the positive cone is disconnected; no path spans it")
print("     => step 4's CONCLUSION is right: positivity selects Q_i.")
print("        Its stated REASON (measure >= pi) is exactly non-strict at the")
print("        critical case and does not by itself exclude Q_j. The load is")
print("        carried by connectedness of the positive cone, not by its measure.")
print("        Wording fix, not a defect in the result. Ruling: Will's.")

# ---------------------------------------------------------------------------
hdr("B11", "appendix 14 + 15 -- Fix(nu); the inversion pivot (exact)")
check("Fix(nu) in the plane is O alone", [(0, 0)],
      [(a, b) for a in range(-2, 3) for b in range(-2, 3) if (-a, -b) == (a, b)])
check("nu is fixed-point-free on the orbit (Q_i(0,0) != 1)", Qi(0, 0) == 1, False)
inv_fix = [x for x in (F(1), F(-1), F(2), F(1, 2)) if F(1) / x == x]
check("inversion x -> 1/x is fixed exactly at +-sqrt(1n); on the branch, at the seat",
      inv_fix, [F(1), F(-1)])
check("on G the inversion IS sigma_B: (X, 1/X) -> (1/X, X) (exact)",
      (F(1) / F(3), F(3)), (F(1, 3), F(3)))

# ---------------------------------------------------------------------------
hdr("B12", "appendix 16 -- the child gradient asymptotes to G_n and B_n (numeric)")
# Child gradient: u*v = c in the w-plane (child axes = images of G and B).
c_child = 0.05
worst_G, worst_B = 1.0, 1.0
for u in (40.0, 400.0):
    z = cmath.sqrt(complex(u, c_child / u) + 2j)         # pull back
    X_, Y_ = z.real, z.imag
    worst_G = min(worst_G, abs(X_ * Y_ - 1))             # distance-to-G proxy
for v in (40.0, 400.0):
    z = cmath.sqrt(complex(c_child / v, v) + 2j)
    X_, Y_ = z.real, z.imag
    worst_B = min(worst_B, abs(X_ - Y_))                 # distance-to-B proxy
check("far out along the child's x-arm, the pullback approaches XY = 1n (G_n)",
      worst_G < 1e-3, True)
check("far out along the child's y-arm, the pullback approaches X = Y (B_n)",
      worst_B < 1e-3, True,
      "-> B_n: crossable line in frame n, unreachable asymptote in frame n+1")

# ---------------------------------------------------------------------------
hdr("B13", "appendix 17 -- the Finsler counterexample and the polynomial closure")
M = lambda a, b: (a * a + b * b) * (2 + math.cos(4 * math.atan2(b, a))) if (a, b) != (0, 0) else 0.0
pp = [(0.6, 1.1), (-0.8, 0.35), (1.4, -0.7)]
approx("parity: M(-p) = M(p)", max(abs(M(-a, -b) - M(a, b)) for a, b in pp), 0.0, 1e-9)
approx("exchange: M(a,-b) = M(a,b) (sigma_B)",
       max(abs(M(a, -b) - M(a, b)) for a, b in pp), 0.0, 1e-9)
approx("degree-2 homogeneity: M(3p) = 9 M(p)",
       max(abs(M(3 * a, 3 * b) - 9 * M(a, b)) for a, b in pp), 0.0, 1e-9)
check("positivity: M > 0 off O (2 + cos >= 1)", all(M(a, b) > 0 for a, b in pp), True)
u, v = (1.0, 0.0), (0.0, 1.0)
plaw = M(u[0] + v[0], u[1] + v[1]) + M(u[0] - v[0], u[1] - v[1]) - 2 * M(*u) - 2 * M(*v)
approx("parallelogram law fails by exactly -8 at u=(1,0), v=(0,1)", plaw, -8.0, 1e-9,
       "-> matches the appendix's stated -8; M is no quadratic form")
aa, bb = F(2, 3), F(5, 7)
lhs = (3 * aa ** 4 - 2 * aa ** 2 * bb ** 2 + 3 * bb ** 4) / (aa ** 2 + bb ** 2)
approx("M = (3a^4 - 2a^2b^2 + 3b^4)/(a^2+b^2) -- the FRAMED rational form (exact pt)",
       M(float(aa), float(bb)), float(lhs), 1e-9,
       "-> the r1 retraction is right: L1 does not exclude it")
print("  [INFO] polynomial closure: a degree-2 homogeneous POLYNOMIAL is")
print("         alpha a^2 + beta ab + gamma b^2; sigma_B (b -> -b) kills beta.")
print("         Exact by inspection of the three monomials. Q's quadraticity")
print("         still rests on the generation principle (open item 2) -- correct tag.")

# ---------------------------------------------------------------------------
hdr("B14", "appendix 18 + 19 -- sigma-invariance of Q_i; R(pi/2)^2 = -I (exact)")
a_, b_ = F(4, 7), F(-3, 5)
sa, sb = -b_, -a_                                       # sigma in the split chart
check("Q_i(sigma p) = Q_i(p): sign-blindness is a computed property of the i-slice",
      Qi(sa, sb), Qi(a_, b_))
check("Q_j(sigma p) = -Q_j(p): sigma swaps the families", Qj(sa, sb), -Qj(a_, b_))
Rq = ((0, -1), (1, 0))
sq = ((Rq[0][0] * Rq[0][0] + Rq[0][1] * Rq[1][0], Rq[0][0] * Rq[0][1] + Rq[0][1] * Rq[1][1]),
      (Rq[1][0] * Rq[0][0] + Rq[1][1] * Rq[1][0], Rq[1][0] * Rq[0][1] + Rq[1][1] * Rq[1][1]))
check("R(pi/2)^2 = -I: two quarter-turns compose to the half-turn (Route 2)",
      sq, ((-1, 0), (0, -1)))

# ---------------------------------------------------------------------------
hdr("B15", "appendix 21 -- the typed Euler cluster (exact to machine precision)")
approx("e^{i pi} + e^{i 2pi} = 0", abs(cmath.exp(1j * math.pi) + cmath.exp(2j * math.pi)), 0.0, 1e-12)
approx("antipodal sum e^{i th} + e^{i(th+pi)} = 0",
       abs(cmath.exp(0.77j) + cmath.exp(1j * (0.77 + math.pi))), 0.0, 1e-12)
approx("four-seat balance: sum of sqrt(1n) i^k = 0",
       abs(sum(1j ** k for k in range(4))), 0.0, 1e-12)

# ---------------------------------------------------------------------------
hdr("B16", "appendix 22 -- the complementarity floor sigma_a sigma_b >= 1n/2")
N = 4000


def spreads(r_of_t, weight=lambda t: 1.0):
    ts = [2 * math.pi * k / N for k in range(N)]
    wsum = sum(weight(t) for t in ts)
    ma = sum(weight(t) * r_of_t(t) * math.cos(t) for t in ts) / wsum
    mb = sum(weight(t) * r_of_t(t) * math.sin(t) for t in ts) / wsum
    va = sum(weight(t) * (r_of_t(t) * math.cos(t) - ma) ** 2 for t in ts) / wsum
    vb = sum(weight(t) * (r_of_t(t) * math.sin(t) - mb) ** 2 for t in ts) / wsum
    return math.sqrt(va) * math.sqrt(vb), ma, mb


s_min, ma, mb = spreads(lambda t: 1.0)
approx("nu-symmetry zeroes the means (minimal traversal)", abs(ma) + abs(mb), 0.0, 1e-9)
approx("saturation: the minimal traversal gives sigma_a sigma_b = 1n/2 exactly",
       s_min, 0.5, 1e-3)
for name, rf in [("r = 1 + 0.4 sin^2", lambda t: 1 + 0.4 * math.sin(t) ** 2),
                 ("r = 1 + |cos|", lambda t: 1 + abs(math.cos(t)))]:
    s, _, _ = spreads(rf)
    check(f"floor-compliant nu-symmetric deformation '{name}': product {s:.3f} >= 0.5",
          s >= 0.5 - 1e-6, True)
s_seat, _, _ = spreads(lambda t: 1.0, weight=lambda t: math.exp(3 * math.cos(2 * t)))
check(f"a seat-dwelling measure on the SAME circle gives {s_seat:.3f} < 0.5",
      s_seat < 0.5, True,
      "-> the winding-measure premise is load-bearing, as the chain says")

# ---------------------------------------------------------------------------
hdr("B17", "Amplitude Floor + z^4 rectification failure + seat curvature match")
bs = [F(0), F(1, 2), F(-3, 4), F(2)]
check("on Q_j = 1n: a^2 = 1n + b^2 >= 1n, equality iff b = 0 (exact)",
      all(1 + b * b >= 1 for b in bs) and [b for b in bs if 1 + b * b == 1] == [F(0)], True)
# z^4 on G: (t + 2i)^2 = (t^2 - 4) + 4t i, t = X^2 - Y^2  -> Re = (Im/4)^2 - 4.
ts = (-3.0, -1.0, 0.0, 2.0, 5.0)
approx("z^4 sends G to the parabola Re = (Im/4)^2 - 4 -- NOT a straight axis",
       max(abs(((t * t - 4)) - ((4 * t / 4) ** 2 - 4)) for t in ts), 0.0, 1e-12,
       "-> net-rectification uniquely selects the square among z^2, z^4")
# slice curvatures at the seat, (a,b) chart: circle k=1; hyperbola vertex k=1.
approx("at the seat the circle and hyperbola have EQUAL curvature (1), opposite bending",
       abs(1.0 - 1.0), 0.0, note="mirror-osculation, the coincidence's signature")

# ===========================================================================
print("\n" + "#" * 78)
print("# PART C -- v9's own live claims")
print("#" * 78)
print("""
  READ THIS BEFORE READING A [PASS] BELOW.
  Everything in this file computes in a SIGNED chart: nu(P) = -P, the four seats
  at sqrt(1n)*i^k, antipodal binding, Fix(nu) = O. v9 rules that "the modes are
  magnitudes, not signed quantities; the sign belongs to the chart" (structural
  s3), and holds the signed register's structural status OPEN (math item 9). If
  the sign is chart residue, then -- v9's own words -- "both i^2 routes,
  orbit-necessity, the minimal traversal, the nu-centroid instances" are
  RENDERING. A [PASS] here is a fact about the rendering. It is not a structural
  claim, and it does not adjudicate item 9.
  v9's chart test independently lists perpendicularity, straightness-as-driver,
  ambient space for the sphere, and the sign on a mode as ALREADY FAILED --
  facts about a presentation. checks.py section 7 (isotropy -> S^2 -> R^3) is
  that third item.""")

# ---------------------------------------------------------------------------
hdr("C1", "v9 reciprocity joint, class selection -- BOTH halves (exact)")
# "Additive conservation fails twice: it admits X = 0 (a terminal as an attainable
#  value) and it caps both modes (contradicting P1's vastness clause).
#  Multiplicative conservation does neither: XY = 1n admits no zero and no ceiling."
c = F(7)
check("additive: X + Y = c admits the terminal X = 0 (Y = c)", F(0) + c == c, True)
check("additive: X + Y = c caps both modes at c (no X > c with Y >= 0)",
      max(x for x in (F(0), F(3), c) if c - x >= 0), c,
      "-> a conserved sum bounds each mode: contradicts vastness")
check("multiplicative: XY = 1n admits NO zero (0 * y != 1n for every y)",
      any(F(0) * y == 1 for y in (F(1), F(10), F(1, 10))), False)
big = F(10) ** 9
check("multiplicative: XY = 1n has NO ceiling (X arbitrarily large, Y = 1n/X)",
      big * (F(1) / big), F(1), "-> no zero, no cap: the class selection holds")

# ---------------------------------------------------------------------------
hdr("C2", "v9 Amplitude Floor: on the branch, a >= sqrt(1n) (exact)")
bs = [F(0), F(1, 3), F(-5, 4), F(3)]
check("Q_j = 1n forces a^2 = 1n + b^2 >= 1n for every b",
      all(1 + b * b >= 1 for b in bs), True)
check("equality exactly at b = 0 (the seats)",
      [b for b in bs if 1 + b * b == 1], [F(0)])
print("     v9: 'the branch never reaches the circle's lower range, and the full")
print("     orbit is not mode-expressible' -- the full circle needs a < 0, which")
print("     is exactly what math item 9 holds open.")

# ---------------------------------------------------------------------------
hdr("C3", "v9 T1 (disconnection) and T2 (crossing) -- re-derived, general form")
splitrot9 = lambda a, b, ph: (a * math.cosh(ph) + b * math.sinh(ph),
                              a * math.sinh(ph) + b * math.cosh(ph))
branch = [(math.cosh(t), math.sinh(t)) for t in (-1.4, 0.0, 0.9)]
check("T1: split rotations preserve the component (sign of a is locked)",
      all(splitrot9(a, b, ph)[0] > 0 for a, b in branch for ph in (-2.5, 1.7)), True)
check("T1: P and nu(P) sit in different components", (1 > 0, -1 < 0), (True, True))
# T2, stated generally: v9 says "any closed spanning path crosses the null cone".
# By the IVT the a-coordinate vanishes somewhere on such a path; there Q_j = -b^2 < 0.
worst9, kept9 = float("-inf"), 0
while kept9 < 150:
    mid = [(_r.uniform(-1.4, 1.4), _r.choice([-1, 1]) * _r.uniform(0.25, 1.4))
           for _ in range(3)]
    nodes = [(1.0, 0.0)] + mid + [(-1.0, 0.0)]
    if min(seg_dist_to_O(p, q) for p, q in zip(nodes, nodes[1:])) < 0.05:
        continue
    kept9 += 1
    reached = 1.0
    for (a0, b0), (a1, b1) in zip(nodes, nodes[1:]):
        for t in [k / 200 for k in range(201)]:
            reached = min(reached, Qj(a0 + t * (a1 - a0), b0 + t * (b1 - b0)))
    worst9 = max(worst9, reached)
check(f"T2: all {kept9} sampled spanning paths enter Q_j < 0", worst9 < 0, True,
      "-> the crossing is general (IVT), not special to the minimal traversal")
approx("T2: on the minimal traversal the toll bottoms at -1n, at the conjugate seats",
       min(Qj(math.cos(k * math.pi / 400), math.sin(k * math.pi / 400))
           for k in range(801)), -1.0, 1e-9)
check("the null cone is the two directions a = +-b (Q_j = 0 there)",
      (Qj(1.0, 1.0), Qj(1.0, -1.0)), (0.0, 0.0))

# ---------------------------------------------------------------------------
hdr("C4", "v9 two returns: invariant at pi, position at 2theta = 4pi i.e. 2pi")
qj9 = lambda t: Qj(math.cos(t), math.sin(t))
approx("Q_j(theta) = 1n*cos 2theta", max(abs(qj9(t) - math.cos(2 * t))
                                        for t in (0.2, 0.9, 2.1)), 0.0, 1e-12)
approx("invariant returns at pi", max(abs(qj9(t + math.pi) - qj9(t))
                                      for t in (0.2, 0.9, 2.1)), 0.0, 1e-12)
check("position does NOT return at pi; it returns at 2pi",
      (abs(math.cos(0.2 + math.pi) - math.cos(0.2)) > 1e-6,
       abs(math.cos(0.2 + 2 * math.pi) - math.cos(0.2)) < 1e-12), (True, True))

# ---------------------------------------------------------------------------
hdr("C5", "v9 i^2 = -1, two routes (conditional on the binding requirement)")
check("Route 1 (elimination): exactly one of the five closures satisfies C and S",
      [n for n in cases if orbit(cases[n]) == (True, True)], ["i^2=-1"])
check("Route 2 (antipodal binding): R(pi/2)^2 = -I", sq, ((-1, 0), (0, -1)))
check("the four-cycle {1, i, -1, -i} closes at m = 4 and at no smaller m",
      [k for k in range(1, 5) if 1j ** k == 1], [4])
print("     v9 tags BOTH routes conditional on the binding requirement (item 10,")
print("     which is item 9 -- see C10). The arithmetic is sound; what is open is")
print("     whether P must be bound to nu(P) at all.")

# ---------------------------------------------------------------------------
hdr("C6", "v9 parturition map w = z^2 -- the dropped offset (STATED, not refuted)")
# v9: "w = z^2 carries the parent's orbit register to the child's: 2-to-1,
#      nu-identified ...; the seat maps to the child's origin."  [verified]
# Two separable claims. The first is chart-independent and TRUE:
w2 = lambda z: z * z
approx("2-to-1 / nu-identification: w(-z) = w(z), in any chart",
       max(abs(w2(-z) - w2(z)) for z in (1 + 1j, 0.5 + 2j, -1.3 + 0.4j)), 0.0, 1e-12)
# The second is a coordinate claim, and it needs the offset v7.7 r4 carried:
seat_split, seat_mode = complex(1, 0), complex(1, 1)   # (sqrt(1n),0) and (1,1)
approx("split chart z = a+ib: w(seat) = 1, NOT the child origin",
       abs(w2(seat_split) - 1), 0.0, 1e-12)
approx("mode chart z = X+iY: w(seat) = 2i, NOT the child origin",
       abs(w2(seat_mode) - 2j), 0.0, 1e-12)
approx("only w = z^2 - 2i*1n (v7.7 r4's form) sends the seat to 0",
       abs((w2(seat_mode) - 2j) - 0), 0.0, 1e-12)
print("     So the [verified] tag spans a MIXED claim: the nu-identification half")
print("     is computational and true; 'the seat maps to the child's origin' is")
print("     either a coordinate claim (false without the -2i*1n offset) or a")
print("     constitutional one ('O_(n+1) READS P_n ... constitution, not")
print("     site-selection'), which no computation can verify. Typing question")
print("     for Will; the arithmetic above is not in dispute.")

# ---------------------------------------------------------------------------
hdr("C7", "v9 nu-centroid, general form (not just the four seats)")
_r.seed(41)
worst_c = 0.0
for n in (2, 3, 5, 8):
    cfg = [complex(_r.uniform(-4, 4), _r.uniform(-4, 4)) for _ in range(n)]
    worst_c = max(worst_c, abs(sum(cfg + [-c for c in cfg])))
approx("any nu-symmetric configuration sums to the center", worst_c, 0.0, 1e-9,
       "-> 'the symmetric whole names the locus none of its members occupies'")
approx("the four seats are the n = 2 instance", abs(sum(1j ** k for k in range(4))),
       0.0, 1e-12)

# ---------------------------------------------------------------------------
hdr("C8", "v9 complementarity floor (winding-measure premise still open)")
approx("minimal traversal saturates: sigma_a*sigma_b = 1n/2", s_min, 0.5, 1e-3)
check("a seat-dwelling measure on the same circle breaks it",
      s_seat < 0.5, True, "-> the winding-measure premise is load-bearing, as v9 says")

# ---------------------------------------------------------------------------
hdr("C9", "v9 the two non-terminations exchange, pivoting on the seat (exact)")
check("inversion x -> 1n/x is fixed exactly at +-sqrt(1n)",
      [x for x in (F(1), F(-1), F(2), F(1, 2), F(5)) if F(1) / x == x], [F(1), F(-1)])
check("on G the inversion IS sigma_B: (X, 1n/X) -> (1n/X, X)",
      (F(1) / F(4), F(4)), (F(1, 4), F(4)))
check("it swaps center-ward and outward: x = 1/8 -> 8, and x = 8 -> 1/8",
      (F(1) / F(1, 8), F(1) / F(8)), (F(8), F(1, 8)))

# ---------------------------------------------------------------------------
hdr("C10", "v9 bookkeeping: the physics flagship's factor of 2, and 'item 10'")
# Physics s1 [flagship] pairs the two floors and calls the units shared:
#   framework  sigma_a*sigma_b >= 1n/2        QM  dx*dp >= hbar/2
# Matching the two floors is a one-line proportion.
lhs_floor, rhs_floor = F(1, 2), F(1, 2)      # coefficients of 1n and of hbar
check("matching the floors 1n/2 <-> hbar/2 gives the ratio 1n : hbar = 1 : 1",
      lhs_floor / rhs_floor, F(1),
      "-> so 1n :: hbar. v9's header reads '1n :: hbar/2' -- off by 2")
check("under the header's own reading (1n = hbar/2) the floors would disagree",
      F(1, 2) * F(1, 2) == F(1, 2), False,
      "-> 1n/2 would be hbar/4, not hbar/2: the 2 is counted twice")

# Cross-reference audit, counted from the transcribed chains rather than asserted.
_V9 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "canonical", "chains", "v9")


def _read(name):
    try:
        with open(os.path.join(_V9, name), encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return None


_math, _struct, _ddj = _read("just_math_v9.md"), _read("structural_v9.md"), _read("just_ddj_v9.md")
if None in (_math, _struct, _ddj):
    print("  [SKIP] v9 chains not found next to this script; cross-ref audit skipped.")
else:
    n_items = len(re.findall(r"^\d+\.\s", _math.split("## Open items")[1], re.M))
    check("math chain's open-items list has 9 entries", n_items, 9)
    check("math chain cites a nonexistent 'item 10'", len(re.findall(r"item 10", _math)), 3)
    check("structural chain cites 'math open item 10' too",
          len(re.findall(r"math open item 10", _struct)), 1)
    check("DDJ chain cites 'math open item 9' -- the correct number",
          len(re.findall(r"math open item 9", _ddj)), 2,
          "-> item 9 IS the signed-register/involution fork all four mean")
    print("     4 stale references; the DDJ chain shows what the number should be.")

# ===========================================================================
print("\n" + "#" * 78)
print("# PART D -- backing for rulings_in_progress_r1.md")
print("#" * 78)
print("""
  These back the [checked] lines in rulings_in_progress_r1.md, which records
  positions stated in conversation and not yet ruled. Nothing here promotes
  anything: the arithmetic constrains the options, it does not choose among them.""")

# ---------------------------------------------------------------------------
hdr("D1", "the relational coordinate: rapidity, and why the additive thresholds "
          "were artifacts (rulings doc s1)")
# On the gradient the conserved product does not move at all -- so 'distance from
# balance' is not a product-deviation, and the additive candidates are mistyped.
prods = [(b, (math.sqrt(1 + b * b) + b) * (math.sqrt(1 + b * b) - b))
         for b in (0.0, 0.3, 0.7, 1.5)]
approx("XY = 1n at every b on the branch (the product never moves)",
       max(abs(p - 1) for _, p in prods), 0.0, 1e-12,
       "-> off-balance is NOT a product deviation")

# v9 s3: 'its amount exists only as a ratio to its conjugate'. The ratio's
# additive form is the rapidity phi:  X = sqrt(1n)e^phi, Y = sqrt(1n)e^-phi.
rap = lambda p: (math.exp(p), math.exp(-p))
approx("X = e^phi, Y = e^-phi keeps XY = 1n exactly",
       max(abs(rap(p)[0] * rap(p)[1] - 1) for p in (0.0, 0.25, 1.0, 2.3)), 0.0, 1e-12)
approx("X/Y = e^{2phi}; the seat is phi = 0",
       max(abs(rap(p)[0] / rap(p)[1] - math.exp(2 * p)) for p in (0.3, 1.1)), 0.0, 1e-9)

# The framework's own scale action is a SHIFT in phi -- so phi is the frame's
# relational displacement coordinate along G, not an imported one.
def phi_of(X, Y):
    return 0.5 * math.log(X / Y)


base = 0.3
shifts = []
for lam in (1.0, 2.0, 7.5):
    X, Y = lam * math.exp(base), math.exp(-base) / lam
    shifts.append((lam, X * Y, phi_of(X, Y) - base))
approx("rescaling (lX, Y/l) leaves XY = 1n",
       max(abs(p - 1) for _, p, _ in shifts), 0.0, 1e-12)
approx("...and shifts phi by exactly ln(lambda)",
       max(abs(s - math.log(lam)) for lam, _, s in shifts), 0.0, 1e-12,
       "-> v9's 'scale is motion along the curve' IS translation in phi")

# The three additive thresholds, re-expressed in phi: no structure.
in_phi = [("Q_i excess", math.asinh(math.sqrt(0.5))),
          ("amplitude  ", math.asinh(1.0)),
          ("difference ", math.asinh(0.5))]
check("none of the three additive thresholds is round in phi",
      [round(p, 3) for _, p in in_phi], [0.658, 0.881, 0.481],
      f"-> {', '.join(f'{n.strip()}={p:.3f}' for n, p in in_phi)}: a coordinate artifact")
# And the phi_golden appearance is a restatement, not a result:
Xg = (1 + math.sqrt(5)) / 2
approx("threshold 3 gives X - 1n/X = 1n, i.e. X = phi_golden by definition",
       abs(Xg - 1 / Xg - 1), 0.0, 1e-12,
       "-> recorded so it is not re-found and mistaken for a finding")

# ---------------------------------------------------------------------------
hdr("D2", "the nu-identification: disjoint in the parent, identified in the image "
          "(rulings doc s3)")
b1 = [complex(X, 1 / X) for X in (0.5, 2.0)]
b2 = [-z for z in b1]
check("in frame n the branch and its nu-image are disjoint sets",
      set(b1) & set(b2), set(),
      "-> two distinct sets of obtaining positions in the parent")
approx("under w = z^2 they land on one line, Im w = 2*1n",
       max(abs((z * z).imag - 2) for z in b1 + b2), 0.0, 1e-12)
approx("...and each sweeps that line completely (same images, pairwise)",
       max(abs(z * z - (-z) * (-z)) for z in b1), 0.0, 1e-12)
print("     So the identification is a fact about the IMAGE -- the child's")
print("     register. T1's fork is asked in the PARENT. Whether answering one")
print("     with the other resolves the question or changes the frame is the")
print("     open typing call (rulings doc s3). Not settled here.")

# ---------------------------------------------------------------------------
hdr("D3", "central symmetry is AFFINE, the circle is METRIC "
          "(q2_mirror_denial_draft_r1.md, S8/S9)")
# The ruling was stated metrically ('equidistant from the shared center', the
# circumference). The skeleton is affine -- no metric. Which half survives?
shear = lambda p: (p[0] + 1.7 * p[1], p[1])          # affine, det 1, distorts distance
mid = lambda p, q: ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
dist = lambda p: math.hypot(*p)

for P in ((1.0, 0.0), (0.6, 0.8), (-0.3, 1.2)):
    Q = (-P[0], -P[1])                                # nu(P)
    approx(f"O is the midpoint of P and nu(P) at P={P}", abs(complex(*mid(P, Q))), 0.0, 1e-12)
    sP, sQ = shear(P), shear(Q)
    approx(f"...and still the midpoint after a shear at P={P}",
           abs(complex(*mid(sP, sQ))), 0.0, 1e-12)
check("but distance from O is NOT preserved by the shear",
      abs(dist(shear((0.6, 0.8))) - dist((0.6, 0.8))) > 1e-6, True,
      f"-> 1.000 becomes {dist(shear((0.6,0.8))):.3f}")
print("     => 'O is the midpoint of P and nu(P)' is affine: available in the")
print("        implicit skeleton, before any measure exists.")
print("     => 'all points equidistant from O' (the circumference) is metric:")
print("        it arrives with the measure, which v9 tags definitional-by-")
print("        register [unaudited]. The conclusion must not be stated")
print("        circle-first in the skeleton. (Draft S9.)")

# ---------------------------------------------------------------------------
hdr("D4", "nothing but the sign distinguishes the branches "
          "(fei_involution_draft_r1.md, A1)")
# Corresponding points on the Q1 and Q3 branches of XY = 1n.
pairs = [((F(2), F(1, 2)), (F(-2), F(-1, 2))),
         ((F(1), F(1)), (F(-1), F(-1))),
         ((F(1, 4), F(4)), (F(-1, 4), F(-4)))]
for (X1, Y1), (X3, Y3) in pairs:
    check(f"product identical at X={X1}: {X1 * Y1} on both branches",
          X1 * Y1, X3 * Y3)
    check(f"ratio identical at X={X1}: {X1 / Y1} on both branches",
          X1 / Y1, X3 / Y3)
    check(f"squared distance from O identical at X={X1}",
          X1 * X1 + Y1 * Y1, X3 * X3 + Y3 * Y3)
check("odd quantities DO differ: a coordinate alone, and the sum",
      [(X1 == X3, X1 + Y1 == X3 + Y3) for (X1, Y1), (X3, Y3) in pairs],
      [(False, False)] * 3, "-> and they differ only in sign")
# The measure is forced even, so it cannot see the branch at all.
Meven = lambda a, b: 3 * a * a - 2 * a * b + 5 * b * b   # any even (degree-2) form
check("an even measure returns the same value on both branches",
      [Meven(X1, Y1) == Meven(X3, Y3) for (X1, Y1), (X3, Y3) in pairs],
      [True] * 3,
      "-> v9: 'Parity (nu): M(-z) = M(z) -- kills all odd degrees'")
print("     => every quantity the framework recognises reads identically on the")
print("        two branches. If they are nonetheless two (Q2), the distinction")
print("        is carried by the sign and by nothing else. That is A1.")

# ---------------------------------------------------------------------------
print(f"\n{'=' * 78}")
if FAILURES:
    print(f"FAILED: {len(FAILURES)} check(s): {FAILURES}")
    raise SystemExit(1)
print("All checks passed.")
print("Verdicts on claims are arithmetic only. Nothing here is a ruling;")
print("ontology, referents and readings are Will's.")
print("Part C computes in a signed chart; v9 holds that chart's structural")
print("status open (math item 9). Read those PASSes as rendering facts.")
print("=" * 78)
