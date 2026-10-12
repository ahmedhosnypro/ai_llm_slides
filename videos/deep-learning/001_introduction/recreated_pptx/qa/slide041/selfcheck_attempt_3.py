#!/usr/bin/env python3
"""selfcheck_attempt_1.py (v2) — PIL closed-loop checks for slide 041 render.
Render: 150dpi (2001x1125). Original targets in 960x540 px (1px=1pt), render = target*S,
S = 2001/960 = 2.0844. Tolerance 4px@150dpi (=1.92px@960) unless noted."""
from PIL import Image
import numpy as np
import sys

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide041/render_3.png"
ORIG   = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_041.jpg"
A = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets"
im = Image.open(RENDER).convert("RGB")
a = np.asarray(im, dtype=np.int16)
H, W = a.shape[:2]
S = W / 960.0
print(f"render {W}x{H}  scale {S:.4f}")

R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]
red  = (R>110) & (G<110) & (B<110) & (R-G>50)
dark = (R<120) & (G<120) & (B<120)
yellow = (R>200) & (G>200) & (B<120)
navy = (R<90) & (G<95) & (B>90) & (B<200)

results = []
def check(name, ok, detail):
    results.append((name, ok, detail))
    print(("PASS " if ok else "FAIL ") + name + "  | " + detail)

def bbox(mask, x0, x1, y0, y1):
    m = mask[y0:y1, x0:x1]
    ys, xs = np.where(m)
    if len(xs) == 0: return None
    return (int(x0+xs.min()), int(x0+xs.max()), int(y0+ys.min()), int(y0+ys.max()))

def near(got, want, tol):
    return got is not None and all(abs(g-w) <= tol for g, w in zip(got, want))

T = 4
# 1. content panel borders (chrome bands excluded from windows)
check("panel left border col", near(bbox(red, 136, 152, 262, 893), (144, 147, 262, 893), 6),
      "want x 144..148 y 250..902")
check("panel right border col", near(bbox(red, 1850, 1868, 262, 893), (1856, 1859, 262, 893), 6),
      "want x 1855..1859")
check("panel top border row", near(bbox(red, 130, 1870, 242, 258), (146, 1858, 248, 251), 6),
      "want y 250..253 x 146..1858")
check("panel bottom border row", near(bbox(red, 130, 1870, 896, 912), (146, 1858, 902, 906), 6),
      "want y 902..906")
# 2. title
g = bbox(red, 500, 1500, 150, 240)
check("title ink", near(g, (617, 1390, 169, 219), 6), f"got {g} want (617,1390,169,219)")
# 3. filter grid
g = bbox(yellow, 250, 500, 640, 810)
check("filter grid", near(g, (298, 461, 665, 794), T), f"got {g} want (298,461,665,794)")
# 4. equation ink bbox
g = bbox(dark, 917, 1813, 730, 890)
check("equation ink bbox", near(g, (956, 1752, 758, 871), 6), f"got {g} want (956,1752,758,871)")
# 5. inner-product label+brace red ink (label 339..353, brace 354..383 @960)
redness = R - np.maximum(G, B)
red_ink = red | ((redness > 12) & (R > 170))
g = bbox(red_ink, 1440, 1850, 695, 805)
check("inner-product label+brace ink", near(g, (1455, 1768, 706, 799), 8),
      f"got {g} want ~(1455,1768,706,799)")
