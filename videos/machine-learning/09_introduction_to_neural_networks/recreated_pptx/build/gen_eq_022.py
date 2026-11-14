"""Generate color-sharded 2D equation PNGs for slide 022 (mathtext -> 600dpi RGBA).

Shards are rendered one color at a time via scripts/render_eq.py, then composited on a
canvas using baseline metadata so stacked case rows stay baseline-aligned with a single
stretched red brace.
Usage: python3 gen_eq_022.py    (writes PNGs into equations_slide022/col_ and prints sizes)
"""
import json
import os
import subprocess

from PIL import Image, ImageDraw
import numpy as np

RENDER = "/home/codespace/ai_llm_slides/scripts/render_eq.py"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "equations_slide022")
os.makedirs(OUT, exist_ok=True)
DPI = 600
FONT = 18.0
RED = "#C00000"
BLUE = "#2B3FC4"
GREEN = "#1E8B1E"
BLACK = "#000000"
PAD = 8
CANVAS_W, CANVAS_H = 5000, 1400


class Shard:
    def __init__(self, name, latex, color):
        path = os.path.join(OUT, "col_%s.png" % name)
        info = json.loads(subprocess.run(
            ["python3", RENDER, latex, path, str(FONT), color],
            check=True, capture_output=True, text=True).stdout)
        self.path = path
        self.w = int(info["w_px"])
        self.h = int(info["h_px"])
        self.base = int(info["baseline_px"])

    def paste(self, canvas, x, base_y):
        im = Image.open(self.path).convert("RGBA")
        canvas.paste(im, (int(x), int(base_y - self.base)), im)
        return x + self.w

    def vcenter(self, top, bottom):
        im = Image.open(self.path).convert("RGBA")
        mid = (top + bottom) // 2
        canvas = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
        return canvas


def brace():
    """Return (Shard for the cropped brace, pitch px between its two stacked rows)."""
    sh = Shard("brace", r"\left\{ \substack{0 \\ y} \right.", RED)
    im = Image.open(sh.path).convert("RGBA")
    a = np.asarray(im)[:, :, 3]
    cols = (a > 8).sum(axis=0)
    runs, s = [], None
    for x in range(len(cols)):
        if cols[x] > 0 and s is None:
            s = x
        elif cols[x] == 0 and s is not None:
            runs.append((s, x - 1))
            s = None
    if s is not None:
        runs.append((s, len(cols) - 1))
    x0, x1 = runs[0]
    right = (a > 8)[:, x1 + 1:].sum(axis=1)
    rows, s = [], None
    for y in range(len(right)):
        if right[y] > 0 and s is None:
            s = y
        elif right[y] == 0 and s is not None:
            rows.append((s, y - 1))
            s = None
    pitch = sh.base - rows[0][1]
    Image.fromarray(np.asarray(im)[:, x0:x1 + 1]).save(os.path.join(OUT, "col_brace_crop.png"))
    br = Shard.__new__(Shard)
    br.path = os.path.join(OUT, "col_brace_crop.png")
    br.w = x1 - x0 + 1
    br.h = sh.h
    br.base = sh.base
    return br, pitch


def finish(canvas, name):
    a = np.asarray(canvas)[:, :, 3]
    ys, xs = np.where(a > 8)
    y0, y1 = max(int(ys.min()) - PAD, 0), min(int(ys.max()) + PAD, canvas.height)
    x0, x1 = max(int(xs.min()) - PAD, 0), min(int(xs.max()) + PAD, canvas.width)
    path = os.path.join(OUT, name)
    canvas.crop((x0, y0, x1, y1)).save(path)
    return round((x1 - x0) / DPI, 4), round((y1 - y0) / DPI, 4)


BR, PITCH = brace()
LINE = PITCH
X0 = 600
Y0 = 430


def seq(canvas, shards, x, base_y, gap):
    end = x
    for sh in shards:
        end = sh.paste(canvas, end, base_y) + gap
    return end


