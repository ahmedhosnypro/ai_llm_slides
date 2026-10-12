#!/usr/bin/env python3
"""afix_trace_2.py — founder-defect measurement for slide 046 (002_transformers_part2):
"dark orange arrows have small twists around the path" — PIL-trace every dark-orange
arrow on the 150dpi render, compute the centerline per row, measure perpendicular
deviation from a smooth fit (the wobble), and compare against the ORIGINAL frame
(unique_slides/slide_046.jpg, ground truth: the original's arrows are smooth).

Banks: prints a full report (redirect to qa/slide046/afix_trace_2.txt).

Geometry (slide pts, from components/slide_046.js + parent 045/038):
  cols = [194.9, 270.3, 346.3, 422.8, 499.8, 574.1, 771.8, 848.8]
  uT curves: x in [cx-52, cx+2], y in [149.1, 300.4]   (asset 54x149pt stretched to 151.3)
  uB curves: x in [cx-52, cx+2], y in [369.95, 518.95] (asset 54x149pt exact)
The arrow asset (s038_orangearrow.png) is orange E36C09; the annotation text is
ORANGE E8A020 (G channel differs: 108 vs 160) — the mask separates them.
"""
import numpy as np
from PIL import Image
from scipy import ndimage

QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide046/"
VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/"

COLS = [194.9, 270.3, 346.3, 422.8, 499.8, 574.1, 771.8, 848.8]
UNITS = {"uT": {"y0": 149.1, "y1": 300.4}, "uB": {"y0": 369.95, "y1": 518.95}}
DX, W_PT = -52.0, 54.0
PXPT = 150 / 72.0  # 2.0833 px per slide pt

def orange_mask(arr, rmin=170, gmin=55, gmax=148, bmax=90):
    R = arr[:, :, 0].astype(int); G = arr[:, :, 1].astype(int); B = arr[:, :, 2].astype(int)
    return (R > rmin) & (G > gmin) & (G < gmax) & (B < bmax)

def smooth_fit(xs, ys, window=13):
    """Centered moving quadratic fit -> smooth trend of x(y)."""
    n = len(ys); trend = np.empty(n)
    half = window // 2
    for i in range(n):
        a, b = max(0, i - half), min(n, i + half + 1)
        yy = ys[a:b].astype(float); xx = xs[a:b].astype(float)
        if b - a < 5:
            trend[i] = xs[i]
            continue
        c = np.polyfit(yy - yy.mean(), xx, 2)
        trend[i] = np.polyval(c, ys[i] - yy.mean())
    return trend

def trace_region(mask, y0px, y1px, x0px, x1px):
    """Per-row centerline + width of orange ink inside the box."""
    sub = mask[y0px:y1px, x0px:x1px]
    rows, cx_list, w_list = [], [], []
    for r in range(sub.shape[0]):
        cols_i = np.flatnonzero(sub[r])
        if cols_i.size == 0:
            continue
        rows.append(r + y0px)
        cx_list.append(cols_i.mean() + x0px)
        w_list.append(cols_i.size)
    return np.array(rows), np.array(cx_list), np.array(w_list)

def wobble_stats(rows, cx, label):
    trend = smooth_fit(cx, rows)
    dev = cx - trend
    # sign flips of the high-frequency residual (twist count), ignoring <0.15px noise
    s = np.where(np.abs(dev) < 0.15, 0, np.sign(dev))
    nz = s[s != 0]
    flips = int(np.sum(nz[1:] * nz[:-1] < 0)) if nz.size > 1 else 0
    ad = np.abs(dev)
    print(f"  {label}: rows={len(rows)} maxdev={ad.max():.2f}px ({ad.max()/PXPT:.2f}pt) "
          f"mean={ad.mean():.2f}px p95={np.percentile(ad,95):.2f}px signflips={flips}")
    return ad.max(), ad.mean(), flips, trend, dev

def analyze_render(tag):
    im = np.asarray(Image.open(QA + tag).convert("RGB"))
    mask = orange_mask(im)
    # sanity: orange annotation text (E8A020) must NOT be in mask
    ann = im[398:530, 40:360]  # annotation zone x<180pt,y<530pt region in px approx
    print(f"== {tag}: mask px total={mask.sum()}")
    results = {}
    for unit, uy in UNITS.items():
        for ci, cx in enumerate(COLS):
            x0 = int((cx + DX - 2) * PXPT); x1 = int((cx + DX + W_PT + 2) * PXPT)
            y0 = int(uy["y0"] * PXPT) - 4; y1 = int(uy["y1"] * PXPT) + 4
            rows, cxs, ws = trace_region(mask, y0, y1, x0, x1)
            if len(rows) < 20:
                print(f"  {unit} col{ci} (cx={cx}): NO TRACE ({len(rows)} rows)")
                continue
            label = f"{unit} col{ci} cx={cx}"
            mx, mn, fl, trend, dev = wobble_stats(rows, cxs, label)
            results[(unit, ci)] = dict(rows=rows, cx=cxs, w=ws, trend=trend, dev=dev,
                                       max=mx, mean=mn, flips=fl)
    return results, mask, im

