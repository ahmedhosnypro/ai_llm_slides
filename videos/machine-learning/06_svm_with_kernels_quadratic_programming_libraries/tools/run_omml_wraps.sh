#!/usr/bin/env bash
# run_omml_wraps.sh — OMML dual-representation wrap for all equation slides of
# 06_svm_with_kernels_quadratic_programming_libraries. Run ONLY after all rebuilds
# are final: gate on qa/rejudge2/ledger.jsonl (latest per slide = PASS or
# documented-residual). rel ids are re-derived from the CURRENT pptx at wrap time.
set -euo pipefail

NS=/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries
REPO=/home/codespace/ai_llm_slides
QA=$NS/qa/rejudge2
BUILD=$NS/recreated_pptx/build
PPTX_DIR=$NS/recreated_pptx
LOG=$QA/omml_wrap_run.log
FINAL_MD=$QA/omml_wrap_final.md
LEDGER=$QA/ledger.jsonl
BACKUP=$QA/omml_wrap_backup
RENDER=$QA/omml_wrap_render
RESULTS=$QA/omml_wrap_results.tmp
EQ_SLIDES="003 004 005 006 007 008 009 010 011 012 013 015 016 018 019 020 021 022 023 025 026 027 028 029 030 031 032 034 035 036 037 038 048"

exec > >(tee -a "$LOG") 2>&1
echo "=== omml wrap run $(date '+%Y-%m-%d %H:%M:%S') ==="
mkdir -p "$BACKUP" "$RENDER"; : > "$RESULTS"

# Gate: every equation slide (minus plot-only dirs agent-51 marked SKIPPED in
# omml_manifest_prep.md) must have a latest ledger verdict of PASS, the word
# "residual" in its notes, or a "## Slide NNN" heading in residuals_003_004.md
# (same documented-residual acceptance as tools/run_final_merge.sh).
if ! python3 - "$QA" $EQ_SLIDES <<'PY'
import sys, json, re, os
qa, slides = sys.argv[1], sys.argv[2:]
residual = set()
try:
    for ln in open(os.path.join(qa, "residuals_003_004.md")):
        m = re.match(r"^##\s+Slide\s+(\d+)", ln)
        if m: residual.add(m.group(1).zfill(3))
except FileNotFoundError:
    pass
skipped = set()
for ln in open(os.path.join(qa, "omml_manifest_prep.md")):
    if ln.startswith("|") and "SKIPPED" in ln:
        m = re.match(r"\|\s*(\d{3})\s*\|", ln)
        if m: skipped.add(m.group(1))
gate = [s for s in slides if s not in skipped]
latest = {}
for line in open(os.path.join(qa, "ledger.jsonl")):
    line = line.strip()
    if not line or line.startswith("#"): continue
    try: r = json.loads(line)
    except ValueError: continue
    if str(r.get("verdict", "")).startswith("OMML_FAILED"):
        continue  # wrap not applied (atomic, pptx unchanged): use latest non-OMML row
    latest[str(r.get("slide")).zfill(3)] = r
bad = []
wrapped = []
for s in gate:
    r = latest.get(s)
    if r is None: bad.append((s, "NO_LEDGER_ROW")); continue
    v = str(r.get("verdict", ""))
    if v == "OMML_WRAPPED":
        v = "PASS(wrapped)"  # wrap is pixel-identical; judge PASS stands
        wrapped.append(s)
    note = str(r.get("notes") or r.get("note") or "")
    if not (v.startswith("PASS") or "residual" in note.lower() or s in residual):
        bad.append((s, v))
for s, v in bad: print(f"GATE BLOCK {s}: latest verdict {v!r} (need PASS or documented-residual)")
if bad: sys.exit(1)
accepted = sorted(s for s in gate if s in residual and not str(latest[s].get("verdict", "")).startswith("PASS") and str(latest[s].get("verdict", "")) != "OMML_WRAPPED")
print(f"GATE OK: {len(gate)} eq slides PASS/documented-residual; wrapped-as-PASS: {sorted(wrapped)}; residual-doc accepted: {accepted}; plot-only skipped: {sorted(skipped)}")
PY
then echo "GATE FAIL: ledger not ready — refusing to wrap" >&2; exit 1; fi

