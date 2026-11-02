# FINISH_BRIEF — 08_performance_measure closeout workers (2026-11-01)

Namespace NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
All work stays inside NS. Repo root: /home/codespace/ai_llm_slides

## Mandatory reads first
- $NS/AGENTS.md and repo-root AGENTS.md (house frame rule overrides all)
- $NS/pool_run/MISSION_PROTOCOL.md and $NS/pool_run/REBUILD_BRIEF.md
- $NS/pool_run/defect_patterns.md, spec_gaps.md, spec_drift.md (your slide's section)
- ~/.agents/skills/slide-recreation/SKILL.md + references/building.md + judging.md
- ~/.agents/skills/image-analysis/SKILL.md, visual-judge SKILL.md, doc-parse SKILL.md

## Toolchain (verified working 2026-11-01)
- node v27 + pptxgenjs at repo root node_modules; run builds from $NS/recreated_pptx (node_modules symlink there): `node build/slide_NNN.js` writes recreated_pptx/slide_NNN_recreated.pptx
- Render: `bash recreated_pptx/render_slide.sh NNN K` -> recreated_pptx/qa/slideNNN/render_K.png
- Judge call (copy pattern from pool_run/verify_wing_slide26.sh; run from repo root):
  python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    videos/machine-learning/08_performance_measure/unique_slides/slide_NNN.jpg \
    videos/machine-learning/08_performance_measure/recreated_pptx/qa/slideNNN/render_K.png \
    --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
    -p "$(cat videos/machine-learning/08_performance_measure/pool_run/judge_prompt_template.txt)"
  wrapped in the fleet gate: scripts/16_vision_gate.sh <cmd...>; wrap whole thing in `timeout 540`.
  ORIGINAL FIRST, render SECOND — render-first is a protocol violation. Retry up to 8x on 429/HangError/empty (sleep 300 between), keep going until a FINAL VERDICT line exists. Probe first with --timeout 120.

## Per-slide pipeline (Phase 1 slides)
1. Claim: bash ~/.agents/skills/pooled-missions/scripts/pool-db.sh scope-claim $NS/pool_run/mission.db slide-NNN <your-agent-id>
2. Inputs: pool_run/image_analysis/slide_NNN_analysis.txt, analysis/reanalysis/slide_NNN_raw.json, analysis/slide_NNN_final.json, spec_gaps/spec_drift deltas (add EVERY drifted item), sources/slide_NNN_research.md if present. Dense slides (equations/matrices/ROC): doc-parse crop-cascade banked under pool_run/docparse/slideNNN/ BEFORE first judge.
3. Build from the NEWEST build/slide_NNN*.js (by mtime); copy to slide_NNN.js, fix errors in place; never delete prior scripts.
4. Render, pre-judge PIL self-checks (frame containment, delimiters, tables, line spacing).
5. Judge -> judge_attempt_K.txt; on PASS run a SECOND fresh identical call -> judge_verify_K.txt (dual-read law; both must end FINAL VERDICT: PASS). Any FAIL: fix, render K+1, re-run BOTH reads. Max 6 attempts; adjudicate conflicting reads by pixel arbitration vs the original (see verification_ledger.md precedent rows).
6. Equations: matplotlib mathtext 600dpi PNG (scripts/render_eq*.py) embedded at exact size; OMML wrap via scripts/18_omml_wrapper.py only AFTER dual PASS, then re-run merge update (idempotent, reflects final bytes). Graphs: gen_*_assets.py in build/, embedded in the same single pptx.
7. Dual PASS -> certify: (a) append ONE row to pool_run/verification_ledger.md under flock (append-only, never delete) with both transcript paths, PASS/PASS, reanalysis path, certified=yes; (b) sqlite3 slides_progress.db: update slides set gen_status='passed', visual_check='PASS', visual_transcript='<attempt path>', updated_at=datetime('now') where slide_id=NNN; (c) pool-db.sh scope-done slide-NNN; (d) set final_deck_ledger.json page N status='certified' + source_md5=md5 of the slide pptx (json rewrite, preserve format); (e) from $NS: python3 pool_run/merge_final_deck.py update NNN recreated_pptx/slide_NNN_recreated.pptx 08-performance_final.pptx
8. Report back: slide NNN, attempt count, verdicts, md5 of final pptx, any blockers.
