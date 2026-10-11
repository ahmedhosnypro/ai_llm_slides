#!/usr/bin/env python3
"""run_judge_a2.py — execute the banked judge_prompt_2.txt comparison step byte-for-byte.
Extracts the frozen -p template from the banked prompt and spawns the gate-wrapped
analyze_image.py comparison exactly as written (W4 wall 540, --timeout 420,
--thinking high, --max-tokens 65536)."""
import re
import subprocess
import os
import sys

ROOT = "/home/ahmed/Projects/ai_llm_slides"
QA = f"{ROOT}/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide016"
prompt = open(f"{QA}/judge_prompt_2.txt", encoding="utf-8").read()

# the -p argument: from `-p "` to the terminating `"` on that (long) line
m = re.search(r'-p "(.*)"\s*$', prompt, re.M)
if not m:
    sys.exit("could not extract -p template from banked prompt")
template = m.group(1)
print(f"template length: {len(template)} chars", flush=True)

env = dict(os.environ)
env["TMPDIR"] = f"{ROOT}/videos/deep-learning/001_transformers_part1/scratch/slide016"

cmd = [
    "scripts/16_vision_gate.sh", "timeout", "540", "python3",
    ".agents/skills/image-analysis/scripts/analyze_image.py", "comparison",
    "videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide016/render_2.png",
    "videos/deep-learning/001_transformers_part1/unique_slides/slide_016.jpg",
    "--view", "Slide 016 recreation — fidelity check vs original lecture frame",
    "--capture", "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame",
    "--thinking", "high", "--max-tokens", "65536",
    "--timeout", "420", "--rounds", "1", "--tries", "1",
    "--transcript", f"{QA}/judge_attempt_2.txt",
    "-p", template,
]
r = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True)
print("EXIT =", r.returncode, flush=True)
print("--- stdout tail ---")
print(r.stdout[-4000:], flush=True)
print("--- stderr tail ---")
print(r.stderr[-2000:], flush=True)
