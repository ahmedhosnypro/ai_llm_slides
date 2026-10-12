#!/usr/bin/env bash
# render_omml.sh — LO render pipeline for the OMML wrap pass (video 002_transformers_part2).
# Robust to this host's LO breakages (measured 2026-10-12, scratch/slide011/render_slide011.sh):
#   * direct PPTX->PNG drops all raster images -> PDF->pdftoppm route is MANDATORY;
#   * PDF export fails from the deep project path -> copy to /home/ahmed/lo_pdf_test first.
# Usage: render_omml.sh <pptx> <out_png>
set -e
PPTX="$1"
OUT="$(readlink -f "$2")"
RD=/home/ahmed/lo_pdf_test
mkdir -p "$RD"
B=$(basename "$PPTX")
cp "$PPTX" "$RD/$B"
rm -f "$RD/${B%.pptx}.pdf" "$RD/${B%.pptx}"-*.png
cd "$RD"
TMPDIR="$RD" timeout 300 soffice --headless --norestore \
  -env:UserInstallation=file:///home/ahmed/lo_pdf_test/prof2 \
  --convert-to pdf --outdir . "$B" 2>&1 | tail -1
test -f "${B%.pptx}.pdf" || { echo "PDF EXPORT FAILED" >&2; exit 1; }
pdftoppm -png -r 150 "${B%.pptx}.pdf" "${B%.pptx}"
cp "${B%.pptx}"-1.png "$OUT"
echo "rendered -> $OUT"
