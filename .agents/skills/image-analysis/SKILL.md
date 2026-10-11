---
name: image-analysis
version: 1.4.0
description: Harsh multi-model UI/UX screenshot auditing through the local vision gateway. Use whenever the user asks to analyze, audit, critique, or verify any screenshot, capture, or rendered view (app, Storybook, design comps) — including "find visual defects", "score this view", "compare captures", "verify the fix visually", "run the visual gate", or any multi-model/differential image analysis. Also use when a subagent needs vision evidence for a UI task. Covers capture discipline (agent-browser under the RAM lock), per-image vision analysis via scripts/analyze_image.py, cross-model differential adjudication (DOM-verify before believing), severity-ranked defect registers, and the self-improving shared prompt vocabulary.
---

# image-analysis — multi-model UI screenshot auditing

Audits rendered UI by capturing screenshots and analyzing each image through the
local vision gateway (`scripts/analyze_image.py` against http://localhost:17844),
then adjudicating the findings against the live DOM. Built from Harhaial's
round-1 view-analysis wave (2026-09-26): 8 views × 3 models × 2 contexts, with
every rule below earned from field evidence.

## The tooling contract

`scripts/analyze_image.py` — path is RELATIVE to this skill's directory: the
`scripts/` dir sits alongside this SKILL.md (i.e. `<skill-root>/scripts/analyze_image.py`),
NOT at the repo root. Invoke it from the skill root, or resolve the path from the
SKILL.md location. Strict CLI, 4 modes (analysis/comparison/
batch/per-image). Read `scripts/analyze_image.py --help` once before first use.

Lane-facing process rules — blur-before-capture, the narrow-capture window rule,
degenerate-body tracking (incl. the echo-class, §E), the hover→focus-visible
capture path, refutation recording, the locale-flip probe recipes, the
capture-lane STORM DOCTRINE (§S1–§S4), the routes-recover debt rule (§R1), and
the late-09-29 doctrine set — gateway governance (§G), verdict law (§V),
purpose/subject adjudication incl. false-positive classes (§P), and rig-class
reflexes (§X) — live in `.agents/skills/image-analysis/assets/process-notes.md`. Read that
file once before any capture-heavy lane; the audit-prompt template itself is
frozen and carries only the model-facing rules.

Key flags and their reasons:

- `--view "Name — purpose"` and `--capture "WxH CSS px, scale, app|storybook"`:
  context injection, built into the script. ALWAYS pass both — the original
  round-1 lane that skipped them produced transcripts whose models explicitly
  complained the context was missing, degrading every judgment downstream.
  Author the purpose line from the fixture's ACTUAL state (read the story
  source / DOM signature first): a mis-stated fixture manufactures a false
  FAIL, and the corrected-purpose re-grade of the same bytes becomes the
  banked read (process-notes §P).
- `--max-tokens` (default 8192): §1–§9 audit responses truncated mid-body at the
  old 4096 default; the script now WARNS when a winner reaches ~85% of the budget
  ("likely TRUNCATED") — treat that warning as a re-run signal, not noise.
- `--timeout 240 --rounds 1 --tries 1`: the standard invocation. The script
  internally aborts hang/garbage API calls at a hard wall-clock deadline and
  retries up to 3× on its own — stderr lines like `ABORT GarbageError … abort+retry
  2/3` are script-recovered events. COUNT them in your reliability stats; they are
  not your failure, but they are your data.
- `--models <id>` pins ONE model per invocation. The script races and returns the
  first working response — for DIFFERENTIAL analysis (who caught what), you must
  pin one model per call and keep transcripts separate.

- BAKED-IN FOUNDER DEFAULTS (2026-09-28/29, on disk since the w5-script-patch v3
  landing — never fight them): every request runs thinking/reasoning DISABLED +
  `stream: true` inside the script's single request builder; the default route
  is the `images` alias and lanes pass NO `--models` (routing law below); the
  default `--timeout` is 600s (accommodates the slow glm route's ~180s floor).
  These are NOT flags a lane passes, and there is nothing to "fix" when a
  transcript shows stream-shaped output; the script's only escape hatch is its
  own graceful resend when a route rejects the thinking-disable fields
  (400/422/502). The `--help` line still printing "--max-tokens default 4096"
  is stale text against the 8192 default — known, do not "fix" it by passing
  the flag.

## WAVE-5 ROUTING + STORM BUMP — 2026-09-29

### Routing law (founder, 2026-09-28 evening; v2 amendment 2026-09-29; v3
corrections 2026-09-29 late; v4 additions 2026-09-29 late — dispatch walls +
verdict law) — SUPERSEDES the historical model-pairing
verdicts below AND this bump's own v1 text wherever they conflict (v1 said
"kimi-k3 allowed" — that line is dead; v3 amends the glm and timeout lines)

