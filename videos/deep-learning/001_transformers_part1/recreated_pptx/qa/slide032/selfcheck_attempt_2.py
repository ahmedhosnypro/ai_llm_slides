# selfcheck_attempt_2.py — attempt-2 (rebuilt banked script) region deltas, same corrected math.
# Bug in selfcheck_attempt_1.py: delta mixed scales ((rb - fb)/S where fb is in
# frame px). Correct: d = rb/S - fb (all in frame px). Tolerance: ~1.92 frame px
# = 4 px @150dpi; JPEG antialiasing fuzz on the original adds ~1-2 px per edge,
# so treat <=3 frame px as fuzz-pass, >3 as a real look.
import numpy as np
from PIL import Image
FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_032.jpg"
RN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide032/render_2.png"
f = np.asarray(Image.open(FR).convert("RGB")).astype(int)
r = np.asarray(Image.open(RN).convert("RGB")).astype(int)
S = r.shape[1] / f.shape[1]  # 2001/960

def ink_bbox(img, x0, y0, x1, y1, thr=68):
    reg = img[y0:y1, x0:x1]
    mx = reg.max(axis=2); mn = reg.min(axis=2); sat = mx - mn
    white = (mx >= 238) & (sat <= 14)
    gray = (np.abs(reg[:, :, 0] - reg[:, :, 1]) <= 8) & (np.abs(reg[:, :, 1] - reg[:, :, 2]) <= 8) & (mx >= 200) & (mx < 246)
    ink = ~(white | gray)
    ys, xs = np.where(ink)
    if len(xs) == 0:
        return None
    return (int(xs.min()) + x0, int(ys.min()) + y0, int(xs.max()) + x0, int(ys.max()) + y0)

def cmp(name, fb, rb):
    if fb is None or rb is None:
        print(f"{name:26s} MISSING ink frame={fb} render={rb}  FAIL"); return
    d = [rb[i] / S - fb[i] for i in range(4)]
    worst = max(abs(v) for v in d)
    verdict = "OK" if worst <= 3.0 else ("FUZZ" if worst <= 4.5 else "FIX")
    print(f"{name:26s} d(framepx) dx0={d[0]:+5.1f} dy0={d[1]:+5.1f} dx1={d[2]:+5.1f} dy1={d[3]:+5.1f}  worst={worst:.1f}  {verdict}")

regs = {
 "eq panel border": (50, 62, 475, 282),
 "pill block": (64, 100, 215, 152),
 "matrix": (212, 78, 382, 266),
 "output column": (404, 80, 458, 262),
 "X2 label": (108, 150, 150, 192),
 "WQ label": (168, 198, 222, 242),
 "equals": (378, 158, 408, 192),
 "title": (560, 110, 860, 141),   # narrowed: exclude subtitle bleed rows y>=142
 "subtitle": (540, 143, 870, 178),
 "arrow": (470, 135, 570, 248),
 "net panel": (470, 238, 916, 514),
 "band": (484, 300, 898, 434),
 "out circle row": (500, 248, 895, 310),
 "in circle row": (500, 436, 895, 496),
}
print(f"scale S = {S:.4f}  (render {r.shape[1]}x{r.shape[0]} vs frame {f.shape[1]}x{f.shape[0]})")
for name, (x0, y0, x1, y1) in regs.items():
    fb = ink_bbox(f, x0, y0, x1, y1)
    rb = ink_bbox(r, int(x0 * S), int(y0 * S), int(x1 * S), int(y1 * S))
    cmp(name, fb, rb)

# delimiter geometry: pill [ ] brackets — vertical extent must cover the 4 circles row
print("\n-- pill bracket vs circle-row extent (frame px, from crops/read_c2) --")
for nm, (x0, y0, x1, y1) in {"bracket-left": (70, 100, 86, 152), "bracket-right": (192, 100, 208, 152)}.items():
    fb = ink_bbox(f, x0, y0, x1, y1); rb = ink_bbox(r, int(x0 * S), int(y0 * S), int(x1 * S), int(y1 * S))
    cmp(nm, fb, rb)
circ_fb = ink_bbox(f, 88, 100, 190, 152); circ_rb = ink_bbox(r, int(88 * S), int(100 * S), int(190 * S), int(152 * S))
if circ_fb and circ_rb:
    print(f"circles row  frame y{circ_fb[1]}..{circ_fb[3]} | render/scale y{circ_rb[1]/S:.1f}..{circ_rb[3]/S:.1f}")
