from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_022.jpg').convert('RGB')).astype(float)
H, W, _ = im.shape
R, G, B = im[:,:,0], im[:,:,1], im[:,:,2]
redness = np.clip(R - (G+B)/2, 0, None)

# vertical red strokes: columns 40..80 and 880..920, rows 60..480 (avoid badge/title rows)
def vstroke(x0, x1, y0=60, y1=480):
    band = redness[y0:y1, x0:x1]
    col = band.mean(axis=0)
    xs = np.arange(x0, x1)
    m = col > col.max()*0.5
    cx = (xs[m]*col[m]).sum()/col[m].sum()
    return cx, col.max()
lx, lm = vstroke(40, 85)
rx, rm = vstroke(875, 925)
# horizontal red strokes: rows 30..60 and 500..545, columns 100..850 (avoid badge)
def hstroke(y0, y1, x0=100, x1=850):
    band = redness[y0:y1, x0:x1]
    row = band.mean(axis=1)
    ys = np.arange(y0, y1)
    m = row > row.max()*0.5
    cy = (ys[m]*row[m]).sum()/row[m].sum()
    return cy, row.max()
ty, tm = hstroke(28, 62)
by, bm = hstroke(500, 540)
print(f"left {lx:.2f} (peak {lm:.1f})  right {rx:.2f} (peak {rm:.1f})  top {ty:.2f} (peak {tm:.1f})  bottom {by:.2f} (peak {bm:.1f})")

# fit mapping: left->42, right->918  =>  sx = (rx-lx)/(918-42); ax = lx - 42*sx
sx = (rx-lx)/(918-42); ax = lx - 42*sx
sy = 540.0/516.0  # certified class (bottom stroke -> slide bottom)
ay = 0.0
print(f"sx={sx:.6f} ax={ax:.3f}  => top maps to {ty/sy:.2f} (want 45), bottom to {(by-ay)/sy:.2f} (want 540)")

# badge: yellow circle bbox in frame
yellow = (R>200)&(G>200)&(B<160)
ys, xs = np.where(yellow[40:120, 840:930])
if len(xs): print(f"badge yellow bbox x[{xs.min()+840},{xs.max()+840}] y[{ys.min()+40},{ys.max()+40}] center ({xs.mean()+840:.1f},{ys.mean()+40:.1f})")
# check right-edge zone rows 150..470 for red verticals (020 had them, 021 not)
edge = redness[150:470, 878:900]
print("right-edge redness mean per col:", np.round(edge.mean(axis=0),1))
# letterbox: rows where the whole row is near-black
dark = (R<40)&(G<40)&(B<40)
rowdark = dark.mean(axis=1)
lb = [i for i in range(500, 540) if rowdark[i] > 0.8]
print("letterbox rows:", lb[:5], "...", lb[-5:] if lb else "none", f"(n={len(lb)})")
