#!/usr/bin/env python3
"""PIL measure pass 4 of slide_049.jpg — red samples (fixed), ASCII ink crops,
font metric solving for all lines."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_049.jpg"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)
FONTDIR = "/usr/share/fonts/liberation"

print("== darkest colors (fixed args y0,y1,x0,x1) ==")
def darkest(y0,y1,x0,x1,tag,n=12):
    seg = a[y0:y1, x0:x1].reshape(-1,3)
    lum = seg.sum(axis=1)
    idx = np.argsort(lum)[:n]
    sel = seg[idx]
    print(f"  {tag}: darkest-{n} mean #{'%02X%02X%02X'%tuple(sel.mean(axis=0).astype(int))}  min {sel.min(axis=0).tolist()}")
darkest(230,252, 332,392, "band2 ReLU red")
darkest(268,292, 677,808, "band3 max-pooling red")
darkest(306,332, 145,460, "band4 dark-red bold")
darkest(84,118, 250,710, "title red")

print("\n== ASCII ink crops (binarized, 1 char per px) ==")
def ascii_crop(y0,y1,x0,x1,tag,thr=480):
    seg = a[y0:y1, x0:x1]
    d = seg.sum(axis=2) < thr
    print(f"--- {tag} y{y0}..{y1} x{x0}..{x1} ---")
    for r in d:
        print("".join("#" if v else "." for v in r))
ascii_crop(84,128, 252,320, "title 'Co'")
ascii_crop(160,183, 148,200, "band0 'Sev'")
ascii_crop(199,223, 147,196, "band1 'Aft'")
ascii_crop(228,252, 141,190, "band2 'pop'")
ascii_crop(308,331, 146,196, "band4 'Aft' bold")
ascii_crop(343,367, 220,266, "band5 'Vec'")

print("\n== font metric solve ==")
def ink_w(text, fontpath, size_pt):
    f = ImageFont.truetype(fontpath, int(round(size_pt*4)))
    img = Image.new("L", (6000, 500), 255)
    dr = ImageDraw.Draw(img)
    dr.text((50, 150), text, font=f, fill=0)
    arr = np.asarray(img)
    xs = np.where((arr < 128).any(axis=0))[0]
    return (xs.max()-xs.min()+1)/4.0

LINES = {
 "band0": ("Several convolutional layers ( 5 or more)", 427, False),
 "band1": ("After the convolutional layers non-linearities are added (The most", 691, False),
 "band2": ("popular one is the ReLU)", 260, False),
 "band3": ("After the ReLU usually some pooling ( Most often max pooling)", 666, False),
 "band4": ("After 5 rounds of cascading:", 311, True),
 "band5": ("Vectorize the last convolutional layer (Flatten)", 477, False),
 "band6": ("Use as Input to the first fully connected layer (FC)", 518, False),
 "band7": ("Proceed as in a traditional classification neural network", 575, False),
}
fonts = {
 "SerifR": f"{FONTDIR}/LiberationSerif-Regular.ttf",
 "SansR":  f"{FONTDIR}/LiberationSans-Regular.ttf",
 "SerifB": f"{FONTDIR}/LiberationSerif-Bold.ttf",
 "SansB":  f"{FONTDIR}/LiberationSans-Bold.ttf",
}
for key,(text, mw, isbold) in LINES.items():
    cands = ["SerifB","SansB"] if isbold else ["SerifR","SansR"]
    results = []
    for fname in cands:
        # solve size: scan 20..28 in 0.25 steps
        best = None
        size = 20.0
        lo, hi = 20.0, 30.0
        for _ in range(24):
            mid = (lo+hi)/2
            w = ink_w(text, fonts[fname], mid)
            if w < mw: lo = mid
            else: hi = mid
        results.append((fname, (lo+hi)/2))
    print(f"{key} (meas w {mw}): " + "  ".join(f"{f} solves {s:.2f}pt" for f,s in results))

# title solve
for fname in ["SerifB","SansB"]:
    lo, hi = 38.0, 58.0
    for _ in range(24):
        mid = (lo+hi)/2
        w = ink_w("Convnets in practice", fonts[fname], mid)
        if w < 456: lo = mid
        else: hi = mid
    print(f"title (meas w 456): {fname} solves {(lo+hi)/2:.2f}pt")

# per-word gap check for title with solved serif size
f = ImageFont.truetype(fonts["SerifB"], int(round(49*4)))
img = Image.new("L", (3000, 300), 255); dr = ImageDraw.Draw(img)
dr.text((50, 100), "Convnets in practice", font=f, fill=0)
arr = np.asarray(img); xs = np.where((arr<128).any(axis=0))[0]
print("LibSerifB 49pt title ink w:", (xs.max()-xs.min()+1)/4.0)
