# CONTINUATION PROMPT — deck 03 certification program (run 299640, parked 2026-10-26)

Read this file top to bottom at the start of the next session, on any device. It is the
complete restart state for finishing
`videos/machine-learning/03_ridger_regression_gradient_descent` (Ridge Regression &
Gradient Descent, 51 founder-curated slides). Everything below is measured ground truth
or pool-DB fact — re-verify nothing already marked DONE unless a check fails.

## 0. Mission + governing law

- Goal: all 51 slides judge-certified (`gen_status='passed'` AND `visual_check='PASS'`
  in `slides_progress.db`), each as single-version `slide_NNN_recreated.pptx`, then
  closeout (S9: OMML pass, final-deck merge gate, CLOSEOUT_REPORT).
- **State at park: 43/51 certified. Open set: 14, 15, 19, 25, 34, 43, 44, 48.**
- Read FIRST: this namespace's `AGENTS.md` (house chrome, zoomed-visual-judge
  mandate, dependency graph 10>9, 13>12, 17>13, 18>17, web-research mandate).
- Skills to activate: `slide-recreation` + `visual-judge` + `image-analysis`
  (always via `scripts/16_vision_gate.sh`) + `pooled-missions` + `skill-creator`
  (for any skill edits).
- Judge payloads are frozen from `recreated_pptx/shared_patterns/judge_protocol_03.md`
  — source `-p` payloads byte-for-byte, never hand-edit.

## 1. Hard rules (non-negotiable, from AGENTS.md + pooled-missions)

- Zoomed visual judging EVERY slide: full comparison judge + crop-pair certificates
  (one per dense region), both clean (or PIL-adjudicated) before `visual_check='PASS'`.
- Vision calls ONLY through `scripts/16_vision_gate.sh`, one leg per Bash call, with
  `pgrep -c -f analyze_image.py` < 8 before dispatching. Standard leg shape:
  `timeout 1700 bash scripts/16_vision_gate.sh python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison <render> <orig> --view "<...>" --capture "IMG1=<...>render; IMG2=<...>original upscaled to match effective scale; region: <...>" --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 --transcript <qa path> -p "$(cat <payload>)"`
  (crops use INNER `--timeout 600`).
- Never commit unless the user asks; park-never-delete (banked evidence, *.bak);
  `export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp`; venv python is
  `/home/ahmed/Projects/ai_llm_slides/venv/bin/python3`; renders are 2001×1125
  (S=2001/960); DB PK is `slide_id`; verbatim text incl. source typos ("Ugmented").
- One worker per slide end-to-end; pool members are background subagents only; every
  claim/completion transitions through the pool DB; resume via `Agent(resume=agent-id)`;
  drifted workers are stopped + redispatched fresh, never re-resumed.
- Subagents that "announce-then-end" (narrate next action, then end turn without doing
  it) are the failure mode that cost the fleet days: give every resumed worker a strict
  "reach a terminal scope state in THIS turn" directive, and if it announce-ends again,
  do the scope in-loop yourself.

## 2. Where the state lives

| Artifact | Path |
|---|---|
| Progress DB (source of truth per slide) | `videos/machine-learning/03_ridger_regression_gradient_descent/slides_progress.db` |
| Final-deck ledger | `recreated_pptx/final_deck_state.json` (certified pages) |
| Final combined deck (continuous, 51 pages) | `recreated_pptx/03_ridger_regression_gradient_descent_final.pptx` + `.md5` |
| Final-deck tooling | `recreated_pptx/build/final_deck/{final_deck_tool.py,render_check_pages.py,poll_and_update.sh}` |
| Pool DB (session scratch, may NOT exist on a new device) | `~/.agents/scratch/ai_llm_slides-pool-299640/mission.db` (helper `~/.agents/skills/pooled-missions/scripts/pool-db.sh`) |
| Mission protocol (worker briefs) | `~/.agents/scratch/ai_llm_slides-pool-299640/MISSION_PROTOCOL.md` |
| 048 evidence dir | `recreated_pptx/qa/slide048/` |
| Paren-sweep evidence | `recreated_pptx/qa/paren_sweep_20261026/` + per-slide `paren_sweep.md` |

