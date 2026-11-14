#!/usr/bin/env python3
"""Generate the 600-dpi equation PNGs and provenance sidecars for slide 020.

Each colored run is a separate asset so the OMML wrapper can carry the same
color in PowerPoint's editable math. Content is verbatim from the validated
slide spec; only rendering is professional mathtext.
"""
import json
import subprocess
import sys
from pathlib import Path

V = Path("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks")
OUT = V / "recreated_pptx/build/equations_slide_020"
RENDER = Path("/home/codespace/ai_llm_slides/scripts/render_eq.py")
OUT.mkdir(parents=True, exist_ok=True)

BLACK = "#000000"
RED = "#FF0000"
GREEN = "#00B050"
BLUE = "#0000FF"

# name, mathtext, font pt, color
SEGMENTS = [
    ("def_lhs", r"F(x)=", 11, BLACK),
    ("def_name", r"\text{Rectified Linear Unit}", 11, RED),
    ("def_eq", r"=", 11, BLACK),
    ("def_zero", r"0", 11, RED),
    ("def_cond_lt", r"\text{for }x<0", 11, GREEN),
    ("def_x", r"x", 11, RED),
    ("def_cond_gt", r"\text{for }x>0", 11, GREEN),
    ("head_lhs", r"F(x)=", 14, BLACK),
    ("head_relu", r"\text{ReLU}", 14, RED),
    ("cap_prelu_lhs", r"F(x)=", 13, BLACK),
    ("cap_prelu_parametric", r"\text{Parametric}", 13, BLUE),
    ("cap_prelu_relu", r"\text{ReLU}", 13, RED),
    ("cap_elu_lhs", r"F(x)=", 13, BLACK),
    ("cap_elu_name", r"\text{ELU}", 13, RED),
    ("cap_softplus_lhs", r"F(x)=", 13, BLACK),
    ("cap_softplus_name", r"\text{SoftPlus}", 13, RED),
]

manifest = {}
for name, mathtext, size, color in SEGMENTS:
    png = OUT / f"eq_020_{name}.png"
    sidecar = OUT / f"eq_020_{name}.json"
    proc = subprocess.run(
        [sys.executable, str(RENDER), mathtext, str(png), str(size), color],
        text=True, capture_output=True, check=True,
    )
    info = json.loads(proc.stdout.strip().splitlines()[-1])
    info["mathtext"] = mathtext
    info["name"] = name
    sidecar.write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")
    manifest[name] = info
    print(name, info["w_in"], info["h_in"], info["baseline_frac"])

(OUT / "eq_020_segments.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