- **DEFAULT IS THE ROUTE: run `analyze_image.py` with NO model params, always.**
  Founder, 2026-09-29: "use the script without any model params." The default
  is `DEFAULT_MODELS = ["images"]` (on disk), whose gateway combo includes
  `nvidia/nvidia/ising-calibration-1.5-31b`. Never add `--models` to a
  default-route invocation — the absence of the flag IS the routing decision,
  and there is no second default.
- `nvidia/z-ai/glm-5.3-flash` — the ONLY permitted second opinion, and only as
  a second-model CONSENSUS leg, and only BATCHED: ≥4 concurrent invocations
  (one per image, separate transcripts) in ONE Bash call ending `wait`, ~180s
  floor per invocation. **v3 (2026-09-29 late): this leg is effectively
  DEFERRED/BLOCKED — 8/8 `HangError` @330s all night, the backend's glm
  connection at max concurrency cap 1, and its 463–817s generations queued
  every 270s wall fleet-wide (w5-vision-hang-probe §2).** Do not spend a
  window on it; every certificate that needed it records "glm leg
  DEFERRED/BLOCKED" honestly. The batch rule stands if it ever recovers: a
  lone glm call wastes the shared gateway and is forbidden by the same law
  that allows the batch. Has <4 banked images? Then no glm leg — a single
  capture is certified single-model and the outcome must say so.
- `kimi-k3` — **BANNED entirely (re-affirmed v3, 2026-09-29 late).**
  Founder, 2026-09-29: "don't use kimi k3 at all."
  Never pin it in a lane; a banked re-run command that names it is stale and is
  re-run under the default law instead (process-notes §R).
- **gemini and claude routes are BANNED for lane pinning — founder law, not
  preference.** Evidence: a gemini-family verdict described UI that was ABSENT
  from the DOM (w5-regrade-banned charge; `ai/plans/view-audit/wave5/zerogroups-arm-outcome.md`
  "Routing note (founder amendment 2026-09-28 evening)"), and earlier
  gemini-certified certificates had to be re-graded once the wall lifted. The
  script still ACCEPTS the ids via `--models` — the ban binds LANES.
- DISPATCH — **every lane dispatch runs in the BACKGROUND** (founder law).
  Analysis invocations are background jobs inside ONE Bash call ending `wait`
  — never a foreground serial drip, and never a background call left without
  `wait` (orphaned children stall the task).
- DISPATCH WALLS (v4, 2026-09-29 late) — **≤2 concurrent invocations per lane
  per Bash call, ~15 s spacing**; PROBE FIRST with ONE short-wall call
  (`--timeout 120 --rounds 1 --tries 1` on an already-banked PNG — valid body
  opens the window, hang ⇒ `sleep 300`, re-probe ONCE); then 270 s walls
  (`--timeout 240 --rounds 1 --tries 1`) **wrapped in `timeout 300`** — a 270 s
  wrapper races the script's own 270 s guard and the abort vanishes unlogged
  (no transcript). The combo router retargeting to a saturated backend is
  gateway-side, not yours. Detail in process-notes §G.
- VERDICT LAW (v4, 2026-09-29 late) — verdicts are banked to FILES at run time
  (stdout-only verdicts are not evidence; only `[winner]`-body transcripts
  certify); banned-route verdicts are VOID; a refuted frame is RE-OPENED
  wrong-subject debt, not a cleared row; single-model default-route
  certificates are VALID but must state "glm leg DEFERRED/BLOCKED"; prefer
  PRE-REGISTERED falsifiable predictions (the DOM/source wins). Detail in
  process-notes §V/§P.
- When the script itself ERRORS mid-lane, subagents ARE authorized to patch
  `scripts/analyze_image.py` under standing delegation — no separate grant
  needed. The one fence (only a live dedicated script-patch lane outranks you)
  and the rules live in `assets/process-notes.md` §S4.

**No-thinking + streaming, always.** The script bakes thinking/reasoning OFF and
`stream: true` into its single request builder (`build_payload()`); this is a
default, not a flag. Lanes must never try to restore thinking, and must not
read stream-shaped output as a defect — the reasoning deltas are still
harvested and scanned for leaks. Landed by the w5-script-patch v3 lane
(`ai/plans/view-audit/wave5/script-patch-outcome.md` §2, Directive 1).

