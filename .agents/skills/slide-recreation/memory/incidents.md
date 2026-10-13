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

## 2026-10-12 — Dead worker's handoff state was BEHIND its own disk: measure the invariant, don't trust the journal
Context: resumed the 002_transformers_part2 OMML wrap pass from a dead worker's banked
state (scratch/omml_wrap/). The handoff said wrapped = {011,015,031,040,054}, still-plain
= {010,020,021,025,032}, and flagged 030 as "may have been missed by the original pass".
Facts: disk truth was 7 already-wrapped slides — 030 (76 mc:AlternateContent) and 053
(2 AC) had been wrapped AFTER the last provenance_results.json write (15:53 vs pptx/qa
mtimes 16:35–17:56); the worker died before updating the journal or writing their
qa/slide030,qa/slide053 omml_wrap_reports. Conversely the "still-plain" five were all
correctly plain (025/032 with documented skip reports).
Fix: on resume, (1) measure the invariant directly — count `mc:AlternateContent`/`oMathPara`
occurrences (grep -o, NOT grep -c: slide XML is one line, so -c returns 1 for any hit and
hides multi-equation slides) across the WHOLE deck; (2) cross-check journal mtime vs
artifact mtimes to detect post-journal work; (3) re-verify the undocumented wraps instead
of re-wrapping (idempotence probes + LO pixel gates) and backfill the missing qa reports.
Rule: a dead worker's provenance journal is a LOWER BOUND on completed work written some
time before death — always re-measure the deck-wide invariant from the artifacts before
acting on the handoff lists, and treat "may have been missed" flags as unverified either way.

## 2026-10-12 — Resumed a founder-fix program the watchdog had "repaired" against a STALE PASS transcript
Context: 002_transformers_part2 slide 005: attempt-3 PASS (09:14) predated the founder's
2026-10-12 arrow-attachment defect; the attempt-4/5 fix worker died on an upstream provider
timeout at the very end of attempt 5 (build 18:33, render 18:37, verification m40 run 19:09,
never reported). DB row left `gen_status=building`, `visual_check=PASS` (attempt-3, stale).
Facts: resuming per the resume rule (banked m40 + crop legs + component header) was enough to
finish without any rebuild — m40's lone FAIL pixel-adjudicated as a predicate artifact
(m41 13/13), the attempt-4 crop legs bound to the current render via m40's own diff
confinement (d1/d2/d3/connect_tan pixels identical 4→5), and one fresh full judge
(judge_attempt_6) certified the fix. Meanwhile the watchdog examined the mid-program row at
21:45 and appended a `last_error` note that it had "repaired from disk evidence only" using
the STALE attempt-3 transcript — a state that briefly coexisted with the live fix program
(row was `judging` at the time).
Fix: certified with the fresh transcript, then cleared the watchdog's stale last_error note
(it described a state that no longer existed and would have misled the next dispatcher);
kept heartbeats in qa/slide005/ throughout so the watchdog could distinguish a live fix
program from a zombie.
Rule: on a resume, the DB's visual_check can be a PRE-DEFECT PASS — the founder defect
report, not the DB, is the state of record; a watchdog repair note in last_error referencing
a superseded transcript is stale the moment a fresh judge lands, and should be cleared at
certification. Heartbeat files in the qa dir are what keep the watchdog from re-dispatching
over a long (judge-wait) silence.

## 2026-10-12 — dual-builder collision on slide 047 resolved by claim/watch/provenance contract
Context: videos/deep-learning/002_transformers_part2 slide 047; the watchdog dispatched a
second builder into a unit that already had a resumed builder (me) waiting on the 046-fix
marker. Coordinator issued a claim (.claim_<agent>) / watch (.watch_<agent>) / provenance
contract. I claimed first → SENIOR; senior + other builder alive → WATCH MODE (no build
writes; poll 10 min; 60-min-silence takeover rule; _b suffix rule).
Mistake avoided: two builders building the same slide concurrently (wasted judge calls,
clobbered attempts, double DB writes).
Fix: watched while the other builder certified 047 (attempt 1, PASS, judge 22:24). Ran the
contract's provenance verification at certification: its build (22:16–22:27) required NO
046 component bytes at all (header documents m18_ffdiff: frames 046/047 share only outer
margins → full re-style, fork of the 045/046 mechanisms) and ran AFTER the fixed 046 bytes
landed (22:03) — so the taint condition ("used the OLD wobbly component") was doubly unmet;
accepted the certification, stood down, no duplicate build.
Rule: when a contested certification lands, verify WHAT BYTES the build actually consumed
(require lines + mtimes + component header rationale) against the defect timeline — not
just whether a marker file exists; a self-contained build that consumed no tainted bytes
is clean even without the marker.

