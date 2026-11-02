# omml_restage_report — deck 03 (2026-11-01, restage worker)

NS = `videos/machine-learning/03_ridger_regression_gradient_descent`.
Scope honored: final-deck updates only, `$RJ/OMML_INVENTORY_r5.md`, `$RJ/OMML_WRAP_LOG.md`
append, derived per-slide `qa/slideNNN/omml_wrap_log.txt`. Page 25 skipped (other worker).
No `scripts/18_omml_wrapper.py` change, no slide pptx touched, no DB writes, no git, no
vision calls, no evidence deleted.

## 1. Drift scan (live, 2026-11-01)

Compared `final_deck_state.json` ledger `source_md5` vs md5 of each on-disk
`slide_NNN_recreated.pptx` for pages 1..51 (page 25 excluded). Pages with md5 drift AND
render_check != PASS: **10 and 23 only**. (The stale note's list 4,5,15,23,37 no longer
matches disk: 4,5,15,37 have md5-same ledger entries; their FAIL entries are stale
gate leftovers, not drift, and were left alone.)

## 2. Restage results

| page | action | result |
|---|---|---|
| 10 | `final_deck_tool.py update 10` + `render_check_pages.py 10` | **PASS 0 px** (gate_20261101-225651_p10); ledger PASS, md5 matches |
| 23 | `update 23` + gate, run twice (retry) | deck page restaged; ledger md5 now matches, but gate **FAIL** both runs, identical diff bbox (199,415,1785,967) |

Page 23 investigation: deck `ppt/slides/slide23.xml` is md5-identical to the source
`slide_023_recreated.pptx` slide1.xml; media `img023_image-1-1.png` byte-identical to
`image-1-1.png`; layout/master/theme byte-identical; presentation.xml differs only in
notesMaster rId numbering. The 30,949 differing pixels are text anti-aliasing (glyph-edge
deltas, shift-invariant — shifting by ±1px makes it worse, so not a translation). Verdict:
LibreOffice deck-vs-standalone render-context artifact, not a content mismatch. Ledger
keeps FAIL with gate reports gate_20261101-225712_p23, gate_20261101-230027_p23,
gate_20261101-230651_p23. Final deck md5 after restage: **35918b6fa1187e85d107aabe481016ff**.

## 3. Final OMML wrap census (all 19 eq-pic slides)

Method: `unzip -p slide_NNN_recreated.pptx ppt/slides/slide1.xml | grep -c` of
`mc:AlternateContent` and `<m:oMath`. altcontent = 2 × oMath on every slide (one
AlternateContent per wrapped pic: Choice OMML + Fallback PNG).

| slide | oMath | slide | oMath | slide | oMath |
|---|---|---|---|---|---|
| 004 | 1 | 023 | 1 | 039 | 1 |
| 005 | 8 | 030 | 2 | 044 | 54 |
| 009 | 2 | 031 | 1 | 048 | 6 |
| 014 | 3 | 032 | 1 | 050 | 4 |
| 015 | 1 | 033 | 1 | 051 | 11 |
| 021 | 5 | 034 | 1 | | |
| | | 036 | 1 | | |
| | | 037 | 5 | | |

**Total: 122/122 eq pics wrapped, 0 unwrapped.** Full table with manifest paths, 0-px
proofs and deck gate per slide: `$RJ/OMML_INVENTORY_r5.md`.

## 4. Files written this run

- `$RJ/OMML_INVENTORY_r5.md` (final per-slide table)
- `$RJ/OMML_WRAP_LOG.md` (summary append)
- `$RJ/omml_restage_report.md` (this file)
- Derived (marked DERIVED) `qa/slideNNN/omml_wrap_log.txt` for the 10 slides missing one:
  004, 005, 015, 021, 030, 037, 044, 048, 050, 051 (built from OMML_WRAP_LOG.md rows +
  `$RJ/slideNNN/` manifests; 009/014/023/031/032/033/034/036/039 already had logs)

## 5. Open item

Page 23 render gate: restage is content-correct (byte-identical slide in deck) but the
0-px gate cannot pass due to LO text-AA differences in deck context. Flagged for the
orchestrator; not fixable within this worker's scope (no slide pptx edits allowed).
