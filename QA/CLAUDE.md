# CLAUDE.md — Interview Review System

Hướng dẫn cho Claude Code (và bất kỳ ai) khi làm việc tiếp trên repository này.

## Tổng quan dự án

Web app ôn tập câu hỏi phỏng vấn Junior Developer. **Luồng học mặc định là trắc nghiệm 4 đáp
án** (`question_format=MULTIPLE_CHOICE`): mỗi câu có đúng 4 lựa chọn, đúng 1 đáp án đúng,
backend xáo trộn thứ tự, chấm đúng/sai tức thì dựa trên `selected_option_id` so với
`correct_option_id` lấy từ database (không tin `is_correct` từ client). Free-text keyword/
fuzzy/contradiction evaluator (`app/evaluation/*`) được **giữ lại nguyên vẹn** cho
`question_format=FREE_TEXT` (dữ liệu cũ, endpoint `/evaluate` và `/attempts` đã đánh dấu
`deprecated=True`) — không xóa, không dùng trong luồng học chính.

Admin nạp câu hỏi qua DOCX, dán text (nhiều định dạng), hoặc nhập tay. Câu hỏi chỉ có
question+correct-answer (không đủ 4 lựa chọn) được tự động sinh 3 đáp án sai
(`RuleBasedDistractorGenerator`) và LUÔN ở trạng thái `needs_review=True, active=False` cho
đến khi admin duyệt.

Xem `docs/architecture.md` (kiến trúc gốc), `docs/implementation-plan.md` (tiến độ MVP ban
đầu), và `docs/multiple-choice-migration-plan.md` (kế hoạch + quyết định khi chuyển sang
trắc nghiệm — đọc file này trước khi đổi bất cứ gì liên quan đến `QuestionOption`/
`question_format`).

## Kiến trúc (tóm tắt)

```
API routes -> Services -> Repositories -> DB models
                       -> Evaluation (pure, no FastAPI/SQLAlchemy) -- FREE_TEXT only
                       -> Importers  (pure, no DB)
                       -> Scheduling (pure) -- MultipleChoiceReviewScheduler (mặc định)
                                             -- WeightedReviewScheduler (legacy FREE_TEXT)
```

- `app/evaluation/*` và `app/importers/*` KHÔNG được import FastAPI hoặc SQLAlchemy.
- `app/evaluation/mc_grader.py::MultipleChoiceGrader` là bộ chấm MC (so sánh ID, không phụ
  thuộc TextNormalizer/KeywordMatcher) — dùng cho luồng chính.
- DOCX và pasted-text dùng chung `QuestionTextParser` (`app/importers/text_parser.py`) →
  `StructuredTextParser` (CATEGORY/QUESTION/ANSWER **hoặc** CATEGORY/QUESTION/A-B-C-D/CORRECT
  **hoặc** CATEGORY/QUESTION/OPTION×4/CORRECT_OPTION) hoặc `InterviewDocumentParser`
  (PHẦN/Câu/Trả lời). Không tạo parser thứ hai có logic nhận diện câu hỏi trùng lặp.
- `QuestionOptionService` là nơi DUY NHẤT enforce "đúng 4 option, đúng 1 đáp án đúng, không
  trùng nội dung" — validate xong mới mutate (an toàn khi rollback), và luôn `flush()` sau
  khi `question.options.clear()` trước khi append option mới (tránh vi phạm partial unique
  index `ux_question_options_one_correct` do thứ tự flush của SQLAlchemy).
- `OptionOrderService` xáo trộn option bằng seed `(question_id, session_id, attempt_token)`;
  `StudyService` lưu kết quả vào bảng `question_deliveries` để refresh trong cùng phiên không
  đổi thứ tự.
- CLI scripts (`scripts/import_docx.py`, `scripts/import_text.py`, `scripts/seed.py`,
  `scripts/convert_free_text_questions.py`) gọi thẳng service — không sao chép business logic.

## Lệnh thường dùng

```bash
# venv + cài đặt
python -m venv .venv && source .venv/Scripts/activate   # Windows Git Bash
pip install -e ".[dev]"

# Migration & seed
alembic upgrade head
python scripts/seed.py
python scripts/convert_free_text_questions.py --dry-run   # xem trước khi chuyển dữ liệu cũ
python scripts/convert_free_text_questions.py --generate-distractors

# Chạy server
uvicorn app.main:app --reload

# Quality gate (bắt buộc chạy sau khi sửa evaluator/importer/model/shuffle/submit logic)
ruff format .
ruff check .
mypy app
pytest --cov=app --cov-report=term-missing

# Hoặc gọn hơn:
make check
```

## Quy tắc repository (bắt buộc tuân theo)

1. **Không đặt business logic trong route.** Route chỉ parse request, gọi service, map
   sang schema. Logic thuộc về `app/services/*`.
2. **Mỗi câu hỏi active phải có đúng 4 option, đúng 1 đáp án đúng.** Validate ở cả 3 lớp:
   Pydantic (`app/schemas/question.py::_validate_option_set`), service
   (`QuestionOptionService.validate_and_build`), và DB (partial unique index trên
   `question_options`). Không bỏ bớt lớp nào.
