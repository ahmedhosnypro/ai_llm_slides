# Resume-verification addendum — slide 015 (written by the SECOND resume worker)

This file documents a duplicate-dispatch event. It does NOT modify the certified
state recorded in `worker_report.md` (judge of record: `judge_attempt_1.txt`, PASS,
DB `gen_status=passed` / `visual_check=PASS` at 2026-10-12T04:38:57).

## What happened (timeline, all 2026-10-12)

- ~03:45–03:58 — first resume worker (the one this dispatch calls "dead") finished
  its build + render (`scratch/slide015/render2/`), died before judging.
- ~03:59 — THIS worker was dispatched to resume. Inventoried 80 scratch files + qa/,
  verified the dep gate (`15 ← 001:43`, unblocked), rebuilt the pptx (04:04),
  rendered (04:05), ran `house_chrome_check.py` (PASS), ran the closed loop,
  banked `render_1.png` + `build_attempt_1.js` (04:16) and rewrote
  `judge_prompt_1.txt` (04:18).
- 04:06–04:14 — a CONCURRENT resume worker (evidently dispatched in parallel) rebuilt
  the deliverable at 04:08 with real fixes (rotated pill labels corrected to
  top-down reading per its own `jcmp_fraction.txt` FAIL→FIX cycle; LO pitfall fix:
  0-width `prst="line"` vertical arrows replaced by rect+triangle `varrow()`),
  re-rendered, re-judged: `judge_attempt_1.txt` (04:14) = real comparison body,
  **FINAL VERDICT: PASS**, no BLOCKER/MAJOR, 4 MINOR. DB set to passed at 04:38:57,
  `worker_report.md` written.
- Verification of the certified chain (this worker, no modifications):
  - `build/slide_015.js` md5 `e0179fb12eadaa01ffa648e39dd3c020` == banked
    `qa/slide015/build_attempt_1.js` (the judged build is the on-disk build).
  - `qa/slide015/render_1.png` (04:08) is the render of that build; the judge
    transcript (04:14) evaluated exactly this render; deliverable
    `slide_015_recreated.pptx` (04:08) intact.
  - Its two mandatory dense-region comparisons: `jcmp_fraction2.txt` PASS,
    `jcmp_chips.txt` PASS.
  - `house_chrome_check.py` on the render: PASS (this worker's run).
  - Inheritance diff vs parent 001:43's certified render: chrome bands pixel-identical
    (left/right margins, top/bottom strips 0.0000 hot); badge zone differs only by the
    numeral (15 vs 43 — the required per-slide numeral). Content differs by design
    (frame-vs-frame PIL diff vs 001:43's frame = 49.2% hot px → recap redraws the
    composition at its own measured geometry; dependencies.md slide_045 precedent).

## Provenance incident (disclosed)

THIS worker overwrote `qa/slide015/judge_prompt_1.txt` at 04:18 — AFTER the concurrent
worker's judge had already consumed its own banked copy (judge ran ~04:10–04:14, before
the overwrite). The frozen `-p` GROUND-RULES body is byte-identical in both versions;
only the procedure header/--view text differs. The current file (8451 B) is the second
worker's-substituted template with this worker's cross-video `--view` wording. No
effect on the certification chain (the judge had already read its copy).

## Supplementary zone comparisons run by this worker (on the certified 04:08 render)

Banked as `cropcmp_{A_plane_tail,B_arrows_dots,C_frac_kq,D_query_row,E_title}.txt`:
- C (fraction/K·q zone): PASS. E (title zone): PASS — corroborates the judge.
- A (plane tail) / B (arrows+dots) / D (query row): FAIL findings from single
  zone-crop reads — SUBORDINATE to the judge of record (which passed the full slide
  with "No BLOCKER or MAJOR"), retained here as residual-risk observations:
  1. Back-layer peek-tops ("domes"): PIL-confirmed in the original frame — h2 sliver
     saturated-purple hump x≈185–228, y≈165–183 (tinted read AA9AC8 over lavender);
     h3 sliver olive-yellow hump x≈240–286, y≈145–164 (C9D876); h1 orange back-ellipse
     top with strong orange at y≈230–245, x≈145–175 (E0824E) — the build's orange back
     ellipse starts at y246 and the h2/h3 humps are not drawn. If the founder ever
     re-opens this slide, these measured geometries are the fix.
  2. K-row→dots arrows read blue in the render vs "red/dark" in the original (cropcmp B
     MAJOR); dots' light-blue halos vs solid navy (MINOR). Note: the full-slide judge
     described this zone's arrows as matching, and an earlier frame read (an_cropB)
     mentions "red arrows through a blue ring/dot node" — the zone carries both colors
     in the original; genuinely ambiguous at 3x.
  3. Query row: 4th striped key box sits below the green ellipse in the render
     (keyRows[3]=344 vs ellipse bottom ≈348) — closed-loop `green_ell` matched, so
     marginal; lower W-box arrow direction and bottom pointer angle flagged MAJOR by
     cropcmp D at medium confidence.
  None of these were raised by the judge of record; per the verdict law
  (`scripts/17_worker_instructions.md`) the slide is DONE on its PASS.

## Final state (verified)

- Deliverable: `recreated_pptx/slide_015_recreated.pptx` (single version, no suffix).
- Build: `recreated_pptx/build/slide_015.js` (banked `build_attempt_1.js`).
- Judge of record: `qa/slide015/judge_attempt_1.txt` — PASS, single-read, default
  route (images), glm leg DEFERRED/BLOCKED. 4 MINOR findings (chip-column offsets,
  swoosh tip, ⊗ micro-placement, h=3 bar texture) — documented in `worker_report.md`.
- DB row 15: gen_status=passed, visual_check=PASS, visual_attempts=1,
  visual_transcript=qa/slide015/judge_attempt_1.txt, last_error="none — certified PASS
  attempt 1".
- This worker changed NOTHING in the deliverable/build/DB; its only artifacts are this
  file, `qa/slide015/{render_1.png(overwritten by concurrent worker), closed_loop_
  attempt_1.txt, cropcmp_*.txt/.log, judge_p_body.txt, judge_prompt_1.txt (see
  incident), dome_zone.log}`, and scratch/slide015/{crops_cmp/, probes}.
