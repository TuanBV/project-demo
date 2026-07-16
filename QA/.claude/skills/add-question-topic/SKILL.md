---
name: add-question-topic
description: Add a new category's worth of multiple-choice questions to the seed data (e.g. "add 20 questions about topic X"). Use for bulk-adding hand-authored or researched MC question content, not for one-off admin entry.
allowed-tools: Read, Write, Edit, Bash(python scripts/seed_extended_topics.py), Bash(pytest tests/unit/scripts*)
---

This project's bulk MC content lives as JSON per category under `scripts/data/extended_topics/`
(one file per category, loaded by `scripts/seed_extended_topics.py`) and
`scripts/data/java_python_mc/` (loaded by `scripts/seed_java_python_mc.py`, 11 categories from
the original Java/Python interview bank). Both scripts are idempotent (dedup by
`content_hash`) and both run in the `Dockerfile` `CMD` on every container start.

1. Decide which script/directory the new category belongs in. For a genuinely new topic not
   already covered, add a new JSON file under `scripts/data/extended_topics/<topic_slug>.json`.
2. Each question object must be exactly:
   `{"content": "...", "explanation": "...", "options": [{"content": "...", "is_correct": bool} x4]}`
   — exactly 4 options, exactly 1 `is_correct: true`. Write distractors that are plausible but
   clearly wrong to someone who understands the concept: avoid generic catch-alls ("all of the
   above"), avoid mechanical negation of the correct answer, avoid two options that could both
   be argued correct, avoid making the correct answer noticeably longer/shorter than the others.
3. Register the new category in `_TOPIC_TO_CATEGORY` in `scripts/seed_extended_topics.py`
   (key = filename without `.json`, value = category display name).
4. Validate before seeding: parse the JSON and check every question has exactly 4 options,
   exactly 1 correct, and no duplicate `content` within the file.
5. Run `python scripts/seed_extended_topics.py` against the dev DB and confirm the new
   category's count in the printed summary; re-run once more to confirm it reports the same
   questions as already existing (idempotency).
6. Update or add a test in `tests/unit/scripts/test_seed_extended_topics.py` (structure
   validation + updated total-question-count assertion) and run
   `pytest tests/unit/scripts`.
7. If the change should persist into fresh Docker deployments (it already does automatically
   via the `Dockerfile` `CMD` chain), verify with the `docker-verify` skill.
