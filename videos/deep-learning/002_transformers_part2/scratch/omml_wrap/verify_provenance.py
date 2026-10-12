#!/usr/bin/env python3
"""verify_provenance.py — OMML wrap pre-check: prove each equation PNG's mathtext
provenance by re-rendering with the certified renderer and PIL-comparing 0-diff
against the banked build asset. Never writes into build/assets."""
import json, os, subprocess, sys
import numpy as np
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides"
VID = f"{ROOT}/videos/deep-learning/002_transformers_part2"
ASSETS = f"{VID}/recreated_pptx/build/assets"
OUT = f"{VID}/scratch/omml_wrap/rerender"
TMP = f"{VID}/scratch/omml_wrap/tmp"
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)

BASE_ENV = dict(os.environ, TMPDIR=TMP, MPLCONFIGDIR=TMP)

def render_eq(latex, out, fs, color, matplotlibrc=None):
    env = dict(BASE_ENV)
    if matplotlibrc:
        env["MATPLOTLIBRC"] = matplotlibrc
    r = subprocess.run([sys.executable, f"{ROOT}/scripts/render_eq.py", latex, out,
                        str(fs), color], capture_output=True, text=True, env=env)
    if r.returncode != 0:
        return None, r.stderr.strip().splitlines()[-1] if r.stderr else "fail"
    return json.loads(r.stdout), None

def pil_cmp(a, b):
    A = np.asarray(Image.open(a).convert("RGBA")); B = np.asarray(Image.open(b).convert("RGBA"))
    if A.shape != B.shape:
        return False, f"shape {A.shape} vs {B.shape}"
    d = (A != B).any(axis=-1)
    return (not d.any()), int(d.sum())

def verify(name, latex, color, fs, matplotlibrc=None, scan=0.06, step=0.004):
    """Render candidates; return (proven, fs_found, detail)."""
    banked = f"{ASSETS}/{name}.png"
    tgt = Image.open(banked); tw, th = tgt.size
    # pass 1: linear-scaled fs estimate
    fs_try = fs
    for it in range(6):
        out = f"{OUT}/{name}.png"
        info, err = render_eq(latex, out, round(fs_try, 4), color, matplotlibrc)
        if info is None:
            return False, None, f"render fail: {err}"
        if info["w_px"] == tw and info["h_px"] == th:
            ok, n = pil_cmp(out, banked)
            if ok:
                return True, round(fs_try, 4), "exact (linear fit)"
            # size matches but bytes differ -> fine scan around
            for dfs in np.arange(-scan, scan + 1e-9, step):
                fs2 = round(fs_try + float(dfs), 4)
                if abs(fs2 - fs_try) < 1e-9: continue
                out2 = f"{OUT}/{name}_s.png"
                info2, _ = render_eq(latex, out2, fs2, color, matplotlibrc)
                if info2 and info2["w_px"] == tw and info2["h_px"] == th:
                    ok2, n2 = pil_cmp(out2, banked)
                    if ok2:
                        return True, fs2, "exact (fine scan)"
            return False, round(fs_try, 4), f"size match at fs={round(fs_try,4)} but bytes differ"
        if it == 5:
            break
        # Newton step on width (width ~ linear in fs)
        fs_try = fs_try * tw / info["w_px"]
    return False, None, f"no size match (banked {tw}x{th}, best {info['w_px']}x{info['h_px']} @fs {round(fs_try,4)})"

results = {}

# ---------- slide 031 (eq_manifest.json sidecar) ----------
EQ = json.load(open(f"{ASSETS}/eq_manifest.json"))
r31 = {}
for name, e in EQ.items():
    ok, fsf, det = verify(name, e["latex"], "#" + e["color"], e["fontsize_pt"])
    r31[name] = {"ok": ok, "fs": fsf, "detail": det}
    print(("OK  " if ok else "FAIL"), "031", name, fsf, det, flush=True)
results["031"] = r31

# ---------- slides 011/015 (eq015_kq / eq015_sqrtd; color measured 8B1A10) ----------
r15 = {}
for name, latex in [("eq015_kq", r"K\cdot q"), ("eq015_sqrtd", r"\sqrt{d}")]:
    ok, fsf, det = verify(name, latex, "#8B1A10", 12.0, scan=3.0, step=0.02)
    r15[name] = {"ok": ok, "fs": fsf, "detail": det, "latex": latex}
    print(("OK  " if ok else "FAIL"), "011/015", name, fsf, det, flush=True)
results["011_015"] = r15

# ---------- slide 054 (eq_Kcdotq_over_sqrtd; color measured C00000) ----------
ok, fsf, det = verify("eq_Kcdotq_over_sqrtd", r"\frac{K\cdot q}{\sqrt{d}}", "#C00000", 20.0, scan=3.0, step=0.02)
results["054"] = {"eq_Kcdotq_over_sqrtd": {"ok": ok, "fs": fsf, "detail": det,
                                            "latex": r"\frac{K\cdot q}{\sqrt{d}}"}}
print(("OK  " if ok else "FAIL"), "054", "eq_Kcdotq_over_sqrtd", fsf, det, flush=True)

# ---------- slide 040 (latex from gen_eqs2/gen_eqs3 banked generators; cm fontset) ----------
MRC = f"{VID}/scratch/slide040/matplotlibrc"
LATEX40 = {
    "h1": r"\mathbf{Input:}\ \ \mathrm{Values\ of}\ x\ \mathrm{over\ a\ mini-batch:}\ \mathcal{B}=\{x_{1\ldots m}\};",
    "h2": r"\mathrm{Parameters\ to\ be\ learned:}\ \gamma,\ \beta",
    "h3": r"\mathbf{Output:}\ \ \{y_i=\mathrm{BN}_{\gamma,\beta}(x_i)\}",
    "eq1": r"\mu_{\mathcal{B}} \longleftarrow \frac{1}{m} \sum_{i=1}^{m} x_i",
    "eq2": r"\sigma_{\mathcal{B}}^{2} \longleftarrow \frac{1}{m} \sum_{i=1}^{m} (x_i - \mu_{\mathcal{B}})^2",
    "eq3": r"\widehat{x}_i \leftarrow \frac{x_i - \mu_{\mathcal{B}}}{\sqrt{\sigma_{\mathcal{B}}^2 + \epsilon}}",
    "eq4": r"y_i \leftarrow \gamma\, \widehat{x}_i + \beta \equiv \mathrm{BN}_{\gamma,\beta}(x_i)",
}
r40 = {}
for name, latex in LATEX40.items():
    side = json.load(open(f"{ASSETS}/slide040_{name}_eq.json"))
    color = side["color"].lstrip("#")
    ok, fsf, det = verify(f"slide040_{name}", latex, "#" + color, side["fontsize_pt"],
                          matplotlibrc=MRC, scan=0.12, step=0.01)
    r40[name] = {"ok": ok, "fs": fsf, "detail": det, "latex": latex, "color": color}
    print(("OK  " if ok else "FAIL"), "040", name, fsf, det, flush=True)
results["040"] = r40

with open(f"{VID}/scratch/omml_wrap/provenance_results.json", "w") as f:
    json.dump(results, f, indent=1)
print("BANKED -> scratch/omml_wrap/provenance_results.json")
