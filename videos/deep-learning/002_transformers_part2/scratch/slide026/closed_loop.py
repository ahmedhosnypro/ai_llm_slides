#!/usr/bin/env python3
"""Closed-loop ink check: render_1.png (2001x1125 @150dpi) vs original frame landmarks.
render_px = slide_pt * (200/72); slide_pt from frame via mapping.
Checks: panel, blue box, sub-blocks, bars, container, right rect, key text bands, arrow."""
from PIL import Image
import numpy as np

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide026/render_1.png"
img = Image.open(R).convert("RGB")
a = np.asarray(img).astype(int)
print("render size:", img.size)
K = 150 / 72.0  # render px per slide pt (2000px / 960pt)
MX, SXX, SYY = 18.628, 0.96123, 0.95556
def rp(fx, fy):
    sx = (fx - MX) / SXX; sy = fy / SYY
    return sx * K, sy * K

r, g, b = a[..., 0], a[..., 1], a[..., 2]
def near(c, tol):
    return (abs(r - c[0]) < tol) & (abs(g - c[1]) < tol) & (abs(b - c[2]) < tol)

def bbox(mask):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0: return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())

fails = []
def check(label, fx0, fy0, fx1, fy1, got, tol=6):
    ex0, ey0 = rp(fx0, fy0); ex1, ey1 = rp(fx1, fy1)
    if got is None:
        print(f"FAIL {label}: NO INK (expect {ex0:.0f},{ey0:.0f}-{ex1:.0f},{ey1:.0f})"); fails.append(label); return
    d = max(abs(got[0]-ex0), abs(got[1]-ey0), abs(got[2]-ex1), abs(got[3]-ey1))
    ok = d <= tol
    print(f"{'OK  ' if ok else 'FAIL'} {label}: got {got} expect ({ex0:.0f},{ey0:.0f},{ex1:.0f},{ey1:.0f}) dmax={d:.0f}")
    if not ok: fails.append(label)

# blue box
bb = bbox(near((14,191,235), 60)); check("blue_box", 231,239,379,387, bb, 8)
# container fill (sample away from content): frame 405..455 x 195..215
ex0, ey0 = rp(404, 189); ex1, ey1 = rp(658, 466)
cb = bbox(near((196,220,160), 22)); check("container", 404,189,658,466, cb, 10)
# right rect border (dark green ring): restrict x>1300
rrm = near((30,117,62), 60); rrm[:, :1350] = False
rr = bbox(rrm); check("right_rect_border", 687,187,855,465, rr, 10)
# Host MCU bar (gray fill) between corridor labels: frame x 395..412 y 254..385
hbm = near((215,215,215), 14)
hbm[:, :int(rp(390,0)[0])] = False; hbm[:, int(rp(420,0)[0]):] = False
hb = bbox(hbm); check("host_bar", 395,254,412,385, hb, 10)
# Encoder connector bar
ecm = near((215,215,215), 14)
ecm[:, :int(rp(645,0)[0])] = False; ecm[:, int(rp(670,0)[0]):] = False
ec = bbox(ecm); check("enc_bar", 649,280,666,373, ec, 10)
# Dual ADC pentagon
da = bbox(near((233,153,104), 42)); check("dual_adc", 472,248,545,279, da, 10)
# triangles
tr = bbox(near((108,206,147), 40)); check("tri_top", 543,245,579,279, tr, 10)
# power supplies
ps = bbox(near((208,186,111), 35)); check("power_sup", 462,416,526,456, ps, 10)
# pos arrow (red block) left of panel
arm = near((176,0,17), 60); arm[:, int(rp(230,0)[0]):] = False; arm[int(rp(0,280)[1]):int(rp(0,325)[1]), :] = False
ar = bbox(arm); check("pos_arrow", 155,294,226,319, ar, 10)
# title ink
tm = ((r - np.maximum(g, b)) > 60) & (r > 130); tm[int(rp(0,85)[1]):, :] = False; tm[:int(rp(0,50)[1]), :] = False
tm[:, :int(rp(300,0)[0])] = False; tm[:, int(rp(650,0)[0]):] = False
ti = bbox(tm); check("title_ink", 372,59,551,74, ti, 7)
# subtitle ink
sm = ((b - r) > 60) & (b > 130); sm[int(rp(0,105)[1]):, :] = False; sm[:int(rp(0,78)[1]), :] = False
si = bbox(sm); check("subtitle_ink", 209,83,719,101, si, 8)
# caption L1 ink
cm = ((r - np.maximum(g, b)) > 60) & (r > 130); cm[:int(rp(0,477)[1]), :] = False; cm[int(rp(0,493)[1]):, :] = False
c1 = bbox(cm); check("caption_L1", 334,481,773,491, c1, 8)
cm2 = ((r - np.maximum(g, b)) > 60) & (r > 130); cm2[:int(rp(0,493)[1]), :] = False; cm2[int(rp(0,510)[1]):, :] = False
c2 = bbox(cm2); check("caption_L2", 435,495,677,505, c2, 8)
# wires PNG ink: dark pixels in wire zone
wm = (r + g + b) < 420
wz = np.zeros_like(wm); wz[int(rp(0,300)[1]):int(rp(0,430)[1]), int(rp(668,0)[0]):int(rp(740,0)[0])] = True
wi = bbox(wm & wz)
print("wire-zone ink bbox:", wi, "(expect ink present)")
if wi is None: fails.append("wires_ink")
# frame containment: no content ink outside panel within house frame
print()
print("FAILS:", fails if fails else "NONE")
