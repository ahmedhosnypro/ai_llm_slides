#!/usr/bin/env python3
"""Local STIX-fontset variant of the certified scripts/render_eq.py (same CLI/contract).
render_eq_stix.py in scripts/ points at scripts/../scratch_math/render_eq.py which is
absent in this checkout; this wrapper imports the certified render() and flips the
mathtext fontset to stix (serif), per render_eq_stix.py's documented rationale.
"""
import json, os, sys, importlib.util

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["mathtext.fontset"] = "stix"

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "render_eq", "/home/ahmed/Projects/ai_llm_slides/scripts/render_eq.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

latex, out, fs, color = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
print(json.dumps(mod.render(latex, out, fs, color)))
