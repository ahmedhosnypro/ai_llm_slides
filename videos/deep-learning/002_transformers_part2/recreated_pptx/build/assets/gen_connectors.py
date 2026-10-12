#!/usr/bin/env python3
"""Dashed green curved connectors (bottom container -> side containers) as 600dpi
transparent PNGs. Quadratic Bezier through frame-space control points, embedded at
exact px/600 size. Frame->slide mapping: sx=(fx-18.63)/0.96123, sy=fy/0.95556."""
from PIL import Image, ImageDraw
import numpy as np

GREEN = (146, 208, 80, 255)   # 92D050
DPI = 600
PX_PER_PT = DPI / 72.0

def bezier(p0, p1, p2, n=400):
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * np.array(p0) + 2 * (1 - t) * t * np.array(p1) + t ** 2 * np.array(p2)

def render(name, p0, p1, p2, dash_pt=4.0, gap_pt=3.0, width_pt=1.0):
    pts = bezier(p0, p1, p2)                      # frame px coords
    spts = np.stack([(pts[:, 0] - 18.63) / 0.96123, pts[:, 1] / 0.95556], axis=1)  # slide pt
    # cumulative length in slide pt
    d = np.concatenate([[0], np.cumsum(np.hypot(np.diff(spts[:, 0]), np.diff(spts[:, 1])))])
    total = d[-1]
    img_w = int(np.ptp(spts[:, 0]) * PX_PER_PT) + 40
    img_h = int(np.ptp(spts[:, 1]) * PX_PER_PT) + 40
    img = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    ox = -spts[:, 0].min() * PX_PER_PT + 20
    oy = -spts[:, 1].min() * PX_PER_PT + 20
    # dashed stroke
    pat = dash_pt + gap_pt
    dist = 0.0
    i = 0
    while dist < total:
        seg_end = min(dist + dash_pt, total)
        # collect points within [dist, seg_end]
        mask = (d >= dist) & (d <= seg_end)
        xy = [(spts[j, 0] * PX_PER_PT + ox, spts[j, 1] * PX_PER_PT + oy) for j in np.where(mask)[0]]
        if len(xy) > 1:
            dr.line(xy, fill=GREEN, width=max(1, int(round(width_pt * PX_PER_PT))))
        dist += pat
    # trim to content
    bbox = img.getbbox()
    img = img.crop(bbox)
    img.save(name)
    w_px, h_px = img.size
    print(f'{{"path": "{name}", "w_px": {w_px}, "h_px": {h_px}, "w_in": {w_px/DPI:.4f}, "h_in": {h_px/DPI:.4f}, "off_pt": [({spts[:,0].min():.2f}, {spts[:,1].min():.2f})], "dpi": {DPI}}}')

# LEFT connector: bottom container left end (193,478) -> left container bottom (125,381), sag left
render("conn_left.png", (193, 478), (128, 468), (125, 381))
# RIGHT connector: bottom container right end (490,478) -> right container bottom (770,381)
render("conn_right.png", (490, 478), (620, 468), (770, 381))
