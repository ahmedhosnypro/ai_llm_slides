# worker_report_worker2_duplicate.md — slide 026 DUPLICATE-WORKER COLLISION (worker-2 aborted)

Written 2026-10-12 ~03:45 EEST by the SECOND worker dispatched for slide 026
("Sin/Cos Encoders"). This is a collision/handoff record, NOT a build report —
no judged deliverable was produced by this run. The live worker's own report is
(or will be) `worker_report.md`.

## What happened

This worker was dispatched for slide 026 end-to-end and worked from ~01:15 to
~03:40: full PIL measurement campaign of the original frame
(`scratch/slide026/*.py`), 12 gated vision crop-reads of dense micro-regions
(`cropread_R1..R12*.txt`), and a complete block-granular component build.

At 03:39:08 — 20 seconds after this worker wrote its component — a PARALLEL
worker's files appeared in the same namespace, created by a different agent:

- `recreated_pptx/qa/slide026/render_1.png`           (03:27)
- `recreated_pptx/qa/slide026/../scratch/slide026/cmp_montage.py` (03:28)
- `scratch/slide026/compare_1.png` / `compare_1.txt`  (03:29 / 03:33 — its
  attempt-1 zone-by-zone self-comparison, 7 zones of detailed findings)
- `recreated_pptx/build/slide_026.js` rewritten       (03:39:08 — monolithic
  build, self-contained, does NOT import this worker's component)
- `slides_progress.db` row updated                    (03:39:19)
- `recreated_pptx/slide_026_recreated.pptx` + `build/assets/slide026_wires.png`
  (rebuild after applying its compare_1 fixes, ~03:42+)

Two live writers on one deliverable would corrupt each other's renders,
judgments, and DB fields, so this worker aborted per the no-trample principle
and left the row to the active worker. No DB writes were made by worker-2.

## Handoff state left by worker-2 (all additive, nothing of the live worker touched)

- `build/components/slide_026.js` (worker-2's banked component,
  renderBase(pptx, slide, opts) with opts.skip/opts.only at 23 named blocks) was
  MOVED to `scratch/slide026/worker2_superseded_component.js` so the banked path
  stays clean for the live worker's own banking (a stale component that does not
  match the certified deliverable would be a landmine for children 28/49).
- The build wrapper was never written (Write refused: file already existed with
  the live worker's content).
- Measurement evidence banked under `scratch/slide026/` for reuse:
  - `cropread_R1..R12*.txt` — gated reads of the dense micro-regions (blue-box
    edge labels + 3 connection lines, TIDA upper/middle paths, comparators,
    PSU/24V, right panel, wire-label fan at 6x, encoder/motor at 4x, sub-blocks,
    host+connector).
  - `measure_*.py`, `edges.py`, `fine_struct.py`, `remaining.py`,
    `final_geom.py`, `flood_boxes.py`, `run_scan.py` — PIL geometry/color scans
    (frame->slide mapping re-verified: frame_x = 18.63 + 0.96123*slide_x,
    frame_y = 0.95556*slide_y; chrome borders x 58/901, top 43, bottom 516-517).
  - `fig11_page-02.png` / `fig11_hi-02.png` — TI design-guide TIDUA05B page 2
    (Figure 1-1) rendered at 200/400 dpi from the banked
    `slide_026_source/tidua05b.pdf` (source-figure cross-check route).

## Facts worker-2 established that the live worker should double-check

(already banked in the cropread transcripts; offered as corroboration, not veto)

1. The bottom black band (rows 518-539) is video letterbox BELOW the slide
   bottom edge (slide bottom maps to fy 516, red border 516-517) — correctly
   omitted from the recreation (ground rule c), despite the spec's "black strip"
   region.
2. The "chip/IC icon" near SPI is a presenter cursor overlay artifact
   (cropread_R1, R6: "pen/marker icon ... cursor/screen-annotation overlay") —
   correctly omitted.
3. The 8-wire fan labels: two independent 6x reads (cropread_R11, R5) transcribe
   the last two as "Up" / "Un" (variants Ub/Dn possible) — the transcript of
   record saw only 6 labels. Sub-legible at judge scale either way.
4. Signal-line structure: lines at y~263.5 (SPI, right head into Dual ADC),
   y~319 (Analog, continues past the Analog-path box to the triangle apex and
   onward to the Encoder connector), y~375.5 (TTL into the comparator), each
   with a LEFT arrowhead at the blue-panel end (cropread_R1); analog branch
   drops at x~530.5 to the comparator with a left head (cropread_R3b).
5. Sub-box fills are DIFFERENT per path: top path PEACH ~F5D6BB, middle path
   light green ~D6E7BD, comparators path LAVENDER ~EAE9EF, each with a dark
   olive dashed border (~3C4A1E), inside the C4DCA0 TIDA container with 92D050-
   luma dashed border. The Dual ADC block is a right-pointing PENTAGON
   (homePlate), text "Dual"/"ADC" stacked (cropread_R2).
6. "12-bit ADC" renders as TWO stacked lines ("12-bit" / "ADC") inside the blue
   box, right-aligned near its right edge; SPI and eQEP likewise inside
   (cropread_R1/R7). "Host MCU Interface" reads bottom-to-top, bold
   (cropread_R1); "Encoder connector" likewise (cropread_R2/R3b fragments).

## Status for the orchestrator

- Slide 026 has ONE active build worker (not this one). This run used 0 judge
  attempts and made 0 DB writes.
- Component-banking obligation for 026 (children 28, 49): now on the live
  worker at certification; worker-2's superseded module can be diffed against
  its certified build if useful.
