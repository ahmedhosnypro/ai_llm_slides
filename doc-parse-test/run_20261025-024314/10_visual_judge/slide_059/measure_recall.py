#!/usr/bin/env python3
"""Union text-recall of doc-parse transcripts vs the frozen 46-string GT inventory.

Classification = wave-2 comparison contract (05_comparison/slide_059_comparison.md §1):
  EXACT      case/whitespace-insensitive equality (whole line or token multiset)
  NORMALIZED equal after a named normalization — intact single-token containment
             (merge survivor), underscore/punctuation collapse (incl. subscript
             fold), the disclosed symbol glyph-confusion fold (I/l->1, O->0,
             symbol strings <=5 chars only), or a multiword GT surviving a line
             merge as a contiguous substring
  PARTIAL    GT present contiguously (chars) inside a line that carries stray
             extra glyphs (e.g. parse "1C1" for GT "C1")
  MISSING    no match
Each string is counted at its BEST class across the union of transcripts.
Weights: EXACT 1.0, NORMALIZED 1.0, PARTIAL 0.5 (recall = weighted / 46).
Coordinate tokens (<x_..>, <y_..>) and class tokens (<class_..>) are stripped.
Disclosed folds: subscript/superscript -> ASCII; sigma variants -> SIGMA;
minus/dash variants -> removed (punctuation). Baseline anchor: this matcher
reproduces wave-2's 27/46 = 58.7% on call01_pass1.
"""
import sys, os, re, glob, json, unicodedata

# (id, GT string, occurrences)
GT = [
    (1, "Transformer Encoder", 1), (2, "Transformer Block", 3),
    (3, "Global Average Pooling", 1), (4, "Softmax Layer", 1),
    (5, "Softmax", 3), (6, "Σ", 3), (7, "+", 1), (8, "Output Classes", 1),
    (9, "C₁", 1), (10, "C₂", 1), (11, "C₃", 1),
    (12, "X₀", 1), (13, "X₁", 1), (14, "X₂", 1), (15, "X₃", 1),
    (16, "X₄", 1), (17, "X₅", 1), (18, "X_{N-2}", 1), (19, "X_{N-1}", 1),
    (20, "Y₀", 1), (21, "Y₁", 1), (22, "Y₂", 1), (23, "Y₃", 1),
    (24, "Y₄", 1), (25, "Y₅", 1), (26, "Y_{N-2}", 1), (27, "Y_{N-1}", 1),
    (28, "Vector_{P0}", 1), (29, "Vector_{P1}", 1), (30, "Vector_{P2}", 1),
    (31, "Vector_{P3}", 1), (32, "Vector_{P4}", 1), (33, "Vector_{P5}", 1),
    (34, "Vector_{PN-2}", 1), (35, "Vector_{PN-1}", 1),
    (36, "Single vector representing", 1), (37, "the whole sequence", 1),
    (38, "Output", 1), (39, "Sequence", 1), (40, "Input Sequence", 1),
    (41, "Word", 1), (42, "Embedding", 1), (43, "Vectors", 2),
    (44, "Position", 1), (45, "Information", 1), (46, "59", 1),
]

SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉ₙ⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ", "0123456789n0123456789n")
SYM_FOLD = str.maketrans("ILlO", "1100")  # case-aware symbol fold: I/L/l->1, O->0; NOT i

def norm_tokens(line):
    line = re.sub(r"<class_[A-Za-z_]+>", " ", line)
    line = re.sub(r"<[xy]_[0-9.]+>", " ", line)
    line = unicodedata.normalize("NFKC", line).translate(SUB)
    line = line.replace("∑", "Σ").replace("σ", "Σ").replace("−", "-")
    line = re.sub(r"[_\u2010\u2011\-–—/]+", " ", line)  # underscore, dashes, slash
    line = re.sub(r"[^\wΣ+\s]", " ", line)              # keep + (GT#7)
    return re.sub(r"\s+", " ", line).strip().lower()

def norm_raw(line):
    """Same stripping as norm_tokens but case-preserved (for the glyph fold)."""
    line = re.sub(r"<class_[A-Za-z_]+>", " ", line)
    line = re.sub(r"<[xy]_[0-9.]+>", " ", line)
    line = unicodedata.normalize("NFKC", line).translate(SUB)
    line = line.replace("∑", "Σ").replace("σ", "Σ").replace("−", "-")
    line = re.sub(r"[_\u2010\u2011\-–—/]+", " ", line)
    line = re.sub(r"[^\wΣ+\s]", " ", line)
    return re.sub(r"\s+", " ", line).strip()

