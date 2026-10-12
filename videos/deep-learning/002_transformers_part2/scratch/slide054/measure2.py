#!/usr/bin/env python3
"""Looser masks: red lines/arrows, pale-yellow pills, and precise fill means."""
from PIL import Image
import numpy as np
from scipy import ndimage

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_054.jpg"
img = Image.open(SRC).convert("RGB")
A = np.asarray(img).astype(int)
H, W, _ = A.shape
R, G, B = A[..., 0], A[..., 1], A[..., 2]
X0, SX, SY = 18.63, 0.96123, 0.95556
def to_slide(bb):
    x0, y0, x1, y1 = bb
    return [round((x0-X0)/SX,1), round(y0/SY,1), round((x1-X0)/SX,1), round(y1/SY,1),
            round((x1-x0)/SX,1), round((y1-y0)/SY,1)]
inner = np.zeros((H, W), bool); inner[46:516, 62:899] = True

def comps(mask, min_px, name, topn=60):
    m = mask & inner
    lab, n = ndimage.label(m, structure=np.ones((3,3)))
    out = []
    for i in range(1, n+1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_px: continue
        bb = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
        out.append({"f": bb, "n": int(len(ys)), "s": to_slide(bb)})
    out.sort(key=lambda c: -c["n"])
    print(f"\n== {name}: {len(out)}")
    for c in out[:topn]:
        print(f"   f={c['f']} n={c['n']} slide={c['s']}")
    return out

redline = (R - G >= 40) & (R - B >= 35) & (R >= 165) & (G < 190)
paleY   = (R >= 232) & (G >= 232) & (R - B >= 18) & (G - B >= 18) & (B < 225)
print("== RED LINES"); comps(redline, 40, "RED", 70)
print("== PALE YELLOW"); comps(paleY, 25, "PALEY", 50)

def mean(x0,y0,x1,y1):
    r = A[y0:y1, x0:x1].reshape(-1,3).mean(axis=0)
    return f"#{int(round(r[0])):02X}{int(round(r[1])):02X}{int(round(r[2])):02X}"
print("\nsoftmax@ (516,210)-(522,220):", mean(516,210,522,220), " (516,340)-(522,360):", mean(516,340,522,360), " (513,230)-(526,250):", mean(513,230,526,250))
print("Wk fill @(180,250)-(200,260):", mean(180,250,200,260), " (178,290)-(199,300):", mean(178,290,199,300))
print("Wv fill @(712,255)-(732,265):", mean(712,255,732,265))
print("Wq fill @(292,425)-(302,430):", mean(292,425,302,430))
print("kstrip (206,238)-(216,242):", mean(206,238,216,242), "(220,236)-(232,242):", mean(220,236,232,242))
print("outputbox (600,150)-(620,155):", mean(600,150,620,155))
