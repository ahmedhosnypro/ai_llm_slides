# Addendum — waves 3, 4, 5 (2026-10-25)

This addendum extends `DOC_PARSE_EFFECTIVENESS_REPORT.md` (waves 0–2) with the
three later waves of run_20261025-024314. It is appended at the end of that
report at delivery time; this file is its working copy. Wave-2 scores and the
recall formula `(exact + normalized + 0.5·partial) / gt_total` remain frozen
and immutable; every number below is traceable to banked transcripts.

---

## W3. Wave 3 — does the 9000-token ceiling change anything? (user-directed)

Question: the API supports up to 9000 output tokens. Does raising the budget
from the 1024-token default unlock more slide content?

Method: one primary parse per slide at `--max-output-tokens 9000`
(`03_parses/slide_NNN/call05_t9k/`, config-default everything else), one retry
where the protocol allowed it (037, 057 → `call06_t9k_retry/`), compared
byte-level against the frozen wave-2 passes (`call01_pass1` @1024,
`call02_pass2` @3000) and re-scored against the same GT inventories. Details:
`05_comparison/slide_NNN_t9k_delta.md`; returns banked in
`02_worker_logs/agent-{8,9,10,11}_slide_NNN_t9k_return.md`.

| slide | t9k vs 1024/3000 passes | t9k recall | frozen wave-2 | delta | verdict |
|---|---|---|---|---|---|
| 037 | byte-identical to the 3000 minimal read; the rich 79.3% read exists ONLY at 1024 | 6.9% | 79.3% | −72.4 pp (regression) | MORE BUDGET ≠ MORE CONTENT |
| 052 | three-way byte identity (1024=3000=9000); self-stop at 145 tokens ≪ 9000 | 75.0% | 75.0% | 0.0 pp | ceiling not binding |
| 057 | byte-identical loop (`Decoder` ×3000 tail); finish=length on BOTH t9k calls | 12.5% | 12.5% | 0.0 pp | loop is budget-independent |
| 059 | triple byte identity; self-stop at 119 tokens ≪ 9000 | 58.7% | 58.7% | 0.0 pp | ceiling not binding |

**Wave-3 verdict (all corroborated):** the output ceiling is **not binding**
anywhere. Zero new strings on all four slides. On 052 and 059 the model
*chooses* its summary depth and stops voluntarily at 119–145 tokens no matter
the allowance. On 037 the extra budget is actively harmful (rich reads live
only at 1024). On 057 the repetition loop is a *generation-side* failure — it
burns any budget given. Practical rule for slide work: keep the config default
(1024); raising `--max-output-tokens` buys cost, not information. The one
open question — whether the 057 loop can be escaped by *input-form* change —
is exactly what wave 5's crop cascade tests.

---

## W4. Wave 4 — visual-judge-driven improvement loop (multi-round)

User requirement: use the visual-judge skill over **more than one round** to
improve the prompts so the doc-parse pipeline catches more details, with every
round's prompt, transcript, and ledger row banked. Four scopes ran
(`10_visual_judge/slide_NNN/`); each improved prompt round feeds targeted
crop parses, re-scored against the frozen GT inventories.

Per-slide judged arc (union recall, frozen formula):

| slide | round 1 | round 2 | round 3 | crop-parse calls | verdict arc |
|---|---|---|---|---|---|
| 057 | 12.5% → 33.3% | 46.9% | — | 12, all finish=stop | FAIL → FAIL (deficit shrinks each round; loop-escape proven) |
| 052 | 75.0% → 84.1% | **97.7%** | (final leg INCOMPLETE, honestly labeled) | 12, all EXIT 0 | **FAIL → PASS** |
| 037 | FAIL (15-defect banked) | BLOCKED (window wedge) | prompt-split v2.1: 4/4 hangs — size hypothesis REFUTED | 8, all EXIT 0 | round-1 FAIL banked; crop channel reached 29/29 |
| 059 | FAIL (textless-row + 1C1/1C2 classes) | BLOCKED (window wedge, 8/8 A/B-proven) | — | 4 (crop04 faithful-empty = correct) | round-1 FAIL banked; prompts v2+v2.1 banked |

