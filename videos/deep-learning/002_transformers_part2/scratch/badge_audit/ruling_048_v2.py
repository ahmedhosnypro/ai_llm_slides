#!/usr/bin/env python3
"""Definitive 048 ruling: compare its two visible digit tops against EVERY
deck badge's digit tops (position-anchored, +-1px tolerance), aggregated per
digit. Uses badge_audit.analyze_badge (same ink extraction as the main audit)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import badge_audit as ba
import numpy as np

def iou_shift(obs, tpl, dxs=(-1, 0, 1)):
    best, bestdx = 0.0, None
    for dx in dxs:
        H = max(obs.shape[0], tpl.shape[0]) + 2
        W = max(obs.shape[1], tpl.shape[1]) + 8
        A = np.zeros((H, W), bool); B = np.zeros((H, W), bool)
        A[1:1+obs.shape[0], 4:4+obs.shape[1]] = obs
        x2 = 4 + dx
        if x2 < 0 or x2 + tpl.shape[1] > W:
            continue
        B[1:1+tpl.shape[0], x2:x2+tpl.shape[1]] = tpl
        u = (A | B).sum()
        v = float((A & B).sum()) / u if u else 0.0
        if v > best:
            best, bestdx = v, dx
    return round(best, 3), bestdx

rec48 = ba.analyze_badge("slide_048")
masks48 = rec48["_glyph_masks"]
bbox48 = rec48["_glyph_bboxes"]
obs_left5 = masks48[0][:5, :]          # left digit, 5 visible rows
obs_right2 = masks48[1][:2, :]         # right digit, 2 visible rows
print("048 left  bbox", bbox48[0], "5 rows:")
print("\n".join("".join("#" if v else "." for v in r) for r in obs_left5))
print("048 right bbox", bbox48[1], "2 rows:")
print("\n".join("".join("#" if v else "." for v in r) for r in obs_right2))

# aggregate: per digit char, best IoU over deck occurrences (units digit = last glyph)
best_right, best_left = {}, {}
for i in range(2, 61):
    name = f"slide_{i:03d}"
    if name == "slide_048":
        continue
    rec = ba.analyze_badge(name)
    if "_glyph_masks" not in rec:
        continue
    expected = str(i)
    masks = rec["_glyph_masks"]
    if len(masks) != len(expected):
        continue
    units_mask = masks[-1]
    r_iou, r_dx = iou_shift(obs_right2, units_mask[:2, :])
    l_iou, l_dx = iou_shift(obs_left5, units_mask[:5, :])
    ch = expected[-1]
    if ch not in best_right or r_iou > best_right[ch][0]:
        best_right[ch] = (r_iou, r_dx, name, units_mask.shape[1])
    if ch not in best_left or l_iou > best_left[ch][0]:
        best_left[ch] = (l_iou, l_dx, name)

print("\nRIGHT digit (2 visible rows) vs every deck digit's top-2 rows:")
for ch in sorted(best_right):
    iou, dx, src, w = best_right[ch]
    print(f"  '{ch}': best IoU={iou} at dx={dx}  (from {src}, template w={w})")
print("LEFT digit (5 visible rows) vs every deck digit's top-5 rows:")
for ch in sorted(best_left):
    iou, dx, src = best_left[ch]
    print(f"  '{ch}': best IoU={iou} at dx={dx}  (from {src})")

# per-occurrence detail for the contenders 8, 9, 6, 0
print("\nDetail for contenders (right digit):")
for i in range(2, 61):
    name = f"slide_{i:03d}"
    if name == "slide_048":
        continue
    rec = ba.analyze_badge(name)
    if "_glyph_masks" not in rec:
        continue
    expected = str(i)
    masks = rec["_glyph_masks"]
    if len(masks) != len(expected):
        continue
    ch = expected[-1]
    if ch in "8960":
        um = masks[-1]
        r_iou, r_dx = iou_shift(obs_right2, um[:2, :])
        t2 = "\n".join("".join("#" if v else "." for v in r) for r in um[:2, :])
        print(f"  {name} units '{ch}' w={um.shape[1]} IoU={r_iou} dx={r_dx} top2: {t2!r}")
