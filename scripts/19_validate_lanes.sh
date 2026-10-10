#!/bin/bash
# Launch 4 parallel script-13 validation lanes over disjoint slide ranges.
# Idempotent: each lane skips existing *_final.json. Also kills any leftover
# full-range 13 instance to avoid overlap (its bash parent stage2b is fine).
cd /home/ahmed/Projects/ai_llm_slides || exit 1

pkill -f "python3 scripts/13_validate_slides.py analysis --slides 104$" 2>/dev/null
sleep 1

nohup python3 scripts/13_validate_slides.py analysis --slides 104 --from 1  --to 26  > analysis/run_13_lane1.log 2>&1 &
nohup python3 scripts/13_validate_slides.py analysis --slides 104 --from 27 --to 52  > analysis/run_13_lane2.log 2>&1 &
nohup python3 scripts/13_validate_slides.py analysis --slides 104 --from 53 --to 78  > analysis/run_13_lane3.log 2>&1 &
nohup python3 scripts/13_validate_slides.py analysis --slides 104 --from 79 --to 104 > analysis/run_13_lane4.log 2>&1 &
disown -a
sleep 2
pgrep -cf "13_validate_slides.py analysis --slides 104 --from"
