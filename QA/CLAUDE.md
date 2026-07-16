# CLAUDE.md — Interview Review System

Hướng dẫn cho Claude Code (và bất kỳ ai) khi làm việc tiếp trên repository này.

Rule chi tiết theo khu vực nằm trong `.claude/rules/`; quy trình nhiều bước (thêm import
format, evaluator, question type, migration, endpoint...) nằm trong `.claude/skills/` —
xem `.claude/README.md` để biết danh sách đầy đủ. File này chỉ giữ context nền tảng.

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
- Câu hỏi MC hàng loạt (`scripts/seed_java_python_mc.py`, `scripts/seed_extended_topics.py`)
  đọc từ JSON theo category trong `scripts/data/*/`, dedup bằng `content_hash` (an toàn khi
  chạy lại) — cả hai được gọi trong `Dockerfile` CMD nên mỗi lần container khởi động đều seed
  lại (bỏ qua câu đã tồn tại). Thêm chủ đề mới → dùng skill `/add-question-topic`.

## Lệnh thường dùng

```bash
# venv + cài đặt
python -m venv .venv && source .venv/Scripts/activate   # Windows Git Bash
pip install -e ".[dev]"

# Migration & seed
alembic upgrade head
python scripts/seed.py                        # demo data: FREE_TEXT + MC hand-authored
python scripts/seed_java_python_mc.py          # 112 câu MC từ scripts/data/java_python_mc/*.json
python scripts/seed_extended_topics.py         # ~20 câu MC/chủ đề từ scripts/data/extended_topics/*.json
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

## Quy tắc repository

Danh sách đầy đủ + evidence nằm trong `.claude/rules/` (module hóa theo chủ đề, có `paths`
frontmatter): `architecture.md`, `mc-integrity.md`, `database-migrations.md`, `security.md`,
`testing-requirements.md`, `configuration.md`. Ba quy tắc quan trọng nhất, luôn áp dụng bất
kể đang sửa gì:

1. **Không đặt business logic trong route** — route chỉ parse request, gọi service, map
   sang schema.
2. **Không bao giờ tin `is_correct`/kết quả chấm từ client** — `submit_option_answer` luôn
   tự tra `correct_option_id` từ DB.
3. **Không làm lộ đáp án qua Study API** — xem `.claude/rules/mc-integrity.md`.

Quy trình thêm import format mới / evaluator mới / question type mới / API endpoint mới /
Alembic migration → dùng skill tương ứng (`/add-import-format`, `/add-evaluator`,
`/add-question-type`, `/create-api-endpoint`, `/create-database-migration`).

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
