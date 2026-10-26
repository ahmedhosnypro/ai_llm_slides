#!/usr/bin/env python3
"""Wave-5 crop judges via vision gateway, 2 in-flight max, banked per crop."""
import subprocess, sys, os, time

RUN = "/home/ahmed/Projects/ai_llm_slides/doc-parse-test/run_20261025-024314"
BASE = f"{RUN}/11_cascade/slide_057"
AI = "/home/ahmed/Projects/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py"

COMMON = (" Transcribe EVERY visible text string verbatim, top-to-bottom left-to-right, "
          "including tiny labels, subscripts, serif-italic glyphs, and partial glyphs at crop edges. "
          "For each string give its approximate pixel position (top-left x,y) within THIS crop image. "
          "Mark unreadable glyphs [?]. Do not invent text that is not visible. "
          "End with a line 'VERDICT: <n> strings visible'.")

PROMPTS = {
 "crop01_enc_top_ychips_bars": "This 3x-upscaled crop from a Transformer-architecture lecture slide should contain a row of small serif-italic token chips (letter Y with digit subscripts) near the top and horizontal purple bars labeled 'Encoder Block ...'." + COMMON,
 "crop02_enc_bottom_emb": "This 3x-upscaled crop from a Transformer-architecture lecture slide should contain a rounded box labeled 'Word Embedding' and 'Positional Encoding / Embedding', a row of serif-italic chips (letter X with digit subscripts), and a row of small 'Word N' labels." + COMMON,
 "crop03_enc_mid_bars_vlabel": "This 3x-upscaled crop from a Transformer-architecture lecture slide should contain a rotated vertical 'Encoder' label at the left edge and horizontal purple bars labeled 'Encoder Block 1' and 'Encoder Block 0' with small arrows between them." + COMMON,
 "crop04_central_kv": "This 3x-upscaled crop from a Transformer-architecture lecture slide should contain a narrow vertically-striped column and small badge letters near it (K, V, and tiny Q letters). Check carefully whether ANY letter or word ink exists at all." + COMMON,
 "crop05_dec_top_bars_attn": "This 3x-upscaled crop from a Transformer-architecture lecture slide should contain stacked horizontal bars labeled 'Residual Connection and Layer Normalization' and 'Feed Forward Networks - One Hidden with RELU Activation', possibly a 'Softmax' bar near the top, blue boxes carrying three short lines of text, and a rotated vertical 'Decoder' label at the right edge." + COMMON,
 "crop06_dec_bottom_tokens": "This 3x-upscaled crop from a Transformer-architecture lecture slide should contain lavender boxes labeled 'Multi-Head Self-Attention', a purple bar labeled 'Word and Position Encoding', and a bottom row of five small token texts inside colored boxes." + COMMON,
 "crop07_legend": "This 3x-upscaled crop from a Transformer-architecture lecture slide should contain three legend lines, each with a small colored square: 'Encoder', 'Decoder', 'Attention'." + COMMON,
 "crop08_ychips_tight": "This 3x-upscaled crop should contain ONLY one row of small serif-italic chips: the letter Y with digit or N-based subscripts (expected chips: Y_0 Y_1 Y_2 Y_3 Y_4 Y_5 Y_N-2 Y_N-1). Transcribe each chip separately, subscript included, left to right." + COMMON,
 "crop09_kv_column": "This 3x-upscaled crop from a Transformer-architecture lecture slide should contain a narrow vertically-striped column, small badge labels 'K=' and 'V' beside it, tiny Q letters, and possibly the left edge of decoder bar labels. Check carefully for any letter ink anywhere." + COMMON,
 "crop10_xchips_tight": "This 3x-upscaled crop should contain ONLY one row of small serif-italic chips: the letter X with digit or N-based subscripts (expected chips: X_0 X_1 X_2 X_3 X_4 X_5 X_N-2 X_N-1). Transcribe each chip separately, subscript included, left to right." + COMMON,
 "crop11_wordrow_tight": "This 3x-upscaled crop should contain ONLY one row of small labels under chip boxes (expected: Word 0, Word 1, Word 2, Word 3, Word 4, Word 5, Word N-2, Word N-1). Transcribe each label exactly, left to right." + COMMON,
 "crop12_softmax_bar": "This 3x-upscaled crop should contain one thin horizontal bar carrying a single short word label (expected: 'Softmax'). Transcribe the label exactly." + COMMON,
 "crop13_bottom_tokens": "This 3x-upscaled crop should contain a bottom row of five small token texts (expected: SOS, Je, ne, suis, faisait) inside colored boxes, and possibly the top edge of a purple bar labeled 'Word and Position Encoding'." + COMMON,
 "crop14_big_q": "This 3x-upscaled crop from a Transformer-architecture lecture slide should contain a large letter 'Q' badge in the bottom-right area, plus partial bar labels at the left edge." + COMMON,
 "crop15_ynum_chips_right": "This 3x-upscaled crop should contain ONLY the right-hand serif-italic chips of a Y-chip row (expected: Y_4 Y_5 Y_N-2 Y_N-1). Transcribe each chip exactly." + COMMON,
 "crop16_xnum_chips_right": "This 3x-upscaled crop should contain ONLY the right-hand serif-italic chips of an X-chip row (expected: X_4 X_5 X_N-2 X_N-1). Transcribe each chip exactly." + COMMON,
}

