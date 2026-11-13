# MISSION_PROTOCOL — pool-run-1793594899 (Phase 6 prep, read-mostly)

Namespace: `videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/`
Date: 2026-11-02. Pool size per namespace AGENTS.md: 24; run dir `pool-run-<ts>/`;
all artifacts stay inside this namespace. No agents spawned in this run.

## Goal

Make the continuous-final-deck merge ready to execute the moment all 55 slides certify.

## Done this run

1. Verified placeholder deck `recreated_pptx/06_..._final.pptx`: 55 pages, page N ->
   slideN.xml -> imgNNN_slide_NNN.jpg, matches `unique_slides/slides_index.json`
   (badge == slide_number == N for all 55). 0 mismatches.
2. Verdict on `recreated_pptx/replace_slides.js`: NOT safe (media-name collisions
   across slides, no Content_Types updates, in-place destructive writes, hardcoded
   slides 40-44). Replaced by `tools/merge_final_deck.py` (OPC-level, per-slide
   media namespacing, Content_Types fixes, atomic output, --verify-only gate).
   Test merge of slides 1/3/11 verified byte-identical and LO-rendered to 55-page PDF.
3. Runbook written: `tools/FINAL_MERGE_RUNBOOK.md` (command sequence, gate checks,
   output paths).

## Not done / constraints honored

- No existing pptx, analysis/, or mission.db modified. Test artifacts confined to
  this pool-run dir (merge_test_final.pptx, merge_test_merged.pptx + .pdf).
- Merge itself is NOT executed — awaits 55/55 certification.
