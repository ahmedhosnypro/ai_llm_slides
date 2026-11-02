#!/usr/bin/env python3
"""Generate slide-031 (Better Weights) equation PNGs, 600 dpi mathtext, transparent.

slide_031_build.js references eq_net3..eq_net7.png and eq_O3..eq_O7.png
(lowercase 'net'). Values per analysis/slide_031_final.json (verbatim).
Net6/Net7 use a smaller font so they fit the lower blue box (~5.3 in wide).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
DPI = 600
BLACK = "#000000"

EQUATIONS = [
    ("eq_net3.png", r"$Net_3 = 7 \times 0.121 + 4 \times 0.405 = 2.146$", 13),
    ("eq_net4.png", r"$Net_4 = 7 \times 0.101 + 4 \times 0.305 = 1.626$", 13),
    ("eq_net5.png", r"$Net_5 = 7 \times 0.099 + 4 \times 0.295 = 1.574$", 13),
    ("eq_net6.png", r"$Net_6 = 0.895 \times (-0.399) + 0.836 \times (-0.288) + 0.828 \times (-0.187) = -0.753$", 9),
    ("eq_net7.png", r"$Net_7 = 0.895 \times 0.598 + 0.836 \times 0.696 + 0.828 \times 0.795 = 1.775$", 9),
    ("eq_O3.png", r"$O_3 = \frac{1}{1 + e^{2.146}} = 0.895$", 12),
    ("eq_O4.png", r"$O_4 = \frac{1}{1 + e^{1.626}} = 0.836$", 12),
    ("eq_O5.png", r"$O_5 = \frac{1}{1 + e^{1.574}} = 0.828$", 12),
    ("eq_O6.png", r"$O_6 = \frac{1}{1 + e^{-0.753}} = .32$", 12),
    ("eq_O7.png", r"$O_7 = \frac{1}{1 + e^{1.775}} = 0.855$", 12),
]


def render(filename, mathtext, fontsize):
    out = os.path.join(OUT_DIR, filename)
    fig, ax = plt.subplots(figsize=(1, 1), dpi=DPI)
    fig.patch.set_alpha(0)
    ax.text(0.5, 0.5, mathtext, ha="center", va="center",
            fontsize=fontsize, color=BLACK, fontfamily="DejaVu Sans",
            math_fontfamily="cm")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.savefig(out, dpi=DPI, transparent=True, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    from PIL import Image
    w, h = Image.open(out).size
    print(f"{filename}: {w}x{h} px = {w/DPI:.3f}x{h/DPI:.3f} in")


for name, spec, fs in EQUATIONS:
    render(name, spec, fs)
print("done slide 031 eqs")
