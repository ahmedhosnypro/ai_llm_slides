VISION ADJUDICATION — doc-parse audit, slide_057

You are the isolated image adjudicator for slide slide_057 of the doc-parse accuracy audit. You are the ONLY agent that may look at this image. Open it exactly once with the Read tool and adjudicate from that single look.

Image (the original ground-truth frame):
/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_057.jpg
(960x540 frame; frame px coordinates below are in that frame: x rightward from left edge, y downward from top edge.)

Context: a text-extractor (nemotron-parse family via the doc-parse skill) parsed this frame and degenerated into a "Decoder" repetition loop. Its fragments are being audited against the slide's certified build file. The parse's own text is NOT shown to you — judge only against the IMAGE. Coordinates are approximate frame-px regions (fx,fy) taken from the certified build.

For EACH numbered claim answer exactly:
  <n>. REAL | HALLUCINATED | DEBATABLE — one-line evidence (what you see at that location, measured counts where the claim asks for counts).

Claims:
1. The parse degenerates into a "Decoder" repetition loop (482x at 1024 tokens, 1470x at 3000) after 6 unique lines — verify: the image is a normal schematic (panel + bars + circles), i.e. the loop is model degeneration, not literal repeated "Decoder" text on the slide.
2. The parse's only positioned item "57" maps to (56.3, 42.6) px, top-LEFT margin — verify: the "57" numeral badge actually sits top-RIGHT (build box x875..911, y53..89), i.e. the single coordinate token is mis-anchored.
3. 42/48 build GT strings are missing (all X_*/Y_* chips, Word row, both embedding bars, K/V/Q, SOS/Je/ne/suis/faisait, Softmax, 3 of 4 Encoder Block bars...) — verify: these labels exist on the image with legible ink (the certified build derives from this same frame), confirming the truncation lost them.
4. "Encoder Block 2" was detected but "M/1/0" were not — verify: all four bar labels ("Encoder Block M", 2, 1, 0) are present and similarly legible on the image.
5. The FFN bar was misread as "Feed Forward Networks / One Hidden with RELL Activation" — verify: the image reads "Feed Forward Networks - One Hidden with RELU Activation" (hyphen separator; RELU, not RELL).
6. Build vs analysis wording: decoder purple bar — build "Word and Position Encoding" vs analysis "Word and Position Embedding" — verify on-image which wording is printed.
7. Build vs analysis wording: the 5 masked-attention boxes — build "Multi-Head Self-Attention" vs analysis "Masked Multi-Headed Attention" — verify on-image.
8. Build vs analysis chip law: last token chips — certified 0-BASED law says "X_{N-1}"/"Y_{N-1}" is the final chip; analysis lists an extra "X_N"/"Y_N" — verify the last chip subscript on-image.
9. "Softmax" bar: present in the build (over the 17-circle row) but absent from the analysis label list — verify the maroon bar text on-image.
10. Bottom token row: build labels it "SOS / Je / ne / suis / faisait" (French sentence); analysis calls the boxes unlabeled — verify the tiny red text inside the 5 bottom token boxes.

After the verdicts add a final section:
## Overall — items 11-13
11. Dropped-region sweep: any visible text region or element on the frame NOT mentioned by claims 1-10 that a text extractor should have caught? List them with locations.
12. The slide's total visible distinct text strings (your count) — the parse caught only 6; a rough coverage estimate, high/medium/low.
13. Anything that looks mis-measured about the numbered coordinates themselves.

Output: plain text verdicts only. Do not write any files. Do not fetch anything. No follow-up questions.