#!/usr/bin/env python3
"""Final report-grade evidence for the 048 badge ruling.

Key idea: the badge chrome is identical across slides; a digit's rasterization
depends only on its slot (tens @x867-873, units @x875-882 for 7-wide tens
digits). So for the occluded 048 right digit (2 visible rows) the fair
comparison is against UNITS digits of two-digit badges whose tens digit is
7 wide starting at x867 — the same subpixel phase as "4X".
Also re-checks the left digit against ALL digit slots.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import badge_audit as ba
import numpy as np


def ascii_of(m):
    return "\n".join("".join("#" if v else "." for v in row) for row in m)


def iou_shift(obs, tpl, dxs=(-2, -1, 0, 1, 2)):
    best, bestdx = 0.0, None
    for dx in dxs:
        H = max(obs.shape[0], tpl.shape[0]) + 2
        W = max(obs.shape[1], tpl.shape[1]) + 8
        A = np.zeros((H, W), bool); B = np.zeros((H, W), bool)
        A[1:1 + obs.shape[0], 4:4 + obs.shape[1]] = obs
        x2 = 4 + dx
        if x2 < 0 or x2 + tpl.shape[1] > W:
            continue
        B[1:1 + tpl.shape[0], x2:x2 + tpl.shape[1]] = tpl
        u = (A | B).sum()
        v = float((A & B).sum()) / u if u else 0.0
        if v > best:
            best, bestdx = v, dx
    return round(best, 3), bestdx


def ink_span(row):
    idx = np.where(row)[0]
    return (int(idx.min()), int(idx.max())) if len(idx) else None


rec48 = ba.analyze_badge("slide_048")
m48 = rec48["_glyph_masks"]
b48 = rec48["_glyph_bboxes"]
obsL = m48[0][:5, :]
obsR = m48[1][:5, :]         # right digit: 5 visible rows after occlusion fix
print("OBSERVED 048  left bbox=%s right bbox=%s" % (b48[0], b48[1]))
print("  left top-5 rows (abs ink x-span per row):",
      [(None if ink_span(r) is None else (ink_span(r)[0] + b48[0][0], ink_span(r)[1] + b48[0][0])) for r in obsL])
print("  right top-5 rows (abs ink x-span per row):",
      [(None if ink_span(r) is None else (ink_span(r)[0] + b48[1][0], ink_span(r)[1] + b48[1][0])) for r in obsR])

print("\n=== A. Phase-matched UNITS digits (two-digit badges, tens 7 wide @x867-873) ===")
print("slide  digit  units_bbox        top5 ink spans (abs)      top5 pattern")
phase_rows = []
for i in range(10, 60):
    name = f"slide_{i:03d}"
    if name == "slide_048":
        continue
    rec = ba.analyze_badge(name)
    if "_glyph_masks" not in rec:
        continue
    exp = str(i)
    masks, bxs = rec["_glyph_masks"], rec["_glyph_bboxes"]
    if len(masks) != 2:
        continue
    tens_bb, units_bb = bxs[0], bxs[1]
    if not (tens_bb[0] == 867 and tens_bb[2] == 873):
        continue
    um = masks[-1]
    t2 = um[:5, :]
    spans = [tuple(v + units_bb[0] for v in ink_span(r)) for r in t2]
    pat = " / ".join("".join("#" if v else "." for v in r) for r in t2)
    phase_rows.append((name, exp[-1], units_bb, spans, pat))
    print(f"{name}   {exp[-1]}      {units_bb}   {spans}   {pat!r}")

print("\n=== B. The 4X family directly (tens digit = 4) ===")
for name in ["slide_040", "slide_041", "slide_042", "slide_043", "slide_044",
             "slide_045", "slide_046", "slide_047", "slide_049"]:
    rec = ba.analyze_badge(name)
    if "_glyph_masks" not in rec:
        print(name, "unreadable/occluded", rec.get("error", ""))
        continue
    exp = str(int(name[-3:]))
    masks, bxs = rec["_glyph_masks"], rec["_glyph_bboxes"]
    print(f"--- {name} expected '{exp}' glyph bboxes: {bxs}")
    for gi, (m, bb) in enumerate(zip(masks, bxs)):
        print(ascii_of(m))
    if len(masks) == 2:
        r_iou, r_dx = iou_shift(obsR, masks[-1][:5, :])
        print(f"    units top5 vs 048-observed-right: IoU={r_iou} at dx={r_dx}")

print("\n=== C. Left digit vs ALL slots (best per digit char) ===")
bestL = {}
for i in range(2, 61):
    name = f"slide_{i:03d}"
    if name == "slide_048":
        continue
    rec = ba.analyze_badge(name)
    if "_glyph_masks" not in rec:
        continue
    exp = str(i)
    for pos, (m, bb) in enumerate(zip(rec["_glyph_masks"], rec["_glyph_bboxes"])):
        ch = exp[pos] if len(exp) == len(rec["_glyph_masks"]) else None
        if ch is None:
            continue
        iou, dx = iou_shift(obsL, m[:5, :])
        if ch not in bestL or iou > bestL[ch][0]:
            bestL[ch] = (iou, dx, name, pos)
for ch in sorted(bestL):
    iou, dx, src, pos = bestL[ch]
    tag = "tens" if pos == 0 and len(src[-3:]) == 3 and int(src[-3:]) >= 10 else "units/single"
    print(f"  '{ch}': IoU={iou} dx={dx} from {src} ({tag})")
