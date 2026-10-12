# m36_diag.py — decisive forensics for the two FAILing arrow regions, orig vs render_4.
# Windows in FRAME px; render sampled through the certified mapping.
from PIL import Image
from collections import defaultdict

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
FR = Image.open(VID + "/unique_slides/slide_005.jpg").convert("RGB")
RD = Image.open(VID + "/recreated_pptx/qa/slide005/render_4.png").convert("RGB")
SX, SY = 2.16770, 2.17684  # frame px -> render px


def classify(r, g, b):
    L = 0.299 * r + 0.587 * g + 0.114 * b
    if r > 140 and g < 115 and (r - g) > 60 and (r - b) > 60:
        return "R"                      # strict dark red (C00000 dashed connectors, rect border)
    if L < 100:
        return "D"                      # dark ink
    if r > 150 and 70 < g < 185 and (r - g) > 25 and (r - b) > 25:
        return "p"                      # pinkish-red (C47070 connectors / blends)
    if r > 185 and 140 < g < 215 and 90 < b < 200 and (r - b) > 25:
        return "T"                      # tan / brown head blend
    if 140 < L < 215 and abs(r - g) < 16 and abs(g - b) < 16:
        return "G"                      # gray
    return "."


def maps(name, x0, x1, y0, y1, step):
    print(f"== {name}: frame x{x0}..{x1} y{y0}..{y1} step {step} (R=darkred p=pink D=dark T=tan G=gray)")
    hdr = "     " + "".join(str((x0 + i) // 10 % 10) if (x0 + i) % 10 == 0 else " " for i in range(0, x1 - x0, step))
    po, pr = FR.load(), RD.load()
    for label, px, mapped in (("ORIG", po, False), ("REND4", pr, True)):
        print(f"-- {label}")
        print(hdr)
        for fy in range(y0, y1, step):
            row = []
            for fx in range(x0, x1, step):
                if mapped:
                    rx = round((fx - 18.0787) * SX)
                    ry = round((fy - 0.4700) * SY)
                    row.append(classify(*px[rx, ry]))
                else:
                    row.append(classify(*px[fx, fy]))
            print(f"{fy:4d} " + "".join(row))


# --- region 1: d1 end (under band -> enc MHA box left border) ---------------------
maps("D1-END", 600, 668, 330, 382, 1)

# --- region 2: h assembly (red rect right border -> circle, head, gray line) ------
maps("H-ASM", 456, 512, 322, 392, 1)
