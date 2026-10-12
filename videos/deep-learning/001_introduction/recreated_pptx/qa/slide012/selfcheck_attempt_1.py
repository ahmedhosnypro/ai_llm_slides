from PIL import Image
import numpy as np
from collections import Counter

NS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
ren = np.asarray(Image.open(f"{NS}/recreated_pptx/qa/slide012/render_1.png").convert('RGB')).astype(int)
org = np.asarray(Image.open(f"{NS}/unique_slides/slide_012.jpg").convert('RGB')).astype(int)
S = ren.shape[1] / 960.0
print(f"render {ren.shape[1]}x{ren.shape[0]}, scale {S:.4f}")
results = []

def bbox(arr, fy0, fy1, fx0, fx1, thr, pred=None, k=1.0):
    """Search frame-px window [fy0..fy1]x[fx0..fx1] in arr using factor k (1=orig, S=render).
    Returns bbox in FRAME px."""
    H, W = arr.shape[:2]
    ry0, ry1 = max(0, int(fy0*k)), min(H-1, int(fy1*k))
    rx0, rx1 = max(0, int(fx0*k)), min(W-1, int(fx1*k))
    pts = [(y, x) for y in range(ry0, ry1+1) for x in range(rx0, rx1+1)
           if arr[y, x].sum() < thr and (pred is None or pred(arr[y, x]))]
    if not pts:
        return None
    ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
    return (min(ys)/k, max(ys)/k, min(xs)/k, max(xs)/k)

def cmp(name, o, r, tol=4.0):
    if o is None or r is None:
        print(f"  {name}: MISSING o={o} r={r}"); results.append(False); return
    d = [r[i]-o[i] for i in range(4)]
    ok = all(abs(x) <= tol for x in d)
    print(f"  {name}: orig y{o[0]:.1f}..{o[1]:.1f} x{o[2]:.1f}..{o[3]:.1f} | rend(frame) y{r[0]:.1f}..{r[1]:.1f} x{r[2]:.1f}..{r[3]:.1f} | d {d[0]:+.1f}/{d[1]:+.1f}/{d[2]:+.1f}/{d[3]:+.1f} {'OK' if ok else 'CHECK'}")
    results.append(ok)

cmp("title box border", bbox(org,74,146,85,375,520), bbox(ren,74,146,85,375,520,k=S))
cmp("content box border", bbox(org,150,398,85,895,520), bbox(ren,150,398,85,895,520,k=S))
cmp("black bar", bbox(org,505,539,20,950,150), bbox(ren,505,539,20,950,150,k=S))
cmp("title text", bbox(org,90,130,98,362,430), bbox(ren,90,130,98,362,430,k=S))
cmp("header band", bbox(org,163,190,100,870,430), bbox(ren,163,190,100,870,430,k=S))
cmp("header red run", bbox(org,160,190,100,880,999,lambda p: int(p[0])-int(p[1])>60 and p[0]>130),
                         bbox(ren,160,190,100,880,999,lambda p: int(p[0])-int(p[1])>60 and p[0]>130,k=S))
cmp("underline (black-only)", bbox(org,181,189,340,620,400,lambda p: max(p)<130),
                              bbox(ren,181,189,340,620,400,lambda p: max(p)<130,k=S))
for i,(y0,y1) in enumerate([(226,258),(270,302),(314,346),(358,390)]):
    def band(arr, k):
        def skip(y, x):
            fx, fy = x/k, y/k
            return i == 2 and ((arr is org and 185 <= fx <= 215) or (arr is ren and 386 <= x <= 448))
        return bbox(arr, y0, y1, 100, 880, 430, pred=lambda p, y=None, x=None: True, k=k) if False else None
    # simpler: inline
    y1 = min(y1, 388)  # keep clear of the content-box bottom border rows 389-391
    def bb(arr, k):
        H, W = arr.shape[:2]
        pts = [(y, x) for y in range(max(0,int(y0*k)), min(H-1,int(y1*k))+1)
                       for x in range(max(0,int(100*k)), min(W-1,int(870*k))+1)
                       if arr[y, x].sum() < 430 and not (i == 2 and (185 <= x/k <= 215 if arr is org else 386 <= x <= 448))]
        if not pts: return None
        ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
        return (min(ys)/k, max(ys)/k, min(xs)/k, max(xs)/k)
    cmp(f"bullet{i+1} band", bb(org,1.0), bb(ren,S))

