

## 9. worker-slide044-legs2 — 2026-10-24 ~13:08 — HONEST PARK (NOT certified)

Worker: `worker-slide044-legs2`. Took over the stale `w044` claim
(`claim 44 worker-slide044-legs2`; heartbeat refreshed through the run). No
FINAL VERDICT transcript could be obtained: the image leg was fleet-wide
wedged the entire window, exactly as the orchestrator flagged. **slide 044 is
NOT certified; visual_check stays null, gen_status stays building.** Resume
commands in §9e.

### 9a. Done this run (all gateway-free, all verified)

- Claim takeover + heartbeat verified; `get 44` confirmed
  `worker_id=worker-slide044-legs2`, `gen_status=building`.
- **Render currency**: `qa/slide044/render_2.png` (248,034 B) ==
  `scratch/tmp/044v2/slide-1.png`; it is the post-fix render. No re-render.
- **House chrome**: `house_chrome_check.py render_2.png 44` → **PASS**
  (panel x112-1882 y94-bottom; strokes L/R/bottom present, top bare; badge
  center (1824,152) d=68; tol 8). The render under judgement is chrome-clean.
- **Payload integrity**: `judgepayload_legs_A.txt` md5 `8fc1196…`; the three
  `judgepayload_legs_B_*.txt` md5 `4ec37fe…` — all three byte-identical, which
  is CORRECT (generic Template B; the region is identified by the dispatch
  `--view` + transcript name, not in the payload). Corruption scan clean:
  **no BLOC5ER / B1OCKER, no zero-padded "slide 0NN"**, each B payload carries
  the unpadded "slide 44" once. Nothing was substituted this run (payloads were
  catted straight from disk), so no K-token corruption risk.
- **BUG FIX in `legs_B_dispatch_2.sh`** (it would have silently aborted LEG B):
  1. `cd "/worksp"+"aces/…"` — the literal `+` resolved to
     `/worksp+aces/…` (does NOT exist) → `|| exit 2` would kill the whole
     script before any crop ran. Fixed to the working `"/worksp""aces/…"` form.
  2. `--timeout 600` → `--timeout 1200` (orchestrator provisional lane wall:
     1200 inside the `timeout 1700` wrapper; do not extend past it).
  3. transcript names `crop_2_${NAME}_judge.txt` → `legB_${NAME}_attempt_1.txt`
     (Procedure B transcript law).
- LEG A staged as `qa/slide044/legA_dispatch_attempt_3.sh` (reproduces the
  orchestrator's command exactly; transcript `judge_attempt_3.txt`).
- LEG A/B invocations cross-checked against `analyze_image.py` argparse
  (`comparison` = 2 images + `-p`; all flags valid). `16_vision_gate.sh` caps
  at 16 concurrent via flock (it blocks, never fabricates); the task's stricter
  `pgrep<8` precondition was honored — nothing dispatched at ≥8 procs.

### 9b. Pre-measured adjudication (fresh PIL, both images, phantom-safe ≥3px)

HARNESS `qa/slide044/adj_legs2.py`; output banked at
`qa/slide044/adjudication_legs2_output.txt`. Render_2 downscaled to frame
960x540 LANCZOS (matches the make_crops_2 effective scale). Every prior §9
adjudication is re-confirmed against the FIXED render:

| finding | original | render_2 | verdict |
|---|---|---|---|
| calc-area bg median (the fixed defect) | (254,255,253)/(255,255,255) | (255,255,255) at y150/250/420/500 | **WHITE fix PRESENT**; v1 grey gone |
| eq band ink x (b1/b4/b6) | 288..833 / 284..759 / 284..765 | 288..769 / 288..559 / 284..591 | narrower-right = ground-rule (e) 2D format; **every band non-empty, no BLOCKER** |
| "Check classes of" ink | y80..87 (ink 137) | y82..91 (ink 288) | ~3px y-shift, typed-vs-handwritten → MINOR (d) |
| class rule line x1 | x508 | x491 | ~17px shorter RHS, typed text compact, **full text present** → MINOR (d) |
| Initial-W bracket stack | x330..353 y55..101 (ink 134) | x328..353 y53..102 (ink 249) | both span all 3 enclosed stacks; ~49 vs ~50 px → MINOR (d) |
| "Iteration 3" badge | red block x86..213 y278..304 (ink 2229); white glyph present | red block x84..213 y277..304 (ink 3285); white glyph present | block + glyph present in both, same spot; typed weight → MINOR (d) |

All ≤ MINOR, all inside ground-rules (c)/(d)/(e); none is a fix trigger.
Crop→slide-space map for LEG B (frame = origin + crop_px / 2.0844):
lefttables origin (66,52) eqstack (272,136) centretext (236,52).

### 9c. Verdict transcripts — NONE obtained (honest)

- `judge_attempt_3.txt` — NOT created (LEG A never dispatched).
- `legB_{lefttables,eqstack,centretext}_attempt_1.txt` — NOT created (LEG B
  never dispatched; the prior lane also never launched B).

Gateway evidence this window (`pgrep -c -f analyze_image.py`): 35, 14, 27, 33,
37, 38, 45, 37, 44, 44 across 12:31→13:08 — never < 8; the lone 14 dip was
transient (27 three polls later). No call launched at ≥8 procs → no attempt
burned, nothing fabricated.

### 9d. Final DB state (released; clean for re-dispatch)

`gen_status=building`, `visual_check=null`, `visual_attempts=0`,
`visual_transcript=null`, `worker_id=""`. **No PASS, no `gen_status=passed`** —
those need real FINAL VERDICT transcripts. `last_error` updated with the resume
pointer; claim released (a released row is also available to `claim` auto-take-
over).

Build-lane debt (unchanged, carried forward): DB `build_script` still points at
pre-fix `build/slide_044.js` and the plain-named deliverable
`recreated_pptx/slide_044_recreated.pptx` is still v1 (grey). The fix lives in
`build/slide_044_v2.js` → `recreated_pptx/slide_044_recreated_v2.pptx` →
`render_2.png`. This legs worker does not rebuild; after the legs pass on
render_2 the build lane should promote v2 to the plain-named deliverable and
repoint `build_script` to v2 (044 has no dependents → leaf cleanup, not gated).

### 9e. Exact resume commands (copy-paste ready)

```bash
cd "/worksp""aces/codespaces-blank/ai_llm_slides"
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
python3 scripts/15_progress.py claim 44 worker-slide044-legs3   # fresh worker id
python3 scripts/15_progress.py heartbeat 44 worker-slide044-legs3
pgrep -c -f analyze_image.py        # LAUNCH ONLY when it prints < 8; else heartbeat + sleep 240 + re-probe
# LEG A (full-slide) — staged, run once gateway is clear:
bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044/legA_dispatch_attempt_3.sh
# LEG B (crop pairs) — fixed dispatch, run after LEG A:
bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044/legs_B_dispatch_2.sh
# then PIL-adjudicate any FAIL/MINOR with qa/slide044/adj_legs2.py (§9b already refutes the known ones), and certify:
python3 scripts/15_progress.py set 44 visual_check PASS
python3 scripts/15_progress.py set 44 visual_transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044/judge_attempt_3.txt
python3 scripts/15_progress.py set 44 visual_attempts 3
python3 scripts/15_progress.py set 44 gen_status passed
python3 scripts/15_progress.py release 44 worker-slide044-legs3
python3 scripts/15_progress.py get 44   # verify gen_status=passed, visual_check=PASS, worker_id=""
```

The instant `pgrep -c -f analyze_image.py` prints < 8, LEG A then LEG B run
back-to-back; every other step is staged and verified.
