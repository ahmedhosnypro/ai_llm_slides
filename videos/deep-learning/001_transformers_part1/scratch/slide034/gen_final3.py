import json, subprocess, sys
RE="/home/ahmed/Projects/ai_llm_slides/.agents/skills/slide-recreation/scripts/render_eq_stix.py"
OUT="/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets/"
def gen(latex, name, pt, color):
    r = subprocess.run([sys.executable, RE, latex, OUT+name, str(pt), color], capture_output=True, text=True)
    if r.returncode!=0: print("FAIL",name,r.stderr.strip().splitlines()[-1][:150]); return
    info=json.loads(r.stdout)
    json.dump(info, open(OUT+name.replace(".png",".json"),"w"), indent=1)
    print(f"{name} pt={pt}: ink {(info['w_px']-16)/150*72:.1f}x{(info['h_px']-16)/150*72:.1f}pt basefrac {info['baseline_frac']}")
gen(r"\mathrm{X}","eq34_xonly.png",27,"#990000")
gen(r"i","eq34_isub.png",9.5,"#990000")
gen(r"\mathrm{X}","eq34_xonly_sm.png",19.7,"#990000")
gen(r"i","eq34_isub_sm.png",7.5,"#990000")
gen(r"w","eq34_w.png",24,"#000000")
gen(r"'{ij}","eq34_prij.png",13,"#000000")
gen(r"w_{ij}=","eq34_wij.png",20,"#000000")
