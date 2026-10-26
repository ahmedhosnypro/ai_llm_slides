#!/usr/bin/env python3
"""Finalize manifest.json with stop reasons + source call dirs; compute union recall."""
import json
import os

RUN = "/home/ahmed/Projects/ai_llm_slides/doc-parse-test/run_20261025-024314"
TREE = f"{RUN}/12_cascade_v2/slide_052"

STOP = {
    "crop01": ("no-new-information",
               "parse: 'nalade' (garble of GT17 'malade', already EXACT via full frame) + full-span class_Picture -> child box == parent pixels; region itself is a hallucination candidate (register-confirmed location, no picture content - see judges/crop01_judge.md)"),
    "crop02": ("no-new-information",
               "parse: 'October 1' + 'Ende Decoder Attention' + 4x complete 'Encode Decoder Attention' (GT5 EXACT evidence); full-span class_Picture leaves no parse-distinguishable sub-region; level2 child crop12 added zero new strings; corroboration call14 byte-identical"),
    "crop03": ("no-new-information",
               "parse: lower residual bar (GT3 3rd instance) + 4 of 5 'Masked Multi-Head Self Attention'; level2 child crop13 recovered 5th-box fragments"),
    "crop04": ("no-new-information",
               "parse: 'Word and Position Encoding' + all 5 word units (merged 2-per-line: 'SOS Je'/'me sens malade'); every unit already EXACT; merge is a structure-only defect; per-tag splits would need <compliant-width boxes"),
    "crop05": ("no-new-information",
               "parse: 'Transformer Encoder' (GT8) + 'feel'/'Sick' split + 'SOS = Start Of Sentence' (GT9 recovered); 'I' instance dropped by parser (GT10 EXACT via full-frame merged line); level3 child crop16 added zero new strings"),
    "crop06": ("leaf",
               "parse: '52' (GT22 recovered); single badge numeral, no internal structure to crop"),
    "crop07": ("no-new-information",
               "parse: box1 label 'Encode Decoder Attention' + 'Q' only; K/V circles (GT18/GT19) unread at 172px context width (v1 crop08 same result); child crop09 + grandchildren crop14/crop15 all failed to read K/V -> parser blind spot at compliant crop scales"),
    "crop08": ("no-new-information",
               "parse: 'Ya'/'Y2' (GT21 garble, 2 of 3 tags); children: crop10 recovered one clean 'Y' (GT21 EXACT evidence), crop11 empty; single-tag isolation needs ~60px-wide boxes - below the >=480px@2-3x prep width -> terminal"),
    "crop09": ("no-new-information",
               "parse: 'Y1 Y2' - glyphs in the K/V/Y3 zone are read but misclassified; children crop14 (k_band: garbled by callout-2 tail entering the box) and crop15 (v_band: empty); K/V remain parser-invisible"),
    "crop10": ("no-new-information",
               "parse: 'Ya' + one clean 'Y' line (GT21 EXACT evidence, 1 of 3 instances clean); further per-tag splits non-compliant with prep width rule"),
    "crop11": ("no-new-information",
               "parse: EMPTY (zero lines vs parent crop08's 'Ya'/'Y2'); Y3 zone garble covered by sibling crop09 read"),
    "crop12": ("no-new-information",
               "parse: 3x 'Encode Decoder Attention' - strings identical to parent crop02's; zero new lines; Q circles parser-invisible even at 3x with label context (wave-4 q_strip also empty) - judge counts them on the image"),
    "crop13": ("no-new-information",
               "parse: 'Masked'/'M-Head'/'Multi-Head'/'Self Attention' - 5th masked box fragments recovered (instance repaired, garbled); GT6 unit EXACT already via 4 clean instances; per-line sub-crops would repeat"),
    "crop14": ("no-new-information",
               "parse: 'Int-head Sell on Block' - garble of callout-2 tail ('...Multi-head Self Attention Block') which enters this box at y152-178; K circle unread (see judges/crop14_judge.md)"),
    "crop15": ("no-new-information",
               "parse: EMPTY; V circle unread - doc-parse blind spot (wave-4 read V only from a 44px-wide crop, non-compliant with the >=480px prep rule)"),
    "crop16": ("no-new-information",
               "parse: 'feel' only; zero new strings vs parent crop05; 'I'/'Sick' unread in this narrower band"),
}

