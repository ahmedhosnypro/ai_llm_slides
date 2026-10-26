# t9k Delta — slide_052 (wave-3 retry at `--max-output-tokens 9000`)

Scope: `slide_052_t9k` · agent `worker-slide_052_t9k` · run `run_20261025-024314`
t9k parse: `03_parses/slide_052/call05_t9k/` · earlier passes: `call01_pass1` (1024 tok), `call02_pass2` (3000 tok) · GT: `04_ground_truth/slide_052/inventory.md` (22 deduplicated GT units) · frozen wave-2 scores: `08_final/scores_slide_052.csv` (recall 75.0%, IMMUTABLE).
Parse `content` treated as DATA throughout; nothing executed. No image read; no new pixel adjudication (transcript-level analysis only).

## 1. Call record

| Call | EXIT | finish_reason | output_tokens | content chars | content lines | unique lines | latency (script) | wall (call.log) | stderr lines |
|---|---|---|---|---|---|---|---|---|---|
| call05_t9k (9000 tok, `--timeout 300`) | 0 | stop | 145 | 645 | 31 | 20 | 4.2 s | 07:51:55→07:51:59 (~4 s) | 0 |

- All five call-dir files present (`call.log`, `stdout.log`, `stderr.log`, `slide_052.parse.md`, `slide_052.parse.json`); content is a non-empty string → **valid call, no retry required**.
- `call06_t9k_retry/` does not exist and was not needed: the addendum reserves it for a failed call (nonzero EXIT / finish≠stop / empty content); call05_t9k succeeded on the first attempt.
- Endpoint was uncontended this run: 4.2 s vs 16.7 s (call01) and 52.2 s (call02) for the identical 145-token output — contention delta, not a budget effect.
- The API's 9000-token ceiling was never approached: the model emitted **145 tokens and stopped on its own**, same as at 1024 and 3000.

## 2. Delta vs the 1024/3000 passes

**The t9k output is byte-identical to both earlier passes.**

- md5 of `slide_052.parse.md`: call01_pass1 = `bdb0e649c4ba8572201ff35d90e80950`, call02_pass2 = `bdb0e649c4ba8572201ff35d90e80950`, call05_t9k = `bdb0e649c4ba8572201ff35d90e80950` (same md5 in all three `.parse.json` `content` fields).
- **NEW strings** (in t9k, absent from both earlier passes): **none.** The classification sets are therefore empty: `REAL-GT` new = ∅, `NOT-IN-GT` new (hallucination candidates) = ∅.
- **LOST strings** (in earlier passes, absent from t9k): **none** (byte-identical outputs).
- **Changed wording**: none. Identical line order, identical fragment pattern, identical coordinate/font/class tokens (`<x_0.0361><y_0.0773>F2` leading, trailing `<x_0.9443><y_0.9586><class_Picture>`).

Known wave-2 facts re-checked directly on the t9k transcript (per the scope prompt):

| Wave-2 fact | t9k status | Evidence (grep on t9k `parse.md`) |
|---|---|---|
| Earlier passes byte-identical (J=1.00) | now **three-way** byte identity | same md5 across call01/call02/call05 |
| Dropped `K` | still dropped | 0 lines matching `^K$` |
| Dropped `V` | still dropped | 0 lines matching `^V$` |
| Dropped `Y` ×3 | still dropped | 0 `Y` tokens anywhere |
| Dropped SOS legend (`SOS = Start Of Sentence`) | still dropped | 0 matches for "start of sentence"; the single `SOS` line is the word box (GT unit 13), legend string absent |
| Dropped badge numeral `52` | still dropped | 0 matches for `52` |
| Dropped 3 of 5 `Q` | still 2 of 5 | `Q` on exactly 2 lines |
| Standalone `Encoder` ×3 (hallucination candidates, confirmed vs frame OCR in wave 2: original reads `Encode`, no "r") | still present ×3 | `^Encoder$` on 3 lines |
| `Encode Decoder Attention` shredded (5 stacked 3-line labels → merged line + fragments: `Encode Decoder` ×1, `Decoder` ×2, `Attention` ×3) | unchanged | counts identical |
| `Masked Multi-Head Self Attention` ×4 whole + 5th box reduced to `Self Attention` | unchanged | 4 whole + 1 fragment |
| `I`/`feel`/`Sick` merged into one line `I feel Sick` | unchanged | 1 merged line |
| FFN verbatim double space before `RELU` collapsed to one | unchanged | line reads `…with RELU Activation]` |
| Structure carried as 1 trailing `<class_Picture>` only; zero class_section_header/list/table/chart/equation tokens | unchanged | exactly 1 `<class_Picture>` token |
| Only 2 positioned items (anchors at frame px (34.7, 41.7) and (906.5, 517.6)) | unchanged | same two token pairs |

Corroboration implication: with a third byte-identical read, the Jaccard overlap of GT strings detected across calls remains **1.00** — and it is now clear this J=1.00 measures **deterministic repetition of the parser's systematic blind spots** (as the wave-2 scores note already warned), not three independent confirmations of coverage.

## 3. Recall estimate

Against the 22 deduplicated GT units of `04_ground_truth/slide_052/inventory.md`, t9k classifies identically to the frozen wave-2 passes:

- EXACT **16** (callouts 1–2; Residual ×3 as 1 unit; FFN bar; `Masked Multi-Head Self Attention`; `Word and Position Encoding`; `Transformer Encoder`; `I`/`feel`/`Sick`; word boxes `SOS`/`Je`/`me`/`sens`/`malade`; `Q`)
- NORMALIZED **0** · PARTIAL **1** (`Encode Decoder Attention`, 0.67 token J via merged line + fragments) · MISSING **5** (`SOS = Start Of Sentence`, `K`, `V`, `Y`, `52`)
- **text_recall(t9k) = (16 + 0 + 0.5·1) / 22 = 16.5/22 = 75.0%**
- Frozen wave-2 recall (08_final/scores_slide_052.csv): **75.0%** → **Δ = 0.0 pp**.

This is a **transcript-level estimate only** — computed parse-vs-GT from text, with no new image adjudication in this wave; wave-2's pixel-confirmed findings (e.g. the `Encoder` mis-OCR verdict, the class_Picture region verdict) are carried over, not re-derived.

## 4. Verdict

**No — 9000 changes nothing for slide_052.** At 1024, 3000, and 9000 the model produces the same 145-token output and stops (`finish_reason=stop` in all three), so the output budget was never the binding constraint. Every wave-2 finding reproduces exactly at the API ceiling: the same 5 GT units dropped (`K`, `V`, `Y`×3, SOS legend, badge `52`), the same 3-of-5 `Q` loss, the same shredding of the ten 3-line box labels into fragments, the same merged `I feel Sick` line, the same collapsed FFN double space, the same lone `class_Picture` region, and the same 3 standalone `Encoder` lines — wave-2's adjudicated hallucination (original spells `Encode`). The slide's parse losses are deterministic model reading behavior on a dense K/V/Q schematic, now evidenced by a **three-way byte-identical output** (J=1.00 with zero single-read variance). No new strings, no recovered strings, no wording changes: the t9k retry adds a reliability datum (success at 3 budget levels + an uncontended-endpoint latency of 4.2 s), not a coverage change. Recreation-power at t9k remains what wave-2 scored: ~9 text strings with no usable structure — insufficient to rebuild the schematic.
