#!/usr/bin/env python3
# m2_diff.py — refine fit (LSQ incl. measured badge centroids), warp frame into
# render space, diff, and report delta blocks. Also verify base render == parent's
# certified render outside the badge numeral.
import numpy as np
from PIL import Image

S = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004"
P15 = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide015/render_1.png"
frame_im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_004.jpg").convert("RGB")
render = np.asarray(Image.open(S + "/base-1.png").convert("RGB"), dtype=np.float64)
cert = np.asarray(Image.open(P15).convert("RGB"), dtype=np.float64)
frame = np.asarray(frame_im, dtype=np.float64)

def badge_center(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (r > 200) & (g > 200) & (b < 190) & (np.abs(r - g) < 40)
    m[int(a.shape[0] * 0.4):, :] = False
    m[:, : int(a.shape[1] * 0.7)] = False
    ys, xs = np.where(m)
    return xs.mean(), ys.mean()

fbx, fby = badge_center(frame)
rbx, rby = badge_center(render)
print(f"frame badge centroid ({fbx:.2f},{fby:.2f})  render badge centroid ({rbx:.2f},{rby:.2f})")

# correspondences: (frame, render) per axis
fx_pts = np.array([59.00, 901.00, fbx]); rx_pts = np.array([87.00, 1914.50, rbx])
fy_pts = np.array([43.00, 516.00, fby]); ry_pts = np.array([93.50, 1124.00, rby])
A = np.vstack([fx_pts, np.ones(3)]).T
sx, ax = np.linalg.lstsq(A, rx_pts, rcond=None)[0]
B = np.vstack([fy_pts, np.ones(3)]).T
sy, ay = np.linalg.lstsq(B, ry_pts, rcond=None)[0]
resx = ax + sx * fx_pts - rx_pts
resy = ay + sy * fy_pts - ry_pts
print(f"LSQ: render_x = {ax:.3f} + {sx:.6f}*frame_x  residuals {np.round(resx,2)}")
print(f"LSQ: render_y = {ay:.3f} + {sy:.6f}*frame_y  residuals {np.round(resy,2)}")

# --- inheritance check: my base render vs 001:15 certified render ---
if cert.shape == render.shape:
    d = np.abs(render - cert).sum(axis=2)
    # ignore the badge area (numeral 4 vs 15)
    mask = np.ones(render.shape[:2], bool)
    mask[int(147.9 - 45):int(147.9 + 45), int(1860.4 - 45):int(1860.4 + 45)] = False
    print(f"base vs certified 001:15 render: max diff outside badge {d[mask].max():.0f}, mean {d[mask].mean():.3f}")
else:
    print("certified render shape differs:", cert.shape, render.shape)

# --- warp frame into render space ---
W, H = render.shape[1], render.shape[0]
warped = np.asarray(frame_im.transform((W, H), Image.AFFINE,
    (1 / sx, 0, -ax / sx, 0, 1 / sy, -ay / sy), resample=Image.BILINEAR), dtype=np.float64)
Image.fromarray(warped.astype(np.uint8)).save(S + "/frame_warped.png")

diff = np.abs(warped - render).sum(axis=2)
# valid slide area: inside chrome panel borders
valid = np.zeros((H, W), bool)
valid[int(ry_pts[0]) + 4: int(ry_pts[1]), int(rx_pts[0]) + 4: int(rx_pts[1])] = True

# block report 16x16
bs = 16
hb, wb = H // bs, W // bs
bd = diff[: hb * bs, : wb * bs].reshape(hb, bs, wb, bs).mean(axis=(1, 3))
bv = valid[: hb * bs, : wb * bs].reshape(hb, bs, wb, bs).mean(axis=(1, 3)) > 0.9
idx = np.argsort(bd[bv])[::-1][:40]
coords = np.argwhere(bv)
order = np.argsort(bd[bv])[::-1]
print("top diff blocks (render px, mean abs diff):")
for k in order[:40]:
    y, x = coords[k]
    print(f"  ({x * bs:4d},{y * bs:4d}) mean {bd[y, x]:7.1f}")

print(f"overall masked mean diff {diff[valid].mean():.2f}, median {np.median(diff[valid]):.2f}, p95 {np.percentile(diff[valid], 95):.1f}")
np.save(S + "/diff.npy", diff)
np.save(S + "/fit2.npy", np.array([ax, sx, ay, sy]))
