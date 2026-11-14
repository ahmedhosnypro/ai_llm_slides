#!/usr/bin/env python3
"""Regenerate qa/closeout_data.json for 06_svm_with_kernels_quadratic_programming_libraries.

Reads current state only: qa/rejudge2/ledger.jsonl (latest row per slide in file
order wins; verdicts containing 'PASS' normalized to PASS), residual list from
'## Slide NNN' headings in qa/rejudge2/residuals_003_004.md, file inventory of
recreated_pptx/ (55 slide pptx + final deck/pdf + md5s), and counts in analysis/,
web_sources/, qa/reanalysis2/. Read-only except the JSON write. The progress DB
is intentionally NOT read (owned by other workers).
"""
import glob
import hashlib
import json
import os
import re
from collections import Counter
from datetime import datetime, timezone

TOOLS = os.path.dirname(os.path.abspath(__file__))
NS = os.path.dirname(TOOLS)
LEDGER = os.path.join(NS, "qa", "rejudge2", "ledger.jsonl")
RESIDUALS = os.path.join(NS, "qa", "rejudge2", "residuals_003_004.md")
PPTX_DIR = os.path.join(NS, "recreated_pptx")
OUT = os.path.join(NS, "qa", "closeout_data.json")
ALL_SLIDES = ["%03d" % i for i in range(1, 56)]
DECK = "06_svm_with_kernels_quadratic_programming_libraries_final.pptx"


def norm_slide(s):
    t = str(s).strip()
    return "%03d" % int(t) if t.isdigit() else t.zfill(3)


def norm_verdict(v):
    v = (v or "").strip()
    return "PASS" if "PASS" in v.upper() else v


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def latest_per_slide():
    latest = {}
    rows = 0
    with open(LEDGER, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            rows += 1
            row["_line"] = lineno
            latest[norm_slide(row.get("slide"))] = row
    return rows, latest


def residual_list():
    out = []
    with open(RESIDUALS, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"##\s*Slide\s+(\d+)\s*(.*)", line)
            if m:
                out.append({"slide": "%03d" % int(m.group(1)),
                            "heading": line.strip()})
    return out

def pptx_path(slide):
    return os.path.join(PPTX_DIR, "slide_%s_recreated.pptx" % slide)


def inventory():
    slides = {}
    for s in ALL_SLIDES:
        p = pptx_path(s)
        on_disk = os.path.exists(p)
        slides[s] = {
            "file": "recreated_pptx/slide_%s_recreated.pptx" % s,
            "on_disk": on_disk,
            "md5": md5_of(p) if on_disk else None,
            "size_bytes": os.path.getsize(p) if on_disk else None,
        }
    deck = os.path.join(PPTX_DIR, DECK)
    deck_pdf = deck[:-5] + ".pdf"

    def finfo(p, rel):
        return {"file": rel, "on_disk": os.path.exists(p),
                "md5": md5_of(p) if os.path.exists(p) else None,
                "size_bytes": os.path.getsize(p) if os.path.exists(p) else None}

    final = {
        "pptx": finfo(deck, "recreated_pptx/" + DECK),
        "pdf": finfo(deck_pdf, "recreated_pptx/" + DECK[:-5] + ".pdf"),
        "md5_sidecar_files_on_disk": len(glob.glob(os.path.join(PPTX_DIR, "*.md5"))),
    }
    return slides, final


def counts(rows):
    def n(pat):
        return len(glob.glob(os.path.join(NS, pat)))

    with open(os.path.join(NS, "analysis", "slides_final.json"), encoding="utf-8") as f:
        final_len = len(json.load(f))
    return {
        "unique_slides_jpgs": n("unique_slides/slide_*.jpg"),
        "analysis_raw_json": n("analysis/slide_*_raw.json"),
        "analysis_final_json": n("analysis/slide_*_final.json"),
        "slides_final_json_length": final_len,
        "recreated_slide_pptx": n("recreated_pptx/slide_*_recreated.pptx"),
        "web_sources_dirs": n("web_sources/slide_*"),
        "web_sources_SOURCES_md": n("web_sources/slide_*/SOURCES.md"),
        "reanalysis2_transcripts": n("qa/reanalysis2/slide_*_analysis.txt"),
        "ledger_rows": rows,
    }

def main():
    rows, latest = latest_per_slide()
    residuals = residual_list()
    inv, final = inventory()
    per_slide = {}
    pass_ids = []
    unresolved = []
    for s in ALL_SLIDES:
        row = latest.get(s)
        if row is None:
            per_slide[s] = {"slide": s, "verdict": None, "in_ledger": False}
            unresolved.append({"slide": s, "verdict": None,
                               "reason": "no ledger row"})
            continue
        v = norm_verdict(row.get("verdict"))
        disk = inv[s]
        entry = {
            "slide": s,
            "verdict": v,
            "raw_verdict": row.get("verdict"),
            "pptx_md5": row.get("pptx_md5"),
            "ts": row.get("ts"),
            "transcript": row.get("transcript"),
            "ledger_line": row["_line"],
            "pptx_on_disk": disk["on_disk"],
            "pptx_md5_disk": disk["md5"],
            "md5_matches_ledger": (
                row.get("pptx_md5") == disk["md5"]
                if disk["on_disk"] and row.get("pptx_md5") else None),
        }
        per_slide[s] = entry
        if v == "PASS":
            pass_ids.append(s)
        else:
            unresolved.append(entry)
    verdict_counts = Counter(norm_verdict(r.get("verdict")) for r in latest.values())
    data = {
        "namespace": "videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries",
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "note": ("ledger.jsonl is live (workers appending); latest row per slide in file "
                 "order wins; verdicts containing 'PASS' normalized to PASS. No slides, "
                 "pptx, ledger, or DB modified; progress DB not read (owned by other workers)."),
        "sources": {
            "ledger": "qa/rejudge2/ledger.jsonl",
            "residuals": "qa/rejudge2/residuals_003_004.md",
            "file_inventory": "recreated_pptx/",
        },
        "ledger": {
            "rows_total": rows,
            "slides_covered": len(latest),
            "latest_verdict_counts": dict(sorted(verdict_counts.items())),
            "pass_count": len(pass_ids),
            "pass": pass_ids,
            "unresolved_count": len(unresolved),
            "unresolved": unresolved,
            "per_slide": per_slide,
        },
        "residuals": {
            "source": "qa/rejudge2/residuals_003_004.md",
            "count": len(residuals),
            "slides": [r["slide"] for r in residuals],
            "entries": residuals,
        },
        "recreated_pptx_inventory": {
            "slide_pptx": inv,
            "final_deck": final,
        },
        "counts": counts(rows),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
        f.write("\n")
    print("wrote %s" % OUT)
    print("ledger rows=%d slides=%d PASS=%d unresolved=%d residuals=%d"
          % (rows, len(latest), len(pass_ids), len(unresolved), len(residuals)))


if __name__ == "__main__":
    main()