wrap_one() {
  local NNN=$1
  local EQDIR=$BUILD/eq_$NNN PPTX=$PPTX_DIR/slide_${NNN}_recreated.pptx
  local MC=$EQDIR/manifest_current.json TMP n md5
  [ -f "$PPTX" ] || { echo "SKIP $NNN no pptx"; echo "$NNN SKIPPED no-pptx" >> "$RESULTS"; return 0; }
  [ -f "$EQDIR/manifest.json" ] || { echo "SKIP $NNN no manifest.json"; echo "$NNN SKIPPED no-manifest" >> "$RESULTS"; return 0; }
  if grep -qE "^\|[[:space:]]*$NNN[[:space:]]*\|.*SKIPPED" "$QA/omml_manifest_prep.md"; then
    echo "SKIP $NNN plot-only (prep doc)"; echo "$NNN SKIPPED plot-only" >> "$RESULTS"; return 0
  fi
  n=$(unzip -p "$PPTX" ppt/slides/slide1.xml | grep -o mc:AlternateContent | wc -l)
  if [ "$n" -gt 0 ]; then
    echo "SKIP $NNN already wrapped ($n)"; echo "$NNN ALREADY_WRAPPED $n" >> "$RESULTS"; return 0
  fi
  # Re-derive rel_id/image/mathtext/font_size_pt/color from the CURRENT pptx:
  # map each <p:pic> r:embed -> rels target -> media md5, match eq sidecar PNGs.
  if ! python3 - "$NNN" "$PPTX" "$EQDIR" "$BUILD" <<'PY2'
import sys, json, zipfile, hashlib, os, re
nnn, pptx, eqdir, build = sys.argv[1:5]
md5 = lambda b: hashlib.md5(b).hexdigest()
z = zipfile.ZipFile(pptx)
xml = z.read("ppt/slides/slide1.xml").decode("utf-8")
rels = z.read("ppt/slides/_rels/slide1.xml.rels").decode("utf-8")
relmap = {}
for tag in re.findall(r"<Relationship\b[^>]*>", rels):
    i = re.search(r'Id="([^"]+)"', tag); t = re.search(r'Target="([^"]+)"', tag)
    if i and t: relmap[i.group(1)] = t.group(1)
media = {}
for pic in re.findall(r"<p:pic>.*?</p:pic>", xml, re.S):
    e = re.search(r'r:embed="([^"]+)"', pic)
    if not e: continue
    name = "ppt/media/" + os.path.basename(relmap.get(e.group(1), ""))
    if name in z.namelist():
        media[md5(z.read(name))] = (e.group(1), os.path.basename(name))
eqs, seen = [], set()
for fn in sorted(os.listdir(eqdir)):
    if not fn.endswith(".json") or fn.endswith("_manifest.json") or fn.startswith("manifest"):
        continue
    try: sc = json.load(open(os.path.join(eqdir, fn)))
    except ValueError: continue
    rows = sc.get("rows")
    if not rows: continue
    cands = []
    if sc.get("path"): cands += [os.path.join(build, sc["path"]), os.path.join(eqdir, sc["path"])]
    base = fn[:-5]
    cands += [os.path.join(eqdir, base + ".png"), os.path.join(eqdir, base)]
    png = next((c for c in cands if os.path.isfile(c)), None)
    if png is None: continue
    hit = media.get(md5(open(png, "rb").read()))
    if hit is None or hit[0] in seen: continue
    seen.add(hit[0])
    seg_text = lambda s: s.split(":", 1)[1] if ":" in s else s
    mt = "\\\\".join(" ".join(seg_text(s) for s in row.split("||")) for row in rows)
    color = rows[0].split("||")[0].split(":", 1)[0]
    eqs.append({"rel_id": hit[0], "image": hit[1], "mathtext": mt,
                "font_size_pt": (sc.get("fontsize_pt") or [None])[0], "color": color})
if not eqs: sys.exit(2)
json.dump({"slides": [{"slide": 1, "equations": eqs}]},
          open(os.path.join(eqdir, "manifest_current.json"), "w"), indent=2)
print(f"{nnn} manifest_current: {len(eqs)} equations matched to current pptx media")
PY2
  then echo "FAIL $NNN manifest re-derivation"; echo "$NNN FAILED rederive" >> "$RESULTS"; return 1; fi

  TMP=$(mktemp /tmp/omml_wrap_XXXXXX.pptx)
  if ! python3 "$REPO/scripts/18_omml_wrapper.py" "$PPTX" "$MC" -o "$TMP"; then
    echo "FAIL $NNN wrapper exit nonzero"; echo "$NNN FAILED wrapper" >> "$RESULTS"; rm -f "$TMP"; return 1
  fi
  n=$(unzip -p "$TMP" ppt/slides/slide1.xml | grep -o mc:AlternateContent | wc -l)
  if [ "$n" -le 0 ]; then
    echo "FAIL $NNN verify: 0 mc:AlternateContent after wrap"; echo "$NNN FAILED verify" >> "$RESULTS"; rm -f "$TMP"; return 1
  fi
  cp "$PPTX" "$BACKUP/slide_${NNN}_prewrap.pptx"
  mv "$TMP" "$PPTX"
  n=$(unzip -p "$PPTX" ppt/slides/slide1.xml | grep -o mc:AlternateContent | wc -l)
  md5=$(md5sum "$PPTX" | cut -d' ' -f1)
  printf '{"slide":"%s","verdict":"OMML_WRAPPED","pptx_md5":"%s","ts":"%s","notes":"omml wrap in-place; %s mc:AlternateContent; manifest_current.json; prewrap backup qa/rejudge2/omml_wrap_backup/"}\n' \
    "$NNN" "$md5" "$(date '+%Y-%m-%d %H:%M:%S')" "$n" >> "$LEDGER"
  echo "WRAPPED $NNN: $n mc:AlternateContent"
  echo "$NNN WRAPPED $n" >> "$RESULTS"
}

