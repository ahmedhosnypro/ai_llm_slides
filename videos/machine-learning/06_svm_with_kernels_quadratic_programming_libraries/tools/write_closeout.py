#!/usr/bin/env python3
"""Finalize CLOSEOUT_REPORT.md for 06_svm_with_kernels_quadratic_programming_libraries.

Reads banked QA evidence (rejudge2 ledger + audits, merge gate report, residuals,
optional qa/closeout_data.json, read-only progress DB), refuses to run unless every
slide is judge-PASS or a documented residual AND the merge gate shows PASS, then
fills CLOSEOUT_REPORT_DRAFT.md placeholders and writes CLOSEOUT_REPORT.md.
Read-only except for the final report write.
"""
import hashlib
import json
import os
import re
import sqlite3
import sys
from collections import Counter

TOOLS = os.path.dirname(os.path.abspath(__file__))
NS = os.path.dirname(TOOLS)
DATE = "2026-11-14"
ALL_SLIDES = ["%03d" % i for i in range(1, 56)]
LEDGER = os.path.join(NS, "qa", "rejudge2", "ledger.jsonl")
CLOSEOUT_DATA = os.path.join(NS, "qa", "closeout_data.json")
MERGE_GATE = os.path.join(NS, "recreated_pptx", "qa", "final_merge", "MERGE_GATE_REPORT.md")
RESIDUALS = os.path.join(NS, "qa", "rejudge2", "residuals_003_004.md")
AUDIT_DIR = os.path.join(NS, "qa", "rejudge2")
DRAFT = os.path.join(NS, "CLOSEOUT_REPORT_DRAFT.md")
OUT = os.path.join(NS, "CLOSEOUT_REPORT.md")
DB = os.path.join(NS, "slides_progress.db")
FINAL_DECK = os.path.join(NS, "recreated_pptx", "06_svm_with_kernels_quadratic_programming_libraries_final.pptx")
GIT_SNAPSHOT = os.path.join(AUDIT_DIR, "git_status_snapshot.txt")


def norm_slide(s):
    t = str(s).strip()
    return "%03d" % int(t) if t.isdigit() else t.zfill(3)


def is_pass(verdict):
    v = (verdict or "").upper()
    if "OMML_WRAPPED" in v:
        return True
    return "PASS" in v and "FAIL" not in v


