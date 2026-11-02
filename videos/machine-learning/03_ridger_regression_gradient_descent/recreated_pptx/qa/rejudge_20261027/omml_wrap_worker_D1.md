# OMML wrap worker report D1 — deck 03 shard {014, 031, 032, 033, 034} (2026-11-01)

Scope: exactly these 5 slides of `videos/machine-learning/03_ridger_regression_gradient_descent`.
Wrapper used as-is (`scripts/18_omml_wrapper.py`, untouched; on-disk version already supports
`\underline` -> m:bar pos=bot, so no slide was blocked-on-wrapper). No other slide's files touched.
No git commits, no slides_progress.db writes, no vision calls, no evidence deleted, no LO resave
of any wrapped file. TMPDIR=$ROOT/scratch/tmp throughout.

## Per-slide results

| slide | result | rel ids (re-derived from CURRENT pptx) | manifest | md5 before | md5 after | 0-px proof (LO 150dpi, preOMML bak vs wrapped) | deck gate (update + render_check) |
|---|---|---|---|---|---|---|---|
| 014 | WRAPPED 3/3, rc=0 | rId1=eq_014_Yvec, rId2=eq_014_Yhatvec, rId3=eq_014_final | $RJ/slide014/omml_manifest.json | 18a724a03609dcf4a84ce81750ec2abe | 63fac3cb150bc17d4aeb730eb86d99e7 | 0 px (2001x1125) | page 14 PASS 0px (gate_20261101-203854_p14) |
| 031 | ALREADY WRAPPED on arrival (concurrent shard-2, md5 matches OMML_WRAP_LOG); verified + idempotent re-run (wrapped=0 skipped=1), deliverable bytes untouched | rId1=eq_031_main | $RJ/slide031/omml_manifest.json (reused banked) | c39ca2aa915ea8e10b8128ff9d77bead | c39ca2aa915ea8e10b8128ff9d77bead | 0 px | page 31 PASS 0px (gate_20261101-203922_p31) |
| 032 | ALREADY WRAPPED on arrival (shard-2); verified + idempotent re-run, bytes untouched | rId2=eq_032_main | $RJ/slide032/omml_manifest.json (reused banked) | 269f0316c0dfd7b0fcdcb89f55bccad4 | 269f0316c0dfd7b0fcdcb89f55bccad4 | 0 px | page 32 PASS 0px (gate_20261101-203948_p32) |
| 033 | WRAPPED 1/1, rc=0 | rId1=eq_033_main_v7b | $RJ/slide033/omml_manifest.json | 655eb34ed827f01e499eda9ed1097f0e | f0c7806cc2b967103ba85a6f10d7d9ba | 0 px | page 33 PASS 0px (gate_20261101-204014_p33) |
| 034 | WRAPPED 1/1, rc=0 | rId1=eq_034_main | $RJ/slide034/omml_manifest.json | 00029ccfc4cc2ac5a79318b0d7796f3e | 91a25c27bed85f467279af2fad3c2378 | 0 px | page 34 PASS 0px (gate_20261101-204041_p34) |

## Mathtext banked (sources per plan r4)

- 014: from `build/slide_014.js` + `build/assets/gen_eqs_014_v2.py`. Vectors are COMPOSED
  (hand-drawn parens + entries), banked as delimiter-matrix mathtext:
  `\left(y_{1}\\y_{2}\\\vdots\\y_{n}\right)` and `\left(\hat{y}_{1}\\...\\right)`, 16pt C00000.
  Final objective is a 5-segment multi-color composition; banked as single-color Choice
  `J(W)\;=\;\frac{1}{2}\left[\left(Y-\hat{Y}\right)^{T}\left(Y-\hat{Y}\right)\;+\;\lambda\;W^{T}W\right]`,
  17pt 000000 (multi-color flattened to black in the OMML Choice per the accepted shard-1
  pattern; the mc:Fallback PNG keeps the exact certified multi-color pixels). Note: `\top`
  is not in the wrapper's symbol table, so transpose is authored as `^{T}` in the Choice.
- 033: `f(x)\;=\;\dfrac{x^{2}\cos(x)-x}{10}`, 16.5pt 000000 (sidecar
  `qa/slide033/eq_033_main_v7b.json` fontsize; slide_033.js comment says \dfrac).
- 034: `f(x) = \frac{x^2 \cos(x) - x}{10}`, 18pt 000000 (verbatim from `build/gen_eq_034.py`).
- 031/032: reused banked manifests, mathtext `f(x)=(x-5)^{2}+1` (24pt / 15pt, 000000).

## Verification details

- Wrap mechanics: `python3 scripts/18_omml_wrapper.py <pptx> <manifest> -o $TMPDIR/wrap_N.pptx`
  then mv over the plain-named deliverable. rc=0 everywhere. Zip diff vs preOMML backup touches
  ONLY `ppt/slides/slide1.xml`; media byte-identical; rels/content-types untouched; slide XML
  well-formed (ElementTree). AltContent blocks: 014=3, 033=1, 034=1 (031/032=1 each, pre-existing).
- Backups: `$NS/recreated_pptx/qa/slideNNN/slide_NNN_recreated.preOMML.bak.pptx` (for 031/032
  the backup banks the already-wrapped state, since the pre-wrap bytes were replaced by shard-2
  before this worker arrived; shard-2's md5 before/after in OMML_WRAP_LOG.md is the wrap record).
- 0-px proof per slide: separate LO profiles, `soffice --headless --convert-to pdf`,
  `pdftoppm -r 150 -singlefile -png`, PIL diff of page 1: **0 differing pixels** on all 5.
- Deck: `final_deck_tool.py update {14,31,32,33,34}` + `render_check_pages.py` each ->
  **PASS (0 px)**; final deck md5 after all five updates:
  `1966dcc3c489600da188df2b781a1d8c` (51 pages, structure OK). Gate artifacts under
  `recreated_pptx/qa/final_deck_updates/gate_20261101-*_pNN`.
- Per-slide logs: `$NS/recreated_pptx/qa/slideNNN/omml_wrap_log.txt`.
- Wrapper run logs: `$RJ/slideNNN/wrap_run_NNN.log` (014/033/034).

## Not done / notes

- No slide was blocked-on-wrapper: the on-disk wrapper already handles every construct used
  here (no `\underline` in this shard's mathtext anyway).
- Deck pages for other shards (4/5/15/21/23/30/37/44/48/50/51 etc.) are owned by other workers;
  not touched.
