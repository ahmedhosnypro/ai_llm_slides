#!/usr/bin/env bash
# render_slide046.sh — the WORKING LO render route for this host (see the infra alert):
# PDF export fails from deep paths and direct PPTX->PNG drops raster images, so:
# copy to /home/ahmed/lo_pdf_test, soffice->PDF there, pdftoppm -r 150, copy back.
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