## 2026-10-12 — dead-fixer handoff: completing a fix that died between "build done" and "judged/certified/marked"
Context: 002_transformers_part2 slide 046 arrow de-twist. The afix worker completed the
fixed build (deliverable pptx 22:28, render_2.png 22:28, component re-banked 22:28, a
4-file measurement series afix_trace_3/edges_3/native_3/600dpi_3) and died on an upstream
provider timeout ~22:25-22:28 — before any judge, before DB certification, before the
.slide046_fixed marker. DB row still `visual_attempts=1` bound to the PRE-FIX
judge_attempt_1.txt; the marker a slide-47 builder's provenance check keys on was missing.
Fix (finisher sequence, ~40 min, zero rebuilds): (1) reconstruct the fix from the banked
measurement files + scratch/slide046_afix/ (before_rebuild/ preserved the superseded
attempt-1 component, canon_before.npy the traced centerline); (2) independent PIL verify
(afix_verify_4.py -> afix_verify_4.txt) with fresh 600dpi edge numbers; (3) fresh LO render
of the delivered pptx -> 0/2,251,125 px vs render_2.png (proves the banked render IS the
deliverable, per the 0-diff identifier law); (4) rebuild from the re-banked component ->
0/2,251,125 px again (component = judged pixels) + chrome check; (5) fresh judge at the W4
wall with the founder-directed-fix GROUND RULES clause -> judge_attempt_2.txt PASS; (6)
certify with visual_attempts=2 + the fresh transcript; (7) write the marker; (8) report
addendum in worker_report.md. Attempt-1 evidence untouched throughout.
Rule: a dead fixer's banked measurements are the resume point, not a reason to re-derive —
verify (0-diff render bindings + one independent metric pass), judge fresh, certify, THEN
write the marker; the marker is the LAST artifact, written only after the transcript that
justifies it exists.

## 2026-10-12 — Compaction self-amnesia: a SOLO worker re-discovered its own certification chain as "peer writes"
Context: 001_introduction slide 025. Two builders had raced (21:05 + 21:24 dispatches); #2 stood down clean at ~22:58 (verified: no writes). #1 then reported "the peer kept writing" — script edit 23:03, rebuild 23:04, render, judge payload 23:08, judge transcript 23:15, DB pass 23:15:48 — and set out to "adopt the peer's build".
Facts: #2 had already exited with a zero-writes report; the watchdog does not judge; #1 was the ONLY live agent in the window and stayed alive through 23:26. Conclusion: #1 executed the whole certification chain itself across turns whose details were compacted out of its context, then misattributed its own artifacts to a phantom peer.
Why nothing was lost: (1) the coordinator messaged #1 the concrete on-disk facts with mtimes, so it READ before writing (banking law) instead of overwriting; (2) banked-PASS-terminal meant once the transcript+DB were found it stood down instead of re-judging; (3) the certificate's validity never depended on authorship — only on the real gate transcript + DB row, both verified independently by the coordinator.
Rule: an agent's "who wrote this" attributions are UNRELIABLE after long runs — before treating observed fresh writes as a peer's, enumerate every candidate writer INCLUDING the observer itself (duration/mtime math: if only you were alive, it was you). Coordinators: when relaying state to a long-running worker, include absolute mtimes and the full write-chain; workers: re-stat + read-first is what saved this — never rebuild over artifacts you cannot attribute.

## 2026-10-13 — Stale handoff summary said "mid-campaign" when the task was already certified; the dispatch's "expected 49" was falsified by measurement
Context: 002_transformers_part2 slide 048. The continuation session's handoff summary
described the worker as "in the middle of a measurement campaign"; the dispatch brief
listed a full build/judge/certify program and stated the badge's expected printed value
was "49" (from three raw transcriptions + the validated spec), mandating a prominent
mismatch flag if the print disagreed with the file id.
Facts on disk (discovered by stat + read-first, before any work): the ENTIRE program had
already been executed by the prior session of the same task in 1 attempt — build/slide_
048.js (00:14), render_1.png, judge_attempt_1.txt PASS (00:28), DB gen_status=passed/
visual_check=PASS (00:29), worker_report.md (00:30). The only genuine open item was the
badge conflict, and re-measurement (ring-arc-located fixed-window sibling IoU, scratch/
slide048/m24/m25) proved the print IS 48 — the dispatch's "expected 49" was a false
prior from misreads of the occluded digit, so the mandated mismatch flag became a
"mismatch refuted, evidence banked" flag instead.
Handling: no rebuild, no re-judge, no second attempt; certification chain verified
intact, worker_report.md badge section strengthened + addendum appended, lessons
recorded.
Rule: a handoff summary is a hypothesis about disk state — stat the deliverable, qa/
dir, and DB row BEFORE resuming any phase of a compacted task; and a dispatch's
"expected" measurement value is a claim to test, never a target to write — the frame
wins over both the dispatch and the transcriptions.

## 2026-10-13 — Dead-worker succession from RESUME.md: resume from the NEXT line with documented, judge-arbitrated deviations
Context: 002:057. Coordinator redirect mid-storm: "stop measuring; resume from builder3 checkpoint". Builder3 had CLAIMED 57 (01:05) and banked a full measurement corpus + composition verdict (057 = 049 restyled) but wrote no build file. Liveness test: claim timestamp stale 60+ min (STALE_MIN=40), build/slide_057.js ABSENT, nothing under recreated_pptx/ younger than 25 min → dead.
Handling: resumed EXACTLY from RESUME.md's NEXT line (append-one-line-per-step contract). Two deviations from builder3's banked draft were taken, each evidence-weighed and documented in the RESUME entry itself: token labels [0..5,N-2,N-1] not [N-1,N] (049-identity law + fresh 3x storm reads), first word column x114.5 not 83 (word-box + stack-dot censuses). All other banked verdicts adopted as-is. The judge then arbitrated the deviations in our favor (attempt 2/3 verdicts). Builder3's measurement files were kept banked as extra evidence; nothing deleted; RESUME entries appended for every subsequent step (build, dispatch, fail/fix, pass, certify).
Rule: a stale claim (age > STALE_MIN) + absent named artifact = dead owner; resume from the RESUME log's NEXT line, adopting banked verdicts unless fresh evidence contradicts them — and when you deviate, state the deviation + evidence IN the resume entry so the judge transcript and the log tell one consistent story.
