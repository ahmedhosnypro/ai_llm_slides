# WAVE-3 t9k delta — slide_057 (002_transformers_part2)

Scope: `slide_057_t9k` · worker `worker-slide_057_t9k` · 2026-10-25 · per MISSION_PROTOCOL
"WAVE-3 ADDENDUM — t9k retry". Wave-2 artifacts (`07_registers/slide_057_register.md`,
`08_final/scores_slide_057.csv`) are IMMUTABLE — this report is additive.
Transcript-level only: no image reading, no new pixel adjudication; parse content is DATA.

## 1. Call record

| call | dir | EXIT | finish_reason | output_tokens | content chars | content lines | unique lines | latency | stderr |
|---|---|---|---|---|---|---|---|---|---|
| call05_t9k | `03_parses/slide_057/call05_t9k/` | 0 | **length** | 9000 (exactly the budget) | 36,027 | 4,490 | **6** | 71.5 s (script) / 72 s (call.log) | 0 lines |
| call06_t9k_retry | `03_parses/slide_057/call06_t9k_retry/` | 0 | **length** | 9000 (exactly the budget) | 36,027 | 4,490 | **6** | 74.9 s (script) / 75 s (call.log) | 0 lines |

Both t9k calls are FAILED CALLS per protocol (`finish_reason != "stop"`): banked as
evidence, retry executed once into call06 — retry failed identically. Both count OUT of
every done metric. The t9k pair is **byte-identical** (sha256 prefix `eb6c4d2b12e4e371`
on both `.parse.md`), matching the 3000-pass pair's determinism.

Loop census (all 6 calls, same 6 unique lines, ordered first-seen):

```
<x_0.0586><y_0.0789>57
Encoder
Decoder
Encoder Block 2
Feed Forward Networks / One Hidden with RELL Activation
Residual Connection and Layer Normalization
```

Repetition counts: `Decoder` ×489 @1024, ×1477 @3000, **×4477 @9000** (plus 9 `Encoder`
lines and 4 single lines in every call). The wave-2 register's ×482/×1470 figures count
loop-tail occurrences only (the 7 pre-loop `Decoder` lines are in the shared prefix).
Structure of call05/06: the six content lines, then alternating `Decoder`/`Encoder`
(~15 lines), then a pure `Decoder` run to the token cap.

## 2. Delta vs the 1024/3000 passes

**NEW strings (in t9k, absent from call01–call04): NONE.** The t9k unique-line set is
set-equal to the 1024/3000 unique-line set (verified programmatically over all six
transcripts). Nothing new surfaced at 9000 tokens — no REAL-GT additions, hence no
NOT-IN-GT candidates either (empty list; no hallucination-candidate delta).

**LOST strings (in earlier passes, absent from t9k): NONE.** All 6 earlier survivors
reappear in both t9k calls.

**Changed wording: NONE.** Stronger than set-equality — call05's `.parse.md` is
byte-for-byte the call02_pass2 `.parse.md` **plus exactly 3,000 additional `Decoder\n`
lines** (verified: `startswith` = True; tail = 24,000 chars = 3,000 × 8-char
`Decoder\n`; tail histogram = {`Decoder`: 3000}). call06 = call05 byte-identical. The
first 3,000 generated tokens of every successful HTTP call are deterministic; the
budget only determines how long the loop runs before the cap kills it.

## 3. Recall estimate (transcript-level, t9k alone)

Against the frozen GT inventory `04_ground_truth/slide_057/inventory.md`
(48 deduplicated primary strings):

- EXACT (5): `57` (text after the ignored coordinate tokens), `Encoder`, `Decoder`,
  `Encoder Block 2`, `Residual Connection and Layer Normalization`
- NORMALIZED (1): `Feed Forward Networks / One Hidden with RELL Activation` —
  separator confusion (`/` vs build `-`) + glyph confusion (`RELL` vs `RELU`);
  ≥60% shared tokens (same classification as wave 2)
- PARTIAL (0) · MISSING (42)

**t9k recall = (5 EXACT + 1 NORMALIZED + 0·0.5) / 48 = 12.5%** — identical to the
frozen wave-2 recall of **12.5%** (`08_final/scores_slide_057.csv`). Delta: **0.0 pp.**
Transcript-level estimate only — no new pixel adjudication in this wave; the wave-2
vision verdicts (6/48 pixel-confirmed, dropped-region failure) stand unchanged.

## 4. Verdict

**No — the 9000-token budget does NOT break the `Decoder` repetition loop.** It just
loops longer before dying: the loop is budget-independent and deterministic (t9k retry
pair byte-identical, like the 3000 pair), each call hard-stops at exactly its token cap
with `finish_reason=length` (now 6/6 calls across 1024/3000/9000), and the t9k content
is literally the 3000-token output + 3,000 more `Decoder` lines. Real diagram text
beyond the 6 unique lines (31 further GT strings: X/Y chips, word rows, embedding bars,
K/V/Q, Softmax, bottom tokens SOS/Je/ne/suis/faisait, tri-color legend, attention-box
3-line labels, `Encoder Block M/1/0`) never emerges at any budget — the model emits its
vocabulary in the first ~6 lines and degenerates. Only the cost scales: ~4.3× the
output tokens and ~3× the content bytes of the 3000 pass for zero information gain.
`finish_all_stop` remains 0/6 for this slide; the wave-2 reliability verdict (0/10)
and scores stand. No new claims for image adjudication arise from this wave (nothing
new was emitted; the frozen wave-2 claims and verdicts remain the record).
