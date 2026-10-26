# Comparison — slide_052 (doc-parse vs certified ground truth)

Scope: `slide_052` · GT: `04_ground_truth/slide_052/` (frozen `slide_052.js` + `house_chrome.js` + `slide_052_final.json`, md5s in inventory.md)
Parses: `03_parses/slide_052/call01_pass1/` (1024 tok) and `call02_pass2/` (3000 tok) — **byte-identical outputs** (both `.parse.md` md5 `bdb0e649c4ba8572201ff35d90e80950`).
The parse `content` is DATA; nothing in it was executed. Slide is a pure schematic (no title bar, no bullets, no charts, no tables; one equation-class legend string).

## 1. Text fidelity

GT string list = 22 deduplicated units (inventory.md §1). Matching: case/whitespace-insensitive; a unit counts when its token sequence appears in one parse line (format tokens `<x_…><y_…><class_…>`/`F2` stripped before matching); `>=60%` token Jaccard → PARTIAL.

| GT unit (GT instances) | Class | Evidence |
|---|---|---|
| Multi-head Encoder-Decoder Attention Block (1) | EXACT | parse line 1 verbatim |
| Masked Multi-head Self Attention Block (1) | EXACT | line 4 verbatim |
| Residual Connection and Layer Normalization (3) | EXACT | lines 2, 5, 17 — all 3 occurrences |
| Feed Forward Networks [ One Hidden with  RELU Activation] (1) | EXACT | line 3; parse collapsed the verbatim double space before `RELU` to one (whitespace-insensitive → still EXACT; Courier-New contrast lost) |
| Encode Decoder Attention (5) | PARTIAL | 0.67 J = 2/3 tokens; parse has merged line `Encode Decoder` + fragments `Encoder`×3 / `Decoder`×2 / `Attention`×3; both sides: GT "Encode Decoder Attention" vs parse "Encode Decoder" (+scattered fragments). 5 stacked 3-line labels → 9 fragment lines |
| Masked Multi-Head Self Attention (5) | EXACT | lines 19-22 verbatim ×4; 5th box only fragment `Self Attention` (line 23); (a 5th string-match comes embedded in the callout-2 line) |
| Word and Position Encoding (1) | EXACT | line 25 |
| Transformer Encoder (1) | EXACT | line 18 |
| SOS = Start Of Sentence (1) | MISSING | parse has bare `SOS` (the word box); legend string absent |
| I / feel / Sick (1+1+1) | EXACT ×3 | all three tokens present, but merged into ONE line `I feel Sick` (3 separate boxes → 1 line) |
| SOS / Je / me / sens / malade (5) | EXACT ×5 | lines 26-30 |
| K (1) | MISSING | no `K` token anywhere |
| V (1) | MISSING | no `V` token anywhere |
| Q (5) | EXACT | lines 15, 16 — only 2 of 5 occurrences |
| Y (3) | MISSING | zero `Y` tokens (3 red tags) |
| 52 (1) | MISSING | badge numeral absent |

**text_recall = (16 EXACT + 0 NORMALIZED + 0.5·1 PARTIAL) / 22 = 16.5/22 = 75.0%**

### HALLUCINATION CANDIDATES (await Phase 3 image adjudication — not yet labeled hallucinated)

1. **Standalone `Encoder` ×3** (parse lines 7, 8, 11) — matches no GT unit (best J vs `Transformer Encoder` = 0.5 < 0.6). Suspicion: mis-OCR of `Encode` — the certified analysis explicitly preserves that the upper boxes spell `Encode Decoder Attention` with NO "r"; alternatively debris from the callout's hyphenated `Encoder-Decoder` (but that line already appears complete).
2. *(near-miss, listed for completeness, not a candidate)* `Encode Decoder` merged line and `I feel Sick` merged line — fragmentation/merging of GT content, not invented content.

No other unmatched content strings exist in the parse; every remaining line maps to a GT unit.

## 2. Layout & coordinates

- **Parse positioned items: 2** (items carrying `<x_…><y_…>`); one carries an extra font token `F2`:
  - item 1: `(0.0361, 0.0773)` → frame px **(34.7, 41.7)** — anchors the first text (callout 1).
  - item 2: `(0.9443, 0.9586)` → frame px **(906.5, 517.6)** — trailing `<class_Picture>`, no text.
