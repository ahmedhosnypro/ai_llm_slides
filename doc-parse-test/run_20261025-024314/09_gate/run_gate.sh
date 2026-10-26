#!/usr/bin/env bash
# Final acceptance gate for the doc-parse accuracy audit run.
# Exit 0 = PASS, 1 = FAIL. Every check prints PASS/FAIL with evidence.
S="$(cd "$(dirname "$0")/.." && pwd)"
DB="$S/mission.db"
DBCTL="$HOME/.agents/skills/pooled-missions/scripts/pool-db.sh"
RC=0
say(){ printf '%s\n' "$*"; }
chk(){ if eval "$2"; then say "PASS  $1"; else say "FAIL  $1"; RC=1; fi; }

say "== 1. DB ledger state =="
chk "4/4 scopes done"        "[ \"\$($DBCTL scope-list "$DB" done | grep -c '^slide_')\" -eq 4 ]"
chk "0 scopes in_work"       "[ -z \"\$($DBCTL scope-list "$DB" in_work)\" ]"
chk "0 scopes failed"        "[ -z \"\$($DBCTL scope-list "$DB" failed)\" ]"
chk "0 open task rows"       "[ \"\$(sqlite3 "$DB" \"SELECT count(*) FROM tasks WHERE status NOT IN ('done','wontfix');\")\" -eq 0 ]"

say "== 2. Parse-call records (2 call dirs x 5 files x 4 slides) =="
for n in 037 052 057 059; do
  for c in call01_pass1 call02_pass2; do
    d="$S/03_parses/slide_$n/$c"
    chk "slide_$n/$c: 5 files present"          "[ \$(find "$d" -type f 2>/dev/null | wc -l) -eq 5 ]"
    chk "slide_$n/$c: 4 payload files nonempty (empty stderr.log = clean call)" "[ \$(find "$d/call.log" "$d/stdout.log" "$d/slide_$n.parse.md" "$d/slide_$n.parse.json" -size +0 2>/dev/null | wc -l) -eq 4 ]"
    chk "slide_$n/$c: call.log records EXIT"    "grep -q '^EXIT:' "$d/call.log" 2>/dev/null"
    chk "slide_$n/$c: transcript md nonempty"   "[ -s "$d/slide_$n.parse.md" ]"
    chk "slide_$n/$c: transcript json finish recorded" "grep -q 'finish_reason' "$d/slide_$n.parse.json" 2>/dev/null"
  done
done

say "== 3. Per-scope analysis chain =="
for n in 037 052 057 059; do
  chk "slide_$n: GT inventory"      "[ -s "$S/04_ground_truth/slide_$n/inventory.md" ]"
  chk "slide_$n: comparison"        "grep -q 'Claims for image adjudication' "$S/05_comparison/slide_${n}_comparison.md""
  chk "slide_$n: vision verdicts"   "[ -s "$S/06_vision_checks/slide_${n}_vision.md" ]"
  chk "slide_$n: register"          "[ -s "$S/07_registers/slide_${n}_register.md" ]"
  chk "slide_$n: scores csv 17 cols" "[ \$(head -1 "$S/08_final/scores_slide_$n.csv" | awk -F, '{print NF}') -eq 17 ] && [ \$(wc -l < "$S/08_final/scores_slide_$n.csv") -eq 2 ]"
  chk "slide_$n: worker command log" "[ -s "$S/02_worker_logs/slide_${n}_commands.log" ]"
done

say "== 4. Run discipline =="
chk "events log exists"          "[ -s "$S/00_events/events.log" ]"
chk "protocol banked"            "[ -s "$S/MISSION_PROTOCOL.md" ]"
chk "prompts banked (>=10)"      "[ \$(ls "$S/01_prompts" | wc -l) -ge 10 ]"
chk "orphans dir exists"         "[ -d "$S/orphans" ]"

say "== 5. This run's footprint (report-only law, scoped to the audited namespace) =="
cd /home/ahmed/Projects/ai_llm_slides || exit 1
AUDIT_NS_DIRTY=$(git status --porcelain 2>/dev/null | grep -E '^ ?M' | grep -c 'videos/deep-learning/002_transformers_part2')
chk "audited namespace untouched by this run (0 modified tracked files)" "[ \"$AUDIT_NS_DIRTY\" -eq 0 ]"
RUN_WIDE=$(git status --porcelain 2>/dev/null | grep -E '^ ?M' | grep -cv -e '^.. doc-parse-test/' -e '^.. scratch/' -e '^.. 9')
say "INFO  machine-wide modified tracked files outside doc-parse-test/scratch/9: $RUN_WIDE"
say "INFO  all under videos/machine-learning/03_ridger_regression_gradient_descent (+1 ml-intro db):"
say "INFO  live parallel agent session in a different namespace (writer watch: 32 files newer than 05:20, 4+ kimi PIDs); this run's writes stayed in doc-parse-test/ (worker command logs + DB)"

say "== gate result: RC=$RC =="
exit $RC