**What multi-round prompt improvement bought (where the loop completed):**

1. **The judge as targeting instrument (052).** Round 1 asked "what does the
   transcript miss?" (broad audit → 15-row defect list, FAIL). Round 2 asked
   "where exactly are the remaining glyphs — give me crop boxes" → its
   proposals directly defined the two tight crops that recovered `K` and `V`,
   the strings round 1's wider crops missed. Judged-arc improvement
   **+13.6 pp**; total **+22.7 pp**. The remaining 0.5 weighted unit (`Y` row,
   digit-hallucinated as `Y0`/`Y2` by doc-parse) is parked, labeled.
2. **Crop parsing escapes the repetition loop (057).** Full-frame:
   6/6 calls `finish=length` (`Decoder` ×482–×4489). Crops: 12/12
   `finish=stop`. The loop is a **full-frame phenomenon**, not a budget
   problem — the single most actionable wave-4 finding.
3. **Prompt design converged on the same lesson in every round:** doc-parse's
   own prompt is NOT editable (wire contract carries `decoding` only). All
   gains come from **input-form engineering** (judged-defect-targeted PIL
   crops, LANCZOS 3×, ≤1664×2048) + **judge-driven targeting** — the
   improvement loop's product is better *crops and verdicts*, not a better
   parse prompt.
4. **Request-class wedge discovered (037/059, evening window).** After
   ~20:00 EEST the Tier-2 vision gateway wedged on **audit-class requests**:
   037's 10.8 KB full-frame judge prompt hung 4/4 across two sessions
   (RC=124 @420 s, zero stream deltas); 059's 6.4–9.8 KB prompts hung 8/8;
   and 037's prompt-split v2.1 (~3.5 KB) sub-calls then hung 4/4 —
   **refuting the size hypothesis**. Controls: ≤93 B probes served 4/4, and
   the same lane served a full-frame audit in 13.4 s at 08:16 and all
   morning/afternoon judge legs. All 12 heavy-call hangs sit 20:0x–22:2x
   EEST → a **time-window-correlated request-class wedge** at the serving
   layer, not the route, not the prompt. The sanctioned countermeasure is
   banked and byte-frozen (v2.1 split sub-calls, no redesign needed): re-run
   them in a different load window, then raise the gateway-owner streaming
   question. No verdict was fabricated for any blocked leg; both scopes
   closed `failed` with exhausted budgets and honest debt labels.

**Reliability summary for the wave:** every round prompt, transcript, call
log, and ledger row is banked per slide (`judge/`, `parses/`, `ledger.md`);
incomplete or blocked legs carry honest INCOMPLETE/BLOCKED labels with retry
recipes — nothing was silently dropped, and no blocked read was counted as
evidence.

## W5. Wave 5 — parse-driven recursive crop cascade

User requirement (recorded verbatim in `MISSION_PROTOCOL.md` WAVE-5 ADDENDUM):
crop **every** class block doc-parse returns, rerun a judge over each crop,
recurse into nested picture blocks until a crop's description "means nothing
more to crop", track every crop's position so the final composition is
accurate, and run **parallel script calls inside a single subagent**
(bash `&` + `wait`, ≤4 concurrent). The first wave-5 run (v1, `11_cascade/`)
partially missed the requirements; per the user's verdict it was kept running
as **supporting evidence** while a requirement-compliant rerun (v2,
`12_cascade_v2/`) became the **authoritative** record. Both trees are complete
and closed.

Per-slide union recall (formula frozen from wave 2; GT 29/22/48/46):

