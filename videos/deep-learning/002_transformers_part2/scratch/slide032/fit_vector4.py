#!/usr/bin/env python3
"""Fit the three vector-piece images: brackets, sin, cos."""
import subprocess, json

A = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/'
ENV = {'TMPDIR': '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide032',
       'PATH': '/usr/bin:/bin:/usr/local/bin', 'HOME': '/home/ahmed'}

def render(name, latex, size):
    r = subprocess.run(['python3', 'scripts/render_eq.py', latex, A + name, str(size), 'C00000'],
                       capture_output=True, text=True, cwd='/home/ahmed/Projects/ai_llm_slides', env=ENV)
    if r.returncode != 0:
        print("FAIL", name, r.stderr[-200:]); return None
    return json.loads(r.stdout.strip().splitlines()[-1])

# bracket pair: target ink h 73.3pt
m = render('eq_032_vec_brk.png', r'\left[\vphantom{\sum_{i=1}^{N}}\right]', 20)
print("brackets @20:", m['w_in'] * 72, m['h_in'] * 72, "baseline_frac", m['baseline_frac'])
em_b = 20 * 73.3 / (m['h_in'] * 72)
print("em for brackets:", round(em_b, 2))
m2 = render('eq_032_vec_brk.png', r'\left[\vphantom{\sum_{i=1}^{N}}\right]', round(em_b))
print("brackets fitted:", m2['w_in'] * 72, m2['h_in'] * 72, "baseline_frac", m2['baseline_frac'])

# sin / cos rows: target ink h (parens) 12.6pt, ink w 61.3pt
m = render('eq_032_vec_sin.png', r'\sin(\omega t)', 14)
print("sin @14:", m['w_in'] * 72, m['h_in'] * 72, "baseline_frac", m['baseline_frac'])
em_s = 14 * 12.6 / (m['h_in'] * 72)
print("em for rows:", round(em_s, 2))
m2 = render('eq_032_vec_sin.png', r'\sin(\omega t)', round(em_s, 1))
print("sin fitted:", m2['w_in'] * 72, m2['h_in'] * 72, "baseline_frac", m2['baseline_frac'])
m3 = render('eq_032_vec_cos.png', r'\cos(\omega t)', round(em_s, 1))
print("cos fitted:", m3['w_in'] * 72, m3['h_in'] * 72, "baseline_frac", m3['baseline_frac'])
