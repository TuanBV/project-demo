---
paths:
  - "app/services/question_option_service.py"
  - "app/services/study_service.py"
  - "app/services/option_order_service.py"
  - "app/schemas/study.py"
  - "app/schemas/question.py"
  - "app/api/routes/questions.py"
  - "app/api/routes/study_sessions.py"
---

# Multiple-choice integrity invariants

These invariants protect the core study-flow guarantee: a learner can never see or influence
the correct answer before submitting, and grading can never be spoofed by the client.

- **Exactly 4 options, exactly 1 correct, for every active question.** Enforced at three
  layers — Pydantic (`app/schemas/question.py::_validate_option_set`), service
  (`QuestionOptionService.validate_and_build`), and DB (partial unique index
  `ux_question_options_one_correct` on `question_options`). Don't remove or weaken any layer;
  removing one still leaves invalid states reachable through the others.
- **Never leak the answer through the Study API.** `StudyQuestionResponse` /
  `StudyQuestionOptionResponse` must never gain a field like `is_correct`,
  `correct_option_id`, `reference_answer`, `concepts`, `keywords`, `contradiction_rules`,
  `java_answer`, `python_answer`, or `sql_answer`. Only the admin-facing
  `AdminQuestionResponse` / `QuestionOptionResponse` may contain `is_correct`.
- **Options are shuffled server-side only**, via `OptionOrderService`. Never shuffle in
  JavaScript. Order must stay stable within a session — persisted in `QuestionDelivery` — not
  re-randomized on every `/next` call.
- **Never trust `is_correct` or a grading result sent by the client.**
  `StudyService.submit_option_answer` always looks up `correct_option_id` from the database
  and compares it server-side against the submitted `selected_option_id`.
- **Auto-generated distractors must never be active.** Any code path that creates options
  automatically (import without explicit options, `regenerate-distractors`,
  `convert_free_text_questions.py`) must set `needs_review=True, active=False` until an admin
  approves via `PUT` or `/validate` returns `VALID`.
- When touching `QuestionOptionService.replace_options`, keep the `session.flush()` call
  immediately after `question.options.clear()` — removing it reintroduces a transient
  violation of the partial unique index caused by SQLAlchemy's flush ordering.
