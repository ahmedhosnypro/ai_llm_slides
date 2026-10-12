#!/usr/bin/env python3
"""Generate the slide-025 encoder-disk image v2 (fixed coordinate system + IoU search).
Axis units = frame px relative to IB origin; figure rendered at 4x (dpi 100).
Search amplitude/phase per trace by mask-IoU against the original frame region."""
from PIL import Image
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import math, io

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_025.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets"

im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
redm = (r - g > 60) & (r - b > 50) & (r > 110)
greenm = (g - r > 30) & (g - b > 20) & (g > 70)
graym = (np.abs(r - g) < 25) & (np.abs(g - b) < 25) & (r > 90) & (r < 225)

CX, CY = 592.0, 265.5
IB = (477, 147, 733, 385)
Wf, Hf = IB[2] - IB[0], IB[3] - IB[1]  # 256 x 238
S = 4  # render scale

def masks(arr):
    rr, gg, bb = arr[..., 0].astype(int), arr[..., 1].astype(int), arr[..., 2].astype(int)
    return ((rr - gg > 60) & (rr - bb > 50) & (rr > 110),
            (gg - rr > 30) & (gg - bb > 20) & (gg > 70))

# original masks restricted to IB (labels whited out of the comparison)
om_r = np.zeros_like(redm); om_r[IB[1]:IB[3], IB[0]:IB[2]] = redm[IB[1]:IB[3], IB[0]:IB[2]]
om_g = np.zeros_like(greenm); om_g[IB[1]:IB[3], IB[0]:IB[2]] = greenm[IB[1]:IB[3], IB[0]:IB[2]]
om_r[199:233, 718:755] = False  # cos/sin label zone (native text, not in image)
om_g[199:233, 718:755] = False

