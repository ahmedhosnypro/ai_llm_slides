import json, sys, importlib.util
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["mathtext.fontset"] = "stix"
spec = importlib.util.spec_from_file_location(
    "render_eq", "/home/ahmed/Projects/ai_llm_slides/.agents/skills/slide-recreation/scripts/render_eq.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
latex, out, fs, color = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
print(json.dumps(mod.render(latex, out, fs, color)))
