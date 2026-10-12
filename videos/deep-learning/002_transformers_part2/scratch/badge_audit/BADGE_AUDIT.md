# BADGE AUDIT — slide_048 vs slide_049 printed-badge conflict (002_transformers_part2)

Date: 2026-10-12 · Method: pure PIL + numpy + scipy.ndimage on the 960x540 frames in
`unique_slides/` (read-only). **No vision-model calls.** All scripts and measurements
in `scratch/badge_audit/`.

## Verdict (founder decision input)

| Slide | Prints | How established |
|---|---|---|
| `slide_048.jpg` | **48** | Left digit top = "4" (IoU 1.0). Right digit top (5 visible rows) = "8" — **pixel-identical (IoU 1.0, zero shift) to the units-"8" of slides 018 and 028**; "9" scores 0.769 and is topologically impossible (see below). |
| `slide_049.jpg` | **49** | Badge fully visible; glyph topology + template match. |

**This is NOT a course-side numbering duplicate.** Only slide_049 prints "49".
The three raw transcriptions misread slide_048's badge because ~60% of the disc and
the bottom 6 rows of both digits are hidden behind a green content box in the video
frame itself — only the digit TOPS (y=67..71 of y=67..77) are visible. The machine
evidence below reads those tops decisively as "48".

House-chrome consequence: badge numeral 48 for slide_048, 49 for slide_049 (= file
ids, consistent with the playlist law and the 53/53 deck sweep).

---

## 1. Method

1. **Disc detection** — pale-yellow threshold `(r>215)&(g>205)&(b<215)&(r-b>35)&(g-b>35)`
   restricted to the chrome corner (y<170, x>=830); largest blob within 60 px of the
   measured chrome position (877,70). Disc fill measured as the blob median RGB.
2. **Ink candidate region (the crux)** — the yellow mask has digit-shaped holes, so
   ink is searched inside `fill_holes(disc) | closing(disc, 3x3 x3) | occlusion_extension`,
   where `occlusion_extension` adds, per column, the rows between the column's lowest
   yellow and a detected green box edge `(g-r)>40 & g>110` — only when that edge cuts
   the disc above its natural elliptical bottom (chrome constants cx=876.5, cy=70.5,
   rx=16.5, ry=15.0 measured from full-disc controls 047/050).
3. **Ink guards** — `lum<185` (kills gray background), `r-g>-60` (kills green box),
   `b-r<60` (kills blue-violet ring core; ring is already excluded geometrically).
4. **Ink threshold** — color distance from disc fill > 70 (robustness re-checked at
   100 and 140); connected components (area >= 5), left-to-right; pairs wider than
   8 px split at a zero/minimum ink column (digits sometimes touch).
5. **Glyph evidence per component** — bbox, stroke width, **hole topology** (enclosed
   background components of the padded mask, with hole centroid y as fraction of glyph
   height), and a 1 px = 1 char ASCII bitmap.
6. **Template ruling** — every badge in the deck was measured; digit templates are
   compared by IoU over the visible rows, in the same chrome slot (see §3).

Scripts: `badge_audit.py` (detection + glyph metrics + deck sweep),
`ruling_048.py`, `ruling_048_v2.py`, `ruling_048_v3.py` (phase-matched comparisons),
`checks_final.py` (raw-pixel occlusion checks), `debug_ink.py`, `debug_colors.py`.
Machine-readable dump: `badge_measurements.json`. Full runs: `run_output.txt`,
`ruling_v3_output.txt`.

## 2. Chrome geometry (measured)

- Full disc: ~31x30 px, e.g. 047 bbox `[860,56,892,85]`, center (877.1, 70.9),
  fill RGB (254,255,159). Digit band: **y=67..77** (glyph height 11 px).
- Two-digit layout: **tens digit at x=867..873, units digit at x=875..882**
  (gap column x=874), stable across the deck (phase-matched rendering — same digit in
  the same slot rasterizes identically on every slide, verified across all occurrences).
- Purple ring hugs the disc; its dark core is excluded by geometry, its pink AA by `b-r<60`.

