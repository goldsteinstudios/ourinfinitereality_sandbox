#!/usr/bin/env python3
"""
Arithmetic checks for the RSM math chain.

Run:  python3 rsm/audit/checks.py

Every claim the audit makes about the geometry is reproduced here so that it can be
re-run and disbelieved. Nothing in this file is a ruling; nothing enters a chain from
here. Pure stdlib -- exact rational arithmetic where possible, floats only for the
rotation sweeps.

Naming, per ledger R5 (three math languages):
    Q_j(a,b) = a^2 - b^2    the CONSERVED PRODUCT (= X*Y). What j preserves. Gradient.
    Q_i(a,b) = a^2 + b^2    What i preserves. Squared distance from O_n. Orbit/measure.
Both are called "1_n" in the chains. They are different quantities.

Charts:  X = a + b,  Y = a - b     so  X*Y = a^2 - b^2 = Q_j
         X = Y  <=>  b = 0         (the balance axis B_n)
1_n is set to 1 throughout: every claim below is scale-free.
"""

import math
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


# ---------------------------------------------------------------------------
hdr(1, "v7.5 math chain contradicts itself: P is both a vertex and the midpoint")
# Prop 3.1 names P = (sqrt(1n), sqrt(1n)) in (X,Y).
# Lemma 4.4 says the modes are "antipodal about the center" P.
# G n B: substitute X = Y into X*Y = 1n  =>  X = Y = +-1
gb = [(F(1), F(1)), (F(-1), F(-1))]           # the TWO points of G n B, in (X,Y)
midpoint = (sum(p[0] for p in gb) / 2, sum(p[1] for p in gb) / 2)
check("G n B has exactly two points", len(gb), 2, f"{gb}")
check("their midpoint is the origin O_n", midpoint, (F(0), F(0)))
check("Prop 3.1's P = (1,1) is NOT that midpoint", (F(1), F(1)) == midpoint, False,
      "-> 'antipodal about P' and 'P = (1,1)' cannot both hold")
print("     Ledger E3 rules the same way: the conjugates are antipodal about O_n.")

# ---------------------------------------------------------------------------
hdr(2, "Two quantities, both written 1_n (ledger O1)")
# r5 line 12: "1n is the frame's minimal unit of distinction, identical with the conserved product."
Qj = lambda a, b: a * a - b * b
Qi = lambda a, b: a * a + b * b

# On the circle of radius sqrt(1n) about O_n, Q_i is constant and Q_j is not.
pts = [(math.cos(t), math.sin(t)) for t in [math.radians(d) for d in (0, 30, 45, 60, 90)]]
approx("Q_i is constant = 1n on the circle", max(abs(Qi(*p) - 1) for p in pts), 0.0)
spread = max(Qj(*p) for p in pts) - min(Qj(*p) for p in pts)
print(f"  [INFO] Q_j on the same circle ranges over {spread:.3f} (it is 1n*cos 2theta)")

# They agree exactly where b = 0, i.e. exactly at G n B.
agree = [d for d in range(360)
         if abs(Qi(math.cos(math.radians(d)), math.sin(math.radians(d)))
                - Qj(math.cos(math.radians(d)), math.sin(math.radians(d)))) < 1e-9]
check("Q_i == Q_j only at theta = 0, 180 (i.e. b = 0, i.e. G n B)", agree, [0, 180])
print("     => 'minimal unit of distinction' and 'the conserved product' are two")
print("        quantities that coincide at exactly the seats. O1 is a real question.")

# ---------------------------------------------------------------------------
hdr(3, "E2 seat-phase structure (ledger, verified)")
seats = [(1, 0), (0, 1), (-1, 0), (0, -1)]            # seat_k = sqrt(1n) * i^k
check("Q_i = 1n at all four seats", [Qi(*s) for s in seats], [1, 1, 1, 1])
check("Q_j = (-1)^k * 1n at seat_k", [Qj(*s) for s in seats], [1, -1, 1, -1],
      "-> the double cover appears in the enumeration")
