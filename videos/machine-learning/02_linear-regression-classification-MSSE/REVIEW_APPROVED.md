# Founder approval — unique frame set (2026-10-13)

The founder reviewed and APPROVED the extracted unique frame set for this video and
simultaneously supplied the recreation dependency graph (recorded verbatim below).
This lifts the 2026-10-10 HARD STOP for this set; scripts 12/13, DB registration and
build dispatch are authorized from this point.

Founder message (2026-10-13, to the coordinator session):

> I already extracted unique frames for the video, and they are under:
> /home/ahmed/Projects/ai_llm_slides/videos/machine-learning/02_linear-regression-classification-MSSE/unique_slides/
> so continue to the next step after that
>
> and here are the slides deps
>
> 5 > 4
> 10 > 9
> 11 has a component that has same position and size as of 9 (depends on it, but with bigger similarity, so be careful)
> same also 12 has similar dependancy on 11 as 9,
> 13 depends on 12, because it has a component that is on 12, but it's being resized (smaller and positioned in top left of the frame (the axis component)
>
> 14, 15, 16 can start in parallel but they have a common ooml component,
>
> 19 > 18
> 24 > 23
> 26 > 25
> 29 > 28
> 32 is exactly as 31 (duplication but it's intentional on the original slides, but on ours we will follow it as well)
> 35 depends on 31

Provenance notes:

- The set on disk: `unique_slides/slide_001.jpg` … `slide_039.jpg` (39 slides,
  extraction mtime 2026-10-12 01:51; curated/renumbered densely by the founder).
- The pre-curation namespace state (6198 frames → 210 unique slides, review packet,
  DB) was replaced by the founder's curation; no new2old reconciliation is possible
  or required (no downstream artifacts were ever produced for this video).
- The curation metadata (which frames were dropped) is founder-owned knowledge; the
  39 files are the complete, authoritative set.
