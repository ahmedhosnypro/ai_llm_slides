# Certificate Audit — 001_transformers_part1, slides 16–30

Auditor: read-only certificate audit; writes confined to scratch/audit_001t1/ (this
file + s027 badge crops). No DB writes, no fixes, no banked evidence touched.
Date: 2026-10-12. Deck status: 45/45 certified (per task brief).
Method: DB via `sqlite3 -readonly`; transcripts/prompts/reports read from disk;
house_chrome_check.py executed on the exact render each winning judge_prompt names.

## Structural pass (all 15 slides)

1. **DB terminal state** — sqlite3 -readonly: slides 16–30 ALL gen_status=passed AND
   visual_check=PASS. visual_attempts: 16=2, 25=7, 28=3, 29=2, 30=2, rest=1.
   DB visual_transcript paths resolve to existing qa/slideNNN/judge_attempt_N.txt for
   all 15. ✓
2. **Transcripts** — 15/15 genuine coherent comparison-winner bodies (element-level
   tables/findings, discrepancy lists with severities+confidence, FINAL VERDICT: PASS).
   No degenerate/garbage/missing bodies. ✓
3. **Deliverables** — slide_016..030_recreated.pptx all exist; recreated_pptx/ root
   contains ONLY the 45 exact-name pptx + build/ + qa/ (no _graphed/_omml/_attempt
   variants). ✓
4. **Build scripts** — build/slide_016.js … slide_030.js all exist. ✓
5. **House chrome check** — run on the certified render named in each winning
   judge_prompt: 15/15 PASS (identical geometry: panel x 89–1913, y 95→bottom; badge
   (1860,148) d=70; tol 8). ✓
6. **Badge numerals** — 14/15 banked in the winning transcripts (16–26, 28–30 quote
   the numeral, matched vs IMG2). 027 (not quoted in its transcript) verified by
   crop-read of render_1.png + unique_slides/slide_027.jpg badges: both "27". 15/15
   MATCH. ✓ (crops: s027_badge_render.png, s027_badge_orig.png)
7. **Dep-parent components** — components/ has slide_017/018/019/026/029.js. Wiring
   verified: build_018→comp_018→requires ./slide_017.js; build_019→comp_019→requires
   ./slide_018.js; build_027/028/029→comp_026; build_030→comp_029 (29 itself requires
   26). All 6 in-range edges (18←17, 19←18, 27←26, 28←26, 29←26, 30←29) wired. ✓

## Per-slide results

