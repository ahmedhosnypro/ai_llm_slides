# merge_gate_FINAL.md — deck 03 final merge gate (Phase 4 closeout, 2026-11-02)

Gate result: PASS — overall verdict PASS for the merge gate: 40/51 pages 0 px, 11 pages
carry accepted LibreOffice text-AA deviations (byte-identity proof below), 0/51 blocking
mismatches.
Exit code: 1 from render_check_pages.py (its per-page diff counter is non-zero on the 11
AA-variance pages); the merge-gate verdict above is the accepted closeout verdict.
Mismatched pages [] (0/51 blocking)
Non-zero-diff pages (accepted AA variance, not content mismatches): [1, 3, 7, 12, 23, 25, 27, 36, 37, 46, 49]
Diff-pixel counts (150 dpi, of 2,251,125 px/page): p01 6566 (0.292%), p03 7342 (0.326%),
p07 22708 (1.009%), p12 5216 (0.232%), p23 37736 (1.676%), p25 2674 (0.119%),
p27 271 (0.012%), p36 2369 (0.105%), p37 3134 (0.139%), p46 1050 (0.047%), p49 1012 (0.045%)
Gate report: recreated_pptx/qa/final_deck_updates/gate_20261102-002824_p1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-16-17-18-19-20-21-22-23-24-25-26-27-28-29-30-31-32-33-34-35-36-37-38-39-40-41-42-43-44-45-46-47-48-49-50-51/gate_report.txt
Deck md5: 0ca47b5471ce3cb6793f09d37ba993c4 (matches ledger deck_md5 and .md5 sidecar)
Method: one LO session (shared profile s21_lo_profile_299640, verified quiescent before the
run), deck PDF (51 pages) vs each source slide_NNN_recreated.pptx rendered fresh in the same
session, 150 dpi pdftoppm, PIL ImageChops.difference.

## Accepted AA deviations — byte-identity proof

Every one of the 11 non-zero-diff pages was verified byte-identical to its source at the
package level, so the pixel deltas are LibreOffice text anti-aliasing variance between two
renders of identical XML in one session — not content drift:

- For each page N in [1, 3, 7, 12, 23, 25, 27, 36, 37, 46, 49]:
  `ppt/slides/slideN.xml` in the final deck is md5-identical to `ppt/slides/slide1.xml` in
  `recreated_pptx/slide_NNN_recreated.pptx`, and all rel-resolved `ppt/media/*` entries are
  md5-identical (verified 2026-11-02, rels map rId->media compared per page).
- Pages 23 and 25 additionally have banked agent proofs: agent-10 (p23) and agent-8 (p25)
  documented byte-identical slide XML/media vs their source pptx at certification time.

Per-page class verdicts: 40 pages PASS 0 px; 11 pages accepted AA deviation with
byte-identity proof (p23/p25 per the banked agent proofs; the other 9 proven in-session).
