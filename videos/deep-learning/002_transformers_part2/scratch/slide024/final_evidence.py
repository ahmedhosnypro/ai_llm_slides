#!/usr/bin/env python3
"""Final evidence: L5 middle underline ASCII, 023-frame color census (text ink,
border, subtitle), font width checks."""
import numpy as np
from PIL import Image
from fontTools.ttLib import TTFont

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
img24 = np.asarray(Image.open(f"{V}/unique_slides/slide_024.jpg").convert("RGB")).astype(int)
img23 = np.asarray(Image.open(f"{V}/unique_slides/slide_023.jpg").convert("RGB")).astype(int)

# --- L5 middle underline ASCII (frame x 705..835, y 460..474) ---
print("--- L5 middle zone (frame y 460..474, x 705..835) ---")
reg = img24[460:475, 705:835]
r, g, b = reg[..., 0], reg[..., 1], reg[..., 2]
blue = (b > 90) & (b > r + 25)
for yy in range(reg.shape[0]):
    line = "".join("#" if blue[yy, xx] else "." for xx in range(reg.shape[1]))
    print(f"{460+yy:3d} {line}")

sx = (899 - 58) / (919.0 - 42.0); a = 58 - sx * 42.0
sy = (516 - 43) / (540.0 - 45.0); b0 = 43 - sy * 45.0
print("slide x of frame 705..835:", round((705 - a) / sx, 1), "..", round((835 - a) / sx, 1))

# --- 023 frame census: box text ink (its cyan box text is certified 0000CC) ---
print("\n--- frame23 color census ---")
# 023 box texts: y 377..516 slide -> frame fy = 0.956566*sy - 0.045 (023 mapping) -> 360..493
reg23 = img23[365:490, 100:900]
r2, g2, b2 = reg23[..., 0], reg23[..., 1], reg23[..., 2]
blue23 = (b2 > 100) & (b2 > r2 + 40)
bpix = reg23[blue23]
print("023 box text blue darkest-30% mean:", bpix[bpix[:, 2] < np.percentile(bpix[:, 2], 30)].mean(axis=0).round(1), "n=", len(bpix))
# 023 box border: bottom border row? scan for blue rows with long runs
rowcount = blue23.sum(axis=1)
cands = [(i + 365, int(rowcount[i])) for i in range(len(rowcount)) if rowcount[i] > 200]
print("023 box border rows (frame y, count):", cands)
# 023 subtitle ink census (certified 0000CC @22.5 bold)
regS = img23[78:112, 250:800]
r3, g3, b3 = regS[..., 0], regS[..., 1], regS[..., 2]
bl3 = (b3 > 100) & (b3 > r3 + 40)
spix = regS[bl3]
print("023 subtitle blue darkest-30% mean:", spix[spix[:, 2] < np.percentile(spix[:, 2], 30)].mean(axis=0).round(1), "n=", len(spix))
# 024 rules text blue census (same method)
regT = img24[363:495, 100:900]
r4, g4, b4 = regT[..., 0], regT[..., 1], regT[..., 2]
bl4 = (b4 > 100) & (b4 > r4 + 40)
tpix = regT[bl4]
print("024 rules text blue darkest-30% mean:", tpix[tpix[:, 2] < np.percentile(tpix[:, 2], 30)].mean(axis=0).round(1), "n=", len(tpix))
# red census 024 (rules red text)
red4 = (r4 > 110) & (r4 > b4 + 40) & (g4 < r4 - 30)
rpix = regT[red4]
print("024 rules red darkest-30% mean:", rpix[rpix[:, 0] < np.percentile(rpix[:, 0], 30)].mean(axis=0).round(1), "n=", len(rpix))
# 023 red text census (Problems: / delta labels) for family match
regR = img23[365:490, 100:900]
r5, g5, b5 = regR[..., 0], regR[..., 1], regR[..., 2]
red5 = (r5 > 110) & (r5 > b5 + 40) & (g5 < r5 - 30)
rpix5 = regR[red5]
if len(rpix5):
    print("023 box-region red darkest-30% mean:", rpix5[rpix5[:, 0] < np.percentile(rpix5[:, 0], 30)].mean(axis=0).round(1), "n=", len(rpix5))

# --- font width checks ---
fonts = {
    "bold": TTFont("/usr/share/fonts/TTF/Arialbd.TTF"),
    "boldita": TTFont("/usr/share/fonts/TTF/Arialbi.TTF"),
    "ita": TTFont("/usr/share/fonts/TTF/Ariali.TTF"),
}
UPM = fonts["bold"]["head"].unitsPerEm
def inkw(font, s):
    hmtx = font["hmtx"]; cmap = font.getBestCmap(); glyf = font["glyf"]
    gids = [cmap[ord(c)] for c in s]
    total = sum(hmtx[g_][0] for g_ in gids)
    lsb0 = hmtx[gids[0]][1]
    gl = glyf[gids[-1]]
    xMax = gl.xMax if gl.numberOfContours else 0
    rsb = hmtx[gids[-1]][0] - (hmtx[gids[-1]][1] + xMax)
    return (total - lsb0 - rsb) / UPM

sub = "(Rules Controlling Good Positional Encoder)"
print("\nsubtitle ink widths: measured 470.3 (bloom ~2-3) -> true ~467-468")
print(f"  bold 22.5: {inkw(fonts['bold'], sub)*22.5:.1f}   bold 22: {inkw(fonts['bold'], sub)*22:.1f}   bold 22.24: {inkw(fonts['bold'], sub)*22.24:.1f}")
L1 = "[1] \u03b4 value should be same for Long sequence and short sequence"
L2 = "(same positions will be encoded with same values irrespective of the length of the sequence)"
L3 = "[2] Range of position encoded values should NOT depend on sequence length"
L4 = "(predefined fixed range  e.g. from 0 to 1 , form -1 to 1 , ...)"
L5 = "[3] Position Encoding  should be a  VECTOR (not scalar) and of same dimension as Word Embedding"
L6 = "(in order to easily  combine Position Encoding and Word Encoding vectors)"
meas = {"L1": 547.5, "L2": 725.8, "L3": 662.2, "L4": 447.4, "L5": 833.2, "L6": 586.1}
for tag, s in (("L1", L1), ("L3", L3), ("L5", L5)):
    print(f"{tag}: meas {meas[tag]}  bold18 {inkw(fonts['bold'], s)*18:.1f}  bold18.5 {inkw(fonts['bold'], s)*18.5:.1f}  bold19 {inkw(fonts['bold'], s)*19:.1f}  bold19.5 {inkw(fonts['bold'], s)*19.5:.1f}")
for tag, s in (("L2", L2), ("L4", L4), ("L6", L6)):
    print(f"{tag}: meas {meas[tag]}  ita17 {inkw(fonts['ita'], s)*17:.1f}  ita17.5 {inkw(fonts['ita'], s)*17.5:.1f}  ita18 {inkw(fonts['ita'], s)*18:.1f}  bold17.5 {inkw(fonts['bold'], s)*17.5:.1f}")