### Historical model pairing (round-1 verdicts — SUPERSEDED where they conflict:
gemini, claude and kimi-k3 are BANNED above, so those recommendations no longer
hold; the rest stands as reliability history — cite consensus, never a lone model)

Historical: default = richest findings but truncation-prone; gemini-class =
leanest, most stable, best on structural claims (now BANNED); claude-class =
most voluminous but hallucination-prone on microtext (now BANNED). Verdict
spreads of 4–5 points between models on the same image were observed; only
≥2-model consensus findings go in the final register. The census's pinned set
(agy/gemini-3.7–3.8) is superseded by the routing law; the census table stays
the authoritative reliability inventory (`ai/plans/view-audit/wave5/route-census-outcome.md`).

## The workflow (five stages)

1. **CAPTURE** — all agent-browser work under the RAM lock
   (`python3 scripts/agent-browser-lock.py run -- agent-browser --session <unique> <args>`)
   [2026-10-11: superseded — that lock script does not exist in this project; see the
   2026-10-11 amendment below.],
   explicit viewport numbers (zsh does not word-split unquoted variables), settle
   ≥4s after navigation, and pass `--hide-scrollbars false` whenever scrollbar
   evidence matters (headless Chromium hides native scrollbars by default —
   learned from the scrollbar-fix lane). PIL-check every PNG (dimensions + mean)
   before spending vision on it; verify story ids against `index.json`, never
   trust a guessed id (a wrong id silently renders the no-story fallback).
   [2026-09-30: when the CDP probe layer itself wedges, the fault is almost
   always your OWN browser session — close it (never `--all`) and continue under
   a FRESH session name: amendment W1 below.]
2. **ANALYZE** — per image, ONE default-route invocation with **no `--models`**
   (routing law above: "use the script without any model params"), run as a
   background job inside ONE Bash call ending with `wait` (orphaned background
   children stall tasks; background dispatch is the law). Add a second leg ONLY
   when the bank needs a ≥2-model consensus, ONLY as
   `nvidia/z-ai/glm-5.3-flash`, and ONLY batched — ≥4 concurrent invocations in
   one call so the ~180s waits are amortized (a lone glm call is forbidden). A
   single regression capture therefore sends one default-route call and is a
   SINGLE-MODEL certificate: record it exactly as that; never fake a
   consensus. Default invocation (run from this skill's root, where `scripts/`
   lives): `python3 scripts/analyze_image.py analysis <png>
   --timeout 240 --rounds 1 --tries 1 --view "<...>" --capture "<...>" -p
   "$(cat <the current audit prompt template>)" > <img>-default.txt 2>&1 &`.
   Never read PNG bytes with the Read tool — read the .txt transcripts.
3. **ADJUDICATE** — differential: CONSENSUS (≥2 models) vs UNIQUE. DOM-verify
   every unique plausible finding (locked eval; re-navigate to the RIGHT story and
   settle first — sessions persist across navigations) and classify REAL /
   HALLUCINATED / DEBATABLE with measurements (rects, scrollWidth vs clientWidth,
   font sizes, contrast ratios). The standard is "LOOKS WRONG = flag", not
   "DOM-correct = pass": a full string behind a 4.5px visible sliver is a defect.
   [2026-09-30: hash the frame BEFORE spending a call (W5) and retry a hard-wall
   `HangError` ONCE under the wider wall before banking debt (W4) — amendment below.]
4. **REGISTER** — write a severity-ranked results register (BLOCKER/MAJOR/MINOR +
   confidence) with the consensus items, the adjudicated unique items (with
   finder-model + measurements), and the top-3 problems. Cite file paths.
5. **EVOLVE** — two append-only channels, never mid-run edits of shared files:
   - The shared audit-prompt template's "Issue vocabulary" section (see assets/):
     append NEW defect classes your differential surfaced (re-read the file
     immediately before appending; prefer `echo '…' >> file` — near-atomic; dedup
     against existing entries first; near-duplicates are recorded as
     "confirms <tag>", not appended).
   - The script-proposals file: propose fixes to `scripts/analyze_image.py` with
     the evidence that motivated them. NEVER edit the shared script yourself
     mid-run; the owner applies and records them.

## The audit prompt

Use the current template at `assets/audit-prompt-template.md` — it carries the
v2 structure (layout map with named regions → first-glance test → strengths →
severity+confidence-tagged defect list across categories (a)–(o) → top 3 →
structural proposal → calibrated 12-axis verdict → uncertainties → §9 vocabulary
proposals) plus the grown Issue vocabulary. Pass it verbatim via
`-p "$(cat …)"`; the context arrives via `--view`/`--capture`. Models emit §9
proposals in their output — harvest those into the vocabulary after dedup, the
same as your own differential finds.

