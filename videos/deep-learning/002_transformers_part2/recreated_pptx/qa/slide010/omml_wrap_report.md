# Slide 010 OMML wrap record — SKIPPED (no equation images)

Evaluated 2026-10-12 (OMML wrap pass). Certified build embeds exactly 4 raster images:
`s010_braceL.png` x2 + `s010_braceR.png` x2 (rId1..rId4) — the curly braces around the
matrix and bias column in the two right panels, PIL-drawn via the certified raster-brace
mechanism (same family as slide 020's brace_020). There are NO mathtext equation PNGs in
this build (all math-ish content is typed text runs / drawn shapes).

The braces are glyphs-with-extent, not equations; wrapping them in OMML Choice shapes
has no valid mathtext source and no benefit. **Slide left UNWRAPPED.**
Certified pptx untouched; no manifest created.
