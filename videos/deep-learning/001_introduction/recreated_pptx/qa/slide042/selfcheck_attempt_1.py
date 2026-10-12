#!/usr/bin/env python3
"""selfcheck_attempt_1 — slide 042 pre-judge PIL closed-loop check (150dpi render vs original).

Scale: render 2001x1125 / frame 960x540 -> 1 frame px = 2.0844 render px.
Tolerance (equation alignment law): ~4 px @150dpi = ~1.92 frame px.
"""
from PIL import Image
import numpy as np
import sys

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
REN = np.asarray(Image.open(f"{VID}/recreated_pptx/qa/slide042/render_2.png").convert("RGB")).astype(int)
S = REN.shape[1] / 960.0
print(f"render {REN.shape[1]}x{REN.shape[0]}  scale {S:.4f}")

def lum(img):
    return 0.299 * img[..., 0] + 0.587 * img[..., 1] + 0.114 * img[..., 2]

L = lum(REN)
Rc, Gc, Bc = REN[..., 0], REN[..., 1], REN[..., 2]
fails = []

def check(name, got, want, tol=1.92):
    if not isinstance(got, (list, tuple)):
        got, want = [got], [want]
    errs = [abs(g - w) for g, w in zip(got, want)]
    ok = all(e <= tol for e in errs)
    status = "OK " if ok else "FAIL"
    print(f"[{status}] {name}: got {['%.1f' % g for g in got]} want {list(want)} err {['%.1f' % e for e in errs]} (tol {tol} frame px)")
    if not ok:
        fails.append(name)
    return ok

# ---- 1) house chrome: canvas/panel/badge via the certified checker ----
import subprocess
r = subprocess.run(["python3",
                    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome_check.py",
                    f"{VID}/recreated_pptx/qa/slide042/render_2.png"],
                   capture_output=True, text=True)
print("---- house_chrome_check.py ----")
print(r.stdout.strip())
print(r.stderr.strip())
if "FAIL" in (r.stdout + r.stderr):
    fails.append("house_chrome")

# ---- 2) title ink (red) ----
red = (Rc > 110) & (Rc - Gc > 60) & (Rc - Bc > 50)
sub = red[int(60 * S):int(125 * S), int(100 * S):int(860 * S)]
ys, xs = np.nonzero(sub)
check("title x0", xs.min() / S + 100, 186)
check("title x1", xs.max() / S + 100, 778)
check("title y0", ys.min() / S + 60, 80)
check("title y1", ys.max() / S + 60, 112)

# ---- 3) inner panel strokes ----
check("panel left col", int(np.argmax(red[int(140 * S):int(500 * S), int(70 * S):int(85 * S)].sum(0))) / S + 70, 77)
check("panel right col", int(np.argmax(red[int(140 * S):int(500 * S), int(884 * S):int(898 * S)].sum(0))) / S + 884, 891)
check("panel top row", int(np.argmax(red[int(128 * S):int(145 * S), int(90 * S):int(880 * S)].sum(1))) / S + 128, 135.5)
check("panel bottom row", int(np.argmax(red[int(500 * S):int(515 * S), int(90 * S):int(880 * S)].sum(1))) / S + 500, 507.5)

# ---- 4) eq box border (dark) ----
dark = L < 130
check("eqbox left col", int(np.argmax(dark[int(340 * S):int(455 * S), int(310 * S):int(325 * S)].sum(0))) / S + 310, 317.5)
check("eqbox right col", int(np.argmax(dark[int(340 * S):int(455 * S), int(514 * S):int(528 * S)].sum(0))) / S + 514, 520.5)
check("eqbox top row", int(np.argmax(dark[int(328 * S):int(342 * S), int(325 * S):int(515 * S)].sum(1))) / S + 328, 334)
check("eqbox bottom row", int(np.argmax(dark[int(455 * S):int(470 * S), int(325 * S):int(515 * S)].sum(1))) / S + 455, 462)

# ---- 5) big '=' bars ----
d150 = L < 150
b1 = d150[int(260 * S):int(271 * S), int(495 * S):int(528 * S)]
ys, xs = np.nonzero(b1)
check("=bar1 y0", ys.min() / S + 260, 265.9)
check("=bar1 y1", ys.max() / S + 260, 268.7)
check("=bar1 x0", xs.min() / S + 495, 500)
check("=bar1 x1", xs.max() / S + 495, 523)
b2 = d150[int(270 * S):int(279 * S), int(495 * S):int(528 * S)]
ys, xs = np.nonzero(b2)
check("=bar2 y0", ys.min() / S + 270, 272)
check("=bar2 y1", ys.max() / S + 270, 274.6)

# ---- 6) equation ink boxes (render vs original; x-window excludes eqbox border col 519+) ----
EQS = {
    "EQ1": (330, 516, 336, 373, (343, 340, 496, 370)),
    "EQ2": (330, 516, 374, 408, (340, 378, 501, 404)),
    "EQ3": (330, 516, 410, 432, (343, 414, 417, 428)),
    "EQ4": (330, 516, 436, 457, (359, 440, 424, 453)),
}
d175 = L < 175
for name, (x0, x1, y0, y1, want) in EQS.items():
    reg = d175[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)]
    ys, xs = np.nonzero(reg)
    if len(xs) == 0:
        print(f"[FAIL] {name}: NO INK")
        fails.append(name)
        continue
    got = (xs.min() / S + x0, ys.min() / S + y0, xs.max() / S + x0, ys.max() / S + y0)
    check(f"{name} bbox (x0,y0,x1,y1)", got, want)

# ---- 7) legend: blue bands + word extents ----
blue = (Bc - Rc > 40) & (Bc - Gc > 25)
BANDS = [(370, 393, 107, 184), (393, 414, 107, 185), (414, 435, 107, 185),
         (435, 456, 107, 185), (456, 477, 107, 240), (477, 498, 107, 185)]
for i, (y0, y1, wx0, wx1) in enumerate(BANDS):
    reg = blue[int(y0 * S):int(y1 * S), int(85 * S):int(330 * S)]
    ys, xs = np.nonzero(reg)
    if len(xs) == 0:
        print(f"[FAIL] legend L{i+1}: NO BLUE INK")
        fails.append(f"legend L{i+1}")
        continue
    check(f"legend L{i+1} ink (x0,y0,x1,y1)",
          (xs.min() / S + 85, ys.min() / S + y0, xs.max() / S + 85, ys.max() / S + y0),
          (107, [373, 395, 416, 436, 457, 478][i], [180, 182, 185, 183, 239, 180][i],
           [390, 407, 432, 452, 470, 491][i]))

# ---- 8) diagram PNG regions: ink present ----
for name, (x0, y0, x1, y1) in {"slab": (112, 192, 268, 366), "slices": (262, 210, 470, 325),
                               "output": (545, 158, 880, 366)}.items():
    reg = L[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)]
    print(f"[info] {name} region: min lum {reg.min():.0f}  nonwhite frac {float((reg < 235).mean()):.3f}")

print()
print("SELF-CHECK RESULT:", "PASS" if not fails else f"FAIL -> {fails}")
sys.exit(0 if not fails else 1)
