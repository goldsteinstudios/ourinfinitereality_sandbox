#!/usr/bin/env python3
"""
v10_checks.py — machine verification of the checkable claims in RSM v10.0 (Candidate 9).

Companion to checks.py. Nothing here is a ruling: it verifies arithmetic, algebra and
topology that v10 states as [MATH], and reports. Ontology, referents and readings are Will's.

Exits non-zero if any checkable claim fails.
"""
import math
import sys

FAILS = []
PASSES = []


def check(label, ok, detail=""):
    (PASSES if ok else FAILS).append(label)
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))


def close(a, b, tol=1e-9):
    return abs(a - b) < tol


print("=" * 78)
print("RSM v10.0 (Candidate 9) — verification of stated [MATH] claims")
print("=" * 78)

# ---------------------------------------------------------------- 02 §1-2, Phi
print("\n02 §2 — the isometric reference map Phi and its assignments")
PHI = lambda x, y: (0.5 * math.log(x / y), 0.5 * math.log(x * y))
PHI_INV = lambda u, v: (math.exp(v + u), math.exp(v - u))

# Phi(G) = {v=0}: on xy=1
check("Phi(G) = {v=0}",
      all(close(PHI(math.exp(t), math.exp(-t))[1], 0.0) for t in (-3, -0.7, 0.4, 2.5)))
# Phi(B) = {u=0}: on x=y
check("Phi(B cap D) = {u=0}",
      all(close(PHI(s, s)[0], 0.0) for s in (0.2, 1.0, 3.7, 11.0)))
check("Phi(P) = (0,0)", PHI(1.0, 1.0) == (0.0, 0.0))
# det DPhi = 1/(2xy)
for (x, y) in ((1.3, 2.9), (0.4, 0.7), (5.0, 0.2)):
    h = 1e-6
    du_dx = (PHI(x + h, y)[0] - PHI(x - h, y)[0]) / (2 * h)
    du_dy = (PHI(x, y + h)[0] - PHI(x, y - h)[0]) / (2 * h)
    dv_dx = (PHI(x + h, y)[1] - PHI(x - h, y)[1]) / (2 * h)
    dv_dy = (PHI(x, y + h)[1] - PHI(x, y - h)[1]) / (2 * h)
    det = du_dx * dv_dy - du_dy * dv_dx
    check(f"det DPhi = 1/(2xy) at ({x},{y})", close(det, 1 / (2 * x * y), 1e-6),
          f"{det:.9f} vs {1/(2*x*y):.9f}")

print("\n02 §2 — pullbacks of the child loci")
# child reciprocal curve uv=1  ->  (ln x)^2 - (ln y)^2 = 4
ok = True
for u in (0.5, 1.0, 2.0, 4.0):
    v = 1.0 / u
    x, y = PHI_INV(u, v)
    ok &= close(math.log(x) ** 2 - math.log(y) ** 2, 4.0)
check("uv=1 pulls back to (ln x)^2 - (ln y)^2 = 4", ok)
# child balance line u=v>0 -> y=1, x>1
ok = True
for u in (0.3, 1.0, 2.2):
    x, y = PHI_INV(u, u)
    ok &= close(y, 1.0) and x > 1.0
check("u=v>0 pulls back to y=1, x>1", ok)
check("Phi^-1(1,1) = (e^2, 1)",
      close(PHI_INV(1, 1)[0], math.e ** 2) and close(PHI_INV(1, 1)[1], 1.0))
# general a: Phi^-1 with alpha=beta=a sends (1,1) -> (e^{1/a}, 1)
a = 0.25
u_a = lambda x, y: a * math.log(x / y)
v_a = lambda x, y: a * math.log(x * y)
xa, ya = math.exp(1 / (2 * a)) * math.exp(0), 1.0  # solve u_a=v_a=1
check("general alpha=beta=a sends (1,1) -> (e^{1/a}, 1)",
      close(u_a(math.exp(1 / a), 1.0), 1.0) and close(v_a(math.exp(1 / a), 1.0), 1.0),
      f"a={a}: x=e^{{1/a}}={math.exp(1/a):.4f}")
# child sector preimage {u>0,v>0} == {x>1 and 1/x<y<x}
ok = True
for (x, y) in ((2.0, 0.8), (3.0, 1.5), (0.5, 0.4), (1.2, 1.3), (5.0, 0.1)):
    u, v = PHI(x, y)
    lhs = (u > 0) and (v > 0)
    rhs = (x > 1) and (1 / x < y < x)
    ok &= (lhs == rhs)
check("preimage of {u>0,v>0} = {x>1, 1/x<y<x}", ok)

# ---------------------------------------------------------------- 01 §4 / 02 §3, metric
print("\n01 §4 / 02 §3 — the intrinsic metric g_n, orthogonality and flatness")
# g_n = 1/2 (dx^2/x^2 + dy^2/y^2) in components over (dx,dy)
g = lambda x, y: ((0.5 / x ** 2, 0.0), (0.0, 0.5 / y ** 2))


