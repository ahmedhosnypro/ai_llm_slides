import json, subprocess, sys
RE="/home/ahmed/Projects/ai_llm_slides/.agents/skills/slide-recreation/scripts/render_eq_stix.py"
OUT="/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets/"
def gen(latex, name, pt, color):
    r = subprocess.run([sys.executable, RE, latex, OUT+name, str(pt), color], capture_output=True, text=True)
    if r.returncode!=0: print("FAIL",name,r.stderr.strip().splitlines()[-1][:150]); return
    info=json.loads(r.stdout)
    json.dump(info, open(OUT+name.replace(".png",".json"),"w"), indent=1)
    print(f"{name} pt={pt}: ink@150 {(info['w_px']-16)/4:.1f}x{(info['h_px']-16)/4:.1f}px = {(info['w_px']-16)/150*72:.1f}x{(info['h_px']-16)/150*72:.1f}pt basefrac {info['baseline_frac']}")
# targets in PT -> font = old_pt * 2.0833 (px@150 vs pt unit bug)
gen(r"w'_{ij}=x_i^T x_j","eq34_large.png",25,"#000000")      # 98x26pt
gen(r"w'_{ij}=x_i^T x_j","eq34_small.png",14.6,"#000000")    # 58x16pt
gen(r"w'_{ij}","eq34_wprime.png",27,"#000000")               # 38x31pt
gen(r"w_{ij}=","eq34_wij.png",24.4,"#000000")                # 40x18pt
gen(r"\exp w'_{ij}","eq34_exp1.png",17.5,"#000000")          # 52x17pt
gen(r"\Sigma_j \exp w'_{ij}","eq34_exp2.png",20.8,"#000000") # 78x21pt
gen(r"\mathrm{X}_i","eq34_xi_core.png",27,"#990000")         # X cap 18pt
gen(r"[","eq34_bracket_l.png",53.5,"#990000")                # 44pt tall
gen(r"]","eq34_bracket_r.png",53.5,"#990000")
gen(r"\mathrm{X}_i","eq34_xi_core_sm.png",19.7,"#990000")    # X cap 13pt
gen(r"[","eq34_bracket_l_sm.png",38.7,"#990000")             # 32pt tall
gen(r"]","eq34_bracket_r_sm.png",38.7,"#990000")
