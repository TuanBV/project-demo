"""Handbook ("Sổ tay ôn tập") -- a read-only document viewer, completely independent from
the quiz feature (app/db/models/question.py, app/db/models/study.py), from the JSON seed
data (scripts/data/java_python_mc/*.json, scripts/data/extended_topics/*.json), and from the
practical-review area (app/practical_review/*). No shared state, no shared parser, no shared
templates/static assets.

Its only data source is scripts/data/so_tay_on_tap_de_doc_noi_bat.docx -- a "dễ đọc nổi bật"
(readable/highlighted) formatting of the same 207-question handbook content also used by
practical-review, but this module renders the FULL document per topic (goal, terminology
table, common mistakes, core examples, and every Q&A card) as plain server-rendered pages.
There is no API, no client-side JS, and no progress tracking -- purely a document to read.
"""
