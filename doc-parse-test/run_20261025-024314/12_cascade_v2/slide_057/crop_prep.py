import sys, json, os
from PIL import Image
SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_057.jpg"
im = Image.open(SRC).convert("RGB")
W, H = im.size  # 960x540
out = []
for spec in json.load(open(sys.argv[1])):
    name, box, scale, prov, level = spec["name"], spec["box"], spec["scale"], spec["provenance"], spec["level"]
    x0, y0, x1, y1 = box
    mx, my = (x1-x0)*0.04, (y1-y0)*0.04
    cx0, cy0 = max(0, int(round(x0-mx))), max(0, int(round(y0-my)))
    cx1, cy1 = min(W, int(round(x1+mx))), min(H, int(round(y1+my)))
    c = im.crop((cx0, cy0, cx1, cy1))
    cw, ch = c.size
    up = c.resize((cw*scale, ch*scale), Image.LANCZOS)
    d = os.path.dirname(os.path.abspath(sys.argv[2]))
    p = os.path.join(d, f"{name}.png")
    up.save(p)
    from PIL import ImageStat
    mean = sum(ImageStat.Stat(up).mean)/3
    rec = dict(id=name, provenance=prov, level=level, box=[cx0,cy0,cx1,cy1],
               source_box=box, scale=scale, crop_px=[up.size[0],up.size[1]],
               mean=round(mean,1), transform="frame_x = crop_x/scale + box.x0; frame_y = crop_y/scale + box.y0",
               precheck="ok" if (up.size[0]>0 and mean>1) else "FAIL")
    out.append(rec)
json.dump(out, open(sys.argv[2], "w"), indent=1)
for r in out: print(r["id"], r["box"], f"s{r['scale']}", r["crop_px"], "mean", r["mean"], r["precheck"])
