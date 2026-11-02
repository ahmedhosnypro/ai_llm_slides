# Wave-1 Recon Summary — 09_introduction_to_neural_networks

Run: `run-1793126532` · Date: 2026-11-01 · Recon only; no evidence deleted; no commits.
V = `videos/machine-learning/09_introduction_to_neural_networks`

## 1. Progress DB (scripts/15_progress.py)

- `VIDEO=machine-learning/09_introduction_to_neural_networks python3 scripts/15_progress.py sync` → `synced analysis/ -> db` (exit 0). Note: the script takes the video as env var `VIDEO`, not a `--video` flag (flag form prints usage, exit 1).
- `report` → **32 slides, 2 visually certified PASS** per DB: slide 2 and slide 32 (`gen=passed`, `visual=PASS`); slide 1 and 3 carry `visual=FAIL` with judge-v4 error notes; slides 4–31 `pending`.

## 2. slides_final.json rebuild

- Loaded every `analysis/slide_NNN_final.json` (001..032), added `slide_id` (int), wrote a 31-element JSON array to `V/analysis/slides_final.json`.
- **Missing final: slide_015** (only `slide_015_raw.json` exists — validation never completed). No unparseable finals.
- Previous `slides_final.json` preserved at `pooled_missions/runs/run-1793126532/slides_final_pre_recon_20261101.bak`.

## 3. Verdict audit

Full table in `recon_wave1_verdict_audit.md` (+ `.json`). 22 files audited: 9 valid PASS, 12 FAIL, 1 void (226-byte stub), 1 prompt template (not a transcript). `judge_slide_004_merged.txt` has PASS content but the verdict is on line 1, not the last line (flagged). Conflicts: slide 013 and 016 each have both an old worker PASS and a later relay FAIL parked.

## 4. mission.db stale sweep

The `rejudge_*` rows live in the **scopes** table (the tasks table holds per-slide milestones and has no rejudge items). Updated 28 scopes rows `rejudge_*` with `status='in_work'` and `updated_at < '2026-11-01'` → `status='failed'`, note `stale — worker died with prior session; re-dispatched 2026-11-01`. The 4 already-`done` rejudge scopes (009, 013, 016, 032) were untouched. Post-state: rejudge scopes = 28 failed / 4 done.

## 5. Per-slide status table

| # | analysis final | validation verdict | build js | rendered pdf | judge verdict (banked) |
|---|---|---|---|---|---|
| 1 | yes | PASS_WITH_FIXES | yes | yes | FAIL (wave2 preFAIL) |
| 2 | yes | PASS_WITH_FIXES | yes | yes | FAIL (wave3 relay) — DB says visual PASS: mismatch |
| 3 | yes | PASS_WITH_FIXES | yes | yes | none banked (DB err: judge v4 FAIL) |
| 4 | yes | PASS_WITH_FIXES | yes | yes (+omml pdf) | PASS (merged/attempt1/omml) |
| 5 | yes | PASS_WITH_FIXES | yes | yes | none |
| 6 | yes | PASS_WITH_FIXES | yes | yes | none |
| 7 | yes | PASS_WITH_FIXES | yes | yes | none |
| 8 | yes | PASS_WITH_FIXES | yes | yes | FAIL (x2) |
| 9 | yes | PASS_WITH_FIXES | yes | yes | PASS |
| 10 | yes | PASS_WITH_FIXES | yes (v1-v3) | NO | none |
| 11 | yes | PASS_WITH_FIXES | yes (v1,v3) | yes (+omml) | none |
| 12 | yes | PASS_WITH_FIXES | yes | yes | FAIL (stale) |
| 13 | yes | PASS_WITH_FIXES | yes (v1-v3) | yes | conflict: oldjudge PASS vs relay stale FAIL |
| 14 | yes | PASS_WITH_FIXES | yes | yes | none |
| 15 | **NO (raw only)** | — | yes | NO | none |
| 16 | yes | PASS_WITH_FIXES | yes | yes | PASS (v2 + oldjudge) vs v1/relay FAIL — conflict |
| 17 | yes | PASS_WITH_FIXES | yes | NO | FAIL (superseded) |
| 18 | yes | PASS_WITH_FIXES | yes | yes | none |
| 19 | yes | PASS_WITH_FIXES | yes (v1,v2) | yes | PASS |
| 20 | yes | PASS_WITH_FIXES | yes | NO | none |
| 21 | yes | PASS_WITH_FIXES | **NO build js** | NO | none |
| 22 | yes | PASS_WITH_FIXES | yes | yes | none reliable (parked file is a misfiled 026 copy) |
| 23 | yes | PASS_WITH_FIXES | yes (v1,v2) | yes | none |
| 24 | yes | PASS_WITH_FIXES | yes | yes | none |
| 25 | yes | PASS_WITH_FIXES | yes | NO | none |
| 26 | yes | PASS_WITH_FIXES | yes | NO | FAIL (wave3); oldjudge void stub |
| 27 | yes | PASS_WITH_FIXES | yes | NO | none |
| 28 | yes | PASS_WITH_FIXES | yes | NO | none |
| 29 | yes | PASS_WITH_FIXES | yes | yes | none |
| 30 | yes | PASS_WITH_FIXES | yes (v1,v2) | yes | none |
| 31 | yes | PASS_WITH_FIXES | yes | yes | FAIL |
| 32 | yes | PASS_WITH_FIXES | yes | yes | PASS (oldjudge) |

## 6. Missing builds

- No build script at all: **slide_021** (no `slide_021_build.js`, no `slide_021_recreated.js`).
- Build script exists but no rendered pdf: **010, 015, 017, 020, 021, 025, 026, 027, 028**.
- **No plain `slide_NNN_recreated.pptx` exists anywhere under `recreated_pptx/`** — only `_omml`/`_stale_prebuild` variants in `build/` plus `deck_final.pptx`. The DB's `pptx` path for slide 32 (`recreated_pptx/slide_032_recreated.pptx`) does not exist on disk.

## 7. Slides without a verified PASS (banked transcript ending in `FINAL VERDICT: PASS`)

Verified PASS: **004, 009, 019, 032** (plus conflicting/old PASS for 013, 016).
Without verified PASS: **1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13*, 14, 15, 16*, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31** (*013/016 have an old PASS parked alongside a later FAIL).

## 8. Surprises

1. DB claims slides 2 and 32 are visually certified PASS, but slide 002's only banked rejudge transcript is FAIL, and neither promoted pptx exists on disk.
2. Slide 015 never got a validated final JSON (raw only) yet has a build script.
3. 28 stale `in_work` rejudge scopes were still open in mission.db (all pre-2026-11-01) — now failed per protocol.
4. `recreated_pptx/qa/` is empty — no per-slide judge_re transcripts were banked there despite the protocol requiring them; verdicts live in `build/` and `parked/`.
5. `15_progress.py` takes the video via `VIDEO` env var; `--video` flag is not supported (prints usage).
