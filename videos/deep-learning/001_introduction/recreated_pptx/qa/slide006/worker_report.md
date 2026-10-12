# Worker report — slide 006 "Machine Learning in the real-world" (001_introduction)

## Verdict chain

1. **Deps gate**: `15_progress.py deps` — slide 6 is a ROOT, no `blocked_by` → build allowed.
2. **Spec**: `analysis/slide_006_final.json` (PASS_WITH_FIXES, score 9). `validation.fixes`
   applied; `verbatim_text` treated as law (leading space + double space in bullet 2
   preserved; ".. and many more" two leading dots preserved).
3. **Sources**: `slide_006_source/SOURCES.md` honored (CS229-notes confirmation; text-only
   slide, no figures needed; deck-origin open question noted there — analysis-side item).
4. **PIL forensics on the ground-truth frame** (banked: `measure_original*.py` +
   `*_out.txt`, 6 passes):
   - Title ink x 142..833, y 84..125 → Arial **REGULAR 45.5pt** (per-word advance fit
     spread 44.2..45.3 vs ArialB 39.4..42.0 with 'in' outlier; span solve agrees) —
     spec's "~40pt bold" estimate superseded by ink per the deck pixel law. Color
     modal (181,0,0) = JPEG-darkened C00000 (deck template).
   - Content box outer ink x 87..843, y 132..504, border ~3px → drawn as path rect
     x 88.5, y 133.5, w 754, h 370, line C00000 2.25.
   - Header: Times New Roman **23.9pt** (metric-solved 24pt, trimmed 0.1pt in closed
     loop), black; line 1 = bold+underline "Broadly applicable in many domains"
     (orig underline ink y=158 x 93..467 == TimesB phrase end 468.7) + regular
     " (e.g., finance, robotics,"; line 2 regular. Wrap point verified identical.
   - Bullets: Arial REGULAR 17.5pt, pitch 26.18px, text-left 205 (b2 at 210 via verbatim
     leading space), 11 blue + final ".. and many more" **BLACK** (zero bluish px,
     darkest (0,0,0)) — overrides the spec's all-blue claim (ink wins). Blue = **1A1ACC**
     (pooled 2x2-max one-parameter fit vs certified references: 005 truth 000080 excluded
     by R-channel ceiling, 002 truth 0000AA needs implausible R ringing; 1A1ACC fits G+B
     simultaneously — spec's guess confirmed).
   - Bullet dots: black d 5px, cx 182, 12 measured centers.
   - Black bottom bar x 38..921, y 518..539 (drawn h 19.5, chrome bottom stroke kept
     visible — certified 002/005 convention).
   - Original's own panel chrome sits inset (x ~56..906, top rule y 42..45) vs canonical
     playlist chrome x 42..918 — recreation draws canonical per the 2026-10-11 founder
     directive; judge ground rule (a) preempts.
5. **Build** (`build/slide_006.js`): pptxgenjs 4.0.1, playlist `drawHouseChrome` imported
   (numeral 6), bare hex, fontFace everywhere, margin 0, explicit lineSpacing on every
   text box (52/28/22), single-line boxes at measured baselines.
6. **Closed loop** (3 render/measure iterations; `house_chrome_check.py` PASS every time;
   `selfcheck_attempt_K.py` + outputs banked):
   - Attempt 1: title −1.1% narrow/1.4px low; 6 dot centers ±0.5-1px; self-check script
     artifacts identified (orig dark mask catches JPEG-darkened border; unscaled modal
     windows) and fixed in the checker.
   - Attempt 2: title fixed (45.5pt, top 66.8 — all 4 edges ≤0.9fp); header L2 3fp long
     → 23.9pt; dots d6 bottom edges 2fp over → d5.
   - Attempt 3 (final): **SELFCHECK RESULT: PASS** — every title/box/header/12-bullet/
     12-dot/bar edge within tolerance (≤2.4fp); underline verified contiguous-run at
     y159-160 x93.4..466.2 (orig y158 x93..467); containment PASS. Mandatory crop
     comparison n/a: no equations, no multi-line delimiters, no tables on this slide.
7. **Judge** (attempt 1, K=1): probe valid (full verbatim transcription, badge "6" read);
   comparison `[winner] images (round 1, attempt 1)`, degenerate events 0, coherent body:
   **FINAL VERDICT: PASS** for 'faithful, usable recreation'. 2 MINOR notes only
   (title glyph size slightly larger relative to panel — template-scale artifact;
   bullet block starts marginally lower — MEDIUM confidence). No BLOCKER/MAJOR.
   Certificate: single-read, default route (images), glm leg DEFERRED/BLOCKED.
   Judge procedure executed by worker via Bash byte-for-byte per the banked prompt
   (no Agent/Task spawn tool in this environment — orchestrator-approved fallback).

## DB state (VIDEO=deep-learning/001_introduction, slide 6)

- gen_status=passed, visual_check=PASS, visual_attempts=1
- visual_transcript=videos/deep-learning/001_introduction/recreated_pptx/qa/slide006/judge_attempt_1.txt
- build_script=videos/deep-learning/001_introduction/recreated_pptx/build/slide_006.js
- pptx_path=videos/deep-learning/001_introduction/recreated_pptx/slide_006_recreated.pptx

## Attempts used

3 build/render closed-loop iterations (1 judge attempt, PASS on first comparison).
Attempt numbering: render_1/2/3 (all kept); build_attempt_1/2/3.js banked.

## Deviations from spec (ink-measured, documented)

- Title Arial REGULAR 45.5pt (spec guessed ~40pt bold) — ink per-word fit.
- Header 23.9pt (spec guessed ~20pt) — metric-solved + closed loop.
- Bullets 17.5pt (spec guessed ~16pt); blue 1A1ACC (spec agreed); bullet 12 BLACK
  (spec said blue) — ink.
- Box x 87..843 (spec guessed 8%-92% = 77..883) — ink.
- Last bullet NOT clipped (spec/animation_state claim "slightly clipped") — measured
  ~5px clearance; judge ground rule (g) recorded the measured position as correct.
- Black bottom strip recreated (spec step 9 made it optional; certified 002/005
  precedent in this playlist includes it; cursor artifact omitted per spec step 8).

## Component banking

None — slide 6 is a root with no dependents in `slide_dependencies.json` (no playlist
references), so no banking obligation.

---

## VERIFICATION ADDENDUM — post-interruption re-dispatched worker (2026-10-12 ~06:47)

**Collision protocol.** This slide was re-dispatched after a host interruption under a
"sole owner, nothing banked" premise. On arrival I found a live peer builder already
iterating (build/render/self-check cadence 06:08..06:46). Per the orchestrator's
coordination warning I stood down to READ-ONLY for the peer's entire cycle: no writes to
the build script, renders, transcripts, or DB; monitored to quiescence; then certified
from banked evidence per the resume law. My only artifacts are the independent forensics
under `scratch/slide006/forensics{,2,3,4,5}.py` (never touched by the peer) and this
addendum.

**Independent corroboration (my own PIL forensics, separate code path):** content box
red-border cols/rows x 88/842, y 133/503 (2px); title ink x 143..832, center 487.5,
cap-top 85, baseline ~115.5; header TNR 24pt mixed bold+regular, wrap after "robotics,";
underline = ONE contiguous run x 93..468 at rows 157-158 == TNR-Bold-24 phrase advance
376 (93+376=469) — the bold+underlined phrase only, matching the build; 12 bullet
baselines 209..497 pitch 26.18; dots d≈5 cx=182; bullet 12 ".. and many more" is NEUTRAL
BLACK (modal R=G=B, zero blue chroma) — independent confirmation of the build's
spec-override; black bar x 38..921, y 519..539; cursor artifact present in the original
and correctly omitted. Peer's blue 1A1ACC vs my chroma-dilution lean 0000AA: both are
estimates of a chroma-subsampled 17.5pt JPEG blue; the judge's comparison confirmed the
rendered blue matches — no action.

**Certificate verification (all read-only):**
- `judge_attempt_1.txt` is a real comparison winner body (ground-rules prelude applied,
  element-by-element, 2 MINOR, no BLOCKER/MAJOR, coherent `FINAL VERDICT: PASS`) — not
  degenerate; verdict law satisfied.
- `house_chrome_check.py` re-run by me on the JUDGED render `render_3.png`: **PASS**
  (panel, badge center/size within tol 8).
- Provenance: deliverable `slide_006_recreated.pptx` mtime 06:38:46 == build attempt 3
  (script 06:38:22) which produced judged `render_3.png` 06:38:48 — the certificate
  binds to the judged artifact; single-version law holds (plain name, no variants).
- Peer's closed-loop chain banked: selfcheck 1 FAIL → 2 FAIL (6 sub-tolerance items) →
  **3 PASS**; build_attempt_1/2/3.js + judge_prompt_1.txt + probe_1.txt all banked.
- DB row current: gen_status=passed, visual_check=PASS, visual_attempts=1,
  visual_transcript banked. No DB writes made by me — the peer's writes stand.

**Conclusion:** slide 006 is certified (judge PASS on attempt 1, backed by a real
comparison transcript) and the DB row is current. Re-dispatched worker made no mutations
beyond this addendum; forensics banked at `scratch/slide006/` for future re-openings.
