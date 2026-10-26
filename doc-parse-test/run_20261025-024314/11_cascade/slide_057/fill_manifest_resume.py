#!/usr/bin/env python3
"""Fill null manifest fields from banked evidence: parse_call_dir, judge_files,
novel_strings, stop_reason. Schema (key `nodes`, per-node fields) unchanged."""
import json

B = "/home/ahmed/Projects/ai_llm_slides/doc-parse-test/run_20261025-024314/11_cascade/slide_057"
M = f"{B}/manifest.json"

call_of = {
    "crop01_enc_top_ychips_bars": "call01_crop01_enc_top_ychips_bars",
    "crop02_enc_bottom_emb": "call02_crop02_enc_bottom_emb",
    "crop03_enc_mid_bars_vlabel": "call03_crop03_enc_mid_bars_vlabel",
    "crop04_central_kv": "call04_crop04_central_kv",
    "crop05_dec_top_bars_attn": "call05_crop05_dec_top_bars_attn",
    "crop06_dec_bottom_tokens": "call06_crop06_dec_bottom_tokens",
    "crop07_legend": "call07_crop07_legend",
    "crop08_ychips_tight": "call08_crop08_ychips_tight",
    "crop09_kv_column": "call09_crop09_kv_column",
    "crop10_xchips_tight": "call010_crop10_xchips_tight",
    "crop11_wordrow_tight": "call011_crop11_wordrow_tight",
    "crop12_softmax_bar": "call12_crop12_softmax_bar",
    "crop13_bottom_tokens": "call13_crop13_bottom_tokens",
    "crop14_big_q": "call14_crop14_big_q",
    "crop15_ynum_chips_right": "call17_crop15_ynum_chips_right",
    "crop16_xnum_chips_right": "call18_crop16_xnum_chips_right",
}
novel = {
    "crop01_enc_top_ychips_bars": 1, "crop02_enc_bottom_emb": 9,
    "crop03_enc_mid_bars_vlabel": 2, "crop04_central_kv": 0,
    "crop05_dec_top_bars_attn": 2, "crop06_dec_bottom_tokens": 2,
    "crop07_legend": 1, "crop08_ychips_tight": 7, "crop09_kv_column": 4,
    "crop10_xchips_tight": 7, "crop11_wordrow_tight": 0,
    "crop12_softmax_bar": 1, "crop13_bottom_tokens": 1, "crop14_big_q": 5,
    "crop15_ynum_chips_right": 0, "crop16_xnum_chips_right": 3,
}
judged = ["crop01_enc_top_ychips_bars", "crop02_enc_bottom_emb",
          "crop05_dec_top_bars_attn", "crop06_dec_bottom_tokens",
          "crop08_ychips_tight", "crop09_kv_column"]
nn = {c: c[4:6] for c in judged}
stop = {
    "crop01_enc_top_ychips_bars": "no-new-information (L2 crop08 + L3 crop15 shells)",
    "crop02_enc_bottom_emb": "no-new-information (L2 crop10 'Wired N' garble + crop11 shell; word row captured at this scale)",
    "crop03_enc_mid_bars_vlabel": "no-new-information (bars + vertical label fully read; only arrow scaffolding left)",
    "crop04_central_kv": "no-new-information (legend/central reads banked; L2 crop09 covers the column)",
    "crop05_dec_top_bars_attn": "no-new-information (L2 crop12 'SOHmax' stable garble; EDA read is this branch's yield)",
    "crop06_dec_bottom_tokens": "no-new-information (L2 crop13 dup + crop14 edge partials)",
    "crop07_legend": "no-new-information (legend fully read: 3/3 lines)",
    "crop08_ychips_tight": "no-new-information (Y-chip garbles stable at 3x; L3 crop15 shell)",
    "crop09_kv_column": "no-new-information (K real + banked; 'Read Forward' garble adjudicated by judge, no further crop)",
    "crop10_xchips_tight": "no-new-information ('Wired N' garble stable; sibling crop11 shell)",
    "crop11_wordrow_tight": "no-new-information (empty shell - anchor-less word strip, cf. v2 crop06_wordrow_strip)",
    "crop12_softmax_bar": "no-new-information ('SOHmax' ligature garble, stable)",
    "crop13_bottom_tokens": "no-new-information (read dups crop06's Word-and-Position-Encoding)",
    "crop14_big_q": "no-new-information (edge partials + dups; Q glyph-only, anchor-less)",
    "crop15_ynum_chips_right": "no-new-information (empty shell)",
    "crop16_xnum_chips_right": "backstop (16/16 crop cap; 'Wind N' garble would warrant re-crop)",
}

with open(M) as f:
    m = json.load(f)
for n in m["nodes"]:
    cid = n["id"]
    n["parse_call_dir"] = call_of[cid]
    n["novel_strings"] = novel[cid]
    n["stop_reason"] = stop[cid]
    if cid in judged:
        n["judge_files"] = [
            f"judges/crop{nn[cid]}_judge.log",
            f"judges/crop{nn[cid]}_judge_stderr.log",
            f"judges/crop{nn[cid]}_judge_call.log",
        ]
with open(M, "w") as f:
    json.dump(m, f, indent=2)
    f.write("\n")
print("filled:", sum(1 for n in m["nodes"] if n["stop_reason"]), "stop_reasons,",
      sum(1 for n in m["nodes"] if n["parse_call_dir"]), "call dirs,",
      sum(1 for n in m["nodes"] if n["judge_files"]), "judge sets")
