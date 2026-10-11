# Worker report — slide 009 (deep-learning/001_transformers_part1)

**Deliverable:** `videos/deep-learning/001_transformers_part1/recreated_pptx/slide_009_recreated.pptx`
(single-version law) — built by `recreated_pptx/build/slide_009.js`.
**Final verdict: PASS** (visual judge, attempt 7, transcript
`qa/slide009/judge_attempt_7.txt`). DB: `gen_status=passed`, `visual_check=PASS`.

## Dependency-gated child build (edge 9 ← 6)

Parent 6 certified (passed + PASS) — gate open (`15_progress.py deps`: unblocked).
Base composition imported from the certified `build/components/slide_006.js` — never
re-derived. Slide 9 is a REMOVE/REPLACE child; nothing depends on 9, so no component
export was required.

**Measured delta** (11 PIL passes, `scratch/slide009/measure*.py`):
- The ENTIRE decoder+encoder diagram (all `dec_*`/`enc_*` blocks + `ctx_arc`) is
  rigid-shifted **(+9, +2) frame px** — 27/27 per-block template matches at (9,2).
  Implemented by rendering the parent's block functions through a coordinate-shifting
  slide PROXY (`shiftedSlide`) — the certified drawing code itself does the drawing;
  no geometry copied or re-derived.
- `title`, `dec_caption`, `enc_caption`: UNSHIFTED (template match (0,0), ssd 2.0–4.8;
  title L1 differs only by ≤8px video jitter of the identical string — slide-007 precedent).
- REMOVED: `callout` (pink Context-Vector label) + `leader` — verified absent in the frame.
- **NO blue connector curve to the encoder dot** — the spec's connector (1) is a vision
  hallucination; whole-slide bluish scans find none. NOT drawn.
- A DIFFERENT thin blue leader curve DOES exist (missed by the first mask by 1 tolerance
  point, caught at 2× crop): callout right edge (~391,150) → down just right of the callout
  → diagonal behind the decoder → re-emerges below it (656,295) → meets the backprop
  panel's top border at (~703,314). Drawn as a 600dpi PNG (`assets/bluecurve009.png`)
  BETWEEN the caption pass and the decoder pass so the decoder hides its middle —
  the frame's z-order.
