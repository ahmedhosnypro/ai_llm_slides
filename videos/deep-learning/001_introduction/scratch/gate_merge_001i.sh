#!/usr/bin/env bash
# gate_merge_001i.sh — render gate for the 001_introduction merged deck.
# Modeled on the certified final-deck-merge pattern gate + the host-measured
# LibreOffice route (scratch/slide011/render_slide011.sh):
#   * PPTX -> PNG directly is BROKEN on this host (LO renders red "Image 0 1"
#     placeholders) -> PDF -> pdftoppm -r 150 is MANDATORY;
#   * PDF export FAILS from the deep project path -> files are staged in the
#     short home path /home/ahmed/lo_pdf_test and converted THERE;
#   * /tmp is BLOCKED (tmpfs ENOSPC law) -> TMPDIR lives under the video's
#     scratch, with a per-file fallback to the short path (measured-working).
#
# ONE soffice session (same UserInstallation profile) converts the merged deck
# AND every source deck; pixel-diff page N vs source N — 0 mismatches is the
# only acceptance.
#
# Usage: gate_merge_001i.sh <merged.pptx>
# The certified set is taken LIVE from slides_progress.db — same query the
# merger used — so the gate always checks exactly the slides that went in.
set -euo pipefail

VIDEO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DB="$VIDEO/slides_progress.db"
PPTX_DIR="$VIDEO/recreated_pptx"
MERGED="$(readlink -f "$1")"
BANK="$VIDEO/scratch/merge_gate_002"
VTMP="$BANK/tmp"
RD=/home/ahmed/lo_pdf_test
PROF=file:///home/ahmed/lo_pdf_test/prof2

mkdir -p "$VTMP/pages" "$VTMP/src_png" "$RD"
export TMPDIR="$VTMP"

# ---- certified set, LIVE from the DB (must match what the merger merged) ----
SIDS=($(sqlite3 "$DB" "SELECT slide_id FROM slides WHERE gen_status='passed' AND visual_check='PASS' ORDER BY slide_id;"))
N=${#SIDS[@]}
(( N > 0 )) || { echo "FAIL: no certified slides in DB" >&2; exit 1; }
echo "[gate] certified set (LIVE): $N slides: ${SIDS[*]}"

# ---- stage into the short home path (deep-path LO breakage) -----------------
rm -f "$RD"/merge001i* "$RD"/s[0-9][0-9][0-9].pptx "$RD"/s[0-9][0-9][0-9].pdf
cp "$MERGED" "$RD/merge001i.pptx"
i=0
for sid in "${SIDS[@]}"; do
  i=$((i+1))
  cp "$PPTX_DIR/slide_$(printf %03d "$sid")_recreated.pptx" "$RD/s$(printf %03d "$sid").pptx"
done

convert_one() {  # <basename without ext>
  local b="$1"
  rm -f "$RD/$b.pdf"
  if ( cd "$RD" && TMPDIR="$VTMP" timeout 300 soffice --headless --norestore \
         -env:UserInstallation="$PROF" --convert-to pdf --outdir . "$b.pptx" ) >/dev/null 2>&1 \
     && [[ -f "$RD/$b.pdf" ]]; then
    return 0
  fi
  # fallback: TMPDIR on the measured-working short path
  ( cd "$RD" && TMPDIR="$RD" timeout 300 soffice --headless --norestore \
      -env:UserInstallation="$PROF" --convert-to pdf --outdir . "$b.pptx" ) >/dev/null 2>&1 \
    && [[ -f "$RD/$b.pdf" ]]
}

echo "[gate] rendering merged deck + $N sources in ONE soffice session..."
convert_one merge001i || { echo "FAIL: merged deck PDF export failed" >&2; exit 1; }

FAIL=0
i=0
for sid in "${SIDS[@]}"; do
  i=$((i+1)); b="s$(printf %03d "$sid")"
  if ! convert_one "$b"; then
    echo "FAIL: source slide $sid PDF export failed" >&2; FAIL=1; continue
  fi
  echo "  [$i/$N] rendered $b"
done
(( FAIL == 0 )) || exit 1

pdfinfo "$RD/merge001i.pdf" | grep -q "Pages: *$N" \
  || { echo "FAIL: merged PDF page count != $N" >&2; exit 1; }

pdftoppm -png -r 150 "$RD/merge001i.pdf" "$VTMP/pages/pg"
i=0
for sid in "${SIDS[@]}"; do
  i=$((i+1)); b="s$(printf %03d "$sid")"
  pdftoppm -png -r 150 "$RD/$b.pdf" "$VTMP/src_png/$b"
done

# ---- pixel-diff page N vs source N ------------------------------------------
RC=0
python3 - "$VTMP" "$BANK" "$N" "${SIDS[*]}" <<'EOF' || RC=$?
import sys, glob, datetime
from pathlib import Path
from PIL import Image, ImageChops

vt, bank, n, sids_s = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
sids = [int(x) for x in sids_s.split()]
pages = sorted(glob.glob(f"{vt}/pages/pg-*.png"))
if len(pages) != n:
    sys.exit(f"FAIL: expected {n} merged page PNGs, got {len(pages)}")
bad = []
for k, sid in enumerate(sids, start=1):
    a = Image.open(pages[k-1]).convert("RGB")
    src_pngs = sorted(glob.glob(f"{vt}/src_png/s{sid:03d}-*.png"))
    if len(src_pngs) != 1:
        sys.exit(f"FAIL: source {sid}: expected 1 page PNG, got {len(src_pngs)}")
    b = Image.open(src_pngs[0]).convert("RGB")
    if a.size != b.size or ImageChops.difference(a, b).getbbox():
        bad.append((k, sid))
report = [
    f"MERGE RENDER GATE — 001_introduction",
    f"run: {datetime.datetime.now().isoformat(timespec='seconds')}",
    f"merged deck pages: {n} (certified set taken LIVE from slides_progress.db)",
    f"slide ids in page order: {sids}",
    f"route: LO pdf @/home/ahmed/lo_pdf_test (one session, profile prof2) -> pdftoppm -r 150 -> PIL diff",
    "",
    f"mismatched pages: {bad if bad else 'NONE'}",
    f"result: {'FAIL' if bad else 'PASS — 0/%d mismatched pages, merge is lossless' % n}",
]
txt = "\n".join(report)
Path(bank, "gate_report.txt").write_text(txt + "\n")
print(txt)
sys.exit(1 if bad else 0)
EOF
# ---- bank + clean ------------------------------------------------------------
cp "$RD/merge001i.pdf" "$BANK/merged_render.pdf" 2>/dev/null || true
rm -rf "$VTMP/pages" "$VTMP/src_png" "$VTMP"/*pdf* 2>/dev/null || true
rm -f "$RD"/merge001i* "$RD"/s[0-9][0-9][0-9].pptx "$RD"/s[0-9][0-9][0-9].pdf
echo "[gate] banked: $BANK/gate_report.txt (+ merged_render.pdf)"
exit $RC