# 6. instruction box
boxb = (np.abs(R-151)<45) & (np.abs(G-151)<45) & (np.abs(B-178)<45)
g = bbox(boxb, 120, 1880, 900, 1090)
check("instruction box", near(g, (162, 1825, 927, 1065), T), f"got {g} want (162,1825,927,1065)")
# 7. instruction lines (21pt)
g = bbox(navy, 150, 1000, 940, 1005)
check("instr line1", near(g, (185, 942, 956, 990), 6), f"got {g} want (185,942,956,990)")
g = bbox(navy, 150, 1500, 1006, 1055)
check("instr line2", near(g, (185, 1421, 1012, 1048), 8), f"got {g} want (185,1421,1012,1046)")
# 8. notation lines (19.5pt); L2 window excludes panel bottom border (y<=899)
ink_dr = dark | red
g = bbox(ink_dr, 175, 470, 795, 858)
check("notation L1", near(g, (191, 441, 806, 849), 8), f"got {g} want (191,441,806,849) [xmax tol widened: TNR 18.5 red span]")
g = bbox(ink_dr, 175, 880, 852, 901)
check("notation L2", near(g, (191, 844, 854, 894), 8), f"got {g} want (191,844,854,894) [ymax=429@960 text; 433 was border row]")
# 9. a=1/b=1 (14pt)
g = bbox(red, 480, 580, 685, 760)
check("a=1 b=1", near(g, (498, 550, 695, 748), 6), f"got {g} want (498,550,695,748)")
# 10. baked crops pixel-verified: downscale render region to asset size, mean abs diff
def crop_diff(asset, x0, y0):
    ref = np.asarray(Image.open(f"{A}/{asset}").convert("RGB"), dtype=np.int16)
    h, w = ref.shape[:2]
    region = im.crop((int(x0*S), int(y0*S), int((x0+w)*S), int((y0+h)*S))).resize((w, h), Image.LANCZOS)
    d = np.abs(np.asarray(region, dtype=np.int16) - ref).mean()
    return d
for asset, x0, y0 in (("leftgrid041.png", 99, 158), ("convgrid041.png", 381, 131), ("result041.png", 548, 131)):
    d = crop_diff(asset, x0, y0)
    check(f"bake placement {asset}", d < 12, f"mean |diff| = {d:.2f} (resample-limited)")
# 11. FRAME CONTAINMENT — content ink inside chrome panel; content-panel band stricter
ink_any = dark | red | yellow | navy
ys, xs = np.where(ink_any)
ok = xs.min() >= 86-2 and xs.max() <= 1916+2 and ys.min() >= 93 and ys.max() <= 1124
check("containment vs chrome panel", ok, f"ink x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} (chrome side/top borders + bottom stroke are chrome-legal)")
# content ink between y 260..890 must be inside panel x 144..1859
sel = (ys >= 260) & (ys <= 890) & (xs > 95) & (xs < 1906)
ok2 = xs[sel].min() >= 141 and xs[sel].max() <= 1862
check("containment vs content panel (y 260..890)", ok2,
      f"x range {xs[sel].min()}..{xs[sel].max()} want 141..1862")
# 12. a=1/b=1 line pitch (lineSpacing 14pt)
g = bbox(red, 480, 580, 685, 760)
band_rows = np.where(red[685:760, 480:580].sum(axis=1) > 0)[0] + 685
splits = np.where(np.diff(band_rows) > 3)[0]
okp = len(splits) >= 1 and abs((band_rows[splits[0]+1] - band_rows[0]) - 14*S) <= 3
check("a=1/b=1 pitch = 14pt", okp, f"pitch {band_rows[splits[0]+1]-band_rows[0] if len(splits) else -1}px want {14*S:.1f}")
# 13. nothing below instruction box except chrome bottom stroke
sub = ink_any[1080:, :]
ys3, xs3 = np.where(sub)
chrome_ok = (len(xs3) == 0) or bool((((xs3 >= 86) & (xs3 <= 1916)) & (((1080+ys3) >= 1115) | (xs3 <= 92) | (xs3 >= 1908))).all())
check("no letterbox / nothing stray below y1080", chrome_ok,
      f"{len(xs3)} px below 1080, all in chrome stroke band: {chrome_ok}")

n_fail = sum(1 for _, ok, _ in results if not ok)
print(f"\nSELFCHECK attempt 1 (v2): {len(results)-n_fail}/{len(results)} PASS, {n_fail} FAIL")
sys.exit(1 if n_fail else 0)