If the pool DB does not exist on the new device: rebuild scopes from §4 (names, items,
statuses below) into a fresh run dir, or proceed in-loop — `slides_progress.db` is the
real certification ledger and is committed to git.

## 3. DONE since the last report (do not redo)

- **Slide 051 certified (att5)**: 4 legs PASS; DB updated; transcript
  `qa/slide051/judge_attempt_5.txt`; md5 `e43765e0fb7bddd03a83a0e78d1861cb`; OMML
  skipped (049/050 certified unwrapped); final-deck page 51 updated
  (deck md5 `8444dc1e4c6368d99f7402873c9ee435`, `render_check_pages.py 51` PASS 0px).
  W-underline claim on 051's aug-W DISMISSED (baseline-merged underline doctrine:
  underlines render ON the baseline row, n≥body+3; check AT the baseline).
- **S23 paren-curve sweep DONE, scope `S23_paren_sweep_certified` = done**: 41/41
  certified slides direction-CLEAN, 0 rebuilds, 0 recerts. 6 vision legs (4 PASS,
  003 FAIL→all findings PIL-REFUTED→no rebuild, 021 FAIL→zero delimiter findings,
  sole MAJOR = missing X-matrix underbars → **open task 129, out-of-class**).
  Task 88 (003) = refuted, no action, may be closed.
- **Paren-curve doctrine GROUNDED in both skill copies (user request, DONE)**:
  `~/Projects/ahmed-skills/skills/slide-recreation` (committed: "straight-bar
  delimiter law for matrix/vector parens (v1.6.0)", "scope curved-delimiter guidance
  to genuinely-curved originals") and `~/.agents/skills/slide-recreation` (same text).
  SKILL.md read-map line 62: "delimiter laws (direction; straight bars for
  matrix/vector parens)"; building.md: "Curved delimiters = single quadratic-Bézier
  centerline → 600dpi transparent PNG … matrix/vector paren pairs are STRAIGHT BARS
  (equations.md)". Defect class: mirrored/wrong-direction paren curve (seen on 017);
  builds draw straight 1px delimiter bars at measured positions, no curved parens.
- **Continuous final-deck requirement operating**: 51-page placeholder deck exists;
  every certification must be followed by
  `cd recreated_pptx/build/final_deck && <venv python> final_deck_tool.py update <N>`
  then `<venv python> render_check_pages.py <N>` (PASS = 0px mismatch; retry once on
  concurrent-overwrite). The S21b cron (every ~17 min delta check) was DELETED at
  park — recreate it on the new device or run `bash recreated_pptx/build/final_deck/poll_and_update.sh`
  from `recreated_pptx/` after each cert.
- **048 measurements COMPLETE** (see §5) — the build script is the only missing piece.

## 4. Open scopes — exact briefs (pool DB rows to recreate)

