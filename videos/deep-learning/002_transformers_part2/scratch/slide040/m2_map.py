#!/usr/bin/env python3
"""Stage 2: fit mapping + badge cross-check for slide_040."""
# landmarks measured (m1): left 58, right 901, top 43, bottom 517; badge yellow-bbox center (875.5, 71.0)
L, R, T, B = 58, 901, 43, 517          # frame px of chrome border strokes
SL, SR, ST, SB = 42, 919, 45, 540      # slide pt chrome (playlist law)
bx = (R - L) / (SR - SL)
ax = L - bx * SL
by = (B - T) / (SB - ST)
ay = T - by * ST
print(f"x-fit: frame_x = {ax:.5f} + {bx:.5f}*slide_x")
print(f"y-fit: frame_y = {ay:.5f} + {by:.5f}*slide_y")
# certified slides 002/039 mapping for comparison
print(f"certified:  frame_x = 18.63 + 0.96123*slide_x ; frame_y = 0.95556*slide_y")
# badge cross-check: measured frame center -> slide coords through BOTH fits
mx, my = 875.5, 71.0
sx = (mx - ax) / bx; sy = (my - ay) / by
sx2 = (mx - 18.63) / 0.96123; sy2 = my / 0.95556
print(f"badge center -> slide: own-fit ({sx:.1f},{sy:.1f})  certified-fit ({sx2:.1f},{sy2:.1f})  house (893,71)")
# residuals of certified mapping on the 4 landmarks
for name, f, s in [("left", L, SL), ("right", R, SR), ("top", T, ST), ("bottom", B, SB)]:
    pred = 18.63 + 0.96123*s if name in ("left", "right") else 0.95556*s
    print(f"  {name}: frame {f} vs certified-pred {pred:.1f} (res {f-pred:+.1f}px)")
