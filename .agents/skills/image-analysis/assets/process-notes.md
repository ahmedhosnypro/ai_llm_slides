# image-analysis — lane-facing process rules

Companion to `assets/audit-prompt-template.md` (the model prompt — frozen per
round, bumped between rounds). This file carries the LANE-FACING discipline the
prompt cannot teach: capture recipe rules, verification-cell definitions, and
refutation recording. Applied at the wave-5 between-rounds bump (2026-09-28),
drafted by the skill-amendments lane from provenance in the wave-3/4 outcomes
(`ai/plans/view-audit/wave5/skill-amendments-draft.md` §3) — read it before any
capture-heavy lane.

**WAVE-5 ROUTING + STORM BUMP — 2026-09-29 (v2; v4 additions 2026-09-29 late).**
This bump adds §E (the
echo-class degenerate), §D (background-dispatch law), §S1–§S4 (capture-lane
storm doctrine), and §R (the routes-recover "re-run pending" debt rule), plus
the late-09-29 doctrine set — §G (gateway governance), §V (verdict law), §P
(purpose/subject adjudication), §X (rig classes) and §W (the overnight
close-out doctrines — appended 2026-09-30) — and
records the founder routing law that supersedes model pinning practice
(SKILL.md, "WAVE-5 ROUTING + STORM BUMP" — **DEFAULT IS THE ROUTE: no `--models`,
always**; `nvidia/z-ai/glm-5.3-flash` permitted only as a batched (≥4) consensus
leg; **kimi-k3 BANNED** (founder, 2026-09-29 — a v1 draft of this bump said
"allowed"; that was corrected); gemini/claude BANNED). Every rule stays
evidence-cited per section; the amending lane's outcome is
`ai/plans/view-audit/wave5/skill-amendment-outcome.md`.

## A1 — blur-before-capture (every shot)

After settle-poll and before EVERY screenshot, blur the active element
(`document.activeElement.blur()` via eval, or suppress auto-focus) —
Storybook/Radix auto-focus otherwise pins a focus ring on the first tabbable in
every capture, manufacturing fleet-wide focus-ring misreads. Adjudication
corollary: an accused "accent chrome/ring" that disappears on `blur()` is a
capture artifact, not a product defect — re-shoot before filing.
(Evidence: wave3/WAVE-3-REPORT.md:66-68; applied as practice in
wave4 models:244 / wizard:227 / core-tier:132.)

## A2(b) — refutation recording (the staleness guard's lane half)

The model-facing half (a tag is a class, not a verdict) lives in the template's
KNOWN ISSUE CLASSES preamble. Lane half: when a registered-tag hit is
DOM-disproved on a fixed screen, record the refutation (tag + probe + result)
in your outcome file so the wave report can discount stale hits; on re-captures
of fixed screens, probe the previously-defective computed style before
crediting any re-find. (Evidence: [r3-wizard] vocabulary-state-staleness;
re-confirmed wave4/wizard:253-256, :215.)

## A3 — the narrow-capture window rule

A narrow capture (≤768 wide, or any scrollable/overlay composition) must use a
window tall enough to contain the composition (≥900 tall), or pair EVERY
fold/below-fold/cropped-content finding with a scroll-container probe
(scrollHeight vs clientHeight of the owning container) before it counts as a
defect. For fix-verification cells on scroll compositions, the same-width
taller-window capture is REQUIRED, not optional — short-window fold majors are
evidence-void by default. (Evidence: wave3 report:77-79 — two window-edge-crop
majors manufactured at 700px; wave4/wizard:236,239-245 — 6 findings at 640-tall
became 9 at 900-tall under the rule.)

## A4 — degenerate-body full-page tracking

(a) Full-page captures are the degenerate-prone tier: every round-1
default-model degenerate was a full-page variant while normal-viewport
invocations went 10/10 winners. `scripts/analyze_image.py` should tag every
full-page variant in its [info] line and treat that tier as
pacing/pre-emptive-retry eligible — SPECED, implementation owned by the
orchestrator (scripts/ is orchestrator-fenced), pending post-wave.
(b) Transcript hygiene: a degenerate/garbage response must NEVER overwrite a
valid transcript — write transcript files only for validated winners (a wave-4
welcome loop-3 transcript was lost to exactly this overwrite).
(c) Count degenerate events per-outcome so the tier's failure rate stays
visible across waves. (Evidence: round1/script-proposals.md:234-239;
round1/SYNTHESIS.md:79; wave3/wizard:90; wave4/welcome:286-289.)

