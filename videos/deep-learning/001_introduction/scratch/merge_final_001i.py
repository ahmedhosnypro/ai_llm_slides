#!/usr/bin/env python3
"""merge_final_001i.py — all-in-one deck merge for 001_introduction.

OPC-level lossless merge modeled on the certified ml-intro final-deck-merge
pattern (skill: .agents/skills/slide-recreation/patterns/final-deck-merge/ +
memory lesson 2026-10-10 "Lossless one-deck merge"):

  - certified set is taken LIVE from slides_progress.db
    (gen_status='passed' AND visual_check='PASS', ordered by slide_id) —
    NEVER a hardcoded list;
  - each source deck's ppt/slides/slide1.xml is copied VERBATIM as
    slideN.xml (rIds are per-slide — zero slide-XML edits; decks carrying
    mc:AlternateContent / OMML wraps copy verbatim like any slide XML);
  - media is renamed per slide (imgNNN_<orig>) because pptxgenjs names
    (image-1-K.png) collide across decks;
  - only the slide's .rels is retargeted: layout -> shared skeleton layout,
    notesSlide -> per-slide copy, media -> renamed file;
  - the per-slide notesSlide copy gets its own .rels retargeted
    (its back-reference ../slides/slide1.xml -> ../slides/slideN.xml);
  - presentation.xml / presentation.xml.rels / [Content_Types].xml are
    rebuilt for N slides;
  - skeleton parts (master/layout/theme/notesMaster/presProps/tableStyles/
    viewProps/docProps/_rels/.rels) come from the first certified source and
    are md5-checked against EVERY other source (fail loud on mismatch);
  - every slide XML / media / notes part is byte-verified against its source
    after writing (fail loud).

Usage:
  python3 merge_final_001i.py [-o OUT.pptx] [--db DB] [--pptx-dir DIR]

Default OUT: recreated_pptx/001_introduction_final.pptx
(only produce that once the deck is COMPLETE — for the partial-merge
validation pass -o scratch/merge_gate_002/partial_merge.pptx).

Exit 0 = merge written and byte-verified. Exit 1 = any law violated.
"""

import argparse
import hashlib
import re
import sqlite3
import sys
import zipfile
from pathlib import Path

VIDEO = Path(__file__).resolve().parent.parent  # .../001_introduction
DEFAULT_OUT = VIDEO / "recreated_pptx" / "001_introduction_final.pptx"
DEFAULT_DB = VIDEO / "slides_progress.db"
DEFAULT_PPTX_DIR = VIDEO / "recreated_pptx"

SKELETON_PARTS = [
    "ppt/theme/theme1.xml",
    "ppt/slideMasters/slideMaster1.xml",
    "ppt/slideMasters/_rels/slideMaster1.xml.rels",
    "ppt/slideLayouts/slideLayout1.xml",
    "ppt/slideLayouts/_rels/slideLayout1.xml.rels",
    "ppt/notesMasters/notesMaster1.xml",
    "ppt/notesMasters/_rels/notesMaster1.xml.rels",
    "ppt/presProps.xml",
    "ppt/tableStyles.xml",
    "ppt/viewProps.xml",
    "ppt/presentation.xml",
    "ppt/_rels/presentation.xml.rels",
    "[Content_Types].xml",
    "_rels/.rels",
    "docProps/app.xml",
]

# taken verbatim from the FIRST certified source, not md5-checked across sources:
# docProps/core.xml only carries per-deck creation timestamps (pptxgenjs metadata,
# zero rendering relevance — measured: 51 distinct hashes, all content identical).
FROM_FIRST_SOURCE = ["docProps/core.xml"]

NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
CT_SLIDE = f"{NS_R}/slide"
CT_LAYOUT = f"{NS_R}/slideLayout"
CT_NOTES = f"{NS_R}/notesSlide"
CT_IMAGE = f"{NS_R}/image"

