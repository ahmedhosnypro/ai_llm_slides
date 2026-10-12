#!/usr/bin/env python3
"""Final disambiguation: underline continuity bins (low threshold), L5 tail boldness
excluding underline rows, 023 box border census."""
import numpy as np
from PIL import Image
from fontTools.ttLib import TTFont

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
img24 = np.asarray(Image.open(f"{V}/unique_slides/slide_024.jpg").convert("RGB")).astype(int)
img23 = np.asarray(Image.open(f"{V}/unique_slides/slide_023.jpg").convert("RGB")).astype(int)

sx = (899 - 58) / (919.0 - 42.0); a = 58 - sx * 42.0
def Sx(fx): return (fx - a) / sx
def Fx(sv): return a + sx * sv

def underline_bins(img, y_lo, y_hi, x_lo, x_hi, tag):
    reg = img[y_lo:y_hi, x_lo:x_hi]
    r, g, b = reg[..., 0], reg[..., 1], reg[..., 2]
    blue = (b > 80) & (b > r + 15)
    print(f"{tag} (bins of 4pt from slide {Sx(x_lo):.0f}):")
    out = []
    for sv in range(int(Sx(x_lo)), int(Sx(x_hi)), 4):
        f0, f1 = Fx(sv), Fx(sv + 4)
        c0, c1 = int(f0) - x_lo, int(f1) - x_lo
        n = int(blue[:, max(c0,0):max(c1,0)].sum())
        out.append(f"{sv}:{n}")
    print("   " + " ".join(out))

# L5 underline rows 466..469 (baseline 465.3, underline ~467-469)
underline_bins(img24, 465, 470, 580, 910, "L5 underline rows 465-469")
# L2 underline rows 400..404 (baseline 400.8)
underline_bins(img24, 400, 405, 90, 500, "L2 underline rows 400-404")
# control: L3 same rows relative to its baseline (~442.5 -> frame 423): rows 423..428
underline_bins(img24, 423, 429, 380, 740, "L3 control rows 423-428")

# L5 tail boldness EXCLUDING underline rows: words at slide 594.7..898 -> frame 587..878
reg = img24[453:465, 587:880]  # rows above baseline (cap top ~454 to 464)
r, g, b = reg[..., 0], reg[..., 1], reg[..., 2]
blue = (b > 100) & (b > r + 30)
print("\nL5 tail 'same dimension as Word Embedding' coverage rows 453-464 (no underline):",
      round(float(blue.sum()) / blue.size, 3))
# compare: L5 '(not scalar) and of' slide 445.6..589.5 -> frame 445..583
reg2 = img24[453:465, 445:584]
r2, g2, b2 = reg2[..., 0], reg2[..., 1], reg2[..., 2]
blue2 = (b2 > 100) & (b2 > r2 + 30)
print("L5 '(not scalar) and of' coverage rows 453-464:", round(float(blue2.sum()) / blue2.size, 3))
# L3 blue 'should NOT depend on' slide 388..582 -> frame 390..577, rows 410..422
reg3 = img24[410:423, 390:578]
r3, g3, b3 = reg3[..., 0], reg3[..., 1], reg3[..., 2]
blue3 = (b3 > 100) & (b3 > r3 + 30)
print("L3 'should NOT depend on' coverage rows 410-422:", round(float(blue3.sum()) / blue3.size, 3))
# L1 regular 'for Long sequence...' slide 305..612 -> frame 311..605, rows 365..378
reg4 = img24[365:379, 311:606]
r4, g4, b4 = reg4[..., 0], reg4[..., 1], reg4[..., 2]
blue4 = (b4 > 100) & (b4 > r4 + 30)
print("L1 'for Long sequence and short sequence' coverage rows 365-378:", round(float(blue4.sum()) / blue4.size, 3))
# L1 bold 'should be same' slide 167..300 -> frame 178..305
reg5 = img24[365:379, 178:306]
r5, g5, b5 = reg5[..., 0], reg5[..., 1], reg5[..., 2]
blue5 = (b5 > 100) & (b5 > r5 + 30)
print("L1 'should be same' coverage rows 365-378:", round(float(blue5.sum()) / blue5.size, 3))
# L2 regular reference: slide 229..586 -> frame 237..580, rows 388..400
reg6 = img24[388:401, 237:581]
r6, g6, b6 = reg6[..., 0], reg6[..., 1], reg6[..., 2]
blue6 = (b6 > 100) & (b6 > r6 + 30)
print("L2 'will be encoded with same values irrespective' coverage rows 388-400:", round(float(blue6.sum()) / blue6.size, 3))

# 023 box border census (bottom border): find the blue border row near frame 502 in frame23
reg7 = img23[495:512, 150:800]
r7, g7, b7 = reg7[..., 0], reg7[..., 1], reg7[..., 2]
bl7 = (b7 > 90) & (b7 > r7 + 30)
for yy in range(reg7.shape[0]):
    n = int(bl7[yy].sum())
    if n > 100:
        px = reg7[yy][bl7[yy]]
        print(f"\n023 bottom border row {495+yy}: n={n} mean {px.mean(axis=0).round(1)}")
reg8 = img23[344:356, 150:800]
r8, g8, b8 = reg8[..., 0], reg8[..., 1], reg8[..., 2]
bl8 = (b8 > 90) & (b8 > r8 + 30)
for yy in range(reg8.shape[0]):
    n = int(bl8[yy].sum())
    if n > 100:
        px = reg8[yy][bl8[yy]]
        print(f"023 top border row {344+yy}: n={n} mean {px.mean(axis=0).round(1)}")
# 024 box borders same method
reg9 = img24[495:512, 150:800]
r9, g9, b9 = reg9[..., 0], reg9[..., 1], reg9[..., 2]
bl9 = (b9 > 90) & (b9 > r9 + 30)
for yy in range(reg9.shape[0]):
    n = int(bl9[yy].sum())
    if n > 100:
        px = reg9[yy][bl9[yy]]
        print(f"024 bottom border row {495+yy}: n={n} mean {px.mean(axis=0).round(1)}")
reg10 = img24[344:356, 150:800]
r10, g10, b10 = reg10[..., 0], reg10[..., 1], reg10[..., 2]
bl10 = (b10 > 90) & (b10 > r10 + 30)
for yy in range(reg10.shape[0]):
    n = int(bl10[yy].sum())
    if n > 100:
        px = reg10[yy][bl10[yy]]
        print(f"024 top border row {344+yy}: n={n} mean {px.mean(axis=0).round(1)}")
