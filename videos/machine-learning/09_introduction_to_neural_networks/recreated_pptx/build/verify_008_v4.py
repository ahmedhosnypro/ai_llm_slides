#!/usr/bin/env python3
import sys
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
A = np.asarray(Image.open(V + "/recreated_pptx/build/slide_008_rendered-1.png").convert("RGB")).astype(int)
S = A.shape[1] / 960.0
TOL = 4
results = []


def check(name, ok, detail):
    results.append((name, bool(ok)))
    print("%-4s %-34s %s" % ("PASS" if ok else "FAIL", name, detail))


def win(x0, y0, x1, y1):
    return (slice(int((y0 - TOL) * S), int((y1 + TOL) * S) + 1),
            slice(int((x0 - TOL) * S), int((x1 + TOL) * S) + 1))


def count(name, box, pred, minimum):
    sub = A[win(*box)]
    n = int(pred(sub).sum())
    check(name, n >= minimum, "%d px >= %d" % (n, minimum))


is_red = lambda sub: (sub[..., 0] > 120) & (sub[..., 0] - sub[..., 1] > 60) & (sub[..., 0] - sub[..., 2] > 60)
is_blue = lambda sub: (sub[..., 2] > 170) & (sub[..., 2] - sub[..., 0] > 60) & (sub[..., 2] - sub[..., 1] > 40)
is_green = lambda sub: (sub[..., 1] > 140) & (sub[..., 1] - sub[..., 0] > 40) & (sub[..., 1] - sub[..., 2] > 40)
is_magenta = lambda sub: (sub[..., 0] > 200) & (sub[..., 2] > 200) & (sub[..., 1] < 100)
is_yellow = lambda sub: (sub[..., 0] > 230) & (sub[..., 1] > 230) & (sub[..., 2] < 120)
is_salmon = lambda sub: (sub[..., 0] > 240) & (sub[..., 1] > 195) & (sub[..., 1] < 240) & (sub[..., 2] > 185) & (sub[..., 2] < 228)
is_orange = lambda sub: (sub[..., 0] > 230) & (sub[..., 1] > 30) & (sub[..., 1] < 130) & (sub[..., 2] < 80)
is_black = lambda sub: (sub[..., 0] < 70) & (sub[..., 1] < 70) & (sub[..., 2] < 70)

check("render dimensions", A.shape == (1125, 2001, 3), str(A.shape))
bg = A[int(25 * S), int(550 * S)]
check("background E8E8E8", max(abs(bg - 232)) <= 8, str(tuple(bg)))
fr = A[int(300 * S), int(0.15 * 150)]
check("house red frame", fr[0] > 140 and fr[0] - fr[1] > 50, str(tuple(fr)))
ov = A[int(0.75 * 150), int(12.73 * 150)]
check("badge FFF9C4", abs(ov[0] - 255) <= 10 and abs(ov[1] - 249) <= 10 and abs(ov[2] - 196) <= 12, str(tuple(ov)))
check("badge numeral", int(is_black(A[int(0.30 * 150):int(0.80 * 150), int(12.48 * 150):int(12.98 * 150)]).sum()) >= 20, "black px")

title = A[int(20 * S):int(110 * S), :]
check("title red", int(is_red(title).sum()) >= 100, "%d red px" % int(is_red(title).sum()))
check("title blue", int(is_blue(title).sum()) >= 30, "%d blue px" % int(is_blue(title).sum()))

count("d1 red label", (250, 178, 295, 211), is_red, 20)
count("d2 blue label", (555, 138, 597, 170), is_blue, 20)
count("d3 green label", (700, 198, 750, 227), is_green, 20)
count("C1 yellow", (525, 153, 568, 188), is_yellow, 300)
count("C2 yellow", (594, 295, 637, 330), is_yellow, 300)
count("C3 yellow", (260, 395, 303, 430), is_yellow, 300)
count("q1 salmon", (434, 318, 478, 354), is_salmon, 300)
count("q2 salmon", (591, 177, 633, 210), is_salmon, 300)
count("q3 salmon", (243, 264, 283, 297), is_salmon, 300)
count("q4 salmon", (422, 418, 462, 452), is_salmon, 300)
count("q1 orange glyph", (434, 318, 478, 354), is_orange, 10)
count("q2 orange glyph", (591, 177, 633, 210), is_orange, 10)
count("q3 orange glyph", (243, 264, 283, 297), is_orange, 10)
count("q4 orange glyph", (422, 418, 462, 452), is_orange, 10)
count("+ve 1", (638, 131, 673, 147), is_black, 15)
count("+ve 2", (251, 312, 289, 328), is_black, 15)
count("+ve 3", (494, 448, 531, 464), is_black, 15)
count("Undefined blue", (73, 131, 148, 161), is_blue, 30)
count("New Class magenta", (715, 372, 787, 396), is_magenta, 25)

m = is_magenta(A[win(470, 300, 505, 330)])
ys, xs = np.where(m)
if len(xs):
    got = (xs.min() / S + 470, ys.min() / S + 300, xs.max() / S + 470, ys.max() / S + 300)
    ok = abs(got[0] - 484) <= TOL and abs(got[1] - 312) <= TOL and abs(got[2] - 491) <= TOL and abs(got[3] - 318) <= TOL
    check("tiny magenta ? bbox", ok, "got x%.1f-%.1f y%.1f-%.1f n=%d" % (*got, len(xs)))
else:
    check("tiny magenta ? bbox", False, "no magenta ink")

pan = A[win(167, 120, 798, 505)]
check("graph panel present", float(pan.std()) > 8, "std %.2f" % float(pan.std()))

bad = [n for n, ok in results if not ok]
print("\n%d checks, %d failed" % (len(results), len(bad)))
if bad:
    print("FAILED: " + ", ".join(bad))
    sys.exit(1)
print("ALL CHECKS PASSED")
