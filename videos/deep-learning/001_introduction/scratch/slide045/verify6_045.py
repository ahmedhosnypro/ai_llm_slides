#!/usr/bin/env python3
"""verify6_045.py — closed-loop verification of the attempt-6 judge-finding fixes on
render_6 (banked as verify6_out.txt):
  D1: line-1 ink covered by the starburst fill = render_6 missing ink vs the no-star
      variant (same text metrics; star is the only difference in that band).
      Judge D1 requires ZERO covered ink (original: text drawn over the fill).
  D2: red wedge <-> subscript min clearance (org baseline: 1 px threading).
  D4: the Gradient-line pointer present at its measured position (522..534, 435..449).
"""
import numpy as np
from PIL import Image

QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide045"
SC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch/slide045"
ren6 = np.asarray(Image.open(f"{QA}/render_6.png").convert("RGB")).astype(int)
nost = np.asarray(Image.open(f"{SC}/nostar_render/nostar-1.png").convert("RGB")).astype(int)
org = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_045.jpg").convert("RGB")).astype(int)
S = ren6.shape[0] / 540.0
out = []
def P(*a):
    line = " ".join(str(x) for x in a)
    out.append(line); print(line)

def masks(im):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    lum = (r + g + b) / 3
    red = (r - g > 25) & (r - b > 15) & (r > 90)
    dark = (lum < 205) & ~red
    return red, dark

r6, d6 = masks(ren6)
rn, dn = masks(nost)
ro, do = masks(org)

def win(m, x0, x1, y0, y1, k=1.0):
    return m[int(y0*k):int(y1*k)+1, int(x0*k):int(x1*k)+1]

def dilate(m, it=1):
    for _ in range(it):
        p = np.pad(m, 1)
        m = (p[0:-2,0:-2]|p[0:-2,1:-1]|p[0:-2,2:]|p[1:-1,0:-2]|p[1:-1,1:-1]|p[1:-1,2:]|
             p[2:,0:-2]|p[2:,1:-1]|p[2:,2:])
    return m

P("== D1: starburst-covered line-1 ink (render_6 vs no-star, y118..146 x700..890) ==")
diff = win(dn, 700, 895, 116, 150, S) & ~win(d6, 700, 895, 116, 150, S)
ys, xs = np.where(diff)
if len(ys):
    P(f"  COVERED bbox x{700+xs.min()/S:.1f}..{700+xs.max()/S:.1f} y{116+ys.min()/S:.1f}..{116+ys.max()/S:.1f} n={int(len(ys)/S/S)}  <-- D1 STILL OPEN")
else:
    P("  covered ink = 0 px  -> D1 RESOLVED (text over fill, as the original)")
ys, xs = np.where(win(d6, 700, 895, 118, 146, S))
P(f"  render_6 line-1 tail ink bbox: x{700+xs.min()/S:.0f}..{700+xs.max()/S:.0f} y{118+ys.min()/S:.0f}..{118+ys.max()/S:.0f} n={int(len(ys)/S/S)} (org 945 incl border)")
# contacts (threading) comparable to org
P("  star-vs-text contacts within 1px:")
for nm, redm, darkm, k in (("org", ro, do, 1.0), ("ren6", r6, d6, S)):
    star = win(redm, 756, 895, 117, 150, k)
    tx = win(darkm, 756, 895, 117, 150, k)
    n = int((dilate(star) & tx).sum()/(k*k))
    P(f"    {nm}: {n}")

P("")
P("== D2: red wedge <-> dark ink min clearance (x592..626 y332..360) ==")
for nm, redm, darkm, k in (("org", ro, do, 1.0), ("ren6", r6, d6, S)):
    wr = win(redm, 592, 626, 332, 360, k); wd = win(darkm, 592, 626, 332, 360, k)
    cl = None
    for it in range(0, 6):
        if (dilate(wr.copy(), it) & wd).any():
            cl = it; break
    P(f"  {nm}: min clearance = {cl} px")
ys, xs = np.where(win(r6, 592, 626, 332, 360, S))
P(f"  ren6 wedge bbox: x{592+xs.min()/S:.1f}..{592+xs.max()/S:.1f} y{332+ys.min()/S:.1f}..{332+ys.max()/S:.1f} (org x608..622 y345..357)")

P("")
P("== D4: Gradient-line pointer present (org measured ink x522..534 y435..449) ==")
for nm, darkm, k in (("org", do, 1.0), ("ren6", d6, S)):
    w = win(darkm, 518, 540, 432, 452, k)
    ys, xs = np.where(w)
    if len(ys):
        P(f"  {nm}: pointer ink bbox x{518+xs.min()/k:.1f}..{518+xs.max()/k:.1f} y{432+ys.min()/k:.1f}..{432+ys.max()/k:.1f} n={int(len(ys)/k/k)}")
    else:
        P(f"  {nm}: NONE  <-- D4 STILL OPEN")

open(f"{QA}/verify6_out.txt", "w").write("\n".join(out) + "\n")
print("\nwrote verify6_out.txt")