# relationship types a slide part may carry in these decks (pptxgenjs)
ALLOWED_SLIDE_REL_TYPES = {CT_LAYOUT, CT_NOTES, CT_IMAGE}

MEDIA_TARGET_RE = re.compile(r"^\.\./media/([^/]+)$")


def md5(b: bytes) -> str:
    return hashlib.md5(b).hexdigest()


def load_certified(db_path: Path) -> list[int]:
    """LIVE query — the certified set is whatever the DB says right now."""
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        rows = con.execute(
            "SELECT slide_id FROM slides "
            "WHERE gen_status='passed' AND visual_check='PASS' "
            "ORDER BY slide_id"
        ).fetchall()
    finally:
        con.close()
    return [r[0] for r in rows]


def source_path(pptx_dir: Path, sid: int) -> Path:
    return pptx_dir / f"slide_{sid:03d}_recreated.pptx"


def rewrite_rels(rels_xml: bytes, retargets: dict[str, str]) -> bytes:
    """Retarget ONLY Target= values, by relationship Type. Everything else in
    the .rels part stays byte-identical."""
    text = rels_xml.decode("utf-8")

    def repl(m: re.Match) -> str:
        rid, rtype, target = m.group(1), m.group(2), m.group(3)
        if rtype == CT_IMAGE:
            mt = MEDIA_TARGET_RE.match(target)
            if not mt:
                raise SystemExit(f"FAIL: unexpected image rel target {target!r}")
            new = retargets.get(target)
            if new is None:
                raise SystemExit(f"FAIL: image rel target {target!r} not in retarget map")
            return f'<Relationship Id="{rid}" Type="{rtype}" Target="{new}"/>'
        if rtype in (CT_LAYOUT, CT_NOTES):
            new = retargets.get(target, target)  # layout target passes through
            return f'<Relationship Id="{rid}" Type="{rtype}" Target="{new}"/>'
        raise SystemExit(
            f"FAIL: unexpected relationship type {rtype!r} (target {target!r}) "
            f"— extend ALLOWED_SLIDE_REL_TYPES consciously, never copy blind"
        )

    # tolerate attribute order variations used by pptxgenjs (Id/Type/Target fixed order
    # in these decks, but match generally)
    pat = re.compile(
        r'<Relationship\b[^>]*?\bId="([^"]+)"[^>]*?\bType="([^"]+)"[^>]*?\bTarget="([^"]+)"[^>]*?/>'
    )
    new_text, n = pat.subn(repl, text)
    if n != len(re.findall(r"<Relationship\b", text)):
        raise SystemExit("FAIL: .rels rewrite did not cover every Relationship element")
    return new_text.encode("utf-8")


def rebuild_presentation(tpl_pres: bytes, tpl_pres_rels: bytes, n: int) -> tuple[bytes, bytes]:
    """presentation.xml + rels rebuilt for N slides (sldId ids 256..255+N).
    Only the sldIdLst / slide rels entries change; every NON-slide rId keeps its
    template value (master rId1, notesMaster rId3, presProps rId4, viewProps
    rId5, theme rId6, tableStyles rId7) so no r:id in presentation.xml ever
    dangles — a dangling notesMasterId made LO discard the page size and fall
    back to its 28cm x 15.75cm default (measured). Slides take rId8..rId(7+N);
    rIds need not be contiguous."""
    pres = tpl_pres.decode("utf-8")
    old_lst = re.search(r"<p:sldIdLst>.*?</p:sldIdLst>", pres, re.S)
    if not old_lst:
        raise SystemExit("FAIL: template presentation.xml has no sldIdLst")
    new_lst = "<p:sldIdLst>" + "".join(
        f'<p:sldId id="{255 + i}" r:id="rId{7 + i}"/>' for i in range(1, n + 1)
    ) + "</p:sldIdLst>"
    pres = pres[: old_lst.start()] + new_lst + pres[old_lst.end():]

    rels = tpl_pres_rels.decode("utf-8")
    old_slide_rel = re.search(
        r'<Relationship [^>]*Type="' + re.escape(CT_SLIDE) + r'"[^>]*/>', rels
    )
    if not old_slide_rel:
        raise SystemExit("FAIL: template presentation.xml.rels has no slide rel")
    slide_rels = "".join(
        f'<Relationship Id="rId{7 + i}" Type="{CT_SLIDE}" '
        f'Target="slides/slide{i}.xml"/>'
        for i in range(1, n + 1)
    )
    rels = rels[: old_slide_rel.start()] + slide_rels + rels[old_slide_rel.end():]
    return pres.encode("utf-8"), rels.encode("utf-8")


