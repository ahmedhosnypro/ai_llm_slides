#!/usr/bin/env python3
"""
analyze_image.py — race all configured vision models against each other over a
local OpenAI-compatible endpoint and print the first WORKING response.

Strict 4-mode CLI (see --help for the full menu):
    analysis    — EXACTLY ONE image, one prompt.
    comparison  — EXACTLY TWO images, ONE API request containing both.
    batch       — ANY number of images, ONE shared prompt, ONE API request.
    per-image   — image+prompt pairs + a master prompt; each image gets its OWN
                  sequential API request (pacing discipline).

Wrong or missing arguments print the FULL help menu and exit 2.
Exit code: 0 if every image got a working response, 1 otherwise.

Founder defaults (2026-09-28, w5-script-patch — DEFAULT behavior, not flags):
every gateway request runs with thinking/reasoning DISABLED and `stream: true`
(no tokens/time are ever spent on thinking; streamed answers cannot outlive
the hard wall-clock deadline). Default route: the `images` alias (gateway
combo incl. `nvidia/nvidia/ising-calibration-1.5-31b`). Slow-but-good routes
(`nvidia/z-ai/glm-5.3-flash`, ~180s floor) fit the default 600s timeout.
gemini/claude routes stay accepted by --models but are FOUNDER-BANNED for
lane pinning.
"""

import argparse
import base64
import json
import mimetypes
import os
import queue
import re
import sys
import threading
import time
from collections import Counter

import requests

try:  # A4a (wave-5 amendment, 2026-09-28): pixel-level full-page tier
    from PIL import Image  # detection — guarded; the --capture metadata
except ImportError:  # path works without PIL, and the tier then defaults
    Image = None  # to normal (conservative: no tag, no bonus retry)

HERE = os.path.dirname(os.path.abspath(__file__))
KEY_FILE = os.path.join(HERE, ".analyze-image-key")
ENDPOINT = "http://localhost:17844/v1"

DEFAULT_MODELS = [
    "images",
]

DEFAULT_PROMPT = (
    "You are a meticulous visual QA analyst. Describe this image factually and completely:\n"
    "1. Transcribe ALL visible text verbatim, preserving the original language, digits, and punctuation.\n"
    "2. Describe the layout: what sits at the LEFT edge, RIGHT edge, top, and bottom of the image as seen.\n"
    "3. Note any visual defects: clipped or cut-off content, overlapping elements, placeholder or garbage "
    "strings, or wrong-language text where it does not belong.\n"
    "Do not speculate beyond what is visible; if something is illegible, say so."
)

COMPARISON_PROMPT = (
    "You are a meticulous visual QA analyst comparing two images shown in order "
    "(first = image 1, second = image 2).\n"
    "1. Transcribe the key visible text of each image verbatim, preserving language and punctuation.\n"
    "2. List the SIMILARITIES: shared purpose, layout regions, components, and styling.\n"
    "3. List the DIFFERENCES: content, layout, spacing, colors, typography, and defects present in "
    "only one image (clipping, overlap, placeholders, garbage strings, wrong-language text).\n"
    "4. Verdict: which image is BETTER and why, citing concrete visual evidence.\n"
    "Do not speculate beyond what is visible; if something is illegible, say so."
)


def load_key():
    """Return the API key from the gitignored file beside this script, or None."""
    try:
        with open(KEY_FILE, encoding="utf-8") as f:
            key = f.read().strip()
    except OSError:
        return None
    return key or None


