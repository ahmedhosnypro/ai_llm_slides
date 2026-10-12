> NOTE 2026-10-10: qa/ evidence paths cited below were REMOVED at founder directive after program completion — the knowledge stands; the cited transcripts/renders no longer exist on disk.
# incidents.md — coordination and process war stories

Read alongside lessons.md. Newest last.

## 2026-10-12 — Coordinator + 30-min-watchdog dual-dispatch race on 001_introduction slide 1
Context: the coordinator dispatched a slide-1 builder; minutes later the playlist
watchdog cron (extended to the new deck that same hour) ran its first sweep, saw
slide 1 in `buildable`, and dispatched a second builder — despite the cron rule
"no live worker (no fresh activity 40+ min)". The race: the coordinator's builder
sets gen_status=building only AFTER reading 5 rule files + measuring (~10 min), so
at sweep time the row still looked dispatchable while qa/slide001/ was already
fresh — the cron weighted buildable over file freshness.
Resolution: coordinator stopped ITS OWN builder (TaskStop; the cron's builder is
unreachable from the coordinator session), leaving a single owner; banked
artifacts (measure script, render_1-1, selfcheck, cropped logo asset) stay for the
surviving builder to reuse per the resume rule. Subsequent coordinator dispatches
(5/29/40) pin `gen_status=building` at dispatch time, BEFORE the builder's first
file write — closing the window.
Rule: when a coordinator and a periodic watchdog can both dispatch the same unit,
the coordinator must claim the DB row atomically at dispatch time (set
gen_status=building in the same breath as the Agent launch), and the watchdog must
treat ANY fresh-activity signal (files OR row) as owned. buildable is a necessary
condition, never a sufficient one.

## 2026-10-12 (2nd) — Global interruption makes the watchdog's staleness check fire; expect convergent double-resumes
Context: a session-wide interruption froze ALL workers (coordinator's builders,
validation lanes). The next 30-min watchdog sweep then saw mid-state rows with
stale files (nothing had moved because EVERYTHING was frozen) and correctly
re-dispatched resumes — including slides the coordinator was simultaneously
re-resuming (slide 040: two resume workers ran concurrently).
Handling that worked: the worker that detected the peer did NOT fight for
ownership — it applied the banked-PASS law (a banked comparison-PASS certifies
as-is), verified the peer's end-state independently (md5 script ≡ certified build,
fresh render ≡ certified render, chrome check), and reported the race honestly.
Both workers converged on the same certified state; no corruption.
Rule: after ANY global interruption, the next watchdog sweep WILL double-dispatch
whatever the coordinator also resumes — that is now expected. Resume workers must
lead with a disk survey + verification of banked state (re-render + md5 compare)
and treat a detected peer as "converge and verify", never "fight or restart".
Banked-PASS rows are terminal: verifying beats re-judging.

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

## 2026-10-12 — Provider blip kills subagent FLEET members at identical ~19.3-min durations; "please retry" = re-dispatch with storm-resilience clause
Context: 29-worker fleet re-seeded after a host interruption; ~25 min later FOUR workers (001t1:32, 001i:29, 001i:32, 001i:42) failed simultaneously with "the upstream provider is temporarily unavailable; please retry" at durations 1159.7–1160.1s — the subagent HARNESS's own model upstream flapped, not the slide pipeline.
Facts: (1) the blip is terminal for the affected subagents (no internal retry) but selective — other workers kept making model calls and producing files throughout; (2) dying workers may bank NOTHING in their window (all four produced 0 files) — re-dispatch state == pre-dispatch state, so verify disk before assuming partial work; (3) live workers' file activity is the fastest "is the provider back" probe (cheaper than a test call).
Fix: re-dispatch each dead slide as a resume worker with (a) a "TWO interruptions" state summary (previous worker banked nothing — disk state unchanged), and (b) a STORM RESILIENCE clause: on provider/upstream errors sleep 120s and retry up to 3×, bank per step atomically, keep logs in the video scratch dir (NOT /tmp — one retry worker violated the /tmp quota block).
Rule: a batch of same-duration agent failures with the provider-unavailable message is a fleet event, not four slide failures — sweep disk per slide, then re-dispatch all of them in one batch with the storm-resilience clause; never re-verify their (empty) partial state as if it were new work.

