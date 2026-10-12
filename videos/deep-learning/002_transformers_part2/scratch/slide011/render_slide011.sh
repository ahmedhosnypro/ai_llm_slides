#!/usr/bin/env bash
# render_slide011.sh — LO render pipeline for slide 011, robust to the host's
# LO breakages measured 2026-10-12:
#   * PDF export fails (impl_store Io Write 16) when run with the source file in the
#     deep project path — but WORKS from a short home path (path-dependent, measured).
#   * Direct PPTX->PNG export drops ALL raster images (LO renders "Image" broken-image
#     placeholders instead — measured) — so the PDF->pdftoppm route is MANDATORY.
# Usage: render_slide011.sh <pptx> <out_png>
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
