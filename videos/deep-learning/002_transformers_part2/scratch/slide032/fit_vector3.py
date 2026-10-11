#!/usr/bin/env python3
"""Scan strut/pad combos to hit ink ratio 91.6:73.3 = 1.2497, then fit em."""
import subprocess, json

OUT = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/eq_032_vector.png'
TW, TH = 91.6, 73.3
ENV = {'TMPDIR': '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide032',
       'PATH': '/usr/bin:/bin:/usr/local/bin', 'HOME': '/home/ahmed'}

def render(latex, size=20):
    r = subprocess.run(['python3', 'scripts/render_eq.py', latex, OUT, str(size), 'C00000'],
                       capture_output=True, text=True, cwd='/home/ahmed/Projects/ai_llm_slides', env=ENV)
    if r.returncode != 0:
        return None
    return json.loads(r.stdout.strip().splitlines()[-1])

struts = {
    'S1': '\\phantom{\\Biggl(}',
    'S2': '\\phantom{\\sum_{i=1}^{N}}',
    'S3': '\\genfrac{}{}{0}{}{\\phantom{\\Biggl(}}{\\phantom{()}}',
}
pads = {
    'P0': '',
    'P1': '\\;',
    'P2': '\\;\\;',
    'P3': '\\quad',
    'P4': '\\quad\\;',
    'P5': '\\quad\\quad',
}
best = None
for sn, sv in struts.items():
    for pn, pv in pads.items():
        latex = ('\\genfrac{[}{]}{0}{}{' + pv + '\\sin(\\omega t)' + pv + '}{'
                 '\\genfrac{}{}{0}{}{' + sv + '}{' + pv + '\\cos(\\omega t)' + pv + '}}')
        m = render(latex)
        if not m:
            print(f"{sn}/{pn}: FAIL"); continue
        w, h = m['w_in'] * 72, m['h_in'] * 72
        ratio = w / h
        tag = ''
        if abs(ratio - TW / TH) < 0.02: tag = ' <== RATIO MATCH'
        print(f"{sn}/{pn}: {w:.1f} x {h:.1f} ratio {ratio:.4f}{tag}")
