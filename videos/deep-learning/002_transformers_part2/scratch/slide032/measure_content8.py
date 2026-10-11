#!/usr/bin/env python3
"""v8: font-size fitting from advance sums (Liberation Sans = Arial metrics) + callout lines."""
from PIL import Image, ImageFont
import numpy as np

# find Liberation fonts
import glob
cands = glob.glob('/usr/share/fonts/**/LiberationSans*', recursive=True)
print("fonts:", cands[:6])
reg = [c for c in cands if 'Regular' in c][0]
bold = [c for c in cands if 'Bold' in c and 'Italic' not in c][0]
ital = [c for c in cands if 'Italic' in c and 'Bold' not in c][0]
boldit = [c for c in cands if 'BoldItalic' in c][0] if any('BoldItalic' in c for c in cands) else ital

def em_for(text, target_pt, fontpath, size=200):
    f = ImageFont.truetype(fontpath, size)
    w = f.getlength(text)
    return target_pt / (w / size)

tests = [
    ("title 'Sin/Cos Positional Encoder'", "Sin/Cos Positional Encoder", 288.2, bold),
    ("subtitle", 'Vector of Dimension "2" to define Position', 508.7, bold),
    ("L1 italic full", 'This vector can be used to define word position at step "t" , t=0,1,2,3,4,5,6,7,....', 741.6, ital),
    ("L2 'Values are '", 'Values are ', 192.8 - 87.8 - 0, bold),  # 103..204 frame -> slide 87.8..192.8
    ("L2 highlight", 'between -1 and 1', 157.1, bold),
    ("L2 green ' (bounded values)'", ' (bounded values)', 520.6 - 349.9, None),
    ("L3 'Distance'", 'Distance', 80.1, bold),
    ("L3 mid", ' between vectors representing positions ', 558.0 - 167.9, None),
    ("L3 highlight2", '"t" and "t+1"', 121.7, bold),
    ("L3 '  is '", '  is ', 714.1 - 679.7, None),
    ("L3 'constant'", 'constant', 81.1, bold),
    ("L4 italic", 'irrespective of "t"', 265.7 - 86.9 - 10, ital),  # approx incl trailing spaces
    ("L4 green", '[Distance (Pos1, Pos2) = Distance (Pos90, Pos91)]', 739.0 - 265.7, None),
    ("L5 highlight", '"t" may take any positive value', 292.3, bold),
    ("L5 green", ' (No limitation of length of Sequence )', 739.0 - 380.1, None),
    ("L6 blue", 'Position Vector Length = 2', 355.1 - 86.7, bold),
    ("L6 red", '(Cannot be combined with Word Embedding Vector) ??', 513.9, bold),
]
for label, text, target, fp in tests:
    if fp is None: fp = reg
    try:
        em = em_for(text, target, fp)
        print(f"{label:42s} target {target:7.1f}pt -> em {em:5.2f}pt")
    except Exception as e:
        print(label, "ERR", e)

# ---- callout two text lines: x extents ----
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_032.jpg').convert('RGB')
a = np.asarray(im).astype(int)
FX0, SX, SY = 18.63, 0.96123, 0.95556
def to_slide(fx): return (fx - FX0) / SX
dark = a.sum(axis=2) < 430
for (y0, y1, lbl) in [(126, 146, 'callout line A'), (147, 166, 'callout line B')]:
    m = dark[y0:y1, 215:860]
    xs = np.where(m.any(axis=0))[0]
    ys = np.where(m.any(axis=1))[0]
    if len(xs):
        print(f"{lbl}: frame x {215+xs.min()}..{215+xs.max()} y {y0+ys.min()}..{y0+ys.max()} -> slide x {to_slide(215+xs.min()):.1f}..{to_slide(215+xs.max()+1):.1f}")
        # red chars
        z = a[y0:y1, 215:860]
        redc = (z[:, :, 0] - z[:, :, 1] > 55) & (z[:, :, 0] - z[:, :, 2] > 55) & (z[:, :, 0] > 100)
        ys3, xs3 = np.where(redc)
        if len(ys3):
            print(f"   red chars: frame x {215+xs3.min()}..{215+xs3.max()} (n={len(ys3)})")

# callout border rows/cols exact
ob = (a[:, :, 0] - a[:, :, 2] > 60) & (a[:, :, 0] > 130) & (a[:, :, 1] > 60) & (a[:, :, 1] < 190) & (a[:, :, 2] < 90)
sub = ob[110:180, 200:870]
rs = sub.sum(axis=1); cs = sub.sum(axis=0)
print("callout border rows>30:", [(110 + i, int(rs[i])) for i in np.where(rs > 30)[0]])
print("callout border cols>10:", [(200 + i, int(cs[i])) for i in np.where(cs > 10)[0]][:8], [(200 + i, int(cs[i])) for i in np.where(cs > 10)[0]][-4:])
