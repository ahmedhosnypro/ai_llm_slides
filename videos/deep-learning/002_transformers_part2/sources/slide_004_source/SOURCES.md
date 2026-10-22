# SOURCES.md — slide 004 "Encoder – Decoder Transformer" (Figure 1, plain + recolored recap)

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`
(web-verified analysis mandatory). Written 2026-10-11 by the Part II web-verification
worker.

## Slide identity

- Frame `unique_slides/slide_004.jpg`, badge numeral **4** (matches file id).
- **Cross-video child: 4 ← 001:15 AND 001:18** (`slide_dependencies.json`) — recap
  of Part I's Encoder–Decoder Transformer slide(s). Per the cross-video recap rule,
  the primary provenance is 001's records; only NEW visual differences were
  re-verified here.

## Vision transcript of record

- `transcripts/slide004_vision_2026-10-11.txt` — ONE default-route (`images`) probe,
  `--thinking high --max-tokens 65536`, via `scripts/16_vision_gate.sh`; winner
  `images (round 1, attempt 1)`, degenerate events 0. Cross-checked against the
  pre-existing script-12 raw `analysis/slide_004_raw.json` — consistent.

## Primary source

- **arXiv 1706.03762v7 "Attention Is All You Need" (Vaswani et al., 2017) — Figure 1**
  "The Transformer - model architecture." — ALREADY BANKED, do not re-download:
  `../001_transformers_part1/slide_18_source/The Transformer - model architecture..png`
  (1520×2239), sha256-verified byte-identical to
  https://arxiv.org/html/1706.03762v7/Figures/ModalNet-21.png on 2026-10-11
  (fleet SOURCES_MAP Part II header). agy re-confirmed the asset URL same day
  (`scratch/agy_s004_005.txt`).
- **001 records referenced**: `../001_transformers_part1/slide_015_source/SOURCES.md`
  (same plain + recolored composition) and
  `../001_transformers_part1/slide_18_source/SOURCES.md` (figure bank provenance).

## Figures used by this slide

- **Figure 1 ONLY** (no Figure 2 left/right on this slide). Left panel = the paper's
  Figure 1 rendering (white panel, thin black border); right panel = the SAME
  topology redrawn in the course's style (green-bordered container; orange/peach
  "Encoder" zone + green "Decoder" zone, red-italic/green-italic zone labels).
- Per the 001 family mandate ("slides 14/15 MUST use the downloaded images"), the
  build for this recap should embed/reference the banked Figure 1 for the plain
  copy; the recolored copy is the course's redraw (topology = paper's, pixels =
  course's).

## Composition match vs 001:15 (parent)

- MATCHES: Figure 1 shown twice (plain → recolored), large red right-pointing
  transition block arrow between the panels, recolored copy carries exactly TWO
  small red up-arrows (one beside "Inputs", one beside "Output Probabilities"),
  full label set (Output Probabilities/Softmax/Linear/Add & Norm ×5 per panel/
  Feed Forward/Multi-Head Attention/Masked Multi-Head Attention/Nx ×2/Positional
  Encoding ×2 with sinusoid icon + ⊕/Input & Output Embedding/Inputs/Outputs
  (shifted right)), encoder→decoder cross-connection into the decoder's
  Multi-Head Attention (K/V).
- **NEW vs 001:15's record**: the recolored copy carries **two semi-transparent
  orange highlight rectangles** over the encoder's attention block and the
  decoder's Multi-Head (cross) Attention block (probe + raw both see them;
  001:15's SOURCES.md does not record highlights). Either a Part II teaching delta
  (previewing "both blocks contain multi-head self attention", which slide 005
  then details) or an omission in 001's record. Frame wins for recreation;
  recorded as a visual difference, not a data discrepancy.

## What the source CONFIRMS / CORRECTS

- CONFIRMS: topology and labels = paper Figure 1 exactly (per-figure use unchanged
  from 001's verification: per panel 5× Add & Norm, 2× Feed Forward, 2× attention
  + 1× masked; Nx brackets; shifted-right outputs; Linear→Softmax→Output
  Probabilities).
- CORRECTED/flagged [?]: right-panel encoder block spelling — probe reads
  "Multiheaded Attention" (course redraw spelling), raw reads "Multi-Head
  Attention"; on the left (paper-figure) panel the two reads also disagree
  (probe "Multiheaded", raw "Multi-Head"). The verbatim paper Figure 1 reads
  "Multi-Head Attention" (hyphenated) in all three attention blocks, so the left
  panel's probe reading is most likely a small-text misread. **Build-time
  micro-label re-check at zoom required for the right panel; frame wins.**
- No equation content on the slide ("Nx" repetition notation only).

## [?] Uncertain items

- [?] Right-panel encoder block spelling ("Multiheaded" vs "Multi-Head") — build-time zoom re-check; no patch.
- [?] Whether the orange highlight rectangles exist on 001:15's frame too (not
  re-probed there — out of this run's scope; 002's frame is ground truth for 002).

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows; the banked paper
figure confirms topology/data and carries the build's source image. Discrepancies
are recorded above, never silently "fixed".

## Script-12 raw cross-check (raw-verification worker, 2026-10-11)

- `analysis/slide_004_raw.json` re-read in full (model `images`; old extraction 3;
  kept_frame frame_00030, 15 frames). Fully consistent with this record,
  including the record's NEW-vs-parent finding: raw independently describes BOTH
  semi-transparent orange highlight rectangles (encoder MHA + decoder MHA/Masked
  MHA) and the captured cursor over the encoder's attention block [?].
- **[?] RESOLVED (spelling)**: raw's label list reads "Multi-Head Attention
  (x1 per diagram, encoder column; x2 total)" — i.e., the script-12 raw reads the
  PAPER spelling "Multi-Head Attention" on BOTH panels. The probe's "Multiheaded"
  is now the lone dissenting read (raw + banked paper Fig 1 agree). Treated as
  resolved toward "Multi-Head Attention"; the standing build-time zoom glance may
  confirm at zero cost.
- Raw refinements: "Output Probabilities" printed above Softmax in BOTH diagrams;
  "Nx" appears twice per diagram (one beside each stack; 4 total across both
  panels) — consistent with the record's label set, stated per-panel.
- Script-13 final: NOT YET LANDED for 004. Corrections: none yet — verify against
  script-13 final when it lands.
