#!/usr/bin/env python3
# page_compare.py — dpi-agnostic PIL compare used by run_final_merge.sh step 4.
# Both PNGs are RGB-converted; if sizes differ the reference is resized to the
# render's size with LANCZOS. A pixel differs when any channel abs-diff > TOL;
# a page passes when differing px < PASS_FRAC of total.
# Usage: page_compare.py A.png B.png  -> prints "STATUS<TAB>detail" for one pair
#        page_compare.py --batch RENDER_DIR REF_DIR OUT.tsv -> page_compare.tsv + summary
import os, sys
from PIL import Image, ImageChops

TOL = 8
PASS_FRAC = 0.005

def load_pair(a_path, b_path):
    a = Image.open(a_path).convert("RGB")
    b = Image.open(b_path).convert("RGB")
    if b.size != a.size:
        b = b.resize(a.size, Image.LANCZOS)
    return a, b

def diff_count(a_path, b_path):
    a, b = load_pair(a_path, b_path)
    d = ImageChops.difference(a, b).point(lambda v: 255 if v > TOL else 0).convert("L")
    return a.size[0] * a.size[1] - d.histogram()[0]

def status_detail(a_path, b_path):
    n = diff_count(a_path, b_path)
    sa, sb = Image.open(a_path).size, Image.open(b_path).size
    total = sa[0] * sa[1]
    detail = f"diff_px={n} pct={100.0*n/total:.4f}% size={sa[0]}x{sa[1]} vs {sb[0]}x{sb[1]}"
    if n == 0:
        return "IDENTICAL", detail
    return ("PASS", detail) if n < PASS_FRAC * total else ("DIFF", detail)

def batch(rdir, refdir, out):
    rows = []
    for n in range(1, 56):
        s = f"{n:03d}"
        cands = sorted(f for f in os.listdir(rdir) if f.startswith("page-")
                       and f.endswith(".png") and f[5:-4].isdigit() and int(f[5:-4]) == n)
        ref = os.path.join(refdir, f"slide_{s}.png")
        if not cands:
            rows.append((s, "MISSING_PAGE", "")); continue
        if not os.path.exists(ref):
            rows.append((s, "SKIP_NO_REF", "")); continue
        st, det = status_detail(os.path.join(rdir, cands[0]), ref)
        rows.append((s, st, det))
    with open(out, "w") as f:
        f.write("slide\tstatus\tdetail\n")
        for r in rows:
            f.write("\t".join(r) + "\n")
    n_id = sum(1 for r in rows if r[1] == "IDENTICAL")
    n_pass = sum(1 for r in rows if r[1] == "PASS")
    n_bad = sum(1 for r in rows if r[1] in ("DIFF", "DIFF_SIZE", "MISSING_PAGE"))
    n_skip = sum(1 for r in rows if r[1] == "SKIP_NO_REF")
    print(f"page-compare: {n_id} identical, {n_pass} pass(tol), {n_bad} diff/missing, {n_skip} skipped")

if __name__ == "__main__":
    if sys.argv[1] == "--batch":
        batch(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        st, det = status_detail(sys.argv[1], sys.argv[2])
        print(f"{st}\t{det}")
