# PIL adjudication - slide 004, crop_9_let_boxes FAIL v2 (transcript 00:14, paren-render)

## Provenance note
The prior carrier left an orphaned fix loop that at 00:09-00:12 edited
gen_letbox_assets_att9.py (draw_bar -> draw_paren, bow 2 frame-px), regenerated
eq_004_{Yvec,Yhatvec}.png, rebuilt the pptx (00:09), re-rendered render_9.png
(00:10) and re-cut both crop pairs (00:12). The pptx embeds the current assets
(md5 500aa824 / 1889e1af both present in ppt/media). Current bytes = paren build.

## Judge finding adjudicated (crop_9_let_boxes_judge.txt v2)
MAJOR (high conf): "IMG2 delimiters are round parentheses; IMG1 are straight
vertical bars - delimiter TYPE changed."

## Verdict: MAJOR REFUTED as a type claim - same shape class both sides.

Evidence (adjud_att9_letbox_shape.py/.out, per-row ink centroid over each
delimiter band, thr 690):
- ORIG  L-box: left delim bow +1.24px ('('), right delim -0.32px (straight-ish)
- ORIG  R-box: left delim bow +1.50px ('('), right delim +0.32px (straight-ish)
- REND  L-box: left delim bow +1.36px ('('), right delim -0.87px (')')
- REND  R-box: left delim bow +1.51px ('('), right delim -0.37px (straight-ish)
The judge's cited delimiters (crop-x ~170/890 -> frame x ~156.5/~502 = the two
LEFT delimiters) have IDENTICAL bows in both images (+1.36 vs +1.24; +1.51 vs
+1.50). The render's right delimiters bow <=0.9px (sub-frame-px class). The
perceptual difference the judge reported is stroke weight/AA (render stroke
2-3px crisp vs orig 2px JPEG-softened), not delimiter type. ASCII maps banked
in adjud_att9_letbox_shape.out confirm both sides drift the same way.

## Ruling
- MAJOR-1 (delimiter type): REFUTED. The v1 (pre-fix) FAIL on true straight
  bars was correct for the left delimiters; the 00:09 paren fix addressed it;
  v2's repeat FAIL on the paren render is a weight/AA misread.
- MINOR-2 (N-x-1 'x' vs multiplication sign): accepted MINOR (typographic
  glyph class; original's italic serif x vs mathtext \times).
- MINOR-3 (bold-italic X in the Yhat caption), MINOR-4 (Let face/spacing):
  accepted MINORs (font-substitution class per founder-certified 012/013
  convention).
- Result: let_boxes PASS by adjudication. No further build edit (one
  fix-loop cycle spent on this defect: bars -> parens at 00:09). att10 legA
  re-run dispatched on the current bytes because the att9 legA PASS (00:03)
  judged the superseded pre-fix render.
