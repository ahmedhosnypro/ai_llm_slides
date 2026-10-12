# RUNBOOK — final all-in-one deck merge for 002_transformers_part2

Produces `recreated_pptx/002_transformers_part2_final.pptx` the moment the last
slides certify. Everything is LIVE-DB-driven: the certified set is re-queried at
run time (`gen_status='passed' AND visual_check='PASS'`), never a hardcoded
list — so the same two commands work for the 51-slide partial set and the final
60-slide deck.

Pattern: certified ml-intro final-deck-merge law
(`.agents/skills/slide-recreation/patterns/final-deck-merge/example.sh` +
memory lesson "Lossless one-deck merge: verbatim slide XML + retargeted rels,
never re-encode").

## 1. Merge

```bash
cd /home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2
python3 scratch/merge_final_002.py
# default output: recreated_pptx/002_transformers_part2_final.pptx
```

What it does (OPC level, zero slide-XML edits):
- copies each certified deck's `ppt/slides/slide1.xml` VERBATIM as
  `slideN.xml` (rIds are per-slide; OMML `mc:AlternateContent` and graph-slide
  XML copy verbatim like any slide);
- renames media per slide (`imgNNN_<orig>`) — pptxgenjs names
  (`image-1-K.png`) collide across decks;
- retargets ONLY the slide's `.rels` (layout -> shared skeleton layout,
  notesSlide -> per-slide copy, media -> renamed) and the notes copy's
  back-reference to its own slide;
- rebuilds `presentation.xml` + rels + `[Content_Types].xml` for N slides;
- md5-checks the skeleton (master/layout/theme/notesMaster/presProps/
  tableStyles/viewProps/presentation templates) across ALL sources — fails
  loud if a future source was saved by a different toolchain;
- byte-verifies every slide XML / media / notes part against its source after
  writing. Any FAIL aborts with exit 1 — never ship on a FAIL.

## 2. Render gate (0 mismatched pages is the only acceptance)

```bash
./scratch/gate_merge_002.sh recreated_pptx/002_transformers_part2_final.pptx
```

Renders the merged deck AND every certified source in ONE LibreOffice session
(same profile), page-count-checks, then pixel-diffs page N vs source N at
150 dpi (PIL `ImageChops`). Result is banked in
`scratch/merge_gate_002/gate_report.txt` (+ `merged_render.pdf`).

Route notes (host-measured LO breakages, see `scratch/slide011/render_slide011.sh`):
- direct PPTX->PNG is broken (red "Image 0 1" placeholders) — the script uses
  soffice->PDF then `pdftoppm -png -r 150`;
- PDF export fails from the deep project path — files are staged in
  `/home/ahmed/lo_pdf_test` and converted there;
- `/tmp` is BLOCKED (tmpfs ENOSPC law) — `TMPDIR` lives under
  `scratch/merge_gate_002/tmp`, per-file fallback to the short path.

Only proceed when the report says
`PASS — 0/N mismatched pages, merge is lossless`.

## 3. Done-state definition

- Every slide 1..60 (incl. the placeholder cover 1, which certifies via
  founder sign-off + `house_chrome_check.py`, i.e. it enters this set through
  its own DB state rule) certified in `slides_progress.db`.
- Merge script exits 0; gate report says 0/N mismatched pages.
- `002_transformers_part2_final.pptx` stays a SINGLE deliverable in
  `recreated_pptx/` (single-version rule: no `_merged`/`_partial` variants in
  the deliverable dir; partial/scratch artifacts live only under `scratch/`).

## Known caveats (measured 2026-10-12 on the 51-slide partial merge)

0. **Presentation rels must keep the template's non-slide rIds.** The first
   draft renumbered notesMaster/presProps/theme rels to `rId(N+3)..` while
   `presentation.xml` still referenced `rId3` — a dangling `notesMasterId`
   that made LibreOffice DISCARD the deck's `sldSz` and render every page at
   its default 28cm x 15.75cm (all 51 pages pixel-mismatched vs sources;
   measured, first gate run FAILED). The shipped merger therefore keeps
   master=rId1, notesMaster=rId3, presProps=rId4, viewProps=rId5,
   theme=rId6, tableStyles=rId7 byte-stable and puts slides at
   rId8..rId(7+N); it also fails the merge on any unresolved `r:id`.

1. **Page counts differ between this validation run and the final run.** The
   partial gate validated N=51 pages; the final run re-queries the DB and
   gates N=60 (or whatever is certified then). This is by design — the script
   takes the certified set LIVE, never a hardcoded list. Re-run BOTH commands
   for the final deck; the partial gate is evidence the mechanism is
   lossless, not the final acceptance.
2. **`docProps/app.xml` still says `<Slides>1</Slides>`** (pptxgenjs template
   kept byte-verbatim from the skeleton source). Metadata only — PowerPoint
   and LibreOffice regenerate/ignore it; zero rendering relevance. `core.xml`
   is likewise taken from the first source (per-deck timestamps differ).
3. **Slide order = DB certified order (`ORDER BY slide_id`)** — page k of the
   merged deck is certified slide k in that list. Gaps (5, 12, 14, 16, 44,
   47, 48, 57 at validation time) simply close up in page numbering.
4. **Slide 1 (placeholder cover)**: it is NOT in the visual_check='PASS' set
   by definition (judge comparison impossible). If it should be in the final
   deck, its DB row must be put in the certified state by whoever owns the
   close-out BEFORE running the merge — the merger only ships what the DB
   certifies.
5. **Different-toolchain sources**: the skeleton md5-check fails loud on
   purpose (ml-intro precedent: an LO-saved source with its own master chain
   needed a conscious decision). If the check fires for a real slide, handle
   it per the pattern law (self-contained slide XML, render gate decides) —
   do not weaken the check.
6. **Gate runtime**: ~3–6 min for 52 conversions sequential through one LO
   profile; budget time accordingly and run it to completion.