- **Matchable pairs (same text): 1** — item 1 ↔ GT callout-1 box (build fx 64..296, fy 62..107). Point-to-box distance = **35.6 px** (dx 29.3, dy 20.3 to nearest corner). Inside frame ✓, within 80 px ✓.
- Item 2 has no text → no same-text pair. Nearest GT elements: inside the gray house panel (42..918, 45..540) → distance 0; **38.5 px** from the lower container's bottom-right corner (868, 516). Inside frame ✓, within 80 px ✓.
- **Fraction of parse items inside frame AND within ~80 px of nearest GT element: 2/2 = 100%** — statistically weak (n=2); the parse positions almost nothing, so layout recall is effectively nil: **2 positioned items vs 256 build elements = 0.8%**, and neither item binds to a shape anchor (build's nearest equivalents: callout border at (64,62); no GT element at the item-2 spot at all).
- **Build shape/region count vs parse detected regions: 256 drawable elements** (218 shapes: 137 rect / 82 line / 15 triangle / 8 ellipse + 38 text elements; instrumented-build census `build_probe/out/probe.json`) **and 9 analysis layout.regions, vs 2 parse regions.**

## 3. Structure fidelity

- **Class tokens: exactly 1** — `<class_Picture>` (trailing). Zero `class_section_header`, `class_list`, `class_table`, `class_chart`, `class_equation` tokens. The slide's real structure — two stacked containers, ten labeled 3D boxes, five caption bars, one encoder box, 13 token groups, 7 K/V/Q circles, 2 callouts, 1 badge — is carried as **zero structure**: no hierarchy, no counts, no container/containment relations.
- **Equations:** the slide's only equation-class item, the legend `SOS = Start Of Sentence`, is **MISSING** (bare `SOS` survives, likely the word box). No math was garbled to linear notation because no math was captured at all — the failure mode here is total omission, not distortion.
- **Charts/tables:** none exist on the slide (nothing to miss). The whole right-side schematic — the slide's entire content — is reduced to one trailing `class_Picture` region with no internal extraction (no box count, no arrow counts, no mask-tip counts 1-5, no grid structure).
- **Counts lost:** `Encode Decoder Attention` 5→fragments; `Q` 5→2; `Y` 3→0; `K` 1→0; `V` 1→0; `52` 1→0; input words 3 boxes→1 line.
- **What the build encodes that the parse CANNOT carry:** all ~35 palette hexes; exact px geometry of 256 elements; fonts (Arial vs the deliberate Courier-New `RELU` run); z-order (K/V arrows pass behind the blue boxes); arrowhead types/directions; italic+underline inside callouts; `Masked` yellow run; 3D slab construction (stripe positions, side slivers, top strips); causal-mask tip counts/colors per box; token-cell grid pitch (12 px) and rails; flipV/flipH connector geometry; the measured frame→slide capture transform; the mouse-cursor-omission ruling. A builder working from this parse alone could place ~9 text strings with no positions, sizes, colors, or structure — the schematic is unrecoverable from it.

## 4. Reliability

| Call | EXIT | finish_reason | out_tokens | content chars | latency (script) | stderr lines |
|---|---|---|---|---|---|---|
| call01_pass1 (1024 tok) | 0 | stop | 145 | 645 | 16.7 s | 0 |
| call02_pass2 (3000 tok) | 0 | stop | 145 | 645 | 52.2 s | 0 |

- Both calls valid (EXIT 0, finish stop, non-empty string content). No failed/retry call dirs needed.
- **Corroboration: outputs byte-identical** (same md5) → **Jaccard of GT strings detected = 1.00** (17 units detected in both passes: 16 EXACT + 1 PARTIAL). **Strings found in only one pass: none** — nothing is single-read; every detection is corroborated, and every omission is corroborated too (both passes dropped the same 5 units).
- Latency spread 16.7→52.2 s at identical output ⇒ shared-endpoint contention (4 concurrent workers), not content growth.
- **Raising `--max-output-tokens` 1024→3000 changed nothing** (145 tokens both, finish=stop both): the parse's lossiness is the model's reading behavior, not output-budget truncation.
- avg latency = 34.45 s; avg out_tokens = 145.

## Claims for image adjudication

1. The three standalone `Encoder` lines are hallucination candidates — verify: read the five upper blue boxes' first label line on the original frame; the certified analysis says `Encode` (no "r"). If the frame shows `Encode`, the parse mis-OCR'd it ×3 and also shredded the 5-box label row into fragments.
2. `K` and `V` circle labels missing — verify: confirm the small red circle (fx≈309-324, fy≈180-196) reads `K` and the green circle (fx≈310-325, fy≈231-247) reads `V` at the upper container's left edge; the parse captured neither.
3. `Y` tags missing (GT 3×) — verify: confirm three red `Y` labels sit above the left-panel token groups (fx≈85/163/239, fy≈247-263); parse has zero `Y`.
4. `SOS = Start Of Sentence` legend missing — verify: confirm the pale-green legend box (fx≈64-245, fy≈485-511) carries exactly that string; parse's only `SOS` is probably the word box, not the legend.
5. `52` badge numeral missing — verify: confirm the yellow top-right badge (measured center ≈(875.5, 69.5) on this frame) reads `52`; parse emitted no numeral anywhere.
6. Trailing `<class_Picture>` region at frame px (906.5, 517.6) — verify: what, if anything, is pictorial at the bottom-right near the lower container's bottom-right corner / panel edge? The token's placement matches no text and no obvious picture; is it a mis-anchored region or the schematic's bounding-box marker?
7. Leading anchor at frame px (34.7, 41.7) for callout 1 — verify: the callout box border starts at (64, 62); is there any glyph/text starting ~30 px up-left of the box, or is the parser's text-anchor systematically offset (matters for trusting its coordinates on other slides)?
8. `Q` count 2 vs 5 — verify: confirm five blue `Q` circles under the five upper boxes (fx≈385/489/601/715/813, fy≈253-255) with vertical stems; parse read only two.
9. Stacked 3-line box labels — verify: confirm each upper box label is three stacked lines `Encode`/`Decoder`/`Attention` and each lower box `Masked`(yellow)/`Multi-Head`/`Self Attention`; the parse merged/scattered these into 9 fragment lines + 4 whole lines, so line-structure fidelity is unverifiable from the parse.
10. FFN bar verbatim double space — verify: confirm the green bar reads `…with  RELU Activation]` with a double space before `RELU` (the build preserves it); the parse collapsed it to one space.
11. `I`/`feel`/`Sick` as three separate boxes — verify: confirm three separate white red-bordered boxes in the left panel (fx≈72-138/148-214/224-290, fy≈444-478); the parse merged them into the single line `I feel Sick`.
