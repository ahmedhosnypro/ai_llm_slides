# SOURCES.md — slide 025 "Sine/Cosine Encoders (an industrial application of Motor Control System)"

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Machine-verified 2026-10-11: vision transcript of record
`transcripts/slide_025_vision_2026-10-11.txt` (default `images` route,
`--thinking high --max-tokens 65536`, gated via `scripts/16_vision_gate.sh`,
validated winner round 1) + live curl of three sources + two agy searches.

## Slide identity

- New (curated) slide **025** ← old extraction **47** (kept frame
  `frame_01299.jpg`, shown t≈1289–1298 s — only ~10 s on screen: a quick
  industrial aside) (`unique_slides/slides_index.json`), frame
  `unique_slides/slide_025.jpg`.
- Frame facts (vision transcript): title "Sine/Cosine Encoders", subtitle
  "(an industrial application of Motor Control System)"; badge "25". Left
  panel: grayscale AC-motor clip-art in a green-bordered box, "AC Motor"
  label, tan "Sin/Cos Encoder" callout. Red block arrow "Sin/Cos Encoder
  Output Signals" to the right panel: circular encoder disk drawn as two
  interleaved sinusoidal traces (red "cos", green "sin") around a hub,
  "Rotation direction CCW/CW" double-headed arrow, "Sin/Cos signal period"
  bracket over one scallop, "Line count =16" + "(16 signal periods per
  revolution)". Bottom caption: "Incremental rotary  position encoders are
  used in many applications to measure angular  position and speed."
  "For More Info:" citation (blue italic): "EXTRACTION OF HIGH RESOLUTION
  POSITION INFORMATION FROM SINUSOIDAL ENCODERS / J. Burke, J. F. Moynihan,
  K. Unterkofler". Mouse-cursor artifacts near the encoder label and the
  right panel (recording artifacts).

## The slide's own citation (frame verbatim)

- "EXTRACTION OF HIGH RESOLUTION POSITION INFORMATION FROM SINUSOIDAL
  ENCODERS", J. Burke, J. F. Moynihan, K. Unterkofler — this is the slide's
  "For More Info" pointer; the string itself is a frame fact.
- **Venue [?]**: agy (2026-10-11) attributes it to the **PCIM-Europe 1999**
  conference (pp. 217–222), authors then at Analog Devices. NOT verifiable
  from this environment — see "Failed verification paths" below. An
  alternative hypothesis that it is Analog Devices application note AN-710
  could not be confirmed either (analog.com unreachable; agy contradicted
  itself about AN-710's title across two queries — one answer named the
  PCIM paper, another named an unrelated JESD204B FPGA note; treat both agy
  venue claims as unreliable). Confidence on the venue: **[?]**.

## What the sources CONFIRM (live-verified 2026-10-11)

- **Wikipedia, "Rotary encoder"** —
  https://en.wikipedia.org/wiki/Rotary_encoder (fetched raw wikitext,
  `scratch/webverify/rotary_encoder_wiki.txt`): "A rotary encoder, also
  called a shaft encoder, is an electro-mechanical device that converts the
  angular position or motion of a shaft or axle to analog or digital output
  signals"; and "This is similar to **sine encoders, which output sinusoidal
  waveforms in quadrature (i.e., sine and cosine)**… The waveform frequency
  indicates the speed of shaft rotation… whereas the A-B phase relationship
  indicates the direction of rotation." — confirms the slide's sin/cos pair,
  the CCW/CW direction information, and the position+speed caption.
- **Design World / Motion Control Tips, "What is a sine encoder (aka
  sine-cosine encoder)?"** —
  https://www.motioncontroltips.com/what-is-a-sine-encoder-aka-sine-cosine-encoder/
  (live curl, `scratch/webverify/sine_encoder_mct.html`): "sine encoders
  supply position and direction information as … analog sine waves —
  typically termed "A" and "B" — **in quadrature**… When two sine waves are
  in quadrature, one is actually a cosine. This is why sine encoders are
  also referred to as "sine-cosine encoders""; "The output frequency is
  determined by the **encoder's line count** and mechanical speed…";
  interpolation between sine samples gives "extremely high position
  resolution" — confirms the slide's "Line count = 16 (16 signal periods per
  revolution)" terminology and the sin/cos-encoder framing.
- **Connection to the lecture's own topic**: this industrial aside motivates
  the course's upcoming Sin/Cos positional encoder (slide 032 and the PE
  block 026–034; arXiv 1706.03762 §3.5 — "we use sine and cosine functions
  of different frequencies", live-verified on slide 021's fetch). The
  analogy (rotary sin/cos encoders ↔ transformer sin/cos PE) is the
  lecturer's pedagogy; the paper does not mention it.

## Figures used by this slide

- **None downloaded.** The motor graphic is generic clip-art; the encoder
  disk (two interleaved sinusoids around a hub) is course-drawn in the
  standard encoder-diagram convention (vision transcript: matches no
  published figure verbatim). The cited Burke/Moynihan/Unterkofler paper's
  own figures were not locatable from this environment (see below).

## Failed verification paths (do NOT re-attempt blindly)

- analog.com — unreachable from this network (curl and WebFetch both fail:
  connect timeout / socket closed).
- https://www.analog.com/media/en/technical-documentation/application-notes/AN-710.pdf
  — 404 (via jina reader); no Wayback snapshot of that URL.
- Bing/DDG organic search — bot-walled (returned generic "Extraction (2020
  film)" results, ignoring the quoted phrase).
- Semantic Scholar API — persistent 429; Crossref — the paper is not indexed;
  Google Books API — no result.
- agy gave two contradictory AN-710 attributions — do not trust either.

## [?] Uncertain items

- [?] Publication venue/URL of the slide's citation (PCIM-Europe 1999 [?] vs
  an Analog Devices application note [?]) — needs a future check from a
  network that can reach analog.com or a library database.
- [?] Whether the course's "Line count = 16" figure value comes from the
  cited paper's example or is the lecturer's own illustration choice.

## Corrections

- none — no transformer-content claims on this slide to correct; the
  encoder-domain statements are standard and confirmed.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows. This
source confirms/corrects DATA and records provenance; it never licenses
inventing or "improving" content the slide doesn't show.
