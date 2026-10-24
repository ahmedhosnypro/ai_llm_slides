# HANDOFF — deck 03 (03_ridger_regression_gradient_descent), state at 2026-10-22

Resume point for the next session/device. Machine state = `slides_progress.db`
(`python3 scripts/15_progress.py report` from the project root, always with
`VIDEO=machine-learning/03_ridger_regression_gradient_descent`).

## Certified: 10 / 51 (visual_check = PASS, gen_status = passed, attempt counts in DB)
| slide | notes |
|---|---|
| 001 | judge attempt-1 PASS, crop legs PASS |
| 002 | — |
| 011 | attempt-1 PASS (underline hairline fixed via slide_020 family-rect pattern; "spacing" MINOR refuted after the worker fixed its own matched-resolution measurement bug) |
| 020 | — |
| 022 | — |
| 026 | attempt-5 PASS; rendered from `build/slide_026.js`, final render `render_9.png`. THREE MINOR deviations vs the original frame recorded in `qa/slide026/handover_w8_026_2026-10-21.md` (rowA "Random Weights (W)" bold-in-build/regular-in-frame; rowA pale light-blue rule at y159–160 x315..434 RGB≈(158,155,198) present in original, never in any render; rowD "gradient is " regular-in-build/bold-in-frame). Judge passed; treat as recorded notes, not blockers. **Do not re-dispatch 026.** |
| 027 | certified attempt-10 (md5 `a5f15c5d57342b344f78fc84fb1e5eb3`). Long history, see "027 founder findings" below — the founder reviewed this slide twice. `qa/slide027/adjudication_attempt_9.md` is the controlling record. |
| 029, 035, 038 | — |

## In flight / interrupted
- **009**: unjudged WIP pptx on disk (built 07:54, smoke tests interrupted by the fleet stop). DB `building`, claim RELEASED. Fresh build/judge pass needed. 009 is the root for child 010 (010 imports `build/components/slide_009.js`).
- **023**: 18-file forensics/geometry bank in `qa/slide023/`, no build yet. Ready for a fresh worker.

## Dispatch order (one subagent at a time, background, wait for each notification)
1. 009 (root → unblocks 010)
2. 010 (child of 009)
3. 012 (root → unblocks 013)
4. 013 (child of 012: inherit 12's table PATTERN at 013's measured position/numbers)
5. 017 (child of 13) → 018 (child of 17)
6. Fresh roots: 007, 014, 015, 036, 039, 040, 003, 005, 006, 016, 025, 030, 048, 028
7. Bank-check: 004, 008, 021, 024
8. Finals-gated (all 51 finals exist — briefs pre-banked for 019/031/034/037/042/043/044): 019, 031, 034, 037, 041–047, 049–051
9. Research: SOURCES.md for 025/026/027 (dirs exist, empty; 51/51 close-out requirement) + SOURCES_MAP rows
10. OMML wrap pass on equation slides post-certification (`scripts/18_omml_wrapper.py`, rel-ids re-derived from the current pptx)
11. Final: byte-verbatim OPC deck merge + 0/51 pixel gate + md5 sidecar + CLOSEOUT_REPORT.md

## 027 founder findings (2026-10-21 — BINDING, fixed in attempt 10)
The founder visually reviewed render_8 and rejected it: (a) the black cost curve was
jagged/rippled — it is a quadratic and must render as one smooth mathematical curve;
(b) the grey dashed connectors are ARC ARROWS WITH ARROWHEADS, and were drawn headless;
(c) connectors must be aligned to the purple dot centres. The certified build (attempt 10)
draws: one analytic quadratic for the black curve (ripple rms 0.1202 fpx), nine cubic
arcs anchored dot-centre→dot-centre, and nine filled grey arrowheads on each arc's
terminal tangent. If any future judge or worker claims "the original has no arrowheads",
that claim is defective evidence — the founder settled it. See
`qa/slide027/adjudication_attempt_9.md`.

## Pipeline state
- Analysis + validation COMPLETE: 51/51 raws + finals; `analysis/slides_final.json`
  aggregate rebuilt (51 entries, all PASS_WITH_FIXES, scores 7–10; 37 validated by
  glm-5.3 before the swap, 14 by `validate_slides` after).
- Script 13 now validates with the founder-created `validate_slides` IronRouter model
  (env `IR_TEXT_MODEL`); writes are atomic (temp → replace).
- Script 13 trap: `--slides N` takes the FIRST N raw files, not slide N — use
  `--from/--to` for ranges; a ranged run clobbers `slides_final.json`, so a full
  no-range rebuild (with `--slides 60` or so, the default caps at 10) is required.

## Standing laws (do not re-litigate)
- Cap: ONE parallel subagent this session; dispatch background ONLY
  (`run_in_background: true`); wait for each completion notification before the next.
- Heartbeat every ~10 min on every claim; a live worker with a stale heartbeat reads
  as zombie and draws duplicate dispatches (happened on 026).
- Zoomed judge BOTH legs on every slide (Template A + Procedure B crops, matched
  effective scale LANCZOS ×(H_render/540)≈2.083); payloads byte-identical to
  `shared_patterns/judge_protocol_03.md`; PIL-first adjudication.
- EVERY `15_progress.py` call carries the `VIDEO=` prefix — a stray write once hit the
  CLOSED ml-intro DB (only `updated_at` cells changed; zero semantic corruption; documented
  in `qa/slide001/worker_report.md`, goes in CLOSEOUT_REPORT).
- Chrome: LAYOUT_WIDE 13.33×7.5in, canvas FFFFFF, panel E9E9E7 x54..903 y45..540,
  C00000 1pt strokes LEFT x58.5 / RIGHT x901 / BOTTOM y538.5 ONLY (NO top stroke);
  badge (876,73) d35 FDFD96 ring 6A5ACD, numeral 333333 Arial 18pt = file number.
- Equations: mathtext → 600dpi transparent PNG → addImage px/600 + `eq_*.json` sidecars;
  OMML wrap is an orchestrator post-certification pass.
- Never delete banked evidence; never edit a certified component in place; single
  plain-named `slide_NNN_recreated.pptx`; TMPDIR=`/home/ahmed/Projects/ai_llm_slides/scratch/tmp`.
- Research records: one `sources/slide_NNN_source/SOURCES.md` per slide + SOURCES_MAP.md
  rows (48/51 banked; 025/026/027 pending) — the research contract is
  `~/.zcode/skills/slide-recreation/references/source-research.md`; fetched-live URLs
  only, snippets are leads; no vision calls in research.

## Files that live on DISK ONLY (per the 29d61b6 qa/ convention — NOT in git)
`qa/` (judge transcripts, worker reports, adjudications, crop evidence) and `scratch/`.
The queue file `recreated_pptx/qa/orchestrator_queue.md` was force-added to the tree for
cross-device continuation; the rest of qa/ remains disk-only unless the owner decides
otherwise. The DB `last_error` column carries the per-slide resume spec for any lane
that stops mid-flight.
