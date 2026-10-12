#!/usr/bin/env python3
"""PIL measurement pass 5: quantized modals, text metrics per box, annotation top
border, container right border, verr/pencil zoom crops."""
from PIL import Image
import numpy as np
from collections import Counter

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_019.jpg").convert("RGB")
a = np.asarray(IM).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def qmodal(pix, label, n=5):
    q = (pix // 12) * 12
    cnt = Counter(map(tuple, q.reshape(-1, 3)))
    tot = len(q.reshape(-1, 3))
    print(f"  {label}:", [(f"#{c:02X}{m:02X}{y:02X}", f"{k*100//tot}%") for (c, m, y), k in cnt.most_common(n)])

def darkest(pix, label, pct=8):
    s = pix.sum(axis=1)
    idx = np.argsort(s)[: max(1, len(s) * pct // 100)]
    q = (pix[idx] // 12) * 12
    cnt = Counter(map(tuple, q))
    print(f"  {label} darkest:", [(f"#{c:02X}{m:02X}{y:02X}", k) for (c, m, y), k in cnt.most_common(3)])

# ---- quantized modals ----
qmodal(a[69:92, 222:655][((r[69:92, 222:655] > 120) & (g[69:92, 222:655] < 110))], "title")
qmodal(a[214:256, 82:156], "input fill")
qmodal(a[209:262, 207:278], "pre fill")
qmodal(a[209:262, 323:403], "extr fill")
qmodal(a[209:262, 431:510], "sel fill")
qmodal(a[207:264, 533:629], "classif fill")
qmodal(a[214:256, 662:735], "pred fill")
qmodal(a[173:297, 754:790], "verr fill")
qmodal(a[113:157, 374:465], "ellipse fill")
qmodal(a[196:274, 195:660], "container zone (fill+dashes)")
qmodal(a[336:377, 263:740], "annot fill")
qmodal(a[340:377, 300:700][((g[340:377, 300:700] < 190) & (r[340:377, 300:700] < 180))], "annot text", 6)
darkest(a[340:377, 300:700][((g[340:377, 300:700] < 190) & (r[340:377, 300:700] < 180))], "annot text")
qmodal(a[183:287, 774:787], "verr text", 5)
darkest(a[183:287, 774:787][((r[183:287, 774:787] > 120) & (g[183:287, 774:787] < 110))], "verr text")
qmodal(a[130:212, 114:372][(b[130:212, 114:372] - (r[130:212, 114:372] + g[130:212, 114:372])//2 > 22)], "blue solid", 6)
qmodal(a[255:325, 208:775][(g[255:325, 208:775] - (r[255:325, 208:775] + b[255:325, 208:775])//2 > 18)], "green", 6)
qmodal(a[196:274, 195:660][((r[196:274, 195:660] > 140) & (g[196:274, 195:660] < 90) & (b[196:274, 195:660] < 90))], "container red", 5)

# ---- text metrics per box (dark ink rows/cols inside fill) ----
def textmetrics(label, x0, x1, y0, y1, thr=380):
    sub = a[y0:y1, x0:x1]
    dk = sub.sum(axis=2) < thr
    ys, xs = np.where(dk)
    if not len(ys):
        print(f"{label} text: none"); return
    print(f"{label} text ink: x{xs.min()+x0}..{xs.max()+x0} y{ys.min()+y0}..{ys.max()+y0} (h{ys.max()-ys.min()+1})")
    rowprof = dk.sum(axis=1)
    bands = []
    inb = False
    for i, c in enumerate(rowprof):
        if c > 0 and not inb: s = i; inb = True
        elif c == 0 and inb: bands.append((s + y0, i - 1 + y0)); inb = False
    if inb: bands.append((s + y0, len(rowprof) - 1 + y0))
    print(f"   text row bands: {bands}")

textmetrics("input", 84, 154, 212, 258)
textmetrics("samples", 813, 881, 212, 258)
textmetrics("pre", 209, 277, 207, 263)
textmetrics("extr", 325, 402, 207, 263)
textmetrics("sel", 433, 509, 207, 263)
textmetrics("pred", 664, 734, 212, 258, thr=420)
textmetrics("ellipse", 376, 464, 111, 158)
# classification = white text on dark red
sub = a[207:264, 533:629]
wt = (sub[:, :, 0] > 200) & (sub[:, :, 1] > 200) & (sub[:, :, 2] > 200)
ys, xs = np.where(wt)
print(f"classif white text: x{xs.min()+533}..{xs.max()+533} y{ys.min()+207}..{ys.max()+207}")
# verr text per-band (rotated): col profile
sub = a[175:300, 770:792]
dk = (sub[:, :, 0] > 120) & (sub[:, :, 1] < 110) & (sub[:, :, 2] < 110)
colprof = dk.sum(axis=0)
print("verr text col profile (x770+i:count):", {770+i: int(c) for i, c in enumerate(colprof) if c > 0})

# ---- annotation: top border scan + line x-extents ----
print("annot col x=320: y328..346:", [f"{y}:{tuple(a[y,320])}" for y in range(328, 346)])
sub = a[338:360, 263:740]
dk = sub.sum(axis=2) < 460
ys, xs = np.where(dk)
print(f"annot line1 ink: x{xs.min()+263}..{xs.max()+263}")
sub = a[360:378, 263:740]
dk = sub.sum(axis=2) < 460
ys, xs = np.where(dk)
print(f"annot line2 ink: x{xs.min()+263}..{xs.max()+263}")

# ---- container right border: cols 650..668 excluding arrow band y228..242 ----
red = (r > 130) & (g < 100) & (b < 100)
for col in range(648, 668):
    ys = [y for y in list(range(198, 228)) + list(range(244, 272)) if red[y, col]]
    if len(ys) > 4:
        print(f"container right col {col}: n={len(ys)} y{ys[0]}..{ys[-1]}")

# ---- zoom crops for visual reference ----
for name, (x0, y0, x1, y1) in {
    "crop_verr": (738, 160, 800, 310),
    "crop_pencil": (240, 200, 290, 240),
    "crop_ellipse": (360, 100, 480, 170),
    "crop_annot": (255, 325, 745, 385),
    "crop_containerleft": (150, 190, 340, 285),
}.items():
    crop = IM.crop((x0, y0, x1, y1))
    crop = crop.resize(((x1-x0)*5, (y1-y0)*5), Image.LANCZOS)
    crop.save(f"/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide019/{name}.png")
print("crops saved")
