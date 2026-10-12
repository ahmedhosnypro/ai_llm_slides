#!/usr/bin/env python3
"""Judge attempt 3 driver (slide 003, deep-learning/001_transformers_part1).

Invokes analyze_image.py comparison with argv byte-identical to the banked
judge_prompt_3.txt step-2 command; the -p payload is read verbatim from
judge_p_payload_3.txt (extracted programmatically from judge_prompt_3.txt).
No shell quoting involved -> zero drift vs the frozen template.
"""
import subprocess
import sys

ROOT = "/home/ahmed/Projects/ai_llm_slides"
QA = f"{ROOT}/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide003"

payload = open(f"{QA}/judge_p_payload_3.txt", encoding="utf-8").read()

# Garbage-retry support (17 §Judge 2b): same parameters, separate banked transcript
# per retry; default transcript = judge_attempt_3.txt (first invocation).
suffix = sys.argv[1] if len(sys.argv) > 1 else ""

cmd = [
    sys.executable,
    f"{ROOT}/.agents/skills/image-analysis/scripts/analyze_image.py",
    "comparison",
    f"{QA}/render_4.png",
    f"{ROOT}/videos/deep-learning/001_transformers_part1/unique_slides/slide_003.jpg",
    "--view", "Slide 003 recreation — fidelity check vs original lecture frame",
    "--capture", "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame",
    "--thinking", "high",
    "--max-tokens", "65536",
    "--timeout", "420",
    "--rounds", "1",
    "--tries", "1",
    "--transcript", f"{QA}/judge_attempt_3{suffix}.txt",
    "-p", payload,
]
r = subprocess.run(cmd, cwd=ROOT)
sys.exit(r.returncode)
