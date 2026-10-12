import importlib.util, json, os
import numpy as np
from PIL import Image

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

base = load("re_base", "/home/ahmed/Projects/ai_llm_slides/scripts/render_eq.py")

OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch/matrix_test"

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


class StixMod:
    """Same contract as render_eq.render but with the STIX serif fontset
    (mirrors scripts/render_eq_stix.py, whose ../scratch_math import target is
    absent in this checkout)."""
    DPI = 600
    PAD_PX = 8

    @staticmethod
    def render(latex, out, fontsize, color, bg=None):
        matplotlib.rcParams["mathtext.fontset"] = "stix"
        try:
            return base.render(latex, out, fontsize, color, bg)
        finally:
            matplotlib.rcParams["mathtext.fontset"] = "dejavusans"


stix = StixMod()

def split_ink(png):
    a = np.asarray(Image.open(png).convert("RGBA")).astype(int)
    ink = a[:, :, 3] > 40
    colc = ink.sum(axis=0)
    runs = []; s = None
    for x, v in enumerate(colc > 0):
        if v and s is None: s = x
        if not v and s is not None: runs.append((s, x - 1)); s = None
    if s is not None: runs.append((s, len(colc) - 1))
    th, su = runs[0], runs[-1]
    def yext(x0, x1):
        rows = np.where(ink[:, x0:x1+1].any(axis=1))[0]
        return (rows[0], rows[-1])
    return th, yext(*th), su, yext(*su)

to_pt = lambda v: v / 600 * 72
# Targets: theta w16 h18 (baseline=bottom); sub below-baseline 5.5, h 11.
for tag, mod in [("dejavu", base), ("stix", stix)]:
    for fs in [24, 26, 28, 30, 32]:
        p = f"{OUT}_{tag}_{fs}.png"
        info = mod.render(r"\theta_1", p, fs, "#000000")
        thx, thy, sux, suy = split_ink(p)
        print(f"{tag} fs={fs}: theta w={to_pt(thx[1]-thx[0]+1):.1f} h={to_pt(thy[1]-thy[0]+1):.1f} "
              f"| sub w={to_pt(sux[1]-sux[0]+1):.1f} h={to_pt(suy[1]-suy[0]+1):.1f} "
              f"belowbl={to_pt(suy[1]-info['baseline_px']):.1f} bfrac={info['baseline_frac']}")
