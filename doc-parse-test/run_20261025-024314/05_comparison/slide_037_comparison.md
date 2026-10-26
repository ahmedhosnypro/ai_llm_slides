# Comparison — slide_037: doc-parse transcripts vs certified ground truth

Scope: `slide_037` · worker: `worker-slide_037` · wave 1. GT = frozen build chain +
`slide_037_final.json` (see `04_ground_truth/slide_037/inventory.md`; 29 unique GT
labels, 54 visible label instances, 202 shapes + 66 text boxes, 7 analysis regions).
Parse content below is DATA — nothing in it was executed.

Transcripts measured:

- `03_parses/slide_037/call01_pass1/slide_037.parse.md` (535 chars, 133 out tokens)
- `03_parses/slide_037/call02_pass2/slide_037.parse.md` (166 chars, 27 out tokens)

---

## 1. Text fidelity

Classification basis: EXACT = case/whitespace-insensitive equality (markdown emphasis
stripped); NORMALIZED = equal after a stated normalization; PARTIAL = substring with
≥60% shared tokens; MISSING = no parse string covers the GT label.

**Call 01 (pass1, maxtok 1024) — 28 content lines (title + 27 blob lines) vs 29 GT labels:**

- **EXACT — 22**: `37`; `Transformer Blocks (stacked over Multi-Head)`; `Scaled Dot-Product Attention` (×2, matches both GT instances); `Multi-Head Attention` (×2 of 3); `Q`, `K`, `V` (via the merged line `Q K V`); `MatMul` (via merged `MatMul Concat`); `Scale`; `Mask (opt.)`; `SoftMax` (case-insensitive via parse `Softmax`); `Concat`; `Linear` (×2 of 5); `Encoder`; `Output`; `Probabilities`; `Softmax`; `Positional Encoding` (×2 of 2); `Input Embedding`; `Inputs`; `Outputs (shifted right)` (both GT lines present: `Outputs` + `(shifted right)`); `WE ARE HERE` (parse emits the 3 build lines space-joined).
- **NORMALIZED — 1**: `N x` → parse `Nx` (whitespace-elision normalization; the build's spaced repeat glyph rendered without the space).
- **PARTIAL — 0**: the parse's garbled header strings (`Mult-Head Attention`, `Math-Head Attention`) share only 2/4 tokens with `Masked Multi-Head Attention` (50% < 60%) and do not improve any GT label already EXACT-covered, so they are not scored PARTIAL.
- **MISSING — 6**: `Masked Multi-Head Attention` (only garbled fragments present); `h`; `Decoder` (panel label — `Encoder` present, `Decoder` absent); `Add & Norm` (0 of 4 visible instances; the 5th is occluded by the red disc even on the image); `Feed Forward` (0 of 2); `Output Embedding`.

`text_recall = (22 EXACT + 1 NORMALIZED + 0.5·0 PARTIAL) / 29 = 23/29 = 79.3%`

Instance-count gaps behind the label score: `Linear` 2/5, `Q`/`K`/`V` 3 letters on one line vs 15 circles, `MatMul` 1 merged line vs 2 boxes, `Multi-Head Attention` 2/3, and the six MISSING labels account for 9 visible instances (5× `Add & Norm`-visible-4+occluded-1, 2× `Feed Forward`, 1× `Output Embedding`, 1× `Decoder`, 1× `h`, 1× `Masked MHA`).

**HALLUCINATION CANDIDATES (pass1) — none adjudicated yet, all single-read:**

1. `Scalar Dot-Product Attention` — no GT string contains "Scalar"; suspicion: OCR garble/duplicate of `Scaled Dot-Product Attention` (GT has exactly 2 instances; parse lists 3 SDPA-ish headers).
2. `Mult-Head Attention` — suspicion: truncated garble of `Multi-Head Attention` or of `Masked Multi-Head Attention` (the `Masked` token never appears).
3. `Math-Head Attention` — suspicion: second garble of the same family; no GT string matches.
4. `Max` — no GT string is `Max`; suspicion: fragment garble of `Mask (opt.)` or `SoftMax` (both separately present).

**Call 02 (pass2, maxtok 3000) — 2 content tokens (`**Transformer Blocks (stacked over Multi-Head)** 37`) and ZERO diagram text:**

- EXACT — 2 (`37`, title); MISSING — 27. `text_recall = 2/29 = 6.9%`.
- Hallucination candidates: none (it emitted no unmatched content strings — its failure mode is total omission, not invention).

---

## 2. Layout & coordinates

Token→px conversion: px = token × 960 (x), × 540 (y). "Within 80 px" is measured to
the nearest **content** element (text box or non-chrome shape); the chrome panel/badge
are excluded as reference anchors when a content element is the matchable pair (the
panel spans nearly the whole slide, so interior points would trivially score 0).

**Call 01 — 4 positioned anchors (2 with class tokens):**

| Parse anchor | px | Nearest GT element | GT box (px) | Distance | Verdict |
|---|---|---|---|---|---|
| `<x_0.1104><y_0.1>` (title+37 item) | (106.0, 54.0) | title box | 96,50 800×50 | inside box; 10.8 px to box corner | match |
| `<x_0.9277><y_0.168>` + `class_Section-header` | (890.6, 90.7) | badge circle `37` | 875,53 36×36 | 1.7 px below badge bottom, x inside | match (but classed "Section-header", see §3) |
| `<x_0.0625><y_0.1828>` (27-line text blob) | (60.0, 98.7) | inset-A header (nearest content) | 54,227 148×40 | **128.3 px** | no match — anchor sits on empty panel above the left column |
| `<x_0.916><y_0.9344>` + `class_Picture` | (879.4, 504.6) | figure frame border / `(shifted right)` box | x896 edge; 748,508 76×14 | 16.6 px / 55.5 px | match |

- Items inside the 960×540 frame: **4/4 (100%)**. Items within ~80 px of the nearest GT content element: **3/4 (75%)** (the blob anchor fails).
- Same-text coordinate pairs: only the title is matchable — anchor (106.0, 54.0) vs GT title box (96,50): inside the box, 4 px below its top edge, 10.8 px right of its left edge. No other parse line carries coordinates (all diagram text collapsed into one anchor-less blob), so 26 of 28 content lines have NO coordinate binding at all.
- Detected-region count: **2 class regions** (`Section-header` at the badge, `Picture` at the decoder bottom-right) vs GT 7 analysis regions / 3 diagram groups / 202 drawn shapes. The `Picture` token's anchor touches only the right panel's bottom corner — the two left insets are never region-marked.

**Call 02 — 4 positioned anchors (1 class region):**

| Parse anchor | px | Nearest GT element | Distance | Verdict |
|---|---|---|---|---|
| `<x_0.1104><y_0.1>` (title+37) | (106.0, 54.0) | title box | inside; 10.8 px | match |
| `<x_0.9277><y_0.168>` + `class_Section-header` | (890.6, 90.7) | badge circle | 1.7 px | match |
| `<x_0.0615><y_0.0773>` (Picture TL) | (59.0, 41.7) | title box (96,50) | 37.9 px | region corner, plausible top-left |
| `<x_0.9199><y_0.9531>` (Picture BR) | (883.1, 514.7) | figure frame / `(shifted right)` | 13.0 px to x896 edge / 59.5 px | region corner, plausible bottom-right |

- Items inside frame: **4/4 (100%)**; within 80 px: **4/4 (100%)** — but 2 of the 4 are corners of a single `class_Picture` box spanning (59.0, 41.7)–(883.1, 514.7), i.e. ONE region covering both left insets AND the right panel, whose top edge (y≈41.7) cuts into the title band. GT: 3 separate diagram regions (left inset ≈ 59–189 × 269–491; center inset ≈ 300–508 × 246–515; right panel ≈ 572–896 × 103–526). Under-segmentation: 1 region where GT has 3; region over-extends 162 px left and 61 px above the true figure frame.
- Same-text coordinate pairs: title only (same anchor as pass1 — corroborated).

**Build vs parse region/shape accounting:** build 202 shapes + 66 text boxes (268 draw calls) and 7 analysis regions; pass1 detects 2 region classes + 2 text anchors; pass2 detects 2 region classes (one being the mega-Picture) + 1 text anchor. Neither pass carries any box/arrow geometry for any diagram.

---

## 3. Structure fidelity

- **Class tokens vs build reality.** pass1/pass2 each emit exactly one `class_Section-header` (anchored at the badge, 890.6/90.7 — the slide's only true headers are the 4 red/green *italic* diagram/panel labels at y112–250; the badge is not a header) and one `class_Picture`. No `class_Chart`/`class_Table`/list/heading tokens. GT has no charts/tables (the 3 diagrams are native shape compositions), so the absence of chart/table classes is *correct* — but the diagrams themselves are demoted to `Picture`, which is structurally wrong: they are vector shape drawings, not embedded pictures, and pass2's single Picture swallows all three.
- **Text structure.** pass1 preserves *some* reading structure as a flat 27-line blob with 3 merged lines (`MatMul Concat`, `Q K V`) — box/line grouping is lost; pass2 preserves none.
- **Equations.** GT has none (no math objects on this slide) — nothing to garble; parse emitted no math tokens. Non-issue, recorded for completeness.
- **Charts/tables.** N/A as data objects; for the diagrams: pass1 extracted ~half the label instances (28 lines vs 54 visible label instances) with no structure; pass2 marked the region and missed every label. Neither extracted any arrow/flow semantics (which no class token carries anyway).
- **What the build encodes that the parse CANNOT carry:** all 75 palette hexes; exact px geometry of 202 shapes (incl. dash patterns and the 342° pin rotation); fonts (Arial) and the 6.5–35.5 pt size scale; bold/italic; z-order and occlusion (the `Add & Norm` under the red disc; 017-chain strings hidden under repaint patches); stacked-card shadow copies; clock icons; navy chevrons; the yellow L-shaped band; badge ring color/width; and the fact that the bottom black strip is video-player UI (absent from the build; unmentioned by both parses).

---

## 4. Reliability

| Call | EXIT | finish_reason | out_tokens | content chars | latency (script) | stderr lines |
|---|---|---|---|---|---|---|
| call01_pass1 (maxtok 1024) | 0 | stop | 133 | 535 | 51.8 s | 0 |
| call02_pass2 (maxtok 3000) | 0 | stop | 27 | 166 | 128.3 s | 0 |

- Both calls are VALID (EXIT 0, `finish_reason=stop`, non-empty string content). pass2 used 3000-max-token headroom but emitted 27 tokens — its collapse to title+Picture is model behavior, not truncation.
- **Corroboration (pass1 vs pass2), Jaccard over GT strings detected:** pass1 = 23/29; pass2 = 2/29; intersection = {`37`, title}; union = 23 → **Jaccard = 2/23 = 0.087 (8.7%)**.
- **Single-read strings (found in only one pass):** 21 GT strings detected only by pass1 (everything except `37` and the title), plus all 4 hallucination candidates. Nothing beyond `37`/title was found only by pass2. The title anchor (0.1104, 0.1) and the Section-header anchor (0.9277, 0.168) are byte-identical across passes — title/badge reading is the only corroborated content.
- Avg latency 90.05 s; avg out tokens 80. No 429/5xx, no DB-lock events, no retries needed (two call dirs, two attempts, two successes).

---

## Claims for image adjudication

1. Pass1 string `Scalar Dot-Product Attention` — candidate hallucination (GT has exactly 2 `Scaled Dot-Product Attention` instances; parse shows 3 SDPA-family headers) — verify: does ANY string reading "Scalar…" exist on the image, or is it an OCR garble of a real `Scaled/Multi-Head` header?
2. Pass1 strings `Mult-Head Attention` and `Math-Head Attention` — candidate hallucinations — verify: no such strings exist; expected real strings are `Multi-Head Attention` (3 instances: inset-B header, encoder box, decoder box) and `Masked Multi-Head Attention` (1, decoder purple block).
3. Pass1 string `Max` — candidate hallucination — verify: no standalone "Max" text exists (suspicion: fragment of `Mask (opt.)` / `SoftMax`).
4. Pass1 misses `Add & Norm` (×4 visible), `Feed Forward` (×2), `Output Embedding`, `Decoder` panel label, `h` brace label, `Masked Multi-Head Attention` — verify: all six ARE present and legible on the image (expected per GT), i.e. these are parse omissions, not absent content. Note the 5th `Add & Norm` (encoder lower, box 653,342 69×11.5) is partially occluded by a small solid red disc (~672–696, 331–355) even on the image — verify its legibility state.
5. Pass1's 27-line text blob is anchored at (60.0, 98.7) — empty panel area — verify: there is no text at (60,99); the real text zones are the left inset (~59–189 × 227–491), center inset (~294–508 × 210–515), and right panel (~572–896 × 103–526), and the blob's reading order (Encoder → decoder-top texts → inset headers → …) does not follow any real spatial order.
6. Pass1 merges `MatMul Concat` into one line and `Q K V` into one line — verify: `MatMul` and `Concat` are separate boxes in the center inset (76,429 / 364,312 in inset-A/B respectively) and the 15 V/K/Q letters sit in 5 separate circle groups (3 left, 3 center, 9 in the panel) — i.e. the merges are parse artifacts.
7. Pass2 detected ZERO diagram text and one `class_Picture` box (59.0, 41.7)–(883.1, 514.7) — verify: the true figure extent is three disjoint regions (left ≈ 59–189 × 269–491, center ≈ 300–508 × 246–515, right ≈ 572–896 × 103–526); the mega-Picture's top edge (y≈41.7) wrongly includes the title band, and its left edge (x≈59) wrongly includes the left column.
8. Both passes attach `class_Section-header` at (890.6, 90.7) — verify: that point is the slide-number BADGE (yellow circle, d≈36, center ~(893,71), numeral `37`), not a section header; the real section headers are the 4 italic labels (`Scaled Dot-Product Attention` at ~(54,227), `Multi-Head Attention` at ~(294,210), `Encoder` at ~(581,112), `Decoder` at ~(818,112)).
9. Title reading — both passes agree on `Transformer Blocks (stacked over Multi-Head)` anchored at (106.0, 54.0) — verify: exact title text, top-LEFT placement (~x96–864, y50–100, ~35 pt bold red; NOT centered).
10. Bottom black strip (full width, y≈518–540) — verify: it is video-player progress-bar UI, not slide content (the certified build does not draw it; neither parse mentions it — confirm the adjudicator should exclude it from content scoring).
11. Occlusion nuance for scoring leniency — verify: the small red disc over the encoder's lower `Add & Norm` (and any sliver remnants of the 017-chain texts behind the salmon/tan MHA boxes) means up to ~2 `Add & Norm` instances are partially illegible on the image itself; if confirmed, the parse's `Add & Norm` miss should count the occluded instance as legitimately unreadable, not as a fidelity defect.
