#!/usr/bin/env python3
# gen_brace.py — delimiters-bezier-png pattern variant for CURLY BRACES.
# Original shape measured (slide_010.jpg): "{" spine fx~530-531, vertex fx~524 (mid),
# hooks to fx~537; fy 106..289. "}" mirrored (spine 826, vertex ~832, hooks to ~818).
# Renders one smooth cubic-Bezier centerline stroke at 600dpi, transparent, tight-crop,
# JSON sidecar with exact ink bbox. Embed at EXACT w = px/600 in (pattern law).
import json
from PIL import Image, ImageDraw

DPI = 600
STROKE = 2.1      # pt (frame stroke ~2px)
COL = "4436BC"
PAD = 1.0         # pt canvas padding

def bez(p0, p1, p2, p3, n=60):
    pts=[]
    for i in range(n+1):
        t=i/n
        x=(1-t)**3*p0[0]+3*(1-t)**2*t*p1[0]+3*(1-t)*t*t*p2[0]+t**3*p3[0]
        y=(1-t)**3*p0[1]+3*(1-t)**2*t*p1[1]+3*(1-t)*t*t*p2[1]+t**3*p3[1]
        pts.append((x,y))
    return pts

def brace_path(W, H):
    # "{" in local pt coords: vertex left-middle, hooks right at top/bottom
    sp = 6.5          # spine x
    vx = 0.8          # vertex x (leftmost)
    tip = 13.8        # hook tip x
    pts = []
    pts += bez((tip, 0.0), (tip-1.5, 6.0), (sp+1.5, 8.0), (sp, 16.0))       # top hook
    pts += bez((sp, 16.0), (sp, 55.0), (vx+3.5, 78.0), (vx, 96.0))          # upper spine->vertex
    pts += bez((vx, 96.0), (vx+3.5, 114.0), (sp, 137.0), (sp, 176.0))       # vertex->lower spine
    pts += bez((sp, 176.0), (sp+1.5, 184.0), (tip-1.5, 186.0), (tip, 192.0))# bottom hook
    return pts

def gen(side, out):
    W, H = 16.5, 192.0   # local pt space
    scale = DPI/72.0
    img = Image.new("RGBA", (int(W*scale+2*PAD*scale), int(H*scale+2*PAD*scale)), (0,0,0,0))
    d = ImageDraw.Draw(img)
    pts = brace_path(W, H)
    if side == "rp":   # "}" mirror
        pts = [(W - x, y) for (x, y) in pts]
    pts = [((x+PAD)*scale, (y+PAD)*scale) for (x,y) in pts]
    rgb = tuple(int(COL[i:i+2],16) for i in (0,2,4)) + (255,)
    d.line(pts, fill=rgb, width=int(STROKE*scale), joint="curve")
    bbox = img.getbbox()
    img = img.crop(bbox)
    img.save(out)
    sidecar = {"image": out, "px_w": img.size[0], "px_h": img.size[1],
               "w_in": img.size[0]/DPI, "h_in": img.size[1]/DPI,
               "stroke_pt": STROKE, "color": COL, "span_pt": 192.0}
    open(out.replace(".png", ".json"), "w").write(json.dumps(sidecar, indent=1))
    print(out, img.size, "w_in=%.4f h_in=%.4f" % (img.size[0]/DPI, img.size[1]/DPI))

gen("lp", "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/s010_braceL.png")
gen("rp", "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/s010_braceR.png")
