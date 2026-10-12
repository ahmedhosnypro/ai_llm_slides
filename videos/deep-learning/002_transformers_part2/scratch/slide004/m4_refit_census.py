#!/usr/bin/env python3
# m4_refit_census.py — definitive frame->render fit (robust border landmarks) +
# orange-highlight connected components + palette census.
# Frame 960x540 (1px = 1pt), render 2001x1125 (150dpi, 1px = 1/150 in).
import numpy as np
from PIL import Image

S = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004"
B = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning"
frame_im = Image.open(f"{B}/002_transformers_part2/unique_slides/slide_004.jpg").convert("RGB")
render = np.asarray(Image.open(f"{S}/base-1.png").convert("RGB"), dtype=np.float64)
frame = np.asarray(frame_im, dtype=np.float64)
H, W = frame.shape[:2]

def redness(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return np.clip(r - (g + b) / 2, 0, None) * (r > 120)

# --- top border: row with the LONGEST horizontal red run (border spans panel; title doesn't) ---
red = redness(frame) > 60
best_row, best_run = None, 0
for y in range(0, H // 3):
    row = red[y]
    # longest run
    run = cur = 0
    for v in row:
        cur = cur + 1 if v else 0
        run = max(run, cur)
    if run > best_run:
        best_run, best_row = run, y
print(f"frame top border row {best_row} (longest red run {best_run})")

def vstroke_center(a, x0, x1, y0, y1):
    w = redness(a[y0:y1, x0:x1])
    xs = np.arange(x0, x1)
    return (w.sum(axis=0) * xs).sum() / w.sum()

def hstroke_center(a, x0, x1, y0, y1):
    w = redness(a[y0:y1, x0:x1])
    ys = np.arange(y0, y1)
    return (w.sum(axis=1) * ys).sum() / w.sum()

fl = vstroke_center(frame, 54, 64, 150, 450)
fr_ = vstroke_center(frame, 896, 907, 150, 450)
ft = hstroke_center(frame, 300, 660, best_row - 3, best_row + 4)
fb = hstroke_center(frame, 300, 660, 512, 520)
print(f"frame borders: L {fl:.2f} R {fr_:.2f} T {ft:.2f} B {fb:.2f}")
rl = vstroke_center(render, 80, 95, 300, 900)
rr = vstroke_center(render, 1908, 1922, 300, 900)
rt = hstroke_center(render, 600, 1320, 88, 100)
rb = hstroke_center(render, 600, 1320, 1118, 1125)
print(f"render borders: L {rl:.2f} R {rr:.2f} T {rt:.2f} B {rb:.2f}")

def badge_center(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (r > 200) & (g > 200) & (b < 190) & (np.abs(r - g) < 40)
    m[int(a.shape[0] * 0.4):, :] = False
    m[:, : int(a.shape[1] * 0.7)] = False
    ys, xs = np.where(m)
    return xs.mean(), ys.mean()

fbx, fby = badge_center(frame)
rbx, rby = badge_center(render)
print(f"badge: frame ({fbx:.2f},{fby:.2f}) render ({rbx:.2f},{rby:.2f})")

# LSQ per axis on 3 correspondences
fx_pts = np.array([fl, fr_, fbx]); rx_pts = np.array([rl, rr, rbx])
fy_pts = np.array([ft, fb, fby]); ry_pts = np.array([rt, rb, rby])
A = np.vstack([fx_pts, np.ones(3)]).T
sx, ax = np.linalg.lstsq(A, rx_pts, rcond=None)[0]
Bm = np.vstack([fy_pts, np.ones(3)]).T
sy, ay = np.linalg.lstsq(Bm, ry_pts, rcond=None)[0]
print(f"FIT: render_x = {ax:.3f} + {sx:.6f}*frame_x   residuals {np.round(ax + sx*fx_pts - rx_pts, 2)}")
print(f"FIT: render_y = {ay:.3f} + {sy:.6f}*frame_y   residuals {np.round(ay + sy*fy_pts - ry_pts, 2)}")
# slide-space (pt) equivalent: slide_pt = render_px * 72/150
k = 72.0 / 150.0
print(f"slide_x_pt = {ax*k:.3f} + {sx*k:.6f}*frame_x ; slide_y_pt = {ay*k:.3f} + {sy*k:.6f}*frame_y")
np.save(f"{S}/fit3.npy", np.array([ax, sx, ay, sy]))

# --- orange connected components in FRAME (candidate highlight rects) ---
r, g, b = frame[..., 0], frame[..., 1], frame[..., 2]
m = (r > 200) & (b < 175) & (g > 130) & (g < 225) & ((r - b) > 60) & ((g - b) > 25)
# connected components via BFS (4-neighborhood), min size 300
lab = np.zeros((H, W), np.int32)
cur = 0
from collections import deque
comps = []
mm = m.copy()
for y in range(H):
    for x in range(W):
        if mm[y, x]:
            cur += 1
            q = deque([(y, x)]); mm[y, x] = False
            pts = []
            while q:
                cy, cx = q.popleft(); pts.append((cy, cx))
                for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < H and 0 <= nx < W and mm[ny, nx]:
                        mm[ny, nx] = False; q.append((ny, nx))
            if len(pts) >= 300:
                ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
                comps.append((len(pts), min(xs), max(xs), min(ys), max(ys)))
comps.sort(reverse=True)
print("\nframe orange components (n, x0..x1, y0..y1) [frame px = slide pt]:")
for n, x0, x1, y0, y1 in comps[:12]:
    print(f"  n={n:6d}  x {x0}..{x1}  y {y0}..{y1}   (slide pt: x {x0}..{x1} y {y0}..{y1})")

# mean color inside each big component
for n, x0, x1, y0, y1 in comps[:4]:
    sel = m[y0:y1+1, x0:x1+1]
    px = frame[y0:y1+1, x0:x1+1][sel]
    print(f"  comp x{x0}..{x1} y{y0}..{y1}: mean orange RGB {px.mean(axis=0).round(1)}")

# --- palette census: sample clean interior spots (frame coords) vs render (mapped) ---
def sample(a, x, y, rad=3):
    return a[int(y)-rad:int(y)+rad+1, int(x)-rad:int(x)+rad+1].reshape(-1, 3).mean(axis=0)

spots = {
    "encoder zone peach (x620,y160)": (620, 160),
    "decoder zone mint (x860,y300)": (860, 300),
    "decoder zone mint (x870,y200)": (870, 200),
    "left panel white (x250,y200)": (250, 200),
    "gutter bg (x520,y150)": (520, 150),
    "chrome margin top (x300,y20)": (300, 20),
    "left margin (x20,y270)": (20, 270),
    "FF box blue L (x180,y368)": (180, 368),
    "attn yellow R (x790,y360)": (790, 360),
    "title red (x350,y66)": (350, 66),
}
print("\npalette census (frame RGB vs base-render RGB at mapped spot):")
for name, (x, y) in spots.items():
    fc = sample(frame, x, y)
    rx, ry = ax + sx * x, ay + sy * y
    rc = sample(render, rx, ry) if 0 <= int(ry) < render.shape[0] and 0 <= int(rx) < render.shape[1] else None
    print(f"  {name}: frame {fc.round(0)}  render {rc.round(0) if rc is not None else '-'}")

# --- warp + diff for the record ---
warp = np.asarray(frame_im.transform((render.shape[1], render.shape[0]), Image.AFFINE,
    (1/sx, 0, -ax/sx, 0, 1/sy, -ay/sy), resample=Image.BILINEAR), dtype=np.float64)
Image.fromarray(warp.astype(np.uint8)).save(f"{S}/frame_warped3.png")
diff = np.abs(warp - render).sum(axis=2)
valid = np.zeros(diff.shape, bool)
valid[int(rt)+6:int(rb)-2, int(rl)+6:int(rr)-2] = True
np.save(f"{S}/diff3.npy", diff)
print(f"\nwarp diff: mean {diff[valid].mean():.2f} median {np.median(diff[valid]):.2f} p95 {np.percentile(diff[valid],95):.1f}")
