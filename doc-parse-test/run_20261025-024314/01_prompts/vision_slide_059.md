VISION ADJUDICATION — doc-parse audit, slide_059

You are the isolated image adjudicator for slide slide_059 of the doc-parse
accuracy audit. You are the ONLY agent that may look at this image. Open it
exactly once with the Read tool and adjudicate from that single look.

Image (the original ground-truth frame):
/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_059.jpg
(960x540 frame; frame px coordinates below are in that frame: x rightward from
left edge, y downward from top edge.)

Context: a text-extractor (nemotron-parse family via the doc-parse skill)
parsed this frame. Its output is being audited against the slide's certified
build file. Below are the claims you must settle. The parse's own text is NOT
shown to you — judge only against the IMAGE. Coordinates are approximate
frame-px regions (fx,fy) taken from the certified build.

For EACH numbered claim answer exactly:
  <n>. REAL | HALLUCINATED | DEBATABLE — one-line evidence (what you see at
  that location, measured counts where the claim asks for counts).

Claims:
1. C1/C2/C3 rendering — verify whether the three class labels are exactly "C1 C2 C3" and whether any stray glyph precedes the first two (parse emitted "1C1", "1C2") or whether a "1"-like element really sits left of the class band.
2. Head-column subscript digits — the build code renders X0..X5 / Y0..Y5 while the build's header comment and the analysis JSON say X1..X6 / X1..X5: verify the printed digits of the six head columns on both token rows (this settles what the 8 garbage tokens corrupted).
3. Garbage tokens "Yd Xd Xx XN Xt Yk YNz YNd" — check the image's X/Y row labels: are they serif bold italic with subscripts (which could break a parser into such fragments)? Do any of these fragments correspond to actual glyphs on the slide, or are they invented?
4. Sigma visibility — GT draws a sigma inside each of the 3 navy softmax circles; the parse has no sigma at all: confirm sigma is printed in the circles (total miss vs genuine absence).
5. "Softmax" multiplicity — GT has per-circle "Softmax" x3 plus "Softmax Layer" on the tan bar; the parse emitted only "Softmax Layer": count the visible "Softmax" strings.
6. Vector_{PN-1} case — GT renders capital N ("Vector_{PN-1}"); parse wrote lowercase ("VectorPn-1"): verify the subscript case of the last position-vector label.
7. Pooled-vector row — GT build draws 20 pastel cells, the analysis says ~30, the parse describes no row: count the squares in the pooled row (settles GT's 20-vs-30 split).
8. Transformer Block count — parse matched 3/3 bars; verify the bar count on the image and that the 6 white-3-dot ellipsis columns sit between bars 2-3 (nothing in the parse mentions them).
9. Vertical layout order — the parse gives only 2 coordinate tokens; verify the bottom->top flow on the image (Input Sequence at bottom -> encoder -> Output Sequence -> GAP -> pooled row -> softmax band -> Output Classes at top) to confirm the parse's reading order is the true arrangement.
10. Badge — verify the top-right badge circle shows "59" with the purple ring (playlist chrome) and no other digits, i.e. the parse's "59" is the badge, not stray content.
11. Line-structure loss — verify "Word / Embedding / Vectors", "Position / Information / Vectors" and "Single vector representing / the whole sequence" are 3-/2-line stacked labels on the image (parse merged them to single lines).
12. The textless region point at (906.5, 517.6) px — confirm nothing textual sits at the frame's bottom-right corner (GT has only the lilac container edge there), i.e. the parse's sole region is a whole-frame picture class rather than a missed label.

After the verdicts add a final section:
## Overall — items 13-15
13. Dropped-region sweep: any visible text region or element on the frame NOT
    mentioned by claims 1-12 that a text extractor should have caught? List
    them with locations.
14. The slide's total visible distinct text strings (your count) vs your sense
    of what the parse captured — rough coverage estimate, high/medium/low.
15. Anything that looks mis-measured about the numbered coordinates
    themselves.

Output: plain text verdicts only. Do not write any files. Do not fetch
anything. No follow-up questions.