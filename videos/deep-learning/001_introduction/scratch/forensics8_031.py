from PIL import ImageFont
words = [("Where",105),("to",30),("Get",56),("Filters",101),("for",45),("Recognition",199)]
FONTS = {
 "Serif-Bold": ("/usr/share/fonts/liberation/LiberationSerif-Bold.ttf", 38.3),
 "Sans-Bold": ("/usr/share/fonts/liberation/LiberationSans-Bold.ttf", 34.9),
}
for fname,(path,fs) in FONTS.items():
    f = ImageFont.truetype(path, 80)
    errs = [(w, round(f.getlength(w)*fs/80.0 - meas,1)) for w,meas in words]
    sse = sum((e[1]/e[0] if False else 0) for e in [])  # noop
    rel = sum(((f.getlength(w)*fs/80.0-m)**2)/m**2 for w,m in words)
    print(f"{fname}: title relSSE={rel:.4f} errs(px) {errs}")
# L2 'For example:' word check at body fs
for fname,(path,fs) in {"Serif-Bold":("/usr/share/fonts/liberation/LiberationSerif-Bold.ttf",22.9),"Sans-Bold":("/usr/share/fonts/liberation/LiberationSans-Bold.ttf",20.7)}.items():
    f = ImageFont.truetype(path, 80)
    for w,m in [("For",35),("example:",89)]:
        print(f"{fname} L2 {w}: pred {f.getlength(w)*fs/80.0:.0f} meas {m}")
