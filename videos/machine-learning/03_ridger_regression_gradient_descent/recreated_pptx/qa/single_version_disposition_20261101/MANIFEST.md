# MANIFEST — single-version disposition, deck 03 (2026-11-02)

Phase-4 closeout step G. Non-plain-named slide artifacts moved (never deleted)
from `recreated_pptx/` into this directory. The single-version law is preserved:
exactly one `slide_NNN_recreated.pptx` per slide remains in `recreated_pptx/`.

| File | Bytes | Moved from | Reason |
|---|---|---|---|
| slide_015_recreated_v2.pptx | 546389 | recreated_pptx/ | superseded variant of slide 015 |
| slide_015_recreated_v3.pptx | 578060 | recreated_pptx/ | superseded variant of slide 015 |
| slide_014_recreated.pptx.bak_prefix3 | 183393 | recreated_pptx/ | pre-prefix backup of slide 014 |
| slide_015_recreated.pdf | 621624 | recreated_pptx/ | stray render of slide 015 |
| slide_015_recreated_v2.pdf | 524411 | recreated_pptx/ | stray render of v2 |
| slide_015_recreated_v3.pdf | 527930 | recreated_pptx/ | stray render of v3 |
| slide_025_recreated.pdf | 596975 | recreated_pptx/ | stray render of slide 025 |

Post-move sweep: `ls recreated_pptx/slide_*` filtered to non-plain names →
"single-version clean" (only `slide_001..051_recreated.pptx` remain).