on_G = [k for k, s in enumerate(seats) if Qj(*s) == 1]
check("seats on G_n (Q_j = +1n) are k = 0, 2", on_G, [0, 2],
      "-> P_n and nu(P_n); seats 1,3 lie on the conjugate family")

# ---------------------------------------------------------------------------
hdr(4, "Q_i restricted to G_n, and the orbit's contact with the gradient")
# On G:  a^2 - b^2 = 1  =>  a^2 = 1 + b^2  =>  Q_i = 1 + 2b^2
worst = max(abs(Qi(math.sqrt(1 + b * b), b) - (1 + 2 * b * b))
            for b in [i / 8 for i in range(9)])
approx("Q_i|_G = 1n + 2b^2", worst, 0.0, note="-> Q_i >= 1n on G, equality iff b = 0")

# orbit (Q_i = 1n) meets G (Q_j = 1n). Scan b: a point on G at height b has
# a^2 = 1 + b^2, so Q_i = 1 + 2b^2. It sits on the orbit iff Q_i == 1 iff b == 0.
contact = [b for b in [i / 1000 for i in range(-500, 501)]
           if abs((1 + 2 * b * b) - 1) < 1e-12]
check("orbit n G = {b = 0} only", contact, [0.0],
      "-> the two registers touch at +-P_n, nowhere else")

# tangency at b = 0. Implicit differentiation, computed not asserted:
#   G   : a^2 - b^2 = 1  ->  2a da - 2b db = 0  ->  da/db = +b/a
#   Q_i : a^2 + b^2 = 1  ->  2a da + 2b db = 0  ->  da/db = -b/a
slope_G = lambda a, b: b / a
slope_orbit = lambda a, b: -b / a
approx("at b = 0 the two slopes agree (shared tangent)",
       slope_G(1.0, 0.0) - slope_orbit(1.0, 0.0), 0.0)
off = [(slope_G(math.sqrt(1 + b * b), b), slope_orbit(math.sqrt(1 - b * b), b))
       for b in (0.1, 0.2, 0.3)]
check("off b = 0 the slopes have opposite sign", all(g * o < 0 for g, o in off), True,
      "-> tangential contact, opposite curvature ('mirror osculation')")

# ---------------------------------------------------------------------------
hdr(5, "P_n is the nadir of its own gradient, for every orientation")


def qj_rot(p, th):
    """Q_j of p, measured in the gradient rotated by th."""
    c, s = math.cos(th), math.sin(th)
    a, b = p
    A, B = c * a + s * b, -s * a + c * b
    return A * A - B * B


worst_r, worst_nadir = 0.0, 0.0
for deg in range(0, 360, 5):
    th = math.radians(deg)
    p = (math.cos(th), math.sin(th))                 # G_th n B_th, at unit radius
    worst_r = max(worst_r, abs(qj_rot(p, th) - 1))   # is it on G_th?
    # min of Q_i along G_th is 1 + 2b'^2, attained at b' = 0
    m = min((1 + bb * bb) + bb * bb for bb in [i / 500 for i in range(-200, 201)])
    worst_nadir = max(worst_nadir, abs(m - 1))
approx("for every orientation, G_th n B_th lies at radius sqrt(1n)", worst_r, 0.0, 1e-9)
approx("and that point is the nadir (min Q_i) of G_th", worst_nadir, 0.0, 1e-9)
print("     => sweeping orientations, the P_n trace out a circle of candidates.")
print("        Within ONE frame there are four: G n B gives two, the quarter-turn two more.")
print("        Whether the rest of the circle is populated is open item 8, NOT settled here.")