def encode_image(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"


class HangError(RuntimeError):
    """A call exceeded its HARD wall-clock deadline (stuck request / runaway
    thinking stream that keeps bytes trickling past the read-timeout). The
    attempt is aborted and retried — see HARD_RETRY_CAP."""


class GarbageError(RuntimeError):
    """The response (or its thinking/reasoning stream) is degenerate: infinite
    repeatable text, all-bang bodies, or one line dominating the output.
    Learned from round-1 view-analysis lane stalls (2026-09-26): the default
    model can emit a thinking stream of endlessly repeated garbage — in the
    THINKING part, not the answer — hanging or flooding the race. The call is
    aborted and retried up to HARD_RETRY_CAP times."""


class EmptyStreamError(RuntimeError):
    """HTTP 200 with NO content deltas at all (the combo alias's transient
    empty-stream hiccup under gateway load — observed by the w5-script-patch
    certificate as a non-degenerate `empty content` retry and by the
    w5-regrade-ao-v2 lane as a fleet-storm failure class). NOT a degenerate
    body (no garbage tally): the attempt is aborted and retried on the same
    abort ladder as hang/garbage, up to HARD_RETRY_CAP times — a single
    empty stream must not kill an otherwise healthy call at --tries 1."""


HARD_RETRY_CAP = 3  # abort-and-retry budget for hang/garbage/empty-stream per invocation

# A4a (wave-5 amendment, 2026-09-28): full-page captures are the degenerate-
# prone tier — every round-1 default-model degenerate was a full-page variant
# while normal-viewport invocations went 10/10 winners (round1/script-
# proposals.md:234-239; round1/SYNTHESIS.md:79; wave3/wizard-outcome.md:90;
# wave4/welcome-outcome.md:286-289). Tag the tier in the [info] stream and
# grant it ONE pre-emptive retry allowance; normal-viewport captures behave
# exactly as before.
FULL_PAGE_MIN_CSS_H = 1600  # >=~1600 CSS px tall = the full-page tier
FULL_PAGE_TRIES_BONUS = 1   # the pre-emptive extra retry allowance for that tier

_BANG_RE = None  # compiled lazily

# w5-script-patch-v2 (2026-09-28): THOUGHT-CHANNEL TOKEN LEAK — live 4-parallel
# verification on the `images` alias (w5-script-patch/parallel-1.txt and -3)
# caught a residual degenerate class the repetition gates cannot see: the
# answer opens with "§1 Layout map" then the literal chat-template tokens
# `<|channel>thought` / `<channel|>` appear INSIDE the content and the body
# continues as a leaked thinking channel (a JSON dump of the screen) — the
# actual answer never materializes. The thinking-disable block does not stop
# this member from emitting its channel markers into the content stream.
# Any leaked channel/thought template token marks the body as leaked
# thinking, not an answer: abort + retry (GarbageError ladder), win or lose.
_LEAKED_CHANNEL_RE = re.compile(
    r"<\|?\s*channel\s*\|?>|<channel\|>|<\|thought|<\|\s*end", re.IGNORECASE)


# w5-script-patch-v3 (2026-09-28 overnight, echo-class validator — routed from
# two lanes): the `images` alias's ising member can answer with ECHO-CLASS
# degenerate bodies that every repetition/bang gate lets through: the content
# is the PROMPT's own glossary / section-header list reproduced verbatim (or
# the audit prompt's numbered section headers with NO section bodies), and the
# body then truncates. `_parrots_prompt`'s single long-span test missed the
# reassembled-glossary shape (several shorter verbatim prompt spans, none of
# them 10 consecutive words) and the header-shell shape (headers are the
# prompt's, bodies absent). `_echo_class_reason` is the consolidated validator
# adding both. Live evidence: route-census images-group.txt (w4-harvest
# glossary repeated verbatim instead of a §1–§9 audit) and w5-script-patch/
# parallel-1.txt (channel leak) — see outcome §1/§5.
_ECHO_LONG_SPAN_WORDS = 10    # one run this long = prompt echo
_ECHO_SHORT_SPAN_WORDS = 6    # glossary echo: SEVERAL distinct runs this long
_ECHO_SHORT_SPAN_COUNT = 3
_SHELL_MIN_HEADERS = 3        # section-header shell: >= this many BARE headers
_SHELL_MAX_BODY_CHARS = 80    # ... and less real section body than this
# w5-vision-hang-probe (2026-09-29): SPAN-COVERAGE GATE for the two span rules.
# The lanes pass the 70 KB `audit-prompt-template.md` (11,302 words), which IS a
# defect VOCABULARY: the model is instructed to reuse its tag names and
# checklist phrasing, so a legitimate audit naturally reproduces many short
# verbatim prompt spans. Measured on the gateway's own call logs (235 real
# `images` HTTP-200 bodies, 2026-09-29T00:20-00:39Z): legit audits cover
# 0.7%-4.9% of their words with prompt spans, while true prompt dumps cover
# 64.5%-77.2% (33 KB bodies, 75-86 long runs) — a 7x separation with nothing in
# between. Rule 1/2 therefore fire only when the copied prompt spans are a
# LARGE fraction of the response (the response IS the prompt), never when the
# response merely references it. Rules 3 (header shell) and 4 (zero section
# coverage) are structural and stay unconditional.
_ECHO_SPAN_COVERAGE_MIN = 0.30


def _norm_words(text):
    """Lowercased alphanumeric word tokens (Arabic range kept) — the shared
    normalization for every echo-span comparison."""
    return re.findall(r"[0-9A-Za-z\u0600-\u06FF]+", (text or "").lower())


def _prompt_runs(prompt, response, min_words, max_words=48):
    """Maximal verbatim runs of `prompt` (>= min_words normalized words)
    reproduced anywhere in `response`, as separate copied passages. Greedy
    left-to-right: at each start the run is expanded while the next prompt
    word still appears in the response, then the run is consumed — so one
    copied passage counts ONCE (an overlapping family of windows is not
    mistaken for many hits), which is what distinguishes a glossary dump
    from a legitimate short heading re-use."""
    pw = _norm_words(prompt)
    rw = " ".join(_norm_words(response))
    if len(pw) < min_words or not rw:
        return []
    runs, i = [], 0
    while i + min_words <= len(pw):
        if " ".join(pw[i:i + min_words]) not in rw:
            i += 1
            continue
        k = min_words
        while (i + k + 1 <= len(pw) and k < max_words
               and " ".join(pw[i:i + k + 1]) in rw):
            k += 1
        runs.append(" ".join(pw[i:i + k]))
        i += k                      # consumed: one hit per copied passage
    return runs


def _is_bare_header(line):
    """True when a single line is a SECTION LABEL with no inline answer, not
    body prose: it opens with a section marker (`#`, `§`, `**`, `*`, or
    `N.`/`N)`) and what is left after the marker is a short (<= 4 word) label
    carrying NO colon-introduced text. This is what keeps the shell rule off
    legitimate bodies: a numbered sentence of real findings
    ('3. The header overlaps the hero and clips the avatar.') and a compact
    label-plus-answer line ('1. Layout map: two panes.') are BODY, while
    '3. Left edge content' / '## Layout map' / '**Verdict**' are labels."""
    s = line.strip()
    if not s or len(s) > 90:
        return False
    m = re.match(r"^(?:#{1,6}\s*|§\s*\d+\s*[.:)]?\s*|\d{1,2}\s*[.)]\s*|\*\*|\*)", s)
    if not m:
        return False
    rest = s[m.end():].strip(" *#:.-—–_[]()")
    if not rest:
        return True                 # "##" / "§1" / "**" with no label text
    if re.search(r"[:\u060C]\s*\S", rest):
        return False                # label + inline answer on one line = body
    return len(_norm_words(rest)) <= 4


def _section_shape(text):
    """(bare_header_count, body_chars) for a response body: how many section
    LABELS it declares and how many characters of genuine section body follow
    (non-label lines with >= 8 chars and at least one alphanumeric). The
    header-shell echo class is 'many labels, no bodies'."""
    headers, body_chars = 0, 0
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if _is_bare_header(s):
            headers += 1
            continue
        if len(s) >= 8 and any(ch.isalnum() for ch in s):
            body_chars += len(s)
    return headers, body_chars


def _required_sections(prompt):
    """The numbered markdown headings a section-structured prompt demands, as
    normalized label phrases ('## 1. LAYOUT MAP' -> 'layout map'; a bare title
    longer than 8 words is not a section). Empty for prompts that demand no
    section structure (e.g. the built-in DEFAULT_PROMPT), which keeps every
    section rule below inactive for them."""
    labels = []
    for line in (prompt or "").splitlines():
        m = re.match(r"^#{1,6}\s*(?:\d{1,2}\s*[.)]\s*)?(.{2,60}?)\s*:?\s*$",
                     line.strip())
        if not m:
            continue
        lab = " ".join(_norm_words(m.group(1)))
        if 1 <= len(lab.split()) <= 8 and lab not in labels:
            labels.append(lab)
    return labels


def _section_coverage_reason(prompt, response):
    """The census-class structural check (w5 v3, evidence-derived): the prompt
    demands N nested sections and the response covers NONE of them — the
    route-census `images` echo (4.1 KB of paraphrased `[w4-harvest]` glossary
    entries, no §1–§9 structure at all) versus every banked real winner
    (2/9 labels covered). Undetectable by verbatim matching: the echo is a
    TRANSFORMED glossary, not copied text. Conservative by construction:
    needs >= 3 required labels, and flags only ZERO coverage — a single
    label mention (or a prompt with no section structure) passes."""
    labels = _required_sections(prompt)
    if len(labels) < 3 or not response:
        return None
    rw = " ".join(_norm_words(response))
    if any(lab in rw for lab in labels):
        return None
    return (f"section-coverage: the prompt requires {len(labels)} sections "
            f"(\"{labels[0]}\" … \"{labels[-1]}\") and the response covers "
            f"NONE of them")


def _echo_class_reason(prompt, response):
    """The consolidated ECHO-CLASS validator (w5 v3; span-coverage gate added by
    lane w5-vision-hang-probe, 2026-09-29). Returns a human reason string when
    `response` is echo-class degenerate, else None. Four rules, in order:

    (1) long verbatim span — any >= 10-word non-overlapping run of the prompt
        reproduced verbatim in the response (the original `_parrots_prompt`
        class: prompt echoed then truncated at max-tokens);
    (2) prompt glossary echo — >= 3 DISTINCT >= 6-word prompt passages copied
        verbatim (the ising glossary dump: many short prompt spans, no single
        10-word run — reassembled/lightly-interleaved prompt text);
    (3) section-header shell — >= 3 bare section labels with < 80 chars of
        actual section body across the whole response (the audit prompt's own
        numbered headers listed with no §-section bodies);
    (4) zero required-section coverage — the prompt demands >= 3 numbered
        markdown sections and the response covers NONE of them (the census
        `images` class: a transformed `[w4-harvest]` glossary dump with no
        §-structure — invisible to verbatim matching, so the structural check
        is the only gate that sees it).

    RULES 1 AND 2 ARE SPAN-COVERAGE GATED (`_ECHO_SPAN_COVERAGE_MIN`): they fire
    only when the copied prompt spans are a LARGE fraction of the response's
    own words, i.e. the body essentially IS the prompt. A body that merely
    REFERENCES the prompt is not an echo — with the 70 KB vocabulary prompt the
    lanes use, legitimate audits measure 0.7%-4.9% span coverage while true
    prompt dumps measure 64.5%-77.2% (235-body live corpus, see the constant).
    Before the gate, rule 2 aborted 67 of 235 real audits (28%) for reusing the
    defect vocabulary the prompt instructs them to use. Legitimate short
    heading re-use ('3. Left edge content: nav rail.') stays far below every
    threshold, gated or not."""
    if not prompt or not response:
        return None
    runs = _prompt_runs(prompt, response, _ECHO_SHORT_SPAN_WORDS)
    resp_words = len(_norm_words(response))
    span_words = sum(len(r.split()) for r in runs)
    coverage = (span_words / resp_words) if resp_words else 0.0
    if coverage >= _ECHO_SPAN_COVERAGE_MIN:
        long_runs = [r for r in runs if len(r.split()) >= _ECHO_LONG_SPAN_WORDS]
        if long_runs:
            return (f"prompt-echo: {len(long_runs)} verbatim prompt span(s) "
                    f">= {_ECHO_LONG_SPAN_WORDS} words "
                    f"(first: \"{long_runs[0][:70]}\"; copied-prompt coverage "
                    f"{coverage:.0%} of the response)")
        if len(runs) >= _ECHO_SHORT_SPAN_COUNT:
            return (f"prompt glossary echo: {len(runs)} distinct verbatim "
                    f"prompt spans >= {_ECHO_SHORT_SPAN_WORDS} words "
                    f"(first: \"{runs[0][:70]}\"; copied-prompt coverage "
                    f"{coverage:.0%} of the response)")
    headers, body_chars = _section_shape(response)
    if headers >= _SHELL_MIN_HEADERS and body_chars < _SHELL_MAX_BODY_CHARS:
        return (f"section-header shell: {headers} section headers but only "
                f"{body_chars} chars of section body (zero section bodies)")
    return _section_coverage_reason(prompt, response)


def _parrots_prompt(prompt, response, min_words=10):
    """w5-script-patch-v2 (adversarial-E v7 finding, 2026-09-28): the
    echo/parroting degenerate class — a response that repeats the PROMPT's
    own instruction language verbatim (observed twice tonight: the default
    route echoing the audit prompt then truncating at max-tokens — it
    passed the repetition gates because the echoed prompt is *varied*
    prose). True when the response reproduces a long verbatim span
    (min_words consecutive normalized words) of the prompt. Short echoes
    (a section heading like "3. Left edge content" the model legitimately
    re-uses as its own heading) stay far below the span threshold.

    Kept as the single-span primitive; `_echo_class_reason` (w5 v3) is the
    consolidated validator that adds the glossary and header-shell shapes."""
    return bool(_prompt_runs(prompt, response, min_words))


def _looks_like_garbage(text):
    """True when text is degenerate: massively repeated substrings, one
    dominant repeated line, an all-bang body (the classic gateway family), or
    a body that opens legitimately then degenerates (the short-garbage-winner
    leak, r2-models-1 5th instance: a ~57-char body of a real heading plus a
    `1!!!!` loop escaped every whole-body gate)."""
    if not text:
        return False
    # Length gate lowered 50→16 (r1 settings-rescue finding: 32-char all-bang
    # bodies slipped through) — short degenerate bodies are still garbage.
    if len(text) >= 16 and text.count("!") * 5 >= len(text) * 4:
        return True  # >=80% exclamation marks — the `!!!!!` degenerate body
    # Per-line bang scan at ANY body length: one degenerate line inside an
    # otherwise legitimate opening is garbage (the leak body's `1!!!!…` line).
    for line in text.splitlines():
        s = line.strip()
        if len(s) >= 8 and s.count("!") * 5 >= len(s) * 4:
            return True
    # Identical-line repetition at ANY body length (blank and purely
    # structural/punctuation lines excluded — paragraph separators, markdown
    # code fences, HR rules can never trip it): 8+ identical lines carrying
    # at least one alphanumeric character is never legitimate prose.
    contentful = [
        l for l in text.splitlines()
        if len(l.strip()) >= 4 and any(c.isalnum() for c in l)
    ]
    if contentful:
        _top, n = Counter(contentful).most_common(1)[0]
        if n >= 8:
            return True
    if len(text) >= 400:
        scan = text[:20000]
        # any 8–40 char unit repeated consecutively 25+ times anywhere
        if re.search(r"(.{8,40}?)\1{24,}", scan, re.DOTALL):
            return True
        return False
    if len(text) >= 40:
        # Short-body tight-loop scan (units down to 5 chars, 14+ consecutive
        # repeats) — but only when the body already leans degenerate (>=10%
        # bangs), so long markdown rule lines can never false-positive.
        if text.count("!") * 10 >= len(text):
            if re.search(r"(.{5,40}?)\1{7,}", text[:20000], re.DOTALL):
                return True
    return False


def _parse_capture_dims(capture):
    """Extract (max_declared_height_css, scale) from a --capture metadata
    string, e.g. '1440x900 CSS px, 1x scale, app' -> (900, 1.0). Height is
    None when the string declares no WxH pair; scale defaults to 1.0.
    Batch strings declaring several sizes ('4 images: 320x700, ... 768x900
    ...') report the tallest — the tier question is 'is ANY of this full-page'."""
    height, scale = None, 1.0
    if not capture:
        return height, scale
    m = re.search(r"(\d+(?:\.\d+)?)\s*x\s*scale", capture, re.IGNORECASE)
    if m:
        s = float(m.group(1))
        scale = s if s > 0 else 1.0
    heights = [int(m.group(2)) for m in
               re.finditer(r"(\d{2,5})\s*[x\u00d7]\s*(\d{2,5})(?!\d)", capture)]
    if heights:
        height = max(heights)
    return height, scale


def _is_full_page_capture(capture, image_paths):
    """A4a: is this invocation the degenerate-prone full-page tier?
    Deterministic precedence: (1) an explicit fullPage flag in --capture;
    (2) a declared CSS height >= FULL_PAGE_MIN_CSS_H; (3) the input image's
    own pixel height at the declared scale (PIL, opened once per invocation,
    only when the metadata is inconclusive). Normal-viewport captures are
    never tagged."""
    text = (capture or "").lower()
    if "fullpage" in text or "full-page" in text or "full page" in text:
        return True
    height, scale = _parse_capture_dims(capture)
    if height is not None:
        return height >= FULL_PAGE_MIN_CSS_H
    if Image is None:
        return False
    for path in image_paths or []:
        try:
            with Image.open(path) as im:
                pixel_h = im.size[1]
        except Exception:  # noqa: BLE001 — unreadable input: metadata already said no
            continue
        if pixel_h / scale >= FULL_PAGE_MIN_CSS_H:
            return True
    return False


def _detect_full_page_tier(args, image_paths):
    """A4a hook for main(): decide the invocation's tier. On the full-page
    tier grant the pre-emptive retry allowance (args.tries += 1 in place)
    and return (True, tag_line); a normal-viewport invocation returns
    (False, None) with args untouched — no behavior change for that tier."""
    if not _is_full_page_capture(getattr(args, "capture", None), image_paths):
        return False, None
    before = args.tries
    args.tries += FULL_PAGE_TRIES_BONUS
    return True, (f"[info] full-page tier: yes (degenerate-prone) | "
                  f"pre-emptive retry allowance: --tries {before} -> {args.tries}")


class DegenerateTally:
    """A4c: thread-safe per-invocation count of degenerate/garbage abort
    events, split by tier — printed once at the end of main() so lanes can
    copy the line into reliability stats across waves."""

    def __init__(self):
        self._lock = threading.Lock()
        self.garbage = 0
        self.garbage_full_page = 0

    def bump_garbage(self, full_page):
        """Count one GarbageError abort — a degenerate body or thinking
        stream caught by the 2026-09-26 gates (an EVENT, win or lose: an
        invocation that aborts twice then wins still tallies 2)."""
        with self._lock:
            self.garbage += 1
            if full_page:
                self.garbage_full_page += 1

    def summary(self):
        return (f"degenerate events: {self.garbage} "
                f"(full-page tier: {self.garbage_full_page})")


def _update_transcript(path, winner_text, label):
    """A4b transcript hygiene: a transcript file may ONLY be written with a
    body that passed the garbage/degenerate gates — a race WINNER. A lost
    race (winner_text None: every model degenerate or failed) NEVER
    overwrites an existing transcript from an earlier valid attempt: the
    file is kept and the skip is logged. (wave4/welcome-outcome.md:286-289:
    a valid loop-3 transcript was lost to exactly this overwrite when lanes
    redirected stdout themselves; --transcript moves the write inside the
    script where the gates protect it.) Returns (stream, line) or None;
    never raises — transcript writing is telemetry, not a failure channel.

    w5-script-patch-v3 concurrency hardening (Directive 4, 4+ parallel
    instances): the write is ATOMIC and temp paths are instance-unique. The
    body goes to `<path>.tmp-<pid>-<thread>` (same directory, so
    os.replace is a same-filesystem atomic rename) and is fsync'd before the
    rename — a reader can never observe an empty or half-written transcript,
    which a plain `open(path,'w')` allowed while a 4-way parallel batch was
    still streaming, and two instances pointed at the SAME path can no
    longer interleave into a torn file (last completed writer wins, whole).
    The temp name carries pid+thread so parallel instances (and the race
    workers inside one instance) can never collide on the temp itself."""
    if not path:
        return None
    if winner_text is None:
        if os.path.exists(path):
            return ("error",
                    f"[error] {label}: transcript NOT overwritten — this run "
                    f"produced no validated winner; keeping the existing file: {path}")
        return None
    tmp = f"{path}.tmp-{os.getpid()}-{threading.get_ident()}"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(winner_text + "\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except OSError as e:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        return ("warn", f"[warn] {label}: cannot write transcript {path}: {e}")
    return ("info", f"[info] {label}: transcript written (validated winner, "
                    f"atomic): {path} (pid {os.getpid()})")


# Founder directive (2026-09-28 evening, w5-script-patch): thinking/reasoning
# is disabled on EVERY gateway request this script makes — DEFAULT behavior,
# not a flag — and every request runs with `"stream": true`. Belt-and-braces
# across OpenAI-compatible dialects; "disabled" (not "none") is the enum
# kimi-class validators accept for thinking.type. Top-level `enable_thinking`
# is deliberately NOT sent: the `images` combo's kimi member 400s on it
# ("Unsupported parameter(s): `enable_thinking`"). No tokens/time are ever
# spent on thinking.
THINKING_DISABLE_BLOCK = {
    "reasoning_effort": "none",
    "thinking": {"type": "disabled"},
    "chat_template_kwargs": {"enable_thinking": False},
}

# User directive (2026-10-09, slide-recreation batch): visual-judge lanes run with
# thinking/reasoning at the maximum effort the OpenAI-compatible dialects accept.
# Selected per-invocation via `--thinking high` (founder default `off` is unchanged
# for all other lanes). Same belt-and-braces field set as the disable block, inverted.
THINKING_HIGH_BLOCK = {
    "reasoning_effort": "high",
    "thinking": {"type": "enabled"},
    "chat_template_kwargs": {"enable_thinking": True},
}


def build_payload(model, max_tokens, content, thinking="off"):
    """Build ONE gateway request payload. `stream: true` always (founder
    directive). `thinking`: "off" (founder default — reasoning disabled),
    "high" (user directive — maximum reasoning effort, visual-judge lanes),
    "bare" (no reasoning fields — the 400-fallback resend only: a
    possibly-thinking answer still beats no answer at all)."""
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "stream": True,
        "messages": [{"role": "user", "content": content}],
    }
    if thinking == "off":
        payload.update(THINKING_DISABLE_BLOCK)
    elif thinking == "high":
        payload.update(THINKING_HIGH_BLOCK)
    return payload


def _stream_with_deadline(session, payload, headers, timeout):
    """Stream ONE gateway request to completion under a HARD wall-clock
    deadline. The payload always carries stream:true (founder directive —
    no thinking, streamed answers); this reads the SSE chunks as they arrive
    so a trickling or stuck stream cannot outlive the deadline. Returns a
    result dict: {"status": int, "content": str, "reasoning": str,
    "body": str (non-200 error snippet, "" otherwise)} — raises HangError if
    the wall clock (timeout + 30s) expires, or re-raises any transport error.

    Belt-and-braces: if the endpoint ignores stream:true and answers with a
    plain JSON body, the raw bytes are parsed as a non-streamed response."""
    box = {"status": 0, "content": "", "reasoning": "", "body": "", "err": None}

    def run():
        try:
            resp = session.post(
                f"{ENDPOINT}/chat/completions",
                headers=headers,
                json=payload,
                timeout=(10, timeout),
                stream=True,
            )
            box["status"] = resp.status_code
            if resp.status_code != 200:
                box["body"] = resp.text[:500]
                resp.close()
                return
            content, reasoning, raw = "", "", []
            for line in resp.iter_lines(decode_unicode=True):
                if not line:
                    continue
                raw.append(line)
                if not line.startswith("data:"):
                    continue
                data = line[len("data:"):].strip()
                if data == "[DONE]":
                    break
                try:
                    obj = json.loads(data)
                except ValueError:
                    continue
                if isinstance(obj, dict) and obj.get("error"):
                    box["body"] = f"api error: {str(obj['error'])[:200]}"
                    return
                for ch in obj.get("choices") or []:
                    delta = ch.get("delta") or {}
                    c = delta.get("content")
                    if isinstance(c, str):
                        content += c
                    for rkey in ("reasoning_content", "reasoning", "thinking"):
                        rv = delta.get(rkey)
                        if isinstance(rv, str):
                            reasoning += rv
                        elif isinstance(rv, dict):
                            reasoning += str(rv.get("text", rv.get("content", "")))
            if not content and not reasoning and raw:
                # endpoint ignored stream:true -> plain JSON body
                try:
                    body = json.loads("\n".join(raw))
                except ValueError:
                    body = None
                if isinstance(body, dict):
                    if body.get("error"):
                        box["body"] = f"api error: {str(body['error'])[:200]}"
                        return
                    choices = body.get("choices") or []
                    if choices:
                        msg = choices[0].get("message", {}) or {}
                        c = msg.get("content")
                        if isinstance(c, str):
                            content = c
                        for rkey in ("reasoning_content", "reasoning", "thinking"):
                            rv = msg.get(rkey)
                            if isinstance(rv, str):
                                reasoning += "\n" + rv
                            elif isinstance(rv, dict):
                                reasoning += "\n" + str(rv.get("text", rv.get("content", "")))
            box["content"] = content
            box["reasoning"] = reasoning
        except BaseException as e:  # noqa: BLE001 — transported to caller
            box["err"] = e

    t = threading.Thread(target=run, daemon=True)
    t.start()
    t.join(timeout + 30)
    if t.is_alive():
        raise HangError(
            f"hard wall-clock {timeout + 30}s exceeded — call aborted "
            f"(possible stuck thinking stream)"
        )
    if box["err"] is not None:
        raise box["err"]
    return box


def ask_model(session, model, data_urls, prompt, key, timeout, max_tokens,
              thinking="off"):
    """One STREAMED request (possibly carrying several images). Raises on any
    non-WORKING outcome (transport, HTTP, or content).

    Resilience: if the endpoint 400s while rejecting one of the optional
    reasoning fields (disable OR high block), retry ONCE with none of them
    (streaming kept) — the answer still comes back (the model may just
    think), which beats no answer at all."""
    headers = {"Content-Type": "application/json", "x-omniroute-no-memory": "true"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    content = [{"type": "text", "text": prompt}]
    for data_url in data_urls:
        content.append({"type": "image_url", "image_url": {"url": data_url}})
    payload = build_payload(model, max_tokens, content, thinking)
    result = _stream_with_deadline(session, payload, headers, timeout)
    if result["status"] != 200:
        # Graceful single retry: an endpoint (or, for combo aliases, one of its
        # members) rejecting an unknown optional field by name gets ONE resend
        # with none of the reasoning extras — a possibly-thinking answer beats
        # no answer at all. Streaming + the founder defaults stay.
        applied = (THINKING_DISABLE_BLOCK if thinking == "off"
                   else THINKING_HIGH_BLOCK if thinking == "high" else {})
        if result["status"] in (400, 422, 502) and any(
            f in result["body"] for f in applied
        ):
            payload = build_payload(model, max_tokens, content, thinking="bare")
            result = _stream_with_deadline(session, payload, headers, timeout)
    if result["status"] != 200:
        raise RuntimeError(f"HTTP {result['status']}: {result['body'][:500]}")
    if result["body"].startswith("api error:"):
        raise RuntimeError(result["body"])
    c = result["content"]
    reasoning = result["reasoning"]
    if not isinstance(c, str) or not c.strip():
        raise EmptyStreamError(f"empty content: {result['body'][:200] or 'no deltas'}")
    # Garbage scan: check the ANSWER *and* any thinking/reasoning field the
    # gateway echoes back — the round-1 stall family lives there (endlessly
    # repeated text inside the thinking stream while the answer is short or
    # absent). Abort this attempt; the worker retries up to HARD_RETRY_CAP.
    full = c.strip()
    if reasoning.strip():
        full = full + "\n" + reasoning.strip()
    if _looks_like_garbage(full):
        kind = "thinking stream" if _looks_like_garbage(reasoning) and not _looks_like_garbage(c) else "response"
        raise GarbageError(f"garbage: infinite/looping repetition in {kind}")
    # w5-script-patch-v2: the thought-channel token leak class — literal
    # chat-template markers (`<|channel>thought`, `<channel|>`, `<|thought`)
    # in the content mean the body IS leaked thinking, never an answer.
    # Abort + retry; the transcript gates then never see this shape.
    if _LEAKED_CHANNEL_RE.search(c):
        raise GarbageError("garbage: thought-channel token leak in response "
                           "(literal <|channel>/<channel|> template markers)")
    # w5-script-patch-v3: the ECHO-CLASS validator — the body reproduces the
    # prompt's instruction language / glossary / section-header list verbatim
    # (often then truncating at max-tokens) instead of answering. Three rules:
    # long verbatim span, multi-span glossary echo, and the zero-section-body
    # header shell. Abort + retry (GarbageError ladder); never a winner, never
    # written to a transcript.
    echo_reason = _echo_class_reason(prompt, c)
    if echo_reason:
        raise GarbageError(f"garbage: echo-class response ({echo_reason})")
    return c.strip()


def worker(model, data_urls, prompt, key, out_q, timeout, max_tokens, tries,
           tally=None, full_page=False, thinking="off"):
    """Daemon thread: race one model. Hang/garbage/empty-stream failures ABORT
    the current call and retry independently of --tries, up to HARD_RETRY_CAP
    (3) total — per the round-1 stall post-mortem; transport/HTTP failures
    still honor --tries. Every GarbageError abort bumps `tally` (A4c),
    tier-aware via `full_page` (A4a); EmptyStreamError does NOT (not a
    degenerate body — a transient empty 200 from the combo alias)."""
    session = requests.Session()
    hard_retries = 0
    normal_failures = 0
    attempt = 0
    while True:
        attempt += 1
        try:
            text = ask_model(session, model, data_urls, prompt, key, timeout,
                             max_tokens, thinking)
        except (HangError, GarbageError, EmptyStreamError) as e:
            if isinstance(e, GarbageError) and tally is not None:
                tally.bump_garbage(full_page)
            hard_retries += 1
            out_q.put(("err", model, f"attempt {attempt}: ABORT {type(e).__name__}: {e}"
                       + (f" — abort+retry {hard_retries}/{HARD_RETRY_CAP}" if hard_retries < HARD_RETRY_CAP else " — giving up")))
            if hard_retries >= HARD_RETRY_CAP:
                return
            time.sleep(5)
        except Exception as e:  # noqa: BLE001 — every failure mode is a race loss
            normal_failures += 1
            out_q.put(("err", model, f"attempt {attempt}: {e}"))
            if normal_failures >= tries:
                return
            time.sleep(3)
        else:
            out_q.put(("ok", model, text, attempt))
            return


def race(data_urls, prompt, key, args, label, tally=None, full_page=False):
    """Race all models on ONE request carrying all data_urls.
    Returns (model, text, (round_no, attempt)) on win, (None, errs, None) on loss.
    Passes the A4c degenerate tally (and the invocation's A4a tier) through to
    every worker so garbage aborts are counted per-invocation."""
    all_errs = []
    for round_no in range(1, args.rounds + 1):
        out_q = queue.Queue()
        threads = [
            threading.Thread(
                target=worker,
                args=(m, data_urls, prompt, key, out_q,
                      args.timeout, args.max_tokens, args.tries,
                      tally, full_page, args.thinking),
                daemon=True,
            )
            for m in args.models
        ]
        for t in threads:
            t.start()
        while any(t.is_alive() for t in threads) or not out_q.empty():
            try:
                kind, model, text, *rest = out_q.get(timeout=0.5)
            except queue.Empty:
                continue
            if kind == "ok":
                attempt = rest[0] if rest else "?"
                return model, text, (round_no, attempt)
            print(f"[warn] {label} :: {model} :: {text}", file=sys.stderr)
            all_errs.append(f"{model}: {text}")
        if round_no < args.rounds:
            print(f"[warn] {label} :: round {round_no}: all models failed, "
                  f"restarting race", file=sys.stderr)
            time.sleep(5)
    return None, all_errs, None


class FullHelpParser(argparse.ArgumentParser):
    """Any usage error prints the FULL help menu and exits 2."""

    def error(self, message):
        self.print_help(sys.stderr)
        self.exit(2, f"\n[error] {message}\n")


EXAMPLES = """\
modes (every arg with shape + description; details also via `MODE -h`):
  analysis IMG -p/--prompt PROMPT
      IMG: exactly one image path; PROMPT: question for the models
      (default: full visual-QA description).
  comparison IMG1 IMG2 -p/--prompt PROMPT
      IMG1 IMG2: exactly two image paths (both in ONE API request); PROMPT
      (default: similarities/differences/which-is-better comparison spec).
  batch IMG [IMG ...] -p/--prompt PROMPT
      one or more image paths sharing ONE prompt in ONE API request.
  per-image --image IMG --prompt P (repeatable pairs) --master-prompt M (required)
      each image gets its OWN sequential API request; prompt = M + P;
      len(images) must equal len(prompts) >= 1.

examples (one per mode):
  analysis    python3 scripts/analyze_image.py analysis IMG.png -p "PROMPT"
  comparison  python3 scripts/analyze_image.py comparison IMG1.png IMG2.png -p "PROMPT"
  batch       python3 scripts/analyze_image.py batch IMG1.png IMG2.png -p "PROMPT"
  per-image   python3 scripts/analyze_image.py per-image \\
                  --image IMG1.png --prompt "p1" \\
                  --image IMG2.png --prompt "p2" --master-prompt "master"

global flags (all modes):
  --timeout N          per-request read timeout in seconds (default 600)
  --rounds N           full-race restarts if every model fails (default 2)
  --tries N            attempts per model per round (default 2)
  --models M1,M2,...   comma-separated model list override (default: images)
  --max-tokens N       max_tokens for the completion (default 8192)
  --json               JSON-Lines output (per-image: one line per image)
  --transcript PATH    write the winning body to PATH (a degenerate/failed
                       run never overwrites an existing transcript)

pacing: the gateway is SHARED (Stitch proxy + vision) — prefer per-image mode for
multi-image workloads (sequential requests); never wrap this script in retry loops.
"""


def add_common(sp):
    """Global flags shared by every mode."""
    sp.add_argument("--timeout", type=int, default=600,
                    help="per-request read timeout in seconds (default: 600; >600 prints a pacing warning)")
    sp.add_argument("--rounds", type=int, default=2,
                    help="full-race restarts if every model fails (default: 2)")
    sp.add_argument("--tries", type=int, default=2,
                    help="attempts per model per round (default: 2)")
    sp.add_argument("--models", default=None,
                    help="comma-separated model list override (default: images)")
    sp.add_argument("--thinking", choices=("off", "high"), default="off",
                    help="reasoning effort: 'off' (founder default — thinking "
                         "disabled on every request) or 'high' (user directive "
                         "2026-10-09: visual-judge lanes request maximum "
                         "reasoning effort; same field set as 'off', inverted)")
    sp.add_argument("--max-tokens", type=int, default=8192,
                    help="max completion tokens per request (default: 8192; "
                         "raised from 4096 after r1 lanes' §1–§9 audit "
                         "responses truncated mid-body — a model-ceiling "
                         "misdiagnosis, actually this default)")
    sp.add_argument("--json", action="store_true",
                    help="emit JSON Lines (per-image: one line per image)")
    # Per-run context injection (r1-runs rescue finding: the original lane
    # NEVER injected the VIEW/CAPTURE header lines and the models noticed —
    # every gemini transcript flagged their absence). Baking the injection
    # into the script removes the lane-recipe footgun.
    sp.add_argument("--view", default=None,
                    help="view name + purpose header line, e.g. "
                         "'ModelsScreen — provider management'; prepended "
                         "to the prompt as 'VIEW: <value>'")
    sp.add_argument("--capture", default=None,
                    help="capture metadata header line, e.g. "
                         "'1440x900 CSS px, 1x scale, app'; prepended to "
                         "the prompt as 'CAPTURE: <value>'")
    # A4b (wave-5 amendment): the script-owned transcript write. Lanes used
    # to redirect stdout themselves — a degenerate/failed run then clobbered
    # the earlier valid transcript (wave4/welcome-outcome.md:286-289). This
    # flag moves the write inside the script where the garbage gates protect
    # it: only a validated winner is ever written, a failed run never
    # overwrites an existing file.
    sp.add_argument("--transcript", default=None, metavar="PATH",
                    help="write the winning (gate-validated) response body "
                         "to PATH; a degenerate/failed run NEVER overwrites "
                         "an existing transcript (A4b transcript hygiene)")


def build_parser():
    ap = FullHelpParser(
        prog="analyze_image.py",
        description="Analyze images by racing vision models in parallel; "
                    "first working response wins (HTTP 200, JSON parses, "
                    "non-empty choices[0].message.content, no error wrapper).",
        epilog=EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="mode", required=True, metavar="MODE",
                            parser_class=FullHelpParser)

    sp = sub.add_parser(
        "analysis",
        help="EXACTLY ONE image, one prompt -> one race, one response",
        description="Analyze ONE image. Sends a single API request (raced across "
                    "all models). Default prompt: full visual-QA description spec.",
        epilog="example:\n  python3 scripts/analyze_image.py analysis render.png -p \"Describe the header\"\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sp.add_argument("image", help="image file path (exactly one)")
    sp.add_argument("-p", "--prompt", default=DEFAULT_PROMPT,
                    help="question/prompt for the models (default: full visual-QA description)")
    add_common(sp)

    sp = sub.add_parser(
        "comparison",
        help="EXACTLY TWO images, ONE API request carrying both",
        description="Compare TWO images in one API request (both images in one "
                    "message). Default prompt: side-by-side comparison spec "
                    "(similarities, differences, which is better and why).",
        epilog="example:\n  python3 scripts/analyze_image.py comparison a.png b.png -p \"Which layout is cleaner?\"\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sp.add_argument("images", nargs=2, metavar=("IMG1", "IMG2"),
                    help="exactly two image file paths")
    sp.add_argument("-p", "--prompt", default=COMPARISON_PROMPT,
                    help="comparison prompt (default: similarities/differences/which-is-better spec)")
    add_common(sp)

    sp = sub.add_parser(
        "batch",
        help="ANY number of images, ONE shared prompt, ONE API request",
        description="Analyze ANY number of images together in ONE API request "
                    "(all images in one message, one shared prompt).",
        epilog="example:\n  python3 scripts/analyze_image.py batch a.png b.png c.png -p \"List all UI defects\"\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sp.add_argument("images", nargs="+", metavar="IMG",
                    help="one or more image file paths")
    sp.add_argument("-p", "--prompt", default=DEFAULT_PROMPT,
                    help="shared question/prompt for the models (default: full visual-QA description)")
    add_common(sp)

    sp = sub.add_parser(
        "per-image",
        help="PREFERRED: image+prompt pairs + master prompt; each image in its OWN sequential request",
        description="Analyze each image in its OWN separate API request (one "
                    "image per request, sequential — pacing discipline). Prompt "
                    "for each image = --master-prompt + that image's unique "
                    "--prompt. len(images) must equal len(prompts) >= 1.",
        epilog="example:\n  python3 scripts/analyze_image.py per-image \\\n"
               "      --image a.png --prompt \"check header\" \\\n"
               "      --image b.png --prompt \"check footer\" --master-prompt \"You are a QA analyst.\"\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sp.add_argument("--image", action="append", dest="images", metavar="IMG",
                    required=True, help="image file path (repeatable: once per pair)")
    sp.add_argument("--prompt", action="append", dest="prompts", metavar="P",
                    required=True, help="unique prompt for the preceding --image (repeatable)")
    sp.add_argument("--master-prompt", required=True, metavar="M",
                    help="master prompt prepended to every per-image prompt (required)")
    add_common(sp)

    return ap


def report(args, label, images, model, text, meta, ok):
    """Emit one race result (text or JSON-Lines). Returns True on success."""
    if model is None:
        print(f"[error] {label}: every model failed:\n  " + "\n  ".join(text),
              file=sys.stderr)
        if args.json:
            rec = {"images": images, "errors": text}
            print(json.dumps(rec, ensure_ascii=False))
        # A4b: a lost race (all models degenerate/failed) must never
        # clobber a valid transcript from an earlier attempt — keep it, log
        # the skip. No existing file: nothing to protect, nothing written.
        tlog = _update_transcript(getattr(args, "transcript", None), None,
                                  label or ", ".join(images))
        if tlog:
            print(tlog[1], file=sys.stderr)
        return False
    # Truncation warning (r1 finding, 3 instances across lanes): a winner can
    # be hard-capped by --max_tokens mid-body and still look complete. Heuristic:
    # >= 85% of the token budget expressed as chars (~3.5 chars/token).
    budget_chars = int(getattr(args, "max_tokens", 4096)) * 3.5
    if isinstance(text, str) and len(text) >= budget_chars * 0.85:
        print(f"[warn] {label or ', '.join(images)}: winner length "
              f"{len(text)} chars ≈ the --max-tokens budget — likely TRUNCATED "
              f"mid-body; re-run with a higher --max-tokens if sections are missing",
              file=sys.stderr)
    if args.json:
        rec = {"images": images, "model": model, "text": text}
        if label:
            rec["label"] = label
        print(json.dumps(rec, ensure_ascii=False))
    else:
        print(f"=== {label or ', '.join(images)} ===")
        print(f"[winner] {model} (round {meta[0]}, attempt {meta[1]})")
        print(text)
        print()
    # A4b: the winner body passed the garbage/degenerate gates in
    # ask_model — it is the ONLY thing a transcript file may carry.
    tlog = _update_transcript(getattr(args, "transcript", None), text,
                              label or ", ".join(images))
    if tlog:
        print(tlog[1], file=sys.stderr)
    return ok


def main():
    ap = build_parser()
    args = ap.parse_args()

    if args.mode == "per-image":
        if len(args.images) != len(args.prompts) or len(args.images) < 1:
            ap.error(f"per-image needs len(images)==len(prompts)>=1 "
                     f"(got {len(args.images)} images, {len(args.prompts)} prompts)")
        work = list(zip(args.images, args.prompts))  # (path, unique prompt) pairs
    elif args.mode == "analysis":
        work = [(None, None, [args.image])]
    else:
        work = [(None, None, list(args.images))]

    if args.models:
        args.models = [m.strip() for m in args.models.split(",") if m.strip()]
    else:
        args.models = DEFAULT_MODELS

    key = load_key()
    # Central context injection: build the VIEW/CAPTURE header block once and
    # prepend it to whatever prompt the mode uses (r1-runs rescue proposal).
    header_lines = []
    if getattr(args, "view", None):
        header_lines.append(f"VIEW: {args.view}")
    if getattr(args, "capture", None):
        header_lines.append(f"CAPTURE: {args.capture}")
    context_header = ("\n".join(header_lines) + "\n\n") if header_lines else ""
    if context_header:
        if args.mode == "per-image":
            args.master_prompt = context_header + args.master_prompt
        else:
            args.prompt = context_header + args.prompt
        print(f"[info] context header injected: {' | '.join(header_lines)}",
              file=sys.stderr)
    if args.timeout > 600:
        print("[warn] --timeout > 600s: the gateway at localhost:17844 is shared (Stitch proxy "
              "+ vision). Long-timeout retry loops SATURATE it for everyone — prefer one modest "
              "call and retry later.", file=sys.stderr)
    # w5-script-patch-v3 (Directive 4): the pid stamp makes interleaved
    # stderr from 4+ parallel instances attributable — lanes that share one
    # redirected stderr file still get a per-instance header identifying
    # every following [warn]/[info] line. Per-instance stderr paths remain
    # the recommended contract.
    print(f"[info] mode {args.mode} | endpoint {ENDPOINT} | models: {', '.join(args.models)} | "
          f"auth: {'key file present' if key else 'no key (endpoint allows anonymous)'} | "
          f"pid {os.getpid()}",
          file=sys.stderr)

    # A4a: full-page tier detection — tag the invocation and grant the
    # degenerate-prone tier its ONE pre-emptive retry allowance. Normal-
    # viewport captures print nothing and keep --tries untouched.
    if args.mode == "per-image":
        invocation_images = [p for p, _ in work]
    elif args.mode == "analysis":
        invocation_images = [args.image]
    else:
        invocation_images = list(args.images)
    full_page, tier_line = _detect_full_page_tier(args, invocation_images)
    if tier_line:
        print(tier_line, file=sys.stderr)
    # A4c: one degenerate-event tally for the whole invocation (all races).
    tally = DegenerateTally()

    ok_count = 0
    total = 1 if args.mode in ("analysis", "comparison", "batch") else len(work)

    if args.mode == "per-image":
        for path, iprompt in work:
            if not os.path.isfile(path):
                print(f"[error] not a file: {path}", file=sys.stderr)
                if args.json:
                    print(json.dumps({"images": [path], "error": "not a file"},
                                     ensure_ascii=False))
                continue
            prompt = f"{args.master_prompt}\n\nImage-specific task: {iprompt}"
            try:
                data_urls = [encode_image(path)]
            except OSError as e:
                print(f"[error] {path}: cannot read image: {e}", file=sys.stderr)
                if args.json:
                    print(json.dumps({"images": [path], "errors": [f"cannot read image: {e}"]},
                                     ensure_ascii=False))
                continue
            model, text, meta = race(data_urls, prompt, key, args,
                                     os.path.basename(path), tally, full_page)
            if report(args, os.path.basename(path), [path], model, text, meta, True):
                ok_count += 1
    else:
        label, _, imgs = work[0]
        missing = [p for p in imgs if not os.path.isfile(p)]
        if missing:
            for p in missing:
                print(f"[error] not a file: {p}", file=sys.stderr)
                if args.json:
                    print(json.dumps({"images": [p], "error": "not a file"},
                                     ensure_ascii=False))
            sys.exit(1)
        try:
            data_urls = [encode_image(p) for p in imgs]
        except OSError as e:
            print(f"[error] cannot read image: {e}", file=sys.stderr)
            if args.json:
                print(json.dumps({"images": imgs, "errors": [f"cannot read image: {e}"]},
                                 ensure_ascii=False))
            sys.exit(1)
        model, text, meta = race(data_urls, args.prompt, key, args, args.mode,
                                 tally, full_page)
        if report(args, None, imgs, model, text, meta, True):
            ok_count += 1

    # A4c: the per-invocation degenerate tally — copy this line into
    # reliability stats; the full-page split keeps the tier's failure rate
    # visible across waves.
    print(f"[info] {tally.summary()}", file=sys.stderr)
    print(f"[info] {ok_count}/{total} result(s) analyzed successfully", file=sys.stderr)
    sys.exit(0 if ok_count == total else 1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[info] interrupted", file=sys.stderr)
        sys.exit(130)
