# SOURCES.md — 002 slide 060 "What is Next (as of 2020)" (closing reading list)

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`
(web-verified analysis mandatory). Machine-verified 2026-10-11 by the Part II
web-verification worker: vision transcript banked
(`transcripts/slide_060_vision_2026-10-11.txt`, default `images` route, one
probe, `--thinking high --max-tokens 65536`, via `scripts/16_vision_gate.sh`).
This slide CITES its own sources — each citation was verified live against
arXiv / Wikipedia this session (openai.com itself Cloudflare-blocks bots;
blocked fetches noted below).

## Slide identity

- Video-2 (002_transformers_part2) curated slide **060** ← old extraction
  slide **150** (`unique_slides/new2old_mapping.json`), frame
  `unique_slides/slide_060.jpg` (kept from t≈5440 s; shown 5128–5439 s =
  312 frames — the lecture's long closing summary), badge numeral 60.
- Content (banked vision transcript): title verbatim **"What is Next  (as of
  2020)"** (two spaces before the parenthetical). One blue-outlined white
  container with six entries (model name + underlined citation lines, as
  printed):
  1. **"GPT-1 and GPT-2 (Generative Pre-trained Transformers)"** — "Radford
     et al., OpenAI. June 2018 and February 2019."
  2. **"BERT (Bidirectional Encoder Representations from Transformers)"** —
     "Devlin et al., Google AI Language. May 2019."
  3. **"RoBERTa (Robustly Optimized BERT Approach)"** — "Liu et al.,
     Facebook AI. June 2019."
  4. **"Transformer-XL: Attentive Language ModelsBeyond a Fixed-Length
     Context"** (run-together "ModelsBeyond" as printed) — "Zhang Dai et al.
     Carnegie Mellon University and Google Brain".
  5. **"T5 (Text-to-Text Transfer Transformer)"** (no citation line).
  6. **"GPT-3 (175 Billion Parameter, Beta Release June 2020)"**.
- Live cursor artifact near the T5/GPT-3 lines; bottom black strip = video
  letterboxing.

## Citation verification table (live fetches 2026-10-11)

| Slide entry | Verified source (URL fetched live) | Verified facts | Slide-vs-source note |
|---|---|---|---|
| GPT-1 (Jun 2018) | https://en.wikipedia.org/wiki/GPT-1 (openai.com blocked bots) | OpenAI, June 2018, paper "Improving Language Understanding by Generative Pre-Training" (Radford, Narasimhan, Salimans, Sutskever) | CONFIRMED |
| GPT-2 (Feb 2019) | https://en.wikipedia.org/wiki/GPT-2 | Release 14 February 2019; paper "Language models are unsupervised multitask learners" (Radford, Wu, Child, Luan, Amodei, Sutskever) | CONFIRMED |
| BERT "May 2019" | https://arxiv.org/abs/1810.04805 | Devlin, Chang, Lee, Toutanova (Google AI Language); arXiv v1 11 Oct 2018, **v2 revised 24 May 2019**; published NAACL 2019 | CONFIRMED under the charitable reading (slide's "May 2019" = the v2 revision month; original Oct 2018) |
| RoBERTa "June 2019" | https://arxiv.org/abs/1907.11692 | Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike Lewis, Luke Zettlemoyer (Facebook AI); arXiv **26 Jul 2019** | DISCREPANCY (minor): slide says June 2019, arXiv stamp is July 2019. Slide wins for recreation; record for understanding |
| Transformer-XL | https://arxiv.org/abs/1901.02860 | Title exact ("Beyond a Fixed-Length Context"); arXiv 9 Jan 2019 (v3 2 Jun 2019); authors **Zihang Dai**, Zhilin Yang, Yiming Yang, Jaime Carbonell, Quoc V. Le, Ruslan Salakhutdinov — CMU + Google Brain | DISCREPANCY (name): slide's "Zhang Dai" — first author is **Zihang** Dai. Affiliations CONFIRMED. Slide wins for recreation |
| T5 | https://arxiv.org/abs/1910.10683 | "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer", Colin Raffel et al. (Google), arXiv 23 Oct 2019 / JMLR 2020 — the T5 paper behind the slide's name | CONFIRMED (slide shows no citation line; recorded for understanding) |
| GPT-3 175B, beta Jun 2020 | https://arxiv.org/abs/2005.14165 + https://en.wikipedia.org/wiki/GPT-3 | "Language Models are Few-Shot Learners", Tom B. Brown et al., arXiv 28 May 2020; **175 billion parameters**; **OpenAI API beta June 11, 2020** | CONFIRMED |

- openai.com direct fetches returned Cloudflare bot-stubs (noted, not cited);
  Wikipedia article text carried the needed primary facts.
- BERT was already verified earlier this session for the 058 record (same
  arXiv page); the rest were fetched fresh for this slide.

## Figures downloaded

- None: the slide is a plain text list (no figures to source).

## What the source CONFIRMS / CORRECTS

- CONFIRMED: all six model families, their inventors/institutions, the
  GPT-1/GPT-2 dates, BERT's authorship+institution, Transformer-XL's title
  and affiliations, GPT-3's parameter count and June-2020 beta.
- CORRECTED (recorded; slide wins for recreation per fidelity law):
  RoBERTa arXiv date is 26 Jul 2019, not June 2019; Transformer-XL first
  author is Zihang Dai, not "Zhang Dai"; BERT's original release was
  Oct 2018 (May 2019 = v2 revision/NAACL cycle). These are the slide's own
  simplifications — do not "fix" them on the recreation.

## [?] Open questions

1. Whether the intended BERT date reference was NAACL 2019 (conference held
   June 2019) rather than the arXiv v2 (May 2019) `[?]` — either way the
   slide's "May 2019" stays as printed.
2. The exact run-together "ModelsBeyond" spacing — frame-level (transcript
   flags it as printed with no space) `[?]`.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what each slide shows; web
sources confirm/correct data and provenance, never license inventing content.
`[?]` markers are removed only with a confirming URL recorded here.
