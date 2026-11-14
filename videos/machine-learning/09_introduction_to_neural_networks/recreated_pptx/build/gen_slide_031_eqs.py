#!/usr/bin/env python3
import json
import os
import subprocess
import sys

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
RENDER_EQ = "/home/codespace/ai_llm_slides/scripts/render_eq.py"

EQUATIONS = [
    ("eq_net3.png", r"Net_3 = 7 \times 0.121 + 4 \times 0.405 = 2.146", 18),
    ("eq_net4.png", r"Net_4 = 7 \times 0.101 + 4 \times 0.305 = 1.626", 18),
    ("eq_net5.png", r"Net_5 = 7 \times 0.099 + 4 \times 0.295 = 1.574", 18),
    ("eq_net6.png", r"Net_6 = 0.895 \times (-0.399) + 0.836 \times (-0.288) + 0.828 \times (-0.187) = -0.753", 12),
    ("eq_net7.png", r"Net_7 = 0.895 \times 0.598 + 0.836 \times 0.696 + 0.828 \times 0.795 = 1.775", 12),
    ("eq_O3.png", r"O_3 = \dfrac{1}{1 + e^{2.146}} = 0.895", 16),
    ("eq_O4.png", r"O_4 = \dfrac{1}{1 + e^{1.626}} = 0.836", 16),
    ("eq_O5.png", r"O_5 = \dfrac{1}{1 + e^{1.574}} = 0.828", 16),
    ("eq_O6.png", r"O_6 = \dfrac{1}{1 + e^{-0.753}} = .32", 16),
    ("eq_O7.png", r"O_7 = \dfrac{1}{1 + e^{1.775}} = 0.855", 16),
]

for name, mathtext, fontsize in EQUATIONS:
    out = os.path.join(OUT_DIR, name)
    proc = subprocess.run(
        [sys.executable, RENDER_EQ, mathtext, out, str(fontsize), "#000000"],
        capture_output=True, text=True, check=True,
    )
    info = json.loads(proc.stdout.strip().splitlines()[-1])
    info["mathtext"] = mathtext
    with open(os.path.join(OUT_DIR, name.replace(".png", ".json")), "w") as f:
        json.dump(info, f, indent=2)
    print(name, info["w_px"], info["h_px"], info["w_in"], info["h_in"])
