#!/usr/bin/env python3
"""Generate slide 011 diagram assets at 600dpi transparent PNGs.
Coordinates: frame pt (960x540 frame, 1px = 1pt). Each asset declares its canvas
box; the JSON sidecar records it for exact-size embedding.
Assets: red arc (dots+arrowhead), 2 self-loops, dashed cross-attention curves.
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

DPI = 600

def catmull_rom(pts, n=240):
    pts = np.asarray(pts, float)
    if len(pts) < 3:
        t = np.linspace(0, 1, n)
        return np.stack([np.interp(t, [0, 1], pts[:, 0]), np.interp(t, [0, 1], pts[:, 1])], axis=1)
    # pad ends
    p = np.vstack([pts[0] + (pts[0] - pts[1]), pts, pts[-1] + (pts[-1] - pts[-2])])
    out = []
    segs = len(p) - 3
    for i in range(segs):
        p0, p1, p2, p3 = p[i], p[i+1], p[i+2], p[i+3]
        t = np.linspace(0, 1, max(2, n // segs), endpoint=False)
        out.append(0.5 * ((2*p1) + (-p0+p2)*t[:, None] + (2*p0-5*p1+4*p2-p3)*(t**2)[:, None]
                          + (-p0+3*p1-3*p2+p3)*(t**3)[:, None]))
    out.append(p[-2][None, :])
    return np.vstack(out)

def render(name, x0, y0, x1, y1, draw):
    w_pt, h_pt = x1 - x0, y1 - y0
    fig = plt.figure(figsize=(w_pt/72, h_pt/72), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w_pt); ax.set_ylim(h_pt, 0)  # frame y grows downward
    ax.axis("off")
    draw(ax, x0, y0)
    fig.savefig(name, dpi=DPI, transparent=True)
    plt.close(fig)
    info = {"asset": name, "canvas_pt": [x0, y0, x1, y1],
            "w_in": round(w_pt/72, 5), "h_in": round(h_pt/72, 5)}
    with open(name.replace(".png", ".json"), "w") as f:
        json.dump(info, f, indent=1)
    print(json.dumps(info))

# ---------- 1. red arc: dot at (462.5,330) -> curve -> head+dot at (511,263) ----------
ARC_PTS = [(462.5, 329.5), (464.5, 323.5), (467.5, 318), (470.5, 312.5), (473, 306.5),
           (474.5, 300), (475.5, 294), (476.5, 288), (479, 282), (482, 277),
           (486, 272), (490.5, 268.5), (494.5, 266), (499.5, 263.5), (504.5, 262.3),
           (508.5, 262)]

def draw_arc(ax, X0, Y0):
    P = [(x - X0, y - Y0) for (x, y) in ARC_PTS]
    curve = catmull_rom(P)
    ax.plot(curve[:, 0], curve[:, 1], color="#C00000", lw=3.2, solid_capstyle="round", zorder=2)
    # start dot r=4.7 at (462.5,330)
    ax.add_patch(plt.Circle((462.5 - X0, 330 - Y0), 4.7, color="#C00000", zorder=3))
    # end dot r=4.4 + arrowhead tip (517,261.8), barbs back along the approach
    tip = np.array([517 - X0, 261.8 - Y0])
    base_c = np.array([505.5 - X0, 262.2 - Y0])
    d = tip - base_c; d = d / np.linalg.norm(d)
    n = np.array([-d[1], d[0]])
    for s in (+1, -1):
        barb = base_c + s * 5.2 * n
        ax.add_patch(Polygon([tip, barb + 0.0 * d], closed=True, color="#C00000", zorder=1))
    # proper triangle head
    ax.add_patch(Polygon([tip, base_c + 5.2 * n, base_c - 5.2 * n], closed=True,
                         color="#C00000", zorder=3))
    ax.add_patch(plt.Circle((511 - X0, 263 - Y0), 4.4, color="#C00000", zorder=4))

render("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets/arc011_red.png",
       448, 248, 526, 342, draw_arc)

# ---------- 2. self-loops ----------
def make_loop(cx, cy, name):
    # curl: from upper-left down the left side, around the bottom, up the right, head at upper-right
    thetas = np.linspace(np.radians(150), np.radians(395), 120)
    pts = np.stack([cx + 9.4 * np.cos(thetas), cy + 5.1 * np.sin(thetas)], axis=1)
    def draw(ax, X0, Y0):
        q = pts - [X0, Y0]
        ax.plot(q[:, 0], q[:, 1], color="#222222", lw=1.6, solid_capstyle="round")
        # arrowhead at the end, tangent dir
        end = q[-1]; prev = q[-6]
        d = end - prev; d = d / np.linalg.norm(d)
        nvec = np.array([-d[1], d[0]])
        tip = end + 4.6 * d
        b1 = end + 2.6 * nvec; b2 = end - 2.6 * nvec
        ax.add_patch(Polygon([tip, b1, b2], closed=True, color="#222222"))
    render(name, cx - 17, cy - 10, cx + 17, cy + 10, draw)

make_loop(678.2, 288.3, "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets/loop011_1.png")
make_loop(812.0, 288.3, "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets/loop011_2.png")

# ---------- 3. dashed cross-attention curves (pale mauve) ----------
CURVES = {
    "T1": [(334, 233), (366, 237.5), (390, 243), (401, 249), (413, 254), (418, 260),
           (424, 266), (432, 271), (442, 275.5), (452, 279.5), (462, 282.5), (470, 284.5),
           (486, 287), (502, 289.5), (522, 296), (542, 302.5), (564, 308), (588, 313.5),
           (612, 318.5), (636, 322.5), (648, 324)],
    "T2": [(344, 235), (374, 243), (396, 252), (410, 260), (421, 268), (432, 274.5),
           (444, 280), (456, 284), (466, 286.5), (480, 288.5), (496, 291), (512, 294.5),
           (530, 299.5), (548, 304.5), (568, 309.5), (590, 314.5), (614, 319.5), (638, 323)],
    "T3": [(356, 236.5), (384, 247), (404, 258), (416, 266.5), (427, 274), (438, 280),
           (450, 285), (460, 288), (470, 290), (484, 292), (498, 294.5), (512, 298.5),
           (528, 304), (544, 309), (560, 314), (578, 318.5), (598, 322), (616, 324.5)],
    "T4": [(441, 227), (450, 229.5), (458, 233), (464, 237.5), (469, 242.5), (473.5, 248),
           (478, 254.5), (482.5, 261.5), (486.5, 268.5), (490, 275.5), (493, 282),
           (496, 287.5), (499.5, 291.5)],
}

def draw_curves(ax, X0, Y0):
    for key, pts in CURVES.items():
        q = catmull_rom([(x - X0, y - Y0) for (x, y) in pts])
        ax.plot(q[:, 0], q[:, 1], color="#B790A5", lw=1.0,
                dashes=(4, 2.6), solid_capstyle="butt")

render("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets/dashes011.png",
       326, 220, 656, 332, draw_curves)
