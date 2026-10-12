#!/usr/bin/env python3
"""Compose labeled montages of the banked slide025 crops for vision reads."""
from PIL import Image, ImageDraw
import os

D = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch/slide025"

def montage(parts, out, target_h=560):
    imgs = []
    for tag, f in parts:
        im = Image.open(os.path.join(D, f)).convert("RGB")
        s = target_h / im.height
        im = im.resize((int(im.width * s), target_h), Image.LANCZOS)
        imgs.append((tag, im))
    gap = 24
    W = sum(im.width for _, im in imgs) + gap * (len(imgs) + 1)
    canvas = Image.new("RGB", (W, target_h + 56), (255, 255, 255))
    dr = ImageDraw.Draw(canvas)
    x = gap
    for tag, im in imgs:
        dr.text((x, 8), tag, fill=(200, 0, 0))
        canvas.paste(im, (x, 48))
        x += im.width + gap
    canvas.save(os.path.join(D, out))
    print(out, canvas.size)

# A: diagram labels (neurons closeup + Net_i + Net_j + w_ji labels)
montage([("[A] neurons rows closeup", "c_neurons.png"),
         ("[B] Net_i label+pointer", "c_neti.png"),
         ("[C] Net_j label+pointer", "c_netj.png"),
         ("[D] w_ji labels", "c_w3.png")], "montageA_labels.png")

# B: top strip wide + the two dotted-line ends at 8x
montage([("[A] top strip (Input Samples box, dotted line, Sample Label box)", "c_top.png"),
         ("[B] line LEFT end 8x", "z_line_leftend_8x.png"),
         ("[C] line RIGHT end 8x", "z_line_rightend_8x.png")], "montageB_top.png", target_h=420)

# C: bottom (arrows+callouts), i-arrow closeup, right column (Output/Error/Class)
montage([("[A] below-panel strip (block arrows i,j + callout boxes)", "c_below.png"),
         ("[B] i-arrow closeup", "c_arrow_i.png"),
         ("[C] right column (Output boxes, Error bar, Class boxes)", "c_right.png")], "montageC_bottom.png", target_h=520)
