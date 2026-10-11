import json, subprocess, sys
RE="/home/ahmed/Projects/ai_llm_slides/.agents/skills/slide-recreation/scripts/render_eq.py"
OUT="/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets/"
PAD=16  # 8px pad each side at 600dpi

def gen(latex, name, pt, color, target_ink_px):
    # target_ink_px = (w,h) @150dpi
    tw, th = target_ink_px
    best=None
    for attempt in range(3):
        r = subprocess.run([sys.executable, RE, latex, OUT+name, str(pt), color],
                           capture_output=True, text=True)
        if r.returncode!=0:
            print("FAIL", name, r.stderr[-300:]); return None
        info=json.loads(r.stdout)
        ink_w=(info["w_px"]-PAD)/4; ink_h=(info["h_px"]-PAD)/4
        print(f"{name} pt={pt}: ink@150 {ink_w:.1f}x{ink_h:.1f} target {tw}x{th} basefrac {info['baseline_frac']}")
        best=info
        scale=max(tw/ink_w, th/ink_h)
        if abs(scale-1)<0.06: break
        pt=round(pt*scale,1)
    return best

res={}
res['eq_large']=gen(r"w'_{ij}=x_i^{\mathsf{T}}x_j","eq34_large.png",20,"000000",(98,26))
res['eq_small']=gen(r"w'_{ij}=x_i^{\mathsf{T}}x_j","eq34_small.png",11,"000000",(58,16))
res['eq_softmax']=gen(r"w_{ij}=\dfrac{\exp w'_{ij}}{\sum_j \exp w'_{ij}}","eq34_softmax.png",12,"000000",(124,48))
res['eq_wprime']=gen(r"w'_{ij}","eq34_wprime.png",13,"000000",(38,20))
res['xi']=gen(r"[\mathrm{X}_i]","eq34_xi.png",26,"990000",(36,44))
res['xi_sm']=gen(r"[\mathrm{X}_i]","eq34_xi_sm.png",20,"990000",(31,32))
res['sub1xd']=gen(r"1{\times}d","eq34_1xd.png",11,"0E6F20",(26,11))
res['sub1xd_sm']=gen(r"1{\times}d","eq34_1xd_sm.png",12,"0E6F20",(30,15))
json.dump({k:(v if v is None else {kk:v[kk] for kk in ("path","w_px","h_px","w_in","h_in","baseline_frac","fontsize_pt")}) for k,v in res.items()},
          open("eq_sidecars.json","w"), indent=1)
print("DONE")