def piecewise(name, pre, lines, trailing=None):
    c = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    y1 = Y0 + LINE
    mid = (Y0 + y1) // 2
    end = seq(c, pre, X0, mid, 0)
    xb = BR.paste(c, end + 60, y1)
    xval = xb + 80
    vmax = 0
    for i, (val, cond) in enumerate(lines):
        base = Y0 if i == 0 else y1
        e = seq(c, [val], xval, base, 0)
        vmax = max(vmax, e - xval)
    cend = 0
    for i, (val, cond) in enumerate(lines):
        base = Y0 if i == 0 else y1
        cend = max(cend, seq(c, [cond], xval + vmax + 80, base, 0))
    if trailing is not None:
        trailing.paste(c, cend + 100, y1)
    return finish(c, name)


def simple(name, parts, lines=1):
    c = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    seq(c, parts, X0, Y0, 0)
    return finish(c, name)


def fraction(name, pre, num, den, bar_color):
    c = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    end = seq(c, pre, X0, Y0 + 150, 0)
    xn = end + 60
    n = num[0]
    n.paste(c, xn, Y0)
    xmax = xn + n.w
    d = den[0]
    dn = Y0 + 300
    for sh in den:
        xmax = sh.paste(c, xmax, dn) + 20
    mid = (Y0 + dn) // 2 + 8
    ImageDraw.Draw(c).rectangle([xn, mid, xmax - 20, mid + 6], fill=bar_color)
    return finish(c, name)


def main():
    os.makedirs(OUT, exist_ok=True)
    manifest = {"slide": 22, "dpi": DPI, "font_size_pt": FONT, "equations": []}

    def sh(name, latex, color):
        return Shard(name, latex, color)

    fx = lambda: sh("fx", r"\mathit{f(x)=}", BLACK)
    dfx = lambda: sh("dfx", r"\mathit{f'(x)=}", BLACK)
    eq = lambda: sh("eq", r"=", BLACK)
    cond_lt = lambda: sh("lt", r"\mathit{for}\ x<0", BLACK)
    cond_ge = lambda: sh("ge", r"\mathit{for}\ x\geq 0", GREEN)

    specs = [
        ("eq_relu_f", piecewise("eq_relu_f.png", [fx(), sh("relu", r"\mathit{Rectified\ Linear\ Unit}", RED), eq()], [(sh("v0", r"0", RED), cond_lt()), (sh("vx", r"x", RED), cond_ge())])),
        ("eq_relu_df", piecewise("eq_relu_df.png", [dfx()], [(sh("v0", r"0", RED), cond_lt()), (sh("v1", r"1", RED), cond_ge())])),
        ("eq_prelu_f", piecewise("eq_prelu_f.png", [fx(), sh("p", r"\mathit{P}", BLUE), sh("prelu", r"\mathit{arametric\ ReLU}", RED), eq()], [(sh("ax", r"\alpha x", BLUE), cond_lt()), (sh("x", r"x", RED), cond_ge())], trailing=sh("plus", r"+", "#C98A8A"))),
        ("eq_prelu_df", piecewise("eq_prelu_df.png", [dfx()], [(sh("a", r"\alpha", BLUE), cond_lt()), (sh("one", r"1", RED), cond_ge())])),
        ("eq_elu_f", piecewise("eq_elu_f.png", [fx(), sh("e", r"\mathit{E}", BLUE), sh("elu", r"\mathit{xponential\ LU}", RED), eq()], [(sh("eluval", r"\alpha(e^{x}-1)", RED), cond_lt()), (sh("x", r"x", RED), cond_ge())])),
        ("eq_elu_df", piecewise("eq_elu_df.png", [dfx()], [(sh("fxa", r"\mathit{f(x)}+\alpha", RED), cond_lt()), (sh("one", r"1", RED), cond_ge())])),
        ("eq_softplus_f", simple("eq_softplus_f.png", [fx(), sh("sp", r"\mathit{SoftPlus}", RED), eq(), sh("log", r"\log_{e}(1+e^{x})", BLACK)])),
        ("eq_softplus_df", fraction("eq_softplus_df.png", [dfx()], [sh("num", r"1", BLACK)], [sh("d1", r"1+e", BLACK), sh("d2", r"^{-x}", RED)], BLACK)),
    ]
    for name, (w_in, h_in) in specs:
        manifest["equations"].append({
            "name": name, "image": name + ".png", "w_in": w_in, "h_in": h_in,
            "font_size_pt": FONT, "color": "mixed",
            "mathtext": "color-sharded composite; see gen_eq_022.py",
        })
        print(name, w_in, h_in)
    with open(os.path.join(OUT, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)


if __name__ == "__main__":
    main()
