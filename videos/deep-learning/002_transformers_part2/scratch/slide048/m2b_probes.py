#!/usr/bin/env python3
"""m2b_probes.py — direct color probes + corrected masks for slide_048.jpg elements."""
from PIL import Image
import numpy as np

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_048.jpg'
A = np.asarray(Image.open(F).convert('RGB')).astype(int)
H, W = A.shape[:2]
out = []
def p(*a):
    s = ' '.join(str(x) for x in a); out.append(s); print(s)

def spans(bool_1d, min_len=2):
    res = []
    i = 0; n = len(bool_1d)
    while i < n:
        if bool_1d[i]:
            j = i
            while j < n and bool_1d[j]:
                j += 1
            if j - i >= min_len:
                res.append((i, j - 1))
            i = j
        else:
            i += 1
    return res

p('=== m2b_probes ===')
# MLP row probe: scan y 215..270 for the pink boxes; sample x=200 col
p('col 200, y 215..272:', [(y, tuple(A[y, 200])) for y in range(215, 272, 3)])
p('row 238, x 140..640 every 12:', [(x, tuple(A[238, x])) for x in range(140, 640, 12)])
p()
# plus-circle row probe (between MHSA bar and LayerNorm bar): y ~405..420? and ~345..360?
p('row 350, x 180..640 every 20:', [(x, tuple(A[350, x])) for x in range(180, 640, 20)])
p()
# token rows: bottom X row y ~495..515; sample row 505
p('row 505, x 170..920 every 30:', [(x, tuple(A[505, x])) for x in range(170, 920, 30)])
p()
# top Y row y ~58..72
p('row 65, x 170..920 every 30:', [(x, tuple(A[65, x])) for x in range(170, 920, 30)])
p()
# dots: top blue ~ (620..700, 63..67); bottom green (~620..700, 498..502)
p('top dots row 64, x 615..710:', [(x, tuple(A[64, x])) for x in range(615, 710, 5)])
p('bottom dots row 500, x 615..710:', [(x, tuple(A[500, x])) for x in range(615, 710, 5)])
p()
# inset internals: V/K/Q circles ~y 425..445; Add&Norm boxes; Feed Forward; MHA box
p('col 700, y 130..250:', [(y, tuple(A[y, 700])) for y in range(130, 250, 6)])
p('col 750, y 330..420:', [(y, tuple(A[y, 750])) for y in range(330, 420, 6)])
p('row 437, x 645..860 every 10:', [(x, tuple(A[437, x])) for x in range(645, 860, 10)])
p()
# vertical title zone: x 85..120, y 100..430 (red text on gray)
p('title zone row 200 x 85..125:', [(x, tuple(A[200, x])) for x in range(85, 125, 2)])
p('title zone row 300 x 85..125:', [(x, tuple(A[300, x])) for x in range(85, 125, 2)])
p()
# tags: Block Output (~x58..180, y48..75); Block Input (~y483..510)
p('tag row 60, x 55..185 every 6:', [(x, tuple(A[60, x])) for x in range(55, 185, 6)])
p('tag col 120, y 44..80:', [(y, tuple(A[y, 120])) for y in range(44, 80, 2)])
p('tag col 120, y 480..515:', [(y, tuple(A[y, 120])) for y in range(480, 515, 2)])

with open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide048/m2b_output.txt', 'w') as f:
    f.write('\n'.join(out) + '\n')
