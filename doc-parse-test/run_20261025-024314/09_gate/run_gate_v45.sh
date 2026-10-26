#!/usr/bin/env bash
# ADDENDUM gate for waves 3 (t9k), 4 (visual-judge loop), 5 (cascade).
# The base gate run_gate.sh covers waves 0-2 and stays authoritative for them.
# Exit 0 = PASS, 1 = FAIL. Every check prints PASS/FAIL with evidence.
S="$(cd "$(dirname "$0")/.." && pwd)"
DB="$S/mission.db"
DBCTL="$HOME/.agents/skills/pooled-missions/scripts/pool-db.sh"
RC=0
say(){ printf '%s\n' "$*"; }
chk(){ # args: label result(0/1)
  if [ "$2" -eq 0 ]; then say "PASS  $1"; else say "FAIL  $1"; RC=1; fi
}
present(){ find "$1" -type f 2>/dev/null | wc -l; }   # count files under dir
nz(){ [ -s "$1" ] && echo 0 || echo 1; }              # 0 iff file nonempty (chk passes on 0)

say "== 0. DB ledger state (16 scopes total) =="
NDONE=$($DBCTL scope-list "$DB" done | grep -c '^slide_')
INW=$($DBCTL scope-list "$DB" in_work | wc -l)
FAILS=$($DBCTL scope-list "$DB" failed | wc -l)
OPEN=$(sqlite3 "$DB" "SELECT count(*) FROM tasks WHERE status NOT IN ('done','wontfix');")
chk "12 wave-0..3 scopes done"          "$([ "$NDONE" -ge 12 ]; echo $?)"
chk "20/20 scopes done"                 "$([ "$NDONE" -eq 20 ]; echo $?)"
chk "0 scopes in_work"                  "$([ "$INW" -eq 0 ]; echo $?)"
chk "0 scopes failed"                   "$([ "$FAILS" -eq 0 ]; echo $?)"
chk "0 open task rows"                  "$([ "$OPEN" -eq 0 ]; echo $?)"

say "== 1. Wave 3 — t9k parses (9000-token ceiling probe) =="
for n in 037 052 057 059; do
  d="$S/03_parses/slide_$n/call05_t9k"
  F=$(present "$d")
  P=$([ -s "$d/call.log" ] && [ -s "$d/slide_$n.parse.md" ] && [ -s "$d/slide_$n.parse.json" ]; echo $?)
  E=$([ -f "$d/call.log" ] && grep -q '^EXIT:' "$d/call.log"; echo $?)
  chk "slide_$n/call05_t9k: 5 files present"  "$([ "$F" -eq 5 ]; echo $?)"
  chk "slide_$n/call05_t9k: payload nonempty" "$P"
  chk "slide_$n/call05_t9k: call.log EXIT"    "$E"
  case "$n" in
    037|057)
      d="$S/03_parses/slide_$n/call06_t9k_retry"
      chk "slide_$n/call06_t9k_retry: present+EXIT" "$([ -s "$d/call.log" ] && grep -q '^EXIT:' "$d/call.log"; echo $?)" ;;
  esac
  chk "slide_$n: t9k delta report"  "$(nz "$S/05_comparison/slide_${n}_t9k_delta.md")"
  case "$n" in
    037) w=8;; 052) w=9;; 057) w=10;; 059) w=11;;
  esac
  chk "slide_$n: t9k worker return banked" "$(nz "$S/02_worker_logs/agent-${w}_slide_${n}_t9k_return.md")"
done