- ADDED: blue subtitle "(Challenges)" — **#00007B per frame; the spec's "red" is wrong**
  (ink modes (0,0,117..129)); blue callout "[3] Very Long Sequence / Vanishing Gradient"
  (box x108..391 y130..188, fill #CCE4F7, both lines underlined, L1 18pt / L2 15pt,
  lineSpacing 17 — ink widths match the frame within 4px); gray summary box
  (x61..440 y201..292, #D9D9D9, 3 color-coded lines 17.5pt bold, lineSpacing 25 — the
  frame's wider colon→RNN gap on line 1 = two extra spaces, reproduced); full
  Back-Propagation panel (below).

## Back-Propagation panel — frame-verified structure (resolves the spec's [?] flags)

- **11 nabla squares, NOT ~12** (`[?]` resolved): cream #F9E8D6, thin dusty-red border,
  y373..394, aligned 1:1 with the 11 green boxes; ∇ glyphs (hollow triangles) grow
  left→right (w4→w14, measured 6/8/9/9/10/11/12/13 for squares 4–11).
- **10 small red left-arrows BETWEEN the squares** (y≈385) — found by 2× crop vision.
- **Pink row: 11 light-pink rects (#FAEBFC, mauve hairline) AT the green-box centers**
  (NOT 10 between, and NOT joined by a continuous line) + **10 small red left-arrows
  BETWEEN them** (y≈415.5) — the spec's "11 rects + thin dark line" was wrong on both
  arrangement and connector; resolved from pixels + crop vision.
- 11 green x₀–x₁₀ boxes (y463..483, #ECFFF0, #7AA87A) with dark-green (#106C3B) bold
  labels (true subscripts) and 11 green up-arrows (y419..462, heads at top).
- Panel rect x502..918 y314..498: fill **#EAE6DD (warm gray — spec's "white" is wrong)**,
  thin blue-gray border #A6ABC0 (top border core (151,155,180), sides (192,193,195)).
- Red over-brace: main line y332..334 (x540..882) with a ~26px GAP under the center, a
  pointed ARCH over the gap (apex ~y320.5), curled ends — 600dpi PNG
  (`assets/brace009.png`, matplotlib, same mechanism as the parent's curves).
- "Back Propagation" 15.5pt bold italic #CC0000 (ink x640..771 y338..352).
- Long LEFT-pointing red arrow: shaft y357.5 (lw 3.5), wedge head (tip x520), filled dot
  d15 at (888..903) — all #CC0000 (dot solid-read (194..205, 0, 0..15) anchors the red).

## Attempts

- Renders 1–4: pre-judge build/self-check iterations (closed-loop PIL + crop vision);
  NO judge dispatches, no vision evidence consumed as verdicts.
  - render_1: first build; self-checks → summary lineSpacing 26→25, green borders lighter,
    arrow shaft 3→3.5.
  - render_3 crop check (panel) → found: missing inter-box red arrows, brace needs center
    arch (not smooth bump), pink-row arrangement wrong, and the blue leader curve.
  - render_4: all of the above added; crop re-check → structure fully matches; pointed
    brace peak tweak.
- render_5 = judged build (banked `build_attempt_5.js`).
- **Judge attempt 5** (`judge_attempt_5.txt`): coherent comparison; text inventory identical,
  all components matched, flaws called "minor geometric" — but the mandated
  `FINAL VERDICT:` line missing → per the degenerate/retry clause, re-invoked.
- **Judge attempt 6** (`judge_attempt_6.txt`): same — coherent positive body, no verdict
  line (upstream systematically drops the closing token at `--thinking high`) → retry.
- **Judge attempt 7** (`judge_attempt_7.txt`): **FINAL VERDICT: PASS** — verbatim text
  match incl. double spaces, delta correctly realized, only cosmetic deviations
  (connector routing; faint curve segment below the decoder — present in the original too).
  The closing-line nudge lived in the worker-editable `--view` field; the frozen `-p`
  template was byte-identical across attempts 5–7.

## Mandatory pre-judge self-checks (banked, `qa/slide009/selfcheck_attempt_5*.txt`)

1. `house_chrome_check.py` on render_5: **PASS** (panel x89–1913, badge center (1860,148)).
2. Landmark template match (18 landmarks, render downscaled to frame space): all OK
   (≤2px). title L1 dx=−8 / subtitle dx=−3 = video jitter of identical strings at the
   certified parent position (inheritance variance, documented).
3. Containment: content ink inside the gray panel; only the chrome's own 1px border ring
   outside (2744 px along x41/x919/y44/y539 — chrome antialiasing, chrome check PASS).
4. Ink presence: all delta regions non-empty (callout 3176px, summary 4143, panel text
   1076, arrow+dot 2331, nabla row 1694, pink row 571, green row 1350, brace 1260).
5. Zoomed crop vision (2× crops through the gate): backprop panel v1
   (`crop_panel_check.txt`) → structural fixes; v4 (`crop_panel_check_v4.txt`) →
   structure fully matches, remaining differences are weight/blur perceptions.
6. Delta-owned judge finding re-verified by PIL: "brace bump crosses the panel border" —
   DISPROVEN (render apex ink top frame-y 318.9 vs border ending 314.2 → 4.7px clearance;
   frame: 6px). Inherited-region findings (decoder right-edge proximity, olive curves vs
   s-labels, o-arrow segments) are identical to the certified parent's geometry —
   judge variance per the inheritance law.

## Evidence index (`qa/slide009/`)

- `render_1..7.png`, `build_attempt_1..7.js` (attempt provenance; renders 6–7 = re-judged
  copies of render_5, build unchanged)
- `judge_prompt_5/6/7.txt` (banked prompts, `-p` verbatim)
- `judge_attempt_5/6/7.txt`, `probe_5.txt` (vision transcripts; default route "images",
  single-read; judge subagent spawn unavailable — self-executed per 17 §7 fallback)
- `crop_panel_check.txt`, `crop_panel_check_v4.txt`, `crop_render_*.png`,
  `crop_frame_*.png` (dense-region crop comparisons)
- `selfcheck_attempt_1.py`, `selfcheck_attempt_5.py`, `*_out.txt`

## Spec corrections found (frame wins; recorded for the orchestrator)

1. Subtitle "(Challenges)" is BLUE #00007B (spec said red).
2. Backprop panel fill is warm gray #EAE6DD (spec said white); border is thin blue-gray
   (spec said red 1.5pt).
3. Nabla-square count = 11 (spec's "~12 [?]" resolved); pink rects sit at the green-box
   centers with red left-arrows between (spec's "joined by a thin horizontal line" wrong);
   no continuous chain line.
4. The spec's blue connector "callout → encoder red dot" does not exist; the real blue
   leader runs callout → behind decoder → backprop panel top.
5. Summary line 1 gap after the colon is ~2 spaces wider than lines 2–3 (reproduced).
