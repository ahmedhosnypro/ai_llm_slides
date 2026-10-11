import json, subprocess, sys
RE="/home/ahmed/Projects/ai_llm_slides/.agents/skills/slide-recreation/scripts/render_eq_stix.py"
OUT="/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets/"
PAD=16
def gen(latex, name, pt, color, tw=None, th=None, fit="max"):
    best=None
    for attempt in range(4):
        r = subprocess.run([sys.executable, RE, latex, OUT+name, str(pt), color], capture_output=True, text=True)
        if r.returncode!=0: print("FAIL",name,r.stderr.strip().splitlines()[-1][:150]); return None
        info=json.loads(r.stdout)
        ink_w=(info["w_px"]-PAD)/4; ink_h=(info["h_px"]-PAD)/4
        tgt=f" target {tw}x{th}" if tw else ""
        print(f"{name} pt={pt}: ink {ink_w:.1f}x{ink_h:.1f}{tgt} basefrac {info['baseline_frac']}")
        best=info
        if tw is None: break
        sw,sh = tw/ink_w, th/ink_h
        scale = max(sw,sh) if fit=="max" else sw
        if abs(scale-1)<0.06: break
        pt=round(pt*scale,1)
    return best

gen(r"w'_{ij}=x_i^T x_j","eq34_large.png",12,"#000000",98,26)
gen(r"w'_{ij}=x_i^T x_j","eq34_small.png",7,"#000000",58,16)
gen(r"w'_{ij}","eq34_wprime.png",13,"#000000",38,31)
gen(r"w_{ij}=","eq34_wij.png",13,"#000000",40,18)
gen(r"\exp w'_{ij}","eq34_exp1.png",10,"#000000",52,17)
gen(r"\sum_j \exp w'_{ij}","eq34_exp2.png",10,"#000000",78,21)
gen(r"[\mathrm{X}_i]","eq34_xi.png",26,"#990000",36,44)
gen(r"[\mathrm{X}_i]","eq34_xi_sm.png",20,"#990000",31,32)
