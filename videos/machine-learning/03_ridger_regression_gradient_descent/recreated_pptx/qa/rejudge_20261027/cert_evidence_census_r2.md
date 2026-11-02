# cert_evidence_census_r2.md — deck-03 rejudge census (r2)

Generated 2026-11-01T23:04:36.188183Z by read-only census worker. Namespace: `videos/machine-learning/03_ridger_regression_gradient_descent`. DB opened read-only (`mode=ro`). No writes to DB, pptx, deck, reports, or register.

Method: for each slide, scanned `recreated_pptx/qa/slideNNN` and `recreated_pptx/qa/rejudge_20261027/slideNNN` for files whose name matches a leg (`full` / `crop`) and that contain an explicit `FINAL VERDICT: PASS|FAIL`; picked the newest by mtime per leg. Cross-checked against the read-only DB row (gen_status, visual_check, visual_attempts, visual_transcript).

| # | full-leg newest verdict file | full verdict | crop-leg newest verdict file | crop verdict | DB gen_status | DB visual_check | DB att | DB transcript on disk? | flags |
|---|---|---|---|---|---|---|---|---|---|
| 1 | recreated_pptx/qa/rejudge_20261027/slide001/judge_full_w4.txt | FAIL | recreated_pptx/qa/slide001/crop_1_preparedby_judge.txt | PASS | passed | PASS | 2 | yes | NEWEST-VERDICT-NOT-PASS |
| 2 | recreated_pptx/qa/rejudge_20261027/slide002/judge_full.txt | PASS | recreated_pptx/qa/slide002/crop_payload_B.txt | PASS | passed | PASS | 2 | yes | ok |
| 3 | recreated_pptx/qa/slide003/judge_attempt_5_a_fullslide.txt | FAIL | recreated_pptx/qa/slide003/judge_prompt_5_crop.txt | PASS | passed | PASS | 35 | yes | NEWEST-VERDICT-NOT-PASS |
| 4 | recreated_pptx/qa/rejudge_20261027/slide004/judge_full_r20.txt | PASS | recreated_pptx/qa/slide004/crop_prompt_2_bottom.txt | PASS | passed | PASS | 10 | yes | ok |
| 5 | recreated_pptx/qa/rejudge_20261027/slide005/judge_full_r19.txt | PASS | recreated_pptx/qa/slide005/crop_prompt_4_eqstack.txt | PASS | passed | PASS | 15 | yes | ok |
| 6 | recreated_pptx/qa/rejudge_20261027/slide006/judge_full_r19.txt | PASS | recreated_pptx/qa/slide006/crop_1_subtitle_judge.txt | PASS | passed | PASS | 2 | yes | ok |
| 7 | recreated_pptx/qa/rejudge_20261027/slide007/judge_full_r20.txt | PASS | recreated_pptx/qa/slide007/crop_prompt_1_title.txt | PASS | passed | PASS | 3 | yes | ok |
| 8 | recreated_pptx/qa/rejudge_20261027/slide008/judge_full_r20.txt | PASS | recreated_pptx/qa/slide008/crop_1_subtitle_judge.txt | PASS | passed | PASS | 4 | yes | ok |
| 9 | recreated_pptx/qa/rejudge_20261027/slide009/judge_full_r20.txt | PASS | recreated_pptx/qa/slide009/crop_6_chart_right_judge.txt | FAIL | passed | PASS | 7 | yes | NEWEST-VERDICT-NOT-PASS |
| 10 | recreated_pptx/qa/rejudge_20261027/slide010/judge_full_retry.txt | PASS | recreated_pptx/qa/slide010/crop_3_cap_right_judge.txt | PASS | passed | PASS | 3 | yes | ok |
| 11 | recreated_pptx/qa/rejudge_20261027/slide011/judge_full_r16_r22.txt | PASS | recreated_pptx/qa/slide011/crop_1_subtitle_judge.txt | PASS | passed | PASS | 2 | yes | ok |
| 12 | recreated_pptx/qa/rejudge_20261027/slide012/judge_full.txt | FAIL | recreated_pptx/qa/slide012/crop_2_perfect_table_judge.txt | PASS | passed | PASS | 4 | yes | NEWEST-VERDICT-NOT-PASS |
| 13 | recreated_pptx/qa/rejudge_20261027/slide013/judge_full_r20.txt | PASS | recreated_pptx/qa/slide013/crop_6_wbox2_judge.txt | PASS | passed | PASS | 6 | yes | ok |
| 14 | recreated_pptx/qa/slide014/judge_att8_full.txt | PASS | recreated_pptx/qa/slide014/judge_att8_crop.txt | PASS | passed | PASS | 8 | n/a (empty) | DB-TRANSCRIPT-EMPTY |
| 15 | recreated_pptx/qa/rejudge_20261027/slide015/judge_full_r17.txt | FAIL | recreated_pptx/qa/rejudge_20261027/slide015/crop_dense_judge_r20.txt | FAIL | passed | PASS | 7 | n/a (empty) | NEWEST-VERDICT-NOT-PASS, DB-TRANSCRIPT-EMPTY |
| 16 | recreated_pptx/qa/slide016/crop_8_full_body_judge.txt | FAIL | recreated_pptx/qa/slide016/crop_8_full_body_judge.txt | FAIL | passed | PASS | 9 | n/a (empty) | NEWEST-VERDICT-NOT-PASS, DB-TRANSCRIPT-EMPTY |
| 17 | recreated_pptx/qa/rejudge_20261027/slide17/judge_full_w8.txt | PASS | recreated_pptx/qa/slide017/crop_5_wbox_judge_prompt_5.txt | PASS | passed | PASS | 5 | yes | ok |
| 18 | recreated_pptx/qa/rejudge_20261027/slide018/judge_full_r20.txt | FAIL | recreated_pptx/qa/slide018/crop_5_wbox_judge_prompt_5.txt | PASS | passed | PASS | 5 | yes | NEWEST-VERDICT-NOT-PASS |
| 19 | recreated_pptx/qa/rejudge_20261027/slide019/judge_full_wfix.txt | PASS | recreated_pptx/qa/slide019/crop_27_table_left_judge.txt | PASS | passed | PASS | 0 | yes | ok |
| 20 | recreated_pptx/qa/rejudge_20261027/slide020/judge_full_r21.txt | PASS | recreated_pptx/qa/slide020/crop_1_title_prompt.txt | PASS | passed | PASS | 4 | yes | ok |
| 21 | recreated_pptx/qa/rejudge_20261027/slide021/judge_full_r20.txt | PASS | recreated_pptx/qa/slide021/crop_ps_main_eq_judge.txt | FAIL | passed | PASS | 13 | yes | NEWEST-VERDICT-NOT-PASS |
| 22 | recreated_pptx/qa/rejudge_20261027/slide022/judge_full_fresh.txt | PASS | recreated_pptx/qa/slide022/crop_1_title_prompt.txt | PASS | passed | PASS | 2 | yes | ok |
| 23 | recreated_pptx/qa/rejudge_20261027/slide023/judge_full_r21.txt | FAIL | recreated_pptx/qa/slide023/crop_prompt_2_solution.txt | PASS | passed | PASS | 8 | yes | NEWEST-VERDICT-NOT-PASS |
| 24 | recreated_pptx/qa/rejudge_20261027/slide024/judge_full_r17.txt | PASS | recreated_pptx/qa/slide024/crop_prompt_1_title.txt | PASS | passed | PASS | 3 | yes | ok |
| 25 | recreated_pptx/qa/rejudge_20261027/slide025/judge_full_k17z3.txt | FAIL | recreated_pptx/qa/slide025/crop_5_bl_nonconvex_judge.txt | FAIL | building |  | 4 | n/a (empty) | NEWEST-VERDICT-NOT-PASS, DB-TRANSCRIPT-EMPTY |
| 26 | recreated_pptx/qa/rejudge_20261027/slide026/judge_full_r18.txt | PASS | recreated_pptx/qa/slide026/judge_prompt_1_crop_notes.txt | PASS | passed | PASS | 6 | no | TRANSCRIPT-MISSING-ON-DISK |
| 27 | recreated_pptx/qa/slide027/dispatch_B_10_chain_full.sh | PASS | recreated_pptx/qa/slide027/crop_prompt_7_min_cluster.txt | PASS | passed | PASS | 11 | no | TRANSCRIPT-MISSING-ON-DISK |
| 28 | recreated_pptx/qa/rejudge_20261027/slide028/judge_full_retry.txt | FAIL | recreated_pptx/qa/slide028/crop_4_right_curve_judge.txt | FAIL | passed | PASS | 9 | yes | NEWEST-VERDICT-NOT-PASS |
| 29 | recreated_pptx/qa/rejudge_20261027/slide029/judge_full_r21.txt | PASS | recreated_pptx/qa/slide029/crop_1_title_refutation.txt | PASS | passed | PASS | 2 | yes | ok |
| 30 | recreated_pptx/qa/rejudge_20261027/slide030/judge_full_w03_snap.txt | FAIL | recreated_pptx/qa/slide030/crop_prompt_6_plot.txt | PASS | passed | PASS | 25 | yes | NEWEST-VERDICT-NOT-PASS |
| 31 | recreated_pptx/qa/rejudge_20261027/slide031/judge_full_r21.txt | PASS | recreated_pptx/qa/slide031/crop_34_graph_judge.txt | PASS | passed | PASS | 34 | yes | ok |
| 32 | recreated_pptx/qa/rejudge_20261027/slide032/judge_full_r21.txt | PASS | recreated_pptx/qa/slide032/crop_9_graph_judge.txt | FAIL | passed | PASS | 25 | yes | NEWEST-VERDICT-NOT-PASS |
| 33 | recreated_pptx/qa/rejudge_20261027/slide033/judge_full_w03_snap.txt | FAIL | recreated_pptx/qa/slide033/judge_crop_prompt_3.txt | PASS | passed | PASS | 25 | yes | NEWEST-VERDICT-NOT-PASS |
| 34 | recreated_pptx/qa/rejudge_20261027/slide034/judge_full_w03_snap.txt | PASS | recreated_pptx/qa/slide034/judge_crops_1.sh | PASS | passed | PASS | 3 | yes | ok |
| 35 | recreated_pptx/qa/rejudge_20261027/slide035/judge_full_r20.txt | PASS | recreated_pptx/qa/slide035/crop_payload_B.txt | PASS | passed | PASS | 1 | yes | ok |
| 36 | recreated_pptx/qa/rejudge_20261027/slide036/judge_full_r21.txt | PASS | recreated_pptx/qa/slide036/judge_prompt_1_crop_eq_stack.txt | PASS | passed | PASS | 8 | yes | ok |
| 37 | recreated_pptx/qa/rejudge_20261027/slide037/judge_full_r20.txt | FAIL | recreated_pptx/qa/slide037/crop_6_green_box_judge.txt | PASS | passed | PASS | 6 | yes | NEWEST-VERDICT-NOT-PASS |
| 38 | recreated_pptx/qa/rejudge_20261027/slide038/judge_full_r20.txt | PASS | recreated_pptx/qa/slide038/crop_1_title_l1l2_judge_confirm.txt | PASS | passed | PASS | 2 | yes | ok |
| 39 | recreated_pptx/qa/rejudge_20261027/slide039/judge_full_fresh.txt | FAIL | recreated_pptx/qa/slide039/crop_prompt_1_title_lines.txt | PASS | passed | PASS | 3 | yes | NEWEST-VERDICT-NOT-PASS |
| 40 | recreated_pptx/qa/rejudge_20261027/slide040/judge_full_fresh.txt | PASS | recreated_pptx/qa/slide040/crop_prompt_3_title_block.txt | PASS | passed | PASS | 4 | yes | ok |
| 41 | recreated_pptx/qa/rejudge_20261027/slide041/judge_full_r21.txt | PASS | recreated_pptx/qa/slide041/crop_5_plot_judge.txt | PASS | passed | PASS | 5 | yes | ok |
| 42 | recreated_pptx/qa/rejudge_20261027/slide042/judge_full_r18.txt | PASS | recreated_pptx/qa/slide042/crop_25_topright_prompt.txt | PASS | passed | PASS | 25 | yes | ok |
| 43 | recreated_pptx/qa/slide043/judge_att4_full.txt | PASS | recreated_pptx/qa/slide043/crop_prompt_eqstack.txt | PASS | passed | PASS | 1 | n/a (empty) | DB-TRANSCRIPT-EMPTY |
| 44 | recreated_pptx/qa/slide044/judge_att1_full.txt | PASS | recreated_pptx/qa/slide044/crop_prompt_1_centretext.txt | PASS | passed | PASS | 0 | n/a (empty) | DB-TRANSCRIPT-EMPTY |
| 45 | recreated_pptx/qa/rejudge_20261027/slide045/judge_full_r19.txt | FAIL | recreated_pptx/qa/slide045/pil_adjudication_crop_augtable_r3.md | FAIL | passed | PASS | 4 | yes | NEWEST-VERDICT-NOT-PASS |
| 46 | recreated_pptx/qa/rejudge_20261027/slide046/judge_full_fresh2.txt | FAIL | recreated_pptx/qa/slide046/crop_4_zmatrix_judge.txt | PASS | passed | PASS | 4 | yes | NEWEST-VERDICT-NOT-PASS |
| 47 | recreated_pptx/qa/rejudge_20261027/slide047/judge_full_r21.txt | FAIL | recreated_pptx/qa/slide047/crop_prompt_6_button.txt | PASS | passed | PASS | 6 | yes | NEWEST-VERDICT-NOT-PASS |
| 48 | recreated_pptx/qa/rejudge_20261027/slide048/judge_full_r18.txt | FAIL | recreated_pptx/qa/slide048/crop_9_top_band_judge.txt | FAIL | passed | PASS | 0 | n/a (empty) | NEWEST-VERDICT-NOT-PASS, DB-TRANSCRIPT-EMPTY |
| 49 | recreated_pptx/qa/rejudge_20261027/slide049/judge_full_fresh.txt | FAIL | recreated_pptx/qa/slide049/crop_18_top_band_judge.txt | PASS | passed | PASS | 18 | yes | NEWEST-VERDICT-NOT-PASS |
| 50 | recreated_pptx/qa/rejudge_20261027/slide050/judge_full_r18.txt | FAIL | recreated_pptx/qa/slide050/crop_9_caption_judge.txt | PASS | passed | PASS | 20 | yes | NEWEST-VERDICT-NOT-PASS |
| 51 | recreated_pptx/qa/rejudge_20261027/slide051/judge_full_w2.txt | FAIL | recreated_pptx/qa/slide051/crop_attempt_2_promptB.txt | PASS | passed | PASS | 5 | yes | NEWEST-VERDICT-NOT-PASS |

## Gaps / flags

- Certified slides (DB visual_check=PASS) whose DB `visual_transcript` path(s) are missing on disk: **2** -> [26, 27]
- Slides whose newest on-disk verdict for either leg is not PASS (pointer only; register ownership stays with the census agent): **23** -> [1, 3, 9, 12, 15, 16, 18, 21, 23, 25, 28, 30, 32, 33, 37, 39, 45, 46, 47, 48, 49, 50, 51]
- Slides with DB visual_transcript empty: **[14, 15, 16, 25, 43, 44, 48]**

