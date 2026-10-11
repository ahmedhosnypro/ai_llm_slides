# AGENTS.md — Deep Learning DSAI 308 playlist (all lectures under videos/deep-learning/)

## Founder directive 2026-10-11 — ONE house chrome for the ENTIRE playlist

**Every recreated slide in every lecture under `videos/deep-learning/` MUST use the
same outer frame size and position, and the same slide-number (badge) position and
size — exactly as measured from the reference frame
`001_transformers_part1/unique_slides/slide_001.jpg`** (960×540, 1px = 1pt):

- White canvas `FFFFFF`; gray panel `E9E9E7` spanning x 42..918 px, y 45 px → slide
  bottom (its red bottom stroke at rows 538–539 renders half-visible at the slide
  edge); thin red `C00000` border on the panel's left/right/top.
- Badge: circle d≈36 px centered at (893, 71) px — fill `FDFD96`, purple ring
  `6A5ACD` (~2 pt), bold numeral `333333` (Arial 18 pt). The numeral is the number
  printed on the ORIGINAL slide image (no zero-padding).

This rule is playlist-wide: it binds lecture 001 and every future lecture namespace
under `videos/deep-learning/`, and it OVERRIDES the ml-intro house values quoted in
the root AGENTS.md / `scripts/17_worker_instructions.md` for work in this playlist
(the ml-intro template is a different course's chrome). Per-slide content, layout,
colors, and text remain governed by each slide's own frame (the fidelity law — the
original frame is ground truth for everything INSIDE the chrome).

## Shared patterns (use them, don't re-derive)

`shared_patterns/` holds the playlist-level reusable building blocks:

- `house_chrome.js` — runnable pptxgenjs module: `drawHouseChrome(pptx, slide,
  {numeral})` + the `CHROME` constants. Import it in every build
  (`require('<abs path>/shared_patterns/house_chrome.js')`) instead of re-drawing the
  frame/badge. Per-video component modules (e.g.
  `001_transformers_part1/recreated_pptx/build/components/house_chrome.js`) must
  delegate to or exactly match this one.
- `house_chrome_check.py` — closed-loop PIL checker: run it on every 150dpi render
  (`python3 shared_patterns/house_chrome_check.py <render.png>`) as part of the
  mandatory pre-judge self-check. FAIL = fix the build before judging.

Adding a new playlist-level pattern: runnable example + index.json entry + the law in
comments (same discipline as the project-level `patterns/` library).

## Cross-video slide dependencies (founder directive 2026-10-11)

Lectures in this playlist share content: a lecture may open with a recap of the
previous one, or re-use its figures/compositions. Slides may therefore depend on
slides in ANOTHER lecture's namespace. A cross-video dependency is a CONTENT
dependency (the child re-uses the parent's certified composition) — it is NOT a
reusable pattern-library entry.

- **Qualified refs**: `deep-learning/<video-dir>:<slide_id>` (e.g.
  `deep-learning/001_transformers_part1:15`), stored in the CHILD video's
  `slide_dependencies.json` and `depends_on` CSV. Bare ints = same video. First
  binding use: `002_transformers_part2/slide_dependencies.json` (v2).
- **Cross-video gate**: a child may BUILD only when the cross-video parent is
  CERTIFIED **in the parent's own DB** (`gen_status='passed'` AND
  `visual_check='PASS'` there). `scripts/15_progress.py deps|buildable` resolves
  cross-video parents by reading the parent video's `slides_progress.db`
  (SELECT-only — never write outside your video's namespace).
- **Component import across namespaces**: the child build `require`s the parent
  video's certified component (`<parent>/recreated_pptx/build/components/slide_NNN.js`)
  by absolute path and draws only its measured delta. Identical recap slides are
  typically `parent.renderBase(...)` + own badge numeral (the numeral = the number
  printed on the CHILD's original frame, per the badge law) + whatever tiny delta
  the child's frame shows. Never copy-paste a composition across namespaces.
- **Playlist-scoped banking obligation**: a slide MUST bank a component at
  certification if ANY slide in ANY video's graph references it — even when it has
  no same-video dependents (precedent: 001's slides 15, 19, 33 carry the obligation
  solely because 002 depends on them).
- **Pattern groups** (`slide_dependencies.json` v2 `"pattern_groups"`): members
  share reusable patterns (NOT identical content). They build STRICTLY
  sequentially in listed order — member k starts only after member k−1 is
  certified (verify the pattern, then reuse it). This gates builds only; analysis
  (12) and validation (13) are never gated, by deps or by patterns.
- **Placeholder cover law**: when a lecture's cover frame is missing from the
  video, slide 001 is rebuilt as a placeholder mirroring 001's certified cover
  (shared chrome, badge numeral 1, course title). There is no ground-truth frame,
  so it is certified by FOUNDER SIGN-OFF + `house_chrome_check.py` — never by a
  visual-judge comparison. Its DB row is marked `analysis_status='n/a-placeholder'`,
  `validation_status='ready'`, and its index entry carries `"placeholder": true`.
- **Curation metadata law**: after the founder curates a frame set, the machine
  reconstructs the metadata (002 is the precedent): `unique_slides/new2old_mapping.json`
  + rewritten `slides_index.json` + the old index preserved as
  `slides_index_old###.json` + the pre-curation DB backed up. Founder group splits
  (one extraction group → two slides) and frame swaps are recorded, never
  second-guessed.

## Per-video rules still apply

Each lecture namespace may carry its own `AGENTS.md` (see the root AGENTS.md
multi-video section). Those rules govern everything except this chrome law, which
they cannot relax. Lecture 001's directives (web-verified analysis, dependency-gated
component builds) are the working precedent; lecture 002 adds the cross-video and
pattern-group laws' first binding use.