say "== 2. Wave 4 — visual-judge improvement loop =="
for n in 037 052 057 059; do
  d="$S/10_visual_judge/slide_$n"
  R=$(find "$d/judge" -name 'round*_transcript.md' 2>/dev/null | wc -l)
  RV=$(grep -l 'FINAL VERDICT' "$d/judge"/round*_transcript.md 2>/dev/null | wc -l)
  RP=$(find "$d/judge" -name 'round*_prompt.txt' 2>/dev/null | wc -l)
  C=$(find "$d/parses" -name call.log 2>/dev/null | wc -l)
  CX=$(grep -l '^EXIT:' "$d/parses"/*/call.log 2>/dev/null | wc -l)
  T=$(find "$d/parses" -name '*.parse.md' -size +0 2>/dev/null | wc -l)
  L=$(grep -c -i 'round' "$d/ledger.md" 2>/dev/null)
  chk "slide_$n: >=2 judged rounds banked"   "$([ "$R" -ge 2 ]; echo $?)"
  chk "slide_$n: every round transcript ends in FINAL VERDICT" "$([ "$RV" -eq "$R" ]; echo $?)"
  chk "slide_$n: every round prompt banked"  "$([ "$RP" -ge "$R" ]; echo $?)"
  chk "slide_$n: >=4 crop-parse call dirs"   "$([ "$C" -ge 4 ]; echo $?)"
  chk "slide_$n: every call dir records EXIT" "$([ "$CX" -eq "$C" ]; echo $?)"
  chk "slide_$n: crop parse transcripts nonempty" "$([ "$T" -ge 4 ]; echo $?)"
  chk "slide_$n: ledger has >=2 round rows"  "$([ "$L" -ge 2 ]; echo $?)"
  chk "slide_$n: VJ report banked"           "$(nz "$d/VJ_IMPROVEMENT_REPORT.md")"
done

say "== 3. Wave 5 — cascade crop tree =="
for n in 037 052 057 059; do
  d="$S/11_cascade/slide_$n"
  M=$(jq -e . "$d/manifest.json" >/dev/null 2>&1; echo $?)
  MC=$(jq -e '(.crops // .nodes // []) | length >= 2' "$d/manifest.json" >/dev/null 2>&1; echo $?)
  MB=$(jq -e '([(.crops // .nodes // [])[] | has("box_frame_px") and has("scale") and has("stop_reason")] | all) and ([(.crops // .nodes // [])[].box_frame_px] | all(. != null))' "$d/manifest.json" >/dev/null 2>&1; echo $?)
  CP=$(find "$d/crops" -name '*.png' 2>/dev/null | wc -l)
  C=$(find "$d/parses" -name call.log 2>/dev/null | wc -l)
  CX=$(grep -l '^EXIT:' "$d/parses"/*/call.log 2>/dev/null | wc -l)
  T=$(find "$d/parses" -name '*.parse.md' -size +0 2>/dev/null | wc -l)
  J=$(find "$d/judges" \( -name '*.md' -o -name '*judge*.log' -o -name '*judge*_raw.txt' \) -size +0 2>/dev/null | wc -l)
  COMP=$(nz "$d/compose/COMPOSED_ANALYSIS.md")
  COMPV=$(grep -qiE 'provenance|call[0-9]' "$d/compose/COMPOSED_ANALYSIS.md" 2>/dev/null; echo $?)
  CREP=$(nz "$d/CASCADE_REPORT.md")
  CREPV=$(grep -qiE 'stop|leaf' "$d/CASCADE_REPORT.md" 2>/dev/null; echo $?)
  chk "slide_$n: manifest.json valid JSON"  "$M"
  chk "slide_$n: manifest has >=2 crops"    "$MC"
  chk "slide_$n: every crop carries box+scale+stop_reason" "$MB"
  chk "slide_$n: crops parked on disk"      "$([ "$CP" -ge 2 ]; echo $?)"
  chk "slide_$n: >=4 cascade parse call dirs" "$([ "$C" -ge 4 ]; echo $?)"
  chk "slide_$n: every cascade call dir records EXIT" "$([ "$CX" -eq "$C" ]; echo $?)"
  chk "slide_$n: crop transcripts nonempty" "$([ "$T" -ge 4 ]; echo $?)"
  chk "slide_$n: >=1 crop judge transcript" "$([ "$J" -ge 1 ]; echo $?)"
  chk "slide_$n: composed file present"     "$COMP"
  chk "slide_$n: composed file carries provenance" "$COMPV"
  chk "slide_$n: cascade report present"    "$CREP"
  chk "slide_$n: cascade report records stop reasons" "$CREPV"
