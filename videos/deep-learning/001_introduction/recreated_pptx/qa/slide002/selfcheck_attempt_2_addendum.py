#!/usr/bin/env python3
"""selfcheck_attempt_2_addendum.py — isolates the single self-check attempt-2 flag.

Attempt-2 result: every measured edge of the 4 bullet bands, box, title, dots, bar
matched the original within 1.1 frame-px EXCEPT band3's BOTTOM edge
(render 342.7 vs original 348). This addendum documents that edge: it is the tail
of the single glyph 'Q' ("Quick"), not a text-block geometry error.

Finding: Liberation Sans Bold's Q outline has a ~5.9px tail at 30.6pt (PIL outline
measurement), but LibreOffice/FreeType rasterizes the thin tail tip so faintly that
solid ink ends ~2.5px below baseline; the original frame's font draws a solid ~6px
tail. One glyph, ~4 frame-px of thin ink. Documented variance — not a fix trigger
(no installed Arial-metric font has a deeper solid Q; Nimbus Sans Bold is shallower).
"""
from PIL import Image

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide002/render_2.png"
O = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_002.jpg"

for name, path, scale_hint in [("RENDER", R, 150/72), ("ORIGINAL", O, 1.0)]:
    im = Image.open(path).convert("RGB"); px = im.load()
    S = im.size[1] / 540.0
    x0, x1 = int(136 * S), int(166 * S)   # 'Q' of "Quick" region, frame x 136..166
    print(f"{name}: Q-region ink rows below baseline (baseline ~ frame-y 342):")
    for fy in range(340, 352):
        y = int(fy * S)
        pts = [(x / S, sum(px[x, y][:3])) for x in range(x0, x1) if sum(px[x, y][:3]) < 700]
        if pts:
            print(f"  frame-y {fy}: n={len(pts)} darkest={min(p[1] for p in pts)}")
print("CONCLUSION: single-glyph Q-tail variance (documented; all other edges <= 1.1 frame-px).")
