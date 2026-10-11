#!/usr/bin/env python3
"""Iterate nested-genfrac depth + fontsize to hit 91.6 x 73.3 pt ink."""
import subprocess, json
from PIL import Image
import numpy as np

OUT = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/eq_032_vector.png'
TW, TH = 91.6, 73.3
ENV = {'TMPDIR': '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide032',
       'PATH': '/usr/bin:/bin:/usr/local/bin', 'HOME': '/home/ahmed'}

def render(latex, size):
    r = subprocess.run(['python3', 'scripts/render_eq.py', latex, OUT, str(size), 'C00000'],
                       capture_output=True, text=True, cwd='/home/ahmed/Projects/ai_llm_slides', env=ENV)
    if r.returncode != 0:
        print("FAIL:", r.stderr[-200:]); return None
    return json.loads(r.stdout.strip().splitlines()[-1])

def latex_n(n, pad='\\;\\;'):
    inner = '\\;\\;\\cos(\\omega t)\\;\\;'
    for _ in range(n):
        inner = '\\genfrac{}{}{0}{}{\\phantom{()}}{' + inner + '}'
    return '\\genfrac{[}{]}{0}{}{' + pad + '\\sin(\\omega t)' + pad + '}{' + inner + '}'

for n in range(1, 7):
    m = render(latex_n(n), 20)
    if not m: continue
    w, h = m['w_in'] * 72, m['h_in'] * 72
    print(f"n={n} @20pt: {w:.1f} x {h:.1f}  (w/h {w/h:.3f}, target {TW/TH:.3f})")