def dots(arr, k):
    out = []
    for (y0, y1) in [(232,252),(276,296),(320,340),(364,384)]:
        H, W = arr.shape[:2]
        pts = [(y,x) for y in range(max(0,int(y0*k)), min(H-1,int(y1*k))+1)
                       for x in range(max(0,int(100*k)), min(W-1,int(124*k))+1) if arr[y,x].sum() < 250]
        if pts:
            ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
            out.append(((min(ys)+max(ys))/2/k, (min(xs)+max(xs))/2/k))
    return out
od, rd = dots(org,1.0), dots(ren,S)
print(f"  dots orig: {[(round(y,1),round(x,1)) for y,x in od]}")
print(f"  dots rend: {[(round(y,1),round(x,1)) for y,x in rd]}")
ok = len(od)==len(rd)==4 and all(abs(a[0]-b[0])<=4 and abs(a[1]-b[1])<=4 for a,b in zip(od,rd))
print(f"  dots: {'OK' if ok else 'CHECK'}"); results.append(ok)

print("  title fill rend:", Counter(tuple(ren[int(y*S),int(x*S)]) for y in range(88,96) for x in range(115,345,7)).most_common(1),
      "| orig:", Counter(tuple(org[y,x]) for y in range(88,96) for x in range(115,345,7)).most_common(1))
print("  content fill rend:", Counter(tuple(ren[int(y*S),int(x*S)]) for y in range(200,380,11) for x in range(400,800,13)).most_common(1),
      "| orig:", Counter(tuple(org[y,x]) for y in range(200,380,11) for x in range(400,800,13)).most_common(1))

# CONTENT-zone ink (excludes chrome border strokes, badge ring x875..911 y53..89, black bar
# y518+ — all present in the original too): window x64..870 y60..510
r_all = bbox(ren, 60, 510, 64, 870, 430, k=S)
print(f"  content-zone ink rend(frame): y{r_all[0]:.1f}..{r_all[1]:.1f} x{r_all[2]:.1f}..{r_all[3]:.1f} (window x64..870 y60..510)")
cont = r_all[2] >= 62 and r_all[3] <= 872 and r_all[0] >= 58 and r_all[1] <= 512
# black bar spans x 38..921 in the ORIGINAL frame too (drawn 519..537.5 to keep the chrome
# bottom stroke visible) — its crossing of the panel edge x42/918 is original-parity, not overflow.
r_bar = bbox(ren, 505, 539, 20, 950, 150, k=S)
bar_ok = abs(r_bar[2]-38) <= 2 and abs(r_bar[3]-921) <= 2
print(f"  slide-bounds containment: {'OK' if cont else 'FAIL'}; black bar parity x{r_bar[2]:.1f}..{r_bar[3]:.1f} vs orig 38..921: {'OK' if bar_ok else 'FAIL'}")
results.append(cont and bar_ok)
r_cb = bbox(ren, 163, 388, 97, 879, 430, k=S)
ok2 = r_cb[0] >= 158.5 and r_cb[1] <= 389.5 and r_cb[2] >= 96.5 and r_cb[3] <= 880.5
print(f"  content-box containment: ink y{r_cb[0]:.1f}..{r_cb[1]:.1f} x{r_cb[2]:.1f}..{r_cb[3]:.1f} in (96.5..880.5, 158.5..389.5): {'OK' if ok2 else 'FAIL'}"); results.append(ok2)
print(f"\nTOTAL: {sum(1 for r in results if r)}/{len(results)} checks OK")
