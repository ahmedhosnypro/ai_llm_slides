#!/usr/bin/env python3
"""PIL measure pass 3 of slide_049.jpg — baselines, dots, underlines (sensitive),
darkest colors, font forensics (Liberation Serif vs Sans metric matching)."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_049.jpg"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)

BANDS = [(160,182),(199,222),(228,251),(268,290),(308,330),(343,366),(378,401),(414,431)]
DOTX  = [(112,117),(112,117),None,(112,117),(112,117),(195,201),(195,201),(195,201)]

print("== per-band profile: cap-top / baseline / descender ==")
for k,(s,e) in enumerate(BANDS):
    seg = a[s:e+1, 104:858]
    d = seg.sum(axis=2) < 420
    rc = d.sum(axis=1)
    # cap-top: first row with count>=12; baseline: last row with count>=12 (excluding isolated descenders)
    idx = np.where(rc >= 12)[0]
    captop = idx[0]+s if len(idx) else None
    base   = idx[-1]+s if len(idx) else None
    # x-height top: first row with count>=30
    idx2 = np.where(rc >= 30)[0]
    xtop = idx2[0]+s if len(idx2) else None
    print(f"band{k}: cap-top {captop}  x-top {xtop}  baseline ~{base}  band {s}..{e}")

print("\n== dots ==")
for k,(s,e) in enumerate(BANDS):
    if DOTX[k] is None: continue
    x0,x1 = DOTX[k]
    seg = a[s:e+1, x0-3:x1+4]
    d = seg.sum(axis=2) < 420
    ys,xs = np.where(d)
    if len(ys):
        y0,y1 = ys.min()+s, ys.max()+s
        ink = seg[d]
        print(f"band{k} dot: x {xs.min()+x0-3}..{xs.max()+x0-3} y {y0}..{y1} (d {y1-y0+1}x{xs.max()-xs.min()+1}) modal #{'%02X%02X%02X'%tuple((ink.mean(axis=0)).astype(int))} darkest {ink[ink.sum(1).argmin()]}")

print("\n== sensitive underline scan (sum<560, runs>=15px) ==")
def scan_rows(y_from, y_to, x0, x1, tag):
    for y in range(y_from, y_to):
        row = a[y, x0:x1]
        d = row.sum(axis=1) < 560
        xs = np.where(d)[0]
        if len(xs) >= 15:
            # longest contiguous run
            best = (0,0,0); cs=None
            for i,x in enumerate(xs):
                if cs is None: cs=prev=x; continue
                if x == prev+1: prev=x
                else:
                    if prev-cs > best[1]-best[0]: best=(cs,prev,prev-cs+1)
                    cs=prev=x
            if prev-cs > best[1]-best[0]: best=(cs,prev,prev-cs+1)
            if best[2] >= 15:
                print(f"  {tag} y={y}: run x {best[0]+x0}..{best[1]+x0} len {best[2]} n={len(xs)}")
# band1 baseline ~218; 'non-linearities' spans ~x504..674 (mid of band1)
scan_rows(215, 227, 480, 720, "band1 mid")
# band4 baseline ~326; whole line x112..457
scan_rows(324, 340, 112, 460, "band4 ")
# also full-width scan under band1 and band4
scan_rows(215, 227, 112, 858, "band1 full")
scan_rows(324, 340, 112, 858, "band4 full")
# band2 wrap: ReLU red - check underline under ReLU x334..390
scan_rows(245, 254, 300, 410, "band2  ")

print("\n== darkest colors ==")
def darkest(y0,y1,x0,x1,tag,n=12):
    seg = a[y0:y1, x0:x1].reshape(-1,3)
    lum = seg.sum(axis=1)
    idx = np.argsort(lum)[:n]
    sel = seg[idx]
    print(f"  {tag}: darkest-{n} mean #{'%02X%02X%02X'%tuple(sel.mean(axis=0).astype(int))}  min {sel[lum[idx].argmin()]}")
darkest(153,156, 300,500, "border top")
darkest(159,480, 99,102, "border left")
darkest(159,480, 859,862, "border right")
darkest(489,493, 300,500, "border bottom")
darkest(160,182, 149,576, "band0 ink")
darkest(199,222, 148,839, "band1 ink")
darkest(334,391, 330,395, "band2 ReLU red")
darkest(679,806, 675,810, "band3 maxpooling red")
darkest(308,330, 147,458, "band4 darkred")
darkest(84,117, 252,708, "title red")
darkest(414,432, 222,798, "band7 ink")

print("\n== font forensics ==")
FONTDIR = "/usr/share/fonts/liberation"
def ink_w(text, fontpath, size_pt):
    f = ImageFont.truetype(fontpath, int(round(size_pt*4)))  # 4x for precision
    img = Image.new("L", (4000, 400), 255)
    dr = ImageDraw.Draw(img)
    dr.text((50, 100), text, font=f, fill=0)
    arr = np.asarray(img)
    xs = np.where((arr < 128).any(axis=0))[0]
    return (xs.max()-xs.min()+1)/4.0

def cap_h(fontpath, size_pt):
    f = ImageFont.truetype(fontpath, int(round(size_pt*4)))
    img = Image.new("L", (600, 600), 255)
    dr = ImageDraw.Draw(img)
    dr.text((50, 150), "HC", font=f, fill=0)
    arr = np.asarray(img)
    ys = np.where((arr < 128).any(axis=1))[0]
    return (ys.max()-ys.min()+1)/4.0

TEXT0 = "Several convolutional layers ( 5 or more)"
TEXT5 = "Vectorize the last convolutional layer (Flatten)"
TITLE = "Convnets in practice"
meas = {"band0": 575-149+1, "band5": 697-222+1, "title": 707-252+1}
print(f"measured ink widths: band0 {meas['band0']}  band5 {meas['band5']}  title {meas['title']}")
for name, path in [("LibSerif-Reg", f"{FONTDIR}/LiberationSerif-Regular.ttf"),
                   ("LibSans-Reg", f"{FONTDIR}/LiberationSans-Regular.ttf"),
                   ("LibSerif-Bold", f"{FONTDIR}/LiberationSerif-Bold.ttf"),
                   ("LibSans-Bold", f"{FONTDIR}/LiberationSans-Bold.ttf")]:
    for size in [22, 23, 24, 25, 26]:
        w0 = ink_w(TEXT0, path, size)
        if abs(w0 - meas["band0"]) <= 8:
            w5 = ink_w(TEXT5, path, size)
            print(f"  {name} {size}pt: band0 {w0:.1f} (meas {meas['band0']})  band5 {w5:.1f} (meas {meas['band5']})")
    for size in [44, 46, 48, 49, 50, 51, 52]:
        wt = ink_w(TITLE, path, size)
        if abs(wt - meas["title"]) <= 10:
            print(f"  {name} {size}pt: title {wt:.1f} (meas {meas['title']})  cap@size {cap_h(path,size):.1f}")
print("cap heights @100pt:", {n: round(cap_h(p,100),1) for n,p in [("LibSerif",f"{FONTDIR}/LiberationSerif-Regular.ttf"),("LibSans",f"{FONTDIR}/LiberationSans-Regular.ttf")]})