def rebuild_content_types(tpl_ct: bytes, n: int) -> bytes:
    """Defaults verbatim from the template + Overrides for N slides and
    N notesSlides."""
    ct = tpl_ct.decode("utf-8")
    defaults = re.findall(r"<Default [^>]*/>", ct)
    if not defaults:
        raise SystemExit("FAIL: template Content_Types has no Defaults")
    overrides = [
        '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>',
        '<Override PartName="/ppt/notesMasters/notesMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesMaster+xml"/>',
        '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>',
        '<Override PartName="/ppt/presProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"/>',
        '<Override PartName="/ppt/viewProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml"/>',
        '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>',
        '<Override PartName="/ppt/tableStyles.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml"/>',
        '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>',
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
    ]
    for i in range(1, n + 1):
        overrides.append(
            f'<Override PartName="/ppt/slides/slide{i}.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        )
        overrides.append(
            f'<Override PartName="/ppt/notesSlides/notesSlide{i}.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/>'
        )
    body = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        + "".join(defaults) + "".join(overrides) + "</Types>"
    )
    return body.encode("utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--db", type=Path, default=DEFAULT_DB)
    ap.add_argument("--pptx-dir", type=Path, default=DEFAULT_PPTX_DIR)
    args = ap.parse_args()

    certified = load_certified(args.db)
    if not certified:
        raise SystemExit("FAIL: no certified slides in DB (gen_status='passed' AND visual_check='PASS')")
    print(f"[merge] certified set (LIVE from DB): {len(certified)} slides")
    print(f"[merge] slide ids: {certified}")

    srcs = []
    for sid in certified:
        p = source_path(args.pptx_dir, sid)
        if not p.is_file():
            raise SystemExit(f"FAIL: certified slide {sid} has no package: {p}")
        srcs.append((sid, zipfile.ZipFile(p)))

    # ---- skeleton byte-check across ALL sources -----------------------------
    skel: dict[str, bytes] = {}
    for part in SKELETON_PARTS + FROM_FIRST_SOURCE:
        if part not in srcs[0][1].namelist():
            raise SystemExit(f"FAIL: skeleton part {part} missing from first source")
        skel[part] = srcs[0][1].read(part)
    for sid, z in srcs[1:]:
        for part in SKELETON_PARTS:
            if part in z.namelist():
                if md5(z.read(part)) != md5(skel[part]):
                    raise SystemExit(
                        f"FAIL: skeleton part {part} differs in slide {sid} "
                        f"(md5 {md5(z.read(part))} != {md5(skel[part])}) — per the law, "
                        f"a different-toolchain source must be handled consciously"
                    )
    print(f"[merge] skeleton byte-check: {len(SKELETON_PARTS)} parts identical across all {len(certified)} sources")

    # ---- assemble merged part map -------------------------------------------
    n = len(certified)
    parts: dict[str, bytes] = dict(skel)  # shared skeleton verbatim

    pres_tpl = skel["ppt/presentation.xml"]
    pres_rels_tpl = skel["ppt/_rels/presentation.xml.rels"]
    pres, pres_rels = rebuild_presentation(pres_tpl, pres_rels_tpl, n)
    parts["ppt/presentation.xml"] = pres
    parts["ppt/_rels/presentation.xml.rels"] = pres_rels
    parts["[Content_Types].xml"] = rebuild_content_types(skel["[Content_Types].xml"], n)

    for i, (sid, z) in enumerate(srcs, start=1):
        # slide XML: VERBATIM, zero edits (rIds are per-slide)
        slide_xml = z.read("ppt/slides/slide1.xml")
        parts[f"ppt/slides/slide{i}.xml"] = slide_xml

        # slide .rels: retarget notesSlide + media; layout target passes through
        rels = z.read("ppt/slides/_rels/slide1.xml.rels")
        retargets: dict[str, str] = {
            "../notesSlides/notesSlide1.xml": f"../notesSlides/notesSlide{i}.xml"
        }
        media_map: dict[str, bytes] = {}
        for m in re.finditer(r'Type="' + re.escape(CT_IMAGE) + r'" Target="([^"]+)"', rels.decode("utf-8")):
            target = m.group(1)
            mt = MEDIA_TARGET_RE.match(target)
            if not mt:
                raise SystemExit(f"FAIL: slide {sid}: bad media target {target!r}")
            orig = mt.group(1)
            new_target = f"../media/img{i:03d}_{orig}"
            retargets[target] = new_target
            if target in media_map:
                raise SystemExit(f"FAIL: slide {sid}: duplicate media rel target {target!r}")
            media_map[new_target] = z.read(f"ppt/media/{orig}")
        parts[f"ppt/slides/_rels/slide{i}.xml.rels"] = rewrite_rels(rels, retargets)

        # media: verbatim bytes, renamed per slide
        for new_target, blob in media_map.items():
            parts[f"ppt/media/{new_target.split('/')[-1]}"] = blob

        # notesSlide: per-slide copy (verbatim); its .rels carries notesMaster +
        # slide types — retarget ONLY the slide back-reference to this slide
        parts[f"ppt/notesSlides/notesSlide{i}.xml"] = z.read("ppt/notesSlides/notesSlide1.xml")
        notes_rels = z.read("ppt/notesSlides/_rels/notesSlide1.xml.rels").decode("utf-8")
        notes_rels, nsub = re.subn(
            r'(Type="' + re.escape(CT_SLIDE) + r'" Target="\.\./slides/)slide1\.xml(")',
            rf"\g<1>slide{i}.xml\g<2>", notes_rels,
        )
        if nsub != 1:
            raise SystemExit(f"FAIL: slide {sid}: notesSlide rels slide back-reference not found/ambiguous")
        parts[f"ppt/notesSlides/_rels/notesSlide{i}.xml.rels"] = notes_rels.encode("utf-8")

    # sanity: every rels target inside the package must resolve to a part
    for part_name, blob in parts.items():
        if part_name.endswith(".rels"):
            base = part_name.rsplit("_rels/", 1)[0]
            for m in re.finditer(r'Target="([^"]+)"', blob.decode("utf-8")):
                tgt = m.group(1)
                if tgt.startswith(("http", "/")):
                    continue
                resolved = str(Path(base, tgt).as_posix()) if base else tgt
                norm = re.sub(r"(?<!:)/+", "/", resolved)
                # normalize ../ segments
                stack: list[str] = []
                for seg in norm.split("/"):
                    if seg == "..":
                        if not stack:
                            raise SystemExit(f"FAIL: {part_name}: target {tgt!r} escapes package")
                        stack.pop()
                    elif seg not in (".", ""):
                        stack.append(seg)
                if "/".join(stack) not in parts:
                    raise SystemExit(
                        f"FAIL: {part_name}: rel target {tgt!r} -> {'/'.join(stack)} missing in merged package"
                    )
    print(f"[merge] rel-target resolution check: all targets resolve ({len(parts)} parts)")

    # every r:id in presentation.xml must resolve in its rels (a dangling
    # notesMasterId made LO discard sldSz and render at default page size)
    pres_ids = set(re.findall(r'r:id="(rId\d+)"', parts["ppt/presentation.xml"].decode("utf-8")))
    rel_ids = set(re.findall(r'Id="(rId\d+)"', parts["ppt/_rels/presentation.xml.rels"].decode("utf-8")))
    dangling = pres_ids - rel_ids
    if dangling:
        raise SystemExit(f"FAIL: presentation.xml references {sorted(dangling)} absent from its .rels")
    print(f"[merge] r:id consistency: all {len(pres_ids)} presentation r:ids resolve")

    # ---- write deterministically -------------------------------------------
    # rebuilt parts must be well-formed XML before we write anything
    import xml.etree.ElementTree as ET
    for pn in (["ppt/presentation.xml", "ppt/_rels/presentation.xml.rels",
                "[Content_Types].xml"]
               + [k for k in parts if k.endswith(".rels")]):
        try:
            ET.fromstring(parts[pn])
        except ET.ParseError as e:
            raise SystemExit(f"FAIL: rebuilt part {pn} is not well-formed XML: {e}")
    print(f"[merge] XML well-formedness: presentation/rels/Content_Types + all .rels parse OK")
    out = args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    order = sorted(parts)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in order:
            zi = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(zi, parts[name])
    print(f"[merge] wrote {out} ({out.stat().st_size} bytes, {len(order)} parts, {n} slides)")

    # ---- byte-verification pass ---------------------------------------------
    with zipfile.ZipFile(out) as mz:
        merged_names = set(mz.namelist())
        for i, (sid, z) in enumerate(srcs, start=1):
            if mz.read(f"ppt/slides/slide{i}.xml") != z.read("ppt/slides/slide1.xml"):
                raise SystemExit(f"FAIL: slide {sid}: merged slide{i}.xml not byte-verbatim")
            src_rels = z.read("ppt/slides/_rels/slide1.xml.rels")
            mrg_rels = mz.read(f"ppt/slides/_rels/slide{i}.xml.rels")
            # only Target= values may differ
            st = re.findall(r'Target="([^"]+)"', src_rels.decode("utf-8"))
            mt = re.findall(r'Target="([^"]+)"', mrg_rels.decode("utf-8"))
            if len(st) != len(mt) or len(st) != len(re.findall(r"<Relationship\b", mrg_rels.decode("utf-8"))):
                raise SystemExit(f"FAIL: slide {sid}: rels count changed")
            # layout target must pass through unchanged
            if CT_LAYOUT not in mrg_rels.decode("utf-8") or "../slideLayouts/slideLayout1.xml" not in mt:
                raise SystemExit(f"FAIL: slide {sid}: layout retarget wrong")
            for m in re.finditer(r'Type="' + re.escape(CT_IMAGE) + r'" Target="([^"]+)"', mrg_rels.decode("utf-8")):
                merged_media = f"ppt/media/{m.group(1).split('/')[-1]}"
                orig = m.group(1).split(f"img{i:03d}_", 1)[-1]
                if merged_media not in merged_names:
                    raise SystemExit(f"FAIL: slide {sid}: media {merged_media} missing")
                if mz.read(merged_media) != z.read(f"ppt/media/{orig}"):
                    raise SystemExit(f"FAIL: slide {sid}: media {merged_media} not byte-verbatim")
            if mz.read(f"ppt/notesSlides/notesSlide{i}.xml") != z.read("ppt/notesSlides/notesSlide1.xml"):
                raise SystemExit(f"FAIL: slide {sid}: notesSlide not byte-verbatim")
    for z in (z for _, z in srcs):
        z.close()
    print(f"[merge] byte-verification: {n} slide XMLs + media + notes ALL byte-verbatim vs sources")
    print(f"[merge] OK: {out}")


if __name__ == "__main__":
    main()
