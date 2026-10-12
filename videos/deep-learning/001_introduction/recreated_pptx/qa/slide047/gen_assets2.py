#!/usr/bin/env python3
"""Generate slide_047 equation assets — pass 2 (fixed #colors, calibrated sizes).
Targets (original px, 1px=1pt):
  eq3  ink left 317, baseline ~303.5, band 284..312 (w 220) — 2D upgrade ok
  eq4  ink left 320, bar y 337, stack h target ~38-39, w 164
  frac ink left 775, bar y 427, stack h target ~45 (405..449), w 16
"""
import json, subprocess, sys

SKILL = "/home/ahmed/Projects/ai_llm_slides/.agents/skills/slide-recreation/scripts/render_eq.py"
ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets"

EQ3 = r"a_{r,c} \,=\, \dfrac{1}{r\cdot c}\,\sum_{i,j\in\Omega(r,c)} x_{ij}"
EQ4 = r"\dfrac{\partial a_{r,c}}{\partial x_{ij}} \,=\, \dfrac{1}{r\cdot c}"
FR = r"\dfrac{1}{2}"

def render(latex, out, fs, color):
    r = subprocess.run([sys.executable, SKILL, latex, out, str(fs), color],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL", out, r.stderr[-300:]); return None
    return json.loads(r.stdout)

def show(nm, i, target_h=None, target_w=None):
    if not i: return
    dw, dh = i["w_px"]/600*72, i["h_px"]/600*72
    extra = ""
    if target_h: extra += f" (target h {target_h} -> fs {i['fontsize_pt']*target_h/dh:.1f})"
    if target_w: extra += f" (target w {target_w} -> fs {i['fontsize_pt']*target_w/dw:.1f})"
    print(f"{nm}: {i['w_px']}x{i['h_px']}px -> {dw:.1f}x{dh:.1f}pt, base_frac {i['baseline_frac']}{extra}")

i3 = render(EQ3, f"{ASSETS}/eq_047_act.png", 17, "#333333")
i4 = render(EQ4, f"{ASSETS}/eq_047_grad.png", 17, "#333333")
iF = render(FR,  f"{ASSETS}/eq_047_half.png", 19.5, "#C00000")
show("eq3", i3, target_w=220)
show("eq4", i4, target_h=38.5, target_w=164)
show("frac", iF, target_h=45, target_w=16)
