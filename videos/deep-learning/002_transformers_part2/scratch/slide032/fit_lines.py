#!/usr/bin/env python3
"""Composite per-line font fitting: solve em so the run-advance sum matches the
measured ink width. Also callout text size + left edges."""
from PIL import Image, ImageFont
import numpy as np

LB = '/usr/share/fonts/liberation/LiberationSans-Bold.ttf'
LI = '/usr/share/fonts/liberation/LiberationSans-Italic.ttf'
LBI = '/usr/share/fonts/liberation/LiberationSans-BoldItalic.ttf'
LR = '/usr/share/fonts/liberation/LiberationSans-Regular.ttf'
VB = '/usr/share/fonts/TTF/Verdanab.TTF'
LQ, RQ = '\u201c', '\u201d'
CHI = '\u203a'

def adv(runs, em):
    total = 0.0
    for text, fp in runs:
        f = ImageFont.truetype(fp, 200)
        total += f.getlength(text) / 200 * em
    return total

def solve(runs, target, lo=10, hi=40):
    for _ in range(40):
        mid = (lo + hi) / 2
        if adv(runs, mid) < target: lo = mid
        else: hi = mid
    return (lo + hi) / 2

DQ = '"'
lines = {
    'L1 (all bold-italic)': ([(f'This vector can be used to define word position at step {LQ}t{RQ} , t=0,1,2,3,4,5,6,7,....', LBI)], 810.9 - 69.3),
    'L2 (bold + green bi)': ([('Values are ', LB), (f'between -1 and 1', LB), (f' (bounded values)', LBI)], 520.6 - 87.8),
    'L3 (all bold-italic)': ([(f'Distance', LBI), (' between vectors representing positions ', LBI), (f'{LQ}t{RQ} and {LQ}t+1{RQ}', LBI), ('  is ', LBI), ('constant', LBI)], 795.2 - 87.8),
    'L4 (bi + green bi)': ([(f'irrespective of {LQ}t{RQ}  ', LBI), ('[Distance (Pos1, Pos2) = Distance (Pos90, Pos91)]', LBI)], 739.0 - 86.9),
    'L5 (bi + green bi)': ([(f'{DQ}t{DQ} may take any positive value', LBI), (' (No limitation of length of Sequence )', LBI)], 739.0 - 87.8),
    'L6 (bold + red bold)': ([('Position Vector Length = 2', LB), ('  ', LB), ('(Cannot be combined with Word Embedding Vector) ??', LB)], 870.1 - 86.9),
    'TITLE (Verdana bold)': ([('Sin/Cos Positional Encoder', VB)], 618.3 - 330.2),
    'SUBTITLE (arial bold)': ([(f'Vector of Dimension {LQ}2{RQ} to define Position', LB)], 699.6 - 254.2),
}
for label, (runs, target) in lines.items():
    em = solve(runs, target)
    print(f"{label:26s} target {target:7.1f}pt -> em {em:5.2f}  (adv@20pt {adv(runs,20):7.1f})")

# chevron advance check at 20pt
f = ImageFont.truetype(LR, 200)
print(f"\n'\\u203a' advance/em {f.getlength(CHI)/200:.4f}; bold {ImageFont.truetype(LB,200).getlength(CHI)/200:.4f}")

# callout: line A left edge + size fit
a = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_032.jpg').convert('RGB')).astype(int)
dark = a.sum(axis=2) < 430
mA = dark[126:147, 226:846]
xs = np.where(mA.any(axis=0))[0]
mB = dark[147:167, 226:846]
xsB = np.where(mB.any(axis=0))[0]
FX0, SX = 18.63, 0.96123
sA0 = (226 + xs.min() - FX0) / SX; sA1 = (226 + xs.max() + 1 - FX0) / SX
sB0 = (226 + xsB.min() - FX0) / SX; sB1 = (226 + xsB.max() + 1 - FX0) / SX
print(f"\ncallout lineA ink slide x {sA0:.1f}..{sA1:.1f} (w {sA1-sA0:.1f})")
print(f"callout lineB ink slide x {sB0:.1f}..{sB1:.1f} (w {sB1-sB0:.1f})")
runsA = [(f'Where {LQ}t{RQ} is the step (position) and \u03c9 is the frequency of trigonometric', LR)]
runsB = [('function Sine/Cosine', LR)]
emA = solve(runsA, sA1 - sA0); emB = solve(runsB, sB1 - sB0)
print(f"callout lineA em {emA:.2f} (regular); lineB em {emB:.2f}")
emA_b = solve([(runsA[0][0], LB)], sA1 - sA0)
print(f"callout lineA em if bold {emA_b:.2f}")
EOF = None
