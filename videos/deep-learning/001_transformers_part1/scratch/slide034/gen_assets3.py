import json, subprocess, sys
RE="/home/ahmed/Projects/ai_llm_slides/.agents/skills/slide-recreation/scripts/render_eq.py"
OUT="/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets/"
PAD=16
def render(latex, name, pt, color):
    r = subprocess.run([sys.executable, RE, latex, OUT+name, str(pt), color], capture_output=True, text=True)
    if r.returncode!=0: print("FAIL",name,r.stderr.strip().splitlines()[-1][:160]); return None
    info=json.loads(r.stdout)
    print(f"{name} '{latex}' pt={pt}: ink {(info['w_px']-PAD)/4:.1f}x{(info['h_px']-PAD)/4:.1f} basefrac {info['baseline_frac']}")
    return info
# xi variants
for ltx,pt in [(r"[\!\mathrm{X}_i\!]",23),(r"[\!\mathrm{X}_i\!]",20),(r"[\,\mathrm{X}_i\,]",20)]:
    render(ltx,"t_xi.png",pt,"#990000")
# exp pieces for manual fraction
i1=render(r"\exp w'_{ij}","eq34_exp1.png",10,"#000000")
i2=render(r"\sum_j\,\exp w'_{ij}","eq34_exp2.png",10,"#000000")
i0=render(r"w_{ij}=","eq34_wij.png",13,"#000000")
render(r"\exp w'_{ij}","eq34_exp1_sm.png",9,"#000000")
render(r"\sum_j\,\exp w'_{ij}","eq34_exp2_sm.png",9,"#000000")
render(r"w_{ij}=","eq34_wij_sm.png",12,"#000000")