| Scope | Slides | DB state at park | Brief |
|---|---|---|---|
| `S24_048_rebuild` | 48 | in_work; takeover in-loop; **build NOT yet written** | §5 is the complete spec. Write build → att9 legs → certify → deck update. |
| `S25_043_044` | 43, 44 | 43 judging att0; 44 building att0; worker timed out ×2 | 043: small fix (restore −14, sliver clip, founder deltas "Ugmented Vectors ( from Top )" + B4 [8,−12,−8]), then judge. 044: rebuild then certify cycle. |
| `S26_014_015` | 14, 15 | 14 att7 FAIL PARKED (adjudicated: #1 collision …); 15 att6 PARKED (judge cap) | 014: adjudicate att7 findings PIL-first, fix real ones, att8. 015: legA judge on unchanged bytes (attempt-4 legA on unchanged build was the plan). |
| `S27_019_025` | 19, 25 | 19 att0 PARKED (4 consecutive gate failures); 25 att4 PARKED | 019: PIL-confirm two MAJORs (task rows 51/52: "NO REG g2 third entry 0.61→0.64", "RIDGE 10 g3 third entry 1.07 vs 1.1") then rebuild+judge. 025: att14 legs FULLY STAGED — `qa/slide_025/dispatch_A14_1200.sh` / `dispatch_B14_1200.sh` exist, NEVER restage, just run them. |
| `S28_034_build` | 34 | building att2; worker stopped mid "attempt-27 build" | Build exists (Oct 25 02:44), `render_26` exists, payloads `A_27/B_27` staged 17:04. Write the attempt-27 build (worker banked "current build bytes correct" pre-att2), render, legs, adjudicate, certify. |
| `S9_closeout_omml_merge_report` | — | pending | **DO NOT START until 51/51.** OMML pass, final-deck merge gate, CLOSEOUT_REPORT. |

Also open (informational, from earlier waves): payload-integrity task rows 6–15,
prephase rows 20–52, task 129 (021 X-matrix underbars — real out-of-class MAJOR:
`build/assets/eq_021_invexpr.json` mathtext "X^T X" lacks `\underline`; fix asset →
rebuild → recert 021 in the next quiet wave).

## 5. SLIDE 048 — complete build spec (all measured; write `build/slide_048.js` FRESH, never sed-clone)

Evidence: `qa/slide048/att9_meas_out.txt`, `att9_meas2..6_out.txt`,
`measure_rows456_out.txt`, `measure_rows456b_out.txt` (+ the .py scripts),
`row1_zoom_inspect.txt`, `HANDOFF.md` (att8 dispositions — REFUTED, do not re-fix:
Initial-W order, cream fill, mathzone/tableeq/chart/redstop, REPEAT-bold).
Frame 960×540, 1px=1pt; helpers as in `build/slide_049.js` (fx/fy/fw/fh = px/72,
`dbar(x,y,h,color)` 1px rect, `txt` 16×16-box centred default, `row` per-cell texts,
`addEq(name,xIn,baselineIn)` with sidecar JSON). require `house_chrome.js`, numeral 48.
Colors: BLACK 000000, RED FF0000, CRED C00000, BOXRED C6020A, INK 211776, NAVY 1F1655,
ATITLE 2B207C, GRAY ABAFBA, DGRAY 909090, IGRAY 6E6E6E, DGREEN 008000, GREEN 5B9C4E.

1. **Top-band box**: rect x69 y55 w(719−69) h(129−55), WHITE fill, INK border 1pt.
2. **Top table** (mirror 049 certified verbatim — 048's table zone is pixel-identical
   to 049's; the old build's third data row (1,2,2,4,5,6) was spec-invented, the frame
   has TWO): header x₁..x₆ centres [96.2,118.6,141.0,163.4,185.8,208.2] cellW 22.4,
   y64 h10 bold; digits (1,2,1,5,6,6) y78 h10.5; digits (1,1,2,4,5,6) y97 h10 — NO
   third row; class C₁C₁C₁C₂C₂C₂ y113 h12 bold+italic RED(first3)/INK;
   bars topL=[89.81,111.95,133.86,156.28,179.34,202.25] topR=[101.37,123.59,146.15,
   169.01,191.46,213.61] y77 h31 DGRAY.
3. **Initial-W** (049 verbatim; NO "=" — initialw zone x325..535 y55..105 is
   pixel-identical to 049's certified): dbar 330.28 / 351.72, y57 h49 IGRAY; digits
   "4"/"−2"/"−2" centred (341.5,66.5)/(344.5,82.5)/(344.5,97.5) fs13 BLACK; label runs
   [{text:"Initial", underline},{text:" W"}] x365 y61 w60 h13 fs13 italic left;
   REPEAT "REPEAT using Step η = 1" x426 y60 w150 h16 fs12 RED bold (no italic/underline).
4. **"Check classes of"**: x542 y85 w88 h14 fs10 left (048-measured cols 542..626).
5. **Z-grid** (049 verbatim): centres [648,670.5,693.5] cellW 22.4; Z₁Z₂Z₃ y71 h13
   italic fs12; 0/7/3 y86 h14 fs12; 0/6/2 y106 h12 fs12; bars
   zp=[[640.96,654.65],[664.10,676.56],[686.30,699.07]] y86 h33 DGRAY.
6. **Legend** (049 verbatim, NO commas): runs C₁(RED bold)/" positive "/C₂(NAVY bold)/
   " negative "/Zero(GREEN bold)/" is unaccepted", x239 y108 w300 h17 fs13.5 left.
7. **Aug box**: frame rect x69.5 y139.5 w176 h116 WHITE fill GRAY 0.75; title
   "Ugmented Vectors (from Top)" x82 y146 w160 h15 **fs9.5 italic color 2B207C**
   (048-measured — fixes att8 #4 wrap-collision; NOT 049's fs12 VIOLET); internals
   049 verbatim: centres [100,122,144.5,167,189.5,212]; header x₁..x₆ y166 h10 italic;
   vals [[1,1,1],[1,2,1],[1,1,2],[1,5,4],[1,6,5],[1,6,6]] bands y183/198/213 h10;
   bars augL=[93.59,115.28,137.43,160.65,182.66,205.64] augR=[105.84,127.15,149.74,
   172.35,195.05,217.20] y180 h46 DGRAY; class C₁/C₂ y230 h14 fs11 bold+italic RED/INK.
8. **Iteration-1 box**: KEEP old build's — rect x83 y276 w132 h31 fill+border C6020A,
   "Iteration 1" WHITE bold fs13 centred (measured fill x84..214 y277..305).
9. **Calc panel — CORRECTED by gap census (gaps y197..206 etc. are PANEL-GRAY
   mean≈230, min 225, NOT white; old adjacent-rect partition is wrong)**: six
   SEPARATE white rects (fill WHITE, line none) x274 w(853−274) at bands
   [[140,197],[206,263],[272,330],[338,395],[404,461],[470,528]]; horizontal GRAY 1pt
   rules at [140,197,206,263,272,330,338,395,404,461,470,528] spanning x274..853;
   left vertical GRAY per band (segments y140..197, 206..263, 272..330, 338..395,
   404..461, 470..528 — measured WITH gaps); **NO right vertical** (census x854+ = 0).
10. **Calc rows** (i=0..5 over the bands above): left side KEEP old build's
    `addEq("eq_r1_l".."eq_r6_l", fx(301), fy((t+b)/2) + 5/72)` (box-centred baseline);
    ⇒ box x488 y=t w12 h=b−t fs15 C00000 bold centred; action x509 y=t w80 fs13 left
    ("Update Weight" row 1, "Keep same Weight" rows 2–6). Rows 2–6 LEFT ≈ 049's
    pixel-wise (diff max|d|≤42, npx>60=0) — keeping the eq assets is certified-safe.
11. **Row-1 RIGHT side — decoded update equation** (census ground truth):
    - "W =" text box x615 y162 w26 h16 fs12, runs [{text:"W", bold+underline},{text:" ="}].
    - dbar DGRAY: x643 y150 h45; x665.5 y150 h45; x707.5 y152 h41; x720.5 y152 h41.
    - vec1 digits fs12 BLACK centred: "4"(656,156), "−2"(654.5,172), "−2"(654.5,188);
      semicolon ";" (661,172).
    - red C00000: "+" (677,170) fs12; "1" (688,170) fs12. BLACK "*" (699,168) fs12.
    - vec2 digits fs12 BLACK: "1"(714.5,156), "1"(714.5,172), "1"(714.5,188);
      semicolon ";" (715.5,172); "=" BLACK fs12 (731.5,169.5).
    - vec3 GREEN=DGREEN: dbar x740 y154 h38; dbar x763 y154 h38; digits fs12 DGREEN
      "5"(752,156), "−1"(753,172), "−1"(753,188).
    - "⇐" C00000 fs15 bold, box x784 y160 w17 h16 (centre 792,168).
    - Do NOT draw a dashed line at x713-715 — that vertical is the three stacked 1s.
12. **Rows 2–6 RIGHT side — W column, per-row measured table** (values = 048's own
    pixels; rows 3–6 right side is pixel-identical to 049's, row 2 within 6px):

    ```
    r: Wbox(x,y)   bars L/R (span)      "5"@  "−1"@  digit-cy
    2: 695,229     723 / 744.5 (216..260)  733.5  734    222 / 238.5 / 253.5
    3: 695,292     722.5 / 744.5 (280..322) 734.5  734    285 / 301.5 / 316.5
    4: 708,361     735 / 757   (348..392)  746.5  746    354.5 / 370.5 / 386
    5: 708,424     734 / 756   (410..455)  744.5  744.5  417.5 / 433 / 448.5
    6: 708,490     734 / 756   (476..522)  744.5  744.5  483.5 / 500 / 515
    ```
    "W =" box w26 h16 fs12 runs [{W bold+underline},{" ="}] left-aligned; bars DGRAY
    full measured span; digits fs12 BLACK centred 16×16: "5", "−1", "−1" (same values
    every row — pixel-identity with 049).

**048 verification sequence after the build:**
1. `node <build>/slide_048.js` from the PROJECT ROOT (OUT path is repo-relative) →
   overwrites `slide_048_recreated.pptx`.
2. `export TMPDIR=$PWD/scratch/tmp && soffice --headless --convert-to pdf
   <pptx> --outdir qa/slide048/ && pdftoppm -png -r 150 -singlefile
   qa/slide048/slide_048_recreated.pdf qa/slide048/render_11`.
3. `venv/bin/python3 recreated_pptx/shared_patterns/house_chrome_check.py
   recreated_pptx/qa/slide048/render_11.png 48` (FAIL = fix first).
4. `venv/bin/python3 recreated_pptx/qa/slide048/cut_crops_048_v10.py 11`.
5. att9 legs, ONE per Bash call: full Template A (payload
   `qa/slide048/judge_prompt_1.txt` — all three judge_prompt files are byte-identical,
   md5 8fc11962; crops top_band/aug_iter/calc_panel use the same payload with region
   `--capture`; INNER walls 1200 full / 600 crops; runner shape
   `qa/slide049/run_legs_049_a14.sh`).
6. Adjudicate PIL-first (the REFUTED list above stays refuted); fix + increment only
   real defects; then certify:
   `sqlite3 slides_progress.db "UPDATE slides SET gen_status='passed', visual_check='PASS', visual_attempts=9, visual_transcript='recreated_pptx/qa/slide048/judge_attempt_9.txt' WHERE slide_id=48;"`
   → `cd recreated_pptx/build/final_deck && <venv python> final_deck_tool.py update 48
   && <venv python> render_check_pages.py 48` (PASS = 0px; retry once on concurrent
   overwrite) → pool events + `scope-done S24_048_rebuild`.

## 6. Fleet lessons (earned this run — apply immediately)

1. Announce-then-end is the dominant worker failure: enforce one-turn-to-terminal
   directives; take over in-loop after one failed resume.
2. Never re-execute an old build to "test" it (`node -e require(...)` re-ran the old
   048 build and rewrote the pptx — harmless here, but never repeat).
3. W-underline doctrine: this deck's text underlines render baseline-MERGED (wide
   bottom row, n≥body+3); check AT the baseline row (049 build line 344 idiom:
   `{ text:"W", options:{ bold:true, underline:true } }`).
4. Straight delimiter bars everywhere (doctrine §3): `dbar` 1px rects at measured
   x/spans; never text-glyph parens for matrix/vector delimiters.
5. Read the sidecar baselines (`addEq`) — eq PNG placement is baseline-anchored.

## 7. Recommended next-session order

1. In-loop: write + verify + certify 048 (§5) — everything is staged.
2. Dispatch fresh background workers (one per scope, NOT resumes of dead agents):
   S25 (043→044), S26 (014→015), S27 (019→025), S28 (034) with the briefs in §4 and
   one-turn-to-terminal directives; MISSION_PROTOCOL.md pattern (pool DB optional if
   missing — slides_progress.db governs).
3. Recreate the S21b cron (or run poll_and_update.sh after each cert).
4. Quiet wave: task 129 (021 X-underbars fix + recert).
5. At 51/51: S9 closeout (OMML pass, merge gate, CLOSEOUT_REPORT).
