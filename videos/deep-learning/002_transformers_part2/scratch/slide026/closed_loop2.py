#!/usr/bin/env python3
"""Closed-loop ink check v2: windowed color masks around each expected landmark."""
from PIL import Image
import numpy as np

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide026/render_1.png"
img = Image.open(R).convert("RGB")
a = np.asarray(img).astype(int)
K = 150 / 72.0
MX, SXX, SYY = 18.628, 0.96123, 0.95556
def rp(fx, fy):
    return (fx - MX) / SXX * K, fy / SYY * K

r, g, b = a[..., 0], a[..., 1], a[..., 2]
fails = []

def check(label, fx0, fy0, fx1, fy1, mask_fn, tol=6, pad=25):
    ex0, ey0 = rp(fx0, fy0); ex1, ey1 = rp(fx1, fy1)
    win = np.zeros(a.shape[:2], bool)
    win[max(0, int(ey0 - pad)):int(ey1 + pad), max(0, int(ex0 - pad)):int(ex1 + pad)] = True
    got = None
    m = mask_fn() & win
    ys, xs = np.nonzero(m)
    if len(xs):
        got = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
    if got is None:
        print(f"FAIL {label}: NO INK expect ({ex0:.0f},{ey0:.0f},{ex1:.0f},{ey1:.0f})"); fails.append(label); return
    d = max(abs(got[0]-ex0), abs(got[1]-ey0), abs(got[2]-ex1), abs(got[3]-ey1))
    ok = d <= tol
    print(f"{'OK  ' if ok else 'FAIL'} {label}: got {got} expect ({ex0:.0f},{ey0:.0f},{ex1:.0f},{ey1:.0f}) dmax={d:.0f}")
    if not ok: fails.append(label)

near = lambda c, tol: (abs(r - c[0]) < tol) & (abs(g - c[1]) < tol) & (abs(b - c[2]) < tol)

check("blue_box", 231,239,379,387, lambda: near((14,191,235), 60), 8)
check("container", 404,189,658,466, lambda: near((196,220,160), 14), 12)
check("right_rect_border", 687,187,855,465, lambda: near((30,117,62), 55), 12)
check("host_bar", 395,254,412,385, lambda: near((215,215,215), 12), 12)
check("enc_bar", 649,280,666,373, lambda: near((215,215,215), 12), 12)
check("dual_adc", 472,248,545,279, lambda: near((233,153,104), 40), 10)
check("tri_top", 545,247,577,277, lambda: near((108,206,147), 35), 10)
check("tri_mid", 545,303,577,334, lambda: near((108,206,147), 35), 10)
check("comp_box", 458,350,598,400, lambda: near((236,233,240), 10), 10)
check("power_sup", 462,416,526,456, lambda: near((208,186,111), 30), 10)
check("diff_box", 694,246,831,280, lambda: near((241,211,178), 18), 10)
check("sincos_box", 741,399,799,425, lambda: near((241,211,178), 18), 10)
check("sub1", 233,252,320,284, lambda: near((245,213,188), 14), 8)
check("sub2", 233,306,320,336, lambda: near((214,230,191), 12), 8)
check("pos_arrow", 157,296,224,317, lambda: near((176,0,17), 70), 10)
check("title_ink", 372,59,551,74,
      lambda: ((r - np.maximum(g, b)) > 60) & (r > 130), 8)
check("subtitle_ink", 209,83,719,101,
      lambda: ((b - r) > 60) & (b > 130), 10)
check("caption_L1", 334,481,773,491,
      lambda: ((r - np.maximum(g, b)) > 60) & (r > 130), 10)
check("caption_L2", 435,495,677,505,
      lambda: ((r - np.maximum(g, b)) > 60) & (r > 130), 10)
check("tag_TIDA", 568,191,664,213, lambda: near((255,255,255), 6), 8)
check("whitebox16", 456,220,588,243, lambda: near((255,255,255), 6), 8)
# text micro-bands: ink presence + center check
def textcheck(label, fx0, fy0, fx1, fy1, dark=430):
    ex0, ey0 = rp(fx0, fy0); ex1, ey1 = rp(fx1, fy1)
    win = np.zeros(a.shape[:2], bool)
    win[int(ey0) - 4:int(ey1) + 4, int(ex0) - 4:int(ex1) + 4] = True
    m = ((r + g + b) < dark) & win
    ys, xs = np.nonzero(m)
    if len(xs) < 8:
        print(f"FAIL {label}: NO INK"); fails.append(label); return
    got = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
    d = max(abs(got[0]-ex0), abs(got[1]-ey0), abs(got[2]-ex1), abs(got[3]-ey1))
    print(f"{'OK  ' if d <= 8 else 'FAIL'} {label}: got {got} expect ({ex0:.0f},{ey0:.0f},{ex1:.0f},{ey1:.0f}) dmax={d:.0f} n={len(xs)}")
    if d > 8: fails.append(label)

textcheck("spi_txt", 366,266,392,280)
textcheck("12bitadc_txt", 362,310,394,338)
textcheck("eqep_txt", 364,371,394,386)
textcheck("corridor_top_txt", 414,247,458,276)
textcheck("corridor_mid_txt", 414,300,455,330)
textcheck("corridor_bot_txt", 414,362,456,390)
textcheck("out_top_txt", 588,252,656,268)
textcheck("out_mid_txt", 583,322,658,340)
textcheck("out_R_txt", 592,348,652,362)
textcheck("comparators_txt", 522,382,596,398)
textcheck("24V_txt", 366,426,395,443)
textcheck("5V_txt", 556,428,581,437)
textcheck("33V_txt", 556,444,598,457)
textcheck("encsupply_txt", 598,449,694,462)
textcheck("shielded_txt", 739,321,855,358)
textcheck("ACmotor_txt", 788,398,857,413)
textcheck("diffbox_txt", 700,248,826,278, 470)
textcheck("sincos_txt", 748,401,793,424, 520)
textcheck("tida_txt", 578,194,655,210)
textcheck("wires_ink", 668,300,738,430, 420)
textcheck("poslabel_txt", 141,317,214,345)
textcheck("sub1_txt", 236,255,318,281, 470)
textcheck("sub3_txt", 238,360,316,385, 470)
textcheck("hostmcu_txt", 396,268,411,372, 430)
textcheck("encconn_txt", 650,294,665,370, 430)

print()
print("FAILS:", fails if fails else "NONE")
