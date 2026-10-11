#!/usr/bin/env python3
"""Attempt-2 closed-loop check (render_2.png) — corrected targets/windows.
Fixes vs selfcheck_attempt_1 (all window artifacts diagnosed by PIL probes):
  - vec rows: bottom target 174.8 was wrong (excluded paren descent) -> 183.5
  - callout border: dark mask can't see CC6600 -> orange mask
  - L3 hl2: window overlapped hl3's highlight -> split windows
  - L6: window included panel border (x<=900) -> x<=885; added NO-WRAP assert
  - callout L2: window caught L1 descenders -> rows from 155
  - brackets: separate L/R stroke checks vs measured original ink
  - chevrons: ink-center check at 16.5pt bold
Tolerance ~4px @150dpi = 1.92pt (deltas printed; OK/FIX per edge)."""
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide032/render_2.png').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
print("render size:", W, H)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
S = 150 / 72.0

def bb(mask, x0, y0, x1, y1):
    m = mask[y0:y1, x0:x1]
    ys, xs = np.where(m)
    if not len(ys): return None
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max() + 1, y0 + ys.max() + 1)

def report(name, box, t):
    if box is None:
        print(f"{name:26s} NO INK  (target {t})"); return None
    l, tp, r, b = [v / S for v in box]
    dl, dt, dr, db = l - t[0], tp - t[1], r - t[2], b - t[3]
    ok = max(abs(dl), abs(dt), abs(dr), abs(db)) <= 1.92
    print(f"{name:26s} x {l:7.1f}..{r:7.1f} y {tp:7.1f}..{b:7.1f}  dL{dl:+6.1f} dT{dt:+6.1f} dR{dr:+6.1f} dB{db:+6.1f} {'OK' if ok else 'FIX'}")
    return (dl, dt, dr, db)

red = (R - G > 60) & (R - B > 60) & (R > 120)
navy = (R < 110) & (G < 110) & (B > 100)
dark = (R < 130) & (G < 130) & (B < 130)
blue = (R < 120) & (G < 120) & (B > 120)
yellow = (R > 200) & (G > 200) & (B < 120)
green = (G - R > 50) & (G - B > 50) & (G > 110)
orange = (np.abs(R - 204) < 45) & (np.abs(G - 102) < 45) & (B < 80)
gray = (np.abs(R - G) < 25) & (np.abs(G - B) < 25) & (R > 90) & (R < 190)

X = lambda v: int(v * S); Y = lambda v: int(v * S)
print("== chrome-adjacent content ==")
report("title", bb(red, X(250), Y(50), X(720), Y(85)), (330.2, 61.7, 618.3, 78.5))
report("subtitle", bb(blue, X(200), Y(80), X(760), Y(107)), (254.2, 86.9, 699.6, 103.6))
report("vecbox border", bb(navy, X(60), Y(95), X(205), Y(212)), (70.1, 102.6, 192.3, 205.7))
report("bracket L stroke", bb(red, X(78), Y(112), X(93), Y(194)), (81.5, 118.3, 90.9, 190.5))
report("bracket R stroke", bb(red, X(160), Y(112), X(176), Y(194)), (165.8, 118.3, 173.1, 190.5))
report("vec rows (red text)", bb(red, X(93), Y(122), X(159), Y(193)), (95.1, 128.7, 157.5, 183.5))
report("callout border", bb(orange, X(200), Y(115), X(880), Y(185)), (207.9, 123.5, 868.2, 180.0))
report("panel border", bb(navy, X(50), Y(210), X(900), Y(535)), (57.6, 217.7, 893.9, 531.3))
print("== panel lines ==")
report("L1 (blue italic)", bb(blue, X(60), Y(230), X(860), Y(262)), (69.3, 237.6, 810.9, 255.3))
report("L2 (incl hl+green)", bb(blue | yellow | green, X(80), Y(298), X(560), Y(330)), (87.8, 305.6, 520.6, 323.4))
report("L2 highlight", bb(yellow, X(150), Y(298), X(365), Y(330)), (192.8, 305.0, 349.9, 324.0))
report("L3 (incl hl)", bb(blue | yellow, X(80), Y(332), X(830), Y(363)), (86.9, 339.1, 795.2, 356.9))
report("L3 hl2 ('t and t+1')", bb(yellow, X(540), Y(332), X(690), Y(363)), (558.0, 339.0, 679.7, 357.0))
report("L3 hl3 (constant)", bb(yellow, X(695), Y(332), X(830), Y(363)), (714.1, 339.0, 795.2, 357.0))
report("L4 (incl green)", bb(blue | green, X(80), Y(366), X(790), Y(397)), (86.9, 372.6, 739.0, 390.4))
report("L5 (incl hl+green)", bb(blue | yellow | green, X(80), Y(400), X(790), Y(432)), (87.8, 406.0, 739.0, 423.8))
report("L5 highlight", bb(yellow, X(80), Y(400), X(450), Y(432)), (87.8, 406.0, 380.1, 424.9))
print("== L6 (wrap-fixed; window x<=885 excludes panel border) ==")
report("L6 full (blue+red)", bb(blue | red, X(80), Y(468), X(885), Y(497)), (86.9, 473.0, 871.1, 492.0))
report("L6 red seg", bb(red, X(300), Y(468), X(885), Y(497)), (349.9, 473.0, 871.1, 491.9))
wrap = (blue | red)[Y(497):Y(515), X(84):X(885)]
print(f"L6 NO-WRAP assert (ink px in y 497..515): {int(wrap.sum())}  {'OK' if wrap.sum() < 40 else 'FIX (still wrapping)'}")
print("== chevrons (16.5pt bold; ink-center vs original) ==")
for nm, (y0, y1), cy in [("chev L2", (303, 322), 311.85), ("chev L5", (404, 423), 412.35), ("chev L6", (472, 491), 480.35)]:
    b = bb(gray, X(64), Y(y0), X(80), Y(y1))
    if b is None: print(f"{nm}: NO INK"); continue
    l, t, r, bt = [v / S for v in b]
    print(f"{nm}: ink x {l:.1f}..{r:.1f} y {t:.1f}..{bt:.1f} center ({(l+r)/2:.1f},{(t+bt)/2:.1f}) w {r-l:.1f} h {bt-t:.1f}"
          f"  dcx {(l+r)/2-70.6:+.1f} dcy {(t+bt)/2-cy:+.1f}  {'OK' if abs((l+r)/2-70.6)<=2 and abs((t+bt)/2-cy)<=2 else 'FIX'}")
print("== callout text ==")
report("callout L1", bb(dark, X(210), Y(128), X(860), Y(154)), (216.8, 134.0, 833.7, 150.7))
report("callout L2", bb(dark, X(210), Y(155), X(520), Y(176)), (216.8, 156.0, 397.8, 169.6))
