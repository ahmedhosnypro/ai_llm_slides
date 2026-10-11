#!/usr/bin/env python3
"""Inheritance diff: slide-010 render vs slide-006 certified render.

The delta must be confined to the expected delta zones; outside them the renders
should be near-identical (same certified component draws the shared base).
"""
from PIL import Image
import numpy as np
from scipy import ndimage as ndi

A = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide006/render_1.png"
B = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide010/render_1.png"
a = np.asarray(Image.open(A).convert("RGB"), dtype=np.int16)
b = np.asarray(Image.open(B).convert("RGB"), dtype=np.int16)
print("sizes:", a.shape, b.shape)
H = min(a.shape[0], b.shape[0]); W = min(a.shape[1], b.shape[1])
a, b = a[:H, :W], b[:H, :W]
d = np.abs(a - b).sum(axis=2)
mask = d > 60
print("changed px:", int(mask.sum()), f"({100*mask.sum()/mask.size:.2f}%)")

# frame-px delta zones (from the frame diff + this build's plan), in render px
zones = {
    "title+subtitle":        (200, 50, 710, 112),
    "green callout+conn":    (60, 138, 440, 250),
    "left attention box":    (100, 195, 480, 325),
    "right attention box":   (485, 255, 865, 370),
    "dash fan / heads":      (440, 255, 860, 345),
    "gray summary box":      (510, 425, 915, 535),
    "pink callout (moved)":  (548, 360, 850, 455),
    "pink connector":        (480, 330, 570, 400),
    "decoder content band":  (475, 110, 915, 300),
    "encoder content band":  (40, 295, 500, 505),
    "captions":              (170, 500, 350, 530),
    "badge numeral":         (865, 45, 925, 95),
    "white backdrop card":   (43, 116, 918, 500),
    "Decoder caption delta": (640, 84, 835, 112),
    "Encoder caption delta": (170, 500, 380, 532),
}
cover = np.zeros_like(mask)
for nm, (x0, y0, x1, y1) in zones.items():
    cover[int(y0*2.0833):int(y1*2.0833), int(x0*2.0833):int(x1*2.0833)] = True
outside = mask & ~cover
print("changed px inside delta zones:", int((mask & cover).sum()))
print("changed px OUTSIDE zones:", int(outside.sum()))
lab, n = ndi.label(outside, structure=np.ones((3, 3)))
big = []
for i, sl in enumerate(ndi.find_objects(lab)):
    ar = int((lab[sl] == i + 1).sum())
    if ar > 120:
        big.append((ar, sl[1].start/2.0833, sl[0].start/2.0833, sl[1].stop/2.0833, sl[0].stop/2.0833))
big.sort(reverse=True)
print("outside-zone components >120 render px (frame coords):")
for ar, x0, y0, x1, y1 in big[:20]:
    print(f"  area={ar} x{x0:.0f}..{x1:.0f} y{y0:.0f}..{y1:.0f}")