## E — the echo-class degenerate (WAVE-5 ROUTING + STORM BUMP, 2026-09-29)

A distinct degenerate family that HTTP-200 and old validators can PASS: the
model answers by PARROTING THE PROMPT — its own instruction language, the
audit prompt's glossary entries, or the numbered section labels — instead of
auditing the image. The pure case is the wave-5 census body
(`scratch/screenshots/w5-route-census/images-group.txt`, 4.1 KB): instead of a
§1–§9 audit it reproduced `[w4-harvest]` vocabulary entries verbatim; because
the echoed prompt is VARIED prose, the repetition gates never saw it
(script-patch H3, CONFIRMED). Lanes must suspect any "winner" whose body
echoes the prompt glossary or contains ZERO §-section bodies — bank it as a
degenerate event, never as findings, and re-route.

Status: the script's validator was HARDENED for real — `_echo_class_reason()`
in `scripts/analyze_image.py` (w5-script-patch v3, on disk this lane) runs four
rules in order and aborts these shapes inside `ask_model`, each returning a
named reason string a lane can match in stderr/logs: (1) **prompt-echo** — any
≥10-word verbatim prompt span; (2) **prompt glossary echo** — ≥3 distinct
≥6-word verbatim prompt passages (the transformed-glossary dump); (3)
**section-header shell** — ≥3 section labels with <80 chars of section body
in total; (4) **section-coverage** — the prompt requires ≥3 numbered sections
and the response covers none of them (the only rule that sees a *transformed*
echo; conservative by construction). Suite cases 29–33 claim green. **[2026-09-29
late — superseded by the `w5-vision-hang-probe` closeout patch: rules (1)/(2) are
now coverage-GATED and the suite is 35 cases; corrected below.]** A lane that
still sees an echo body survive to a transcript should file it against the
patch lane's outcome, not shrug.
(Evidence: `ai/plans/view-audit/wave5/script-patch-outcome.md` §1 H3/§2;
`wave5/route-census-outcome.md` images-group row; WAVE-5-REPORT-DRAFT.md
(now `WAVE-5-REPORT.md`, retitled 2026-09-30) §9.V
— "degenerate prompt-template echo truncated at max-tokens — no usable audit,
the census's echo shape, now seen live".)

**[2026-09-29 late — the coverage gate; the C-SKILL correction owed from
`wave5/vision-hang-probe-outcome.md` §5.]** Rules (1)/(2) now fire ONLY inside
`if coverage >= _ECHO_SPAN_COVERAGE_MIN` (`scripts/analyze_image.py:323`;
threshold `0.30` added at `:173` with the measured-corpus provenance comment),
rules (3)/(4) stay unconditional, and the rule-1/2 reason strings append the
measured `copied-prompt coverage N%`. Measured corpus, 235 live HTTP-200
`images`-route bodies: **legit audits run 0.7–4.9 % prompt-span coverage**
(6–19 KB bodies with real `## 1. LAYOUT MAP` sections — the pre-gate validator
flagged 90/235 = 38 %, 67 of them rule-2-only false positives), **true
dumps/echoes 64.5–77.2 %** (33 KB bodies, 75–86 long runs). Suite is 35 cases
(`34-w5ao2-empty-stream-ladders`, `35-hangprobe-echo-span-coverage-gate`).
Read a flag as a degenerate signal only above the gate; a body below it that
carries a real §-section audit is a WINNER. (The glossary prompts are a defect
VOCABULARY — their presence in a body is normal at these rates.)

## A5(a) — the hover→focus-visible capture path

To capture a hover-armed mechanism (tooltips, hover chips): do NOT force state
and do NOT trust an in-harness "hover" — the agent-browser harness matches
`hover: none`, and Tailwind v4 compiles `group-hover:` under
`@media (hover: hover)`, so the hover path cannot render in-harness at all.
Drive the mechanism's own SECOND sanctioned trigger (keyboard focus-visible)
and capture that. Any "hover styling missing" verdict from an in-harness
capture is VOID without a `matchMedia('(hover: hover)')` check; hover-path
verification on real hardware is a separate e2e concern. (Evidence:
wave4/core-tier:93-101, :237-238.)

## Probe recipes (wave-5 additions)

- Locale-flip probes must match the LOCALIZED command title — the ⌘K palette
  localizes under `ar` ("Switch language" becomes "تبديل اللغة"); select
  palette items by stable command id / list position, or match both registers.
- Re-grep the token, never the audit's line number — sibling-lane drift moved
  4 of 9 mechanical sites between audit and execution; the token + grep recipe
  is the durable contract.

## D — background dispatch (WAVE-5 ROUTING + STORM BUMP v2, 2026-09-29)

Founder law: **every lane dispatch runs in the BACKGROUND.** Vision invocations,
capture commands, and probes are background jobs — inside ONE Bash call ending
`wait` when they must be observed together (the analysis batch pattern), or on
the task runner's background channel — never a foreground serial drip that
holds the lane open. Two hard corollaries: a background job without `wait`
(orphaned) stalls the task rather than helping it; and "ran in the background"
never excuses an unreported result — every background job's outcome is banked
(transcript, exit, or explicit failure) per §S1/§R.

## S — storm doctrine for capture lanes (WAVE-5 ROUTING + STORM BUMP, 2026-09-29)

Earned the hard way: the provider storms of Sep 27–29 killed ~6 dispatch
generations of lanes. The wave report's ledger: "roughly five dispatch
generations (v1→v5) were killed by provider 504s, then rate-limiting and DNS
failures … Every casualty was banked … zero work lost" (§8.L), and the ~20:50
window "killed seven lanes (including this report lane's v1 — dead at the
provider wall before writing anything)" (§9.F). The rules below are what made
"zero work lost" true; every storm casualty that lost work had skipped one.

