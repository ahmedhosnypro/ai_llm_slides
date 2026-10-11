import json, subprocess, sys
RE="/home/ahmed/Projects/ai_llm_slides/.agents/skills/slide-recreation/scripts/render_eq_stix.py"
OUT="/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets/"
PAD=16
def gen(latex, name, pt, color, tw=None, th=None, fit="max"):
    for attempt in range(4):
        r = subprocess.run([sys.executable, RE, latex, OUT+name, str(pt), color], capture_output=True, text=True)
        if r.returncode!=0: print("FAIL",name,r.stderr.strip().splitlines()[-1][:150]); return None
        info=json.loads(r.stdout)
        ink_w=(info["w_px"]-PAD)/4; ink_h=(info["h_px"]-PAD)/4
        print(f"{name} pt={pt}: ink {ink_w:.1f}x{ink_h:.1f} target {tw}x{th} basefrac {info['baseline_frac']}")
        if tw is None: return info
        sw,sh = tw/ink_w, th/ink_h
        scale = max(sw,sh) if fit=="max" else sh
        if abs(scale-1)<0.06: return info
        pt=round(pt*scale,1)
    return info
# concept-size pieces: X cap 18px -> F=13; brackets 44px tall
gen(r"\mathrm{X}_i","eq34_xi_core.png",13,"#990000",20,26)
gen(r"[","eq34_bracket_l.png",20,"#990000",None,None)
gen(r"]","eq34_bracket_r.png",20,"#990000",None,None)
# small: brackets 32px tall, X cap ~13
gen(r"\mathrm{X}_i","eq34_xi_core_sm.png",9.5,"#990000",15,19)
gen(r"[","eq34_bracket_l_sm.png",14.5,"#990000",None,None)
gen(r"]","eq34_bracket_r_sm.png",14.5,"#990000",None,None)
