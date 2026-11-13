#!/usr/bin/env python3
"""Render slide 014 derivation equations at their measured 18 pt size."""
import subprocess
import sys

RENDER = "/home/codespace/ai_llm_slides/scripts/render_eq_wide.py"
BUILD = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"
CASES = [
    ("eq14_sum1", r"= w_{11}x_1 + w_{12}x_2"),
    ("eq14_sum2", r"= w_{21}x_1 + w_{22}x_2"),
    ("eq14_sum3", r"= (w_{11}x_1 + w_{12}x_2)\,w_{31} + (w_{21}x_1 + w_{22}x_2)\,w_{32}"),
    ("eq14_expand", r"= (w_{11}w_{31} + w_{21}w_{32})\,x_1 + (w_{21}w_{31} + w_{22}w_{32})\,x_2"),
    ("eq14_linear", r"= w'_1x_1 + w'_2x_2"),
]
for name, latex in CASES:
    out = f"{BUILD}/{name}.png"
    res = subprocess.run([sys.executable, RENDER, latex, out, "18", "#000000"],
                         capture_output=True, text=True)
    if res.returncode:
        print(res.stdout, res.stderr, file=sys.stderr)
        sys.exit(res.returncode)
    print(name, res.stdout.strip())
