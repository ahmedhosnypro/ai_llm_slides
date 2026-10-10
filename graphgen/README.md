# graphgen — advanced-graph generation subproject

Purpose: produce **properly generated graph images** for recreated slides whose originals
contain advanced graphs (3-D scatters, PCA projections, learned-model plots) that the
native pptxgenjs chart/shape engine can only approximate. Founded by the founder directive
2026-10-09 ("Advanced-graph generation rule", see `/home/ahmed/Projects/ai_llm_slides/AGENTS.md`).

## The two-version rule

Every graph slide keeps TWO pptx builds, both banked forever:

| Version | File | Contents |
|---|---|---|
| Native (certified) | `videos/<VIDEO>/recreated_pptx/slide_NNN_recreated.pptx` | native pptxgenjs shapes/charts approximation — **never overwritten, never rebuilt** |
| Graphed | `videos/<VIDEO>/recreated_pptx/slide_NNN_recreated_graphed.pptx` | identical slide (house frame, badge, title, all text unchanged) with the generated graph PNG embedded via `addImage` |

Build scripts: `build/slide_NNN.js` (native, frozen) and `build/slide_NNN_graphed.js`
(copy of the native build with ONLY the graph region swapped for `addImage`).
QA evidence banks under `videos/<VIDEO>/recreated_pptx/qa/slideNNN/graphgen/`
(note: for curated-deck slides the pilot dir is `qa/slide64/graphgen/`, slide id without
zero-padding where the deck's QA dirs use unpadded names — follow whatever the slide's
existing QA dir uses).

## Environment

Python venv in `graphgen/.venv` (pinned in `requirements.txt`):

```bash
graphgen/.venv/bin/pip install -r graphgen/requirements.txt
```

Contains numpy, scikit-learn, matplotlib, pillow (+ deps). Add anything else a slide
genuinely needs — but keep the venv lean and re-pin `requirements.txt` after installs.

## Per-slide decision workflow (MANDATORY order)

1. **Decide + DOCUMENT**: lib → function → algorithm → data, per slide. The graph must run
   the SAME algorithm as the lecture topic on the RIGHT data (e.g. slide 64: the lecture is
   PCA on Iris → `sklearn.decomposition.PCA(n_components=3)` on `sklearn.datasets.load_iris()`,
   the real 150-sample data — "same AI algorithm, same data"). Library choice is researched
   with the agy websearch CLI (below), not guessed.
2. **PIL forensics on the original frame** (`videos/<VIDEO>/unique_slides/slide_NNN.jpg`):
   locate the graph region, measure cluster colors (hex), background color, point size,
   presence of axes/gridlines/labels, region aspect ratio. The session model cannot see
   images — PIL measurement is the only ground truth for these parameters.
3. **Generate**: matplotlib (or the chosen lib) matched to the measured colors, marker
   size, viewpoint (elev/azim tuned by PIL-comparing cluster spread/shape to the original
   region), high dpi, tight bbox, background chosen to composite cleanly in the PPTX
   (transparent PNG works through the soffice render; a baked background color also works).
   Save iterations as `graph_v1.png`, `graph_v2.png`, ... under
   `qa/slideNNN/graphgen/`. Bank the final generation script as `graphgen/slide_NNN_<topic>.py`.
4. **Vision-validate the standalone graph** through
   `scripts/16_vision_gate.sh` (default route = images model, NO `--models` flag, NEVER any
   other model; probe-first per `scripts/17_worker_instructions.md`): comparison of
   `graph_vK.png` vs the original frame, restricted to the graph region. Fix and regenerate
   per findings until FINAL VERDICT: PASS (degenerate garbage = re-invoke; up to 3 garbage
   retries, 6 attempts total on this leg).
5. **Embed**: `cp build/slide_NNN.js build/slide_NNN_graphed.js`, modify ONLY the copy —
   replace the native graph shapes with `addImage` of the validated PNG at the measured
   region position/size. Original frame is 960x540 → 1px = 1pt at 13.33x7.5in.
6. **Certify the graphed slide**: build → soffice render (private
   `-env:UserInstallation` profile) → pdftoppm 150dpi → full judge comparison vs the
   original using the MANDATORY judge template from `scripts/17_worker_instructions.md`
   (GROUND RULES prelude included). Standard verdict law: 6 attempts; PASS only from a real
   comparison-transcript winner body. Write the per-slide report
   (`PILOT_REPORT.md` for the pilot; later slides: add a section to the slide's graphgen dir).

Pilot: slide 64 (`qa/slide64/graphgen/PILOT_REPORT.md`) — reference pattern for all other
graph slides.

## agy websearch CLI (for ALL web research)

```bash
node /home/ahmed/Projects/agy_search/agy_cli/dist/cli.js "<query>"        # human summary + citations
node /home/ahmed/Projects/agy_search/agy_cli/dist/cli.js "<query>" --json # raw JSON
```

Grounded Google-search wrapper, ~5s per query, token discovery automatic. Use it for
lib/API/recipe research instead of guessing. (`dist/index.js` is the MCP stdio server —
do not call it; `dist/cli.js` is the CLI. No `dist/search.js` exists.)

## Operational reminders

- Always go through `scripts/16_vision_gate.sh`; probe the gateway window first.
- Render pipeline: `soffice --headless -env:UserInstallation=file:///tmp/lo_<name>
  --convert-to pdf` → `pdftoppm -png -r 150`.
- Keep everything under `videos/<VIDEO>/` and `graphgen/`. Never delete banked evidence.
