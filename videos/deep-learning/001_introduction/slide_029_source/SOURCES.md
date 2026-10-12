# SOURCES.md — slide 029 ("Spatial Structure of Image")

Research date: 2026-10-12. Worker: web-research lane, slides 021–030 (reverse run).

## Slide nature

Lecture bridge slide into CNNs: bullets argue (1) "Images are 2-D" — "k-D if you also
count the extra channels — RGB, hyperspectral, etc."; (2) "What does a 2-D input really
mean?" — "Neighboring variables are locally correlated". Imagery: Grumpy Cat meme
(same meme as slide 030) with a red box around the nose, a zoomed tilted cat close-up with
four colored arrows pointing inward (local neighborhood), and a fanned stack of the three
RGB channel-separated renderings of the meme (red/green/blue tints).

## Source URLs

1. **d2l.ai — Dive into Deep Learning, §7.1 "From Fully Connected Layers to Convolutions"**
   - URL: https://d2l.ai/chapter_convolutional-neural-networks/why-conv.html
   - Status: FETCHED and CONFIRMED (2026-10-12, curl fallback after docs-fetcher timeout;
     ~100 KB HTML).
   - Confirms (near-verbatim to the slide):
     - Channels: "we blissfully ignored that images consist of three channels: red, green,
       and blue. In sum, images are not two-dimensional objects but rather third-order
       tensors, characterized by a height, width, and channel" (§7.1.4 Channels) → the
       slide's "Images are 2-D / k-D if you also count the extra channels".
     - Hyperspectral: "it is quite natural to add channels other than just red, green, and
       blue. Many satellite images ... have tens to hundreds of channels, generating
       **hyperspectral images** instead." → the slide's "RGB, hyperspectral, etc."
     - Local correlation / locality: "The earliest layers of the network should focus on
       local regions, without regard for the contents of the image in distant regions.
       This is the **locality principle**" (§7.1.2.2) — the architectural consequence of
       the slide's empirical claim "Neighboring variables are locally correlated".
     - Translation invariance (§7.1.2.1) — the other CNN-founding principle the lecture
       section is heading toward.
   - This page's Waldo example (Fig. 7.1.2) motivates detecting a pattern that "can appear
     anywhere" in a 2-D image — the standard lead-in this lecture mirrors.

2. **CS231n — Convolutional Neural Networks for Visual Recognition (Stanford), convnets
   notes**
   - URL: http://cs231n.github.io/convolutional-networks/
   - Status: surfaced by agy search; CS231n is the other canonical source treating images
     as (H, W, C) tensors with spatially local structure. Page not fetched end-to-end from
     this network (earlier cs231n fetch attempts in this run timed out) [? — its role is
     corroborative only; d2l carried the confirmations].

## Downloaded files

Downloaded into `slide_029_source/` from d2l.ai (original filenames preserved; the two
figures of confirming §7.1, embedded as Fig. 7.1.2 "Detect Waldo"):

1. `waldo-football.jpg` (2048×1149 JPEG) — https://d2l.ai/_images/waldo-football.jpg
   - The football-crowd photograph used to motivate spatial locality: find Waldo, who can
     appear anywhere in the 2-D grid. Figure 7.1.2 (left image) of d2l §7.1.
2. `waldo-mask.jpg` (3599×2024 JPEG) — https://d2l.ai/_images/waldo-mask.jpg
   - The corresponding location-mask demo image for the same Waldo figure pair.

## Confirmed / corrected vs the slide

- "Images are 2-D" + "k-D if you also count the extra channels" CONFIRMED (d2l: images
  are third-order tensors H×W×C; more channels → k-D).
- "RGB, hyperspectral, etc." CONFIRMED (d2l §7.1.4 names both RGB and hyperspectral
  satellite imagery explicitly).
- "Neighboring variables are locally correlated" CONFIRMED as the standard motivation
  (d2l's locality principle is the same statement made architecturally).
- Imagery: the Grumpy Cat meme, nose-region red box, zoomed close-up with arrows, and
  RGB channel decomposition are the lecturer's own live-demo construction (same meme as
  slide 030) — frame is ground truth; no external figure needed or used for them.
- Nothing to correct in the slide's claims; bullets are consistent with both d2l and the
  standard CNN curriculum.
- Fidelity note: raw JSON flags a black bottom bar as likely the video-player progress
  bar, not slide content (matches slide 030's bottom bar pattern) — excluded from
  recreation content.

## Open questions

- [?] Whether the lecturer's exact phrasing "Neighboring variables are locally
  correlated" quotes a specific textbook line — no verbatim match found in d2l/CS231n;
  treated as the lecturer's own summary of the locality principle (content-wise, it is
  the same standard fact).

## ADDENDUM (2026-10-12, later same run) — exact origin found

The bullet set is NOT an original summary: it is lifted VERBATIM from **UvA Deep
Learning Course, Lecture 4: Convolutional Neural Networks (Efstratios Gavves)**,
https://uvadlc.github.io/lectures/nov2019/lecture4.pdf — p.15 "What makes images
different?": "Images are 2-D / 3-D if you also count the extra channels / RGB,
hyperspectral, etc. / What does a 2-D input really mean? / Neighboring variables are
locally correlated" (pdftotext-verified). Slide 028's attribution ("Some of Slides are
picked from UVA Deep Learning Course EFSTRATIOS GAVVES") names this deck; the PDF is
banked at `../slide_028_source/lecture4.pdf`. One delta: UvA original says "**3-D** if
you also count the extra channels", DSAI slide generalizes to "**k-D**" — DSAI wording
wins for recreation (fidelity law); UvA wording is the upstream original. This resolves
the open question above: "Neighboring variables are locally correlated" is Gavves's
exact phrasing (via the credited UvA deck).
