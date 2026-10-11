# 002 dependency-graph audit — consolidated findings (awaiting founder rulings)

Both audits (children 2–30 and 31–60) verified every edge against the actual raws.
Nothing was modified — the graph is founder-owned. Rulings needed on:

## A. Re-anchor recommendations (MISMATCH)

| Edge today | Finding | Recommended |
|---|---|---|
| 45←28 | 45 (FFN slide) shares nothing with 28 (sin/cos clock mid-state); 45's exact base is **38's** composition (X→MHA→⊕/LN→Yout, identical labels) | **45←38** (pending 28 raw) |
| 49←26 | 26 = TI motor-encoder interface; 49 = Transformer stacked blocks — zero shared content; 49's real family is the block-diagram thread (36/45/46) | **49←36** (suspected "26" slip for "36") |
| 57←47 | 57's encoder panel = **49's** stacked-encoder composition restyled (47 is a different diagram); AGENTS.md's 47-anchor describes content lineage, not the importable composition | **57←49** (or keep 47 as content anchor — founder's call) |

## B. Missed edges (strong)

- **38←36** — 38 = 36's diagram + ⊕/LayerNorm delta. No edge into 38 today. (Also resolves 59←38 transitively if adopted.)
- **5←001:18** — 002:5 verbatim-contains 001:18's composition (both green flowcharts, callouts, architecture) but has NO edge; today's 4←001:18 grants 001:18's composition to 002:4, whose real parent is **001:15**. Likely fix: 4←001:15, add 5←001:18.
- **23←22** — identical Suggested-Positional-Encoders strips; chain 22→23→24 broken at its first link.
- **52←51** (suggested) — 52 explodes 51's decoder block into the full teaching schematic; composition redraw, founder decides edge vs pattern note.

## C. CONFIRMED (no action)

2-30 range: 8←33, 10←9, 11←001:43, 13←001:33, 17←001:43, 19←001:19, 24←23.
31-60 range: 46←45, 37←001:19 (001:18 noted as an equally good base — removals legal), 51←001:18 (content/topology).

## D. Pending raws (unverifiable yet)

15←001:43, 28←27, 28←26 (26→28 flagged **thematic-only** — founder re-look when 28's raw lands), 47←46, 48←47 (**near-total restyle — builders should NOT expect a clean component-import delta from 47**), 59←38.

## E. Image-mechanism caveat on 51

51's raw styling (Office-palette boxes) does not read as the banked Figure-1 PNG's rendering — whether the frame literally splits 001's source image into halves must be settled by PIL measurement at build time; if not literal pixels, the shared_image_sources clause (not the dependency) needs review.

## F. Badge conflict (slide 48)

Two independent raws read slide_048.jpg's printed badge as "49" (and slide_049.jpg also reads "49") — one of the two raws likely misread. Founder ruling + PIL zoom required before 48's build trusts either number. (Elevated earlier; still open.)

## G. Impact if unamended

Today's buildable already had to be trusted on 42 (fine). The mismatches would surface at build time as wrong-parent imports (the 002:45 dispatch near-miss was exactly this class). Amend before 4/45/49/57 build.

---

## FINAL AUDIT (follow-up pass — all 59 raws landed; audit complete)

**New verdicts (previously pending):**
- 15←001:43 **CONFIRMED** (clean parent+delta, consistent with siblings 11/17)
- 28←27 **CONFIRMED** (element-for-element clock-face; 5→9 words)
- 28←26 **MISMATCH (thematic-only)** — 28 shares zero compositional elements with 26 (TI industrial diagram); every element traces to 27
- 47←46 **CONFIRMED** (same old-115 build; near-total restyle — import composition then restyle, no clean component delta)
- 48←47 **CONFIRMED as lineage** (prior warning stands: near-total restyle, treat 47 as content/pattern anchor and rebuild; third raw also reads the badge as "49" — section F still open)
- 59←38 **CONFIRMED at pattern level only** (family grammar, NOT composition containment — matches AGENTS.md's "don't clone"; transitive if 38←36 adopted)

**Complete founder-ruling list (supersedes prior partial list):**
1. DROP 28←26 — 28's sufficient parent is 27 (confirmed element-for-element). If the industrial→abstract narrative link matters, record as a note, not a build edge.
2. 45←28 → **45←38** (double-confirmed: identical base + annotations; 45's delta = the FFN box).
3. 49←26 → **49←36** (suspected slip).
4. 57←47 → **57←49** (or keep 47 as content anchor).
5. ADD 38←36 (strong).
6. ADD 5←001:18; fix 4←001:18 → 4←001:15.
7. ADD 23←22 (unbroken chain 22→23→24).
8. 52←51 — edge vs pattern note (founder's call).
9. 48 badge ("49" printed per three raws) — PIL zoom + ruling before 48 builds.
10. 51 image-mechanism — PIL at build time.

CONFIRMED overall: 8←33, 10←9, 11←001:43, 13←001:33, 15←001:43, 17←001:43, 19←001:19, 24←23, 37←001:19, 46←45, 51←001:18 (topology; caveat E), 47←46, 48←47 (lineage), 28←27, 59←38 (pattern), 42←P3.
