import json, subprocess, sys
RE="/home/ahmed/Projects/ai_llm_slides/.agents/skills/slide-recreation/scripts/render_eq_stix.py"
OUT="/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets/"
PAD=16
sidecars={}
def gen(latex, name, pt, color):
    r = subprocess.run([sys.executable, RE, latex, OUT+name, str(pt), color], capture_output=True, text=True)
    if r.returncode!=0: print("FAIL",name,r.stderr.strip().splitlines()[-1][:150]); return
    info=json.loads(r.stdout)
    json.dump(info, open(OUT+name.replace(".png",".json"),"w"), indent=1)
    sidecars[name]=info
    print(f"{name} pt={pt}: ink {(info['w_px']-PAD)/4:.1f}x{(info['h_px']-PAD)/4:.1f} basefrac {info['baseline_frac']}")
gen(r"\mathrm{X}_i","eq34_xi_core.png",13,"#990000")
gen(r"[","eq34_bracket_l.png",25.7,"#990000")
gen(r"]","eq34_bracket_r.png",25.7,"#990000")
gen(r"\mathrm{X}_i","eq34_xi_core_sm.png",9.5,"#990000")
gen(r"[","eq34_bracket_l_sm.png",18.6,"#990000")
gen(r"]","eq34_bracket_r_sm.png",18.6,"#990000")
# bank sidecars for the earlier finals (re-render deterministically at their calibrated pts)
gen(r"w'_{ij}=x_i^T x_j","eq34_large.png",12,"#000000")
gen(r"w'_{ij}=x_i^T x_j","eq34_small.png",7,"#000000")
gen(r"w'_{ij}","eq34_wprime.png",13,"#000000")
gen(r"w_{ij}=","eq34_wij.png",11.7,"#000000")
gen(r"\exp w'_{ij}","eq34_exp1.png",8.4,"#000000")
gen(r"\Sigma_j \exp w'_{ij}","eq34_exp2.png",10,"#000000")
