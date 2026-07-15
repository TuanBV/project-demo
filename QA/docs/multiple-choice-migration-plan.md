# Multiple-Choice Migration Plan

## 0. Current state (read before editing)

Read: `CLAUDE.md`, `README.md`, `pyproject.toml`, `app/db/models/*`, `alembic/versions/*`,
`app/api/routes/*`, `app/services/*`, `app/repositories/*`, `app/schemas/*`,
`app/templates/*`, `app/static/js/*`, `tests/*`.

Current flow (free-text, built in the MVP phase):

- `Question` has `reference_answer`, `java_answer`, `python_answer`, `sql_answer`, and a
  rubric of `AnswerConcept` → `ConceptKeyword`, plus `ContradictionRule`.
- `KeywordAnswerEvaluator` (app/evaluation/*) normalizes the submitted free-text answer and
  scores it against the concept/keyword rubric; `ContradictionDetector` applies penalties.
- `StudyService.submit_attempt` calls the evaluator, writes an `Attempt`
  (`submitted_answer`, `normalized_answer`, `score` 0-100, `classification` CORRECT/
  MOSTLY_CORRECT/PARTIALLY_CORRECT/INCORRECT, `evaluation_json`), and updates
  `QuestionProgress` (`attempt_count`, `correct_count`, `average_score`, `best_score`,
  `last_score`, `mastery_level` NEW/LEARNING/REVIEWING/MASTERED, `next_review_at`) via
  `WeightedReviewScheduler`.
- Importers (`DocxTextExtractor`/`PlainTextExtractor` → `QuestionTextParser` →
  `ImportValidationService` → `QuestionImportService`) parse question+reference_answer and
  optionally auto-suggest concepts (`ConceptSuggestionService`).
- Study API (`app/api/routes/questions.py`, `study_sessions.py`) exposes
  `StudyQuestionResponse` (no rubric) and evaluates via `EvaluationService`.
- Web UI: `study.html`/`study.js` render a free-text `<textarea>` + "Chấm điểm" button.
- 20 seed questions exist, all free-text with concepts/keywords, some with contradiction
  rules — this is real data that must not be lost.

## 1. Tables to add / change

| Table | Change |
|---|---|
| `questions` | add `question_format` (enum, default `MULTIPLE_CHOICE`), add `needs_review` (bool, default `False`). Existing free-text columns (`reference_answer`, `java_answer`, `python_answer`, `sql_answer`) are **kept** (used by `question_format=FREE_TEXT`/`CODE`/`SQL` rows going forward, and by legacy data). |
| `question_options` (new) | `id`, `question_id` (FK cascade), `content`, `normalized_content` (indexed, for duplicate detection), `is_correct`, `auto_generated`, `explanation` (nullable), `display_order`, `active`, `created_at`, `updated_at`. Partial unique index `(question_id) WHERE is_correct=1` enforces "at most one correct option" at the DB layer; "exactly one correct + exactly 4 active" is enforced in `QuestionOptionService` inside a transaction (documented in section 4.2 of the request — SQLite can't cheaply express a multi-row COUNT check constraint). |
| `attempts` | add `selected_option_id` (FK nullable), `correct_option_id` (FK nullable), `is_correct` (bool nullable), `answer_order_json` (Text nullable). Make `submitted_answer`, `normalized_answer`, `evaluation_json` **nullable** (were NOT NULL) since MC attempts don't populate them. `score`/`classification` are reused (score: 100/0, classification: CORRECT/INCORRECT — `MOSTLY_CORRECT`/`PARTIALLY_CORRECT` simply never get written by the MC path, enum values stay for legacy row compatibility). |
| `question_progress` | add `incorrect_count`, `accuracy`, `current_correct_streak`, `best_correct_streak`, `last_is_correct`, `last_selected_option_id`. Existing `attempt_count`/`correct_count`/`average_score`/`best_score`/`last_score`/`mastery_level`/`last_reviewed_at`/`next_review_at` are reused. `mastery_level` stays a plain `String` column (no enum constraint in DB), so old values (`REVIEWING`) remain valid rows; new MC logic writes `NEW`/`LEARNING`/`FAMILIAR`/`MASTERED`. |

Because SQLite has limited `ALTER TABLE` support, the Attempt-column-nullability change uses
Alembic **batch mode** (`op.batch_alter_table`), which is enabled project-wide in
`alembic/env.py` (`render_as_batch=True`) so this and future SQLite migrations work
uniformly on SQLite and Postgres.

## 2. APIs that change

| Endpoint | Change |
|---|---|
| `GET /api/questions/{id}`, `GET /api/questions/random`, `GET /api/questions/next` | Response becomes `StudyQuestionResponse` with `options: list[StudyQuestionOptionResponse]` (id + content only, **no** `is_correct`). Options are shuffled server-side per delivery (see §4). Only questions with `question_format=MULTIPLE_CHOICE`, `active=True`, `needs_review=False`, and exactly 4 active options are eligible. |
| `POST /api/study-sessions/{id}/next` | Same response shape as above; persists the shuffled order as a `QuestionDelivery` row keyed by `(session_id, question_id)` so a refresh replays the same order. |
| `POST /api/study-sessions/{id}/questions/{question_id}/answer` (**new**) | Body `{selected_option_id, response_time_seconds}`. Validates session open, question active, option belongs to question, option was part of the delivered set, and the question hasn't already been answered in this session (idempotent: re-submitting after success returns 409, not a silent re-score). Returns per-option `is_selected`/`is_correct` plus `explanation` — **only after** a valid submit. |
| `POST /api/questions/{id}/evaluate` | **Deprecated** for the MC flow (kept only for `FREE_TEXT`/legacy questions so old integrations don't 404 outright); marked `deprecated=True` in OpenAPI. New question creation defaults to MC and this path is not used by the UI anymore. |
| `POST /api/admin/questions`, `PUT .../{id}` | Body gains `options: list[{content, is_correct, explanation?}]` (exactly 4, exactly 1 correct) instead of `concepts`/`contradiction_rules` for MC questions. The old `concepts`/`contradiction_rules` fields remain accepted (optional) for `FREE_TEXT` rows only. |
| `POST /api/admin/questions/generate-distractors` (**new**) | `{question, correct_answer, context?}` → 3 suggested distractors (rule-based). |
| `POST /api/admin/questions/{id}/regenerate-distractors` (**new**) | Regenerates the 3 non-edited auto-generated options for an existing question. |
| `POST /api/admin/questions/{id}/validate` (**new**) | Returns `VALID`/`NEEDS_REVIEW`/`INVALID` + reasons, without changing state. |
| `POST /api/admin/questions/{id}/duplicate` (**new**) | Clones a question + its options (all marked `auto_generated=False`, `active=False`) for editing. |
| `POST /api/admin/import/docx`, `/api/admin/import/text` | Same request shape; response items now include 4 options + which is correct + `NEEDS_REVIEW` status when distractors are auto-generated and unreviewed. |

`SuggestRubricRequest`/`SuggestRubricResponse` and `/suggest-rubric` stay as-is (still useful
for `FREE_TEXT` questions) but are **not** called by the MC admin form.

## 3. Old code kept vs. no longer used by the default flow

**Kept, unchanged, still tested** (module stays, just not on the MC path):
- `app/evaluation/*` (`normalizer.py`, `matcher.py`, `keyword_evaluator.py`,
  `contradiction_detector.py`, `feedback_builder.py`, `base.py`) — still used for
  `question_format=FREE_TEXT` questions via `EvaluationService`/`/evaluate`.
- `app/importers/concept_suggester.py` (`ConceptSuggestionService`) — still used by
  `/api/admin/questions/suggest-rubric` for FREE_TEXT authoring.
- `AnswerConcept`, `ConceptKeyword`, `ContradictionRule` models/tables — untouched, still
  populated for FREE_TEXT questions and for the 20 pre-existing seed questions (converted
  to MC drafts per §5, but their concept rows are left in place, not deleted).
- `app/scheduling/weighted_scheduler.py` (`WeightedReviewScheduler`) — kept for FREE_TEXT
  review scheduling; **not** used by the new default MC study flow.

**New, used by the default (MC) flow**:
- `app/db/models/question_option.py` (`QuestionOption`).
- `app/services/question_option_service.py` (`QuestionOptionService`) — enforces the
  4-option/1-correct invariant transactionally.
- `app/services/option_order_service.py` (`OptionOrderService`) — deterministic per-delivery
  shuffle.
- `app/db/models/question_delivery.py` (`QuestionDelivery`) — records the shown option order
  per `(session_id, question_id)` so refresh doesn't reshuffle.
- `app/importers/distractor_generator.py` (`RuleBasedDistractorGenerator`,
  `DistractorGenerator` Protocol).
- `app/importers/distractor_quality_validator.py` (`DistractorQualityValidator`).
- `app/scheduling/mc_scheduler.py` (`MultipleChoiceReviewScheduler`) — new priority formula
  (§17 of the request) + NEW/LEARNING/FAMILIAR/MASTERED mastery rule.
- `app/evaluation/mc_grader.py` (`MultipleChoiceGrader`) — trivial `selected_option_id ==
  correct_option_id` grading; deliberately has **no** dependency on the keyword evaluator.

Nothing is deleted in this pass — `AnswerEvaluator`/`KeywordAnswerEvaluator` etc. are marked
`@deprecated`-by-docstring for the MC context, not removed, since FREE_TEXT stays a valid
`question_format` and the spec explicitly says not to force a full rewrite.

## 4. Data migration strategy

1. Alembic migration `add_multiple_choice_support`:
   - create `question_options` (+ partial unique index on `is_correct`).
   - create `question_deliveries` (session_id, question_id, option_order_json, created_at;
     unique on `(session_id, question_id)`).
   - add `question_format` (default `MULTIPLE_CHOICE` server-side default for new rows) and
     `needs_review` (default `False`) to `questions`.
   - add `incorrect_count`, `accuracy`, `current_correct_streak`, `best_correct_streak`,
     `last_is_correct`, `last_selected_option_id` to `question_progress`.
   - batch-alter `attempts`: add `selected_option_id`, `correct_option_id`, `is_correct`,
     `answer_order_json`; relax `submitted_answer`/`normalized_answer`/`evaluation_json` to
     nullable.
   - **backfill existing rows**: set `question_format='FREE_TEXT'` for all 20 existing
     questions (they keep their concepts/keywords and stay exactly as usable as before via
     `/evaluate`) — the migration does **not** flip them to MC or touch `active`/content.
2. Separate, explicit, opt-in step (not part of the schema migration): CLI script
   `scripts/convert_free_text_questions.py` converts FREE_TEXT questions to MC drafts:
   - `--dry-run`: report only, no writes.
   - default run: for each FREE_TEXT question, create 1 correct option from
     `reference_answer` + 3 rule-based distractor drafts (`auto_generated=True`), set
     `question_format=MULTIPLE_CHOICE`, `needs_review=True`, `active=False` (so it never
     appears in study until an admin reviews it in `/admin/questions`).
   - `--generate-distractors`: force regeneration of distractors even if some already exist.
   - Never deletes `reference_answer`/concepts/keywords — they stay as historical context
     visible in the admin edit screen.
   - Reports: total free-text questions, converted, needs-review, errored.
3. Old `Attempt` rows (`submitted_answer` populated, `selected_option_id` NULL) remain
   readable in history; the history UI renders them using their existing `evaluation_json`/
   `classification` fields exactly as before (branch on `selected_option_id is None`).

No destructive operation is ever run against `answer_concepts`, `concept_keywords`,
`contradiction_rules`, or `attempts.submitted_answer`.

## 5. Config

New settings in `app/core/config.py` / `.env.example`: `default_question_format`,
`multiple_choice_option_count` (=4, validation still hard-requires exactly 4 regardless),
`multiple_choice_correct_option_count` (=1), `shuffle_question_options`,
`allow_option_reselection_before_submit`, `allow_answer_change_after_submit`,
`practice_reveal_answer_immediately`, `exam_reveal_answer_immediately`,
`auto_generated_questions_active`, `distractor_generator_mode`.

## 6. Phased implementation order

Phase 2 DB → Phase 3 Admin → Phase 4 Study API → Phase 5 Progress → Phase 6 Import →
Phase 7 UI → Phase 8 legacy conversion script → Phase 9 docs/quality gate. Tracked live in
this file's checklist below.

### Checklist
- [x] Phase 1: analysis + this plan
- [x] Phase 2: `question_format`/`needs_review`, `QuestionOption`, `QuestionDelivery`,
      Attempt fields, migration, model-level tests
- [x] Phase 3: `QuestionOptionService`, admin CRUD + validate/duplicate/generate-distractors,
      manual entry form
- [x] Phase 4: Study DTOs, `OptionOrderService`, answer endpoint, idempotency
- [x] Phase 5: `MultipleChoiceReviewScheduler`, progress fields, dashboard
- [x] Phase 6: text A/B/C/D + OPTION/CORRECT_OPTION parser, DOCX distractor pipeline,
      `DistractorQualityValidator`, preview updates
- [x] Phase 7: UI (radio options, submit/next flow, keyboard shortcuts, history)
- [x] Phase 8: `scripts/convert_free_text_questions.py`
- [x] Phase 9: README/CLAUDE.md/OpenAPI + full quality gate
