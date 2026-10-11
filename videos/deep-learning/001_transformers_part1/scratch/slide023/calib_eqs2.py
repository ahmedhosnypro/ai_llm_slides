import json, subprocess, sys
SCR = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide023'
ASSETS = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets'
EQS = {
 'eq_a': (r'\mathit{Normalized}\ \underline{\boldsymbol{a}} = \dfrac{\boldsymbol{a}}{|\boldsymbol{a}|}', '#000000', 162, 42),
 'eq_b': (r'\mathit{Normalized}\ \underline{\boldsymbol{b}} = \dfrac{\boldsymbol{b}}{|\boldsymbol{b}|}', '#000000', 162, 47),
 'eq_unit': (r'|\underline{\boldsymbol{a}}| = |\underline{\boldsymbol{b}}| = 1', '#000000', 100, 21),
}
out = json.load(open(f'{SCR}/eq_sidecars.json'))
for name, (latex, color, tw, th) in EQS.items():
    fs = out[name]['fontsize'] if name in out else 21.0
    for it in range(4):
        r = json.loads(subprocess.run(
            [sys.executable, f'{SCR}/render_stix.py', latex, f'{ASSETS}/{name}.png', str(fs), color],
            capture_output=True, text=True).stdout)
        ink_w = (r['w_px'] - 16) / 600 * 72
        ink_h = (r['h_px'] - 16) / 600 * 72
        if abs(ink_w - tw) <= 2.5 or it == 3:
            break
        fs = round(fs * tw / ink_w, 2)
    out[name] = dict(latex=latex, color=color, fontsize=fs, ink_w=round(ink_w,1), ink_h=round(ink_h,1),
                     target_w=tw, target_h=th, **{k: r[k] for k in ('w_px','h_px','w_in','h_in','baseline_frac')})
    print(name, 'fs=', fs, 'ink', round(ink_w,1), 'x', round(ink_h,1), 'target', tw, 'x', th)
json.dump(out, open(f'{SCR}/eq_sidecars.json','w'), indent=1)
