import numpy as np
from PIL import Image

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide041/render/slide-1.png").convert("RGB")).astype(int)
H, W = im.shape[:2]
S = 150 / 72.0

def at(x, y):  # sample by FRAME px coords
    return im[int(y*S), int(x*S)]

def runs_col(x, y0, y1, label):
    print(f"--- col x={x} ({label}) ---")
    col = im[int(y0*S):int(y1*S)+1, int(x*S)]
    prev = None; start = y0
    for i, pxv in enumerate(col):
        t = tuple(int(v) for v in pxv)
        if prev is None:
            prev = list(t); start = y0 + i; continue
        if abs(t[0]-prev[0])>16 or abs(t[1]-prev[1])>16 or abs(t[2]-prev[2])>16:
            print(f"  {start:4d}..{y0+i-1:4d} rgb({prev[0]},{prev[1]},{prev[2]})")
            prev = list(t); start = y0 + i
        else:
            for j in range(3): prev[j] = int(prev[j]*0.85 + t[j]*0.15)
    print(f"  {start:4d}..{y1:4d} rgb({prev[0]},{prev[1]},{prev[2]})")

def runs_row(y, x0, x1, label):
    print(f"--- row y={y} ({label}) ---")
    row = im[int(y*S), int(x0*S):int(x1*S)+1]
    prev = None; start = x0
    for i, pxv in enumerate(row):
        t = tuple(int(v) for v in pxv)
        if prev is None:
            prev = list(t); start = x0 + i; continue
        if abs(t[0]-prev[0])>16 or abs(t[1]-prev[1])>16 or abs(t[2]-prev[2])>16:
            print(f"  {start:4d}..{x0+i-1:4d} rgb({prev[0]},{prev[1]},{prev[2]})")
            prev = list(t); start = x0 + i
        else:
            for j in range(3): prev[j] = int(prev[j]*0.85 + t[j]*0.15)
    print(f"  {start:4d}..{x1:4d} rgb({prev[0]},{prev[1]},{prev[2]})")

# encoder column center + decoder column center (frame px)
runs_col(690, 100, 530, "encoder stack center")
runs_col(787, 100, 530, "decoder stack center")
# center zoom mid columns
runs_col(405, 200, 535, "center zoom left-mid")
runs_col(440, 200, 535, "center zoom mid")
# rows through the right panel MHA level and bottom
runs_row(300, 570, 900, "right panel y=300")
runs_row(465, 570, 900, "right panel y=465")
# row through center zoom circles
runs_row(496, 290, 525, "center zoom circles row")
