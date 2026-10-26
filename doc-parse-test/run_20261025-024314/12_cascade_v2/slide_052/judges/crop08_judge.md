=== /home/ahmed/Projects/ai_llm_slides/doc-parse-test/run_20261025-024314/12_cascade_v2/slide_052/crops/crop08_y_row/crop.png ===
[winner] images (round 1, attempt 1)
**Crop geometry:** box (30,236)â(310,287) â 280Ã51 px, shown at 3Ã (840Ã153). Coordinates below are in original crop-px.

## (1) Full transcription (crop-px)

| Text (red) | Position (crop-px) | Notes |
|---|---|---|
| `Ya` | x â 68â80, y â 28â46 | Y + small round subscript 'a', sits on 3rd cell of left table |
| `Y1` | x â 146â158, y â 28â46 | Y + tiny degraded subscript (thin stroke), middle table |
| `Y2` | x â 222â236, y â 28â46 | Y + clear subscript '2', right table |

Non-text elements (no glyphs): pastel 6-cell table bodies at y â 23â43 (x â 42â105, 122â182, 207â266); blue rule across top (y â 20); red diagonal strike entering top-right, crossing down through the third table region (â(190,0)â(232,51)); three red arrowheads poking up from the bottom edge at x â 72, 150, 230 (y â 45â51); colorless slivers of neighboring icons in the extreme top corners. No other legible text anywhere in the crop.

## (2) Red Y tag count, positions, readings

- **Count: 3** (doc-parse caught only 2 â it missed the middle one).
- **x positions (crop-px):** â 72, â 150, â 228.
- **Glyph readings:**
  - Tag 1 (xâ72): **'Ya'** â subscript shows a bowl/round shape, matches parse.
  - Tag 2 (xâ150): **'Y1'** â subscript survives only as a thin vertical stroke; unlike tag 1 it has no bowl, so it is a digit '1', not 'a', and definitely not a bare 'Y'.
  - Tag 3 (xâ228): **'Y2'** â clear '2', matches parse.

JUDGE VERDICT: Three red Y tags, not two â 'Ya' (xâ72), 'Y1' (xâ150, dropped by doc-parse), 'Y2' (xâ228).