| slide | disc bbox | center | yellow px | fill RGB | state |
|---|---|---|---|---|---|
| 047 | [860,56,892,85] | (877.1, 70.9) | 732 | (254,255,159) | full disc |
| 048 | [864,56,892,78] | (878.0, 63.8) | 396 | (254,255,161) | **bottom cut by green box at y=72** (natural bottom y=85) |
| 049 | [858,56,892,79] | (875.5, 67.5) | 626 | (255,255,160) | full disc (bottom 2 px under box shadow) |
| 050 | [859,56,892,85] | (875.6, 70.4) | 768 | (254,255,159) | full disc |

Direct RGB at the occlusion line (slide_048): box border row y=72 is green —
e.g. (32,105,0) at x=872, (103,179,71) at x=873; digit rows y=67..71 are visible on
both digits; y>=72 is box.

## 3. Calibration controls (the method must read these right)

**slide_047 → prints "47"** — 2 components:
- glyph 0 "4": 7x11 @ [867,67,873,77], area 43, stroke 3.0, **one closed counter, low**
  (hole area 2-4 px, centroid cy_frac **0.59**) — classic closed-4 signature.
- glyph 1 "7": 6x11 @ [876,67,881,77], area 31, stroke 2.0, **no holes**; top bar +
  descending diagonal.

**slide_049 → prints "49"** — 2 components:
- glyph 0 "4": 7x11 @ [867,67,873,77], area 43 — byte-for-byte the same glyph as 047's.
- glyph 1 "9": 8x11 @ [875,67,882,77], area 51, **bowl counter high** (area 9-10 px,
  cy_frac **0.39**) + tail notch (area 4 px, cy_frac 0.8); right stem continues below.

**slide_050 → prints "50"** — one merged 16x11 component (5 and 0 touch); column-min
split yields "5" (no holes) + "0" (large centered counter, area 21-25 px, cy_frac
0.55). ASCII plainly shows `5` and `0`.

**Deck-wide sweep (002..060): 53 of 53 machine-readable badges print their own file
id — 0 mismatches.** Not machine-readable by component count (each verified by direct
ASCII inspection): 014 (extra 3 px AA fragment; the two real glyphs read "14"),
053/054/055 (digit pairs touching; ASCII shows 53/54/55), 046 (disc 100% hidden behind
slide content — 1 yellow px in the whole chrome region), and 048 itself (the subject,
partially occluded). This sweep validates the extraction pipeline end-to-end.

## 4. slide_048 — the contested badge

