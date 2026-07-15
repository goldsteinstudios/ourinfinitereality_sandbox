# The Pattern — storyboard (r1)

**Status: DRAFT FOR RULING.** The front page reconceived as a **film you scroll through** —
one continuous space, one camera, scroll as the playhead. Not panels; a single evolving scene.

**The whole arc in one breath:** the camera **pushes in** toward a center that keeps receding →
settles into an **orbit** around it → **pulls back** to find the whole world was one point inside
a larger identical one → keeps pulling back **without end**. The camera move *is* the argument.

**Visual rhyme (the craft spine):** "push in and there's always more" is planted in Shot 0 (a line
that never stops subdividing), paid off in Shot 5 (the center recedes as you approach), and
detonated in Shot 8 (the infinite zoom). Same motion, three meanings — premise, center, cosmos.

**Idiom:** line-art, currentColor, accent purple, on the calm paper background. One SVG "stage,"
pinned to the viewport (`position: sticky`), whose transform + contents are driven by scroll
progress. Narration appears as **cards** that pass through as you scroll. Vanilla JS (scroll →
progress → transform), reduced-motion falls back to the static panels we already have.

---

## SHOT LIST

**Shot 0 — COLD OPEN · the premise**
- ON SCREEN: a single horizontal line, centered in a quiet field. It begins to subdivide — ticks
  multiply, finer and finer. Camera pushes in *slightly*; the closer it gets, the more
  subdivisions appear. It never bottoms out.
- CAMERA: slow, patient push-in.
- CARD: *"If reality is truly infinite — no largest thing, no smallest…"*
- Establishes the motif: **push in, and there is always more.**

**Shot 1 — THE BET · a title card, held**
- ON SCREEN: the field stills. Everything holds.
- CAMERA: locked. A deliberate pause — the one still moment before the machine starts.
- CARD: *"Grant me this one thing. Everything after is just logic."*

**Shot 2 — THE CUT · distinction**
- ON SCREEN: a single line draws down across the field, splitting it. The two sides tint apart —
  this / not-this.
- CAMERA: locked, close.
- CARD: *"To be anything is to differ."*

**Shot 3 — THE EXTREMES · impossible ends**
- ON SCREEN: the cut opens into a gradient — a bar from one pole to the other. Both ends flare,
  then are struck through. Labels ghost in: *nothing · everything.*
- CAMERA: small pull to take in the whole bar.
- CARD: *"Perfect nothing, perfect everything — no difference left in either. You never reach the ends."*

**Shot 4 — THE WORLD ASSEMBLES · a cut brings a world** · `[RULE — geometry]`
- ON SCREEN: from the gradient, the full figure builds itself — two axes crossing, the
  conserved-product curve, the balance line, the crossing. A whole little world drawn in a
  breath.
- CAMERA: settle, centered on the new structure.
- CARD: *"One cut, and you have a world: two poles, a gradient, a center."*
- `[RULE]` The axes / gradient-curve / balance / O / P geometry is yours to rule (checks.py
  territory). This is the shot that must be *right*, not just pretty.

**Shot 5 — PUSH IN · the center recedes** · (the motif returns)
- ON SCREEN: camera pushes toward the center of that world. Rings crowd, and crowd, and crowd —
  the nearer the camera, the more rings appear between it and the middle. It never arrives.
- CAMERA: the Shot-0 push-in, now *relentless* — and it never lands.
- CARD: *"But that center is the one place that can't exist. You approach forever; the meeting never comes."*

**Shot 6 — ORBIT · circulation**
- ON SCREEN: unable to reach or cross the center, the camera's motion bends into an orbit; a point
  swings around the hollow middle. The orbit settles into a steady turn.
- CAMERA: from push-in to circling — the move itself discovers rotation.
- CARD: *"You can't rest there, can't pass through. So everything circles. The circling is the stability."*

**Shot 7 — PULL BACK · the twist**
- ON SCREEN: the camera pulls back — and the whole orbiting world we've been living in shrinks to
  a single point: the center of a *larger* world, with its own orbit, its own hollow center. A
  match cut across scale.
- CAMERA: reverse — the first pull-back, and the gut-drop moment.
- CARD: *"And that whole world? One point inside a larger one."*

**Shot 8 — INFINITE ZOOM · every frame is its own ground** · `[RULE — the hero]`
- ON SCREEN: the pull-back keeps going, and every level is the same — orbit within orbit within
  orbit, endless, in both directions. The camera can travel forever and the view never changes.
- CAMERA: the endless zoom — the climax.
- CARD: *"No smallest, no largest. Every frame is its own ground. Wherever you look from, you're in the middle. The middle is everywhere."*
- `[RULE]` The self-similar geometry + the "no privileged bottom" reading (gauge; open item #6
  stays untouched) — the hero shot; rule the look and the claim together.

**Shot 9 — LAND · name the shape**
- ON SCREEN: the zoom eases to rest on one clean frame.
- CARD (the thesis): *"Stable things persist by circulating around a center that is never met."*
- Hands off to the recognition cascade (the objects), then the DDJ reveal, then the soft door —
  those stay as they are.

---

## Build notes (after the storyboard is ruled)
- **One pinned SVG stage.** A tall scroll container; the stage is `position: sticky` and fills the
  viewport. A scroll handler maps progress (0→1) across the container to the shot timeline —
  camera scale/translate + which elements are drawn/faded. `requestAnimationFrame`-throttled.
- **Continuity is the whole point.** The center the camera pushes into (Shot 5) is the same locus
  that becomes a point of the larger world (Shot 7) — one object, transformed, never cut away.
- **Scale-safe transforms only** (scale/rotate/opacity/draw-on), as established — the infinite zoom
  is repeated scale with element recycling, not translate.
- **Reduced-motion / no-JS fallback:** the static per-beat panels already built. The film is an
  enhancement layer, never a requirement to follow the argument.
- The recognition cascade, DDJ reveal, and soft door (Shots after 9) are already drafted and ruled;
  the film is Shots 0–9 only.

## Rulings needed
1. **The shot list** — order, pacing, which beats get a shot vs. a card. (Is 10 shots right, or
   too many / too few?)
2. **Shot 4 geometry** — the "cut brings a world" figure, ruled against the structure.
3. **Shot 8** — the hero infinite-zoom: the look, and the gauge claim (no privileged bottom;
   #6 untouched).
4. **The two flagged narration cards' wording** vs. the ruled spine (they're compressions).