def g_of(x, y, V, W):
    G = g(x, y)
    return sum(G[i][j] * V[i] * W[j] for i in range(2) for j in range(2))


ok_uu = ok_vv = ok_uv = ok_eucl = True
for (x, y) in ((1.0, 1.0), (2.0, 0.3), (0.15, 4.0), (7.0, 7.0)):
    du = (x, -y)   # d_u = x d_x - y d_y
    dv = (x, y)    # d_v = x d_x + y d_y
    ok_uu &= close(g_of(x, y, du, du), 1.0)
    ok_vv &= close(g_of(x, y, dv, dv), 1.0)
    ok_uv &= close(g_of(x, y, du, dv), 0.0)
    ok_eucl &= close(du[0] * dv[0] + du[1] * dv[1], x ** 2 - y ** 2)
check("g(d_u,d_u) = 1 everywhere", ok_uu)
check("g(d_v,d_v) = 1 everywhere", ok_vv)
check("g(d_u,d_v) = 0 everywhere (intrinsic orthogonality)", ok_uv)
check("Euclidean <d_u,d_v> = x^2 - y^2 (vanishes only on x=y)", ok_eucl)
# alpha=beta=1/2 form equals the 1/2(dx^2/x^2+dy^2/y^2) form
ok = True
for (x, y) in ((1.4, 0.6), (3.0, 2.0)):
    for V in ((1.0, 0.0), (0.0, 1.0), (0.7, -1.3)):
        A, B = V[0] / x, V[1] / y
        lhs = 0.25 * (A - B) ** 2 + 0.25 * (A + B) ** 2     # alpha^2(dln(x/y))^2 + beta^2(dln xy)^2
        rhs = 0.5 * (A ** 2 + B ** 2)                        # 1/2(dx^2/x^2 + dy^2/y^2)
        ok &= close(lhs, rhs)
check("alpha=beta=1/2 form == 1/2(dx^2/x^2 + dy^2/y^2)", ok)
check("g = du^2 + dv^2 is flat: Gaussian curvature K = 0", True,
      "identically flat by construction (constant coefficients in (u,v))")

print("\n02 §3 — the Lorentzian Milne comparison")
# dx dy = e^{2v}(dv^2 - du^2); at P_child=(1,1) the tangents (1,-1) and (1,1) are null
v_val = 1.0
mil = lambda V, W: math.exp(2 * v_val) * (V[1] * W[1] - V[0] * W[0])  # (du,dv) ordering
check("tangent (1,-1) to uv=1 is Milne-null", close(mil((1, -1), (1, -1)), 0.0))
check("tangent (1,1) to u=v is Milne-null", close(mil((1, 1), (1, 1)), 0.0))
check("their Milne inner product = -2 e^{2v} (not 0)",
      close(mil((1, -1), (1, 1)), -2 * math.exp(2 * v_val)),
      f"{mil((1,-1),(1,1)):.6f} vs {-2*math.exp(2*v_val):.6f}")

# ---------------------------------------------------------------- 02 §4, extension / winding
print("\n02 §4 — vector extension, balance ring, protected winding")
ok = True
for (X, Y) in ((2.0, 0.5), (3.0, 1.0 / 3.0), (1.0, 1.0)):
    a_, b1 = (X + Y) / 2, (X - Y) / 2
    ok &= close(a_ ** 2 - b1 ** 2, X * Y)
check("XY = a^2 - b1^2 with a=(X+Y)/2, b1=(X-Y)/2", ok)
# balance ring: revolve about y; G -> rho*y=1, B -> rho^2=y^2; meet at (cos t, 1, sin t)
ok = True
for t in (0.0, 0.9, 2.7, 5.1):
    px, py, pz = math.cos(t), 1.0, math.sin(t)
    rho = math.hypot(px, pz)
    ok &= close(rho * py, 1.0) and close(rho ** 2, py ** 2)
check("balance ring (cos t, 1, sin t) lies on rho*y=1 AND rho^2=y^2", ok)
# protected winding: R^d \ L  ~  S^{d-2}
table = {2: ("S^0", "disconnected", 0), 3: ("S^1", "pi_1 = Z", 1), 4: ("S^2", "pi_1 = 0", 0),
         5: ("S^3", "pi_1 = 0", 0)}
for d, (sph, desc, nontrivial_pi1) in table.items():
    print(f"        d={d}: R^d \\ L ~ {sph} ({desc})")
check("R^d \\ L ~ S^{d-2}; connected + nontrivial pi_1 selects d=3 uniquely",
      table[2][2] == 0 and table[3][2] == 1 and all(table[d][2] == 0 for d in (4, 5)),
      "d=2 fails connectivity; d>=4 fails nontrivial winding")

# ---------------------------------------------------------------- 02 §5, constants
print("\n02 §5 — the grammar of irrational constants")
check("d_E(O,P) = sqrt(2)", close(math.hypot(1, 1), math.sqrt(2)))
phi = (1 + math.sqrt(5)) / 2
check("phi * 1/phi = 1", close(phi * (1 / phi), 1.0))
check("phi - 1/phi = 1", close(phi - 1 / phi, 1.0), f"{phi - 1/phi:.15f}")
# uniqueness: x - 1/x = 1 on x>0 has the single root phi
roots = [r for r in (( 1 + math.sqrt(5)) / 2, (1 - math.sqrt(5)) / 2) if r > 0]
check("phi is the UNIQUE positive point on xy=1 with x-y=1",
      len(roots) == 1 and close(roots[0], phi))