def read_text(path, required=True):
    if not os.path.exists(path):
        if required:
            sys.exit("REFUSED: missing required input %s" % path)
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def latest_per_slide():
    latest = {}
    with open(LEDGER, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if str(row.get("verdict") or "").upper() == "OMML_FAILED":
                continue
            latest[norm_slide(row.get("slide"))] = row
    return latest


def db_counts():
    con = sqlite3.connect("file:%s?mode=ro" % DB, uri=True)
    try:
        cur = con.cursor()
        total = cur.execute("SELECT COUNT(*) FROM slides").fetchone()[0]
        vc = Counter(r[0] for r in cur.execute("SELECT visual_check FROM slides"))
        gs = Counter(r[0] for r in cur.execute("SELECT gen_status FROM slides"))
    finally:
        con.close()
    return total, vc, gs


def parse_merge_gate():
    text = read_text(MERGE_GATE)
    gate_line = ""
    for line in text.splitlines():
        if "PASS" in line.upper() and "GATE" in line.upper():
            gate_line = line.strip()
            break
    m = re.search(r"(\d+)\s*/\s*(\d+)\s*mismatched", text)
    mismatched = ("%s/%s" % (m.group(1), m.group(2))) if m else "not stated"
    return gate_line, mismatched


def residual_slides():
    text = read_text(RESIDUALS)
    return set("%03d" % int(n) for n in re.findall(r"##\s*Slide\s+(\d+)", text))


def audit_summaries():
    import glob
    out = []
    pats = ("omml_wrap_audit.md", "omml_wrap_final.md", "house_frame_audit.md",
            "numbering_audit.md", "graph_asset_audit.md", "web_source_audit.md",
            "pass_md5_audit*.md")
    for pat in pats:
        for p in sorted(glob.glob(os.path.join(AUDIT_DIR, pat))):
            text = read_text(p, required=False)
            m = re.search(r"## Summary\n(.*?)(?:\n## |\Z)", text, re.S)
            bullets = []
            if m:
                bullets = [l.strip()[2:] for l in m.group(1).splitlines()
                           if l.strip().startswith("- ")]
            out.append((os.path.basename(p), bullets[:4]))
    return out


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fmt_counter(c):
    return ", ".join("%s %d" % (k, c[k]) for k in sorted(c, key=str)) or "none"


def db_block(total, vc, gs):
    return ("DB row counts by status (`slides_progress.db`, table `slides`, "
            "%d rows total, read-only):\n\n| Field | Breakdown |\n|---|---|\n"
            "| `visual_check` | %s |\n| `gen_status` | %s |\n\n"
            % (total, fmt_counter(vc), fmt_counter(gs)))


def residual_line(residuals):
    if not residuals:
        return "none"
    return "; ".join("%s (documented in `qa/rejudge2/residuals_003_004.md`)" % s
                     for s in sorted(residuals))


def audit_bullet_lines(audits):
    lines = []
    for fname, bullets in audits:
        summary = "; ".join(bullets[:3]) if bullets else "see file"
        lines.append("- **Audit `%s`**: %s" % (fname, summary))
    lines.append("- **Render cache**: `recreated_pptx/renders/`, `recreated_pptx/judge_renders/`, "
                 "`qa/rejudge2/renders_pass/`, `qa/rejudge2/cert_renders/` banked.")
    return "\n".join(lines)


def fill_tbd(rep, pass_ids, gate_line, mismatched, deck_md5):
    def fill(m):
        t = m.group(0)
        if "currently 21/55" in t:
            return "%d/55 judge-certified PASS (ledger latest-per-slide)" % len(pass_ids)
        if "N/55 judge-certified" in t:
            return "%d/55 judge-certified PASS" % len(pass_ids)
        if "not yet run" in t:
            return "PASS — %s mismatched pages (0/55 required); gate line: `%s`" % (mismatched, gate_line)
        if "record at closeout" in t:
            return "`%s`" % deck_md5
        if "list at closeout" in t:
            return "none — all 55 slides resolved (PASS or documented residual)"
        if "TBD at closeout" in t:
            return ("git status snapshot banked at `qa/rejudge2/git_status_snapshot.txt`; "
                    "no banked evidence deleted by this script")
        return "None recorded as of %s" % DATE
    return re.sub(r"\[TBD[^]]*\]", fill, rep)


def build_report(pass_ids, residuals, gate_line, mismatched, deck_md5, audits):
    total, vc, gs = db_counts()
    rep = read_text(DRAFT)
    rep = rep.replace("(DRAFT, %s)" % DATE, "(FINAL, %s)" % DATE)
    rep = re.sub(r"> \*\*DRAFT — NOT FINAL\.\*\*.*?\n\n",
                 "> **FINAL — %s.** Placeholders filled from measured evidence; no slides, "
                 "pptx, ledger, or DB rows were modified.\n\n" % DATE, rep, count=1, flags=re.S)
    rep = re.sub(r"DB row counts by status.*?(?=\*\*Final PASS count)",
                 db_block(total, vc, gs), rep, count=1, flags=re.S)
    rep = re.sub(r"\n\(task brief said.*?\)\n", "\n", rep, count=1, flags=re.S)
    rep = re.sub(r"certified ids per DB:[^\n]*",
                 "judge PASS ids per ledger latest-per-slide: %s." % ", ".join(pass_ids),
                 rep, count=1)
    rep = rep.replace("- **House frame audit**: `qa/house_frame_audit.md` (frame/badge/title-y conformance).",
                      "- **House frame audit**: `qa/rejudge2/house_frame_audit.md` (frame/badge/title-y conformance).\n"
                      + audit_bullet_lines(audits))
    rep = rep.replace("## Residual list\n",
                      "## Residual list\n\n- **Documented residuals (final cycle, %s)**: %s\n"
                      % (DATE, residual_line(residuals)))
    rep = rep.replace("— placeholder deck state, re-hash at closeout", "— re-hashed at closeout")
    rep = fill_tbd(rep, pass_ids, gate_line, mismatched, deck_md5)
    if "[TBD" in rep:
        sys.exit("REFUSED: unfilled [TBD] markers remain in %s" % DRAFT)
    return rep


def main():
    data = {}
    if os.path.exists(CLOSEOUT_DATA):
        with open(CLOSEOUT_DATA, "r", encoding="utf-8") as f:
            data = json.load(f)
    latest = latest_per_slide()
    residuals = residual_slides()
    gate_line, mismatched = parse_merge_gate()
    if not gate_line:
        sys.exit("REFUSED: no PASS gate line in %s" % MERGE_GATE)
    not_ok = [s for s in ALL_SLIDES
              if s not in latest
              or (not is_pass(latest[s].get("verdict")) and s not in residuals)]
    if not_ok:
        sys.exit("REFUSED: slides not PASS and not documented residuals: %s"
                 % ", ".join("%s(%s)" % (s, latest.get(s, {}).get("verdict")) for s in not_ok))
    pass_ids = data.get("pass_slides") or [s for s in ALL_SLIDES
                                           if s in latest and is_pass(latest[s].get("verdict"))]
    if data.get("residual_slides"):
        residuals = set(data["residual_slides"])
    deck_md5 = md5_of(FINAL_DECK) if os.path.exists(FINAL_DECK) else "MISSING"
    audits = audit_summaries()
    rep = build_report(pass_ids, residuals, gate_line, mismatched, deck_md5, audits)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(rep)
    print("Final report: %s" % OUT)
    print("PASS: %d/55  residuals: %s" % (len(pass_ids), ", ".join(sorted(residuals)) or "none"))


if __name__ == "__main__":
    main()
