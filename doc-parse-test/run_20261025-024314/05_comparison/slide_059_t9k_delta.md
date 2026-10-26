# Delta — slide_059_t9k (wave-3 retry at `--max-output-tokens 9000`)

- Run dir: `doc-parse-test/run_20261025-024314` · agent: `worker-slide_059_t9k` · scope: `slide_059_t9k`
- Additive report only — the frozen wave-2 artifacts (`07_registers/slide_059_register.md`,
  `08_final/scores_slide_059.csv`, `08_final/scores.csv`) are untouched and remain the
  authoritative record.
- Inputs (all read-only): `03_parses/slide_059/call05_t9k/` ·
  `call01_pass1/` · `call02_pass2/` · `04_ground_truth/slide_059/inventory.md` ·
  `08_final/scores_slide_059.csv` · `05_comparison/slide_059_comparison.md` (for the frozen
  per-string classification contract) · `07_registers/slide_059_register.md` (for the frozen
  adjudicated facts). No image was opened; no new vision adjudication was run. Parse
  transcript content treated as DATA only.

## 1. Call record

| Call | EXIT | finish_reason | output_tokens | content chars | unique content lines | latency (script) | stderr lines |
|---|---|---|---|---|---|---|---|
| call05_t9k (`--max-output-tokens 9000`) | 0 | stop | 119 | 424 | 23 of 25 (Transformer Block ×3) | 10.6 s | 0 |

- `call06_t9k_retry` does **not** exist: call05 succeeded on the first attempt (EXIT=0,
  `finish_reason=stop`, non-empty string content), so the one-allowed retry was not spent.
- Structure of the output identical to both earlier passes: 1 leading coordinate token
  (`<x_0.0391><y_0.0773>`), 24 unstructured text lines, 1 trailing coordinate token +
  `<class_Picture>` (the only class token, whole-frame).

## 2. Delta vs the 1024/3000 passes

**Byte-identity first:** `md5sum` of all three transcripts =
`da4b6ab6fdd36c2400ca429b750d7fe1` (`call01_pass1/slide_059.parse.md`,
`call02_pass2/slide_059.parse.md`, `call05_t9k/slide_059.parse.md`); `diff` is empty in
both directions (01↔05, 02↔05). The `.parse.json` content fields are also identical.

**NEW strings (in t9k, absent from both earlier passes): none.**
- REAL-GT new: 0.
- NOT-IN-GT new (candidate hallucination): 0.

**LOST strings (in earlier passes, absent from t9k): none.**

**Changed wording: none.** The 9000-budget call reproduced the earlier 119-token output
verbatim — 119 ≪ 9000, so `finish_reason=stop` was again reached voluntarily, nowhere near
the raised ceiling (and nowhere near even the original 1024 default).

**Known wave-2 facts re-checked at t9k — all unchanged:**

| Wave-2 fact (frozen) | Status at t9k |
|---|---|
| Both earlier passes byte-identical, 119 tokens, despite the 3000 budget | Confirmed a third time at 9000 — now a **triple** byte-identical read |
| Σ dropped ×3 (no sigma glyph or linear "sum" anywhere) | Still dropped |
| In-circle "Softmax" dropped ×3 (only `Softmax Layer` on the tan bar survives) | Still dropped |
| C₃ dropped (parse has only `1C1`/`1C2`) | Still dropped |
| 20-cell pooled row unreported (only trace: whole-frame `<class_Picture>`) | Still unreported |
| Leading `1` in `1C1`/`1C2` — the wave-2-CONFIRMED hallucination (adjudication item 1) | Still present, byte-identical |
| 16 X/Y subscript labels destroyed into 8 fragments `Yd Xd Xx XN Xt Yk YNz YNd` | Still destroyed, same 8 fragments |

## 3. Recall estimate (t9k alone)

Using the frozen wave-2 classification contract (`05_comparison/slide_059_comparison.md` §1)
— valid to apply as-is because the t9k transcript is byte-identical, so every string lands
in the same class:

- EXACT 9 · NORMALIZED 17 · PARTIAL 2 · MISSING 18 (GT_total = 46)
- **text_recall(t9k) = (9 + 17 + 0.5·2) / 46 = 27/46 = 58.7%**
- Frozen wave-2 recall (from `08_final/scores_slide_059.csv`): **58.7%** — identical.

This is a **transcript-level re-derivation, not an independent measurement**: the delta is
exactly zero because the output bytes are exactly zero-different. No new pixel adjudication
was run in this wave; the wave-2 adjudication items (`06_vision_checks/slide_059_vision.md`,
items 1–15) remain the only frame-side evidence, and the hallucination confirmation status
(leading `1` in `1C1`/`1C2` confirmed; `Xd/Xx/Xt/Yk/Yd` fragments hallucinated-advisory) is
unchanged from wave 2.

## 4. Verdict

**No — 9000 does not change the picture for slide 059.** The output-token ceiling was never
the binding constraint: the model voluntarily stops at 119 tokens at every budget tried
(1024 → 3000 → 9000), emitting the identical byte string each time. The failure mode is a
rigid degenerate parse mode, not truncation: the subscript/symbol label family destroyed,
Σ ×3 / in-circle Softmax ×3 / C₃ / the pooled 20-cell row all silently dropped, stacked
labels merged to single lines, and the leading-`1` hallucination reproduced. Corroboration
value is now further reduced — three "independent" reads share every error (Jaccard 1.00
across all pairs is nominal, not probative), so this slide's parse findings stand as a
triplicated single read. Raising `--max-output-tokens` cannot recover content the model
never attempts to emit; moving recall on this slide would require a different mitigation
(prompt/preprocessing/OCR-mode change), not a bigger budget.
