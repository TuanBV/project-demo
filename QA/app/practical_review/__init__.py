"""Practical Review ("Ôn lý thuyết thực chiến") -- a self-contained study-guide area with
no dependency on the multiple-choice quiz feature (app/db/models/question.py,
app/db/models/study.py), no dependency on the JSON seed data
(scripts/data/java_python_mc/*.json, scripts/data/extended_topics/*.json), and no shared
state with StudySession/Attempt. Its only data source is
scripts/data/so_tay_on_tap_sap_xep_theo_chu_de_uu_tien.docx.

Progress tracking for this area lives entirely client-side in localStorage
(namespace "practicalReview.*") -- there is no server-side progress model here.
"""
