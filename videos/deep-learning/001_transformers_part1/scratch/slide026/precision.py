#!/usr/bin/env python3
"""Precision pass: point samples + row/col scans to pin every box edge."""
import numpy as np
from PIL import Image

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_026.jpg").convert("RGB")
A = np.asarray(IM).astype(int)

def px(name, x, y):
    c = A[y, x]
    print(f"{name:34s} ({x:3d},{y:3d}) #{c[0]:02X}{c[1]:02X}{c[2]:02X} {tuple(int(v) for v in c)}")

def rowscan(name, y, x0, x1, target, tol):
    t = np.array(target)
    m = np.abs(A[y, x0:x1] - t).sum(axis=1) <= tol
    runs = []
    s = None
    for i, v in enumerate(m):
        if v and s is None: s = i
        if not v and s is not None: runs.append((x0 + s, x0 + i - 1)); s = None
    if s is not None: runs.append((x0 + s, x0 + len(m) - 1))
    print(f"{name:34s} y={y} runs={runs}")

def colscan(name, x, y0, y1, target, tol):
    t = np.array(target)
    m = np.abs(A[y0:y1, x] - t).sum(axis=1) <= tol
    runs = []
    s = None
    for i, v in enumerate(m):
        if v and s is None: s = i
        if not v and s is not None: runs.append((y0 + s, y0 + i - 1)); s = None
    if s is not None: runs.append((y0 + s, y0 + len(m) - 1))
    print(f"{name:34s} x={x} runs={runs}")

print("== point samples ==")
px("arrow_stack_to_dot_row1", 200, 246)
px("arrow_stack_to_dot_row1b", 170, 247)
px("arrow_dot_to_softmax", 420, 240)
px("query_arrow", 298, 440)
px("query_arrow2", 297, 450)
px("w_arrow_row1", 560, 247)
px("w_arrow_row1b", 600, 247)
px("vert_up_into_sigma", 555, 190)
px("vert_up_into_sigma2", 555, 180)
px("canvas_right_line", 867, 300)
px("canvas_right_line2", 868, 250)
px("pill_sim_fill", 270, 165)
px("pill_sim_fill2", 335, 175)
px("pill_prob_fill", 430, 165)
px("pill_wsum_fill", 595, 165)
px("pill_wsum_fill2", 660, 175)
px("highlight_core", 620, 66)
px("title_ink", 260, 65)
px("subtitle_ink", 200, 88)
px("red_token_sub", 738, 88)
px("glyph_yellow_L1", 72, 246)
px("glyph_pink_L1", 117, 246)
px("glyph_lav_L1", 135, 246)
px("glyph_gap", 90, 246)
px("stack_border_top", 98, 227)
px("strip_fill_between", 160, 495)
px("x2_highlight_border", 263, 490)
px("x2_highlight_border2", 300, 506)
px("x2_fill", 300, 490)
px("x2_fill2", 310, 495)
px("w_label_row1", 520, 240)
px("node1_area", 560, 246)
px("node_area2", 640, 287)
px("ybox_vector_mid", 590, 132)
px("ybox_border", 565, 121)
px("green_arrow_core", 590, 170)
px("dashed_curve_left", 60, 430)
px("dashed_curve_left2", 90, 450)
px("dashed_curve_right", 860, 440)
px("softmax_label", 473, 280)

print("\n== row scans (tan DotProduct box edges) ==")
rowscan("tan@y300", 300, 130, 480, (219, 204, 188), 40)
rowscan("tan@y250", 250, 130, 480, (219, 204, 188), 40)
rowscan("tan@y390", 390, 130, 480, (219, 204, 188), 40)
print("\n== col scans (DotProduct box top/bottom) ==")
colscan("tan@x300", 300, 150, 460, (219, 204, 188), 40)
colscan("tan@x270", 270, 150, 460, (219, 204, 188), 40)
print("\n== sigma box ==")
rowscan("cyan@y205", 205, 480, 700, (236, 252, 252), 30)
colscan("cyan@x530", 530, 150, 260, (236, 252, 252), 30)
print("\n== softmax bar ==")
colscan("pink@x473", 473, 150, 460, (249, 217, 248), 40)
rowscan("pink@y300", 300, 420, 520, (249, 217, 248), 40)
print("\n== left stack container ==")
colscan("mint@x98", 98, 200, 430, (229, 252, 236), 40)
rowscan("mint@y300", 300, 30, 180, (229, 252, 236), 40)
print("\n== right stack container ==")
colscan("mint@x803", 803, 200, 430, (229, 252, 236), 40)
rowscan("mint@y300", 300, 740, 900, (229, 252, 236), 40)
print("\n== strip container ==")
colscan("mint@x220", 220, 440, 540, (229, 252, 236), 40)
rowscan("mint@y495", 495, 150, 520, (229, 252, 236), 40)
print("\n== peach canvas edges ==")
rowscan("peach@y300", 300, 20, 940, (247, 227, 206), 30)
rowscan("peach@y150", 150, 20, 940, (247, 227, 206), 30)
colscan("peach@x700", 700, 80, 540, (247, 227, 206), 30)
colscan("peach@x480", 480, 80, 540, (247, 227, 206), 30)
