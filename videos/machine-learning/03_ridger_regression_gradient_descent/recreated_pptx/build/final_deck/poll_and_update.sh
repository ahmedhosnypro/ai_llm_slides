#!/usr/bin/env bash
# S21 standing lane: poll the deck DB for newly certified slides and update
# their pages in the continuous final deck (MODE=update N + render gate).
# Idempotent: pages already certified in the ledger are skipped.
set -euo pipefail
cd /home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
POOL_DB=/home/ahmed/.agents/scratch/ai_llm_slides-pool-299640/mission.db

NEW=$(python3 - <<'EOF'
import json, sqlite3
led = json.load(open("recreated_pptx/final_deck_state.json"))
done = {int(k) for k, v in led["pages"].items() if v["status"] == "certified"}
con = sqlite3.connect("file:slides_progress.db?mode=ro", uri=True)
cert = {r[0] for r in con.execute(
    "SELECT slide_id FROM slides WHERE gen_status='passed' AND visual_check='PASS'")}
print(" ".join(str(n) for n in sorted(cert - done)))
EOF
)

if [ -z "$NEW" ]; then
  echo "poll: no newly certified pages (ledger is current)"
  exit 0
fi

echo "poll: newly certified pages: $NEW"
python3 recreated_pptx/build/final_deck/final_deck_tool.py update $NEW
python3 recreated_pptx/build/final_deck/render_check_pages.py $NEW

bash /home/ahmed/.agents/skills/pooled-missions/scripts/pool-db.sh event "$POOL_DB" \
  "s21-progress" "S21 continuous deck: updated newly certified pages [$NEW] (MODE=update, render gate 0-px PASS); ledger + addendum current" \
  >/dev/null 2>&1 || true
echo "pool event logged"