| slide | frozen wave-2 | v1 cascade (`11_cascade/`) | v2 cascade (`12_cascade_v2/`, authoritative) |
|---|---|---|---|
| 037 | 79.3% | **100%** (29/29; 8 crops, 9 calls, ~1.7×) | **100%** (29/29; 7 crops L1→L3, 7 calls + 5 judges, ~2.5×; 2 hallucinations caught) |
| 052 | 75.0% | 86.4% transcript (19/22) / **100% judge-corroborated**; 12 crops, 12 calls, ~2.7× | **90.9% transcript / 100% judge-corroborated** (16 crops, 17 calls, ~2.5×) |
| 057 | 12.5% | **49.0%** (23.5/48; 16 crops [cap], 17 calls, ~2.3×) | **61.5%** (16 crops, 19 calls, ~2.4×; all finish=stop) |
| 059 | 58.7% | 88.0% (40.5/46; 16 crops, 21 calls, ~2.7×) | **100%** (46/46; 16 crops L1→L3, 16 calls + 13 judges, ~2.6×) |

**Cascade findings (corroborated across both variants):**

1. **Crop parsing kills the full-frame failure modes.** On 057 the full-frame
   `Decoder` repetition loop (`finish=length`, ×482–×4489 tails, budget-
   independent per wave 3) does not survive region-targeted input: 12/12 v1
   crop calls and 19/19 v2 calls finished `finish=stop`. On 059 the wave-2
   `1C1/1C2` leading-`1` hallucination dies at crop scale (lollipop-marker
   misread). Crop parsing buys TEXT, not geometry — corner coordinate
   artifacts persist on every crop (`x_0/y_0 ↔ x_0.999/y_0.999`).
2. **The anchor law.** Anchor-less strips return empty `<class_Picture>` +
   corner coords; a readable in-crop anchor (e.g. the "Word Embedding" title
   on 057) unlocks the neighboring target rows. But an anchor can also crowd
   out the target (057 crop06: chart scaffold around the embedding title).
3. **Doc-parse's hard floors.** 15–22 px K/V/Q/Y glyphs (052) are invisible at
   full-frame at ANY budget and at multi-element crop scales; only
   near-single-glyph crops partially escape, while the vision judge reads
   every glyph cleanly from the same frame. ≤4 px serif subscript digits
   (059 X₄/X₅/Y₀/Y₁) are unrecoverable by doc-parse at any scale — judge-
   confirmed REAL, parked as the deficit.
4. **Textless-region structural omission.** 059's 20-cell table row is
   faithfully parsed as `<class_Picture>` with corner coords and zero text
   tokens — the region is detected, its textlessness is not represented.
   A compliant crop re-parse returns the same faithful-empty result.
5. **Hallucination control improves with scale.** v1 037: every novel string
   was adjudicated to a real GT label or killed (`Aad & Norm`→`Add & Norm`
   misread, `Multi-lead`/`Fixed Forward` garbles); 0 hallucinations survived
   judging. 037's one true blind spot: `Probabilities` (printed, unreadable
   by doc-parse even at 3× crop zoom).
6. **Recursion semantics.** Crops recurse until a semantic stop: `leaf`,
   `no-internal-structure`, `too-small`, `no-new-information`, or the ≤16
   crops / ≤24 calls backstop. v1 037 stopped purely semantically (leaf ×1,
   no-internal-structure ×1, recursed ×3, no-new-information ×3); v1 057/059
   and all v2 slides reached the 16-crop cap with per-node stop reasons in
   every manifest. Stop reasons are recorded per node; no null boxes.
7. **Parallelism works.** In-subagent parallel parse calls (`&`+`wait`, ≤4
   concurrent) deliver **2.3–2.9× wall-clock speedup** measured from call.log
   timestamps (e.g. v2 037 batch1: 38 s summed vs 13 s wall = 2.9×; v1 059:
   126 s serial vs 46 s batched = 2.7×), with one caveat: the vision-judge
   legs are sequential (one in flight) and dominated v1 059's closing wall
   (92 min for 14 judges).
8. **Position tracking enables accurate composition.** Every crop carries
   box_frame_px + scale + a crop→frame transform; the composed files
   (`compose/COMPOSED_ANALYSIS.md`) merge full-frame + all crop transcripts
   into one y-ordered, per-element classified (REAL / NOT-IN-GT / GT-gap),
   provenance-carrying inventory — the accurate multi-file→one-file
   composition the requirement asked for.
