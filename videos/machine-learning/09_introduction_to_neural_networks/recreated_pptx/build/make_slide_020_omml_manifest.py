#!/usr/bin/env python3
"""Derive the slide-020 OMML manifest from the CURRENT pptx rel ids."""
import json
import re
import sys
import zipfile
from pathlib import Path

V = Path("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks")
PPTX = V / "recreated_pptx/build/slide_020_recreated.pptx"
SEGS = json.loads((V / "recreated_pptx/build/equations_slide_020/eq_020_segments.json").read_text())
OUT = V / "recreated_pptx/build/slide_020_omml_manifest.json"

with zipfile.ZipFile(PPTX) as z:
    xml = z.read("ppt/slides/slide1.xml").decode()
    rels = z.read("ppt/slides/_rels/slide1.xml.rels").decode()

rid_by_target = dict(re.findall(r'Id="([^"]+)"[^>]*Target="([^"]+)"', rels))
eqs = []
for pic in re.findall(r"<p:pic>.*?</p:pic>", xml, re.S):
    descr = re.search(r'descr="([^"]+)"', pic).group(1)
    rid = re.search(r'r:embed="([^"]+)"', pic).group(1)
    name = Path(descr).stem.replace("eq_020_", "", 1)
    if name not in SEGS:
        continue
    m = SEGS[name]
    eqs.append({
        "rel_id": rid,
        "image": Path(descr).name,
        "mathtext": m["mathtext"],
        "font_size_pt": float(m["fontsize_pt"]),
        "color": m["color"],
    })

if len(eqs) != len(SEGS):
    sys.exit(f"expected {len(SEGS)} equation pics, found {len(eqs)}")
OUT.write_text(json.dumps({"slides": [{"slide": 1, "equations": eqs}]}, indent=2) + "\n")
print(OUT)
