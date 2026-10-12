#!/usr/bin/env python3
"""fix_beam.py — replace the (LO-unrenderable) beam011.png <p:pic> in
slide_011_recreated.pptx with vector custGeom polygons of the measured ribbons.

Bbox (slide pts): (392,58)..(742,192) — w=350, h=134; ALL path points inside it
(points outside the declared path box made LibreOffice degrade the whole slide's
image layer — measured: every fix_beam'd deck lost its raster images; every
non-fix_beam deck rendered them).

Ribbons (slide pts):
  main:  (524,68),(690,68),(692,172),(392,172)   — drawn twice (overlap-saturated core)
  strip: (686,160),(742,160),(727,192),(686,192)
Fill: FFFC28 @55% per layer (hashed hex; COLOR LAW).

Idempotent; fails loudly if the anchor pic is missing.
"""
import re
import shutil
import zipfile

PPTX = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_011_recreated.pptx"
TMP = PPTX + ".tmp"

EMU = 914400
X, Y = 392 / 72 * EMU, 58 / 72 * EMU
W, H = 350 / 72 * EMU, 134 / 72 * EMU


def pt(x, y):  # slide pts -> path coords (1:1)
    return int(x - 392), int(y - 58)


def sp(name, sid, pts, alpha):
    path = "".join(
        (f'<a:moveTo><a:pt x="{px}" y="{py}"/></a:moveTo>' if i == 0
         else f'<a:lnTo><a:pt x="{px}" y="{py}"/></a:lnTo>')
        for i, (px, py) in enumerate((pt(*p) for p in pts)))
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="{name}"/>'
        '<p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr>'
        f'<a:xfrm><a:off x="{X}" y="{Y}"/><a:ext cx="{W}" cy="{H}"/></a:xfrm>'
        '<a:custGeom><a:avLst/><a:gdLst/><a:ahLst/><a:cxnLst/><a:rectLst/>'
        f'<a:pathLst><a:path w="350" h="134">{path}'
        '<a:close/></a:path></a:pathLst></a:custGeom>'
        f'<a:solidFill><a:srgbClr val="FFFC28"><a:alpha val="{alpha}"/></a:srgbClr></a:solidFill>'
        '<a:ln><a:noFill/></a:ln></p:spPr></p:sp>'
    )


SPS = (
    sp("beam011", 8801, [(524, 68), (690, 68), (692, 172), (392, 172)], 55000)
    + sp("beam011_b", 8803, [(524, 68), (690, 68), (692, 172), (392, 172)], 55000)
    + sp("beam011_strip", 8802, [(686, 160), (742, 160), (727, 192), (686, 192)], 55000)
)

zin = zipfile.ZipFile(PPTX)
xml = zin.read("ppt/slides/slide1.xml").decode("utf8")
pics = re.findall(r"<p:pic>.*?</p:pic>", xml, re.S)
anchor = [p for p in pics if "beam011.png" in p]
assert anchor, "beam anchor pic not found — rebuild first"
xml2 = xml.replace(anchor[0], SPS)
assert "beam011.png" not in xml2

zout = zipfile.ZipFile(TMP, "w", zipfile.ZIP_DEFLATED)
for item in zin.infolist():
    data = zin.read(item.filename)
    if item.filename == "ppt/slides/slide1.xml":
        data = xml2.encode("utf8")
    zout.writestr(item, data)
zout.close()
zin.close()
shutil.move(TMP, PPTX)
print("beam replaced with 3 custGeom shapes (all path points inside the bbox); pics left:", xml2.count("<p:pic>"))
