#!/usr/bin/env python3
"""Regenerate equation PNGs from sidecar JSONs whose images were never written."""
import json, os, sys
import numpy as np
from PIL import Image

BUILD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUILD)
from render_eq_multi import render_segment, PAD_PX

def compose(eqdir, name):
    meta = json.load(open(os.path.join(eqdir, name + ".json")))
    segs = []
    for r in meta["rows"]:
        for part in r.split("||"):
            if part:
                color, latex = part.split(":", 1)
                segs.append((color, latex))
    fs = meta["fontsize_pt"][0] if isinstance(meta.get("fontsize_pt"), list) else meta.get("fontsize_pt", 16)
    rendered = [render_segment(latex, color, fs) for color, latex in segs]
    max_b = max(b for _, b in rendered)
    heights = [a.shape[0] for a, _ in rendered]
    total_h = max_b + max(h - b for (_, b), h in zip(rendered, heights)) + 2 * PAD_PX
    total_w = sum(a.shape[1] for a, _ in rendered) + 4 * (len(rendered) - 1) + 2 * PAD_PX
    canvas = np.zeros((total_h, total_w, 4), dtype=np.uint8)
    x = PAD_PX
    for (arr, b) in rendered:
        y = max_b - b
        canvas[y:y + arr.shape[0], x:x + arr.shape[1]] = arr
        x += arr.shape[1] + 4
    out = os.path.join(eqdir, name + ".png")
    Image.fromarray(canvas).save(out)
    meta.update(w_px=int(total_w), h_px=int(total_h), w_in=round(total_w / 600, 5), h_in=round(total_h / 600, 5))
    json.dump(meta, open(out + ".json", "w"), indent=1)
    print("wrote", out, meta["w_in"], "x", meta["h_in"])

if __name__ == "__main__":
    for eqdir, names in [("eq_012", ["e3", "e4", "e5", "e7", "e13"])]:
        for n in names:
            compose(os.path.join(BUILD, eqdir), n)
