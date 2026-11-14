#!/usr/bin/env python3
"""PIL self-check for slide 036: render_8.png vs unique_slides/slide_036.jpg (both 960x540)."""
import sys
from PIL import Image
import numpy as np

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
R = np.asarray(Image.open(f"{NS}/recreated_pptx/qa/slide036/render_8.png").convert("RGB").resize((960, 540), Image.LANCZOS)).astype(int)
O = np.asarray(Image.open(f"{NS}/unique_slides/slide_036.jpg").convert("RGB").resize((960, 540), Image.LANCZOS)).astype(int)
H, W = R.shape[:2]
print("render_size", (W, H), "orig_size", O.shape[:2])
results = []

def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(("PASS" if ok else "FAIL"), name, detail)

def is_red(p):   # dark red ~ (139,0,0)/(192,0,0)
    return (p[..., 0] > 90) & (p[..., 0] < 220) & (p[..., 1] < 70) & (p[..., 2] < 70)

def is_navy(p):
    return (p[..., 2] > 110) & (p[..., 0] < 90) & (p[..., 1] < 90)

def is_yellow(p):
    return (p[..., 0] > 230) & (p[..., 1] > 230) & (p[..., 2] < 220)

def is_purple(p):
    return (p[..., 0] > 90) & (p[..., 2] > 90) & (p[..., 1] < 90)

def is_blue(p):
    return (p[..., 2] > 90) & (p[..., 0] < 90) & (p[..., 1] < 130)

def is_green(p):
    return (p[..., 1] > 150) & (p[..., 0] < 180) & (p[..., 2] < 120)

def frac(mask, x0, y0, x1, y1):
    return mask[y0:y1, x0:x1].mean()

# house red frame at 0.15in -> px: 0.15/13.33*W, 0.15/7.5*H
fx, fy = 0.15 / 13.33 * W, 0.15 / 7.5 * H
fw, fh = 13.03 / 13.33 * W, 7.2 / 7.5 * H
red = is_red(R)
top = frac(red, int(fx), int(fy) - 2, int(fx + fw), int(fy) + 3)
bot = frac(red, int(fx), int(fy + fh) - 2, int(fx + fw), int(fy + fh) + 3)
lef = frac(red, int(fx) - 2, int(fy), int(fx) + 3, int(fy + fh))
rig = frac(red, int(fx + fw) - 2, int(fy), int(fx + fw) + 3, int(fy + fh))
check("house_red_frame", min(top, bot, lef, rig) > 0.3, f"top/bot/left/right={top:.2f}/{bot:.2f}/{lef:.2f}/{rig:.2f}")

# badge yellow oval x12.48..12.98in y0.30..0.80in
bx0, bx1 = int(12.48 / 13.33 * W), int(12.98 / 13.33 * W)
by0, by1 = int(0.30 / 7.5 * H), int(0.80 / 7.5 * H)
yel = is_yellow(R)
bbox = np.argwhere(yel[by0 - 5:by1 + 5, bx0 - 5:bx1 + 5])
if len(bbox):
    ys, xs = bbox[:, 0], bbox[:, 1]
    check("badge_yellow_bbox", True, f"bbox x[{bx0-5+xs.min()},{bx0-5+xs.max()}] y[{by0-5+ys.min()},{by0-5+ys.max()}] n={len(bbox)}")
    dark = (R[..., 0] < 90) & (R[..., 1] < 90) & (R[..., 2] < 90)
    sub = dark[by0:by1, bx0:bx1]
    check("badge_dark_numeral", sub.sum() > 40, f"n={sub.sum()}")
else:
    check("badge_yellow_bbox", False, "no yellow")

# outside house frame background ~ #E8E8E8
bg = R[: int(fy) - 3, : int(fx) - 3]
check("outside_house_frame_background", np.abs(bg - 232).mean() < 12, f"mean={bg.mean(axis=(0,1)).round(1)}")

