# doc-parse accuracy audit — for slide recreation

**Question:** is the `doc-parse` skill (nemotron-parse family) accurate, reliable,
detailed, and powerful enough to support recreating lecture slides as PPTX?

**Method:** two independent doc-parse calls per slide (pass1 + pass2, full token
budget) → text recall vs a ground-truth inventory taken from the certified
build files + project analysis JSONs → pixel-adjudication of every claim
(tesseract OCR incl. masked/upscaled crops, PIL/numpy ink & color maps, ASCII
glyph maps, cross-anchored to the certified build geometry) → severity-ranked
register → 17-column score CSV per slide.

**Slides under test** (deep-learning/002_transformers_part2, 4 difficulty tiers):
037 (dense equations + list), 052 (3-D model diagram), 057 (dense diagram,
dense math), 059 (stacked tensor blocks + table).

**Honesty note:** all adjudication was done by deterministic pixel measurement,
not model vision — the adjudicator subagents had no image input. Every banked
verdict cites its measurement.

**Run:** `run_20261025-024314/` (pooled-missions discipline; 4 scopes, 8+ parse
calls, 2 waves of workers). See `run_20261025-024314/08_final/DOC_PARSE_EFFECTIVENESS_REPORT.md`
for the verdict.

## Run tree

```
run_20261025-024314/
  MISSION_PROTOCOL.md          worker contract (claim/done criteria/verification)
  mission.db                   pooled-missions ledger (scopes, tasks, events)
  00_events/
    events.log                 append-only run ledger (every orchestration action)
    docparse_process_notes_evidence_copy.md   skill defect-vocabulary copy
  01_prompts/                  every prompt sent to every worker (wave1, resume,
                               wave2, vision adjudicator)
  02_worker_logs/              worker returns (text only) + per-slide command logs
  03_parses/                   per-call parse records: call.log (full invocation),
                               stdout.log, stderr.log, slide_NNN.parse.{md,json}
                               (call01_pass1, call02_pass2; slide_057 also retries)
  04_ground_truth/             per-slide GT inventory from build + analysis JSON,
                               with the build .js files used as evidence
  05_comparison/               per-slide claim lists (what to adjudicate, why)
  06_vision_checks/            pixel-adjudication verdicts (REAL/HALLUCINATED/DEBATABLE)
  07_registers/                severity-ranked defect registers (BLOCKER/MAJOR/MINOR)
  08_final/                    scores_slide_NNN.csv (17 cols) + merged scores.csv
                               + DOC_PARSE_EFFECTIVENESS_REPORT.md
  09_gate/                     run_gate.sh (acceptance gate) + final_gate.log
  orphans/                     parked files (nothing was ever deleted)
```

## Conventions

- Every doc-parse invocation is recorded: command line, exit code, timing,
  and both transcript files, in one directory per call.
- No image bytes in agent context; workers return text only.
- Report-only vs the project: nothing outside `doc-parse-test/` was modified.