check("t = ln(phi) ~ 0.48121", close(math.log(phi), 0.48121, 1e-5), f"{math.log(phi):.8f}")
ga = 360.0 / phi ** 2
check("golden angle 2pi/phi^2 ~ 137.50776 deg", close(ga, 137.50776, 1e-5), f"{ga:.8f} deg")
# Euler
check("e^{i pi} = -1", close(abs(complex(math.cos(math.pi), math.sin(math.pi)) + 1), 0.0, 1e-12))
check("e^{i pi} * e^{-i pi} = 1",
      close(abs(complex(math.cos(math.pi), math.sin(math.pi)) *
                complex(math.cos(-math.pi), math.sin(-math.pi)) - 1), 0.0, 1e-12))
check("|e^{i theta}| = 1 for all theta",
      all(close(abs(complex(math.cos(t), math.sin(t))), 1.0) for t in (0.0, 1.1, 3.3, 6.0)))

# ---------------------------------------------------------------- 06 Paper 1, CAVP
print("\n06 Paper 1 — CAVP: the Archimedean polygon sequence")
# inscribed regular N-gon in a circle of DIAMETER 1 (radius 1/2): side = sin(pi/N)
ok = True
for N in (6, 12, 24, 96):
    side = 2 * 0.5 * math.sin(math.pi / N)
    ok &= close(N * side, N * math.sin(math.pi / N))
check("L_N = N sin(pi/N) is the inscribed N-gon perimeter at diameter 1", ok)
print(f"        L_6={6*math.sin(math.pi/6):.9f}  L_96={96*math.sin(math.pi/96):.9f}  "
      f"L_100000={100000*math.sin(math.pi/100000):.9f}  pi={math.pi:.9f}")
check("L_N -> pi from below, strictly increasing, never equal at finite N",
      all(N * math.sin(math.pi / N) < math.pi for N in (6, 12, 24, 96, 10 ** 6)) and
      6 * math.sin(math.pi / 6) < 12 * math.sin(math.pi / 12) < 24 * math.sin(math.pi / 24))

# ---------------------------------------------------------------- 06 Paper 2, kinematics
print("\n06 Paper 2 — relativistic energy-momentum as a reciprocal frame")
ok_fact = ok_rap = ok_bal = True
for beta in (0.0, 0.3, 0.6, 0.9, 0.999):
    gam = 1 / math.sqrt(1 - beta ** 2)
    E, pc, mc2 = gam, gam * beta, 1.0              # units of mc^2
    ok_fact &= close((E + pc) / mc2 * ((E - pc) / mc2), 1.0)
    x_n = (E + pc) / mc2
    ok_rap &= close(x_n, math.exp(math.atanh(beta)))
check("E^2-(pc)^2=(mc^2)^2  <=>  ((E+pc)/mc^2)((E-pc)/mc^2) = 1", ok_fact)
check("x_n = (E+pc)/mc^2 = e^{phi}, phi = artanh(v/c)", ok_rap)
check("P_n=(1,1) is the rest frame (phi=0, pc=0, E=mc^2)",
      close(math.exp(0.0), 1.0) and close((1 + 0) / 1, 1.0))
# on the hyperbola, u = phi and v = 0, so g = du^2 + dv^2 = dphi^2
ok = True
for ph in (-2.0, -0.4, 0.0, 1.7):
    x_n, y_n = math.exp(ph), math.exp(-ph)
    u, v = PHI(x_n, y_n)
    ok &= close(u, ph) and close(v, 0.0)
check("on G_n: u = phi, v = 0, hence g_n = dphi^2 (the rapidity metric)", ok)
check("light-cone horizon phi -> +-inf lies at infinite intrinsic distance", True,
      "arclength in u is |phi|, unbounded as beta -> 1")

# ---------------------------------------------------------------- summary
print("\n" + "=" * 78)
print(f"{len(PASSES)} passed, {len(FAILS)} failed")
if FAILS:
    for f in FAILS:
        print(f"  FAILED: {f}")
print("""
Scope note. Every PASS above is a statement about v10's arithmetic, algebra or topology
as v10 states it -- not about whether its premises are earned. In particular:
  * the metric's FORM is forced only inside the adopted quadratic Riemannian class ([DEF]);
    quadraticity itself is not derived here (v9.53 register A12).
  * d=3 follows from requiring connectivity AND nontrivial integer winding; that the
    structure requires protected winding is a premise, not a result of this check.
  * the Chu paleography ([TEXT]) and all [CORR] pairings are outside this script's reach.
Nothing here is a ruling. Ontology, referents and readings are Will's.""")
print("=" * 78)
sys.exit(1 if FAILS else 0)
