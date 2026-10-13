# AGENTS.md — 002_transformers_part2 (Transformers — Part II, Deep Learning DSAI 308)

## Curation record (HARD STOP satisfied 2026-10-11)

Founder reviewed the 150 machine-extracted frames and curated them to **60 slides**:
59 real frames `slide_002..slide_060.jpg` + **slide 001 = placeholder cover** (the
cover frame is missing from the video). State of record (machine-reconstructed from
byte-exact frame matching, deterministic and verified 59/59):

- `unique_slides/slides_index.json` — 60 entries (slide 1 = `"placeholder": true`).
- `unique_slides/new2old_mapping.json` — new → old extraction slide, with the 3
  founder group splits (22+23 ← old 45, 28+29 ← old 60, 46+47 ← old 115; 001
  precedent) and 4 founder frame swaps (8, 22, 28, 46).
- `unique_slides/slides_index_old150.json` + `slides_progress_old150.db.bak` —
  pre-curation evidence (never delete).
- Frames (5440) and review packet untouched.

The HARD STOP law (root AGENTS.md) still binds every FUTURE extraction in this
playlist; for THIS frame set it is satisfied — analysis, validation, and gated
builds may run.

## House chrome — binding (playlist law)

Read `../AGENTS.md` first: every recreated slide here uses
`../shared_patterns/house_chrome.js` (`drawHouseChrome(pptx, slide, {numeral})`) and
`../shared_patterns/house_chrome_check.py` runs on every 150dpi render pre-judge
(FAIL = fix the build). Badge numeral = the number printed on THIS slide's original
frame (= file id, 2..60). ml-intro house values are superseded for this playlist.

## Web-verified analysis is MANDATORY (inherited from 001 — this is a CRUCIAL video)

For EVERY slide's analysis (12), validation (13), recreation, and QA: websearch the
primary source behind the slide (`agy -p "<query>"`; on 401/403 run `agy -p "hi"`
once, then retry), webfetch to confirm content, download the source's own images
into `slide_NNN_source/`. Per slide: `slide_NNN_source/SOURCES.md` provenance record
(source URLs, what was confirmed/corrected, `[?]` open questions). **No SOURCES.md =
the research step did not happen.** Extend `../001_transformers_part1/SOURCES_MAP.md`
by APPENDING video-2 rows — never delete or edit 001's rows. The Transformers sources
already verified for 001 (arXiv 1706.03762v7 figures banked in
`../001_transformers_part1/slide_18_source/`, Cho 2014, Bahdanau 2014, Peter Bloem
"Transformers from scratch", Mikolov 2013) cover most of this lecture's content —
recap slides must reference them; new Part-II content gets new verification. Vision
work runs through `.agents/image-analysis` (banked `.txt` transcripts).

## Slide dependency graph & pattern groups (founder directive 2026-10-11)

Canonical: `slide_dependencies.json` (v2 — qualified cross-video refs + pattern
groups). View: `VIDEO=deep-learning/002_transformers_part2 python3 scripts/15_progress.py deps`.
Builds are gated (`deps`/`buildable`); analysis and validation are NEVER gated.

**Cross-video edges** (child ← parent in 001; parents certify in 001's DB):

- 4 ← 001:15 AND 001:18 | 8 ← 001:33 | 11 ← 001:43 | 13 ← 001:33 | 15 ← 001:43 |
  17 ← 001:43 | 19 ← 001:19 | 37 ← 001:19 | 51 ← 001:18

**In-video edges**: 10←9 | 24←23 | 28←[27,26] | 29←28 | 45←28 | 46←45 | 47←46 |
48←47 | 49←26 | 57←47 | 59←38.

**Pattern groups** (sequential build, listed order — verify the pattern, then
reuse it): P1 [9,10,12,14,16] · P2 [20,21,22,34] · P3 [42,43,44] · P4 [54,55].

**Founder assumptions encoded pending veto** (founder did not answer; recorded in
`slide_dependencies.json` → `founder_assumptions_pending_veto`):

1. Slide 001 placeholder mirrors 001's certified cover (title "Deep Learning",
   badge numeral 1) — founder sign-off + chrome check, no judge comparison.
2. Slide 49 hard-depends on 26 only ("its deps" resolve transitively).
3. Slide 59 hard-depends on video-2 slide 38 only (likewise transitively).

## Special slides (founder-flagged — extra care)

- **Slide 1 (placeholder cover)**: no source frame. Build from the shared chrome +
  001 slide-1 layout (badge 1, course title "Deep Learning"). DB:
  `analysis_status='n/a-placeholder'`, `validation_status='ready'`. Certification =
  founder sign-off + `house_chrome_check.py`; a judge comparison is impossible.
- **Slide 51**: uses 001 slide 18's SOURCE IMAGE split into left and right halves at
  different measured positions on this slide. Pull the halves from the banked
  figure (`../001_transformers_part1/slide_18_source/`), PIL-measure each half's
  placement/size on THIS frame, compose exactly. Attention needed.
- **Slide 57**: encoder (from slide 47 — chains back through 46/45/28) + decoder
  composed professionally on ONE slide. MANDATORY web research for the correct
  decoder architecture; if a correct image is found online, download it into
  `slide_057_source/`; otherwise compose the decoder separately first, then compose
  encoder+decoder onto the single slide. First candidate to verify against the
  frame: 001's banked `The Transformer - model architecture..png` (arXiv
  1706.03762v7 Figure 1 IS the encoder+decoder composition).
- **Slide 49 / 59**: pattern-derived dependencies ("common patterns with … but not
  same as them") — re-use the family's verified patterns; do NOT clone their
  compositions.

## Fidelity law

The ORIGINAL VIDEO FRAME is ground truth for what each slide shows; web sources
confirm/correct data and provenance, never license inventing content. Slide wins
for recreation, source wins for understanding; disagreements are recorded in the
slide's SOURCES.md. `[?]` markers are removed only with a confirming URL.

## Close-out: slide 001 placeholder cover — FOUNDER SIGN-OFF recorded 2026-10-13 ("slide 1 signed off"). Row 1 in certified state per merge RUNBOOK caveat 4 (sign-off + house_chrome_check PASS evidence at recreated_pptx/qa/slide001/; deliverable md5 45edefe7d3b80df70217373a4965c0f6). Final merge now gated only on slides 016 + 057 certifying.