# content frame dark red x[58,901] y[43,517] (960x540 scale)
cf = is_red(R)
c_top = frac(cf, 58, 41, 901, 46); c_bot = frac(cf, 58, 515, 901, 520)
c_lef = frac(cf, 56, 43, 61, 517); c_rig = frac(cf, 899, 43, 904, 517)
check("content_frame_darkred", min(c_top, c_bot, c_lef, c_rig) > 0.3, f"{c_top:.2f}/{c_bot:.2f}/{c_lef:.2f}/{c_rig:.2f}")

check("divider_x635", frac(cf, 633, 43, 638, 517) > 0.5, f"{frac(cf,633,43,638,517):.2f}")
navy = is_navy(R)
check("navy_x344", frac(navy, 342, 43, 347, 517) > 0.5, f"{frac(navy,342,43,347,517):.2f}")
check("navy_y163_287_401", all(frac(navy, 58, y - 2, 635, y + 3) > 0.5 for y in (163, 287, 401)),
      "/".join(f"{frac(navy,58,y-2,635,y+3):.2f}" for y in (163, 287, 401)))

# ROC panel fill near-white greenish #EEFEFB in x[642,900] y[50,406]
panel = R[60:400, 650:895]
check("roc_panel_fill", np.abs(panel - np.array([238, 254, 251])).mean() < 12, f"dominant={np.median(panel.reshape(-1,3),axis=0).round(0)} frac={np.mean(np.abs(panel-np.array([238,254,251])).sum(axis=2)<30):.3f}")
check("roc_panel_navy_border", frac(navy, 640, 48, 902, 53) > 0.3 and frac(navy, 640, 403, 902, 408) > 0.3 and frac(navy, 640, 50, 645, 406) > 0.3 and frac(navy, 897, 50, 902, 406) > 0.3,
      f"{frac(navy,640,48,902,53):.2f}/{frac(navy,640,403,902,408):.2f}/{frac(navy,640,50,645,406):.2f}/{frac(navy,897,50,902,406):.2f}")
pur = is_purple(R)
check("purple_roc_curve", pur[43:407, 636:901].sum() > 300, f"n={pur[43:407,636:901].sum()}")

# no numeric tick labels on ROC axes: compare ink in tick zones vs original
def ink_zone(img, x0, y0, x1, y1):
    z = img[y0:y1, x0:x1]
    return ((z.sum(axis=2) < 300)).sum()
# left of y-axis x[640,664] y[50,406] and below x-axis y[370,407] x[664,895]
check("no_numeric_x_ticks", ink_zone(R, 664, 372, 895, 406) < 40, f"render={ink_zone(R,664,372,895,406)} orig={ink_zone(O,664,372,895,406)}")
check("no_numeric_y_ticks", ink_zone(R, 640, 50, 663, 369) < 40, f"render={ink_zone(R,640,50,663,369)} orig={ink_zone(O,640,50,663,369)}")

# TPR dark red / FPR blue in each of 7 panels (formula text right of each matrix)
panels = [(224, 95, 344, 119), (224, 215, 344, 239), (224, 339, 344, 363), (224, 453, 344, 477),
          (569, 95, 689, 119), (569, 215, 689, 239), (569, 339, 689, 363)]
tpr_ok = all(frac(is_red(R), x0, y0, x1, y1) > 0.01 for x0, y0, x1, y1 in panels)
fpr_ok = all(frac(is_blue(R), x0, y0 + 33, x1, y1 + 33) > 0.01 for x0, y0, x1, y1 in panels)
check("tpr_darkred_all_panels", tpr_ok, str([round(frac(is_red(R), *p), 3) for p in panels]))
check("fpr_blue_all_panels", fpr_ok, str([round(frac(is_blue(R), p[0], p[1] + 33, p[2], p[3] + 33), 3) for p in panels]))

