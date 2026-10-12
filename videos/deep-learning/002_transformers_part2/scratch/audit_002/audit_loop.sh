#!/usr/bin/env bash
# Certificate audit loop — 002_transformers_part2 slides 27-60 (certified only).
# READ-ONLY except appends to scratch/audit_002/. Appends after EVERY slide.
set -u
ROOT=/home/ahmed/Projects/ai_llm_slides
DECK=$ROOT/videos/deep-learning/002_transformers_part2
DB=$DECK/slides_progress.db
AUD=$DECK/scratch/audit_002/certificate_audit_002.md
CHK=$ROOT/videos/deep-learning/shared_patterns/house_chrome_check.py

# slide:render pairs (certified render per worker reports)
PAIRS="027:6 028:1 029:1 030:4 031:2 032:2 033:5 034:1 035:1 036:2 037:2 038:1 039:1 040:7 041:3 042:4 043:1 045:1 046:1 049:2 050:2 051:6 052:5 053:6 054:7 055:8 056:4 058:1 059:2 060:3"

if [ ! -f "$AUD" ]; then
cat > "$AUD" <<'HDR'
# CERTIFICATE AUDIT — 002_transformers_part2, slides 27-60 (certified set only)

Auditor: read-only certificate audit, 2026-10-12. Scope: DB rows with
gen_status=passed AND visual_check=PASS among 27-60. Mid-flight rows skipped:
44 (gen_status=building), 47 (building), 48 (pending), 57 (pending).
NOTE 24 is outside 27-60; 41 IS a certified slide of THIS deck (own frame/pptx
under 002_transformers_part2/) and was audited as such.
Method per slide: (1) DB row terminal; (2) visual_transcript on disk + coherent
winner body; (3) single-variant deliverable; (4) build script; (5) house_chrome_check.py
on the certified render; (6) badge numeral vs printed frame numeral (banked
badge_audit sweep + render-badge crops in badge_sheets/); (7) component demand
(only-if-referenced) for dep-parents 28,29,36,38,42,43,45,49,54.

HDR
fi

for pair in $PAIRS; do
  n=${pair%%:*}; r=${pair##*:}
  NN=$(printf "%03d" $((10#$n)))
  L="" # accumulate result line
  # 1. DB row
  db=$(sqlite3 -readonly "$DB" "SELECT gen_status||'/'||visual_check||' att='||visual_attempts||' upd='||updated_at FROM slides WHERE slide_id=$NN;")
  # 2. transcript
  vt=$(sqlite3 -readonly "$DB" "SELECT visual_transcript FROM slides WHERE slide_id=$NN;")
  vtp=$ROOT/$vt
  if [ -f "$vtp" ]; then
    sz=$(wc -c < "$vtp")
    verdict=$(grep -h "FINAL VERDICT" "$vtp" | tail -1 | tr -s ' ')
    coherent=OK
    if [ "$sz" -lt 800 ]; then coherent=THIN; fi
    T="transcript=$vt ($sz B, $coherent) verdict: ${verdict:-<none-found>}"
  else
    T="transcript MISSING: $vt"
  fi
  # 3. deliverable single variant
  ppts=$(ls "$DECK"/recreated_pptx/slide_${NN}_recreated*.pptx 2>/dev/null | wc -l)
  pptlist=$(ls "$DECK"/recreated_pptx/slide_${NN}_recreated*.pptx 2>/dev/null | xargs -r -n1 basename | tr '\n' ' ')
  # 4. build script
  bs=$(sqlite3 -readonly "$DB" "SELECT build_script FROM slides WHERE slide_id=$NN;")
  bsdisk="$DECK/recreated_pptx/build/slide_${NN}.js"
  if [ -f "$bsdisk" ]; then bx="build/slide_${NN}.js on disk YES (db field: '${bs:-<empty>}')"; else bx="build/slide_${NN}.js on disk NO (db field: '${bs:-<empty>}')"; fi
  # 5. chrome check on certified render
  rend="$DECK/recreated_pptx/qa/slide$NN/render_$r.png"
  if [ -f "$rend" ]; then
    cc=$(python3 "$CHK" "$rend" 2>&1 | tr '\n' ' ' | tr -s ' ')
  else
    cc="CERTIFIED RENDER MISSING qa/slide$NN/render_$r.png"
  fi
  echo "## Slide $NN" >> "$AUD"
  echo "- DB: $db" >> "$AUD"
  echo "- $T" >> "$AUD"
  echo "- deliverable: $ppts variant(s): $pptlist" >> "$AUD"
  echo "- build: $bx" >> "$AUD"
  echo "- certified render: qa/slide$NN/render_$r.png" >> "$AUD"
  echo "- chrome: $cc" >> "$AUD"
done
echo "LOOP DONE"
