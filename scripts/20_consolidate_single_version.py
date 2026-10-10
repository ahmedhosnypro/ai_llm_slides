#!/usr/bin/env python3
"""Consolidate to ONE version per slide (founder directive 2026-10-10).

End state: for each slide 1..64 exactly one pptx named `slide_NNN_recreated.pptx`
(NO suffix) — the variant with the graph/OMML baked in; superseded builds live only
in QA evidence dirs.

Steps:
1. Verify every slide's FINAL variant exists (omml > graphed > base). Slide 54's
   omml MUST exist before this runs (its content fix + rewrap complete first).
2. For slides that HAVE a variant (graphed or omml): archive the plain-named base
   build script into the slide's QA dir (provenance), then DELETE the plain-named
   base pptx and the plain-named build script.
3. Rename the variant pptx → plain name; rename `build/slide_NNN_graphed.js` →
   `build/slide_NNN.js` (graph slides; if the live graphed build script lives only
   in the slide's graphgen dir, copy it into build/ under the plain name).
4. Print the inventory. DB pptx_path/build_script updates are done by the caller
   (orchestrator) after reviewing the printed map.

Usage: python3 scripts/20_consolidate_single_version.py <recreated_pptx_dir>
"""

import re
import shutil
import sys
from pathlib import Path


def main() -> None:
    d = Path(sys.argv[1])
    build = d / "build"

    omml = {int(p.stem.split("_")[1]): p for p in d.glob("slide_*_recreated_omml.pptx")}
    graphed = {int(p.stem.split("_")[1]): p for p in d.glob("slide_*_recreated_graphed.pptx")}
    base = {int(p.stem.split("_")[1]): p for p in d.glob("slide_*_recreated.pptx")}

    # 1. final variant must exist for all 64
    finals = {}
    for n in range(1, 65):
        if n in omml:
            finals[n] = ("omml", omml[n])
        elif n in graphed:
            finals[n] = ("graphed", graphed[n])
        elif n in base:
            finals[n] = ("base", base[n])
        else:
            sys.exit(f"FATAL: no pptx at all for slide {n}")
    missing_variant = [n for n, (v, _) in finals.items() if v != "base" and n not in omml and n not in graphed]
    # slide 54's omml is required (its rewrap must have completed)
    if 54 not in omml:
        sys.exit("FATAL: slide 54's omml pptx does not exist yet — its content fix + "
                 "OMML rewrap must complete before consolidation")

    renamed, deleted, archived = [], [], []
    for n, (variant, path) in sorted(finals.items()):
        plain = d / f"slide_{n:03d}_recreated.pptx"
        if variant == "base":
            continue  # the plain pptx IS the final version
        # 2a. archive the base build script into QA (provenance) before deleting
        base_build = build / f"slide_{n:03d}.js"
        qa_dirs = sorted(d.glob(f"qa/slide{n:03d}")) + sorted(d.glob(f"qa/slide{n}/"))
        qa_dir = qa_dirs[0] if qa_dirs else None
        if base_build.exists():
            if qa_dir:
                dest = qa_dir / "base_build_archived_single_version.js"
                shutil.copy2(base_build, dest)
                archived.append(str(dest))
            base_build.unlink()
            deleted.append(str(base_build))
        # 2b. delete the plain-named base pptx (superseded by the variant)
        if plain.exists():
            plain.unlink()
            deleted.append(str(plain))
        # 3a. rename variant pptx -> plain name
        path.rename(plain)
        renamed.append(f"{path.name} -> {plain.name}")
        # 3b. rename the variant build script -> plain name
        gbuild = build / f"slide_{n:03d}_graphed.js"
        if gbuild.exists():
            gbuild.rename(build / f"slide_{n:03d}.js")
            renamed.append(f"build/slide_{n:03d}_graphed.js -> build/slide_{n:03d}.js")
        else:
            # live graphed build script may live in the graphgen dir
            cands = sorted(list(d.glob(f"qa/slide{n:03d}/graphgen/build_graphed*.js"))
                           + list(d.glob(f"qa/slide{n}/graphgen/build_graphed*.js")))
            if cands:
                latest = max(cands, key=lambda p: p.stat().st_mtime)
                shutil.copy2(latest, build / f"slide_{n:03d}.js")
                renamed.append(f"{latest.name} copied -> build/slide_{n:03d}.js")

    # inventory
    print(f"final pptx per slide (single version, plain names):")
    counts = {"omml": 0, "graphed": 0, "base": 0}
    for n, (v, _) in sorted(finals.items()):
        counts[v] += 1
    print(f"  {counts}")
    print(f"\nrenamed ({len(renamed)}):")
    for r in renamed:
        print(f"  {r}")
    print(f"\ndeleted ({len(deleted)}):")
    for x in deleted:
        print(f"  {x}")
    print(f"\nbase builds archived to QA ({len(archived)}):")
    for a in archived:
        print(f"  {a}")

    # post-condition: exactly one pptx per slide, all plain-named
    all_pptx = sorted(p.name for p in d.glob("slide_*_recreated*.pptx"))
    bad = [p for p in all_pptx if not re.fullmatch(r"slide_\d{3}_recreated\.pptx", p)]
    print(f"\npost-condition: {len(all_pptx)} slide pptx, non-plain-named leftovers: {bad if bad else 'NONE'}")


if __name__ == "__main__":
    main()
