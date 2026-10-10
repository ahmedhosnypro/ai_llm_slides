#!/bin/bash
# Stage 2b: fill analysis gaps, then validate all slides (script 13), then sync the DB.
# Launched detached by the orchestrator after the first script-12 pass completes.
cd /home/ahmed/Projects/ai_llm_slides || exit 1

count_missing() {
  python3 - <<'EOF'
import os
have = {int(f.split('_')[1]) for f in os.listdir('analysis') if f.endswith('_raw.json')}
missing = [i for i in range(1, 105) if i not in have]
print(len(missing))
EOF
}

# Gap re-run: script 12 is idempotent (skips existing raw JSON). Truncated-JSON
# failures get the larger 32000-token budget (AGENTS.md remedy for finish=length).
for round in 1 2 3; do
  missing=$(count_missing)
  echo "[stage2b] gap round $round: $missing missing raw analyses" >> analysis/run_12b.log
  [ "$missing" -eq 0 ] && break
  python3 scripts/12_analyze_slides.py unique_slides analysis --slides 104 --max-tokens 32000 >> analysis/run_12b.log 2>&1
done
remaining=$(count_missing)
echo "[stage2b] gap re-run complete: $remaining still missing after 3 rounds" >> analysis/run_12b.log

# Validation pass (glm-5.3, text-only) over all slides with raw JSON.
python3 scripts/13_validate_slides.py analysis --slides 104 >> analysis/run_13b.log 2>&1
echo "[stage2b] script 13 exited with $?" >> analysis/run_13b.log

python3 scripts/15_progress.py sync
echo "[stage2b] done"