| # | Result | Evidence clause |
|---|--------|-----------------|
| 16 | PASS-CHAIN | DB passed/PASS (a2); qa/slide016/judge_attempt_2.txt genuine PASS (3 MINOR); render_2.png chrome PASS; badge "16" banked; single pptx + build_016.js present; a1 FAIL (MAJOR label collision) superseded by a2 fixes |
| 17 | PASS-CHAIN | DB passed/PASS (a1); judge_attempt_1.txt genuine PASS (5 MINOR); render_1.png chrome PASS; badge "17" banked; single pptx + build_017.js; component slide_017.js banked for child 18 |
| 18 | PASS-CHAIN | DB passed/PASS (a1, depends_on=17); judge_attempt_1.txt genuine PASS (3 MINOR); render_1.png chrome PASS; badge "18" banked; single pptx + build_018.js requiring components/slide_018.js→slide_017.js |
| 19 | PASS-CHAIN | DB passed/PASS (a1, depends_on=18); judge_attempt_1.txt genuine PASS (4 MINOR); judge_prompt_1 names render_4.png (certified, post z-order fix — worker_report documents render_1..3 lineage + 14/14 selfcheck); render_4 chrome PASS; badge "19" banked; build_019 wrapper requires components/slide_019.js→slide_018.js; 0-px component-verify banked |
| 20 | PASS-CHAIN | DB passed/PASS (a1); judge_attempt_1.txt genuine PASS (0 discrepancies); render_1.png chrome PASS; badge "20" banked twice; single pptx + build_020.js |
| 21 | PASS-CHAIN | DB passed/PASS (a1); judge_attempt_1.txt genuine PASS (1 MINOR); render_1.png chrome PASS; badge "21" banked; single pptx + build_021.js |
| 22 | PASS-CHAIN | DB passed/PASS (a1); judge_attempt_1.txt genuine PASS (3 MINOR); render_1.png chrome PASS; badge "22" banked; single pptx + build_022.js |
| 23 | PASS-CHAIN | DB passed/PASS (a1); judge_attempt_1.txt genuine PASS (3 MINOR); render_2.png chrome PASS; badge "23" banked; single pptx + build_023.js |
| 24 | PASS-CHAIN | DB passed/PASS (a1); judge_attempt_1.txt genuine PASS (4 MINOR); render_1.png chrome PASS; badge "24" banked; single pptx + build_024.js |
| 25 | PASS-CHAIN | DB passed/PASS (a7); judge_attempt_7.txt genuine PASS (4 MINOR); render_7.png chrome PASS; badge "25" banked; single pptx + build_025.js; NOTE: a6 PASS transcript was lost to a host crash — re-judged a7 on pixel-identical re-render (diff bbox None, banked) per verdict law; a1–5 never judged (provider outage) |
| 26 | PASS-CHAIN | DB passed/PASS (a1); judge_attempt_1.txt genuine PASS (3 MINOR); render_1.png chrome PASS; badge "26" banked; single pptx + build_026.js; component slide_026.js banked for children 27/28/29 |
| 27 | PASS-CHAIN | DB passed/PASS (a1, depends_on=26); judge_attempt_1.txt genuine PASS (4 MINOR); render_1.png chrome PASS; badge numeral 27/27 verified by crop-read (not quoted in transcript — only gap, closed); single pptx + build_027.js requiring components/slide_026.js |
| 28 | PASS-CHAIN (with documented override — see anomalies) | DB passed/PASS (a3, depends_on=26); judge_attempt_3.txt PASS verdict; render_3.png chrome PASS; badge "28" banked; single pptx + build_028.js requiring components/slide_026.js; a2 FAIL superseded (8 diamonds delta added); judge's MAJOR item falsified by banked pixel forensics (worker_report.md) |
| 29 | PASS-CHAIN | DB passed/PASS (a2, depends_on=26); judge_attempt_2.txt genuine PASS (3 MINOR); render_2.png chrome PASS; badge "29" banked; single pptx + build_029.js requiring components/slide_026.js; a1 FAIL (BLOCKER missing diagonal connectors) superseded |
| 30 | PASS-CHAIN | DB passed/PASS (a2, depends_on=29); judge_attempt_2.txt genuine PASS (4 MINOR); render_2.png chrome PASS; badge "30" banked; single pptx + build_030.js requiring components/slide_029.js (30←29←26 chain); NOTE: a1 was PASS with 4 MINOR — the one on the worker's own delta (missing leader lines, ink-scan confirmed real) was fixed voluntarily and re-judged a2 PASS; 3 inherited minors overridden per inheritance law |

## Anomalies

### BLOCKER-class
**None.** No DB/terminal-state divergence, no missing/garbage transcript, no missing
deliverable or stray deliverable variant, no failed chrome check, no badge mismatch,
no missing dep-parent component or broken wiring across slides 16–30.

### Cosmetic / observational
1. **Slide 028 — MAJOR finding inside a PASS transcript, no attempt 4.**
   judge_attempt_3.txt lists "MAJOR (confidence ~60%)" (block arrow vs inner panel
   bottom edge) and recommends a nudge "in attempt 4" that never happened. NOT a
   blocker: the verdict line is PASS and qa/slide028/worker_report.md banks a
   pixel-forensic override — the arrow is certified-parent (26) geometry, frame-diff
   026↔028 = 0 and parent-render-vs-recreation diff = 0 in that region, and the
   ORIGINAL frame carries the same ink below the canvas bottom; nudging would have
   broken fidelity. Certificate stands; flagged so the orchestrator knows the tension
   between transcript text and banked override is documented, not lost.
2. **Slide 027 — badge numeral not quoted in the winning transcript** (only slide in
   range). Closed by auditor crop-read: render badge "27" = original frame badge "27"
   (crops banked in this dir). Cosmetic process gap only.
3. **Slides 25/30 — multi-attempt histories** (a6-PASS-lost-to-crash → a7 re-judge on
   pixel-identical render; a1-PASS → voluntary delta fix → a2 re-judge). Both
   documented in worker reports and DB-consistent (DB points at the banked winners).
   No action needed.
4. **scratch/ artifacts, not deliverable variants:** scratch/slide029/
   component_validation.pptx (component test build) and scratch/slide_032_recreated.pptx
   (out of range, slide 32) exist in the video scratch dir. Neither lives in
   recreated_pptx/ and neither carries a deliverable name; per the single-version law
   these are working artifacts. No action needed; noted for completeness.

## Verdict

Slides 16–30: **15/15 PASS-CHAIN, 0 BLOCKER-class anomalies.** Certificates are
disk-verifiable end to end (DB terminal → banked genuine transcript → single-version
deliverable + build script → chrome PASS on the named certified render → badge
numeral match → dependency components present and wired).