ORDER = ["crop01_enc_top_ychips_bars","crop02_enc_bottom_emb","crop03_enc_mid_bars_vlabel",
         "crop04_central_kv","crop05_dec_top_bars_attn","crop06_dec_bottom_tokens","crop07_legend",
         "crop08_ychips_tight","crop09_kv_column","crop10_xchips_tight","crop11_wordrow_tight",
         "crop12_softmax_bar","crop13_bottom_tokens","crop14_big_q","crop15_ynum_chips_right",
         "crop16_xnum_chips_right"]

def run_one(cid):
    out = f"{BASE}/judges/{cid}_judge.md"
    if os.path.exists(out) and "VERDICT" in open(out).read():
        return f"{cid}: already banked"
    crop = f"{BASE}/crops/{cid}/crop.png"
    cmd = ["python3", AI, "analysis", crop, "-p", PROMPTS[cid],
           "--timeout", "300", "--rounds", "1", "--tries", "1"]
    for attempt in (1, 2, 3):
        t0 = time.time()
        p = subprocess.run(cmd, capture_output=True, text=True)
        body = (p.stdout or "") + (("\n--stderr--\n" + p.stderr) if p.stderr.strip() else "")
        if p.returncode == 0 and len(body.strip()) > 40:
            with open(out, "w") as f:
                f.write(f"# crop judge — {cid}\nCOMMAND: {' '.join(cmd[:6])} ...\n"
                        f"ATTEMPT: {attempt} LATENCY: {time.time()-t0:.0f}s\n\n{body}")
            return f"{cid}: OK attempt {attempt} ({time.time()-t0:.0f}s)"
        time.sleep(60)
    with open(out, "w") as f:
        f.write(f"# crop judge — {cid}\nFAILED after 3 attempts\nstdout:\n{p.stdout}\nstderr:\n{p.stderr}")
    return f"{cid}: FAILED 3 attempts"

pairs = [ORDER[i:i+2] for i in range(0, len(ORDER), 2)]
for pair in pairs:
    procs = [subprocess.Popen([sys.executable, "-c",
        "import sys;sys.path.insert(0,'/home/ahmed/Projects/ai_llm_slides/doc-parse-test/run_20261025-024314/11_cascade/slide_057');"
        "import judge_runner as jr;print(jr.run_one(sys.argv[1]))", cid],
        stdout=subprocess.PIPE, text=True) for cid in pair]
    for pr in procs:
        out, _ = pr.communicate()
        print(out.strip())
print("ALL_JUDGES_DONE")
