#!/usr/bin/env python3
"""m21_assets.py — slide 047 block-arrow PNG assets (mechanism per scratch/slide038/m18_assets.py).
Style A (X->MHA gap): light lavender fill #E9E7F5, blue #4472C4 outline+spiral hatch, 16x20pt.
Style B (three upper gaps): hollow (transparent), plum #7A3A40 outline+spiral hatch, 15x14.5pt.
Drawn at 4 px/pt, placed at exact pt/72 sizes."""
from PIL import Image, ImageDraw
import math

OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/"
S = 4

def block_arrow(w_pt, h_pt, fill, outline, fname):
    W, H = int(w_pt * S), int(h_pt * S)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    lw = max(2, int(0.9 * S))
    tip = (W / 2, 1)
    hb = 0.52 * H
    hb_l, hb_r = (0.6 * S, hb)
    sh_l, sh_r = (W * 0.33, W * 0.67)
    poly = [(W / 2, 1), (hb_r, hb), (sh_r, hb), (sh_r, H - 1), (sh_l, H - 1), (sh_l, hb), (hb_l, hb)]
    d.polygon(poly, fill=fill, outline=outline, width=lw)
    cx, cy = W / 2, (hb + H) / 2
    rmax = min(sh_r - sh_l, H - hb) / 2 - 1.2 * S
    pts = []
    for i in range(0, 260):
        t = i / 260 * 2.6 * 2 * math.pi
        r = rmax * (i / 260)
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t) * 0.9))
    if rmax > 2:
        d.line(pts, fill=outline, width=max(2, int(0.55 * S)), joint="curve")
    im.save(OUT + fname)
    print(fname, im.size)

block_arrow(16.0, 20.0, (233, 231, 245, 255), (68, 114, 196, 255), "s047_blkarrow_A.png")
block_arrow(15.0, 14.5, (0, 0, 0, 0), (122, 58, 64, 255), "s047_blkarrow_B.png")
