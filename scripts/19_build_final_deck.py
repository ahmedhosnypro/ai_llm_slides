#!/usr/bin/env python3
"""Build the final all-in-one deck from the certified per-slide packages.

Variant precedence per slide (founder directive 2026-10-10): OMML > graphed > base.
After the single-version consolidation (scripts/20_consolidate_single_version.py) the
per-slide pptx are all plain-named `slide_NNN_recreated.pptx` (graph/OMML baked in) and
this script's globs fall back to those plain names — one per slide, unchanged behavior.
Every chosen slide's XML and media are copied VERBATIM — rIds are per-slide, so the
slide XML needs no edits; only the slide's .rels targets are retargeted:
  layout    -> the shared skeleton layout (byte-identical across all decks, md5-checked)
  notesSlide-> a per-slide copy of the source notesSlide
  media     -> ppt/media/imgNNN_<origname> (renamed, bytes identical)

The skeleton (master/layout/theme/notesMaster/props/docProps) comes from
slide_001_recreated.pptx. The result is proven lossless by render+pixel-diff in the
verify step — the certified bytes are never re-encoded.

Usage:  python3 scripts/19_build_final_deck.py <recreated_pptx_dir> <out.pptx>
"""

import re
import sys
import zipfile
from pathlib import Path


def choose_sources(pptx_dir: Path):
    """Pick the variant for each slide number, in slide order."""
    omml = {int(p.stem.split("_")[1]) for p in pptx_dir.glob("slide_*_recreated_omml.pptx")}
    graphed = {int(p.stem.split("_")[1]) for p in pptx_dir.glob("slide_*_recreated_graphed.pptx")}
    chosen = []
    for n in range(1, 65):
        if n in omml:
            f = pptx_dir / f"slide_{n:03d}_recreated_omml.pptx"
            variant = "omml"
        elif n in graphed:
            f = pptx_dir / f"slide_{n:03d}_recreated_graphed.pptx"
            variant = "graphed"
        else:
            f = pptx_dir / f"slide_{n:03d}_recreated.pptx"
            variant = "base"
        if not f.exists():
            sys.exit(f"FATAL: missing source for slide {n}: {f}")
        chosen.append((n, variant, f))
    return chosen


