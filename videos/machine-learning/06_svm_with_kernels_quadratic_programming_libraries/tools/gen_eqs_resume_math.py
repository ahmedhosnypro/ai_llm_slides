#!/usr/bin/env python3
import json, os, subprocess, sys

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
OUT = os.path.join(NS, "recreated_pptx/build/assets/resume_math")
os.makedirs(OUT, exist_ok=True)
RENDER = "/home/codespace/ai_llm_slides/scripts/render_eq_wide.py"

def stack(*rows):
    if len(rows) > 4:
        return r"\substack{" + r"\\".join(rows) + "}"
    value = rows[-1]
    for row in reversed(rows[:-1]):
        value = r"\overset{%s}{\underset{}{%s}}" % (row, value)
    return value

def vec(*rows):
    return r"\left\vert%s\right\vert" % stack(*rows)

def pvec(*rows):
    return r"\left(%s\right)" % stack(*rows)

EQS = {
  23: [
    ("rbf", r"\left[e^{-\gamma\Vert a-b\Vert^{2}}\right]", 16, "#000000"),
    ("rbf_plain", r"e^{-\gamma\Vert a-b\Vert^{2}}", 15, "#000000"),
    ("input", vec("a_1", "a_2") + r"\quad" + vec("b_1", "b_2"), 13, "#000000"),
    ("normal", r"\left\vert a_1\quad a_2\right\vert" + vec("b_1", "b_2"), 13, "#000000"),
    ("mapped", vec("u_1", "u_2", "u_3", r"\vdots", r"u_\infty") + r"\quad" + vec("v_1", "v_2", "v_3", r"\vdots", r"v_\infty"), 11, "#000000"),
    ("kernel", r"\left\vert u_1\ u_2\ u_3\ \cdots\ u_\infty\right\vert" + vec("v_1", "v_2", "v_3", r"\vdots", r"v_\infty"), 11, "#000000"),
  ],
  25: [
    ("vecpair", r"a=" + vec("a_1", "a_2") + r"\quad b=" + vec("b_1", "b_2"), 16, "#000000"),
    ("eq1", r"[a^{T}b]^{2}=\left(\left\vert a_1\ a_2\right\vert" + vec("b_1", "b_2") + r"\right)^{2}=(a_1b_1+a_2b_2)^{2}=a_1^{2}b_1^{2}+a_2^{2}b_2^{2}+2a_1b_1a_2b_2", 14, "#000000"),
    ("eq2", r"[a^{T}b]^{2}=\left\vert a_1^{2}\ a_2^{2}\ \sqrt{2}a_1a_2\right\vert" + vec("b_1^{2}", "b_2^{2}", r"\sqrt{2}b_1b_2") + r"=\phi(a)^{T}\phi(b)", 14, "#000000"),
    ("where", r"\mathrm{Where:}\ \phi(x)\equiv" + vec("x_1", "x_2") + r"\Rightarrow" + vec("x_1^{2}", "x_2^{2}", r"\sqrt{2}x_1x_2"), 14, "#000000"),
  ],
  26: [
    ("ab", r"a=" + vec("a_1", "a_2") + r"\quad b=" + vec("b_1", "b_2"), 13, "#000000"),
    ("eq1", r"[a^{T}b]^{2}=\left(\left\vert a_1\ a_2\right\vert" + vec("b_1", "b_2") + r"\right)^{2}=(a_1b_1+a_2b_2)^{2}=a_1^{2}b_1^{2}+a_2^{2}b_2^{2}+2a_1b_1a_2b_2", 12, "#000000"),
    ("eq2", r"[a^{T}b]^{2}=\left\vert a_1^{2}\ a_2^{2}\ \sqrt{2}a_1a_2\right\vert" + vec("b_1^{2}", "b_2^{2}", r"\sqrt{2}b_1b_2") + r"=\phi(a)^{T}\phi(b)", 12, "#000000"),
    ("phi", r"\phi(x)\equiv" + vec("x_1", "x_2") + r"\Rightarrow" + vec("x_1^{2}", "x_2^{2}", r"\sqrt{2}x_1x_2"), 12, "#000000"),
    ("abnum", r"a=" + vec("1", "2") + r"\quad b=" + vec("3", "4"), 13, "#000000"),
    ("num", r"\phi(a)^{T}\phi(b)=\left\vert1^{2}\ 2^{2}\ \sqrt{2}\,1{\cdot}2\right\vert" + vec("3^{2}", "4^{2}", r"\sqrt{2}\,3{\cdot}4") + r"=\left\vert1\ 4\ 2\sqrt{2}\right\vert" + vec("9", "16", r"12\sqrt{2}") + r"=9+64+48=121", 12, "#000000"),
    ("alt", r"[a^{T}b]^{2}=(1{\cdot}3+2{\cdot}4)^{2}=11^{2}=121", 12, "#000000"),
  ],
  27: [
    ("adef", r"a\ " + pvec("a_1", "a_2"), 15, "#C00000"),
    ("bdef", r"b\ " + pvec("b_1", "b_2"), 15, "#0000CC"),
    ("rem_all", r"\mathrm{Remember:}\ [a^{T}b]^{2}=\left(a_1\ a_2\right)" + pvec("b_1", "b_2") + r"=(a_1b_1+a_2b_2)^{2}=a_1^{2}b_1^{2}+a_2^{2}b_2^{2}+2a_1b_1a_2b_2", 12, "#000000"),
    ("exp_all", r"[a^{T}b+1]^{2}=(a^{T}b)^{2}+2{\cdot}a^{T}b+1=(a_1b_1+a_2b_2)^{2}=a_1^{2}b_1^{2}+a_2^{2}b_2^{2}+2a_1b_1a_2b_2+2(a_1b_1+a_2b_2)+1", 12, "#000000"),
    ("brace_label", r"|a^{T}b|^{2}", 9, "#C00000"),
    ("l3", r"=a_1^{2}b_1^{2}+a_2^{2}b_2^{2}+2a_1b_1a_2b_2+2a_1b_1+2a_2b_2+1", 13, "#000000"),
    ("tan", r"[a^{T}b+1]^{2}=", 14, "#C00000"),
    ("arow", r"\left(a_1^{2}\ a_2^{2}\ \sqrt{2}a_1a_2\ \sqrt{2}a_1\ \sqrt{2}a_2\ 1\right)", 13, "#C00000"),
    ("bcol", pvec("b_1^{2}", "b_2^{2}", r"\sqrt{2}b_2b_1", r"\sqrt{2}b_1", r"\sqrt{2}b_2", "1"), 13, "#0000CC"),
    ("eq", r"=\phi(a)^{T}\phi(b)", 13, "#000000"),
    ("wherex", r"\mathrm{Where:}\ \phi(x)\equiv" + pvec("x_1", "x_2") + r"\Rightarrow", 13, "#000000"),
    ("xcol", pvec("x_1^{2}", "x_2^{2}", r"\sqrt{2}x_1x_2", r"\sqrt{2}x_1", r"\sqrt{2}x_2", "1"), 13, "#000000"),
  ],
}

manifest = {}
for slide, items in EQS.items():
    entry = {}
    for key, latex, size, color in items:
        path = os.path.join(OUT, f"s{slide:03d}_{key}.png")
        run = subprocess.run([sys.executable, RENDER, latex, path, str(size), color], capture_output=True, text=True)
        if run.returncode:
            raise RuntimeError(f"s{slide:03d} {key}: {run.stderr}")
        info = json.loads(run.stdout.strip().splitlines()[-1])
        info["mathtext"] = latex
        with open(path + ".json", "w") as f:
            json.dump(info, f, indent=1)
        entry[key] = info
    manifest[str(slide)] = entry
mpath = os.path.join(OUT, "manifest.json")
with open(mpath, "w") as f:
    json.dump(manifest, f, indent=1)
print(mpath)
for slide, entry in manifest.items():
    print(slide, {k: (v["w_in"], v["h_in"]) for k, v in entry.items()})