**S1 — bank-skeleton-first, then append-per-step.** Write the outcome
skeleton (header + one stub per section you intend to fill) BEFORE any field
work, inside the first minutes; bank the PNG/transcript/probe the moment each
exists — never hold evidence in-head. A lane that dies mid-flight then loses
only unreached stubs: light-theme-verify's predecessor died "with only a
skeleton banked" and its successor resumed from it
(`wave5/light-theme-verify-outcome.md`:3-5); `wave5/vision-debt2-clearance-outcome.md`:6-7
"CLAIMS the v2 skeleton (w5-vision-debt-v2, died at the wall before any field
work)".

**S2 — respawn-claims-banked-state.** A respawned lane (v2/v3/…) first READS
what its predecessor banked — skeleton, contracts, transcripts, landed edits
— claims it explicitly in the header, then reconstruct-verifies rather than
redoing. Adversarial-D v1 died mid-hunt "with edits landed but unrecorded, v2
died reading, v3 reconstructed-verified"; runs-ring v1/v2 died at the wall
"with v3 reconstruct-verified" (§8.L). eslint-toolchain v2 re-derived its
crash from scratch and verified the landed fix by reading the files
(`wave5/eslint-toolchain-outcome.md`:5).

**S3 — disk-mtime is the ONLY liveness truth.** Never trust task status,
memory, or a lane's own claim that work is done: check the file's mtime/size
on disk (and re-read it) before acting. The eslint-toolchain v1 "died after
the repair landed on disk but before its bank reached this file" — the files
carried 23:39:53/23:40:42 mtimes while the banked outcome still held the
stale template (same file, :5). Sibling lanes are the same: an mtime 18s
before your probe means you are inside a live edit window and judge NOTHING
of that file (`wave5/brand2-dark-verify-outcome.md`:304-336).

**S4 — script-error delegation (standing founder delegation; re-affirmed v2,
2026-09-29).** Subagents are AUTHORIZED to patch `scripts/analyze_image.py`
when it errors — standing delegation, no prior grant needed, not a fence
violation. The one fence: while a DEDICATED script-patch lane is live, only
that lane edits the script; every other lane files a proposal to it, never
parallel edits. The delegation exists because the script is the fleet's shared
sensor — a broken sensor costs every lane downstream (founder law,
`wave5/WAVE-5-REPORT-DRAFT.md` (now `WAVE-5-REPORT.md`, retitled 2026-09-30)
§9; the w5-script-patch lane is the recorded implementation).

**Storm-signature taxonomy (count events; never fake one).**
- **"Background agent task stopped" arriving as a batch** across concurrently
  dispatched tasks is the dispatch-side signature of the provider wall (the
  ~20:50 window that killed seven lanes at once, §9.F). A batch stop is storm
  truth, not your failure: bank what you have and respawn under S1/S2.
