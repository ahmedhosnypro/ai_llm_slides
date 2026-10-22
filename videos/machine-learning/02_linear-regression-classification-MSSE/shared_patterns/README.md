# shared_patterns — 02_linear-regression-classification-MSSE

Deck-level reusable building blocks (this deck's chrome differs from BOTH the
deep-learning playlist values and the 01_ml-intro values — measured 2026-10-13,
see `house_chrome.js` header for the numbers and the family history).

- `house_chrome.js` — runnable pptxgenjs module: `drawHouseChrome(pptx, slide,
  {numeral})` + the `CHROME` constants. Import it in every build
  (`require('<abs path>/shared_patterns/house_chrome.js')`) instead of re-drawing
  the frame/badge. Per-slide component modules must delegate to or exactly match
  this one.
- `house_chrome_check.py` — closed-loop PIL checker: run it on every 150dpi render
  (`python3 shared_patterns/house_chrome_check.py <render.png> [numeral]`) as part
  of the mandatory pre-judge self-check. FAIL = fix the build before judging.

Adding a new deck-level pattern: runnable example + an index.json entry + the law
in comments (same discipline as the project-level `patterns/` library).
