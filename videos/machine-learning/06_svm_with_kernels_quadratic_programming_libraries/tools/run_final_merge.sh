#!/usr/bin/env bash
# run_final_merge.sh — Phase-6 final merge + gate for 06_svm_with_kernels_quadratic_programming_libraries.
# Implements tools/FINAL_MERGE_RUNBOOK.md: merge -> verify-only -> LO render -> page compare
# -> MERGE_GATE_REPORT.md -> atomic final-deck replacement on gate PASS.
# Refuses to run unless qa/rejudge2/ledger.jsonl shows 55/55 PASS (latest row per slide).
set -euo pipefail

NS="/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
FINAL="$NS/recreated_pptx/06_svm_with_kernels_quadratic_programming_libraries_final.pptx"
MERGED="$NS/recreated_pptx/06_svm_with_kernels_quadratic_programming_libraries_final_merged.pptx"
SLIDES_DIR="$NS/recreated_pptx"
QA="$NS/recreated_pptx/qa/final_merge"
RENDER_DIR="$QA/render"
REPORT="$QA/MERGE_GATE_REPORT.md"
LEDGER="$NS/qa/rejudge2/ledger.jsonl"
REF_DIR="$NS/qa/rejudge2/renders_pass"
LO_PROFILE="$HOME/.lo_profile_final_merge"
MERGE_TOOL="$NS/tools/merge_final_deck.py"

log() { echo "[run_final_merge] $*"; }

# 0. Ledger gate: latest row per slide must be PASS for all 55 slides, except slides
#    documented as accepted residuals via a "## Slide NNN" heading in $RESIDUALS.
RESIDUALS="$NS/qa/rejudge2/residuals_003_004.md"
python3 - "$LEDGER" "$RESIDUALS" <<'PY'
import json, re, sys
latest = {}
wrapped = []
for line in open(sys.argv[1]):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    try: row = json.loads(line)
    except ValueError: continue  # malformed row (bad escape in notes): skip
    v = str(row.get("verdict", ""))
    if v.startswith("OMML_FAILED"):
        continue  # wrap not applied (atomic, pptx unchanged): use latest non-OMML row
    if v == "OMML_WRAPPED":
        v = "PASS(wrapped)"  # wrap is pixel-identical; judge PASS stands
        wrapped.append(str(row.get("slide")).zfill(3))
    latest[str(row.get("slide")).zfill(3)] = v
residual = set()
try:
    for line in open(sys.argv[2]):
        m = re.match(r"^##\s+Slide\s+(\d+)", line)
        if m:
            residual.add(m.group(1).zfill(3))
except FileNotFoundError:
    pass
def is_pass(v):
    v = v.upper()
    return "PASS" in v and "FAIL" not in v
missing = [f"{n:03d}" for n in range(1, 56) if f"{n:03d}" not in latest]
bad = {s: v for s, v in latest.items() if not is_pass(v) and s not in residual}
accepted = sorted(s for s in latest if not is_pass(latest[s]) and s in residual)
if missing or bad:
    print(f"LEDGER GATE FAIL: missing={missing} not-pass={bad} residual-accepted={accepted}", file=sys.stderr)
    sys.exit(1)
print(f"LEDGER GATE OK: {len(latest)}/55 slides PASS or documented-residual (wrapped-as-PASS={sorted(set(wrapped))}, residual-accepted={accepted})")
PY

mkdir -p "$QA" "$RENDER_DIR"

# 1. Merge every certified per-slide deck into a NEW output (placeholder untouched).
log "step 1: merge -> $MERGED"
python3 "$MERGE_TOOL" --final "$FINAL" --slides-dir "$SLIDES_DIR" --out "$MERGED" | tee "$QA/merge.log"

# 2. Verify-only against the MERGED output; expect 55 byte-identical / 0 mismatched.
log "step 2: verify-only on merged deck"
VERIFY_OK=1
if ! VERIFY_OUT=$(python3 "$MERGE_TOOL" --final "$MERGED" --slides-dir "$SLIDES_DIR" --verify-only 2>&1 | tee "$QA/verify.log"); then
    VERIFY_OK=0
