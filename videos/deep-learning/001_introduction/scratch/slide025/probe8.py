#!/usr/bin/env python3
"""probe8 — block-arrow head/stem/letter geometry for i and j arrows, and
the exact panel right edge / eq-box left-right borders still ambiguous."""
from PIL import Image
import numpy as np

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_025.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r_, g_, b_ = a[:,:,0], a[:,:,1], a[:,:,2]

def runs(m):
    idx = np.where(m)[0]
    if len(idx) == 0: return []
    out, s, p = [], idx[0], idx[0]
    for v in idx[1:]:
        if v == p+1: p = v
        else: out.append((int(s), int(p))); s = p = v
    out.append((int(s), int(p)))
    return out

# arrow region: classify each pixel as FILL / OUTLINE-dark / BG
print("== i arrow x234..300, y364..402: per-row classification ==")
for y in range(364, 403):
    row = []
    for x in range(234, 301):
        R, G, B = a[y, x]
        if abs(R-228) < 16 and abs(G-234) < 16 and B > 243:
            c = "F"   # lavender fill
        elif R+G+B < 400:
            c = "D"   # dark (outline/letter)
        elif abs(R-218) < 12 and abs(G-208) < 12 and abs(B-196) < 12:
            c = "b"   # beige
        else:
            c = "."
    # build string
    s = "".join(("F" if (abs(a[y,x,0]-228)<16 and abs(a[y,x,1]-234)<16 and a[y,x,2]>243)
                 else "D" if a[y,x].sum() < 400
                 else "b" if (abs(a[y,x,0]-218)<12 and abs(a[y,x,1]-208)<12 and abs(a[y,x,2]-196)<12)
                 else ".") for x in range(234, 301))
    print(f"  y{y}: {s}")
print("   x ruler: 234..." + "".join(str((234+i)//100 % 10) if (234+i) % 10 == 0 else " " for i in range(67)))

print("== j arrow x392..472, y364..402 ==")
for y in range(364, 403):
    s = "".join(("F" if (abs(a[y,x,0]-215)<14 and a[y,x,1]>243 and abs(a[y,x,2]-180)<16)
                 else "D" if a[y,x].sum() < 400
                 else "b" if (abs(a[y,x,0]-218)<12 and abs(a[y,x,1]-208)<12 and abs(a[y,x,2]-196)<12)
                 else ".") for x in range(392, 473))
    print(f"  y{y}: {s}")

# panel right edge: raw colors x560..615 at y145, y200, y300
print("== panel right edge raw ==")
for y in [145, 200, 300, 380]:
    s = "".join(("B" if (abs(a[y,x,0]-218)<14 and abs(a[y,x,1]-208)<14 and abs(a[y,x,2]-196)<14)
                 else "G" if (abs(a[y,x,0]-232)<8 and abs(a[y,x,1]-232)<8)
                 else "R" if (a[y,x,0]>130 and a[y,x,1]<80)
                 else "?") for x in range(556, 616))
    print(f"  y{y} x556..615: {s}")

# eq box1 left/right borders at y480; box2 right; box3 right
print("== eq box borders raw (x-classified at y480 / y470) ==")
for (y, x0, x1, tag) in [(475, 66, 90, "box1 left"), (475, 238, 262, "box1 right"),
                          (475, 284, 308, "box2 left"), (475, 492, 516, "box2 right"),
                          (475, 530, 556, "box3 left"), (475, 738, 762, "box3 right")]:
    vals = [f"{x}:{tuple(a[y,x])}" for x in range(x0, x1)]
    print(f"  {tag} y{y}: {vals}")

# error bar exact x extent at y200
print("== error bar row y200 ==")
m = (r_>120) & (g_<60) & (b_<60)
print("  runs:", [(s+560, e+560) for s, e in runs(m[200, 560:640])])