- Transport failures, in the order observed: **504 provider timeouts → TLS
  failures → rate-limiting → DNS failures** (§8.L); overlay routes: HTTP-400
  invalid-key combos and read-timeout hangers (the census table inventories
  them, `wave5/route-census-outcome.md`:29-57). Retry with PACING — cheap
  `/v1/models` liveness probes that do not burn real attempts, ≥10-minute
  spacing, waits spent on other banked sections (deferred-vision-upgrade's
  patience protocol, `wave5/deferred-vision-upgrade-outcome.md`:5,16).
- **Servers are taken AS FOUND — never restarted.** A capture lane that finds
  Storybook 6055 / the dev app answering at all uses them as they are; restarting
  a shared server to "clean" it destroys other lanes' evidence and is out of
  fence everywhere (6055 never restarted, 6006 never touched). If a server is
  down, that is a storm datum (§R), not a repair task.
- **The 5xx ladder: 5xx → wait 30s → re-probe ONCE → then pace.** A single
  transient 5xx earns exactly one paced re-probe after ~30s (cheap, e.g.
  `curl -s -o /dev/null -w '%{http_code}'` against the route behind the gateway);
  a second failure puts the route on the paced-probe schedule above (≥10-min
  spacing) and the lane proceeds on §R. Blind rapid retries convert one storm
  into an account-wide block — the reason this ladder is short and explicit.
- Never wrap `analyze_image.py` in retry loops; its internal ladder plus your
  pacing IS the retry story. Count every degenerate/timeout event in the
  outcome so the storm stays visible across waves (A4c).

## R — routes recover: the "re-run pending" debt rule (WAVE-5 ROUTING + STORM BUMP, 2026-09-29)

When the wall blocks every allowed route after paced retries, a vision-gated
lane does NOT close blocked and does NOT fake a verdict. It banks
deterministic evidence + a named "re-run pending" debt:

1. Bank the PNG (PIL-checked) + every transcript that DID answer + a DOM
   probe for anything structural — the deciding evidence must not depend on
   the missing model.
2. In the outcome's §Vision, write **"re-run pending"** together with THE
   EXACT RE-RUN COMMAND — the full `analyze_image.py` invocation, the banked
   PNG path, and the routing it needs (under the v2 law that is simply "no
   `--models`", plus a batched glm leg only where a ≥2-model consensus is
   required AND ≥4 images are banked) — so a later lane can clear it verbatim
   without reconstructing your context.
3. Record the failure honestly: routes tried, timeout/degenerate counts,
   attempts. "Consensus NOT achieved — re-run pending, nothing faked" is a
   complete, closable state.

A later lane (or a dedicated debt-sweep lane) clears the row once routes
recover and appends a dated DEBT-CLEARED annotation to the OWNING outcome.
**v2 correction: a banked re-run command that pins a now-BANNED route is
itself stale.** kimi-k3 is banned (founder, 2026-09-29) and gemini/claude were
already banned, so a debt banked against any of them is cleared by re-running
the banked PNG under the CURRENT routing law — the default `images` route, no
`--models` (plus a batched glm leg only if a ≥2-model consensus is still
required and ≥4 images are banked). Do not resurrect the banned pin to
"honor" the banked command; note the substitution in the DEBT-CLEARED
annotation instead.
Tonight's evidence: the kimi-k3 504 wall left zerogroups one model short with
the command banked — "One rerun of analyze_image.py on
`zerogroups-1440x900-v2.png` … completes the consensus when the route recovers"
(`wave5/zerogroups-arm-outcome.md`, Vision §; the banked command's
`--models kimi-k3` is superseded per the correction above); the
vision-debt-clearance lane swept `grep 're-run pending'` across all wave-5
outcomes and cleared the rows against BANKED PNGs — "no PNG was re-shot"
(`wave5/vision-debt-clearance-outcome.md`:16-25); a4a's storm-blocked model A
was re-run on the banked PNG when the wall lifted
(`wave5/a4a-consensus-adjudication-outcome.md`:192,208); five such debts were
formally claimed and serviced by `wave5/vision-debt2-clearance-outcome.md`.

## G — gateway governance (pacing, walls, wrappers) — v4, 2026-09-29 late

The gateway is a shared, capacity-bounded resource; every rule here exists
because a lane skipped it and paid in the fleet's budget.