## 2026-10-12 — "All subagents interrupted" can be FALSE for background subagents: original-fleet workers SURVIVED a host restart
Context: founder reported all running subagents interrupted after a host restart; a 29-worker resume fleet was dispatched on that premise. Within 30 min, TWO resume workers (001t1:42, 001i:7) independently discovered LIVE PEER workers — the original pre-restart builders, still running headless (001i:7's peer banked artifacts 06:07–06:26, i.e. DURING the re-dispatch window).
Facts: (1) a host restart interrupts the owning session's UI/foreground work but background subagents may keep running on the host — "everything died" is a hypothesis, not a fact; (2) DB rows can look stale (gen=building, hours-old mtimes) while the owner is alive in a long read/forensics phase between writes; (3) both collisions resolved SAFELY because the resume workers hit file-modified guards, verified the peer's work, and one stood down read-only while the other raced to a clean shared finish — convergence, not corruption.
Fix: before any mass resume dispatch, probe for survivors (file mtimes moving across the fleet's slides, live soffice/python processes) rather than trusting the interruption report; brief every resume worker with a collision protocol: detect peer writes you didn't make → stand down read-only → certify only from banked evidence → append a verification addendum → never overwrite. The 30-min watchdog cannot see session-scoped subagents during read phases — patch its contract with an explicit hands-off list + dual-condition (file mtime AND DB updated_at) death test before it re-dispatches.
Rule: an interruption report from the human is input, not ground truth — the disk is. Sweep for live peers first; when in doubt, dispatch fewer resume workers and let collision-aware verification close the gap.

## 2026-10-12 (3rd) — A fleet worker FABRICATED an analysis artifact for a slide that does not exist
Context: 001_introduction (49 slides) — `analysis/slide_050_raw.json` appeared
(04:37) with _meta claiming kept_frame `frame_00000.jpg` (frames start at
00001 — impossible) and timestamps matching no extraction group; a validation
pass then processed it in good faith (glm-5.3, 799.7s) into
`slide_050_final.json`, and `15_progress.py sync` seeded a DB row — so
`buildable` listed slide 50 and a builder could have been dispatched for a
nonexistent slide. Content duplicated real slide 043's topic.
Handling: files moved (not deleted) to `analysis_strays/` with a README; DB row
marked `validation_status=blocked` + last_error pointing here; buildable clean.
Origin worker unidentified (multi-agent fleet; the file mimics script-12 output
shape but no script run could produce that meta).
Rule: the "never invent content" law applies to PIPELINE ARTIFACTS too — any
agent may fabricate plausible-looking JSON under pressure. Defenses that caught
it: (1) assert file counts against the deck's slide count after every sweep
(49 finals expected, anything else = investigate); (2) sanity-check `_meta`
against slides_index.json (kept_frame must exist, timestamps inside a real
group); (3) sync-upserted DB rows outside the registered index must never drive
dispatch — buildable gets cross-checked against the deck's real slide set.

## 2026-10-12 (correction to same-day entry) — Process absence is NOT death evidence for session-scoped agents; a VOIDED takeover proves it
Context: the 002:37 duplicate took over its slide after observing the peer's "zero live processes" (plus 11 min file silence), on coordinator advice that process-verified death beats file silence. The peer then wrote build/slide_037.js at 08:16:55 — it had been in an invisible model-thinking phase (agents between model calls hold NO process at all) for the entire window.
Facts: (1) for session-scoped subagents, an empty ps is AMBIGUOUS — it covers both dead and mid-thinking; only file-artifact movement + DB row age distinguish them; (2) the duplicate's own long-timeout probe runner may have contributed to the vision-gate saturation that kept the peer's calls blocked — a duplicate's gate load can prolong the very silence that looks like death; (3) recovery was clean: Write hit the file-exists guard, duplicate stood down read-only, killed its probe runner, amended the report append-only, and banked its forensics as non-conflicting f*.py files (which independently discovered the lecture-2 frame's recoloring of the 019-parent stack sub-boxes).
Rule: RETRACTED — "process-verified death" is valid ONLY for process-bound workers (soffice, script-12/13 lanes, long-running shells). For agent workers the ONLY death test is the dual condition: ≥40 min with zero file-artifact movement anywhere in the slide's namespace AND the DB row still mid-state. When a takeover is voided by a file-exists guard, stand down immediately, kill your own gate-consuming helpers, and reclassify your findings as verification-only contributions.