for NNN in $EQ_SLIDES; do
  if ! wrap_one "$NNN"; then echo "ERROR wrapping $NNN (see $LOG)"; fi
done

# Pixel sanity: re-render one wrapped slide via soffice; the PNG fallback must
# still render (wrapped render vs pre-wrap backup render should be ~identical).
FIRST=$(awk '$2=="WRAPPED"{print $1; exit}' "$RESULTS")
if [ -n "${FIRST:-}" ]; then
  P=$PPTX_DIR/slide_${FIRST}_recreated.pptx
  B=$BACKUP/slide_${FIRST}_prewrap.pptx
  soffice --headless --convert-to pdf --outdir "$RENDER" "$P" >/dev/null 2>&1
  soffice --headless --convert-to pdf --outdir "$RENDER" "$B" >/dev/null 2>&1
  pdftoppm -png -r 100 -singlefile "$RENDER/slide_${FIRST}_recreated.pdf" "$RENDER/wrapped_$FIRST"
  pdftoppm -png -r 100 -singlefile "$RENDER/slide_${FIRST}_prewrap.pdf" "$RENDER/prewrap_$FIRST"
  python3 - "$RENDER/wrapped_$FIRST.png" "$RENDER/prewrap_$FIRST.png" "$FIRST" <<'PY3'
import sys, os
try:
    from PIL import Image, ImageChops
    a = Image.open(sys.argv[1]).convert("RGB"); b = Image.open(sys.argv[2]).convert("RGB")
    d = ImageChops.difference(a, b)
    hist = sum(d.convert("L").histogram()[1:])
    print(f"RENDER SANITY slide {sys.argv[3]}: size={a.size} diff_bbox={d.getbbox()} differing_px={hist}")
except ImportError:
    print(f"RENDER SANITY slide {sys.argv[3]}: PIL unavailable; wrapped={os.path.getsize(sys.argv[1])}B prewrap={os.path.getsize(sys.argv[2])}B")
PY3
  echo "RENDER SANITY done for slide $FIRST (wrapped vs prewrap)"
else
  echo "No slide wrapped; render sanity skipped"
fi

{
  echo "# OMML wrap final — 06_svm_with_kernels_quadratic_programming_libraries"
  echo "Run: $(date '+%Y-%m-%d %H:%M:%S') via tools/run_omml_wraps.sh"
  echo
  echo "## Per-slide results (NNN VERDICT detail)"
  cat "$RESULTS"
  echo
  echo "Wrapped: $(grep -c WRAPPED "$RESULTS" || true)  Failed: $(grep -c FAILED "$RESULTS" || true)  Skipped: $(grep -c SKIPPED "$RESULTS" || true)  Already: $(grep -c ALREADY "$RESULTS" || true)"
} > "$FINAL_MD"
echo "Wrote $FINAL_MD"
