# Comparison — slide_057 (doc-parse vs certified ground truth)

## Call inventory (protocol naming)

| dir | params | EXIT | finish_reason | out_tokens | chars | latency | stderr |
|---|---|---|---|---|---|---|---|
| `03_parses/slide_057/call01_pass1` | `--max-output-tokens 1024` | 0 | **length** | 1024 (maxed) | 4123 | 64.0 s | 0 lines |
| `03_parses/slide_057/call02_pass2` | `--max-output-tokens 3000` | 0 | **length** | 3000 (maxed) | 12027 | 109.0 s | 0 lines |
| `03_parses/slide_057/call03_retry_pass1` | 1024 (retry of pass1) | 0 | **length** | 1024 (maxed) | 4123 | 66.4 s | 0 lines |
| `03_parses/slide_057/call04_retry_pass2` | 3000 (retry of pass2) | 0 | **length** | 3000 (maxed) | 12027 | 115.3 s | 0 lines |

`call02_pass2` and `call04_retry_pass2` transcripts are **byte-identical** (cmp). `call01` vs `call03` differ only inside the degenerate tail's Encoder/Decoder alternation; their unique-line sets are identical. All four calls collapse to the same **6 unique lines**, then a `"Decoder"` repetition loop that consumes the entire token budget (`Decoder` ×482 in the 1024-budget calls, ×1470 in the 3000-budget calls). The 21-line prefix is identical across all four.

Per protocol, `finish_reason != "stop"` = FAILED CALL; retries were run (fresh dirs) and also failed identically → the truncation is budget-independent model degeneration, not a transient. The two protocol-named dirs (`call01_pass1`, `call02_pass2`) hold the five required files each, EXIT 0, non-empty content — but NOT `finish=stop`; this is recorded as a DB task (blocker) and drives `finish_all_stop = 0` in wave-2. All numbers below are measured on these truncated transcripts.

## 1. Text fidelity

GT string list = 48 deduplicated build strings (primary, see `04_ground_truth/slide_057/inventory.md`) + 8 analysis-only strings (union 56). Classification per protocol (EXACT = case/whitespace-insensitive equality ignoring coordinate tokens; NORMALIZED = equality after punctuation/spacing collapse + named glyph confusions; PARTIAL = substring with ≥60% shared tokens).

Per-call results are identical across all four calls:

- **EXACT (5):** `57` (from `<x_0.0586><y_0.0789>57`, coordinate prefix ignored) · `Encoder` · `Decoder` · `Encoder Block 2` · `Residual Connection and Layer Normalization`
- **NORMALIZED (1):** GT `Feed Forward Networks - One Hidden with RELU Activation` ← parse `Feed Forward Networks / One Hidden with RELL Activation` (confusions: hyphen↔slash, U↔L in RELU)
- **PARTIAL (0)** — e.g. parse `Encoder` alone vs GT `Encoder Block M/1/0` shares only 1/3 tokens; not partial.
- **MISSING (42):** all 16 `X_*`/`Y_*` chips; all 8 `Word N` labels; `Word Embedding`; `Positional  Encoding / Embedding`; `Attention`; `Encoder Block M/1/0` (only "2" detected); `Encoder Decoder Attention`; `Multi-Head Self-Attention`; `Softmax`; `K`; `V`; `Q`; `Word and Position Encoding`; `SOS`; `Je`; `ne`; `suis`; `faisait` — plus (union list) `Tokens`, `POS`, `m/t/de [?]`, `X_N`, `Y_N`, `Masked Multi-Headed Attention`, `Word and Position Embedding`, `Multi-Head [?]`.

**text_recall = (5 EXACT + 1 NORMALIZED + 0.5·0 PARTIAL) / 48 = 6/48 = 12.5%** (identical for both passes; 6/56 = 10.7% against the analysis-union list).

**HALLUCINATION CANDIDATES: none** — every unique parse line maps to a GT string ("Decoder"/"Encoder" are GT panel labels). The degeneration manifests as massive *repetition*, not invention: 482–1470 duplicate `Decoder` lines with no coordinates or class tokens. No content string in the parse lacks a GT counterpart, so nothing is queued for hallucination adjudication; the repetition loop itself is a reliability defect, not a content claim.

## 2. Layout & coordinates

- Parse distinct **positioned items** (lines carrying `<x_…><y_…>`): **1 of 502 lines** (call01) / **1 of 1490** (call02). Both passes emit exactly one: `<x_0.0586><y_0.0789>57`.
- Token→frame-px conversion (px = token×960 for x, ×540 for y): x 0.0586 → **56.3 px**, y 0.0789 → **42.6 px**.
- Matchable pair (same text "57"): build badge numeral box x875..911, y53..89 (center 893,71). Parse point (56.3, 42.6) → **distance to badge center ≈ 837 px** (≈ 819 px to the box corner) — 10× beyond the ~80 px tolerance. The single coordinate is mis-anchored (lands in the top-left margin, the badge is top-right).
- Fraction of parse items landing inside the frame: 1/1 = 100% (56.3, 42.6 is on-frame). Fraction within ~80 px of the nearest GT element: **0/1 = 0%** (nearest GT text, the vertical `Encoder` label at x≈73..89/y256..360, is ≈214 px away).
- Build shape/region count vs parse detected-region count: build = 113 helper-call sites ≈ **820 drawn primitives** in 4 macro-regions (+chrome); parse = **0 declared regions, 0 class tokens, 1 positioned item**. The parse carries essentially none of the layout.

