# RSM v10.0 — Mathematical Construction & The Grammar of Irrational Constants

**Candidate 9 · 26 October 2026**

## 1. Domain, Operative Restriction, and Normal Form

Use $D = (0,\infty)^2$, $G = \{xy=1\}$, $B = \{x=y\}$, and $P = (1,1)$, with completed coordinate
origin $O = (0,0) \notin D$. Operative restriction removes $P$ from $G$:
$(x,y) \in G^* \iff x>0, y>0, xy=1,$ and $x \neq y$. Parameterizing $G$ by $x = e^t, y = e^{-t}$
($t \in \mathbb{R}$) and removing $t=0$ yields $G^* = G^+ \sqcup G^-$ with no positive gap around
zero; any positive resolution floor $\delta_n > 0$ is a separate threshold assumption. The
involution $\sigma(x,y) = (y,x)$ exchanges $G^+$ and $G^-$, but no continuous path in $G^*$
connects them.

**Conditional Normal-Form Theorem:** Suppose a relation is the graph $y = g(x)$ of a continuous
strictly decreasing bijection of $(0,\infty)$ satisfying $g(g(x)) = x$. In logarithmic coordinates,
$f(t) = \ln g(e^t)$ is a decreasing involution of $\mathbb{R}$ with a unique fixed point $p$. For
any increasing homeomorphism $h_+: [p,\infty) \to [0,\infty)$, setting $h(t) = h_+(t)$ above $p$
and $h(t) = -h_+(f(t))$ below $p$ gives $h(f(t)) = -h(t)$, so $H(x) = \exp(h(\ln x))$ satisfies
$H(g(x)) = 1/H(x)$, carrying the relation to $XY = 1$.

---

## 2. Exact Isometric Transformation and Repeatability Theorem

For symmetric scale parameters $\alpha_n = \beta_n = \frac{1}{2}$, define $\Phi: D \to \mathbb{R}^2$
by:

$$ u = \frac{1}{2}\ln\frac{x}{y}, \qquad v = \frac{1}{2}\ln(xy), \qquad \det D\Phi = \frac{1}{2xy} > 0. $$

Its inverse is $x = e^{v+u}, y = e^{v-u}$, and its reference assignments are exact:

$$ \Phi(G) = \{v=0\}, \qquad \Phi(B \cap D) = \{u=0\}, \qquad \Phi(P) = (0,0). $$

**Child Sector Preimage:** The child positive sector $Q_{\mathrm{child}} = \{u>0, v>0\}$ pulls back
to the parent wedge $\{x > 1 \text{ and } 1/x < y < x\} \subset D$. Neither $G$ nor $B \cap D$ lies
in $Q_{\mathrm{child}}$; they supply its orthogonal boundary axes.

**Pullback of Child Loci:** The child reciprocal curve $uv = 1$ ($u,v > 0$) pulls back to
$(\ln x)^2 - (\ln y)^2 = 4$ within that sector. The child balance line $u = v > 0$ pulls back to
$y = 1, x > 1$, and the child balance point $P_{\mathrm{child}} = (1,1)$ pulls back to
$\Phi^{-1}(1,1) = (e^2, 1)$ (or $(e^{1/a}, 1)$ when $\frac{1}{2}$ is replaced by $a > 0$).

**Repeatability Theorem (**[MATH]**):** Given the positive reciprocal frame-form, the reference map
$\Phi$, and permission to instantiate that form in each new positive sector, applying $\Phi^{-1}$
finitely many times to any admissible positive final pair yields positive finite coordinates at
every stage, establishing consistent reference chains of arbitrary finite depth.

---

## 3. The Scale Bridge and Intrinsic Logarithmic Isometry

Under the Scale Bridge and swap symmetry, the intrinsic quadratic Riemannian metric on
$D_n = (0,\infty)^2$ is uniquely forced to be:

$$ g_n = \alpha_n^2\left(d\ln\frac{x_n}{y_n}\right)^2 + \beta_n^2\left(d\ln(x_n y_n)\right)^2 = du_{n+1}^2 + dv_{n+1}^2. $$

In the symmetric convention $\alpha_n = \beta_n = \frac{1}{2}$,
$g_n = \frac{1}{2}\left(\frac{dx_n^2}{x_n^2} + \frac{dy_n^2}{y_n^2}\right)$.

**Global Geodesic Orthogonality and Zero Curvature:** Because
$g_n = du_{n+1}^2 + dv_{n+1}^2$, its Gaussian curvature is identically $K = 0$. The coordinate
vector fields $\partial_u = x_n\partial_{x_n} - y_n\partial_{y_n}$ and
$\partial_v = x_n\partial_{x_n} + y_n\partial_{y_n}$ satisfy
$g_n(\partial_u,\partial_u) = g_n(\partial_v,\partial_v) = 1$ and
$g_n(\partial_u,\partial_v) = 0$ everywhere on $D_n$, whereas their flat Euclidean inner product is
$x_n^2 - y_n^2$ (vanishing only along $x_n = y_n$).

**Comparison with the Lorentzian Milne Metric:** Under the Lorentzian form
$dx_n\,dy_n = e^{2v}(dv^2 - du^2)$ with $T = (x_n+y_n)/2 = e^v\cosh u$ and
$Z = (x_n-y_n)/2 = e^v\sinh u$, the $u$ and $v$ axes are Lorentz-orthogonal, but at
$P_{\mathrm{child}}=(1,1)$ the tangent directions $(1,-1)$ and $(1,1)$ to $uv=1$ and $u=v$ are null
vectors with inner product $-2e^{2v} \neq 0$. Thus $g_n$, rather than $dx_n\,dy_n$, is the
canonical recursive metric.

---

## 4. Extended Distinction Space, Orientation Rings, and Protected Winding

**Vector Distinction Extension:** Setting $a = (X+Y)/2$ and $b_1 = (X-Y)/2$ gives
$XY = a^2 - b_1^2$. Extending to a vector distinction $\vec{b} = (b_1, b_2)$ with invariant
$a^2 - b_1^2 - b_2^2 = k$ and excluding only the vertex $(\sqrt{k}, 0, 0)$ on the positive-$a$
sheet permits the circular path $b_1 = r\cos\theta, b_2 = r\sin\theta, a = \sqrt{k+r^2}$ ($r>0$),
which continuously reverses the sign of $b_1$ while keeping $|\vec{b}| = r > 0$.

**Circle of Orientations:** Defining $E_\theta(u,v) = (u\cos\theta, v, u\sin\theta)$
($\theta \in S^1$) fixes the origin $E_\theta(0,0) = (0,0,0)$ and vertical axis while sweeping
$P_{\mathrm{child}}=(1,1)$ into the ring $(\cos\theta, 1, \sin\theta)$ and $uv=1$ into the surface
$rv = 1$ ($r = \sqrt{\xi^2+\zeta^2}$).

**Protected Winding Theorem (**[MATH]**):** For an affine line $L \subset \mathbb{R}^d$
($d \ge 2$), $\mathbb{R}^d \setminus L \cong \mathbb{R} \times (\mathbb{R}^{d-1} \setminus \{0\})
\simeq S^{d-2}$. At $d=2$ it is disconnected ($S^0$); at $d=3$ it is path-connected with
$\pi_1(S^1) \cong \mathbb{Z}$ (protected integer winding); for $d \ge 4$ it is simply connected
($\pi_1 = 0$). Connectivity plus nontrivial loop winding around an excluded affine balance line
uniquely selects $d = 3$.

---

## 5. The Implicit Grammar of Irrational Constants and Euler's Identity

Irrational and transcendental constants emerge whenever a curved, exponential, or diagonal
structural invariant (恆 / 妙) is projected onto a linear, discrete coordinate ruler (可 / 徼). Were
these constants rational fractions $p/q$, the curved or recursive invariant would lock into a
finite integer grid at scale $q$, violating ontological nonterminality ("no final inside").

