import json, subprocess, sys
SCR = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide023'
ASSETS = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets'
# name: (mathtext, color, target_ink_w_px72, target_ink_h_px72)
EQS = {
 'eq_a': (r'\mathrm{Normalized}\ \underline{\boldsymbol{a}} = \dfrac{\boldsymbol{a}}{|\boldsymbol{a}|}', '#000000', 162, 42),
 'eq_b': (r'\mathrm{Normalized}\ \underline{\boldsymbol{b}} = \dfrac{\boldsymbol{b}}{|\boldsymbol{b}|}', '#000000', 162, 47),
 'eq_dot': (r'\boldsymbol{a}.\boldsymbol{b} = \boldsymbol{a}^T\boldsymbol{b} = |\boldsymbol{a}|\,|\boldsymbol{b}|\cos(\theta)', '#000000', 224, 23),
 'cos_red': (r'\boldsymbol{\cos(\theta)}', '#CC0000', 61, 23),
 'cos_black': (r'= \dfrac{\boldsymbol{a}^T\boldsymbol{b}}{|\boldsymbol{a}|\,|\boldsymbol{b}|} = \boldsymbol{a}^T\boldsymbol{b}', '#000000', 127, 51),
 'eq_unit': (r'|\boldsymbol{a}| = |\boldsymbol{b}| = 1', '#000000', 100, 21),
}
out = {}
for name, (latex, color, tw, th) in EQS.items():
    fs = 17.0
    for it in range(3):
        r = json.loads(subprocess.run(
            [sys.executable, f'{SCR}/render_stix.py', latex, f'{ASSETS}/{name}.png', str(fs), color],
            capture_output=True, text=True).stdout)
        # ink size at 72dpi: sidecar includes PAD 8px@600dpi each side
        ink_w = (r['w_px'] - 16) / 600 * 72
        ink_h = (r['h_px'] - 16) / 600 * 72
        err = abs(ink_w - tw)
        if err <= 2.5 or it == 2:
            break
        fs = round(fs * tw / ink_w, 2)
    out[name] = dict(latex=latex, color=color, fontsize=fs, ink_w=round(ink_w,1), ink_h=round(ink_h,1),
                     target_w=tw, target_h=th, **{k: r[k] for k in ('w_px','h_px','w_in','h_in','baseline_frac')})
    print(name, 'fs=', fs, 'ink', round(ink_w,1), 'x', round(ink_h,1), 'target', tw, 'x', th)
json.dump(out, open(f'{SCR}/eq_sidecars.json','w'), indent=1)
