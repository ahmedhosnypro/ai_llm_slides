# SLIDE51_MECHANISM.md — pixel-forensics verdict: the two panels are a COURSE REDRAW, not literal halves of the banked Figure 1

Settled 2026-10-11 by the PIL-forensics worker (PIL + numpy + scipy only — **zero
vision-model calls**). Read-only inputs: `unique_slides/slide_051.jpg` (960×540 JPEG),
`../001_transformers_part1/slide_18_source/The Transformer - model architecture..png`
(1520×2239 RGBA, banked, untouched), and the certified halves
`slide_051_source/fig1_left_half_x0-760.png` / `fig1_right_half_x760-1520.png`
(760×2239 each, composited on white for all tests). Diagnostic sheet:
`diagnostic_sheet.png` (this dir). This settles the `shared_image_sources` caveat and
SOURCES.md open questions 1–2 for the founder's ruling.

## Method

1. Panel detection: calibrated color masks (bright green / orange / cream / mint, each
   with a saturation floor ≥0.05 to exclude the #E8E8E8 chrome and JPEG noise); column/
   row density projection inside the slide content band y=88–512. Masks rejected the
   neutral background (first pass leaked onto gray; fixed with the saturation floor).
2. Hypothesis A (literal halves of the banked PNG placed on the slide) tested two ways:
   - **A1 exact placement**: each banked half resized to the measured panel bbox
     (distortion included, i.e. "the half fills the panel"), grayscale NCC, global SSIM
     (win=7), Sobel-gradient NCC, and binary ink-mask (lum<0.72) Dice.
   - **A2 free placement**: each half resized aspect-preserving at the only legal
     undistorted scale (fit panel height, width 135 px) and slid over every position of
     the panel via FFT correlation — best NCC over all placements/crops.
3. Controls: positive control = same image resample roundtrip (metric ceiling);
   same-style baseline = banked LEFT half vs banked RIGHT half (same style, different
   content).
4. Palette: 16-step RGB quantization of each panel vs each half; targeted fill samples;
   red / dark-navy pixel fractions; mean saturation of non-neutral pixels.
5. Split-stub test: SOURCES.md's own measurement says a literal x=760 split leaves a
   4–5 px black K/V-connector stub at each half's cut edge — checked for dark
   (lum<0.30) pixels at both panels' inner edges and the inter-panel gap.

## Measured panel bboxes (frame 960×540)

| Panel | bbox (x0,y0)-(x1,y1) | size | aspect w/h |
|---|---|---|---|
| LEFT (Encoder) | (140,105)-(443,501) | 304×397 | 0.766 |
| RIGHT (Decoder) | (566,99)-(880,506) | 315×408 | 0.772 |
| banked half | — | 760×2239 | **0.339** |

Gap between panels: x=444–565 (122 px of #E8E8E8 chrome). A half at panel height
(397 px) is only **135 px wide** — each panel is **2.26× wider** than an undistorted
half. Filling the panels requires a 2.26× horizontal stretch distortion.

## Correlation results (Hypothesis A)

| Test | LEFT panel vs left half | RIGHT panel vs right half |
|---|---|---|
| A1 NCC (luminance) | **+0.200** | **+0.103** |
| A1 SSIM (global) | **+0.540** | **+0.233** |
| A1 NCC (gradient/structure) | **+0.071** | **−0.024** |
| A1 ink-mask Dice | 0.227 | 0.313 |
| A2 best sliding NCC (any placement) | **+0.377** | **+0.343** |

Controls:

| Control | NCC_lum | NCC_grad |
|---|---|---|
| POSITIVE: same image, half-res roundtrip | **+0.950** (SSIM +0.892) | — |
| banked L half vs banked R half (same style, diff content) | +0.071 | +0.060 |
| frame L panel vs frame R panel | −0.009 | −0.125 |

The panel-vs-half scores sit **in the "different content" band** (≈ the banked-L-vs-
banked-R baseline), nowhere near the +0.95 a literal placement scores. Even with free
placement, cropping, and aspect preserved, the best match anywhere in either panel is
+0.38. A literal-half slide would read >0.8 on every metric.

## Palette comparison (the decisive signature)

| Statistic | Frame LEFT | Frame RIGHT | Banked L half | Banked R half |
|---|---|---|---|---|
| non-neutral (saturated) pixels | **98.3%** | **94.2%** | 9.3% | 15.4% |
| mean saturation (non-neutral) | 0.573 | 0.408 | 0.183 | 0.188 |
| red pixels (callouts/ellipses/borders) | **0.32%** | **0.53%** | **0.00%** | **0.00%** |
| dark-navy pixels (badge circles) | **1.06%** | **1.34%** | **0.00%** | **0.00%** |

- Frame panel backgrounds: bright green **#11FF74** (46.8% of LEFT panel), cream
  #FDEDDD, orange **#F2A557** (34.8% of RIGHT panel), mint #CFFFE2.
- Frame box fills (sampled): Multi-Head Attention **#B56B50** (terracotta), Feed
  Forward #888574, Input Embeddings #A87D50, Masked Multi-Head Attention **#C675BA**
  (orchid), Encoder-Decoder Attention #AF8658, Output box #788800, badge circles
  **#0F0D78** (navy) — plus course-authored red callouts ("Decoder Only" ×2, "Encoder –
  Decoder Attention", "Adding Mask"), red dashed ellipses, and the yellow "Output /
  Probabilities" banner. None of these elements exist in the banked image, and no
  recolor/transform of the banked raster can create the callouts or red ellipses.
- Banked halves: 79.5% / 66.3% white with pastel fills only (#C8E8F8 pale blue,
  #F8E8B8 pale amber, #F8F8C8 pale yellow) — 0.00% red, 0.00% dark blue.

Side finding: the pending-raw styling note ("Office-blue #4472C4-style boxes") is
inaccurate in detail — the measured redraw palette is custom saturated fills
(terracotta/orchid/tan/gray-olive + navy badges on green/orange/mint panels), not
Office #4472C4. The eventual script-12/13 pass should re-extract colors from the
measured values above.

## Split-stub test

- LEFT panel inner edge (x=430–450): **0** dark (lum<0.30) pixels.
- RIGHT panel inner edge (x=556–576): **0** dark pixels.
- Inter-panel gap (x=450–560): **0** dark pixels.

A literal split at x=760 (or the x=736/784 alternatives) leaves a black connector stub
at the cut edge per SOURCES.md's own pixel measurement; the frame has none. SOURCES.md
open question 1 (which cut line) is therefore **moot for recreation**: no literal cut
exists on this frame.

## CONCLUSION: COURSE REDRAW (Hypothesis B) — with the numbers

The frame does **not** show halves of the banked
`The Transformer - model architecture..png`. It shows a **course-authored redraw** of
the same encoder/decoder topology: two custom panels (304×397 and 315×408, aspect ≈0.77
vs the halves' 0.34), fully saturated custom backgrounds (#11FF74 / #F2A557 / #FDEDDD /
#CFFFE2), terracotta/orchid box fills, navy badge circles, and red callout annotations
that exist nowhere in the source. Structure correlation is at the
different-content baseline (grad NCC +0.071 / −0.024; best possible placement +0.38)
against a +0.95 metric ceiling, ink density 63–65% vs 9.5–15.6%, and the literal-split
stub signature is absent.

Provenance impact: the *content/topology* of 002:51 still inherits 001:18's banked
Figure-1 provenance (arXiv 1706.03762v7 Fig 1, byte-identity proof in SOURCES.md holds
for *understanding*), but the *raster assets* `fig1_left_half_x0-760.png` /
`fig1_right_half_x760-1520.png` are **not what the frame displays** and must **not** be
embedded by the builder.

Builder directive (for the recreation pass): **redraw both panels as vector shapes** at
the measured placements — LEFT (140,105) w=304 h=397, RIGHT (566,99) w=315 h=408 px on
the 960×540 frame — using the measured palette above, with the red callout boxes /
dashed ellipses and banner as course-authored elements. Do not template-match or embed
the banked halves.
