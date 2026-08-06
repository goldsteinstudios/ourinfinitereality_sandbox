# RSM — layer separation policy

*Governance. Standing rule, not session-specific. Upload once; applies to every filing pass.*

## The rule

Three layers. Content flows down; nothing flows up into content.

**Layer 1 — canonical chains** (`rsm/canonical/chains/…`).
Assertions only: what the framework currently holds, stated as it is held. A chain file
contains claims and their *live epistemic status* — nothing else. No change-records, no
withdrawn material, no "was X, now Y," no pending-rewrite comments, no correction dates,
no provenance archaeology. The chains already declare this ("Unresolved material lives in
the open-items register, not in the chains"); this policy is that sentence made enforceable.

**Layer 2 — editorial / staging** (`staging/editorial/…`).
Expository readings, tier three. Same discipline as Layer 1 on change-history: corrections
are applied silently, and the *corrected* text stands clean. A reading's live status —
candidate, pending facsimile, priced as pedagogy, deflation-risk noted — is content and
stays. The record that a reading was *changed*, and why, is not content and goes to Layer 3.

**Layer 3 — tracking** (`rsm/audit/…`, `reports/…`).
All change-history: registers, the divergence ledger, diff reports, correction records,
provenance, withdrawn sections, "no filed record" flags, blast-radius notes. Everything a
future maintainer needs to know *how the content got to be what it is* lives here and only here.

## The line that decides layer

The test is a single question about any caveat: **does it describe the claim's standing, or
the claim's history?**

- *Standing* → content (Layer 1 or 2). "This is a candidate." "Pending facsimile." "Priced
  as pedagogy, never evidence." "This may deflate." "Held open."
- *History* → tracking (Layer 3). "Corrected 2026-08-06." "The first draft said |0|." "This
  used to sit in canonical." "Withdrawn; see Entry 006." "Originates in register item A-n13."

Both wear the grammar of a caveat. Only history is evicted. When a line mixes both — a live
caveat with a dated change-note stapled to it — keep the standing clause, strip the history
clause, and let the tracking layer carry the history.

## Standing prohibitions in content files

- No dated correction parentheticals.
- No `WITHDRAWN` / `STRUCK` / `SUPERSEDED` blocks. The tracking layer records what was struck;
  the content file simply reads as the corrected version.
- No `<!-- pending -->` / `<!-- rewrite in session -->` comments. Pending status lives in the
  register, which the chain's own colophon already points to.
- No commit hashes, branch names, or recovery archaeology. Provenance is Layer 3.
- No register item codes (A-n13, B-n9…) inside content prose. A content file must read to a
  reader who has never seen the register.

## What a filing agent may and may not do

**May, unprompted:** move a change-record out of a content file into the correct tracking
file; add a tracking entry; verify a checkable claim and report; enumerate a blast radius.

**May not, ever:** rule; promote an item tagged OFFERED or CHECKABLE to a finding; write
rationale or history into a content file; resolve a held item; convert a reading's status
from candidate to established. Those are the author's, and they arrive as content only after
he rules them.