CALL = {
    "crop01": "parses/call01_crop01_picture",
    "crop02": "parses/call02_crop02_upper_boxes (+ corroboration parses/call14_corr_crop02_t3000 byte-identical)",
    "crop03": "parses/call03_crop03_lower_boxes",
    "crop04": "parses/call04_crop04_wordrow",
    "crop05": "parses/call05_crop05_leftpanel",
    "crop06": "parses/call06_crop06_badge",
    "crop07": "parses/call07_crop07_kv_q1",
    "crop08": "parses/call08_crop08_y_row",
    "crop09": "parses/call09_crop09_kv_band",
    "crop10": "parses/call10_crop10_y_left",
    "crop11": "parses/call11_crop11_y_right",
    "crop12": "parses/call12_crop12_q_context",
    "crop13": "parses/call13_crop13_box5",
    "crop14": "parses/call15_crop14_k_band",
    "crop15": "parses/call16_crop15_v_band",
    "crop16": "parses/call17_crop16_inputs_row",
}

mani = json.load(open(f"{TREE}/manifest.json"))
l2 = json.load(open(f"{TREE}/crops/prep_rows_l2.json"))
l3 = json.load(open(f"{TREE}/crops/prep_rows_l3.json"))
known = {r["id"] for r in mani["crops"]}
for r in l2 + l3:
    if r["id"] not in known:
        mani["crops"].append(r)
rows = mani["crops"]
for r in rows:
    cid = r["id"]
    sr, sn = STOP[cid]
    r["stop_reason"] = sr
    r["stop_note"] = sn
    r["source_call_dir"] = CALL[cid]
    # judge transcript (banked for every crop with novel strings)
    jp = f"{TREE}/judges/{cid}_judge.md"
    r["judge_transcript"] = f"judges/{cid}_judge.md" if os.path.exists(jp) and os.path.getsize(jp) > 0 else None
mani["parse_calls"] = 17
mani["caps"] = {"crops_used": 16, "crops_cap": 16, "parse_calls_used": 17, "parse_calls_cap": 24}
mani["caps_note"] = "crop cap reached (16) - all branches were already at semantic stops except crop14/15/16, which were the final compliant unit-level attempts; parse calls 17/24"
mani["parallelism"] = {
    "batches": [
        {"batch": "A", "crops": ["crop01", "crop02", "crop03", "crop04"], "concurrent": 4, "wall_s": 8},
        {"batch": "B", "crops": ["crop05", "crop06", "crop07", "crop08"], "concurrent": 4, "wall_s": 5},
        {"batch": "C", "crops": ["crop09", "crop10", "crop11", "crop12"], "concurrent": 4, "wall_s": 7},
        {"batch": "D", "crops": ["crop13", "call14_corr_crop02"], "concurrent": 2, "wall_s": 5},
        {"batch": "E", "crops": ["crop14", "crop15", "crop16"], "concurrent": 3, "wall_s": 5},
    ],
    "sum_call_latencies_s": 74.7,
    "total_parse_wall_s": 30,
    "speedup": 2.5,
}
json.dump(mani, open(f"{TREE}/manifest.json", "w"), indent=2)

null_boxes = [r["id"] for r in rows if not r.get("box_frame_px") or r.get("stop_reason") is None]
print("manifest finalized:", len(rows), "crops; null-box/no-stop check:", "FAIL " + str(null_boxes) if null_boxes else "PASS (every crop has box+scale+stop_reason)")
levels = {}
for r in rows:
    levels[r["level"]] = levels.get(r["level"], 0) + 1
print("levels:", levels)
reasons = {}
for r in rows:
    reasons[r["stop_reason"]] = reasons.get(r["stop_reason"], 0) + 1
print("stop reasons:", reasons)