done

say "== 4. Wave 4/5 worker returns banked =="
for n in 037 052 057 059; do
  L=$(find "$S/02_worker_logs" -name "agent-*_slide_${n}_*return*.md" 2>/dev/null | wc -l)
  chk "slide_$n: >=2 worker return logs (vj+cascade)" "$([ "$L" -ge 2 ]; echo $?)"
done

say "== 5. Report-only law (scoped to the audited namespace) =="
cd /home/ahmed/Projects/ai_llm_slides || exit 1
AUDIT_NS_DIRTY=$(git status --porcelain 2>/dev/null | grep -E '^ ?M' | grep -c 'videos/deep-learning/002_transformers_part2')
chk "audited namespace untouched (0 modified tracked files)" "$([ "$AUDIT_NS_DIRTY" -eq 0 ]; echo $?)"

say "== 3B. Wave 5B — requirement-compliant cascade (AUTHORITATIVE) =="
for n in 037 052 057 059; do
  d="$S/12_cascade_v2/slide_$n"
  M=$(jq -e . "$d/manifest.json" >/dev/null 2>&1; echo $?)
  MC=$(jq -e '.crops | length >= 2' "$d/manifest.json" >/dev/null 2>&1; echo $?)
  MB=$(jq -e '([.crops[] | has("box_frame_px") or has("box")] | all) and ([(.crops[] | (.box_frame_px // .box))] | all(. != null)) and ([.crops[] | has("scale") and has("stop_reason")] | all)' "$d/manifest.json" >/dev/null 2>&1; echo $?)
  CP=$(find "$d/crops" -name '*.png' 2>/dev/null | wc -l)
  C=$(find "$d/parses" -name call.log 2>/dev/null | wc -l)
  CX=$(grep -l '^EXIT:' "$d/parses"/*/call.log 2>/dev/null | wc -l)
  T=$(find "$d/parses" -name '*.parse.md' -size +0 2>/dev/null | wc -l)
  J=$(find "$d/judges" \( -name '*.md' -o -name '*judge*.log' -o -name '*judge*_raw.txt' \) -size +0 2>/dev/null | wc -l)
  COMP=$(nz "$d/compose/COMPOSED_ANALYSIS.md")
  COMPV=$(grep -qiE 'provenance|call[0-9]' "$d/compose/COMPOSED_ANALYSIS.md" 2>/dev/null; echo $?)
  CREP=$(nz "$d/CASCADE_REPORT.md")
  CREPV=$(grep -qiE 'stop|leaf' "$d/CASCADE_REPORT.md" 2>/dev/null; echo $?)
  SPD=$(grep -qiE 'speedup|wall-clock|parallel' "$d/CASCADE_REPORT.md" 2>/dev/null; echo $?)
  chk "v2 slide_$n: manifest valid"   "$M"
  chk "v2 slide_$n: >=2 crops"        "$MC"
  chk "v2 slide_$n: every crop box+scale+stop_reason, no null boxes" "$MB"
  chk "v2 slide_$n: crops parked"     "$([ "$CP" -ge 2 ]; echo $?)"
  chk "v2 slide_$n: >=4 parse call dirs" "$([ "$C" -ge 4 ]; echo $?)"
  chk "v2 slide_$n: all call dirs EXIT"  "$([ "$CX" -eq "$C" ]; echo $?)"
  chk "v2 slide_$n: crop transcripts nonempty" "$([ "$T" -ge 4 ]; echo $?)"
  chk "v2 slide_$n: >=1 crop judge"   "$([ "$J" -ge 1 ]; echo $?)"
  chk "v2 slide_$n: composed file present" "$COMP"
  chk "v2 slide_$n: composed file provenanced" "$COMPV"
  chk "v2 slide_$n: cascade report present" "$CREP"
  chk "v2 slide_$n: report has stop reasons" "$CREPV"
  chk "v2 slide_$n: report states parallel speedup" "$SPD"
done
say "== addendum gate result (with 5B): RC=$RC =="
exit $RC