## Self-improvement (gated)

Agents improve this skill from run experience, but ONLY with the skill-creator
skill loaded to validate the improvement — no exceptions, and no bloat: a
proposed change must name the run and finding that motivates it, and it must
generalize (a one-off observation is a results-file note, not a skill change).
Valid improvements: new vocabulary entries (the append-only section), new
pitfalls in this SKILL.md (with the evidence that earned them), template
restructurings after a full round (frozen per round, bumped between rounds),
and script proposals. Invalid: restating existing rules louder, encoding
single-run anomalies, or growing the prompt file mid-round.

## Ports and standing rules

Storybook lives on 6055 (never restart it; port 6006 belongs to SUR — never
touch). The dev app on 5173 may be live — capture from it when the audit target
is the mounted view, not the story. No image bytes in agent context. No git
actions from inside an audit lane.

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

## AMENDMENT 2026-09-30 — gateway migration truth-up (17844 → 17844)

Appended by the wave-6 skill-amendment lane (outcome:
`ai/plans/view-audit/wave5/skill-endpoint-truthup-outcome.md`). Version
1.2.0 → 1.3.0. **Zero doctrine changes** — W1–W6 and every other doctrine
above (the routing law, §G, §V, §P, §X, §S, §R, the dispatch walls) stand
unchanged. This block only brings the gateway's operational facts to the
founder's 2026-09-30 post-migration truth:

- **The vision gateway endpoint is `http://localhost:17844` — the committed
  route (`scripts/analyze_image.py` ENDPOINT) — and the gateway API key was
  ROTATED on 2026-09-30; the founder confirmed the new route + key working
  live, and the wave-6 lane independently re-confirmed it end-to-end (ONE
  default no-params call, no overrides: `[winner] images (round 2,
  attempt 1)`, `rc=0`, on `endpoint http://localhost:17844/v1`, key file
  present).** The intro above already names the current route.
- **Every historical `:17844` reference describes the PRE-migration state
  and is SUPERSEDED for routing purposes.** Where wave-5 outcomes, banked
  verdict-file headers, or worklog history cited by this skill still say
  `:17844` — including all 15 combined re-cert verdicts, produced by the
  DEFAULT no-params route against the then-working 17844 route on
  2026-09-30 (`ai/plans/view-audit/wave5/apply-fixes-order-outcome.md`
  §2.15: 15/15 REAL verdicts, zero BLOCKED) — treat them as history, never
  as a routing instruction. 17844 is not a fallback, a second route, or a
  dial; route ONLY via the committed default.
- **The in-memory endpoint-override technique from the 2026-09-30 key
  outage (rewrite the endpoint string in memory and exec the unmodified
  source — `scratch/worklogs/w5-apply-fixes-v4.md` v4-t1) is OBSOLETE.**
  It existed to reach 17844 while the committed route 401'd the then-banked
  key; the migration + key rotation removed its reason. Never revive it —
  no endpoint overrides, in-memory or otherwise.

## AMENDMENT 2026-10-11 — transplant repairs (location + missing capture lock)

Appended by the skill-creator gate in `ai_llm_slides` after this skill was
found unloadable by agents. Version 1.3.2 → 1.4.0. Two repairs; no other
doctrine above changes.

- **Location.** The skill sat at `.agents/image-analysis/` — one level too
  shallow for the project skill loader, which scans `.agents/skills/`. It now
  lives at `.agents/skills/image-analysis/` (moved with `git mv`, history
  kept). The body's references to
  `.agents/skills/image-analysis/assets/…` are correct at this location.
- **Capture lock script.** `scripts/agent-browser-lock.py` does not exist in
  this project and is not in this skill's `scripts/` dir — the CAPTURE stage's
  lock-wrapped invocation cannot run here. [2026-10-11: superseded — capture
  with agent-browser directly under a unique `--session` name, keeping the
  rest of the CAPTURE rules: explicit viewport numbers, ≥4s settle,
  PIL-check every PNG, verify story ids against `index.json`. If the RAM-lock
  discipline is wanted here, port the lock script into this skill's
  `scripts/` dir; do not improvise one mid-lane.]

Historical note: evidence paths under `ai/plans/view-audit/wave5/…` cite the
origin project's outcome tree, which does not exist in this repo — they are
provenance for the rules above, not local records to consult.