def analyze_original():
    im = np.asarray(Image.open(VID + "unique_slides/slide_046.jpg").convert("RGB"))
    H, Wd = im.shape[:2]
    # frame mapping (worker report m-series): frame_x = slide_x*0.962329 + 17.582 ; frame_y = slide_y*0.955556
    fx = lambda sx: sx * 0.962329 + 17.582
    fy = lambda sy: sy * 0.955556
    # sample arrow colors on the original: probe the uB col0 arrow vertical section
    mask = orange_mask(im, rmin=150, gmin=50, gmax=165, bmax=120)
    print(f"== original frame ({Wd}x{H}): washed-orange mask px total={mask.sum()}")
    res = {}
    for unit, uy in UNITS.items():
        for ci, cx in enumerate(COLS):
            x0 = int(fx(cx + DX - 2)); x1 = int(fx(cx + DX + W_PT + 2)) + 1
            y0 = int(fy(uy["y0"])) - 3; y1 = int(fy(uy["y1"])) + 3
            rows, cxs, ws = trace_region(mask, y0, y1, x0, x1)
            if len(rows) < 12:
                print(f"  {unit} col{ci} (cx={cx}): NO TRACE ({len(rows)} rows)")
                continue
            # scale original px -> render px equivalent: render is 2.0833 px/pt, frame is 960/540 => 1px frame = 1pt-ish? frame 960px wide = 13.33in*72=960pt => 1px = 1pt. deviations in frame px * (PXPT*0.9556..) ~ report in frame px and pt
            label = f"{unit} col{ci} cx={cx}"
            trend = smooth_fit(cxs, rows, window=9)
            dev = cxs - trend
            ad = np.abs(dev)
            s = np.where(np.abs(dev) < 0.12, 0, np.sign(dev))
            nz = s[s != 0]
            flips = int(np.sum(nz[1:] * nz[:-1] < 0)) if nz.size > 1 else 0
            print(f"  {label}: rows={len(rows)} maxdev={ad.max():.2f}fpx mean={ad.mean():.2f}fpx "
                  f"p95={np.percentile(ad,95):.2f}fpx signflips={flips} width_mean={ws.mean():.1f}fpx")
            res[(unit, ci)] = (ad.max(), ad.mean(), flips)
    return res, mask, im

if __name__ == "__main__":
    print("### BEFORE-FIX RENDER TRACE (render_before_afix.png, 150dpi, 2.0833 px/pt)")
    before, bmask, bim = analyze_render("render_before_afix.png")
    print()
    print("### ORIGINAL FRAME TRACE (unique_slides/slide_046.jpg, 960x540, 1px~1pt)")
    orig, omask, oim = analyze_original()
    print()
    # save crops for visual banking: one arrow per unit at high zoom
    for (unit, ci), d in before.items():
        if ci != 3:
            continue
        r0, r1 = d["rows"].min() - 8, d["rows"].max() + 8
        x0 = int((COLS[ci] + DX - 3) * PXPT); x1 = int((COLS[ci] + DX + W_PT + 3) * PXPT)
        crop = Image.fromarray(bim[int(r0):int(r1), x0:x1])
        z = 3
        crop = crop.resize((crop.width * z, crop.height * z), Image.NEAREST)
        crop.save(QA + f"afix_arrow_{unit}_c{ci}_before.png")
        print("saved", f"afix_arrow_{unit}_c{ci}_before.png", crop.size)
    # original counterpart crops
    fx = lambda sx: sx * 0.962329 + 17.582
    fy = lambda sy: sy * 0.955556
    for unit, uy in UNITS.items():
        x0 = int(fx(COLS[3] + DX - 3)); x1 = int(fx(COLS[3] + DX + W_PT + 3))
        y0 = int(fy(uy["y0"])) - 4; y1 = int(fy(uy["y1"])) + 4
        crop = Image.fromarray(oim[y0:y1, x0:x1])
        z = 5
        crop = crop.resize((crop.width * z, crop.height * z), Image.LANCZOS)
        crop.save(QA + f"afix_arrow_{unit}_c3_orig.png")
        print("saved", f"afix_arrow_{unit}_c3_orig.png", crop.size)
    # aggregate
    if before:
        mx = max(v["max"] for v in before.values())
        mn = float(np.mean([v["mean"] for v in before.values()]))
        fl = sum(v["flips"] for v in before.values())
        print(f"\nBEFORE aggregate: worst maxdev={mx:.2f}px ({mx/PXPT:.2f}pt) mean-of-means={mn:.2f}px total signflips={fl}")
