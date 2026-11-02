# Worker report — slide 013 label-column fix (2026-11-01)

Scope: slides 013/017/018 only (deck 03, NS=videos/machine-learning/03_ridger_regression_gradient_descent).
No git commits; no evidence deleted; DB writes limited to rows 13/17/18 (only 13 written).

## Root cause
The standing r18 FULL FAIL (R18_FULL_DISPOSITION=FAIL STANDS, PIL-confirmed) was the
missing row-label column (X1/X2/y) in slide 013's three TEST tables. The fix was
already staged in the writer `build/slide_013.js` (skips the component's
label-less `testTables` block and redraws 4-column tables at x669 w204,
cols [50,51,51,51], blank header cell, BLACK non-bold left-aligned labels,
mint y-row), but the pptx had not been rebuilt/judged since.

## Work done
1. Regenerated missing `build/assets/wbox_band{1,2,3}.png` via the banked
   `build/assets/make_013_wbox.py` (600-dpi STIX PNGs; they were absent, which
   blocked the rebuild).
2. Rebuilt: `node recreated_pptx/build/slide_013.js` -> slide_013_recreated.pptx
   (md5 e79ab1c5b835a4fefc15eadd89df1a11).
3. Render: soffice -> pdf -> pdftoppm -r 150 -> `qa/rejudge_20261027/slide013/render.png`
   (2001x1125). `house_chrome_check.py render.png 13` = PASS (chrome_check_fix.txt).
4. PIL on the render: TEST-zone vlines + label-column ink rows 1-3 present
   (127/129/70 ink px), matching the original's 4-column test tables.
5. Judge legs (payload_A.txt FULL / payload_B_013.txt CROP, via 16_vision_gate.sh):
   - FULL `judge_full_fresh.txt`: FINAL VERDICT PASS
   - CROP `crop_dense_judge.txt`: FINAL VERDICT PASS

## DB
Row 13: visual_attempts 6->7, visual_transcript -> rejudge_20261027/slide013/judge_full_fresh.txt,
visual_check kept PASS, updated_at 2026-11-01 23:43:53. Rows 17/18 untouched.

## Deck
`final_deck_tool.py update 13` staged page 13 (deck md5 -> acabd3216ff27d19affb63923db43f3e);
`render_check_pages.py 13` = PASS (0 px differ).

## Cascade (17/18)
`components/slide_013.js` was NOT modified (fix lives in the writer), and
`components/slide_017.js` overrides its own test tables (own label col at x668);
slide_018 imports components/slide_017.js. No rebuild needed.
`render_check_pages.py 17 18` = PASS both (0 px differ; gate_20261101-234725_p17-18).
No fresh judge legs needed for 17/18 (components unchanged since their certified builds).