- **≤2 concurrent invocations per lane per Bash call, ~15 s spacing between
  dispatch waves.** The observed-good shape: `w5-blocked-frames-rerun` §2 ran
  16 frames at ≤2 concurrent / ~15 s spacing and got **15/16 valid bodies on
  attempt 1**; `w5-regrade-ao` v3 ran its probe loop under ~5–7 sibling calls
  and needed its one retry. More concurrency does not buy wall-clock back — it
  queues behind the same cap and manufactures HangErrors that are fleet-wide,
  not yours.
- **Probe FIRST with ONE short-wall call** — `--timeout 120 --rounds 1 --tries 1`
  on an already-banked PNG, so the probe's verdict DOUBLES as that frame's
  analysis (no call is wasted). A valid body opens the window; a hang ⇒
  `sleep 300`, re-probe ONCE, then close on §R rather than burning the window.
  Evidence: `w5-blocked-frames-rerun` P1 returned valid on attempt 1 (window
  open, no sleep needed); `w5-regrade-ao` v3 attempt 1 `HangError @150s` →
  attempt 2 valid — the slow-first-token class, not a dead route.
- **270 s walls: `--timeout 240 --rounds 1 --tries 1`** is the standard
  invocation wall (the script's own hard guard fires at 270 s; its internal
  ladder owns the retries — never wrap `analyze_image.py` in retry loops, §S).
- **Wrap the shell command in `timeout 300`** — wider than the script's own
  270 s guard. A `timeout 270` wrapper RACES that guard: the abort is killed
  before it can be logged and the failure vanishes silently — no
  `degenerate events` line, no transcript (BF-TOOL; `w5-blocked-frames-rerun`
  §2 note 2, R14's first attempt). With `timeout 300` every abort still writes
  its transcript.
- **The gateway's combo router is not your dial.** When the default `images`
  combo retargets to a saturated first target (the cap-1 glm leg:
  `comboStepId=images-model-1-nvidia-z-ai-glm-5-3-flash`, `status=499 dur≈280 s
  out=0 tokens`, 463–817 s generations queued fleet-wide — `w5-vision-hang-probe`
  §2/§4), every lane's 270 s wall fires INSIDE a queue, and SSE keepalives hold
  the connection so no read-timeout can ever fire. That is gateway-side
  capacity, not a lane defect and not a script bug: pace, bank, and use §R;
  never "fix" it lane-side.

## V — verdict law: what counts as evidence — v4, 2026-09-29 late

From the evidence index's own method law (`EVIDENCE-INDEX.md` findings 3/4/8 /
11, L-METHOD): **a winning leg is not certification.**

- **Verdicts must be banked to FILES at run time.** A verdict that only ever
  existed on stdout is not evidence. Only `[winner]`-body transcripts certify —
  a dead leg still writes its `models:` header, so a HangError transcript would
  otherwise score as "a route graded this capture" (`w5-evidence-index` method).
- **Banned-route verdicts are VOID.** kimi-k3/gemini/claude/agy legs produce no
  citable verdict under the routing law: 57 captures across 19 lanes were VOID
  on that ground, 40 of them with no default-route re-grade on disk
  (`EVIDENCE-INDEX.md` findings 2–3; `w5-regrade-banned` S7 "kimi-k3 legs VOID").
  Re-grade under §R on the default route; never quote the banned read.
- **A refuted frame is RE-OPENED wrong-subject debt, not a cleared row.** When a
  default-route read shows a banked frame cannot certify the claim it was
  captured for, the owning lane's COMPLETE verdict does not survive:
  `orch-options-1440x900.png` does NOT show an open options menu (two
  independent high-confidence reads) → VT-1 RE-OPENED (`w5-void-triage-v2`;
  same class as finding 8 — four winning reads of Storybook's error overlay
  cannot certify a StatePill).
- **Single-model default-route certificates are VALID — with the honest-record
  clause.** State it: "glm leg DEFERRED/BLOCKED" (8/8 HangError @330 s, backend
  cap 1; the batch rule stands if it recovers). All 16 `w5-blocked-frames-v2`
  certificates carry exactly that clause (BF-CLEAR). Never fake a consensus.
- **Prefer PRE-REGISTERED, falsifiable predictions.** Write the expected numbers
  BEFORE the capture (hv21's banked AFTER prediction: card 142→358, line 72→288,
  title ≈31.6→≈150.4 @390×844; listrow's static prediction recorded before its
  DOM probe) so the verdict is decided by MEASUREMENT — and the DOM/source wins
  any disagreement.

## P — purpose lines, subject, and adjudication (false-positive classes) — v4, 2026-09-29 late

