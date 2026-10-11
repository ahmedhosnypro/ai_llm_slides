from PIL import ImageFont
import glob

candidates = {}
for pat, name in [("/usr/share/fonts/**/LiberationSans-Bold.ttf","LiberationSans-Bold"),
                  ("/usr/share/fonts/**/DejaVuSans-Bold.ttf","DejaVuSans-Bold"),
                  ("/usr/share/fonts/**/Arial*.ttf","Arial"),
                  ("/usr/share/fonts/**/Verdana*.ttf","Verdana"),
                  ("/usr/share/fonts/**/Calibri*.ttf","Calibri")]:
    hits = glob.glob(pat, recursive=True)
    if hits: candidates[name] = hits[0]
print("fonts found:", candidates)

strings = {
 "L1": ("Processing Sequential Data", 259),
 "L2": ("Transformer Building Blocks", 270),
 "L3": ("Self Attention Mechanism", 239),
 "L4": ("Multi-Head  Attention", 198),
 "TITLE": ("Transformers \u2013 Part I", 398),
}
# For each font, find best-fit size for L2 (largest body line), then report all lines + title size
for name, path in candidates.items():
    # fit size to L2 = 270 px advance (ink ≈ advance - bearings ~ 97% of advance)
    lo, hi = 8, 40
    best = None
    for size10 in range(80, 400):
        size = size10/10
        f = ImageFont.truetype(path, int(round(size*4)))  # 4x for precision
        w = f.getbbox("Transformer Building Blocks")[2] - f.getbbox("Transformer Building Blocks")[0]
        if abs(w/4 - 270) < 1.5:
            best = size; break
    if best is None:
        # fallback: compute width at 20pt and scale
        f = ImageFont.truetype(path, 80)
        bb = f.getbbox("Transformer Building Blocks")
        w20 = (bb[2]-bb[0])/80*20
        best = 20*270/w20
    print(f"\n== {name}: fit size for L2=270px -> {best:.2f}pt ==")
    for k,(s,target) in strings.items():
        size = best if k!="TITLE" else best*2  # title ~2x body
        f = ImageFont.truetype(path, int(round(size*4)))
        bb = f.getbbox(s)
        w = (bb[2]-bb[0])/4
        print(f"  {k}: width at {size:.1f}pt = {w:.0f}px (target {target})")
    # cap height at best size
    f = ImageFont.truetype(path, int(round(best*4)))
    bb = f.getbbox("T")
    print(f"  cap height at {best:.1f}pt = {(bb[3]-bb[1])/4:.1f}px (target ~15)")
    bb2 = f.getbbox("T")
