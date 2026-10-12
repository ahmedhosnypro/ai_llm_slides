# Certificate Audit — 002_transformers_part2, slides 27–60 (addendum)

Audit time: 2026-10-12 (UTC+3 local). Auditor: read-only + additive only. No DB writes, no fixes, no evidence modification.
Audit file: /home/ahmed/Projects/ai_llm_slides/scratch/audit_002/certificate_audit_slides27-60.md

## DB snapshot (sqlite3 -readonly slides_progress.db)

Scope rule: gen_status='passed' AND visual_check='PASS', slides 27–60 only.

Certified set (30): 27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,45,46,49,50,51,52,53,54,55,56,58,59,60
Excluded (mid-flight): 44 (gen_status=building, visual_check=PASS), 47 (pending), 48 (pending), 57 (pending).

Coordinator-listed mid-flight rows 10/12/22 are outside the 27–60 window.
Slide 46: coordinator described as mid-flight, but DB row is terminal (gen_status=passed, visual_check=PASS, last_error empty, judge_attempt_1 recorded) — not skipped; audited, and on-disk state double-checked for in-flight markers.

Notable DB facts to verify on disk:
- Slide 58: build_script column is EMPTY in DB (must find build script on disk or flag).
- Dep-parents in scope: 28(dep 27,26), 29(dep 28), 36, 38, 42(P3 head), 43(P3), 45, 49(dep 26), 54(P4 head).
- 46 depends_on=45.

## Per-slide results

(being appended incrementally)