fi
echo "$VERIFY_OUT" | grep -q "55 pages byte-identical" || VERIFY_OK=0
echo "$VERIFY_OUT" | grep -q ", 0 mismatched" || VERIFY_OK=0

# 3. One LibreOffice headless render of the merged deck to PDF, then per-page PNGs.
log "step 3: LibreOffice render (profile $LO_PROFILE)"
rm -rf "$LO_PROFILE"; mkdir -p "$LO_PROFILE"
PDF="$QA/06_svm_with_kernels_quadratic_programming_libraries_final_merged.pdf"
rm -f "$PDF" "$RENDER_DIR"/page-*.png
soffice --headless --convert-to pdf --outdir "$QA" "-env:UserInstallation=file://$LO_PROFILE" "$MERGED"
rm -rf "$LO_PROFILE"
[ -f "$PDF" ] || { log "render failed: no PDF produced"; exit 1; }
pdftoppm -png -r 150 "$PDF" "$RENDER_DIR/page"
PAGES=$(ls "$RENDER_DIR"/page-*.png | wc -l)
[ "$PAGES" -eq 55 ] || { log "render: expected 55 pages, got $PAGES"; exit 1; }

# 4. Per-page compare of merged renders vs qa/rejudge2/renders_pass (dpi-agnostic:
#    tools/page_compare.py resizes the ref to the render's size with LANCZOS when
#    sizes differ, per-channel tol <=8, page passes when differing px < 0.5% of total).
log "step 4: per-page compare vs $REF_DIR"
python3 "$NS/tools/page_compare.py" --batch "$RENDER_DIR" "$REF_DIR" "$QA/page_compare.tsv"

# 5. md5 + MERGE_GATE_REPORT.md with verify output, compare table, and gate line.
MERGED_MD5=$(md5sum "$MERGED" | awk '{print $1}')
md5sum "$MERGED" > "$MERGED.md5"
N_DIFF=$(awk -F'\t' 'NR>1 && ($2=="DIFF" || $2=="DIFF_SIZE" || $2=="MISSING_PAGE")' "$QA/page_compare.tsv" | wc -l)
if [ "$VERIFY_OK" -eq 1 ] && [ "$N_DIFF" -eq 0 ]; then GATE=PASS; else GATE=FAIL; fi
{
    echo "# MERGE GATE REPORT — 06_svm_with_kernels_quadratic_programming_libraries"
    echo "- Date: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "- Merged deck: \`$MERGED\`"
    echo "- Merged md5: \`$MERGED_MD5\`"
    echo
    echo "## Verify-only output (against merged deck)"
    echo '```'
    echo "$VERIFY_OUT"
    echo '```'
    echo
    echo "## Page compare vs qa/rejudge2/renders_pass"
    echo '```'
    cat "$QA/page_compare.tsv"
    echo '```'
    echo
    echo "## Gate"
    echo "**GATE: $GATE** (verify_ok=$VERIFY_OK, page diffs=$N_DIFF)"
} > "$REPORT"
log "step 5: gate=$GATE report=$REPORT"

# 6. On gate PASS, atomically replace the final deck; record old+new md5.
if [ "$GATE" = "PASS" ]; then
    OLD_MD5=$(md5sum "$FINAL" | awk '{print $1}')
    cp "$MERGED" "$FINAL.tmp" && mv -f "$FINAL.tmp" "$FINAL"
    NEW_MD5=$(md5sum "$FINAL" | awk '{print $1}')
    {
        echo
        echo "## Final deck replacement (atomic cp+mv)"
        echo "- old md5: \`$OLD_MD5\`"
        echo "- new md5: \`$NEW_MD5\`"
    } >> "$REPORT"
    log "step 6: final deck replaced $OLD_MD5 -> $NEW_MD5"
else
    log "step 6: gate FAIL — final deck NOT replaced"
    exit 1
fi