def main() -> None:
    pptx_dir = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    chosen = choose_sources(pptx_dir)

    skeleton = zipfile.ZipFile(chosen[0][2])  # slide 001 base package
    src_zips = {n: zipfile.ZipFile(f) for n, _, f in chosen}

    # sanity: skeleton parts are expected byte-identical in every source. Slide 63's
    # graphed package is a LibreOffice save (own master/layout/theme) — its slide XML
    # is self-contained (own p:bg, explicit fonts), so a shared skeleton only affects
    # inheritable style defaults; the render+pixel-diff gate proves this lossless.
    for part in ("ppt/slideLayouts/slideLayout1.xml",
                 "ppt/slideMasters/slideMaster1.xml",
                 "ppt/theme/theme1.xml",
                 "ppt/notesMasters/notesMaster1.xml"):
        ref = skeleton.read(part)
        for n, _, _ in chosen:
            if src_zips[n].read(part) != ref:
                print(f"WARN: skeleton part {part} differs in slide {n} source "
                      f"(relying on pixel-diff gate)")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    zf = zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED)

    # 1. skeleton parts as-is (layout/master/theme/notesMaster/props/docProps)
    copied_slides = ("ppt/slides/slide1.xml", "ppt/slides/_rels/slide1.xml.rels",
                     "ppt/notesSlides/notesSlide1.xml",
                     "ppt/notesSlides/_rels/notesSlide1.xml.rels")
    for name in skeleton.namelist():
        if name.endswith("/"):
            continue
        if name in copied_slides or name in ("ppt/presentation.xml",
                                             "ppt/_rels/presentation.xml.rels",
                                             "[Content_Types].xml"):
            continue  # rebuilt below
        zf.writestr(name, skeleton.read(name))

    # slide 1 keeps the skeleton's own slide/notesSlide parts verbatim
    for name in copied_slides:
        zf.writestr(name, skeleton.read(name))

    # 2. slides 2..64: verbatim XML, retargeted rels, renamed media
    for n, variant, f in chosen[1:]:
        z = src_zips[n]
        zf.writestr(f"ppt/slides/slide{n}.xml", z.read("ppt/slides/slide1.xml"))
        zf.writestr(f"ppt/notesSlides/notesSlide{n}.xml",
                    z.read("ppt/notesSlides/notesSlide1.xml"))

        rels = z.read("ppt/slides/_rels/slide1.xml.rels").decode("utf-8")
        media_names = {m for m in z.namelist()
                       if m.startswith("ppt/media/") and not m.endswith("/")}
        for m in sorted(media_names):
            base = Path(m).name
            zf.writestr(f"ppt/media/img{n:03d}_{base}", z.read(m))

        def retarget(mo):
            rid, rtype, target = mo.groups()
            t = rtype.rsplit("/", 1)[-1]
            if t == "slideLayout":
                new = "../slideLayouts/slideLayout1.xml"
            elif t == "notesSlide":
                new = f"../notesSlides/notesSlide{n}.xml"
            elif t == "image":
                new = f"../media/img{n:03d}_{Path(target).name}"
            else:
                sys.exit(f"FATAL: slide {n} uses unhandled rel type {rtype}")
            return f'<Relationship Id="{rid}" Type="{rtype}" Target="{new}"/>'

        rels = re.sub(r'<Relationship Id="([^"]+)" Type="([^"]+)" Target="([^"]+)"/>',
                      retarget, rels)
        zf.writestr(f"ppt/slides/_rels/slide{n}.xml.rels", rels)

        nrels = z.read("ppt/notesSlides/_rels/notesSlide1.xml.rels").decode("utf-8")
        nrels = nrels.replace("../slides/slide1.xml", f"../slides/slide{n}.xml")
        zf.writestr(f"ppt/notesSlides/_rels/notesSlide{n}.xml.rels", nrels)

    # 3. presentation.xml + rels: 64 slides
    pres = skeleton.read("ppt/presentation.xml").decode("utf-8")
    sld_ids = "".join(f'<p:sldId id="{255 + n}" r:id="rId{n + 1}"/>' for n in range(1, 65))
    pres = re.sub(r"<p:sldIdLst>.*?</p:sldIdLst>", f"<p:sldIdLst>{sld_ids}</p:sldIdLst>", pres)
    pres = re.sub(r'<p:notesMasterId r:id="[^"]+"/>', '<p:notesMasterId r:id="rId66"/>', pres)
    zf.writestr("ppt/presentation.xml", pres)

    prels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
             '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument'
             '/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>'
             + "".join(f'<Relationship Id="rId{n + 1}" Type="http://schemas.openxmlformats.org'
                       f'/officeDocument/2006/relationships/slide" Target="slides/slide{n}.xml"/>'
                       for n in range(1, 65))
             + '<Relationship Id="rId66" Type="http://schemas.openxmlformats.org/officeDocument'
             '/2006/relationships/notesMaster" Target="notesMasters/notesMaster1.xml"/>'
             '<Relationship Id="rId67" Type="http://schemas.openxmlformats.org/officeDocument'
             '/2006/relationships/presProps" Target="presProps.xml"/>'
             '<Relationship Id="rId68" Type="http://schemas.openxmlformats.org/officeDocument'
             '/2006/relationships/viewProps" Target="viewProps.xml"/>'
             '<Relationship Id="rId69" Type="http://schemas.openxmlformats.org/officeDocument'
             '/2006/relationships/theme" Target="theme/theme1.xml"/>'
             '<Relationship Id="rId70" Type="http://schemas.openxmlformats.org/officeDocument'
             '/2006/relationships/tableStyles" Target="tableStyles.xml"/>'
             "</Relationships>")
    zf.writestr("ppt/_rels/presentation.xml.rels", prels)

    # 4. [Content_Types].xml: overrides for every slide + notesSlide
    ct = skeleton.read("[Content_Types].xml").decode("utf-8")
    overrides = "".join(
        f'<Override PartName="/ppt/slides/slide{n}.xml" ContentType="application/vnd.'
        f'openxmlformats-officedocument.presentationml.slide+xml"/>'
        f'<Override PartName="/ppt/notesSlides/notesSlide{n}.xml" ContentType="application/'
        f'vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/>'
        for n in range(2, 65))
    ct = ct.replace("</Types>", overrides + "</Types>")
    zf.writestr("[Content_Types].xml", ct)

    zf.close()

    # summary
    by_v = {}
    for n, v, _ in chosen:
        by_v.setdefault(v, []).append(n)
    print(f"wrote {out_path}")
    for v, ns in by_v.items():
        print(f"  {v:7s}: {len(ns):2d} slides -> {ns}")


if __name__ == "__main__":
    main()
