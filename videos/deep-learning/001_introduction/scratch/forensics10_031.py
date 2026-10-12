from PIL import Image
import numpy as np

def landmarks(path, name):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(int)
    H, W, _ = a.shape
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    darkred = (R > 100) & (R - G > 50) & (R - B > 40)
    print(f"== {name} ({W}x{H})")
    # left red vline: scan x 30..90, find longest vertical darkred run
    best = None
    for x in range(30, 95):
        col = darkred[:, x]
        rr = np.where(col)[0]
        if len(rr) > 100:
            d = np.diff(rr); splits = np.where(d > 4)[0]
            segs = np.split(rr, splits + 1)
            lg = max(segs, key=len)
            if best is None or len(lg) > best[3]:
                best = (x, lg[0], lg[-1], len(lg))
    print("  left red vline:", best)
    # right red vline: x 870..940
    best = None
    for x in range(860, min(945, W)):
        col = darkred[:, x]
        rr = np.where(col)[0]
        if len(rr) > 100:
            d = np.diff(rr); splits = np.where(d > 4)[0]
            segs = np.split(rr, splits + 1)
            lg = max(segs, key=len)
            if best is None or len(lg) > best[3]:
                best = (x, lg[0], lg[-1], len(lg))
    print("  right red vline:", best)
    # top red hline: y 25..60, longest horizontal run
    best = None
    for y in range(25, 62):
        row = darkred[y, :]
        rr = np.where(row)[0]
        if len(rr) > 300:
            d = np.diff(rr); splits = np.where(d > 4)[0]
            segs = np.split(rr, splits + 1)
            lg = max(segs, key=len)
            if best is None or len(lg) > best[3]:
                best = (y, lg[0], lg[-1], len(lg))
    print("  top red hline:", best)
    # bottom black bar rows
    dark = (R < 90) & (G < 90) & (B < 90)
    for y in range(H - 30, H):
        if dark[y].sum() > 700:
            rr = np.where(dark[y])[0]
            print(f"  black bar y={y}: x {rr[0]}..{rr[-1]} n={len(rr)}")
            break
    # gray field bbox (E9E9E7-ish)
    graybg = (abs(R - 233) < 12) & (abs(G - 233) < 12) & (abs(B - 231) < 12)
    rows = np.where(graybg.sum(axis=1) > 200)[0]
    cols = np.where(graybg.sum(axis=0) > 100)[0]
    if len(rows): print(f"  gray field: y {rows[0]}..{rows[-1]}, x {cols[0]}..{cols[-1]}")

base = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/"
landmarks(base + "slide_005.jpg", "slide_005 (certified, direct 1px=1pt)")
landmarks(base + "slide_031.jpg", "slide_031")
landmarks("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_001.jpg", "REFERENCE 001_transformers_part1/slide_001")
