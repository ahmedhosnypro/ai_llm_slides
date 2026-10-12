# Worker report — slide 038 "Filters parameters" (deep-learning/001_introduction)

Date: 2026-10-12. Worker: slide-recreation builder subagent (fresh start; no prior artifacts).
Dispatch walls honored: judge through `scripts/16_vision_gate.sh`, `--timeout 280` inside
`timeout 1700` outer, `-p` payload sourced byte-for-byte from the banked
`judge_payload.txt`; TMPDIR redirected to `scratch_038/` for every soffice/gate call
(/tmp quota blocked); absolute `-env:UserInstallation`.

## Verdict chain

| Attempt | Render | Judge transcript | Verdict | Key findings |
|---|---|---|---|---|
| pre-judge | render_1..3 | qa/slide038/crop_fbox.txt | PASS (crop: formula box, 2 MINOR: ~2% narrower text, red hue) | house_chrome_check.py PASS on every render; PIL closed-loop: title/lines/circles/dashes/bars pinned (baselines corrected +12.2 title / +9.6 lines; circles d 30→28) |
| pre-judge | — | crop_diag.txt / crop_diag_2x.txt | NOT OBTAINED | 6 attempts (2.5x and 2x pairs, walls up to 1500s) all EmptyStreamError 3/3 — gateway refused the diagram-crop pair while other calls succeeded. Slide has no equations/multi-line delimiters/tables (the mandatory crop triggers); formula-box crop (all the text) PASSED; diagram covered by full-slide judge + PIL closed-loop. Documented, not skipped silently. |
| 1 | render_3 | qa/slide038/judge_attempt_1.txt | FAIL | BLOCKER: original annotates the dashed projection lines with handwritten "7"s (7×7 receptive field), absent in recreation. MINOR: 3-dims arrow direction; white pencil quad reads as artifact. |
| 2 | render_4 | qa/slide038/judge_attempt_2.txt | **PASS** | "No BLOCKER or MAJOR defects found. No missing elements, no frame overflows... all text verbatim, all colors within tolerance." 3 MINORs (see below). |

**FINAL: PASS** — single-read, default route (images), glm leg DEFERRED/BLOCKED.

## Attempt-2 MINORs (documented, non-blocking)

1. "3 dims" arrow direction differs slightly (original: toward the slab's top edge; mine:
   pencil-gray stroke (329,297)→(286,331) per PIL-measured ink — the original's strokes are
   gray 120..175 and run parallel to the slab's top edge; head placement in a hand-drawn
   squiggle is ambiguous at 960×540).
2. "Extra bold 7 numerals on four of the five slabs" (medium confidence) — judge variance:
   attempt 1 read the same 7s as "cyan top, red, purple — Match". The 7s follow the
   validated spec's label list ("7 above the stack / mid-height between slabs / right side
   of the purple slab") AND PIL ink (vertical strokes at x 450, 507-510, 519-522, 547-550,
   y 355..397). Spec + pixels kept over the attempt-2 reading; flagged for founder review
   as the judge requested.
3. Handwriting medium difference — ground rule (d), mandated upgrade.

## What was built

- `recreated_pptx/build/slide_038.js` (attempt copies banked: build_attempt_1.js = render_3
  chain, build_attempt_2.js = render_4 chain) — pptxgenjs, LAYOUT_WIDE, direct 1px=1pt
  mapping (certified precedent of slides 001/002/005/031), playlist house chrome via
  `shared_patterns/house_chrome.js` (badge numeral 38; frames carry no printed numbers —
  PENDING FOUNDER VETO assumption per 001_introduction/AGENTS.md).
- Custom 3D geometry (brown slab + 5-slab filter stack) rendered as matplotlib 600dpi
  transparent PNGs (`build/assets/slab038_brown.png|.json`, `slab038_stack.png|.json`),
  embedded at EXACT size w=px/600 (the certified equation-PNG mechanism; pptxgenjs has no
  custom polygons). Brown slab got a dark top-face band in attempt 2 (judge + PIL ink band).
- Formula lines: verbatim typed text, TNR 21pt (PIL advance 669/654/177 vs measured
  672/656/175), color terms red C00000 / blue 000080 (PIL modal (0,0,131-144) — deck pixel
  law beats the spec's 0000CC guess) / green 009900, double spaces preserved. No mathtext:
  the original's formula is itself typed linear text with no stackable constructs
  (verbatim_text law; ground rule (e) covers the format question).
- Title TNR Bold 38pt C00000 (advance 301 vs 300 measured; deck-template serif precedent).
- Diagram: 4 dashed lines (PIL count; spec flagged the count uncertain) y 355/366/376/387
  x 350..390, X sign, two 6699FF "=" bars, five circles d28 + tan D58429 rings at cx
  625.5/663.5/701.5/741.5/778.5 cy 369, Comic Sans MS annotations (RGB charSpacing 7,
  3 dims, three 7s + the two dashed-line 7s added in attempt 2, 3 + pencil strokes,
  735 weights charSpacing 2.5), 5 fanned arrows + 3-dims arrow (pencil gray 595959).
- EXCLUDED per spec brief step 18 + ground rules (c): the bottom black video-player bar.
- No equations → no OMML wrap obligation. Single-version law: one pptx, no suffixes.

## Evidence

- Deliverable: `recreated_pptx/slide_038_recreated.pptx`
- Renders: `qa/slide038/render_1..4.png` (150 dpi, 2001×1125)
- Transcripts: `qa/slide038/crop_fbox.txt` (PASS), `crop_diag.txt`/`crop_diag_2x.txt`
  (aborted — EmptyStreamError), `judge_attempt_1.txt` (FAIL), `judge_attempt_2.txt` (PASS)
- Prompt bank: `qa/slide038/judge_payload.txt` (frozen -p payload),
  `judge_prompt_1.txt`/`judge_prompt_2.txt`
- Measurements: `scratch_038/measure_1..16.py`, `selfcheck_1..6.py`, `colorcheck.py`
- DB: gen_status=passed, visual_check=PASS, visual_attempts=2,
  visual_transcript=qa/slide038/judge_attempt_2.txt, pptx_path + build_script set.
- Component banking: NOT required — slide 38 is a dependency root with no children in
  `slide_dependencies.json` (edges: 16←9, 17←16, 18←9, 19←9, 25←24, 37←36, 41←35) and no
  cross-video references; no pattern group.