## 3. Structure fidelity

- Class tokens (`<class_…>`): **0** in all four calls. No section-header/list/table/chart/region markup of any kind.
- Equations: GT has none (`equations: []`); parse has none — correct rejection, N/A.
- Charts/tables: GT has none; parse none — N/A.
- What the parse CANNOT carry that the build encodes (all absent here): ~60 palette hexes; frame-px geometry for ~820 primitives; fonts (Arial + Times New Roman serif-italic chips, 5–20pt, two 270°-rotated vertical labels); shape semantics (up/down/right arrows, hatched arrows, arcs with angleRange, dashed/solid lines, roundRects, 3-D shadow pairs); z-order (decoder → central → encoder); the badge-numeral law; multi-run text (chip letter+subscript pairs, 3-line attention-box stacks).
- The diagram's *structure* (4 encoder bars, 3 decoder blocks, 20 attention boxes, 17-circle row, K/V/Q feed badges, token rows) is entirely absent — the parse reads like 6 labels of a much simpler slide, then loops.

## 4. Reliability

| metric | call01 | call02 | call03 | call04 |
|---|---|---|---|---|
| EXIT | 0 | 0 | 0 | 0 |
| finish_reason | length | length | length | length |
| output_tokens | 1024 | 3000 | 1024 | 3000 |
| content chars | 4123 | 12027 | 4123 | 12027 |
| latency (script) | 64.0 s | 109.0 s | 66.4 s | 115.3 s |
| stderr lines | 0 | 0 | 0 | 0 |
| unique lines | 6 | 6 | 6 | 6 |
| repetition loop | `Decoder` ×482 | `Decoder` ×1470 | `Decoder` ×482 | `Decoder` ×1470 |

- `finish_all_stop` over successful calls = **0/4** (all four truncated at their token budgets; retries reproduced the failure exactly, pass2 pair byte-identical).
- Corroboration (pass1 vs pass2): detected-GT-set **Jaccard = 1.000** (both = the same 6 strings). Strings found in only one pass: **none** — but corroboration here is degenerate: pass2 is the same 21-line prefix with a longer loop, not a richer read. Nothing on this slide is meaningfully "corroborated"; everything detected is effectively single-read-quality output from a collapsed generation.
- Shared-resource health: no HTTP 429/5xx, no auth errors, no DB locks encountered; latency variance (64→66 s, 109→115 s) is normal endpoint load. The failure is intrinsic to this image+prompt+budget combination (densest slide in the set).
- Bottom line (protocol): this is not an empty parse (it carried 6 GT strings), so it is not the protocol's hard-FAIL case, but a builder could not reconstruct the slide from it — recreation_power is near floor (wave-2 will score it).

## Claims for image adjudication

1. The parse degenerates into a `Decoder` repetition loop (482× at 1024 tokens, 1470× at 3000) after 6 unique lines — verify: the image is a normal schematic (panel + bars + circles), i.e. the loop is model degeneration, not literal repeated "Decoder" text on the slide.
2. The parse's only positioned item `57` maps to (56.3, 42.6) px, top-LEFT margin — verify: the "57" numeral badge actually sits top-RIGHT (build box x875..911, y53..89), i.e. the single coordinate token is mis-anchored.
3. 42/48 build GT strings are missing (all X_*/Y_* chips, Word row, both embedding bars, K/V/Q, SOS/Je/ne/suis/faisait, Softmax, 3 of 4 Encoder Block bars…) — verify: these labels exist on the image with legible ink (the certified build derives from this same frame), confirming the truncation lost them.
4. `Encoder Block 2` was detected but `M/1/0` were not — verify: all four bar labels ("Encoder Block M", 2, 1, 0) are present and similarly legible on the image.
5. The FFN bar was misread as `Feed Forward Networks / One Hidden with RELL Activation` — verify: the image reads `Feed Forward Networks - One Hidden with RELU Activation` (hyphen separator; RELU, not RELL).
6. Build vs analysis wording: decoder purple bar — build `Word and Position Encoding` vs analysis `Word and Position Embedding` — verify on-image which wording is printed.
7. Build vs analysis wording: the 5 masked-attention boxes — build `Multi-Head Self-Attention` vs analysis `Masked Multi-Headed Attention` — verify on-image.
8. Build vs analysis chip law: last token chips — certified 0-BASED law says `X_{N-1}`/`Y_{N-1}` is the final chip; analysis lists an extra `X_N`/`Y_N` — verify the last chip subscript on-image.
9. `Softmax` bar: present in the build (over the 17-circle row) but absent from the analysis label list — verify the maroon bar text on-image.
10. Bottom token row: build labels it `SOS / Je / ne / suis / faisait` (French sentence); analysis calls the boxes unlabeled — verify the tiny red text inside the 5 bottom token boxes.
