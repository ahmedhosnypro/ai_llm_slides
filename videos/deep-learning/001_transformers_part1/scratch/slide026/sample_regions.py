#!/usr/bin/env python3
"""Targeted forensics: sample the interior of each expected region, then mask each
measured color for precise bboxes."""
import numpy as np
from PIL import Image

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_026.jpg").convert("RGB")
A = np.asarray(IM).astype(int)

def sample(name, x, y, r=3):
    reg = A[y-r:y+r+1, x-r:x+r+1].reshape(-1, 3)
    med = np.median(reg, axis=0).astype(int)
    print(f"{name:28s} ({x:3d},{y:3d}) med=#{med[0]:02X}{med[1]:02X}{med[2]:02X} {tuple(med)}")

print("== region interior samples (960x540) ==")
sample("left_stack_fill", 100, 300)
sample("right_stack_fill", 800, 300)
sample("sentence_strip_fill", 200, 495)
sample("dotproduct_box", 300, 320)
sample("softmax_bar", 475, 300)
sample("sigma_box", 580, 205)
sample("y_box_fill", 570, 130)
sample("pill_similarity", 300, 172)
sample("pill_probabilities", 475, 172)
sample("pill_weightedsum", 640, 172)
sample("vector_block_left_X1", 100, 250)   # guess
sample("badge_fill", 893, 71)
sample("highlight", 620, 65)
sample("peach_mid", 430, 240)
sample("peach_low", 620, 440)

def mask(name, target, tol):
    t = np.array(target)
    m = (np.abs(A - t).sum(axis=2) <= tol)
    n = int(m.sum())
    if n == 0:
        print(f"{name:24s} n=0"); return None
    ys, xs = np.where(m)
    # largest connected-ish blobs via column/row runs
    cols = np.where(m.sum(axis=0) >= 4)[0]
    rows = np.where(m.sum(axis=1) >= 4)[0]
    def runs(idx, gap=5):
        if len(idx) == 0: return []
        r, s, p = [], idx[0], idx[0]
        for v in idx[1:]:
            if v > p + gap: r.append((int(s), int(p))); s = v
            p = v
        r.append((int(s), int(p)))
        return r
    print(f"{name:24s} n={n:6d} bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} cols={runs(cols)[:14]} rows={runs(rows)[:14]}")
    return m

print("\n== measured-color masks ==")
mask("tan_dotproduct", (200, 179, 156), 45)
mask("plum_softmax", (223, 166, 223), 40)
mask("lightblue_sigma", (197, 224, 245), 40)
