#!/usr/bin/env python3
"""Audit driver: pdftoppm 150dpi + house chrome check + badge OCR per certified slide.
Writes only inside scratch/audit_001i/. Appends results to chrome_badge_results.txt."""
import os, subprocess, sys

ROOT = "/home/ahmed/Projects/ai_llm_slides"
REN = f"{ROOT}/scratch/audit_001i/renders"
CHK = f"{ROOT}/videos/deep-learning/shared_patterns/house_chrome_check.py"
OUT = f"{ROOT}/scratch/audit_001i/chrome_badge_results.txt"
CERT = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,26,27,28,29,30,
        31,32,33,34,35,36,37,38,39,40,41,42,43,44,46,47,48,49]

def render(n):
    pdf = f"{REN}/slide_{n:03d}_recreated.pdf"
    png = f"{REN}/c{n:03d}"
    if not os.path.exists(png + "-1.png"):
        r = subprocess.run(["pdftoppm", "-r", "150", "-png", pdf, png], capture_output=True, text=True)
        if r.returncode != 0:
            return None, f"pdftoppm failed: {r.stderr.strip()[:100]}"
    return png + "-1.png", None

def ocr_badge(png):
    from PIL import Image
    im = Image.open(png).convert("L")
    W, H = im.size
    sc = H / 540.0
    cx, cy, d = 893 * sc, 71 * sc, 36 * sc
    box = im.crop((int(cx - d*0.45), int(cy - d*0.45), int(cx + d*0.45), int(cy + d*0.45)))
    box = box.resize((box.width * 8, box.height * 8), Image.LANCZOS)
    bw = box.point(lambda p: 0 if p < 140 else 255)
    bw.save(f"{ROOT}/scratch/audit_001i/badge_tmp.png")
    votes = []
    for psm in (7, 10, 6):
        r = subprocess.run(["tesseract", f"{ROOT}/scratch/audit_001i/badge_tmp.png", "-", "--psm", str(psm),
                            "-c", "tessedit_char_whitelist=0123456789"], capture_output=True, text=True)
        t = r.stdout.strip().replace(" ", "")
        if t:
            votes.append(t)
    return votes

def main():
    with open(OUT, "a") as f:
        for n in CERT:
            png, err = render(n)
            if err:
                f.write(f"S{n} RENDER-FAIL {err}\n"); f.flush(); continue
            c = subprocess.run([sys.executable, CHK, png, str(n)], capture_output=True, text=True)
            chrome = "PASS" if c.returncode == 0 else "FAIL:" + " / ".join(l.strip() for l in c.stdout.splitlines()[1:3])
            votes = ocr_badge(png)
            ok = all(v == str(n) for v in votes) and votes
            badge = "OK" if ok else f"MISMATCH votes={votes} expected={n}"
            f.write(f"S{n} chrome={chrome} badge={badge}\n"); f.flush()
    print("done")

if __name__ == "__main__":
    main()
