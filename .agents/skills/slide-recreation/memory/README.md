# memory/ — the skill's self-learning store

This directory is how the skill evolves. `SKILL.md` and `references/` are the stable
playbook; everything learned AFTER the skill was written lands here as dated entries.
A worker/agent using this skill must:

1. **Read before starting**: scan `lessons.md` and `incidents.md` for anything relevant
   to the current slide/topic/tooling (entries are short; recent ones matter most).
2. **Append after every task** (and immediately after any novel failure): add a dated
   entry to the right file. Appending is part of the task's definition of done.
3. **Never edit SKILL.md or references/ during a task.** If a lesson repeatedly
   re-occurs and belongs in the stable playbook, note that in the entry ("promote
   candidate") — a skill-maintenance pass can promote it later.

## Entry format

```
## YYYY-MM-DD — <short title>
Context: <slide/task/tooling>
Mistake: <what went wrong, with the measured number if any>
Fix: <what actually worked>
Rule: <the distilled instruction, imperative, one or two sentences> (optional)
```

## Which file

- `lessons.md` — technical mistakes and fixes: renderer behavior, tool quirks, model
  failure modes, geometry math, pipeline bugs. One entry per distinct lesson.
- `incidents.md` — coordination/process war stories: worker collisions, dead-worker
  misdiagnoses, curation renumbering, evidence provenance, stale UI, dispatch errors.
  What happened, how it was detected, how it was recovered.

Keep entries atomic and specific (numbers, paths, commands). Correcting an earlier
entry is fine — append the correction, never rewrite history.
