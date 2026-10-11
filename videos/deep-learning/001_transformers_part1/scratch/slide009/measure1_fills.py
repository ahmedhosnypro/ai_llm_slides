#!/usr/bin/env python3
"""Pass 1: locate colored fill regions in slide_009.jpg via color masks."""
from PIL import Image
import numpy as np
from scipy import ndimage

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(IM).convert("RGB"), dtype=np.int16)

def mask_near(color, tol):
    c = np.array(color)
    return (np.abs(a - c).sum(axis=2) <= tol)

def report(name, m, min_area=300):
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    objs = ndimage.find_objects(lab)
    out = []
    for i, sl in enumerate(objs):
        ys, xs = sl
        area = int((lab[sl] == i + 1).sum())
        if area >= min_area:
            out.append((area, xs.start, ys.start, xs.stop, ys.stop))
    out.sort(reverse=True)
    print(f"--- {name}: {len(out)} comps (area>={min_area})")
    for area, x0, y0, x1, y1 in out[:12]:
        print(f"    area={area:6d} x{x0}..{x1} y{y0}..{y1} (w{x1-x0} h{y1-y0})")

# decoder-ish yellows (slide6 FDFF85 fill / FAEC69 hidden / E8FF6E green)
report("yellow FDFF85", mask_near((253, 255, 133), 60))
report("hidden FAEC69", mask_near((250, 236, 105), 60))
report("green E8FF6E", mask_near((232, 255, 110), 70))
# encoder peach (slide6 F8D5AD)
report("peach F8D5AD", mask_near((248, 213, 173), 60))
report("tan F9D5A3", mask_near((249, 213, 163), 50))
report("pink F2C7A7", mask_near((242, 199, 167), 50))
# slide9 additions
report("blue callout CCE4F7", mask_near((204, 228, 247), 45))
report("gray D9D9D9", mask_near((217, 217, 217), 30))
report("white FFFFFF", mask_near((255, 255, 255), 20))
report("bp pink F8BBD0", mask_near((248, 187, 208), 60))
report("bp green D5E8D5", mask_near((213, 232, 213), 45))
