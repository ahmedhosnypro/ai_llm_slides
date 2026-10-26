VISION ADJUDICATION — doc-parse audit, slide_052

You are the isolated image adjudicator for slide slide_052 of the doc-parse
accuracy audit. You are the ONLY agent that may look at this image. Open it
exactly once with the Read tool and adjudicate from that single look.

Image (the original ground-truth frame):
/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_052.jpg
(960x540 frame; frame px coordinates below are in that frame: x rightward from
left edge, y downward from top edge.)

Context: a text-extractor (nemotron-parse family via the doc-parse skill)
parsed this frame. Its output is being audited against the slide's certified
build file. Below are the claims you must settle. The parse's own text is NOT
shown to you — judge only against the IMAGE. Coordinates are given as
approximate frame-px regions (fx,fy) taken from the certified build.

For EACH numbered claim answer exactly:
  <n>. REAL | HALLUCINATED | DEBATABLE — one-line evidence (what you see at
  that location, measured counts where the claim asks for counts).

Claims:
1. The three standalone "Encoder" lines are hallucination candidates — verify: read the five upper blue boxes' first label line on the original frame; the certified analysis says "Encode" (no "r"). If the frame shows "Encode", the parse mis-OCR'd it x3 and also shredded the 5-box label row into fragments.
2. "K" and "V" circle labels missing — verify: confirm the small red circle (fx~309-324, fy~180-196) reads "K" and the green circle (fx~310-325, fy~231-247) reads "V" at the upper container's left edge; the parse captured neither.
3. "Y" tags missing (GT 3x) — verify: confirm three red "Y" labels sit above the left-panel token groups (fx~85/163/239, fy~247-263); parse has zero "Y".
4. "SOS = Start Of Sentence" legend missing — verify: confirm the pale-green legend box (fx~64-245, fy~485-511) carries exactly that string; parse's only "SOS" is probably the word box, not the legend.
5. "52" badge numeral missing — verify: confirm the yellow top-right badge (measured center ~(875.5, 69.5) on this frame) reads "52"; parse emitted no numeral anywhere.
6. Trailing picture-region token at frame px (906.5, 517.6) — verify: what, if anything, is pictorial at the bottom-right near the lower container's bottom-right corner / panel edge? Is it a mis-anchored region or the schematic's bounding-box marker?
7. Leading text anchor at frame px (34.7, 41.7) for callout 1 — verify: the callout box border starts at (64, 62); is there any glyph/text starting ~30 px up-left of the box, or is the parser's text-anchor systematically offset?
8. "Q" count 2 vs 5 — verify: confirm five blue "Q" circles under the five upper boxes (fx~385/489/601/715/813, fy~253-255) with vertical stems; parse read only two.
9. Stacked 3-line box labels — verify: confirm each upper box label is three stacked lines "Encode"/"Decoder"/"Attention" and each lower box "Masked"(yellow)/"Multi-Head"/"Self Attention"; the parse merged/scattered these into fragment lines, so line-structure fidelity is unverifiable from the parse.
10. FFN bar verbatim double space — verify: confirm the green bar reads "...with  RELU Activation]" with a double space before "RELU" (the build preserves it); the parse collapsed it to one space.
11. "I"/"feel"/"Sick" as three separate boxes — verify: confirm three separate white red-bordered boxes in the left panel (fx~72-138/148-214/224-290, fy~444-478); the parse merged them into the single line "I feel Sick".

After the verdicts add a final section:
## Overall — items 12-14
12. Dropped-region sweep: any visible text region or element on the frame NOT
    mentioned by claims 1-11 that a text extractor should have caught? List
    them with locations.
13. The slide's total visible distinct text strings (your count) vs your sense
    of what the parse captured — rough coverage estimate, high/medium/low.
14. Anything that looks mis-measured about the numbered coordinates
    themselves.

Output: plain text verdicts only. Do not write any files. Do not fetch
anything. No follow-up questions.