def render(redpar, greenpar, dash_scale=1.0):
    """redpar/greenpar = (R0, A, phase_deg) or None to skip that trace."""
    fig = plt.figure(figsize=(Wf * S / 100, Hf * S / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, Wf); ax.set_ylim(Hf, 0)
    ax.axis("off")
    th = np.linspace(0, 2 * np.pi, 6000)
    for par, col in ((redpar, "#FF0000"), (greenpar, "#00CC00")):
        if par is None:
            continue
        R0, A, ph = par
        rr = R0 + A * np.cos(16 * th - math.radians(ph))
        ax.plot(CX - IB[0] + rr * np.cos(th), CY - IB[1] + rr * np.sin(th),
                color=col, lw=2.2 * S / (100 / 72), solid_capstyle="round", zorder=3)
    hub = plt.Circle((CX - IB[0], CY - IB[1]), 11.0, facecolor="white",
                     edgecolor="#9A9A9A", lw=1.6 * S / (100 / 72), zorder=4)
    ax.add_patch(hub)
    def dash_line(ang_up_deg, far):
        t = math.radians(-ang_up_deg)
        x0 = CX + 12.2 * math.cos(t); y0 = CY + 12.2 * math.sin(t)
        ax.plot([x0 - IB[0], far[0] - IB[0]], [y0 - IB[1], far[1] - IB[1]],
                color="#222222", lw=1.2 * S / (100 / 72),
                linestyle=(0, (3.6 * dash_scale, 2.6 * dash_scale)), zorder=2)
    dash_line(7.2, (731, 248))
    dash_line(-16.3, (720, 303))
    def arc_arrow(r_arc, ang0_up, ang1_up, color="#222222"):
        t0, t1 = math.radians(-ang0_up), math.radians(-ang1_up)
        ts = np.linspace(t0, t1, 300)
        xs = CX + r_arc * np.cos(ts); ys = CY + r_arc * np.sin(ts)
        ax.plot(xs - IB[0], ys - IB[1], color=color, lw=1.2 * S / (100 / 72), zorder=2)
        for t, sgn in ((t0, -1), (t1, 1)):
            tx, ty = -math.sin(t), math.cos(t)
            tipx = CX + r_arc * math.cos(t) + sgn * 5.5 * tx
            tipy = CY + r_arc * math.sin(t) + sgn * 5.5 * ty
            bx = CX + r_arc * math.cos(t) - sgn * 1.5 * tx
            by = CY + r_arc * math.sin(t) - sgn * 1.5 * ty
            px_, py_ = -ty, tx
            tri = np.array([[tipx - IB[0], tipy - IB[1]],
                            [bx + 3.2 * px_ - IB[0], by + 3.2 * py_ - IB[1]],
                            [bx - 3.2 * px_ - IB[0], by - 3.2 * py_ - IB[1]]])
            ax.add_patch(plt.Polygon(tri, closed=True, color=color, zorder=2))
    arc_arrow(127.0, 7.2, -16.3)
    arc_arrow(74.0, 64.3, 115.7)
    # cos/sin leader lines (measured from the 5x leaders_detail vision pass:
    # elbow connectors colored to match their labels, thin ~0.8px, open-V arrowheads)
    def open_v(tip, direction, color):
        import math as _m
        L = 4.2
        for da in (math.radians(152), math.radians(-152)):
            bx = tip[0] + L * _m.cos(direction + da)
            by = tip[1] + L * _m.sin(direction + da)
            ax.plot([tip[0] - IB[0], bx - IB[0]], [tip[1] - IB[1], by - IB[1]],
                    color=color, lw=0.8 * S / (100 / 72), solid_capstyle="round", zorder=2)
    for seg_pts, tip, direction, col in (
            (((719.6, 205.4), (709.6, 205.4), (692.0, 223.0)), (691.2, 224.2),
             math.atan2(224.2 - 205.4, 691.2 - 709.6), "#E03040"),
            (((731.6, 225.6), (718.4, 225.6), (701.6, 239.4)), (700.8, 240.6),
             math.atan2(240.6 - 225.6, 700.8 - 718.4), "#2FA84F")):
        xs_ = [p[0] - IB[0] for p in seg_pts]; ys_ = [p[1] - IB[1] for p in seg_pts]
        ax.plot(xs_, ys_, color=col, lw=0.8 * S / (100 / 72), solid_capstyle="round", zorder=2)
        open_v(tip, direction, col)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", transparent=True)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("RGBA")

def iou(img, orig_mask):
    tgt = img.resize((Wf, Hf), Image.LANCZOS)
    canvas = Image.new("RGB", (960, 540), (255, 255, 255))
    canvas.paste(tgt, (IB[0], IB[1]), tgt)
    cm_r, cm_g = masks(np.asarray(canvas))
    A = cm_r[IB[1]:IB[3], IB[0]:IB[2]] if orig_mask is om_r else cm_g[IB[1]:IB[3], IB[0]:IB[2]]
    inter = (A & orig_mask[IB[1]:IB[3], IB[0]:IB[2]]).sum()
    union = A.sum() + orig_mask[IB[1]:IB[3], IB[0]:IB[2]].sum() - inter
    return inter / max(union, 1)

# ---- search amplitude & phase per trace (R0 from fit)
best = {}
for name, om, R0, ph0 in (("red", om_r, 101.6, 88.8), ("green", om_g, 101.7, 179.6)):
    bb = None
    for A in (3.0, 4.0, 5.0, 6.0, 6.8, 8.0, 10.0, 13.0):
        for dph in (-6, -3, 0, 3, 6):
            img = render(None, (R0, A, ph0 + dph)) if om is om_g else render((R0, A, ph0 + dph), None)
            # render only the searched trace, in its own color
            v = iou(img, om)
            if bb is None or v > bb[0]:
                bb = (v, A, ph0 + dph)
    best[name] = bb
    print(f"{name}: best IoU={bb[0]:.3f} A={bb[1]} phase={bb[2]}")

# final: render both traces with best params
R0r, R0g = 101.6, 101.7
fin = render((R0r,) + best["red"][1:], (R0g,) + best["green"][1:])
fin.save(f"{OUT}/s025_ring.png")
print("saved final ring:", fin.size)

# final IoU report (both traces)
tgt = fin.resize((Wf, Hf), Image.LANCZOS)
canvas = Image.new("RGB", (960, 540), (255, 255, 255))
canvas.paste(tgt, (IB[0], IB[1]), tgt)
cm_r, cm_g = masks(np.asarray(canvas))
for nm, cm, om in (("red", cm_r, om_r), ("green", cm_g, om_g)):
    A2 = cm[IB[1]:IB[3], IB[0]:IB[2]]
    inter = (A2 & om[IB[1]:IB[3], IB[0]:IB[2]]).sum()
    union = A2.sum() + om[IB[1]:IB[3], IB[0]:IB[2]].sum() - inter
    ys, xs = np.nonzero(A2)
    print(f"final {nm}: IoU {inter/max(union,1):.3f} gen px {A2.sum()} bbox x{xs.min()+477}..{xs.max()+477} y{ys.min()+147}..{ys.max()+147}")

# ---- motor clip (frame 103,174 - 301,301), white-out AC Motor label (218..288, 212..227)
mot = im.crop((103, 174, 301, 301)).convert("RGB")
ma = np.asarray(mot).copy()
ma[212 - 174:227 - 174 + 1, 218 - 103:288 - 103 + 1] = 255
Image.fromarray(ma).save(f"{OUT}/s025_motor.png")
print("motor clip saved (198x127)")
