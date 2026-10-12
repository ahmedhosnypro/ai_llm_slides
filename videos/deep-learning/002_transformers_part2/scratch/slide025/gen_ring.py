#!/usr/bin/env python3
"""Generate the slide-025 encoder-disk image (traces + hub + dashes + two arc arrows)
and the motor clip. All geometry in FRAME px (960x540, 1px=1pt pre-mapping); the PNG is
rendered at 4x and embedded at EXACT mapped size (w = frame_w/0.96123/72 in)."""
from PIL import Image
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_025.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets"

im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
redm = (r - g > 60) & (r - b > 50) & (r > 110)
greenm = (g - r > 30) & (g - b > 20) & (g > 70)
graym = (np.abs(r - g) < 25) & (np.abs(g - b) < 25) & (r > 90) & (r < 225)

CX, CY = 592.0, 265.5
IB = (477, 147, 733, 385)  # image bbox in frame px

# ---- trace fit: r(theta) = R0 + C cos(16t) + D sin(16t), theta = y-down angle
def fit_trace(mask, name):
    sub = np.zeros_like(mask)
    y0, y1, x0, x1 = IB[1], IB[3], IB[0], IB[2]
    sub[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    sub[199:233, 718:755] = False   # cos/sin label zone
    yy, xx = np.nonzero(sub)
    d = np.hypot(xx - CX, yy - CY)
    t = np.arctan2(yy - CY, xx - CX)  # y-down
    sel = (d > 55) & (d < 145)
    t, d = t[sel], d[sel]
    bins = ((np.degrees(t) % 360) / 0.25).astype(int)
    T, R = [], []
    for k in np.unique(bins):
        m = bins == k
        if m.sum() >= 2:
            T.append(np.median(t[m])); R.append(np.median(d[m]))
    T = np.array(T); R = np.array(R)
    M = np.stack([np.ones(len(T)), np.cos(16 * T), np.sin(16 * T)], axis=1)
    sol, *_ = np.linalg.lstsq(M, R, rcond=None)
    R0, C16, S16 = sol
    A = np.hypot(C16, S16)
    ph = np.degrees(np.arctan2(S16, C16))  # r = R0 + A*cos(16t - ph)
    pred = M @ sol
    rms = np.sqrt(np.mean((R - pred) ** 2))
    print(f"{name}: R0={R0:.2f} A={A:.2f} phase={ph:.2f}deg (y-down) rms={rms:.2f} n={len(T)}")
    return R0, A, ph

R0r, Ar, phr = fit_trace(redm, "red")
R0g, Ag, phg = fit_trace(greenm, "green")
R0, A = (R0r + R0g) / 2, (Ar + Ag) / 2
print(f"shared: R0={R0:.2f} A={A:.2f}")

# ---- hub circle fit (gray px, r<20)
yy, xx = np.nonzero(graym[int(CY) - 22:int(CY) + 22, int(CX) - 22:int(CX) + 22])
px = xx + int(CX) - 22; py = yy + int(CY) - 22
d0 = np.hypot(px - CX, py - CY)
k = (d0 > 5) & (d0 < 19)
x, y = px[k].astype(float), py[k].astype(float)
Mm = np.stack([x, y, np.ones_like(x)], axis=1)
sol, *_ = np.linalg.lstsq(Mm, x**2 + y**2, rcond=None)
hcx, hcy = sol[0] / 2, sol[1] / 2
hrad = np.sqrt(sol[2] + hcx**2 + hcy**2)
dres = np.abs(np.hypot(x - hcx, y - hcy) - hrad)
k2 = dres < 2
sol2, *_ = np.linalg.lstsq(np.stack([x[k2], y[k2], np.ones(k2.sum())], axis=1), x[k2]**2 + y[k2]**2, rcond=None)
hcx, hcy = sol2[0] / 2, sol2[1] / 2
hrad = np.sqrt(sol2[2] + hcx**2 + hcy**2)
print(f"hub: center ({hcx:.1f},{hcy:.1f}) r={hrad:.2f} n={k2.sum()}")

# ---- draw at 4x
S = 4
W, H = (IB[2] - IB[0]) * S, (IB[3] - IB[1]) * S
fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, IB[2] - IB[0]); ax.set_ylim(IB[3] - IB[1], 0)
ax.axis("off")

