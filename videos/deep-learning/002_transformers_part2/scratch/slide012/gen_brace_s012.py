#!/usr/bin/env python3
# gen_brace_s012.py — curly-brace -> 600dpi transparent PNG pattern (qa/slide010/
# gen_brace_pattern.py, certified on slide 010), parameterized for slide 012's four
# thin red braces (2 tall flanking the panel band, 2 short flanking the strip band).
# Frame-measured (scratch/slide012/measure9/10_output.txt), frame px (1px = 1pt):
#   tall "{": ink fx 241..253 (spine 243..246, tips ->252), fy 152..337  (h 185, w 12)
#   tall "}": ink fx 714..728 (spine 724..726, tips ->714), fy 152..337  (h 185, w 14)
#   short "{": ink fx 242..253, fy 349..388 (h 39, w 11)
#   short "}": ink fx 719..730, fy 349..388 (h 39, w 11)
# Embed at EXACT size: w = px_w/600 in, h = px_h/600 in (pattern law). Sidecar JSON
# carries the exact numbers; slide_012.js reads them.
import json
from PIL import Image, ImageDraw

DPI = 600
COL = "C00000"
PAD = 1.0

def bez(p0, p1, p2, p3, n=80):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] + 3*(1-t)*t*t*p2[0] + t**3*p3[0]
        y = (1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] + 3*(1-t)*t*t*p2[1] + t**3*p3[1]
        pts.append((x, y))
    return pts

def brace_path(H, W):
    # "{" in local pt coords: spine left, vertex mid-left, tips right at top/bottom.
    # Proportions follow the certified s010 path (hook depth ~0.085H, vertex ~0.5H).
    sp = W * 0.42          # spine x
    vx = W * 0.06          # vertex x (leftmost)
    tip = W * 0.94         # hook tip x
    hy = H * 0.085         # hook vertical depth
    pts = []
    pts += bez((tip, 0.0), (tip - 0.10 * W, hy * 0.38), (sp + 0.12 * W, hy * 0.62), (sp, hy))
    pts += bez((sp, hy), (sp, H * 0.30), (vx + 0.28 * W, H * 0.40), (vx, H * 0.50))
    pts += bez((vx, H * 0.50), (vx + 0.28 * W, H * 0.60), (sp, H * 0.70), (sp, H - hy))
    pts += bez((sp, H - hy), (sp + 0.12 * W, H - hy * 0.62), (tip - 0.10 * W, H - hy * 0.38), (tip, H))
    return pts

def gen(side, H, W, stroke, out):
    scale = DPI / 72.0
    img = Image.new("RGBA", (int(W * scale + 2 * PAD * scale), int(H * scale + 2 * PAD * scale)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pts = brace_path(H, W)
    if side == "rp":  # "}" mirror
        pts = [(W - x, y) for (x, y) in pts]
    pts = [((x + PAD) * scale, (y + PAD) * scale) for (x, y) in pts]
    rgb = tuple(int(COL[i:i + 2], 16) for i in (0, 2, 4)) + (255,)
    d.line(pts, fill=rgb, width=max(2, int(round(stroke * scale))), joint="curve")
    bbox = img.getbbox()
    img = img.crop(bbox)
    img.save(out)
    sidecar = {"image": out, "px_w": img.size[0], "px_h": img.size[1],
               "w_in": img.size[0] / DPI, "h_in": img.size[1] / DPI,
               "stroke_pt": stroke, "color": COL, "span_pt": H}
    open(out.replace(".png", ".json"), "w").write(json.dumps(sidecar, indent=1))
    print(out, img.size, "w_in=%.4f h_in=%.4f" % (img.size[0] / DPI, img.size[1] / DPI))

A = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/"
gen("lp", 185.0, 12.0, 1.6, A + "s012_brace_tall_L.png")
gen("rp", 185.0, 14.0, 1.6, A + "s012_brace_tall_R.png")
gen("lp", 39.0, 11.0, 1.6, A + "s012_brace_short_L.png")
gen("rp", 39.0, 11.0, 1.6, A + "s012_brace_short_R.png")
