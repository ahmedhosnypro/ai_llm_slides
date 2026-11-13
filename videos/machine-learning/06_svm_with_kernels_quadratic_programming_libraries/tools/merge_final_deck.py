#!/usr/bin/env python3
"""OPC-level continuous final-deck merge for 06_svm_with_kernels_quadratic_programming_libraries.

For each certified slide_NNN_recreated.pptx, replace page N of the placeholder final
deck byte-verbatim: slide XML, slide rels (rewritten so media/fonts land under
per-slide names), media, and Content_Types entries. Presentation rels are untouched
because slide part names (slides/slideN.xml) are preserved. Never re-encodes media.

Usage:
  merge_final_deck.py --final <final.pptx> --slides-dir <dir> --out <merged.pptx>
      [--slide NNN ...]            # default: all slide_NNN_recreated.pptx found
  merge_final_deck.py --final <final.pptx> --slides-dir <dir> --verify-only
"""
import argparse, hashlib, os, posixpath, re, shutil, sys, zipfile
from xml.etree import ElementTree as ET

NS = {"p": "http://schemas.openxmlformats.org/package/2006/relationships",
      "ct": "http://schemas.openxmlformats.org/package/2006/content-types"}
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"


def sha(b): return hashlib.md5(b).hexdigest()


def slide_rels_targets(rels_xml):
    """Return list of (rId, Target, Type) for a slide .rels part."""
    root = ET.fromstring(rels_xml)
    out = []
    for r in root.findall("p:Relationship", NS):
        out.append((r.get("Id"), r.get("Target"), r.get("Type")))
    return out


def replace_slide(final_zip, n, src_path):
    """Replace page n of final_zip (in-memory dict of name->bytes) with src's slide1."""
    src = zipfile.ZipFile(src_path)
    src_names = set(src.namelist())
    if "ppt/slides/slide1.xml" not in src_names:
        raise RuntimeError(f"{src_path}: no ppt/slides/slide1.xml")
    slide_xml = src.read("ppt/slides/slide1.xml")
    src_rels_path = "ppt/slides/_rels/slide1.xml.rels"
    src_rels = slide_rels_targets(src.read(src_rels_path)) if src_rels_path in src_names else []

    # Rewrite rels: external targets untouched; internal targets get per-slide part names.
    new_rels = ET.fromstring(src.read(src_rels_path)) if src_rels_path in src_names else None
    media_map = {}   # old media name -> new media name
    font_map = {}
    for r in new_rels.findall("p:Relationship", NS):
        tgt, rtype = r.get("Target"), r.get("Type")
        if tgt.startswith("http") or r.get("TargetMode") == "External":
            continue
        base = posixpath.normpath(posixpath.join("ppt/slides", tgt))
        kind = base.split("/")[1]  # media | fonts | theme | ...
        if kind in ("media", "fonts"):
            new_base = f"ppt/{kind}/s{n:03d}_{posixpath.basename(base)}"
            media_map[base] = new_base if kind == "media" else None
            if kind == "fonts":
                font_map[base] = new_base
            r.set("Target", posixpath.relpath(new_base, "ppt/slides"))
            src_bytes = src.read(base)
            final_zip[new_base] = src_bytes
        elif kind == "theme":
            # Single shared theme: only overwrite if final lacks it; placeholder keeps its own.
            pass
        # notesSlide / other slide-level parts: copy with per-slide name as well
        elif base.startswith("ppt/"):
            new_base = re.sub(r"(slide)\d+(\.xml)", lambda mm: f"{mm.group(1)}{n}{mm.group(2)}", base)
            if base != new_base and base in src_names:
                final_zip[new_base] = src.read(base)
                r.set("Target", posixpath.relpath(new_base, "ppt/slides"))
    rels_xml = ET.tostring(new_rels, xml_declaration=True, encoding="UTF-8")

    final_zip[f"ppt/slides/slide{n}.xml"] = slide_xml
    final_zip[f"ppt/slides/_rels/slide{n}.xml.rels"] = rels_xml

    # Content_Types: add overrides for the new slide part (always present) and
    # defaults for any new media extensions copied.
    ct = final_zip["[Content_Types].xml"].decode()
    ext_overrides = set(re.findall(r'Extension="([^"]+)"', ct))
    part_overrides = set(re.findall(r'PartName="(/ppt/slides/slide\d+\.xml)"', ct))
    if f"/ppt/slides/slide{n}.xml" not in part_overrides:
        ct = ct.replace("</Types>",
            f'<Override PartName="/ppt/slides/slide{n}.xml" '
            f'ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/></Types>')
    for base in list(media_map) + list(font_map):
        new_base = media_map.get(base) or font_map[base]
        ext = new_base.rsplit(".", 1)[-1].lower()
        if ext not in ext_overrides:
            ct = ct.replace("</Types>", f'<Default Extension="{ext}" ContentType="application/octet-stream"/></Types>')
            ext_overrides.add(ext)
    final_zip["[Content_Types].xml"] = ct.encode()
    src.close()


def load(path):
    z = zipfile.ZipFile(path)
    return {i.filename: z.read(i.filename) for i in z.infolist() if not i.is_dir()}


def save(files, out):
    tmp = out + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in files.items():
            z.writestr(name, data)
    shutil.move(tmp, out)


def verify(final_path, slides_dir):
    """Gate: page N of final must be byte-identical slide XML to slide_NNN_recreated.pptx."""
    z = zipfile.ZipFile(final_path)
    names = set(z.namelist())
    mism = []
    replaced = 0
    for fn in sorted(os.listdir(slides_dir)):
        m = re.fullmatch(r"slide_(\d{3})_recreated\.pptx", fn)
        if not m:
            continue
        n = int(m.group(1))
        src = zipfile.ZipFile(os.path.join(slides_dir, fn))
        if f"ppt/slides/slide{n}.xml" not in names:
            mism.append((n, "missing part")); continue
        if z.read(f"ppt/slides/slide{n}.xml") != src.read("ppt/slides/slide1.xml"):
            mism.append((n, "xml differs"))
        else:
            replaced += 1
    return replaced, mism


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--final", required=True)
    ap.add_argument("--slides-dir", required=True)
    ap.add_argument("--out")
    ap.add_argument("--verify-only", action="store_true")
    ap.add_argument("--slide", action="append", default=[])
    a = ap.parse_args()

    if a.verify_only:
        rep, mism = verify(a.final, a.slides_dir)
        print(f"verify: {rep} pages byte-identical to per-slide decks, {len(mism)} mismatched")
        for n, why in mism:
            print(f"  MISMATCH slide {n}: {why}")
        sys.exit(1 if mism else 0)

    files = load(a.final)
    nums = [int(s) for s in a.slide] if a.slide else None
    count = 0
    for fn in sorted(os.listdir(a.slides_dir)):
        m = re.fullmatch(r"slide_(\d{3})_recreated\.pptx", fn)
        if not m:
            continue
        n = int(m.group(1))
        if nums and n not in nums:
            continue
        replace_slide(files, n, os.path.join(a.slides_dir, fn))
        count += 1
        print(f"replaced page {n} <- {fn}")
    out = a.out or a.final
    save(files, out)
    print(f"wrote {out} ({count} pages replaced), md5={sha(open(out,'rb').read())}")


if __name__ == "__main__":
    main()
