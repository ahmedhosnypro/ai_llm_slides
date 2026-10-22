# AGENTS.md — machine-learning lecture 02: Linear Regression & Classification (MSSE)

Namespace: `videos/machine-learning/02_linear-regression-classification-MSSE/`
39 founder-curated unique slides (`unique_slides/slide_001.jpg` … `slide_039.jpg`,
numbered densely by the founder 2026-10-13; frames are 960×540, 1px = 1pt).
**Founder approved the frame set 2026-10-13** (message to the coordinator, together
with the dependency graph below) — the 2026-10-10 HARD STOP is lifted for this set.
Approval record: `REVIEW_APPROVED.md`.

## House chrome — THIS deck (measured 2026-10-13; overrides 17_worker_instructions.md's ml-intro values)

Every recreated slide uses the SAME outer template, taken from the reference frame
`unique_slides/slide_003.jpg` and verified constant across the parent slides
(001/004/009/018/025/028/031). This is the deep-learning DSAI 308 template FAMILY,
but the geometry differs from the DL playlist's ratified values — use THESE:

- Slide `LAYOUT_WIDE` 13.33 × 7.5 in; canvas `FFFFFF`.
- Gray panel `E9E9E7`: rect at x 61px, y 46px, w 839px, h to the slide bottom
  (540px); thin red `C00000` border 1pt on left/right/top; the red bottom stroke
  renders at rows 538–539, half-visible at the slide edge.
- Badge: circle d≈35px centered (876, 73)px — fill `FDFD96`, purple ring `6A5ACD`
  ~2pt, bold numeral `333333` (Arial 18pt). **Numeral = the number printed on the
  ORIGINAL slide image** = the file number N (no zero-padding).
- Runnable module + checker: `shared_patterns/house_chrome.js`
  (`drawHouseChrome(pptx, slide, {numeral})`) and `shared_patterns/house_chrome_check.py`
  — run the checker on every 150dpi render BEFORE judging; FAIL = fix first.
- Title band: content-slide title ink starts at y≈60–62px (measure your slide; the
  frame is ground truth — title placement is per-slide measured, unlike ml-intro's
  pinned y0.28).
- NOT the ml-intro chrome (E8E8E8 / 0.15in C00000 frame / outline-less FFF9C4 badge),
  and NOT the DL playlist's geometry (panel x42..918, badge (893,71) d36). The
  GROUND RULES clause in judge prompts must describe THESE values.

## Slide dependency graph (founder-supplied 2026-10-13 — canonical, also in slide_dependencies.json)

Edges (child → parent; child builds on the parent's certified composition):

- `5 > 4`
- `10 > 9`
- `11 > 9` — a component shares position AND size with slide 9's (stronger
  similarity than a normal child; careful: inherit 9's component, draw the delta)
- `12 > 11` — same kind of dependency on 11 as 11 has on 9 (chain 9→11→12)
- `13 > 12` — inherits 12's axis component RESIZED smaller and repositioned to the
  top-left of the frame
- `14, 15, 16` — parallel roots that share ONE OMML equation component (bank the
  shared equation asset ONCE under `recreated_pptx/build/assets/` with a shared
  name; siblings md5-verify and reuse — never re-derive per slide)
- `19 > 18`
- `24 > 23`
- `26 > 25`
- `29 > 28`
- `32 ≡ 31` — EXACT duplicate (intentional in the original deck; we follow it):
  slide 32's build = slide 31's certified component + badge numeral 32, nothing else
- `35 > 31`

Builds gate on parent certification (`gen_status='passed'` AND `visual_check='PASS'`);
children import the parent's certified component from
`recreated_pptx/build/components/slide_NNN.js` (`renderBase(pptx, slide, opts)` +
per-block exports; never copy-paste, never re-derive). Full law:
`~/.agents/skills/slide-recreation/references/dependencies.md` + the DEPENDENCY-GATED
section of `scripts/17_worker_instructions.md`.

## Deck-specific notes

- No cross-video dependencies. No web-source/SOURCES.md mandate for this deck (the
  deep-learning 001 rule does not transfer; standard scripts 12→13 pipeline).
- Old extraction state (6198 frames → 210 unique slides, opened 2026-10-12 under
  the pre-curation namespace) was replaced by the founder's curated 39 — pre-curation
  index/mapping not recoverable and not needed (no downstream artifacts ever existed).
- Equations: professional 2D format (matplotlib mathtext → 600dpi PNG → addImage at
  exact size), OMML wrap post-certification per the single-version law.
- Advanced graphs (if any slide shows fitted curves / decision plots): graphgen venv
  + topic-correct library per the advanced-graph rule; single plain-named deliverable.
