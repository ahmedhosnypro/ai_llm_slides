# shared_patterns — Deep Learning DSAI 308 playlist

Playlist-level reusable building blocks for slide recreation across ALL lectures
under `videos/deep-learning/` (founder directive 2026-10-11). Discipline matches the
project-level `patterns/` library: one runnable example per pattern, the law in the
comments, a checker where one can exist.

## house_chrome (binding for every recreated slide in this playlist)

- `house_chrome.js` — `drawHouseChrome(pptx, slide, {numeral})` + `CHROME` constants.
  Import in every build; never re-draw the frame/badge per slide.
- `house_chrome_check.py` — run on every 150dpi render before judging:
  `python3 house_chrome_check.py <render.png>` (exit 0 = pass).

Canonical geometry (measured from `001_transformers_part1/unique_slides/slide_001.jpg`,
960×540, 1px = 1pt): gray `E9E9E7` panel x 42..918 px, y 45 px → slide bottom, red
`C00000` border (bottom stroke half-visible at the slide edge), badge circle d≈36 px
at (893, 71) px — `FDFD96` fill, `6A5ACD` ring, bold `333333` numeral — on a white
canvas. Full law: `../AGENTS.md`.
