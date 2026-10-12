#!/usr/bin/env python3
"""Side-by-side delta sheets: 001 slide_043 (top, reference) vs 002 slide_017 (bottom).
002 crop is mapped from frame coords to the same slide-coord window and rescaled 1/0.9615.
Zones chosen from the normalized frame-vs-frame delta hotspots."""
from PIL import Image, ImageDraw
import os

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning"
P = Image.open(BASE + "/001_transformers_part1/unique_slides/slide_043.jpg").convert("RGB")
F = Image.open(BASE + "/002_transformers_part2/unique_slides/slide_017.jpg").convert("RGB")
OUT = BASE + "/002_transformers_part2/scratch/slide017/sheets"
os.makedirs(OUT, exist_ok=True)
AX, SX, AY, SYy = 18.250, 0.96150, 1.950, 0.95500

def sheet(name, sx0, sy0, sx1, sy1, zoom):
    # reference: slide coords == 001 frame px
    ref = P.crop((int(sx0), int(sy0), int(sx1), int(sy1)))
    # variant: window in 002 frame coords
    fx0, fy0 = AX + SX * sx0, AY + SYy * sy0
    fx1, fy1 = AX + SX * sx1, AY + SYy * sy1
    var = F.crop((int(round(fx0)), int(round(fy0)), int(round(fx1)), int(round(fy1))))
    var = var.resize((ref.width, ref.height), Image.LANCZOS)
    w, h = ref.width, ref.height
    S = Image.new("RGB", (w, h * 2 + 6), (255, 0, 255))
    S.paste(ref, (0, 0))
    S.paste(var, (0, h + 6))
    S = S.resize((w * zoom, (h * 2 + 6) * zoom), Image.LANCZOS)
    d = ImageDraw.Draw(S)
    d.line([(0, h * zoom + 3), (S.width, h * zoom + 3)], fill=(255, 0, 255), width=3)
    S.save(OUT + "/" + name + ".png")
    print(name, S.size)

# S1 top band: title + vecbox + 1xd + LT box
sheet("s1_topband", 385, 42, 915, 120, 2)
# S2 concat bar with labels
sheet("s2_bar", 180, 118, 700, 158, 3)
# S3 left column: input strips, W_k boxes, K bars, K labels, Dot Product left edge
sheet("s3_leftcol", 86, 296, 262, 448, 3)
# S4 right column: nodes, V labels/bars, W_v, X cells
sheet("s4_rightcol", 415, 295, 625, 448, 3)
# S5 climbing chips + ovals + Probabilities
sheet("s5_chips", 280, 168, 545, 312, 3)
# S6 legend + query-right + W1 zone
sheet("s6_bottomright", 545, 435, 915, 540, 2)
# S7 swoosh label + wochips
sheet("s7_wochips", 595, 235, 800, 420, 3)
