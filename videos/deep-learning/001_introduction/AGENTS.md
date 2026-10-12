# AGENTS.md — 001_introduction (Introduction — Deep Learning DSAI 308)

## Curation record (2026-10-12) — the state of record

The founder reviewed the 80-group review packet and curated the deck to **49 slides**
(dense renumbering; blank transitions and annotation-state duplicates culled). Curation
metadata rebuilt from content hashes:
- `unique_slides/slides_index.json` — 49 entries (old_group, kept_frame, founder swaps).
- `unique_slides/new2old_mapping.json` — new→old mapping; 5 founder frame swaps recorded
  (new 22←old27, 23←old28, 35←old43, 36←old48, 48←old79); no group splits.
- `unique_slides/slides_index_old80.json` — pre-curation index, preserved.
The HARD STOP for this video is LIFTED. The law itself still binds every future extraction.

## Web-verified analysis is MANDATORY (playlist precedent — 001_transformers_part1's founder directive applies here)

For EVERY slide's analysis (script 12), validation (13), recreation, and QA: websearch
the primary source (`agy -p "<query>"`; on 401/403 mint with `agy -p "hi"` then retry),
webfetch it, download the site's own figures when they exist into `slide_NNN_source/`,
and write `SOURCES.md`. **No SOURCES.md = the research step did not happen.** Vision work
runs through `.agents/skills/image-analysis` (banked `.txt` transcripts). Research
fleets bank per slide, atomically (SOURCES.md via temp name → move), staggered — never
all-at-once into a storming provider.

This deck's likely sources: classic ML/CNN references — Rosenblatt perceptron, McCulloch-
Pitts, LeCun LeNet/CNN gradient learning, Sobel filters, zero-padding/stride/pooling
formulas (e.g. CS231n), UDL book. Confirm per slide; never invent.

## House chrome — playlist law binds (founder directive 2026-10-11)

Every recreated slide uses the PLAYLIST chrome measured from
`../001_transformers_part1/unique_slides/slide_001.jpg`:
`../shared_patterns/house_chrome.js` (`drawHouseChrome(pptx, slide, {numeral})`) — import
it, never re-draw. Run `../shared_patterns/house_chrome_check.py` on every 150dpi
render pre-judge. Binding values in `../AGENTS.md`.

**Badge numeral — assumption PENDING FOUNDER VETO (2026-10-12):** this lecture's original
frames carry NO yellow badge and NO printed slide numbers (PIL-probed, 2026-10-12). The
playlist law still mandates the badge on every recreated slide; the numeral is therefore
the slide's own file number (dense 1..49, no zero-padding). If the founder vetoes badges
on this deck, rebuilds drop the badge ONLY via shared_patterns (never per-slide edits).

## Slide dependency graph & shared component builds (founder directive 2026-10-12)

`slide_dependencies.json` is canonical (also DB `depends_on`). Edges (child ← parent):
16←9, 17←16, 18←9, 19←9, 25←24, 37←36, 41←35.

- Builds gated on parent certification (`gen_status=passed` AND `visual_check=PASS`);
  analysis (12) and validation (13) never gated. Siblings unblock together (9's
  certification unblocks 16/18/19; 36's unblocks 37; 35's unblocks 41; 24's unblocks 25;
  16's unblocks 17 — note 17 is a GRANDCHILD via 16, so building it needs both 16 and,
  transitively, 9 certified).
- Child builds IMPORT the parent's certified composition from
  `recreated_pptx/build/components/slide_NNN.js` (u-components model) and draw only
  their measured delta. Components are certified single-source-of-truth; editing one
  re-opens its descendant subtree.
- **Slide 37 (founder note): the original has a content-crowding issue.** Build its
  delta deliberately to resolve crowding per founder intent; document any intentional
  layout deviation in the build report + judge ground rules.
- Chains: 17←16←9 composes transitively (17 imports 16's component, which imports 9's).

## Deck character (drives build strategy)

Heavy live-stylus lecture: many slides are hand-drawn/hand-annotated diagrams
(perceptron sketches, conv arithmetic, pooling). Ink forensics (PIL measured geometry)
and the equation laws apply unchanged — hand-drawn ≠ imprecise. Several content-slide
families are annotation states of one base diagram (see dep graph). Small-text color
claims settle via pixel column-profiles, never full-slide vision reads.
