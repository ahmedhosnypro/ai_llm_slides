import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["mathtext.fontset"] = "custom"
matplotlib.rcParams["mathtext.rm"] = "Liberation Sans"
DPI = 200


def rend(latex, fs):
    fig = plt.figure(figsize=(6, 3), dpi=DPI)
    fig.patch.set_alpha(0)
    fig.text(0.02, 0.5, "$" + latex + "$", fontsize=fs, ha="left", va="center")
    fig.canvas.draw()
    buf = matplotlib.keyence if False else None
    import numpy as np
    b = np.asarray(fig.canvas.buffer_rgba())
    a = b[:, :, 3]
    ink = a > 8
    cs = np.where(ink.any(axis=0))[0]
    rs = np.where(ink.any(axis=1))[0]
    c = a[rs.min():rs.max() + 1, cs.min():cs.max() + 1]
    h, w = c.shape
    thick = int((c[h // 2, :12] > 200).sum())
    return w / DPI * 72, h / DPI * 72, thick


for fs in (19, 20, 21, 22, 23, 24):
    w, h, t = rend(r"\left( \substack{4 \\ -2 \\ -2} \right)", fs)
    print("fs=%2d w=%.1fpt h=%.1fpt stroke=%dpx" % (fs, w, h, t))
