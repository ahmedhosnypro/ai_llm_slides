# Slide 032 OMML wrap record — SKIPPED (equation PNGs not wrappable; documented)

Evaluated 2026-10-12 (OMML wrap pass). Certified build embeds exactly 2 mathtext PNGs:
`eq_032_vec_brkL.png` (rId1) and `eq_032_vec_brkR.png` (rId2) — the TALL vector
delimiter brackets [ ] around the sin/cos vector rows (rendered by
`scripts/render_eq.py` from `\left[\vphantom{\sum_{i=1}^{N}}\right.`-style source,
fit to 73.3pt ink height, later recolored to C00000 with alpha/geometry unchanged;
blue originals archived in scratch/slide032/bug_evidence_blue_brk/). All other content
is typed text.

Why NOT wrapped (would corrupt the PowerPoint view):
1. The wrapper's certified converter does not support `\vphantom` (fails loudly).
2. A single-sided stretched delimiter cannot be expressed in the converter's OMML set:
   `\left[ ... \right.` would emit a literal "." as endChr (m:d requires both), and
   OMML's zero-width-endChr idiom (`<m:endChr m:val=""/>`) is not producible without
   editing the certified wrapper script (out of scope for this pass).
3. Falling back to a plain "[" char run would render a 20pt unstretched bracket in
   PowerPoint instead of the 71.4pt-tall stretched delimiter — a wrong representation,
   which the wrap pass must never ship.

**Slide left UNWRAPPED** (both equation PNGs remain the certified single
representation). Certified pptx untouched; no manifest created.
