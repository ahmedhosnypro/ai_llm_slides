# Certificate Audit — 001_transformers_part1, slides 1–15

Auditor: read-only certificate audit; writes confined to scratch/audit_001t1/.
Started: 2026-10-12. Deck status: 45/45 certified (per task brief).

## Banked evidence (structural pass so far)

1. **DB terminal state** — sqlite3 -readonly on slides_progress.db: slides 1–15 ALL have
   gen_status=passed AND visual_check=PASS. ✓ (rows read 2026-10-12)
2. **Transcript paths banked in DB** — each slide's visual_transcript points to
   recreated_pptx/qa/slideNNN/judge_attempt_N.txt (attempt 1 except: 4→a2, 5→a3,
   6→a2, 8→a1b, 9→a7). Existence+coherence check below per slide.
3. **Deliverable uniqueness** — recreated_pptx/ contains ONLY 45 files matching
   `slide_NNN_recreated.pptx` plus build/ and qa/ dirs. Zero _graphed/_omml/attempt
   variants. ✓
4. **Build scripts** — build/slide_001.js … slide_015.js all exist. ✓
7. **Dep-parent components** — build/components/ contains slide_006.js, slide_013.js,
   slide_014.js, slide_015.js (+ house_chrome.js). All parents 6/13/14/15 present. ✓

## Per-slide results

Legend: 1=DB terminal 2=transcript 3=deliverable unique 4=build js 5=chrome check on
certified render 6=badge numeral 7=components (parents 6/13/14/15). All renders checked
with `python3 videos/deep-learning/shared_patterns/house_chrome_check.py <render> <N>`.

- **S001** PASS-CHAIN — DB passed/PASS; judge_attempt_1.txt genuine element-level body,
  "FINAL VERDICT: PASS"; sole slide_001_recreated.pptx; build js; chrome check PASS on
  render_1.png; badge "1" banked; no deps.
- **S002** PASS-CHAIN — DB passed/PASS; genuine body ("FINAL VERDICT: PASS"); badge
  "numeral 2 … present in BOTH images" banked; chrome check PASS on render_1.png.
- **S003** ANOMALY (BLOCKER-class, see below) — items 1/2/3/4/6/7 individually OK
  (DB passed/PASS, transcript genuine "FINAL VERDICT: PASS", sole pptx, build js, badge
  "3" banked in both images) but item 5 FAILS: house_chrome_check.py on certified
  render_2.png = FAIL (7 failures: gray panel spans 0..1999 / full-bleed background,
  panel bottom 7px short, badge center (1909,84) vs canonical (1860,148), badge d=19
  vs 75, purple ring missing). Chain broken at the mandated gate.
- **S004** PASS-CHAIN — genuine attempt-2 body ("FINAL VERDICT: PASS"); badge "4"
  banked; chrome check PASS on render_2.png.
- **S005** PASS-CHAIN — genuine attempt-3 body ("FINAL VERDICT: PASS"); badge "5"
  banked; chrome check PASS on render_3.png.
- **S006** PASS-CHAIN — DB passed/PASS; judge_attempt_2.txt genuine, "FINAL VERDICT:
  PASS"; badge "6" banked; chrome check PASS on render_1.png; component
  build/components/slide_006.js exported. Cosmetic variance: judge_prompt_2.txt names
  render_2.png, which does not exist on disk; worker report banks "Attempt 2 — same
  render (no rebuild)" and lists render_1.png as the render; prompt path is stale
  naming, evidence chain intact.
- **S007** PASS-CHAIN — genuine body ("FINAL VERDICT: PASS"); badge "7" banked; chrome
  check PASS on render_1.png; requires components/slide_006.js (dep honored).
- **S008** PASS-CHAIN — DB passed/PASS; judge_attempt_1b.txt genuine element-level
  comparison-winner body ("IMG1 (recreation) is better… no observed omissions"); no
  literal "FINAL VERDICT:" line (documented in worker report; garbage-retry clause
  exercised once; 4 literal-PASS crop comparisons corroborate the delta regions);
  badge "8" banked; chrome check PASS on render_1.png; requires components/slide_006.js.
- **S009** PASS-CHAIN — genuine attempt-7 body ("FINAL VERDICT: PASS"); badge "9"
  banked; chrome check PASS on render_7.png; requires components/slide_006.js.
- **S010** PASS-CHAIN — genuine body ("FINAL VERDICT: PASS"); badge "10" banked
  ("identical in both, certified"); chrome check PASS on render_1.png; requires
  components/slide_006.js.
- **S011** PASS-CHAIN — DB passed/PASS; judge_attempt_1.txt genuine (JSON verdict pass
  + element-level body, "No MAJOR or BLOCKER defects… PASS"); badge "11" banked.
  Chrome check FAIL on render_1.png is a DOCUMENTED false positive (banked control run
  in selfcheck_attempt_1_output.txt: check fails identically rc=1 on the ORIGINAL
  frame — the slide's white content rectangle x40..920/y114..499 covers panel+side
  borders in both images; adapted chrome check 7/7 incl. badge center (1860,148)
  canonical + purple ring). Cosmetic/documentable variance, not a gate violation.
