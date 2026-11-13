# FINAL_MERGE_RUNBOOK — 06_svm_with_kernels_quadratic_programming_libraries

Phase 6 prep runbook: merge all 55 certified per-slide decks into the continuous
final deck at OPC/zip level, byte-verbatim, then run the merge gate.
All paths inside `videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/`.
Never modify the placeholder deck in place — always merge to a new output first.

## State verified 2026-11-02

- Placeholder `recreated_pptx/06_svm_with_kernels_quadratic_programming_libraries_final.pptx`:
  55 pages; presentation order page N -> `ppt/slides/slideN.xml` -> media
  `imgNNN_slide_NNN.jpg`; matches `unique_slides/slides_index.json` (55 slides,
  slide_number == badge == N). 0 mismatches.
- `recreated_pptx/replace_slides.js` is NOT safe to use (see below) — use
  `tools/merge_final_deck.py`.

## Why replace_slides.js was replaced

- Copies source media into the final deck under their ORIGINAL names
  (`ppt/media/image1.png`...), so two slides using the same internal media name
  overwrite each other — not byte-verbatim per slide.
- Never updates `[Content_Types].xml` for newly introduced media extensions.
- Overwrites the final deck in place on every call (destructive; no atomic output).
- Hardcodes slides 40–44.

## Merge tool

`tools/merge_final_deck.py` — for each `slide_NNN_recreated.pptx`: copies
`ppt/slides/slide1.xml` byte-verbatim to `ppt/slides/slideN.xml`, rewrites the
slide rels so every media/font part lands under a per-slide name
(`ppt/media/sNNN_<orig>`, `ppt/fonts/sNNN_<orig>`), copies those parts
byte-verbatim, adds required Content_Types entries, leaves
`ppt/_rels/presentation.xml.rels` untouched (slide part names preserved).
Writes atomically (`.tmp` then move). Tested 2026-11-02: 3-slide test merge
verified byte-identical and rendered by LibreOffice headless to a 55-page PDF.

## Command sequence (run when all 55 slides certify)

```bash
NS=videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries
FINAL="$NS/recreated_pptx/06_svm_with_kernels_quadratic_programming_libraries_final.pptx"
OUT="$NS/recreated_pptx/06_svm_with_kernels_quadratic_programming_libraries_final_merged.pptx"

# 1. Merge every certified per-slide deck into a NEW output (placeholder untouched)
python3 "$NS/tools/merge_final_deck.py" --final "$FINAL" --slides-dir "$NS/recreated_pptx" --out "$OUT"

# 2. Merge gate step 1: 0/55 mismatched pages (byte-compare slide XML vs source decks)
python3 "$NS/tools/merge_final_deck.py" --final "$OUT" --slides-dir "$NS/recreated_pptx" --verify-only
#    expect: "55 pages byte-identical ... 0 mismatched", exit 0

# 3. Merge gate step 2: one LibreOffice headless render of the merged deck
soffice --headless --convert-to pdf "$OUT" --outdir "$NS/recreated_pptx/qa/final_merge/"
#    expect 55-page PDF; render pages: pdftoppm -png -r 150 <pdf> page

# 4. Merge gate step 3: compare every merged page render vs the per-slide source render
#    (pixel diff; record per-page result in the gate report)

# 5. Write gate report + md5
md5sum "$OUT" > "$OUT.md5"
#    gate report: $NS/recreated_pptx/qa/final_merge/MERGE_GATE_REPORT.md
#    (0/55 mismatches, render-compare table, LO session info, md5)
```

## Outputs (all under the namespace)

- Final deck: `recreated_pptx/06_svm_with_kernels_quadratic_programming_libraries_final_merged.pptx`
- `..._merged.pptx.md5`
- Gate report + renders: `recreated_pptx/qa/final_merge/MERGE_GATE_REPORT.md`

## Do not

- Do not edit the placeholder pptx, any existing `slide_NNN_recreated.pptx`,
  `analysis/`, or `mission.db`.
- Do not re-encode media; do not re-save the merged deck through LibreOffice.
