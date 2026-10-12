#!/usr/bin/env python3
"""chrome_supplement_6.py — disc-only badge verification for render_6 (documented
workaround: house_chrome_check.py's badge sub-check false-positives on the starburst's
yellow dust overlapping the badge zone; slide_045 build header step 1). Same method as
chrome_supplement_3/4/5_out.txt. Banked as chrome_supplement_6_out.txt."""
import numpy as np
from PIL import Image
from collections import deque

QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide045"
ren = np.asarray(Image.open(f"{QA}/render_6.png").convert("RGB")).astype(int)
S = ren.shape[0] / 540.0
out = []
def P(*a):
    line = " ".join(str(x) for x in a)
    out.append(line); print(line)

# badge window: canonical disc (893,71) d36 frame px -> generous window
X0, X1, Y0, Y1 = 860, 930, 40, 105
r, g, b = ren[:, :, 0], ren[:, :, 1], ren[:, :, 2]
# badge-fill-specific yellow: FDFD96 has r-b ~= 103; the starburst's pale fill F0F6CE
# has r-b ~= 34 and must NOT be caught (it is what fooled the main checker).
yel = (r > 235) & (g > 235) & (b > 110) & (b < 215) & ((r - b) > 60) & ((g - b) > 60)
pur = (b - r > 40) & (b - g > 40) & (b > 120)
dark = ((r + g + b) / 3 < 120) & ~pur & ~yel

w = yel[int(Y0*S):int(Y1*S)+1, int(X0*S):int(X1*S)+1]
lab = np.zeros(w.shape, bool); comps = []
for y in range(w.shape[0]):
    for x in range(w.shape[1]):
        if w[y, x] and not lab[y, x]:
            q = deque([(y, x)]); lab[y, x] = True; pts = []
            while q:
                cy, cx = q.popleft(); pts.append((cy, cx))
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = cy+dy, cx+dx
                        if 0 <= ny < w.shape[0] and 0 <= nx < w.shape[1] and w[ny, nx] and not lab[ny, nx]:
                            lab[ny, nx] = True; q.append((ny, nx))
            comps.append(pts)
comps.sort(key=len, reverse=True)
sizes = [len(c) for c in comps]
P(f"yellow components in window: {len(comps)}; sizes: {sizes[:6]}")
disc = comps[0]
ys = [p[0] for p in disc]; xs = [p[1] for p in disc]
cx, cy = (min(xs)+max(xs))/2, (min(ys)+max(ys))/2
dx, dy = (max(xs)-min(xs)+1), (max(ys)-min(ys)+1)
acx, acy = X0*S + cx, Y0*S + cy          # absolute render px
ccx, ccy = 893*S, 71*S                    # canonical absolute render px
P(f"DISC center render ({acx:.0f},{acy:.0f}) vs canonical ({ccx:.0f},{ccy:.0f}) tol 8")
P(f"DISC diameter {dx:.0f}x{dy:.0f} vs 75 tol 12")
P(f"dust components (non-disc): {len(comps)-1}, largest dust size {sizes[1] if len(sizes)>1 else 0} px")
ring = int(pur[int(Y0*S):int(Y1*S)+1, int(X0*S):int(X1*S)+1].sum())
P(f"purple ring px: {ring} (need >=10)")
core = dark[int((71-9)*S):int((71+9)*S)+1, int((893-9)*S):int((893+9)*S)+1].sum()
P(f"numeral dark px in badge core: {int(core)} (need >0)")
ok = (abs(acx-ccx) <= 8 and abs(acy-ccy) <= 8 and abs(dx-75) <= 12 and abs(dy-75) <= 12
      and ring >= 10 and core > 0)
P("CHROME SUPPLEMENT (disc-only): " + ("PASS" if ok else "FAIL"))
open(f"{QA}/chrome_supplement_6_out.txt", "w").write("\n".join(out) + "\n")
