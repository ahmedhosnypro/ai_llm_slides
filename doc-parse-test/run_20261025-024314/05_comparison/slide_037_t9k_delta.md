# t9k delta report — slide_037 (`slide_037_t9k`, wave-3 addendum)

Scope: `slide_037_t9k` · worker: `worker-slide_037_t9k` · wave 3 (t9k retry,
2026-10-25). Additive-only report; frozen wave-2 artifacts
(`05_comparison/slide_037_comparison.md`, `07_registers/`,
`08_final/scores_slide_037.csv`, `08_final/scores.csv`) are untouched.

Question: does `--max-output-tokens 9000` (API ceiling) change what doc-parse
returns for slide_037 vs the wave-2 1024-token pass (`call01_pass1`) and
3000-token corroboration pass (`call02_pass2`)?

Inputs (all read-only): `03_parses/slide_037/call05_t9k/`,
`call06_t9k_retry/`, `call01_pass1/`, `call02_pass2/`,
`04_ground_truth/slide_037/inventory.md` (29 unique GT labels),
`08_final/scores_slide_037.csv` (frozen wave-2: recall 79.3, exact 22,
normalized 1, partial 0, missing 6, hallucinated_confirmed 3 groups/4 strings).
No image reading, no new vision adjudication; parse content is DATA.

## 1. Call record

| call | EXIT | finish_reason | output_tokens | content chars | unique non-empty content lines | latency | stderr lines |
|---|---|---|---|---|---|---|---|
| call05_t9k | 0 | stop | 27 | 166 | 2 | 3.7 s | 0 |
| call06_t9k_retry | 0 | stop | 27 | 166 | 2 | 5.8 s | 0 |

Both calls valid per protocol (EXIT 0, finish stop, non-empty string content).
Neither failed, but call06 was run anyway as a one-shot variance check because
call05 came back byte-identical to the wave-2 3000-token pass in 3.7 s (pass2
took 128.3 s for the same bytes) — worth one corroboration read.

t9k content (both calls, verbatim — 2 lines):

```
<x_0.1104><y_0.1>**Transformer Blocks (stacked over Multi-Head)** 37<x_0.9277><y_0.168><class_Section-header>

<x_0.0615><y_0.0773><x_0.9199><y_0.9531><class_Picture>
```

For context, wave-2 calls: call01_pass1 (1024) = EXIT 0, stop, 133 tokens,
535 chars, 28 content lines, 51.8 s; call02_pass2 (3000) = EXIT 0, stop, 27
tokens, 166 chars, 2 lines, 128.3 s.

Observation (hypothesis, not confirmed): two independent t9k calls and pass2
produced **byte-identical** content while latencies differ ~35× (128.3 s vs
3.7 s) — consistent with an endpoint-side cache hit on the repeated identical
request, and proof the minimal read is deterministic/stable here, not a
transient degeneration.

## 2. Delta vs the 1024/3000 passes

t9k detected exactly 2 GT strings: the title `Transformer Blocks (stacked over
Multi-Head)` and the badge numeral `37` (one Section-header line). This set is
a **strict subset of pass1's** detections and **identical to pass2's**.

**NEW strings (in t9k, absent from both earlier passes): NONE.**
- NEW REAL-GT: 0
- NEW NOT-IN-GT (hallucination candidates, transcript-vs-GT only, single-read):
  0

**LOST strings (detected by pass1 at 1024 tokens, absent from t9k): 21 GT
labels** — `Encoder`, `Output`, `Probabilities`, `Softmax`, `Linear`,
`WE ARE HERE`, `Scaled Dot-Product Attention`, `Multi-Head Attention`,
`MatMul`, `Concat`, `Nx` (GT `N x`), `Mask (opt.)`, `Scale`,
`Positional Encoding`, `Input Embedding`, `Q`, `K`, `V`, `Inputs`,
`Outputs`, `(shifted right)`. Also absent from t9k are pass1's four garble
strings that wave-2 confirmed as hallucination candidates (`Scalar
Dot-Product Attention`, `Mult-Head Attention`, `Math-Head Attention`, `Max`):
t9k dropped the hallucinations along with the real text. Relative to pass2,
t9k lost nothing (pass2 had only title + badge already).

**Changed wording: none.** t9k output is byte-identical to call02_pass2
(166 chars, `diff` empty) and byte-identical between call05 and call06.

**Layout/coordinates delta:** none. t9k carries the same 2 positioned items as
pass2. Token→frame-px (px = token × 960 / × 540): Section-header
`x0.1104,y0.1 → x0.9277,y0.168` = box (106.0, 54.0)–(890.6, 90.7): starts
~10 px from the GT title box origin (96, 50 800×50) and its right end lands on
the badge numeral box (875,53 36×36) — inside the frame, within ~80 px of
nearest GT element (2/2 items = 100%). Picture `x0.0615,y0.0773 →
x0.9199,y0.9531` = box (59.0, 41.7)–(883.1, 514.7): the one mega-region
covering all three GT diagram regions (build: 7 analysis regions, 268 draw
calls → parse: 1 region + 1 header item). Same as pass2; zero new geometry.

**Structure delta:** none. Class tokens unchanged (`class_Section-header`,
`class_Picture`): the dense 3-diagram vector slide is still reduced to a
single Picture region with no inner text, no per-diagram roles, and nothing of
the build's colors/fonts/z-order/occlusion/rotation (untransportable, as in
wave 2).

## 3. Recall estimate (transcript-level, t9k alone)

GT total = 29 unique labels (inventory). t9k: EXACT 2 (title, `37`),
NORMALIZED 0, PARTIAL 0, MISSING 27.

**t9k recall = (2 + 0 + 0.5·0) / 29 = 2/29 = 6.9%** — vs the frozen wave-2
recall of **79.3%** (pass1-primary at 1024 tokens; pass2-primary would be
6.9%). Delta: **−72.4 points** vs the wave-2 primary read. This is a
transcript-level estimate only: no new pixel adjudication was performed in
this wave (the wave-2 vision verdicts stand untouched); per-call rec-
corroboration Jaccard between the two t9k calls = 1.0 on detected GT strings
(identical set {title, 37}), so the t9k figure is effectively a corroborated
double-read of the minimal output.

## 4. Verdict

**No — 9000 max-output-tokens does not change the picture for slide_037.**
- The token budget is not the binding constraint: t9k used **27 of 9000**
  output tokens. The parser's own content decision — collapse the dense
  3-diagram slide into one `<class_Picture>` — is what caps the yield, and at
  9000 it made the same decision as at 3000.
- Output is byte-identical across call05, call06, and the wave-2 3000 pass:
  the minimal read is stable and reproducible, and there is no repetition-loop
  or truncation to break (this is not a 057-type failure; finish stop, tiny
  output).
- Consequence: at this endpoint, raising the ceiling does not recover the
  21 diagram labels that the 1024-token pass1 happened to emit. Pass1's
  richer read (79.3%) looks like sampling variance in the parser's
  text-vs-picture decision, not a budget effect — the LOW ceiling read the
  diagram, the HIGH ceilings skipped it.
- Recreation power from a t9k transcript alone would be worse than the frozen
  wave-2 2/10 (≈1/10: title + badge + "a picture exists"), but wave-2 scores
  are frozen and stand; this report adds the t9k evidence only.

No new claims for image adjudication arise from this wave (nothing new was
detected; all wave-2 claims/vision verdicts stand as frozen).