3. **Không làm lộ đáp án qua Study API.** `StudyQuestionResponse`/`StudyQuestionOptionResponse`
   không bao giờ được thêm field `is_correct`/`correct_option_id`/`reference_answer`/
   `concepts`/`keywords`/`contradiction_rules`/`java_answer`/`python_answer`/`sql_answer`.
   Chỉ `AdminQuestionResponse`/`QuestionOptionResponse` (admin) mới chứa `is_correct`.
4. **Option phải được xáo trộn ở backend** (`OptionOrderService`), không random bằng
   JavaScript. Thứ tự phải ổn định trong cùng session (dùng `QuestionDelivery`, không tạo
   shuffle mới mỗi lần gọi `/next`).
5. **Không bao giờ tin `is_correct`/kết quả chấm từ client.** `submit_option_answer` luôn tự
   tra `correct_option_id` từ DB và so sánh với `selected_option_id` phía server.
6. **Không thực thi code hoặc SQL không tin cậy.** `DisabledCodeRunner`/`DisabledSqlEvaluator`
   (khi thêm) phải luôn trả `NOT_CONFIGURED`.
7. **Phải chạy test sau khi sửa evaluator/importer/submit/shuffle logic.**
   `pytest tests/unit/evaluation`, `pytest tests/unit/importers`,
   `pytest tests/unit/services/test_study_service.py test_question_option_service.py` tối
   thiểu; ưu tiên `make check` đầy đủ.
8. **Phải thêm Alembic migration khi thay đổi model** (`Question`/`QuestionOption`/
   `QuestionDelivery`/`Attempt`/`QuestionProgress`...). Dùng `render_as_batch=True` (đã bật
   trong `alembic/env.py`) vì SQLite không hỗ trợ `ALTER TABLE` đầy đủ; đặt tên rõ ràng cho
   mọi `create_foreign_key`/`drop_constraint` trong batch mode (không truyền `None`).
9. **Câu hỏi có distractor tự sinh không được active.** Bất kỳ chỗ nào tạo option tự động
   (import, `regenerate-distractors`, `convert_free_text_questions.py`) đều phải đặt
   `needs_review=True, active=False` cho tới khi admin xác nhận qua PUT hoặc
   `/validate` trả `VALID`.
10. **SQLAlchemy model không được trả thẳng ra API** — luôn map qua Pydantic schema.
11. **Threshold/scoring weight nằm trong config** (`app/core/config.py`, đọc từ `.env`),
    gồm cả `multiple_choice_option_count`/`multiple_choice_correct_option_count`.

## Quy tắc thêm một import format mới

1. Thêm field vào `ParsedQuestion` (`app/importers/dto.py`) nếu cần (ví dụ thêm `options`/
   `correct_option_index` khi thêm định dạng MC mới).
2. Viết parser mới, implement `QuestionDocumentParser` Protocol (`can_parse` + `parse`),
   trả `ParsedImportDocument`. **Không** truy cập DB trong parser.
3. Đăng ký vào `QuestionTextParser` theo thứ tự ưu tiên `can_parse`.
4. Nếu định dạng có option rõ ràng, thêm validate số lượng/trùng lặp vào
   `ImportValidationService._validate_explicit_options` — không viết validator riêng.
5. Viết unit test trong `tests/unit/importers/`, tái dùng `QuestionImportService` hiện có.

## Quy tắc thêm evaluator mới (semantic/hybrid/LLM cho FREE_TEXT)

1. Implement `AnswerEvaluator` Protocol (`app/evaluation/base.py`).
2. Đăng ký qua `EVALUATOR_MODE` + factory ở `app/api/dependencies.py::evaluation_service`.
3. Không dùng cho MC — MC luôn dùng `MultipleChoiceGrader` (so sánh ID).
4. Vẫn phải áp dụng `ContradictionDetector` sau coverage score (không đổi hành vi FREE_TEXT).

## Quy tắc thêm question type mới

1. Thêm value vào `QuestionType` hoặc `QuestionFormat` (`app/db/models/enums.py`) + migration.
2. Nếu type cần thực thi (code/SQL), dùng abstraction (`CodeRunner`/`SqlEvaluator` Protocol).
3. Cập nhật parser nếu type mới cần nhận diện từ header đặc biệt.

## Giới hạn hiện tại (đừng ngạc nhiên khi thấy)

- Single implicit user, chưa có auth.
- Chưa chạy code/SQL người dùng nhập (chỉ lưu attempt).
- FREE_TEXT evaluator giữ nguyên nhưng không còn là luồng học mặc định; `/evaluate` và
  `POST /study-sessions/{id}/attempts` đánh dấu `deprecated=True` trong OpenAPI.
- `RuleBasedDistractorGenerator` chỉ có 2 chiến lược an toàn (hoán đổi thuật ngữ dễ nhầm +
  mượn đáp án đúng của câu khác cùng category) rồi fallback placeholder — không đảm bảo luôn
  ra 3 distractor chất lượng cao, đó là lý do bắt buộc `needs_review`.
- Chế độ thi thử (`StudyMode.EXAM`) mới có enum/DB, chưa có luồng API/UI reveal-cuối-bài
  riêng — ưu tiên hoàn thiện practice mode trước theo đúng spec.
- Review scheduler MC (`MultipleChoiceReviewScheduler`) dùng công thức/ladder đơn giản, chưa
  phải SM-2/FSRS thật.
