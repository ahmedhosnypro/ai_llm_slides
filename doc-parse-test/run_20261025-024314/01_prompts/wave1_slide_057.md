SCOPE: slide_057 (doc-parse accuracy audit, pooled-missions run)

Run dir (absolute): /home/ahmed/Projects/ai_llm_slides/doc-parse-test/run_20261025-024314
Ledger DB: /home/ahmed/Projects/ai_llm_slides/doc-parse-test/run_20261025-024314/mission.db
Protocol: /home/ahmed/Projects/ai_llm_slides/doc-parse-test/run_20261025-024314/MISSION_PROTOCOL.md

FIRST ACTION: Read that MISSION_PROTOCOL.md in full and follow it exactly for your scope.

Your scope's inputs:
- Slide image (do NOT open/read it — no image bytes in your context): /home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_057.jpg
- Ground-truth build: /home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_057.js
- Ground-truth analysis: /home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/analysis/slide_057_final.json
- Your agent-id for DB claims: worker-slide_057
- Dependency hint: the densest build in the set. It requires (by absolute path, read-only) build/slide_049.js, build/components/slide_047.js, build/components/slide_026.js and ../shared_patterns/house_chrome.js — follow every require() the build pulls; all their strings/geometry are ground truth for this slide (encoder+decoder composition).

Wave-1 deliverables (protocol "Done criteria" items 1-3):
1. scope-claim the DB.
2. Two doc-parse call dirs: 03_parses/slide_057/call01_pass1 (--max-output-tokens 1024) and call02_pass2 (--max-output-tokens 3000), each with the five per-call files; log every command to 02_worker_logs/slide_057_commands.log; Bash timeout >=240s for parse calls.
3. 04_ground_truth/slide_057/inventory.md + frozen copies of your GT files (build + all required components + analysis JSON).
4. 05_comparison/slide_057_comparison.md with the four measured sections and the "Claims for image adjudication" list.
5. scope-done with a one-line note. Blockers -> task-add. Do NOT start the wave-2 register/scores items — a later resumed turn hands you the vision verdicts.

Your final message: a compact report of what you did, the key numbers, and the DB state.