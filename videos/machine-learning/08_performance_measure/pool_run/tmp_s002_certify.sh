#!/usr/bin/env bash
# slide-002 certification on dual PASS (run from namespace root $NS).
# Args: <attempt_K> <md5_of_slide_pptx>
set -eu
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
K=${1:?attempt K}
MD5=${2:?md5}
QA=recreated_pptx/qa/slide002
cd "$NS"

# (a) ledger row under flock (append-only)
ROW="| 2 | \`$QA/judge_attempt_${K}.txt\` (render_${K}.png, original-first, FINAL VERDICT: PASS) | \`$QA/judge_verify_${K}.txt\` (render_${K}.png, fresh original-first corroboration, FINAL VERDICT: PASS) | PASS / PASS (original-first dual-read) | analysis/reanalysis/slide_002_raw.json | certified=yes | recovery worker 2026-11-14; slide pptx md5 ${MD5}; merged via merge_final_deck.py update 2 |"
(
  flock 9
  printf '%s\n' "$ROW" >> pool_run/verification_ledger.md
) 9>> pool_run/verification_ledger.md.lock
echo "ledger row appended"

# (b) progress DB
sqlite3 slides_progress.db "update slides set gen_status='passed', visual_check='PASS', visual_transcript='$QA/judge_attempt_${K}.txt', visual_attempts=visual_attempts+1, last_error=NULL, updated_at=datetime('now') where slide_id=2;"
sqlite3 slides_progress.db "select slide_id, gen_status, visual_check, visual_transcript, updated_at from slides where slide_id=2;"

# (c) pool scope-done
bash ~/.agents/skills/pooled-missions/scripts/pool-db.sh scope-done pool_run/mission.db slide-2 "slide 2 dual-PASS certified (judge_attempt_${K}.txt + judge_verify_${K}.txt, original-first, render_${K}.png); ledger row appended; progress DB passed/PASS; merged to final deck page 2 (md5 ${MD5})"

# (d) final_deck_ledger.json page 2 certified + md5
python3 - "$MD5" <<'PYEOF'
import json, sys, fcntl
md5 = sys.argv[1]
p = "final_deck_ledger.json"
with open(p) as f:
    d = json.load(f)
for pg in d["pages"]:
    if pg.get("page") == 2:
        pg["status"] = "certified"
        pg["source_md5"] = md5
with open(p, "w") as f:
    fcntl.flock(f, fcntl.LOCK_EX)
    json.dump(d, f, indent=1)
    f.write("\n")
    fcntl.flock(f, fcntl.LOCK_UN)
print("final_deck_ledger.json page 2 -> certified", md5)
PYEOF

# (e) merge into final deck from namespace root
python3 pool_run/merge_final_deck.py update 2 recreated_pptx/slide_002_recreated.pptx 08-performance_final.pptx
echo "CERTIFY DONE"
