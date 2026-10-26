VISION ADJUDICATION — doc-parse audit, slide_037

You are the isolated image adjudicator for slide slide_037 of the doc-parse accuracy audit. You are the ONLY agent that may look at this image. Open it exactly once with the Read tool and adjudicate from that single look.

Image (the original ground-truth frame):
/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg
(960x540 frame; frame px coordinates below are in that frame: x rightward from left edge, y downward from top edge.)

Context: a text-extractor (nemotron-parse family via the doc-parse skill) parsed this frame. Its output is being audited against the slide's certified build file. Below are the claims you must settle. The parse's own text is NOT shown to you — judge only against the IMAGE. Coordinates are approximate frame-px regions (fx,fy) taken from the certified build.

For EACH numbered claim answer exactly:
  <n>. REAL | HALLUCINATED | DEBATABLE — one-line evidence (what you see at that location, measured counts where the claim asks for counts).

Claims:
1. Pass1 string "Scalar Dot-Product Attention" — candidate hallucination (GT has exactly 2 "Scaled Dot-Product Attention" instances; parse shows 3 SDPA-family headers) — verify: does ANY string reading "Scalar..." exist on the image, or is it an OCR garble of a real "Scaled/Multi-Head" header?
2. Pass1 strings "Mult-Head Attention" and "Math-Head Attention" — candidate hallucinations — verify: no such strings exist; expected real strings are "Multi-Head Attention" (3 instances: inset-B header, encoder box, decoder box) and "Masked Multi-Head Attention" (1, decoder purple block).
3. Pass1 string "Max" — candidate hallucination — verify: no standalone "Max" text exists (suspicion: fragment of "Mask (opt.)" / "SoftMax").
4. Pass1 misses "Add & Norm" (x4 visible), "Feed Forward" (x2), "Output Embedding", "Decoder" panel label, "h" brace label, "Masked Multi-Head Attention" — verify: all six ARE present and legible on the image (expected per GT), i.e. these are parse omissions, not absent content. Note the 5th "Add & Norm" (encoder lower, box 653,342 69x11.5) is partially occluded by a small solid red disc (~672-696, 331-355) even on the image — verify its legibility state.
5. Pass1's 27-line text blob is anchored at (60.0, 98.7) — empty panel area — verify: there is no text at (60,99); the real text zones are the left inset (~59-189 x 227-491), center inset (~294-508 x 210-515), and right panel (~572-896 x 103-526), and the blob's reading order (Encoder -> decoder-top texts -> inset headers -> ...) does not follow any real spatial order.
6. Pass1 merges "MatMul Concat" into one line and "Q K V" into one line — verify: "MatMul" and "Concat" are separate boxes in the center inset (76,429 / 364,312 in inset-A/B respectively) and the 15 V/K/Q letters sit in 5 separate circle groups (3 left, 3 center, 9 in the panel) — i.e. the merges are parse artifacts.
7. Pass2 detected ZERO diagram text and one picture box (59.0, 41.7)-(883.1, 514.7) — verify: the true figure extent is three disjoint regions (left ~ 59-189 x 269-491, center ~ 300-508 x 246-515, right ~ 572-896 x 103-526); the mega-Picture's top edge (y~41.7) wrongly includes the title band, and its left edge (x~59) wrongly includes the left column.
8. Both passes attach a section-header class at (890.6, 90.7) — verify: that point is the slide-number BADGE (yellow circle, d~36, center ~(893,71), numeral "37"), not a section header; the real section headers are the 4 italic labels ("Scaled Dot-Product Attention" at ~(54,227), "Multi-Head Attention" at ~(294,210), "Encoder" at ~(581,112), "Decoder" at ~(818,112)).
9. Title reading — both passes agree on "Transformer Blocks (stacked over Multi-Head)" anchored at (106.0, 54.0) — verify: exact title text, top-LEFT placement (~x96-864, y50-100, ~35 pt bold red; NOT centered).
10. Bottom black strip (full width, y~518-540) — verify: it is video-player progress-bar UI, not slide content (the certified build does not draw it; neither parse mentions it — confirm the adjudicator should exclude it from content scoring).
11. Occlusion nuance for scoring leniency — verify: the small red disc over the encoder's lower "Add & Norm" (and any sliver remnants of the 017-chain texts behind the salmon/tan MHA boxes) means up to ~2 "Add & Norm" instances are partially illegible on the image itself; if confirmed, the parse's "Add & Norm" miss should count the occluded instance as legitimately unreadable, not as a fidelity defect.

After the verdicts add a final section:
## Overall — items 12-14
12. Dropped-region sweep: any visible text region or element on the frame NOT mentioned by claims 1-11 that a text extractor should have caught? List them with locations.
13. The slide's total visible distinct text strings (your count) vs your sense of what the parse captured — rough coverage estimate, high/medium/low.
14. Anything that looks mis-measured about the numbered coordinates themselves.

Output: plain text verdicts only. Do not write any files. Do not fetch anything. No follow-up questions.