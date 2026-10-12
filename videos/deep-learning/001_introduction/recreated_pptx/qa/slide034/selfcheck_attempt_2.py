#!/usr/bin/env python3
"""Closed-loop self-check: render_2.png (2001x1125 @150dpi) vs slide_034.jpg (960x540).

Frame-px = render-px * 72/150 (i.e. *0.48). Tolerance ~4 render-px (~2 frame-px) for
positions, ~8 render-px for sizes. Banked as selfcheck_attempt_1_out.txt.
"""
import numpy as np
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
ren = np.asarray(Image.open(f"{BASE}/recreated_pptx/qa/slide034/render_2.png").convert("RGB")).astype(int)
org = np.asarray(Image.open(f"{BASE}/unique_slides/slide_034.jpg").convert("RGB")).astype(int)
S = 150 / 72.0  # render px per frame px (~2.0833)

def runs(idx):
    out, s, p = [], None, None
    for i in idx:
        if s is None: s = p = i
        elif i == p + 1: p = i
        else: out.append((s, p)); s = p = i
    if s is not None: out.append((s, p))
    return out

def frame_bbox(im, mask, x0, y0, x1, y1):
    ys, xs = np.where(mask[y0:y1, x0:x1])
    if len(xs) == 0:
        return None
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max(), len(xs))

def report(tag, tb, ob, tol=4.0):
    if tb is None or ob is None:
        print(f"  {tag}: MISSING render={tb} original={ob}")
        return
    f = [v / S for v in tb[:4]]
    print(f"  {tag}: render(frame-px) x {f[0]:.1f}..{f[2]:.1f} y {f[1]:.1f}..{f[3]:.1f} | "
          f"original x {ob[0]}..{ob[2]} y {ob[1]}..{ob[3]} | "
          f"dx0 {f[0]-ob[0]:+.1f} dx1 {f[2]-ob[2]:+.1f} dy0 {f[1]-ob[1]:+.1f} dy1 {f[3]-ob[3]:+.1f}")

R = ren[:, :, 0]; RG = ren[:, :, 1]; RB = ren[:, :, 2]
O = org[:, :, 0]; OG = org[:, :, 1]; OB = org[:, :, 2]
red_r = (R > 120) & (RG < 110) & (RB < 110)
red_o = (O > 120) & (OG < 110) & (OB < 110)
dark_r = (R < 130) & (RG < 130) & (RB < 130)
dark_o = (O < 130) & (OG < 130) & (OB < 130)

print("== 1. title (red ink, window x150..800 y55..125 frame) ==")
report("title", frame_bbox(ren, red_r, int(150*S), int(55*S), int(800*S), int(125*S)),
       frame_bbox(org, red_o, 150, 55, 800, 125))

print("== 2. header (dark ink, x70..380 y195..249) ==")
report("header", frame_bbox(ren, dark_r, int(70*S), int(195*S), int(380*S), int(249*S)),
       frame_bbox(org, dark_o, 70, 195, 380, 255))

print("== 3. label '3-D Filter' (red, x740..875 y225..260) ==")
report("label", frame_bbox(ren, red_r, int(740*S), int(225*S), int(875*S), int(260*S)),
       frame_bbox(org, red_o, 740, 225, 875, 260))

print("== 4. content box strokes ==")
# vertical strokes: red count per col in y 200..470 frame
for tag, x0, x1 in [("left stroke", 55, 75), ("right stroke", 885, 905)]:
    cr = red_r[int(200*S):int(470*S), int(x0*S):int(x1*S)].sum(axis=0)
    co = red_o[200:470, x0:x1].sum(axis=0)
    xr = np.where(cr > 100)[0]; xo = np.where(co > 100)[0]
    print(f"  {tag}: render cols {[(x0 + v/S).__round__(1) for v in xr]} | original {list(x0 + xo)}")
for tag, y0, y1 in [("top stroke", 160, 180), ("bottom stroke", 480, 500)]:
    cr = red_r[int(y0*S):int(y1*S), int(100*S):int(850*S)].sum(axis=1)
    co = red_o[y0:y1, 100:850].sum(axis=1)
    xr = np.where(cr > 200)[0]; xo = np.where(co > 200)[0]
    print(f"  {tag}: render rows {[(y0 + v/S).__round__(1) for v in xr]} | original {list(y0 + xo)}")

print("== 5. crop regions (nonwhite bbox; window = crop box ±6) ==")
nw_r = (R < 244) | (RG < 244) | (RB < 244)
nw_o = (O < 244) | (OG < 244) | (OB < 244)
for tag, (x0, y0, x1, y1) in [("meme", (83, 251, 331, 445)), ("rgbstack", (438, 218, 728, 453)),
                               ("cube", (680, 268, 881, 457))]:
    report(tag,
           frame_bbox(ren, nw_r, int((x0-4)*S), int((y0-4)*S), int((x1+4)*S), int((y1+4)*S)),
           frame_bbox(org, nw_o, x0-4, y0-4, x1+4, y1+4), tol=6)

print("== 6. background sampling ==")
pts = [((60, 250), "inside box left gap"), ((480, 190), "box top strip"), ((900, 300), "right gap"),
       ((480, 497), "below box"), ((300, 130), "panel above box")]
for (x, y), tag in pts:
    print(f"  ({x},{y}) {tag}: render {tuple(ren[int(y*S), int(x*S)])} vs original {tuple(org[y, x])}")

print("== 7. matrix presence (red ink inside meme area, x100..320 y280..445) ==")
mr = frame_bbox(ren, red_r, int(100*S), int(280*S), int(320*S), int(445*S))
mo = frame_bbox(org, red_o, 100, 280, 320, 445)
report("matrix", mr, mo, tol=6)
print(f"  matrix ink px: render {mr[4] if mr else 0} vs original {mo[4] if mo else 0}")