**$\sqrt{2} \approx 1.41421356\dots$ (The Orthogonal Bridge / 天地):** In the normalized chart, the
Euclidean distance from the origin $O_n(0,0)$ (始) to the balance point $P_n(1,1)$ (母/玄) is
$d_E(O_n,P_n) = \sqrt{1^2+1^2} = \sqrt{2}$, and $1/\sqrt{2}$ is the orthogonal rotation factor
between mode coordinates $(x_n,y_n)$ and sum-difference coordinates $(T,Z)$. Its irrationality
proves that the balance diagonal $B_n$ ($x=y$) is incommensurable with integer steps along a single
axis.

**$e \approx 2.71828182\dots$ (Generator of Continuous Reciprocal Flow / 相生 & Φₙ):**
$e = \lim_{N\to\infty}(1+1/N)^N$ is the unique base satisfying $\frac{d}{dt}e^t = e^t$ (rate of
change equals state, realizing the Scale Bridge). It parameterizes hyperbolic exchange
$(e^t, e^{-t})$ on $G_n$, defines the isometric recursive map $\Phi_n = \frac{1}{2}\ln_e(\dots)$,
and sets the pullback $(e^2, 1)$ of the child balance point.

**$i = \sqrt{-1}$ (The Orthogonal Turn / ⊢ & 反):** Multiplication by $i = e^{i\pi/2}$ rotates a
state by $90^\circ$ out of the 1D real line into the second component of the vector distinction
$(h_1, h_2)$, converting radial exponential scaling ($e^t$) into constant-radius circular phase
($|e^{i\theta}| = 1$).

**$\pi \approx 3.14159265\dots$ (Circular Closure, Return, and Winding / 周行 & 復):** While $e$
governs the open hyperbola $xy=1$, $\pi$ governs the closed unit circle $h_1^2+h_2^2=1$ around the
excluded center: a half-turn of arc length $\pi$ executes mode-swap ($e^{i\pi} = -1$) without
passing through $(0,0)$, and a full turn of $2\pi$ returns to the identity ($e^{i2\pi} = 1$) while
incrementing the topological winding number $k \in \mathbb{Z}$.

**$\varphi = \frac{1+\sqrt{5}}{2} \approx 1.61803398\dots$ (Unit-Difference Point &
Non-Resonant Packing / 萬物):** $\varphi$ is the unique point on the positive reciprocal curve
$xy=1$ where the additive modal difference $x - y = 1$ simultaneously equals the multiplicative
frame unit $xy = 1$:

$$ \varphi \cdot \frac{1}{\varphi} = 1 \quad \text{and} \quad \varphi - \frac{1}{\varphi} = 1 \quad (t = \ln\varphi \approx 0.48121). $$

Because $\varphi = [1; 1, 1, 1, \dots]$ is the most irrational number, budding child frames spaced
around the parent's $2\pi$ balance ring by the Golden Angle
$\theta_\varphi = 2\pi/\varphi^2 \approx 137.50776^\circ$ never align radially, packing infinite
lineage without fracturing the parent frame.

**Euler's Identity ($e^{i\pi} + 1 = 0$) as the Compressed Structural Equation:** On the unit circle
$S^1$, multiplicative reciprocity holds the boundary product at unit distinction
($e^{i\pi}\cdot e^{-i\pi} = 1$), while additive vector superposition balances antipodal poles
across the unoccupied center:

$$ e^{i\pi} + 1 = 0. $$

Starting from the manifest unit 1 ($1_n$, 有), continuous exponential flow ($e$, 生) turned
orthogonally by $i$ (⊢, 反) travels through a half-turn of $\pi$ (周行) to the conjugate pole
($e^{i\pi} = -1$). Neither $+1$ nor $e^{i\pi}$ sits at zero, yet their opposition across the
diameter holds open the central void ($= 0$, 無 / 沖氣以為和).
