#!/usr/bin/env python3
"""Build matched crop sheets: render_2 vs original frame, identical regions A-G."""
from PIL import Image, ImageDraw

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
REN = Image.open(f"{BASE}/recreated_pptx/qa/slide008/render_2.png").convert("RGB")
FRM = Image.open(f"{BASE}/unique_slides/slide_008.jpg").convert("RGB")
SC = 150 / 72.0

# (label, frame x0,y0,x1,y1, upscale, caption) — same regions as the build-time reads
CROPS = [
    ("A", 135, 208, 258, 266, 3, "W_k box row1 + K4 vector"),
    ("B", 630, 208, 762, 266, 3, "W_v box row1 + V4 vector"),
    ("C", 243, 373, 357, 482, 3, "query path: q2 / W_q box / arrows"),
    ("D", 493, 198, 662, 387, 2, "all 4 multiply nodes"),
    ("E", 526, 103, 634, 157, 3, "Y output strip + label"),
    ("F", 316, 174, 380, 214, 4, "K.q corner + DP top-right"),
    ("G", 173, 438, 502, 517, 2, "sentence row X1..X4 + red arrow"),
]

def f2r_rect(fx0, fy0, fx1, fy1):
    def m(fx, fy):
        return ((fx - 17.628) / 0.961232 * SC, fy / 0.955556 * SC)
    ax, ay = m(fx0, fy0); bx, by = m(fx1, fy1)
    return int(ax), int(ay), int(bx), int(by)

def make_sheet(im, is_render):
    panels = []
    for (lbl, x0, y0, x1, y1, s, cap) in CROPS:
        if is_render:
            r = f2r_rect(x0, y0, x1, y1)
            c = im.crop(r)
        else:
            c = im.crop((x0, y0, x1, y1))
        c = c.resize((c.width * s, c.height * s), Image.LANCZOS)
        panels.append((lbl, c, cap))
    pad, label_h = 14, 32
    rows = [[0, 1, 4], [2, 5], [3], [6]]
    colw = max(p[1].width for p in panels) + pad
    rowh = [max(panels[i][1].height for i in r) + label_h + pad for r in rows]
    W = pad + colw * 3
    H = pad + sum(rowh)
    sheet = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    y = pad
    for r_i, row in enumerate(rows):
        x = pad
        for idx in row:
            lbl, c, cap = panels[idx]
            d.rectangle([x - 2, y - 2, x + c.width + 2, y + c.height + label_h + 2], outline=(200, 0, 0), width=2)
            d.text((x + 4, y + 2), f"[{lbl}] {cap}", fill=(0, 0, 200))
            sheet.paste(c, (x, y + label_h))
            x += colw
        y += rowh[r_i]
    return sheet

s1 = make_sheet(REN, True)
s2 = make_sheet(FRM, False)
s1.save(f"{BASE}/recreated_pptx/qa/slide008/crops_render2_sheet.png")
s2.save(f"{BASE}/recreated_pptx/qa/slide008/crops_orig_sheet2.png")
print("render sheet:", s1.size, " orig sheet:", s2.size)
