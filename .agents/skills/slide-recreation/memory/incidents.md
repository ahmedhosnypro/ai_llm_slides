> NOTE 2026-10-10: qa/ evidence paths cited below were REMOVED at founder directive after program completion — the knowledge stands; the cited transcripts/renders no longer exist on disk.
# incidents.md — coordination and process war stories

Read alongside lessons.md. Newest last.

## 2026-10-09 — Banked QA evidence may belong to a different slide after curation
Context: deck re-curated from 104 to 64 slides; files renamed by the printed badge
number; mapping kept at `unique_slides/new2old_mapping.json`.
Incident: slide 53's banked QA evidence actually belonged to current slide 41 (old
numbering); slide 64's prior build was the OLD deck's KNN slide, a different slide
entirely; slide 54's banked attempts 1–2 were pre-curation different slides.
Recovery: resume rule — every worker verifies banked artifacts against its own
ground-truth frame (`unique_slides/slide_NNN.jpg`) before trusting them.
Rule: a file name is not provenance; the ground-truth frame is.

## 2026-10-09 — Silently-resumed worker + re-dispatched resume worker = collision
Context: slide 19 (also 26, 27, 54) had dual workers.
Incident: an "original" worker resumed silently alongside the re-dispatched resume
worker; its DB writes overwrote the certification (row regressed judging/FAIL mid-loop);
it banked into unpadded `qa/slide19/` while the other used padded `qa/slide019/`. It
later passed on attempt 6 on its own.
Recovery: let both finish, reconcile the DB row from the actual transcripts, bank BOTH
evidence tracks (never merge/delete). Re-dispatched workers should first check for a
live peer's fresh file activity — if the row is moving, don't double-own it.

## 2026-10-09 — "Stuck running" workers were done; UI state was stale
Context: founder reported slides 19/26/63/27/64 "appearing as running but they
reported the final result without stopping" after a location switch.
Incident: TaskStop on all candidates returned "not running (status: completed)" — the
runs had finished; only the UI state was stale.
Rule: verify with TaskStop probes/file mtimes/DB rows before declaring a worker dead
and re-dispatching — a false "dead" call is what CREATES the dual-worker collision.

## 2026-10-09 — Provider failures kill workers but not their work
Context: TLS failure to the upstream provider killed the slide-27 worker; upstream
timeouts killed the renderer-research and scratch-math agents.
Recovery: re-dispatch a resume worker WITH a state summary: what's banked, what
attempt number is next, and what does NOT count as a spent attempt (a judge prompt
banked without a transcript). The scratch-math restart resumed from vision-validation
only, skipping already-bankeded build artifacts — zero duplicated work.

## 2026-10-09 — Judge misread a small badge numeral
Context: slide 19's judge read the original's badge as "16" (actual: 19).
Handling: house-rule override (badge numeral = file id = printed number is law);
recorded as a documented deviation for close-out rather than "fixed".
Rule: judge findings on house-template elements are overridden, but note them in the
close-out report — don't silently discard.

## 2026-10-09 — Score-7 slides certified against real pixels = accepted deviations
Context: slides 35, 43, 46, 48 scored 7 on the content gate (threshold 8).
Handling: each was judge-certified PASS against the actual original pixels; the DB
`validation_status` quirk shows them as "failed" while verdicts are accurate. They
were accepted as documented deviations, explicitly reported at close-out.
Rule: the content gate is a screen, not an absolute — a judge-certified sub-8 slide is a
documented deviation, never a silent pass, and never a silent re-run either.

## 2026-10-09 — The judge needs the GROUND RULES prelude or it flags intent as defect
Context: slide 2 failed 6 consecutive judges before the template was fixed.
Incident: judges flagged the intentional house template and equation-format upgrades as
discrepancies. After adding the founder ground-rules prelude (house template
intentional; contentless-matches-contentless; video artifacts omitted; typed-vs-
handwritten minor; 2D-equation upgrade mandated), attempt 7 PASSed.
Rule: never dispatch a comparison without the ground-rules prelude; a streak of FAILs
on intentional differences is a prompt bug, not a slide bug.

## 2026-10-10 — OMML application started against a pptx that was being rebuilt
Context: slide 55's alignment fixer re-rendered equations and rebuilt the pptx minutes
after the wrapper-application agent was dispatched for it.
Detection: completion notification for the fixer arrived after the dispatch.
Recovery: messaged the application agent to discard the stale slide-55 manifest,
verify pptx mtime post-fix, and re-derive from the current pptx rels + current
sidecars (old PNGs were banked under `assets_pre_align_fix/` — tempting but wrong).
Rule: before any post-pass consumes a deliverable, check that no worker still owns
that slide's files (fresh mtimes = an active owner).

## 2026-10-10 — Stray ground-truth file in the wrong QA dir
Context: `qa/slide022/ground_truth.jpg` — a ground-truth frame banked under another
slide's QA dir during early worker experiments.
Handling: banked, not deleted (evidence law); flagged in the close-out report as a
known stray.
Rule: close-out reports list known strays rather than "cleaning" them.

## 2026-10-10 — "Dead" slide-26 worker was alive in a long wall/probe cycle (3rd false-positive)
Context: slide 26 math rework — watchdog saw the attempt-5 PASS transcript banked (01:11)
with no DB update and no file activity for >60 min, declared the worker dead, and
dispatched a resume worker.
Reality: the original worker was alive — sitting in its probe/hang-retry ladder (its
own protocol includes a 12x600s probe ladder, i.e. up to 2 hours of quiet). It
completed attempt 6 (rework under the alignment law + closed-loop evidence + judge
PASS + DB update) while the resume worker was mid-verification.
Handling: the resume worker was immediately re-scoped to READ-ONLY (no DB writes, no
judge calls, no banking) so it could not overwrite the newer attempt-6 state with
stale attempt-5 values.
Rule: before declaring a worker dead on "no file movement for 60 min", check whether
its protocol has quiet phases (probe ladders, sleep-300 re-probes, W4 hang-retry walls
of 450-540s each) and whether the last banked artifact is a terminal state the worker
just hasn't recorded yet. A banked PASS + stale row is ambiguous — prefer messaging
the suspected-dead worker or waiting one more cycle over dispatching a second owner;
if you must dispatch, scope the resume worker to verification-first and hold DB writes.
