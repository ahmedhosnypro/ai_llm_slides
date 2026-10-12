#!/usr/bin/env python3
"""Generate slide_047 equation assets (mathtext -> 600dpi PNG) + crop the arrow.
Targets (original-frame px, 1px=1pt):
  eq3  ink left 317, math baseline ~303.5, band y 284..312 (upgraded 2D render ok)
  eq4  ink left 320, fraction bar y ~337, stack h target 38-39 (y 321..359), w 164
  frac red 1/2: ink left 795, bar y ~439, stack h target 29 (y 425..453), w 38
"""
import json, subprocess, sys
from PIL import Image
import numpy as np

SKILL = "/home/ahmed/Projects/ai_llm_slides/.agents/skills/slide-recreation/scripts/render_eq.py"
ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets"

EQ3 = r"a_{r,c} \,=\, \dfrac{1}{r\cdot c}\,\sum_{i,j\in\Omega(r,c)} x_{ij}"
EQ4 = r"\dfrac{\partial a_{r,c}}{\partial x_{ij}} \,=\, \dfrac{1}{r\cdot c}"
FR = r"\dfrac{1}{2}"

def render(latex, out, fs, color):
    r = subprocess.run([sys.executable, SKILL, latex, out, str(fs), color],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL", out, r.stderr[-500:]); return None
    return json.loads(r.stdout)

# --- first pass: probe sizes ---
info3 = render(EQ3, f"{ASSETS}/eq_047_act.png", 17, "333333")
info4 = render(EQ4, f"{ASSETS}/eq_047_grad.png", 17, "333333")
infof = render(FR,  f"{ASSETS}/eq_047_half.png", 14, "C00000")
for nm, i in [("eq3", info3), ("eq4", info4), ("frac", infof)]:
    if i:
        disp_w, disp_h = i["w_px"]/600*72, i["h_px"]/600*72
        print(f"{nm}: {i['w_px']}x{i['h_px']}px -> displayed {disp_w:.1f}x{disp_h:.1f}pt "
              f"baseline_frac {i['baseline_frac']}")
