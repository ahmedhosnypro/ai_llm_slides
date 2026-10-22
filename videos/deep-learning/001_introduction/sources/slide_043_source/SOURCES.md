# Slide 043 — "Problem: Image will vanish if applying more filters in cascade" — web sources

Slide content (from `../analysis/slide_043_raw.json`): bullets "Our images get smaller and
smaller", "Not too deep architectures", "Details are lost"; a cascade demo: 5x5 image
(same values as slide 041) -> "After conv 1" 3x3 = [[4,3,4],[2,4,3],[2,3,4]] -> "After
conv 2" 1x1 = [18].

## Arithmetic CHECK (hand-verified, numpy)

Convolving the slide's 5x5 image with the slide-041 filter [[1,0,1],[0,1,0],[1,0,1]]
(stride 1, no padding) gives exactly [[4,3,4],[2,4,3],[2,3,4]], and convolving that 3x3
with the same 3x3 filter gives exactly 18. The slide's numbers are arithmetically correct
and internally consistent with slide 041. Size arithmetic matches slide 042's formula:
(5-3)/1+1 = 3, then (3-3)/1+1 = 1.

## Source URLs (fetched 2026-10-12)

1. **Goodfellow, Bengio & Courville, *Deep Learning* (MIT Press), ch. 9**
   <http://www.deeplearningbook.org/contents/convnets.html>
   CONFIRMS the slide's problem verbatim: "the size of the output shrinks at each layer.
   If the input image has width m and the kernel has width k, the output will be of
   width m - k + 1. The rate of this shrinkage can be dramatic if the kernels used are
   large. Since the shrinkage is greater than 0, it limits the number of convolutional
   layers that can be included in the network." Figure 9.13 (see download) shows exactly
   this: kernel width 6, no padding -> shrink by 5 pixels/layer, 16-pixel input supports
   only 3 conv layers; "some shrinking is inevitable in this kind of architecture".
2. **Dive into Deep Learning (d2l.ai), ch. 7.3 "Padding and Stride"**
   <https://d2l.ai/chapter_convolutional-neural-networks/padding-and-strides.html>
   CONFIRMS: "one tricky issue when applying convolutional layers is that we tend to
   lose pixels on the perimeter of our image ... we might only lose a few pixels but
   this can add up as we apply many successive convolutional layers." (Same page gives
   zero padding as the fix — relevant to the follow-up slide.)
3. **CS231n — Convolutional Neural Networks**
   <https://cs231n.github.io/convolutional-networks/>
   The zero-padding paragraph: without padding the output size (W - F + 2P)/S + 1
   shrinks with every layer; zero padding "allows us to control the spatial size of the
   output volumes (most commonly ... to exactly preserve the spatial size of the input
   volume)".

## Downloaded figures

- `dl_book_figure_9_13.png` — Figure 9.13 from Goodfellow et al. ch. 9, "The effect of
  zero padding on network size" (extracted from the book page's embedded base64 image,
  hence the descriptive name; 769x614 PNG). Top row: cascaded convolutions WITHOUT
  padding shrink the representation by 5 pixels per layer (kernel width 6) until it
  vanishes — the slide's "image will vanish" point; bottom row: zero padding preserves
  size with depth. Source page: http://www.deeplearningbook.org/contents/convnets.html

## Confirmed vs the slide

- The problem is the classic border-effect shrinkage of valid convolutions; the slide's
  bullets ("images get smaller and smaller", "not too deep architectures") match
  Goodfellow's "shrinkage ... limits the number of convolutional layers" and d2l's
  "lose pixels ... can add up".
- "Details are lost": consistent with the sources (perimeter/corner pixels are used
  less by the kernels — d2l Fig. 7.3.1 "pixel utilization"; Goodfellow: less expressive
  networks). No correction needed.

## Corrections vs the slide

None. The slide's cascade arithmetic (5x5 -> 3x3 -> 1x1; values 4,3,4/2,4,3/2,3,4 then
18) is exactly reproducible.

## Open questions

None material. [?] Note: the demo reuses slide 041's 5x5 image and filter, so the
"after conv 1" grid is the completed version of slide 041's 3x3 "Result" grid — an
intra-deck consistency fact (slide-internal, not web-verifiable).