def fx(x): return (x - IB[0]) * S
def fy(y): return (y - IB[1]) * S

th = np.linspace(0, 2 * np.pi, 4000)
# traces (y-down angles; matplotlib y flipped via fy)
rr = R0r + Ar * np.cos(16 * th - np.radians(phr))
ax.plot(fx(CX + rr * np.cos(th)), fy(CY + rr * np.sin(th)), color="#FF0000", lw=2.3 * S / 2.2, solid_capstyle="round", zorder 	=3)
rg = R0g + Ag * np.cos(16 * th - np.radians(phg))
ax.plot(fx(CX + rg * np.cos(th)), fy(CY + rg * np.sin(th)), color="#00CC00", lw=2.3 * S / 2.2, solid_capstyle="round", zorder=3)

# hub: white fill + gray outline
hub = plt.Circle((fx(hcx), fy(hcy)), hrad * S, facecolor="white", edgecolor="#9A9A9A", linewidth=1.5 * S / 2.2, zorder=4)
ax.add_patch(hub)

# dashed radial lines: hub edge -> far endpoints (measured)
import math
def dash_line(ang_up_deg, far):
    t = math.radians(-ang_up_deg)  # y-down
    x0 = hcx + hrad * math.cos(t) * 0.2
    y0 = hcy + hrad * math.sin(t) * 0.2
    # start just outside hub along direction
    x0 = hcx + (hrad + 1.0) * math.cos(t)
    y0 = hcy + (hrad + 1.0) * math.sin(t)
    ax.plot([fx(x0), fx(far[0])], [fy(y0), fy(far[1])], color="#222222",
            lw=1.3 * S / 2.2, linestyle=(0, (3.6, 2.6)), zorder=2)
dash_line(7.2, (731, 248))
dash_line(-16.3, (720, 303))

# arc arrows: polyline along constant radius + triangle heads
def arc_arrow(r_arc, ang0_up, ang1_up, color="#222222"):
    t0, t1 = math.radians(-ang0_up), math.radians(-ang1_up)
    ts = np.linspace(t0, t1, 200)
    xs = CX + r_arc * np.cos(ts); ys = CY + r_arc * np.sin(ts)
    ax.plot(fx(xs), fy(ys), color=color, lw=1.3 * S / 2.2, zorder=2)
    for t in (t0, t1):
        # tangent direction along increasing t
        tx, ty = -math.sin(t), math.cos(t)
        # head points along +tangent at t1, -tangent at t0
        sgn = 1 if t == t1 else -1
        tipx = CX + r_arc * math.cos(t) + sgn * 5.5 * tx
        tipy = CY + r_arc * math.sin(t) + sgn * 5.5 * ty
        # head triangle: tip + two base corners perpendicular
        bx = CX + r_arc * math.cos(t) - sgn * 1.5 * tx
        by = CY + r_arc * math.sin(t) - sgn * 1.5 * ty
        px_, py_ = -ty, tx
        tri = np.array([[fx(tipx), fy(tipy)],
                        [fx(bx + 3.2 * px_), fy(by + 3.2 * py_)],
                        [fx(bx - 3.2 * px_), fy(by - 3.2 * py_)]])
        ax.add_patch(plt.Polygon(tri, closed=True, color=color, zorder=2))

# period arc: r~127, from +7.2 to -16.3 (y-up)
arc_arrow(127.0, 7.2, -16.3)
# rotation arc: r~74, from 64.3 to 115.7 (y-up)
arc_arrow(74.0, 64.3, 115.7)

fig.savefig(f"{OUT}/s025_ring.png", transparent=True)
plt.close(fig)
print(f"ring png: {W}x{H}px (4x of {(IB[2]-IB[0])}x{(IB[3]-IB[1])} frame px)")

# ---- motor clip (frame 103,174 - 301,301), white-out AC Motor label (218..288, 212..227)
mot = im.crop((103, 174, 301, 301)).convert("RGB")
ma = np.asarray(mot).copy()
ma[212 - 174:227 - 174 + 1, 218 - 103:288 - 103 + 1] = 255
Image.fromarray(ma).save(f"{OUT}/s025_motor.png")
print(f"motor clip: {mot.size} -> whited label region; saved")
EOF_MARKER = None