Occlusion: a green-bordered content box (slide's own graphic) covers the disc from
y=72 down; the disc's lower half and the digits' lower 6 rows are hidden. Visible ink:
2 components, digit TOPS only (rows 0-4 of 0-10).

```
LEFT glyph  4x5 @ [869,67,872,71]  area 14        RIGHT glyph 7x5 @ [875,67,881,71]  area 25
   ...#                                            ..####.
   ..##                                            .######
   .###                                            ###..##
   ####                                            ##...##
   ####                                            .######   ← waist closes: ENCLOSED counter
                                                                     (hole area 5 px, cy_frac 0.72)
```

Ink x-spans per visible row (absolute frame coordinates):

| row (y) | left glyph | right glyph |
|---|---|---|
| 67 | 872 | 877-880 |
| 68 | 871-872 | 876-881 |
| 69 | 870-872 | 875-881 |
| 70 | 869-872 | 875-881 |
| 71 | 869-872 | 876-881 |

(The "4"'s stem right edge at x=873, rows 68-71, is washed out by the box edge AA —
direct RGB there is light yellow-olive (192-213, 195-216, 140-147) — which is why the
left component is 4 px wide, not 5. All structural rows match the deck's "4".)

### Left digit = "4"
IoU of the visible 5-row top (ink-bbox aligned) vs every deck digit's top: **"4" family
0.875-1.0** (040's tens-4: 1.0; 049's tens-4: 0.933; 047's: 0.875 — differences are the
faded x=873 edge only), vs "9" 0.346, "7" 0.185, everything else <= 0.53. Unique match.

### Right digit = "8" — three independent pixel proofs

**(a) Exact template match.** Phase-matched units digits (two-digit badges with the
same 7-wide tens at x=867-873), rows 0-4 ink spans vs the observed:

| digit | deck occurrences (same slot) | top-5 IoU vs observed | verdict |
|---|---|---|---|
| **8** | 018, 028 (also 038, 058) | **1.0 — exact, zero shift, all 5 row spans identical** | MATCH |
| 9 (the raws' claim) | 019, 029, 039, 049, 059 | **0.769** — all 5 occurrences differ identically | excluded |
| 2 | 022, 042, 052 | 0.8 | excluded |
| 3 | 023, 043 | 0.8 | excluded |
| 6 | 026 (also 016/036/056) | 0.741 | excluded |
| 0 | 020, 040 | 0.741 | excluded |
| 5 | 025, 045 | 0.704 | excluded |
| 7 | 027, 047 | 0.419 | excluded |
| 1, 4 | 021/041, 024/034/044 | 0.3-0.4 | excluded |

The "9" failure is concrete: every deck "9" in this slot renders row 67 as a 3 px apex
(x877-879), row 68 ending at x880, and rows 69-71 as an OPEN bowl `##...##` — the
observed glyph has a 4-5 px apex (x877-880), row 68 reaching x881, and a CLOSED waist
`.######` at y=71. Slide_049's own "9" (identical chrome, identical tens "4", identical
slot) is the direct counterexample: IoU 0.769, differing in exactly those pixels.

**(b) Topology.** Within the visible 5-row window the observed glyph contains an
**enclosed counter (5 px)** — the bowl closed from below by the waist row `.######`.
A "9" clipped at this height cannot enclose anything (its bowl drains downward into
the occluded tail); nor can "2", "3" (left wall collapses by row 70: `.#...##` /
`.....##`), "6" (right side opens), "0"/"5"/"7"/"1"/"4". Among digits 0-9, only the
"8" produces a closed upper counter inside these 5 rows.

**(c) Course sequence.** 047 prints "47" (verified), 049 prints "49" (verified); the
dependency record has 48←47 and 49←26. A "42"/"43" print would break the monotonic
course numbering, and no raw transcription claimed it — the only contested value was
"49", which the pixels exclude.

### Why the raw transcriptions read "49"
The visible sliver is exactly the digit tops `4?` where the tops of "8" and "9" look
alike (both are round arcs at 1-2 px stroke). Three models interpolating a 60%-hidden
badge converged on the wrong completion; the neighboring slide_049 (a fully visible
"49") plausibly anchored the guess.

## 5. Conclusion

- **slide_048.jpg prints "48"** (left "4" IoU 1.0; right "8" IoU 1.0 exact vs 018/028,
  "9" excluded at 0.769 with 5/5 consistent phase-matched counterexamples and an
  impossible topology). Badge numeral for the recreation = **48**.
- **slide_049.jpg prints "49"**. Badge numeral = **49**.
- **No course-side duplicate**: each of 048/049 prints its own number; the file-id
  mapping is correct, and the deck sweep (53/53, 0 mismatches) confirms file id =
  printed badge across the whole video.

## 6. Evidence index (scratch/badge_audit/)

- `slide047_badge_x8.png`, `slide048_badge_x8.png`, `slide049_badge_x8.png`,
  `slide050_badge_x8.png` — 8x nearest-neighbor crops of the badge region
  (slideNNN_badge_x8.png for all 59 frames also present).
- `badge_audit.py` — full method (detection, ink region, guards, components, holes,
  sweep); `badge_measurements.json` — machine-readable results.
- `ruling_048.py`, `ruling_048_v2.py`, `ruling_048_v3.py` — template rulings;
  `ruling_v3_output.txt` — phase-matched span tables (section A), 4X-family IoUs
  (section B), left-digit table (section C).
- `checks_final.py` — raw-pixel occlusion check (box edge y=72; direct RGB table),
  slide_046 status, 014/053/054/055 inspection.
- `run_output.txt` — complete final run log.