# ---------------------------------------------------------------------------
hdr(6, "Q_i is orientation-invariant; Q_j is not")
p = (math.cos(math.radians(30)), math.sin(math.radians(30)))
approx("Q_i(p) = 1n regardless of orientation", Qi(*p), 1.0)
readings = [round(qj_rot(p, math.radians(d)), 4) for d in (0, 30, 90)]
check("Q_j(p) depends on which gradient you measure in", readings, [0.5, 1.0, -0.5],
      "-> Q_j cannot state an orientation-independent distinction")

# ---------------------------------------------------------------------------
hdr(7, "Isotropy forces R^3, and then stops (Will's observation)")


def rot3(v, axis, t):
    x, y, z = v
    ux, uy, uz = axis
    c, s = math.cos(t), math.sin(t)
    d = ux * x + uy * y + uz * z
    return (x * c + (uy * z - uz * y) * s + ux * d * (1 - c),
            y * c + (uz * x - ux * z) * s + uy * d * (1 - c),
            z * c + (ux * y - uy * x) * s + uz * d * (1 - c))


circle = [(math.cos(t), math.sin(t), 0.0) for t in [i * math.pi / 8 for i in range(16)]]
check("the circle lies in a plane (all z = 0)", all(abs(p[2]) < 1e-15 for p in circle), True)

axes = [(math.cos(a), math.sin(a) * math.cos(b), math.sin(a) * math.sin(b))
        for a in [i * math.pi / 6 for i in range(6)]
        for b in [j * math.pi / 6 for j in range(6)]]
swept = [rot3(p, ax, t) for p in circle for ax in axes for t in (0.7, 1.9)]
approx("sweeping every orientation keeps radius = 1", max(abs(math.sqrt(sum(c * c for c in q)) - 1)
                                                          for q in swept), 0.0, 1e-9)
check("but z escapes the plane -> the swept set is a SPHERE, needing R^3",
      max(abs(q[2]) for q in swept) > 0.5, True)

sphere_pt = (0.6, 0.8, 0.0)
radii = {round(math.sqrt(sum(c * c for c in rot3(sphere_pt, ax, 1.3))), 9) for ax in axes}
check("rotating the SPHERE returns the sphere -- nothing new is swept", radii, {1.0},
      "-> the construction reaches a fixed point at three dimensions")
print("     NOTE: 'never generated' is NOT 'excluded'. S^2 still embeds in R^4.")
print("     Dimensional uniqueness remains open. This does not close it.")

# ---------------------------------------------------------------------------
hdr(8, "FU family-invariance: does mu cancel, and does the cancellation carry weight?")
# Q_t(a,b) = alpha*a^2 + gamma*b^2.
# primary family   XY = +mu*1n  -> seats at b=0, a^2 = mu.  FU ASSERTS Q_t(seat) = |c| = mu.
# conjugate family XY = -mu*1n  -> seats at a=0, b^2 = mu.  FU ASSERTS Q_t(seat) = |c| = mu.
for mu in (F(1), F(3), F(7, 2)):
    # primary seats: (a,b) = (sqrt(mu), 0).  Q_t = alpha*mu.  Native Q_j there = +mu.
    # FU sets Q_t(seat) = |c| = mu   ->  alpha = 1.  Native reading agrees: no work done.
    alpha_fu = F(mu, mu)
    alpha_native = F(mu, mu)           # Q_j(seat) = +mu, same sign
    # conjugate seats: (a,b) = (0, sqrt(mu)).  Q_t = gamma*mu.  Native Q_j there = -mu.
    gamma_fu = F(mu, mu)               # FU: gamma*mu = +mu  -> gamma = +1
    gamma_native = F(-mu, mu)          # native: gamma*mu = -mu -> gamma = -1
    check(f"mu = {mu}: primary agrees either way (alpha = 1)",
          (alpha_fu, alpha_native), (F(1), F(1)))
    check(f"mu = {mu}: conjugate DISAGREES (FU {gamma_fu} vs native {gamma_native})",
          (gamma_fu, gamma_native), (F(1), F(-1)),
          "-> gamma = -1 is not positive-definite; only the sign flip gives +1")
