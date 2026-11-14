#!/usr/bin/env python3
"""Slide 030 v3 equation assets: red labels + black bodies, certified renderer + sidecars."""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RENDER = Path("/home/codespace/ai_llm_slides/scripts/render_eq.py")
FONT_PT = 12.0
RED = "#C00000"
BLACK = "#000000"

SPECS = [
    ("eq030_net3_label", r"Net_3", RED, "eq030_net3_body", r"= 7 \times 0.1 + 4 \times 0.4 = 2.3", BLACK),
    ("eq030_net4_label", r"Net_4", RED, "eq030_net4_body", r"= 7 \times 0.2 + 4 \times 0.5 = 3.4", BLACK),
    ("eq030_net5_label", r"Net_5", RED, "eq030_net5_body", r"= 7 \times 0.3 + 4 \times 0.6 = 4.5", BLACK),
    ("eq030_net6_label", r"Net_6", RED, "eq030_net6_body", r"= 0.909 \times 0.3 + 0.968 \times 0.4 + 0.989 \times 0.5 = 1.1544", BLACK),
    ("eq030_net7_label", r"Net_7", RED, "eq030_net7_body", r"= 0.909 \times 0.3 + 0.968 \times 0.4 + 0.989 \times 0.5 = 1.1544", BLACK),
    ("eq030_o3_label", r"O_3", RED, "eq030_o3_body", r"= \dfrac{1}{1+e^{-2.3}} = 0.909", BLACK),
    ("eq030_o4_label", r"O_4", RED, "eq030_o4_body", r"= \dfrac{1}{1+e^{-3.4}} = 0.968", BLACK),
    ("eq030_o5_label", r"O_5", RED, "eq030_o5_body", r"= \dfrac{1}{1+e^{-4.5}} = 0.989", BLACK),
    ("eq030_o6_label", r"O_6", RED, "eq030_o6_body", r"= \dfrac{1}{1+e^{-1.1544}} = 0.76", BLACK),
    ("eq030_o7_label", r"O_7", RED, "eq030_o7_body", r"= \dfrac{1}{1+e^{-1.1544}} = 0.76", BLACK),
]

manifest = []
for label_name, label_mt, label_color, body_name, body_mt, body_color in SPECS:
    for name, mt, color in ((label_name, label_mt, label_color), (body_name, body_mt, body_color)):
        png = HERE / f"{name}.png"
        side = HERE / f"{name}.json"
        out = subprocess.check_output(
            [sys.executable, str(RENDER), mt, str(png), str(FONT_PT), color],
            text=True,
        ).strip()
        info = json.loads(out)
        info["mathtext"] = mt
        side.write_text(json.dumps(info, indent=2) + "\n")
        manifest.append(info)

(HERE / "eq_030_v3_manifest.json").write_text(json.dumps({"equations": manifest}, indent=2) + "\n")
print(f"wrote {len(manifest)} equation assets + eq_030_v3_manifest.json")
