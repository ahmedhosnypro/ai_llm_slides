#!/usr/bin/env python3
"""Generate mathtext equation PNGs + manifest for slides 023-033 builds."""
import json, os, subprocess, sys

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
ASSETS = os.path.join(NS, "recreated_pptx/build/assets")
os.makedirs(ASSETS, exist_ok=True)

# slide -> list of (key, latex, fontsize_pt, color)
EQS = {
  25: [
    ("vecpair", r"a = [a_1\ a_2]^T\quad b = [b_1\ b_2]^T", 18, "000000"),
    ("eq1", r"[a^T b]^2 = ([a_1\ a_2\ |\ b_1; b_2])^2 = (a_1 b_1 + a_2 b_2)^2 = a_1^2 b_1^2 + a_2^2 b_2^2 + 2 a_1 b_1 a_2 b_2", 14, "000000"),
    ("eq2", r"[a^T b]^2 = (a_1^2\ \ a_2^2\ \ \sqrt{2} a_1 a_2\ |\ b_1^2; b_2^2; \sqrt{2} b_1 b_2) = \varphi(a)^T \varphi(b)", 14, "000000"),
    ("where", r"Where:\ \varphi(x) \equiv [x_1; x_2] \Rightarrow [x_1^2; x_2^2; \sqrt{2} x_1 x_2]", 14, "000000"),
  ],
  26: [
    ("ab", r"a = (a_1; a_2)\quad b = (b_1; b_2)", 13, "000000"),
    ("eq1", r"[a^T b]^2 = (a_1\ a_2; b_1\ b_2) = (a_1 b_1 + a_2 b_2)^2 = a_1^2 b_1^2 + a_2^2 b_2^2 + 2 a_1 b_1 a_2 b_2", 12, "000000"),
    ("eq2", r"[a^T b]^2 = (a_1^2\ a_2^2\ \sqrt{2} a_1 a_2 ; b_1^2\ b_2^2\ \sqrt{2} b_1 b_2) = \varphi(a)^T \varphi(b)", 12, "000000"),
    ("phi", r"\varphi(x) \equiv (x_1; x_2) \Rightarrow (x_1^2; x_2^2; \sqrt{2} x_1 x_2)", 12, "000000"),
    ("abnum", r"a = (1; 2)\quad b = (3; 4)", 13, "000000"),
    ("num", r"\varphi(a)^T \varphi(b) = (1^2\ 2^2\ \sqrt{2}\ 1{\cdot}2)(3^2; 4^2; \sqrt{2}\ 3{\cdot}4) = (1\ 4\ \sqrt{2}\ 2)(9; 16; \sqrt{2}\ 12) = 9+64+48 = 121", 12, "000000"),
    ("alt", r"[a^T b]^2 = (1{\cdot}3 + 2{\cdot}4)^2 = 11^2 = 121", 12, "000000"),
  ],
  27: [
    ("def", r"[a^T b]^2 = [a_1\ a_2](b_1; b_2) = (a_1 b_1 + a_2 b_2)^2 = a_1^2 b_1^2 + a_2^2 b_2^2 + 2 a_1 b_1 a_2 b_2", 11, "000000"),
    ("exp", r"[a^T b + 1]^2 = (a^T b)^2 + 2 a^T b + 1 = (a_1 b_1 + a_2 b_2)^2 + 2(a_1 b_1 + a_2 b_2) + 1", 12, "000000"),
    ("cont", r"= a_1^2 b_1^2 + a_2^2 b_2^2 + 2 a_1 b_1 a_2 b_2 + 2 a_1 b_1 + 2 a_2 b_2 + 1", 12, "000000"),
    ("head", r"[a^T b + 1]^2 =", 13, "000000"),
    ("bcol", r"(b_1^2; b_2^2; \sqrt{2} b_2 b_1; \sqrt{2} b_1; \sqrt{2} b_2; 1)", 13, "000000"),
    ("xcol", r"(x_1^2; x_2^2; \sqrt{2} x_1 x_2; \sqrt{2} x_1; \sqrt{2} x_2; 1)", 13, "000000"),
    ("whereab", r"Where: \varphi(a)^T \varphi(b)", 12, "000000"),
    ("wherex", r"Where: \varphi(x) \equiv (x_1; x_2) \Rightarrow (x_1^2; x_2^2; \sqrt{2} x_1 x_2; \sqrt{2} x_1; \sqrt{2} x_2; 1)", 12, "000000"),
  ],
  28: [
    ("head", r"[a^T b + 1]^2", 13, "000000"),
    ("arow", r"(a_1^2\ \ a_2^2\ \ \sqrt{2} a_1 a_2\ \ \sqrt{2} a_1\ \ \sqrt{2} a_2\ \ 1)", 13, "FF0000"),
    ("bcol", r"(b_1^2; b_2^2; \sqrt{2} b_1 b_2; \sqrt{2} b_1; \sqrt{2} b_2; 1)", 13, "0000CD"),
    ("eq", r"[a^T b + 1]^2 = (a_1^2\ a_2^2\ \sqrt{2} a_1 a_2\ \sqrt{2} a_1\ \sqrt{2} a_2\ 1)(b_1^2; b_2^2; \sqrt{2} b_1 b_2; \sqrt{2} b_1; \sqrt{2} b_2; 1) = \varphi(a)^T \varphi(b)", 11, "000000"),
    ("phi", r"\varphi(x) \equiv (x_1; x_2; \sqrt{2} x_1 x_2; \sqrt{2} x_1; \sqrt{2} x_2; 1) \Rightarrow (x_1^2; x_2^2; \sqrt{2} x_1 x_2; \sqrt{2} x_1; \sqrt{2} x_2; 1)", 11, "000000"),
    ("ab", r"a = (1; 2)\quad b = (3; 4)", 13, "000000"),
    ("num", r"\varphi(a)^T \varphi(b) = (1^2\ 2^2\ \sqrt{2}\ 1{\cdot}2\ \sqrt{2}\ 2\sqrt{2}\ 1)(3^2; 4^2; \sqrt{2}\ 3{\cdot}4; 3\sqrt{2}; 4\sqrt{2}; 1) = (1\ 4\ 2\sqrt{2}\ \sqrt{2}\ 2\sqrt{2}\ 1)(9; 16; 12\sqrt{2}; 3\sqrt{2}; 4\sqrt{2}; 1)", 10, "000000"),
    ("sum", r"= 9+64+48+6+16+1 = 144", 12, "000000"),
    ("alt", r"= (1{\cdot}3+2{\cdot}4+1)^2 = 12^2 = 144", 12, "000000"),
  ],
  29: [
    ("eq1", r"e^{-\frac{1}{2}(a-b)^2} = e^{-\frac{1}{2}(a^2+b^2-2ab)} = e^{-a^2/2} e^{-b^2/2} e^{ab}", 14, "000000"),
    ("eq2", r"e^{ab} = 1 + \frac{ab}{1!} + \frac{(ab)^2}{2!} + \frac{(ab)^3}{3!} + \frac{(ab)^4}{4!} + \frac{(ab)^5}{5!} + \dots\infty", 14, "000000"),
    ("ex", r"e^x = 1 + \frac{x}{1!} + \frac{x^2}{2!} + \frac{x^3}{3!} + \frac{x^4}{4!} + \frac{x^5}{5!} + \dots\infty", 14, "000000"),
    ("e3", r"e^3 = 1 + \frac{3}{1!} + \frac{3^2}{2!} + \frac{3^3}{3!} + \frac{3^4}{4!} + \frac{3^5}{5!} + \dots\infty", 14, "000000"),
  ],
  30: [
    ("deriv", r"e^{-\frac{1}{2}(a-b)^2} = e^{-\frac{1}{2}(a^2+b^2-2ab)} = e^{-a^2/2}\ e^{-b^2/2}\ e^{ab} =", 15, "000000"),
    ("rowvec", r"e^{-a^2/2}\ (\ 1\ \ \frac{a}{\sqrt{1!}}\ \ \frac{a^2}{\sqrt{2!}}\ \ \frac{a^3}{\sqrt{3!}}\ \ \frac{a^4}{\sqrt{4!}}\ \ \dots\ \ \dots\infty\ )", 14, "000000"),
    ("colvec", r"(\ 1\ ;\ \frac{b}{\sqrt{1!}}\ ;\ \frac{b^2}{\sqrt{2!}}\ ;\ \frac{b^3}{\sqrt{3!}}\ ;\ \frac{b^4}{\sqrt{4!}}\ ;\ \dots\ ;\ \dots\infty\ )", 14, "000000"),
    ("rbf", r"e^{-\gamma(a-b)^2}", 16, "000000"),
    ("bfactor", r"e^{-b^2/2}", 13, "000000"),
    ("phiat", r"\varphi(a)^T", 14, "C00000"),
  ],
  31: [
    ("k1", r"K(a,b)=a^T b", 14, "FF0000"),
    ("k2a", r"K(a,b)=[a^T b]^2", 14, "FF0000"),
    ("k2b", r"K(a,b)=[a^T b + 1]^2", 14, "FF0000"),
    ("k3a", r"K(a,b)=[a^T b]^d", 14, "FF0000"),
    ("k3b", r"K(a,b)=[a^T b + 1]^d", 14, "FF0000"),
    ("k4", r"K(a,b)=[e^{-\gamma(a-b)^2}]", 14, "FF0000"),
  ],
  32: [
    ("r1", r"\kappa(a,b) = \kappa_1(a,b) + \kappa_2(a,b)", 15, "000000"),
    ("r2", r"\kappa(a,b) = \alpha\ \kappa_1(a,b)", 15, "000000"),
    ("r3", r"\kappa(a,b) = \kappa_1(a,b) * \kappa_2(a,b)", 15, "000000"),
    ("r4", r"\kappa(a,b) = \kappa_1(a,b) * \kappa_2(a,b) + \alpha\ \kappa_3(a,b)", 15, "000000"),
  ],
}

manifest = {}
for slide, eqs in EQS.items():
    m = {}
    for key, latex, fs, color in eqs:
        out = os.path.join(ASSETS, f"s{slide:03d}_{key}.png")
        r = subprocess.run([sys.executable, "/home/codespace/ai_llm_slides/scripts/render_eq.py", latex, out, str(fs), color],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(f"FAIL s{slide} {key}: {r.stderr[:200]}")
            continue
        info = json.loads(r.stdout.strip().splitlines()[-1])
        m[key] = info
    manifest[str(slide)] = m
mpath = os.path.join(ASSETS, "eqs_023_033.json")
json.dump(manifest, open(mpath, "w"), indent=1)
print("wrote", mpath)
for s, m in manifest.items():
    print(s, {k: (v["w_in"], v["h_in"]) for k, v in m.items()})