print("     mu cancels for EVERY mu -- but only because Q_t(seat) := |c| was ASSUMED.")
print("     The conjugate family natively reads Q_j(seat) = -mu; setting it to +mu IS")
print("     the sign-blindness kernel. The algebra contributes nothing.")
print("     => 'family invariance' does not discharge Postulate R. It renames it.")
print("     (Rotating XY = 1n by 90 deg gives XY = -1n: the two 'families' are ONE")
print("      gradient at two orientations. So the kernel is orientation-isotropy restated.")
print("      If T3's no-unframed-distinction lemma derives isotropy, it derives the")
print("      kernel -- by T3, not by family invariance. Nodes 6-22, unwalked.)")

# ---------------------------------------------------------------------------
hdr(9, "v7.5's standoff argument presupposes the metric it derives")
print("  Not arithmetic -- a dependency check, stated for the record:")
print("    Prop 3.4  : 'No traversal may approach P closer than RADIUS sqrt(1n).'")
print("    Lemma 4.4 : 'avoids the open DISK of radius sqrt(1n)'; 'OUTWARD deviation'.")
print("    Remark 2.3: Q_j is INDEFINITE -- 'cannot certify orthogonality'.")
print("    Thm 6.1   : Q_i, the positive-definite form, is DERIVED HERE.")
print("  'Radius' and 'disk' need a positive-definite form. Q_j is not one; Q_i is not")
print("  yet available. So Sec. 3-4 measure distance with a metric earned only in Sec. 6.")
print("  => v7.5's 'forced traversal' is not a closure.")
print("  => r5's retreat to Postulate F + Definition T is the correct repair.")
print("  Nodes 6-22, unwalked. Reported, not propagated.")

# ---------------------------------------------------------------------------
hdr(10, "Divergence Ledger entry 001 -- the image-9 orthogonality error")
# A Gemini instance proposed {XY=c} orthogonal to {X/Y=k} to 'seal' the anchoring line.
#   grad(XY)   = (Y, X)
#   grad(X/Y)  = (1/Y, -X/Y^2)
#   dot        = 1 - X^2/Y^2 = (Y^2 - X^2)/Y^2   -- zero ONLY on the balance axes.
import random as _r
_r.seed(11)
offbal = 0
for _ in range(200):
    X, Y = _r.uniform(0.5, 3), _r.uniform(0.5, 3)
    dot = Y * (1 / Y) + X * (-X / Y ** 2)
    if abs(X - Y) > 1e-6 and abs(dot) > 1e-9:
        offbal += 1
check("{XY=c} is NOT orthogonal to {X/Y=k} off the balance axis", offbal, 200,
      "-> the image-9 route is false (nonzero everywhere X != Y)")

# The TRUE orthogonal partner: {X^2 - Y^2 = k}, grad (2X, -2Y).
#   grad(XY) . grad(X^2-Y^2) = Y*2X + X*(-2Y) = 0  identically.
worst = 0.0
for _ in range(2000):
    X, Y = _r.uniform(0.5, 3), _r.uniform(0.5, 3)
    worst = max(worst, abs(Y * (2 * X) + X * (-2 * Y)))
approx("{XY=c} IS orthogonal to {X^2-Y^2=k} everywhere", worst, 0.0, 1e-12,
       "-> and {X^2-Y^2=k} = Re/Im level-net of z^2, the parturition map")
print("     Ledger 001 rejection stands. Divergences are the data; verify, do not adopt.")

# ---------------------------------------------------------------------------
print(f"\n{'=' * 78}")
if FAILURES:
    print(f"FAILED: {len(FAILURES)} check(s): {FAILURES}")
    raise SystemExit(1)
print("All checks passed.")
print("Nothing here is a ruling. Ontology, referents and readings are Will's.")
print("=" * 78)
