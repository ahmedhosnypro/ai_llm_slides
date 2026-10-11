import json, subprocess, sys
RE="/home/ahmed/Projects/ai_llm_slides/.agents/skills/slide-recreation/scripts/render_eq.py"
OUT="/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets/"
PAD=16
def gen(latex, name, pt, color, tw, th, fit="max"):
    best=None
    for attempt in range(4):
        r = subprocess.run([sys.executable, RE, latex, OUT+name, str(pt), color], capture_output=True, text=True)
        if r.returncode!=0:
            print("FAIL", name, r.stderr[-300:]); return None
        info=json.loads(r.stdout)
        ink_w=(info["w_px"]-PAD)/4; ink_h=(info["h_px"]-PAD)/4
        print(f"{name} pt={pt}: ink {ink_w:.1f}x{ink_h:.1f} target {tw}x{th} basefrac {info['baseline_frac']}")
        best=info
        sw, sh = tw/ink_w, th/ink_h
        scale = max(sw,sh) if fit=="max" else sw
        if abs(scale-1)<0.06: break
        pt=round(pt*scale,1)
    return best

gen(r"w'_{ij}=x_i^T x_j","eq34_large.png",10.4,"#000000",98,26)
gen(r"w'_{ij}=x_i^T x_j","eq34_small.png",6.1,"#000000",58,16)
gen(r"w'_{ij}","eq34_wprime.png",13,"#000000",38,31)
# softmax: try genfrac tight; fit width, keep height sane
gen(r"w_{ij}=\genfrac{}{}{0.8pt}{}{\exp w'_{ij}}{\sum_j \exp w'_{ij}}","eq34_softmax.png",12,"#000000",124,48,fit="w")
gen(r"[\mathrm{X}_i]","eq34_xi.png",26,"#990000",36,44)
gen(r"[\mathrm{X}_i]","eq34_xi_sm.png",20,"#990000",31,32)
gen(r"1{\times}d","eq34_1xd.png",11,"#0E6F20",26,11)
gen(r"1{\times}d","eq34_1xd_sm.png",12,"#0E6F20",30,15)
print("---parens---")
GEN="/home/ahmed/Projects/ai_llm_slides/.agents/skills/slide-recreation/patterns/delimiters-stretched-glyph/gen_delimiter.py"
for glyph,name,span,stroke,color in [("(","paren_red_l.png",122,10,"#990000"),(")","paren_red_r.png",122,10,"#990000"),
                                     ("(","paren_blue_l.png",114,8,"#0033CC"),(")","paren_blue_r.png",114,8,"#0033CC")]:
    r=subprocess.run([sys.executable,GEN,glyph,str(span),str(stroke),color,OUT+name],capture_output=True,text=True)
    print(r.stdout.strip() or r.stderr[-200:])