def ctok(t):
    """Token collapse: delete spaces/underscores/dashes/slashes (punct-collapse)."""
    return re.sub(r"[\s_\-–—/]+", "", t)

def classify(gtid, gt, lines):
    g = norm_tokens(gt)
    gtoks = g.split()
    g_collapse = g.replace(" ", "")
    g_collapse = ctok(g)
    best = None
    for ln in lines:
        l = norm_tokens(ln)
        if not l:
            continue
        ltoks = l.split()
        ltoks_raw = norm_raw(ln).split()
        l_collapse = ctok(l)
        # boundary-aligned consecutive-token span collapses (spans up to 4 tokens),
        # case-preserved for the fold branch
        span_cts = set()
        span_raw = set()
        n = len(ltoks)
        for i in range(n):
            acc = acc_raw = ""
            for j in range(i, min(n, i + 4)):
                acc += ctok(ltoks[j])
                acc_raw += ctok(ltoks_raw[j]) if j < len(ltoks_raw) else ctok(ltoks[j])
                span_cts.add(acc)
                span_raw.add(acc_raw)
        cand = None
        if g == l or gtoks == ltoks:
            cand = (0, "EXACT", ln)
        elif len(gtoks) == 1 and gtoks[0] in ltoks:
            cand = (1, "NORMALIZED(intact-token containment)", ln)
        elif g_collapse and (g_collapse == l_collapse or g_collapse in span_cts):
            cand = (1, "NORMALIZED(underscore/punct/subscript collapse)", ln)
        elif g_collapse and 0 < len(g_collapse) <= 5 and any(
                s.translate(SYM_FOLD).lower() == g_collapse.translate(SYM_FOLD)
                for s in span_raw):
            cand = (1, "NORMALIZED(symbol glyph-confusion fold I/L/l->1, O->0)", ln)
        elif len(gtoks) > 1 and g in l:
            cand = (1, "NORMALIZED(merge-surviving multiword substring)", ln)
        elif g_collapse and len(g_collapse) >= 2 and g_collapse in l_collapse:
            cand = (2, "PARTIAL(GT contiguous in line with stray glyphs)", ln)
        if cand and (best is None or cand[0] < best[0]):
            best = cand
            if best[0] == 0:
                break
    return best

def load_lines(paths):
    out = []
    for p in paths:
        for f in (glob.glob(p) if any(ch in p for ch in "*?[") else [p]):
            fs = glob.glob(os.path.join(f, "*.parse.md")) + glob.glob(os.path.join(f, "*.parse.json")) \
                if os.path.isdir(f) else [f]
            for fp in fs:
                txt = open(fp, encoding="utf-8", errors="replace").read()
                if fp.endswith(".json"):
                    try:
                        j = json.loads(txt)
                        txt = j.get("content") or ""
                    except Exception:
                        pass
                out.extend(l for l in txt.splitlines() if l.strip())
    return out

def score_of(per):
    return (sum(1.0 for b in per.values() if b and b[0] == 0)
            + sum(1.0 for b in per.values() if b and b[0] == 1)
            + sum(0.5 for b in per.values() if b and b[0] == 2))

def main(paths):
    union_best = {}
    for p in paths:
        lines = load_lines([p])
        tag = p.rstrip("/").split("/")[-1]
        per = {gtid: classify(gtid, gt, lines) for gtid, gt, occ in GT}
        for gtid, b in per.items():
            if b and (gtid not in union_best or b[0] < union_best[gtid][0]):
                union_best[gtid] = b
        s = score_of(per)
        print(f"== {tag}: recall {s:.1f}/46 = {100*s/46:.1f}%")
    s = score_of(union_best)
    n_exact = sum(1 for b in union_best.values() if b[0] == 0)
    n_norm = sum(1 for b in union_best.values() if b[0] == 1)
    n_part = sum(1 for b in union_best.values() if b[0] == 2)
    print(f"== UNION ({len(paths)} transcripts): recall {s:.1f}/46 = {100*s/46:.1f}% "
          f"(EXACT {n_exact} + NORMALIZED {n_norm} + PARTIAL {n_part})")
    print("\n-- union per-string detail --")
    for gtid, gt, occ in GT:
        b = union_best.get(gtid)
        if b:
            print(f"  #{gtid:>2} {gt!r:30} {b[1]:52} <- {b[2][:60]!r}")
        else:
            print(f"  #{gtid:>2} {gt!r:30} MISSING")
    missed = [gt for (gtid, gt, occ) in GT if gtid not in union_best]
    print(f"\nMISSING ({len(missed)}): " + " · ".join(missed))

if __name__ == "__main__":
    main(sys.argv[1:])
