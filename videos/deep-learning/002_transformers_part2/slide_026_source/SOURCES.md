# SOURCES.md — slide 026 "Sin/Cos Encoders (an industrial application of Motor Control System)" — TIDA-00176 block diagram

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Machine-verified 2026-10-11: vision transcript of record
`transcripts/slide_026_vision_2026-10-11.txt` (default `images` route,
`--thinking high --max-tokens 65536`, gated via `scripts/16_vision_gate.sh`,
validated winner round 1) + live curl of TI.com + the design-guide PDF
downloaded and text-verified. **This slide heads the PE-family build chain
(children 027/028/029 per `slide_dependencies.json`).**

## Slide identity

- New (curated) slide **026** ← old extraction **57** (kept frame
  `frame_01509.jpg`, shown t≈1459–1508 s) (`unique_slides/slides_index.json`),
  frame `unique_slides/slide_026.jpg`.
- Frame facts (vision transcript): title "Sin/Cos Encoders", subtitle "(an
  industrial application of Motor Control System)"; badge "26". A full
  system block diagram, left-to-right: red "Position (Angle)" left arrow;
  blue panel (Fine Angle: atan(A/B) → Option 1: 16 bit / Fine Angle:
  atan(A/B) → Option 2: 12-bit / Coarse Angle: Incremental count; 12-bit
  ADC; eQEP); grey "Host MCU Interface" bar (A,B + SPI / A,B + Analog /
  A,B + TTL); green dashed container titled "TIDA-00176" (16-bit high-res
  path, Dual ADC, Analog path, Comparators, Power Supplies 24 V→5 V/3.3 V,
  Encoder Supply: 5.25 V, Encoder connector); right panel: "Differential
  Sine and Cosine A+,A-,B+,B-,and Marker R+,R-", "Shielded twisted pairs
  cable, up to 50...150m", AC Motor + Sin/Cos Encoder drawings. Bottom
  caption: "EMC-compliant interface to Sin/Cos incremental position encoder"
  + "1-VPP  Differential analog output signals".

## Primary source — CONFIRMED, figure identity established

- **Texas Instruments reference design TIDA-00176, "Interface to Sin/Cos
  Encoders With High-Resolution Position Interpolation"** —
  https://www.ti.com/tool/TIDA-00176 (verified live 2026-10-11 via curl:
  "The TIDA-00176 reference design is an EMC compliant industrial interface
  to Sin/Cos position encoders… utilizes a 16-bit dual sample ADC with
  drop-in compatible 14- or 12-bit versions… connection to external
  processors using SPI and QEP").
- **Design guide PDF downloaded into this dir as `tidua05b.pdf`** (4,636,630
  bytes, application/pdf):
  https://www.ti.com/lit/ug/tidua05b/tidua05b.pdf — "Design Guide:
  TIDA-00176 — Interface to Sin/Cos Encoders With High-Resolution Position
  Interpolation", TIDUA05B, JUNE 2015, REVISED MARCH 2025.
- **Figure identity: the slide is the course's redraw/recolor of the guide's
  Figure 1-1 "Simplified System Block Diagram of TIDA-00176"** — verified by
  text extraction of the PDF: the figure region contains verbatim the slide's
  every label: "Coarse Angle Incremental count", "12-bit ADC", "SPI",
  "Analog path", "A, B", "A+,A-,B+,B-, R+,R-", "Analog", "A, B, R", "TTL",
  "Differential Sine and Cosine A+, A-, B+,B- and Marker R+/R-", "Shielded
  twisted pairs cable, up to 50...150m", "AC Motor", "Comparators",
  "TMS320F28069M LaunchPad", "24 V", "Encoder connector", "Fine Angle:
  atan(A/B)" (×2), "Æ Option 1: 16-bit", "Æ Option 2: 12-bit", "Dual ADC",
  "16-bit high-res path", "5V", "3.3 V", "Power Supplies", "Sin/Cos
  Encoder", "Encoder Supply: 5.25 V", "Host MCU interface". (Note: the
  guide's own revision history replaced an earlier "EMC-compliant" design;
  the current edition's Figure 1-1 is the match.)

## What the source CONFIRMS

- The whole diagram: topology, labels, signal names (differential A+, A-,
  B+, B- + marker R+, R-), 1-VPP differential signaling ("1-VPP Differential
  Output at 2.5-V Offset" in the guide's features), 24-V input → 5 V/3.3 V
  rails, 5.25-V encoder supply, shielded-twisted-pair cable
  ("Cable Length Tested up to 70 m" in the features; "50...150m" in the
  figure), SPI/QEP host interfaces, 16-bit high-res path vs 12-bit ADC
  option, comparators/TTL path, fine angle by atan(A/B) + coarse angle by
  incremental line count (guide §1.2.2/§1.2.3 "Signal Processing Block
  Diagram for Interpolated Angle Calculation": "The total interpolated
  angular position is composed of coarse and fine angle").
- The interpolation idea (position within one sin/cos period recovered from
  the ratio of the two quadrature signals) is the technical bridge the
  course uses to motivate the transformer's sin/cos positional encoding
  (block 026–034; arXiv 1706.03762 §3.5, live-verified on slide 021's
  fetch).

## Course-authored elements / deltas vs the guide

- Title/subtitle and badge "26"; the course recolored the guide's figure
  (blue/green/orange panels) and redrew it in its own style; the red
  "Position (Angle)" output arrow is the course's annotation of the system
  output.
- [?] The vision transcript read the fine-angle label as "atan1(A,B)" in
  places (likely atan⁻¹ with the superscript flattened, or the guide's
  "atan(A/B)"); the guide prints "Fine Angle atan(A/B)" and "Fine Angle:
  atan(A/B)" in Figure 1-1. Frame wins for recreation — confirm the exact
  glyph from the frame at build time; the guide's form is "atan(A/B)".
- [?] The bottom caption's trailing word "switch" (transcript) is likely a
  transcription artifact; the guide's title phrase is "EMC-Compliant
  Industrial Interface Design for Sin/Cos Encoders".

## Corrections

- none of the slide's content contradicts the guide — every label traces to
  Figure 1-1 / the guide text.

## [?] Uncertain items

- [?] "atan1(A,B)" vs "atan⁻¹" vs "atan(A/B)" exact on-frame glyph (see
  above).
- [?] Whether the guide revision the course copied from is TIDUA05 (June
  2015 original) or TIDUA05B (revised March 2025) — the labels are identical
  in both where checked; the B revision is what was downloaded.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows. This
source confirms/corrects DATA and records provenance; it never licenses
inventing or "improving" content the slide doesn't show.