- **Author every purpose line from the fixture's ACTUAL state.** Read the story
  source / DOM signature FIRST, then write the `--view` purpose. A mis-stated
  fixture manufactures a false FAIL: the rtl-stragglers initial FAIL was an
  artifact of a mis-stated fixture locale in the authored purpose line, and the
  corrected-purpose re-grade of the SAME BYTES is the banked PASS (VT-3).
  Purpose lines are evidence — author them like evidence.
- **Route-counting is not evidence.** A frame can pass a count (PIL-clean, four
  winning reads) while depicting the WRONG SUBJECT: the decision-pack StatePill
  set's winning transcripts describe Storybook's error overlay, not the
  component — "count the winners" would certify an error page
  (`EVIDENCE-INDEX.md` finding 8). Read what the transcript SAYS about the
  subject, not that a winner exists.
- **Adjudicate every vision FAIL against DOM/source truth before filing** (the
  skill's ADJUDICATE stage; the banked refutation recipe): `scrollW == clientW`
  on an accused clip disproves the clip; `w5-rig-recovery`'s "title-bar string
  cut off mid-glyph" FAIL was refuted by geometry — the glyph box starts 9 px
  INSIDE the 720 px bar (1 px border + 8 px `px-2` padding), no self-overflow,
  nothing truncated (the model read the bar's border as a clip line). FAIL is a
  LEAD, never a verdict.
- **Unrenderable stories: the validated direct mount + single-variable CSS A/B.**
  When the story frame cannot be produced (rig defect), mount the story's OWN
  exported render component in the real Storybook iframe — same document, same
  fonts, same `globals=theme:*`, same viewport, dynamic-importing the SAME module
  URLs Storybook loads (timestamped story module + i18n module), inside the same
  provider/decorator wrapper, as an ELEMENT (`createElement(Story.render)`).
  Then PROVE equivalence: inject CSS forcing the changed variable back to its
  baseline value and reproduce the recorded baseline numbers EXACTLY — listrow
  Validation A's `max-width:40% !important` reproduced 286 / 194 / 182–252 /
  39.6 % / false; the new state is then a single-variable A/B in the same render
  (16 measured cases + the validation arm; light geometry verified identical to
  dark 8/8). A direct mount without the equivalence proof is a new rig, not a
  certificate.

## X — rig classes and staleness reflexes — v4, 2026-09-29 late

- **Gate on SETTLEMENT, and know its failure mode.** The capture gate is "no
  writes for ≥10 min across the writer's dirs" (smoke gate (a):
  `ui/src/components/**` + `ui/src/i18n/locales/storybook/**`) — BUT a bulk
  writer re-emitting files makes mtime-guards non-convergent: a **36.1-min
  quiet stretch looked settled**, then the campaign resumed at ~1 file/min
  after it (HV21-PREMISE). A single quiet sample yields a false settled window;
  gate capture lanes on the thing that actually unblocks them (the fix landing
  — `preview.ts` bytes/mtime), never on campaign quiet alone. Record md5+mtime
  per arm; a writer that re-emits byte-identical content can silently revert an
  edit — re-verify by `md5sum` after any edit and again before any commit.
- **Stale acorn index → `/index.json` 500 → every iframe blank.** Signature:
  `Unable to index files: … Could not parse import/exports with acorn` while the
  story module itself still compiles (vite transform 200). It is a mid-write
  artifact of the editing lane, not a rig death: **remedy = a content-neutral
  `touch` of the named files, with md5-before/after proof the bytes did not
  move — NEVER a restart** (rig-recovery: the 6055 restart grant was revoked and
  the index healed by the authorized md5-neutral touch, 200 / 398 entries).
  Captures are HELD and retried in 10–15 min; nothing blank is ever recorded as
  a product finding.
- **Migrated stories throwing `next-typed-intl [INVALID_CONFIG]: no
  <I18nProvider> found above this component` = render-path defect class, not
  staleness.** Root cause shape: `.storybook/preview.ts`'s decorator calls
  `Story()` eagerly, so hooks in story `render:` arrows execute ABOVE the
  provider element the decorator returns; the fix is `createElement(Story)`
  (element render), not a restart. **Discriminate staleness with the SAME-FILE
  test: one export with a hook in `render:` throws while another export of the
  SAME module instance renders** (brandmark `--labeled` throws / `--default`
  renders, `probes.jsonl`) — no stale or duplicated module can differ between
  two exports of one module. A restart does not fix this class; do not ask for
  one.

## W — the overnight close-out doctrines (corpus + debt, 2026-09-30)

Source: `SKILL.md` `## AMENDMENT 2026-09-30 — the overnight close-out doctrines (wave-5)`, lines 220–325 — extracted verbatim (heading included, diff-verified byte-identical) by lane `w5-skill-assets-sync`.
Mandated by `ai/plans/view-audit/wave5/skill-amendment-outcome.md` §P2.4 (owed forward); landed and verified 2026-09-30 (§P2.8 there records range + hashes).

## AMENDMENT 2026-09-30 — the overnight close-out doctrines (wave-5)

Appended by the wave-5 skill-amendment lane (outcome:
`ai/plans/view-audit/wave5/skill-amendment-outcome.md`) from the campaign's final
night (2026-09-30 00:0x–02:0x). Version 1.1.0 → 1.2.0. Nothing above is
superseded or rewritten — these are additions, and where a rule already exists
above (noted per item) the item only sharpens it. Lane-facing operational detail
for W1–W6 is OWED to `assets/process-notes.md` §W (paste-ready text banked in the
outcome file, §4 — this lane's write fence covered this file only).

**W1 — a wedged agent-browser SESSION is repaired by closing YOUR OWN session,
then using a FRESH name.** Symptom: every `Runtime.evaluate` dies on a CDP timeout
(~30–75 s; ~2.6 min/id) while the same story measures in seconds elsewhere.
Diagnosis: re-probe ONE already-failed id in YOUR OWN session — the corpus's
`ui-core-toast--default` measured DEFINITE in 2.6 s there, which localizes the
wedge to the FAILING session's own browser, not to Storybook, the stories or the
daemon. Repair, in order: (1) `agent-browser --session <your-session> close` —
never `--all`, never another lane's session, never a daemon/server restart; it
typically recovers IN FLIGHT (347 ids in ~11 min at 2–3 s/id after the close, ~4×
the expected rate); (2) if timeouts return (close+reuse drifted back in ~12 min),
re-run under a FRESH session name — the durable fix (a fresh session settled 4/4
ids in 168 s). `prune` and restarts are LAST resorts, and only when the lock tool
itself reports stale holders — the lock was healthy throughout (live PIDs, 0–1 of
4 slots). Standing trigger: a memory-pressured machine (1.7 GB available, an
unrelated 6.5 GB process, 3 browsers). (Evidence:
`ai/plans/view-audit/wave5/corpus-hardening-outcome.md` §"Skill-amendment input"
(i); `…/smoke-v3-resume-outcome.md` §"The in-flight wedge";
`…/OVERNIGHT-FINDINGS-REGISTER.md` §9 ~01:0x delta; `…/WAVE-5-REPORT.md` §10.11.)

**W2 — a blank document is NO-RESULT, never a definite verdict.**
`childCount = -1` means `#storybook-root` was absent: the page was blank
(mid-navigation when the browser was interrupted/closed) — a harness artifact,
not a story verdict. Bank it NON-DEFINITE (`noResult="blank-document"`), retry it
once in flight, and keep it out of every `done`/progress counter so a later run
re-probes it. Why the rule exists: two Toast rows with
`cc=-1, dir='', lang='', snip=''` were banked FAIL and then SILENTLY SKIPPED by
every resume (`"childCount" in r ⇒ done`) until a fresh session restored both to
PASS — a hidden failure is worse than a crash. Generalization: any observation
that is not a real document observation (no `childCount`, an exception) is
NO-RESULT and stays re-probable. (A blank CAPTURE from a stale acorn index is the
different, already-governed case — §X: hold and retry, never a finding.)
(Evidence: `ai/plans/view-audit/wave5/corpus-hardening-outcome.md` §2 P2 + its row
table; `…/smoke-v3-resume-outcome.md`; `…/WAVE-5-REPORT.md` §10.11 — the
re-adjudication moved PASS 398→399, FAIL 1→0.)

**W3 — text-free visual components need a GEOMETRY BRANCH in the verdict
predicate, and "definiteness" and "pass/fail" are SEPARATE questions.** A
component that renders no copy and no SVG by design (ProgressBar is the exemplar —
its own story declares "renders no copy") cannot be adjudicated by text presence;
a text-or-svg predicate false-FAILs a correct render. Extend the predicate to
accept, in addition to text/svg: (a) **DOM geometry** — ≥1 visible
child/descendant box ≥4 px² inside the story root, respecting `display` /
`visibility` / `opacity`; or (b) **non-blank pixels** — content pixels beyond the
story frame's modal background (count ≥32, bbox ≥2×2); (b) is decidable OFFLINE
from the banked PNG, (a) needs one line in the live probe. Worked example — three
independent facts, all agreeing with the story's declared `progress: 0.65`: DOM
`track 736×3 / fill 478×3 = 64.9 %` ≡ declared `0.65` ≡ pixel `65.0 %` (content
bbox 736×3, 2208 px), measured on a screenshot byte-identical to the banked FAIL
PNG (`8303d54fff78c89c…`). Reporting corollary: a *definite* row can be PASS or
FAIL, and only definite rows count as corpus progress (see W2). (Evidence:
`ai/plans/view-audit/wave5/corpus-hardening-outcome.md` §3 + §"Skill-amendment
input" (iii); `…/smoke-v3-resume-outcome.md`:86; `…/WAVE-5-REPORT.md` §10.11.)

**W4 — a hard-wall `HangError` (rc 124) is usually a WALL artifact: retry ONCE
under the wider wall BEFORE banking it as debt.** The night's one casualty
(`HangError: hard wall-clock 270s exceeded`) graded cleanly on its first attempt
under the wider wall: `[winner] images (round 1, attempt 1)`,
`degenerate events: 0`, `rc=0`, **in 68 s of a 420 s budget**. Same PNG, same
route, same prompt; the only change was `--timeout 420` wrapped in `timeout 540`
instead of `--timeout 240` wrapped in `timeout 300` (the wall is `--timeout` + 30 s,
computed in `scripts/analyze_image.py`). So the 270 s signature is not
a deterministic property of the frame, and a debt row banked from a single
hard-wall hit is larger than it looks. Cost: 1 call. This is a classified single
retry, NOT a retry loop — §G's "never wrap `analyze_image.py` in retry loops"
stands, and §G's short-wall probe ladder still owns the window-open question.
(Evidence: `ai/plans/view-audit/wave5/vision-debt-v4-outcome.md` §9.3 + §9.7.)

**W5 — sha-check the frame BEFORE spending a vision window.** Hash first: a frame
whose bytes are already certified inherits its certified winner's verdict at ZERO
calls — 15 of 18 default-BLOCKED ledger rows were cleared this way (8 of them
without any gateway call), and the debt finish then collapsed 81 of 124 rows by
certified byte-family (47 own + 29 byte-identical + 5 minted), the 124 rows
resolving to 103 distinct byte-contents. Method: (1) sha256(16) the candidate;
(2) compare against the certified byte-families listed in
`ai/plans/view-audit/wave5/vision-debt-v3-outcome.md` §8.2 (extend that list as
you certify); (3) before inheriting, confirm the sibling's log carries
`models: images` AND a winner marker (`[winner]` / `validated winner`) — a dead leg
still writes its `models:` header (§V); (4) a PIL-pixel-equivalent near-twin
(meanΔ ≤ 0.10, pctGT8 ≤ 0.25 %) is also a zero-call class, quoted with its
tolerance. Zero-vision-cost CLOSURE PROOFS work the same way: map witnesses by
sha16 and require, per row, a real transcript (≥8 sections, ≥4000 bytes, no
harness text in the body) — `verify-finish.py` proved 26/26 remainder rows
witnessed, EXIT=0. (Evidence: `…/vision-debt-v3-outcome.md` §3.1 / §8.2 / "Net on
the ledger rows"; `…/OVERNIGHT-FINDINGS-REGISTER.md` §9 ("sha-check before
spending a vision window is now doctrine"); `…/vision-debt-v4-outcome.md`
§PHASE B.)

**W6 — label every banked verdict: `single-read` vs `corroborated`.** Verdicts and
findings carry their leg count in the register — "single-read, unconfirmed" (one
default-route read, no confirmer; the honest label for most of the night's tail)
vs corroborated (name the second read and the single question it was asked).
Never phrase a single read as a consensus, and never bank a claim as a defect when
two reads CONTRADICT — advisory at most; a verdict would need a two-model
consensus. This sharpens, and does not replace, §V's "never fake a consensus" and
its single-model certificate clause. (Evidence: `…/vision-debt-v4-outcome.md`
§9.2 + §9.7; `ai/plans/view-audit/wave5/EVIDENCE-INDEX.md` findings 11 and 13.)
