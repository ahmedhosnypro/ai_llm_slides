# Rebuttal of judge_attempt_1 finding D1 (MAJOR "frame overflow") — measured forensics

Judge attempt 1 (transcript judge_attempt_1.txt, real winner body, coherent, degenerate
events 0) returned FAIL on a single MAJOR defect:

> D1: "The inner white content frame's right border sits at ~x 1975/2000 (~98.7% slide
> width), while the house panel's right red border sits at ~x 1912 (~95.6%) ... crosses
> over the panel's right red border, burying it. In the original, the inner frame's right
> edge (~93.5%) stops safely inside the panel ... in the recreation there is no visible
> panel border or gray to the right of the inner frame at all."

## Measured rebuttal (render_3.png, 2001x1125 @150dpi; frame-px = render-px * 72/150)

1. Content-box right stroke: render cols 1864-1865 = frame 894.7-895.2, color exactly
   (192,0,0) = C00000. Original stroke: col 894 (322 red px). Delta +0.7 frame-px.
   93.2% of slide width — NOT 98.7%. The judge's own original-side reading (~93.5%)
   matches the recreation's actual 93.2%.
2. House panel right border: render cols 1914-1915 (frame 918.7-919.2) with 1031-1032
   red px per column = the FULL slide height — the border is fully visible, not buried.
3. Gray sliver between frame and panel border: cols 1866..1913 sample (233,233,231)
   = E9E9E7, present and intact.
4. At the judge's claimed frame position (col 1975 = frame 948): pure white canvas
   (255,255,255) — there is NO ink and NO frame edge anywhere right of the panel border.
5. "Cube image's white background reaching ~x 1930": cube crop C spans frame x 680..881
   (render 1417..1835); at col 1930 (frame 926) the render is white CANVAS (chrome), not
   cube imagery. The cube's extent is identical to the original's (self-check cube bbox
   delta <= 0.3 frame-px).
6. selfcheck_attempt_3_out.txt: box strokes left 64.6-65.1 vs orig 65; right 895.1-895.6
   vs orig 894; top 168.6-169.1 vs 169; bottom 491.5-492.0 vs orig 490-491 — all within
   ~1.5 frame-px.

## Other findings

- D2 (frame ~5% too wide): consequence of D1 — false by the same measurement.
- D3 (MINOR, red tone "brighter than ~#C00000"): the recreation's red IS C00000
  ((192,0,0) measured). The original's JPEG capture darkens its red to ~(137,37,49)
  modal ~B01020 — the documented deck-wide precedent (certified slides 005/029/040) is
  to use the design color C00000, not the JPEG-darkened sample. Pre-existing MINOR
  class per judging.md; not a fix trigger.
- D4 (MINOR, typed vs handwritten header): ground rule (d) — at most MINOR, explicitly
  not a fix trigger.

## Disposition

No finding survives measurement; no build change is warranted (moving the frame right
edge to the judge's suggested ~95.5% would CONTRADICT the measured original at 93.1%
and break fidelity). Re-judging the unchanged build as attempt 2 (fresh render_4.png
from the same build script, build_attempt_4.js = build_attempt_3.js).
