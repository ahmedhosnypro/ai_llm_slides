# Slide 044 — "Solution? Zero-padding!, Others!!" — web sources

Slide content (from `../analysis/slide_044_raw.json`): bullet "For s = 1, surround the
image with (h_f-1)/2 and (w_f-1)/2 layers of 0"; diagram 7x7 padded input (original 5x5
surrounded by a one-cell cyan zero ring) * 3x3 yellow filter [[0,0,1],[0,1,1],[1,1,1]]
= 5x5 output grid; note box: "Original 5x5 / After padding ONE pixel (surrounding the
image) it will be 7x7 / After apply one filter of size 3x3, output will be 5x5 again /
Do the same for next applied filter".

## Source URLs (fetched 2026-10-12)

1. **CS231n — Convolutional Neural Networks**
   <https://cs231n.github.io/convolutional-networks/>
   CONFIRMS the slide's bullet verbatim: "In general, setting zero padding to be
   P = (F - 1)/2 when the stride is S = 1 ensures that the input volume and output
   volume will have the same size spatially." Also: zero padding "allows us to control
   the spatial size of the output volumes (most commonly ... to exactly preserve the
   spatial size of the input volume so the input and output width and height are the
   same)". For the slide's F=3, S=1 case: P = (3-1)/2 = 1 layer — matches the slide's
   one-cell zero ring, and 7x7 -> (7-3+2*1)/1+1 = 5 = original size.
2. **Dive into Deep Learning (d2l.ai), ch. 7.3 "Padding and Stride"**
   <https://d2l.ai/chapter_convolutional-neural-networks/padding-and-strides.html>
   CONFIRMS: "we will want to set p_h = k_h - 1 and p_w = k_w - 1 to give the input and
   output the same height and width ... Assuming that k_h is odd here, we will pad
   p_h/2 rows on both sides of the height" — i.e. (k-1)/2 = (h_f-1)/2 zero layers on
   each side, exactly the slide's formula; "CNNs commonly use convolution kernels with
   odd height and width values, such as 1, 3, 5, or 7."
3. **Goodfellow, Bengio & Courville, *Deep Learning*, ch. 9**
   <http://www.deeplearningbook.org/contents/convnets.html>
   Figure 9.13 (bottom): "By adding five implicit zeros to each layer, we prevent the
   representation from shrinking with depth" — the same solution for the cascade problem
   of slide 043.
4. **Wikipedia — Convolutional neural network**
   <https://en.wikipedia.org/wiki/Convolutional_neural_network>
   For the "Others!!" in the title: "Sometimes, it is convenient to pad the input with
   zeros (or other values, such as the average of the region) on the border" — the
   page's boundary-conditions figure (downloaded below) shows the four standard padding
   strategies: zero, replication, reflection, circular.

## Downloaded figures (original filenames kept)

- `Convolutional_neural_network,_boundary_conditions.png` — Wikipedia CNN-article figure
  "Three example padding conditions": zero padding vs replication (pad with nearest
  inside pixel), reflection (mirror), and circular (wrap-around) — the "other" padding
  variants the slide's "Others!!" alludes to.
  Source: <https://commons.wikimedia.org/wiki/Special:FilePath/Convolutional_neural_network,_boundary_conditions.png>
  (file page: <https://en.wikipedia.org/wiki/File:Convolutional_neural_network,_boundary_conditions.png>)

## Confirmed vs the slide

- The same-size padding rule ((h_f-1)/2, (w_f-1)/2 zero layers for s=1, odd filter) is
  CONFIRMED verbatim by CS231n and d2l.
- The size arithmetic is CONFIRMED: 5x5 + 1-cell pad -> 7x7; 7x7 * 3x3, s=1 ->
  (7-3+2*1)/1+1... i.e. (7-3)/1+1 = 5x5 — output size preserved.

## DISCREPANCY recorded (slide wins for recreation; source wins for understanding)

The vision-read OUTPUT grid values [[1,1,2,0,0],[0,1,1,1,0],[0,0,1,2,1],[1,0,2,1,0],
[0,1,1,3,0]] are NOT the arithmetic convolution of the stated 7x7 padded input with the
stated filter under any standard orientation (forward correlation gives
[[3,4,4,2,1],[2,4,4,4,2],[1,3,5,4,2],[1,4,5,3,0],[1,3,2,0,0]]; rot180/transpose/rot90
also fail — all four tested). The claimed grid equals the ORIGINAL image with only 5
cells altered, consistent with a LIVE-LECTURE frame captured while the lecturer was
mid-annotation of the output grid, or with a vision misread of hand-written numerals.
[?] RECREATION NOTE: the original frame is ground truth — before rebuilding, re-derive
the output-grid digits from the frame itself (pixel-level, per the deck's ink-forensics
rule); do NOT "fix" them to the computed convolution. The pedagogical point (output
returns to 5x5) is unaffected.

## Open questions

- [?] What exactly the lecturer meant by "Others!!" is not spelled out on the frame;
  the Wikipedia padding-variants figure (zero/replication/reflection/circular) is the
  standard "other paddings" taxonomy — flagged as interpretation, not slide text.
