#!/usr/bin/env python3
"""Iterate the column-vector mathtext to hit target ink 91.6 x 73.3 pt (slide)."""
import subprocess, json
from PIL import Image
import numpy as np

OUT = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/eq_032_vector.png'
TW, TH = 91.6, 73.3  # target ink pt

def render(latex, size):
    r = subprocess.run(['python3', 'scripts/render_eq.py', latex, OUT, str(size), 'C00000'],
                       capture_output=True, text=True, cwd='/home/ahmed/Projects/ai_llm_slides',
                       env={'TMPDIR': '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide032', 'PATH': '/usr/bin:/bin:/usr/local/bin', 'HOME': '/home/ahmed'})
    if r.returncode != 0:
        print("RENDER FAIL:", r.stderr[-300:]); return None
    return json.loads(r.stdout.strip().splitlines()[-1])

# gap strut: phantom content height ~ tune; start with a phantom of '()()' (paren-height rows)
for strut in ['\\phantom{()}', '\\phantom{()()}', '\\genfrac{}{}{0}{}{\\phantom{()}}{\\phantom{()}}']:
    latex = '\\genfrac{[}{]}{0}{}{\\sin(\\omega t)}{' + strut.replace('PH', '') + '\\cos(\\omega t)}'
    latex = '\\genfrac{[}{]}{0}{}{\\sin(\\omega t)}{\\genfrac{}{}{0}{}{' + strut + '}{\\cos(\\omega t)}}'
    m = render(latex, 20)
    if not m: continue
    w, h = m['w_in'] * 72, m['h_in'] * 72
    print(f"strut={strut[:30]:32s} @20pt: {w:.1f} x {h:.1f} pt  (target {TW} x {TH})")