# eq boxes white fill + red border at x[650,748] y[416,455] and y[466,503]
for i, (y0, y1) in enumerate([(416, 455), (466, 503)]):
    box = R[y0 + 4:y1 - 4, 654:744]
    white = np.mean(np.all(box > 235, axis=2))
    border = frac(is_red(R), 648, y0, 750, y1)
    check(f"eq{i+1}_white_box_red_border", white > 0.5 and border > 0.2, f"white={white:.2f} border={border:.2f}")

# legend grid x[748,889] y[407,499]: red lines present
lg = frac(is_red(R), 748, 405, 889, 501)
check("legend_grid", lg > 0.05, f"{lg:.2f}")
# legend cells: TP (lc1,lr2) green, TN (lc2,lr3) green, FN (lc2,lr2) red, FP (lc1,lr3) red
lc = [748, 774, 831, 889]; lr = [407, 432, 455, 477, 499]
def cellmean(x0, x1, y0, y1):
    return R[y0 + 3:y1 - 3, x0 + 3:x1 - 3].reshape(-1, 3).mean(axis=0).round(1)
check("legend_TP_green", is_green(R[lr[2]+3:lr[3]-3, lc[1]+3:lc[2]-3]).mean() > 0.3, f"mean={cellmean(lc[1],lc[2],lr[2],lr[3])}")
check("legend_TN_green", is_green(R[lr[3]+3:lr[4]-3, lc[2]+3:lc[3]-3]).mean() > 0.3, f"mean={cellmean(lc[2],lc[3],lr[3],lr[4])}")
check("legend_FN_red", is_red(R[lr[2]+3:lr[3]-3, lc[2]+3:lc[3]-3]).mean() > 0.3, f"mean={cellmean(lc[2],lc[3],lr[2],lr[3])}")
check("legend_FP_red", is_red(R[lr[3]+3:lr[4]-3, lc[1]+3:lc[2]-3]).mean() > 0.3, f"mean={cellmean(lc[1],lc[2],lr[3],lr[4])}")

# title two dark red lines in box x[344,635] y[426,476]
tb = is_red(R[426:476, 344:635])
rows = np.where(tb.any(axis=1))[0]
bands = []
if len(rows):
    s = rows[0]; p = rows[0]
    for r in rows[1:]:
        if r > p + 3:
            bands.append((s + 426, p + 426)); s = r
        p = r
    bands.append((s + 426, p + 426))
check("title_two_darkred_lines", len(bands) == 2, f"bands={bands}")

# verbatim strings in pptx
import zipfile, re
z = zipfile.ZipFile(f"{NS}/recreated_pptx/slide_036_recreated.pptx")
xml = z.read("ppt/slides/slide1.xml").decode("utf8")
texts = re.findall(r"<a:t>([^<]*)</a:t>", xml)
joined = "|".join(texts)
need = ["36", "Threshold=0.0", "Threshold=0.1", "Threshold=0.3", "Threshold=0.4", "Threshold=0.6",
        "Threshold=0.7", "Threshold=1", "Predicted as", "Actual", "ROC Curve for",
        "Same Model -different thresholds", "TPR=5/(5+0)=1", "FPR=6/(6+0)=1", "FPR=4/(4+2)=0.66",
        "FPR=2/(2+4)=0.33", "FPR=1/(1+5)=0.16", "TPR=3/(3+1)=0.6", "TPR=3/(3+2)=0.6",
        "FPR=0/(0+6)=0", "TPR=0/(0+5)=0", "TPR=4/(4+1)=4/5", "1.0", "TP", "TN", "FP", "FN", "P", "N"]
missing = [n for n in need if n not in joined]
check("pptx_verbatim_strings_and_badge", not missing, f"missing={missing}")

npass = sum(1 for _, ok, _ in results if ok)
print(f"SUMMARY {'PASS' if npass == len(results) else 'FAIL'} {npass}/{len(results)}")
sys.exit(0 if npass == len(results) else 1)