- **S012** PASS-CHAIN — genuine body ("FINAL VERDICT: PASS"); badge "12" banked
  ("present in both"); chrome check PASS on render_1.png. (Chrome drawn inline in
  build js — no house_chrome require — but passes the gate.)
- **S013** PASS-CHAIN — DB passed/PASS; judge_attempt_1.txt genuine comparison-winner
  body ("Image 1 wins on quality and fidelity"); no literal "FINAL VERDICT:" line —
  verdict substance unambiguous; judge's "bottom border clipped" caveat is the
  ratified chrome's bottom-stroke-at-edge design and is explicitly OVERRIDDEN in
  worker_report.md ("documented, not a fix trigger"; chrome check PASSES incl. bottom
  stroke); badge "13" banked in BOTH images; component build/components/slide_013.js
  exported.
- **S014** PASS-CHAIN — genuine body ("FINAL VERDICT: PASS"); badge "14" banked
  (present in both); chrome check PASS on render_1.png; component
  build/components/slide_014.js exported.
- **S015** PASS-CHAIN — genuine body ("FINAL VERDICT: PASS"); badge "15" banked;
  chrome check PASS on render_1.png; requires components/slide_014.js (15←14 honored).

Score: 14/15 clean PASS-CHAIN (4 with documented cosmetic variances); 1 BLOCKER-class
anomaly (S003).

## Anomalies by severity

### BLOCKER-class (1)

**S003 — certified render fails the mandatory house-chrome gate; deliverable draws the
SUPERSEDED ml-intro chrome. Certificate chain broken at audit item 5.**

- `house_chrome_check.py` on the certified render `qa/slide003/render_2.png` (the one
  judge_prompt_1.txt names): **FAIL**, 7 failures — gray spans the full canvas
  (cols 0–1999, i.e. no white canvas margin), badge center (1909,84) vs ratified
  (1860,148), badge d=19 vs 75, purple ring missing.
- `recreated_pptx/build/slide_003.js` confirms the root cause — it draws the old
  ml-intro chrome: `s.background = E8E8E8` full-bleed, red frame inset 0.15in, badge
  `x:12.48 y:0.30 w:0.5 h:0.5 fill FFF9C4` — values the namespace AGENTS.md marks
  superseded ("The ml-intro house values … are superseded for this playlist"), and
  which build/slide_002.js explicitly calls out as NOT matching this deck.
- The S003 judge prompt embedded the OLD chrome as ground rule (a), so its PASS
  certifies content fidelity under the superseded spec — it cannot certify chrome
  compliance under the 2026-10-11 playlist ratification ("ONE outer frame + ONE badge
  for EVERY slide"). No banked false-positive/override disposition exists (unlike S011).
- Timestamps chain cleanly (build js 10:53:38 → pptx 10:53:56 → render_2 10:53:57 →
  judge ~10:56 on 2026-10-11): the judged render IS the deliverable's render; no later
  rebuild.
- Contradicts the namespace AGENTS.md claim "Certified slides 2 and 3 already conform"
  — slide 2 conforms (check PASS); slide 3 does not.
- Auditor did NOT fix anything (audit is read-only + this file). Remediation belongs to
  the build/judge pipeline: rebuild slide 003 on components/house_chrome.js values and
  re-judge; cascade law does NOT apply (slide 3 has no dependents in
  slide_dependencies.json).

### Cosmetic / documented variances (5) — no action required

1. **S006** — judge_prompt_2.txt names render_2.png, absent from disk; worker report
   banks "Attempt 2 — same render (no rebuild)" and the evidence index lists
   render_1.png, on which the chrome check PASSES. Stale prompt-path naming only.
2. **S008** — certifying transcript ends "IMG1 (recreation) is better" (comparison-winner
   form) without the literal "FINAL VERDICT:" line; worker report documents the
   garbage-retry clause use and 4 literal-PASS crop comparisons on the delta regions.
3. **S013** — same verdict-phrasing variance; judge's bottom-border caveat explicitly
   overridden in worker_report.md as ratified-chrome design (check PASSES incl. the
   bottom stroke).
4. **S011** — standard chrome check false-positives on this slide by design; banked
   control run shows the ORIGINAL frame fails identically; adapted check 7/7.
5. **CLOSEOUT_REPORT.md wording** — "Every build imports shared_patterns/house_chrome.js"
   is imprecise: slides 002/003/012/013 draw chrome inline (002/012/013 still pass the
   gate; 003 is the S003 BLOCKER above). Immaterial except as it masked S003.

## Verification method note

- Badge numerals (item 6): all 15 banked in the certified transcripts (judge compares
  render vs original element-by-element; numeral read in both images for 1,2,3,4,5,6,
  8,9,10,11,12,13,14,15; S7 via "yellow '7' badge" house-chrome line). No vision-gate
  crop read was needed; no judges re-litigated.
- S008's prompt: judge_prompt_1.txt covers attempts 1 and 1b (1b = garbage-retry of the
  same dispatch per prompt clause 2b); render_1.png is the render for both.
- All checks run from disk only; DB read with sqlite3 -readonly; zero writes outside
  scratch/audit_001t1/; no banked evidence modified or deleted.
