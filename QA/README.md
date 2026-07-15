# Interview Review System

Web app để ôn tập câu hỏi phỏng vấn Junior Developer bằng hình thức **trắc nghiệm 4 đáp
án**: mỗi câu có đúng 1 đáp án đúng và 3 đáp án sai, thứ tự đáp án được xáo trộn ở backend,
hệ thống chấm đúng/sai ngay sau khi xác nhận và hiển thị giải thích. Các câu hỏi tự luận cũ
(free-text, chấm bằng keyword/fuzzy/concept matching) vẫn được giữ lại làm định dạng phụ
(`question_format=FREE_TEXT`) cho dữ liệu lịch sử.

## 1. Tính năng

- Quản lý category và câu hỏi trắc nghiệm: 4 option, đúng 1 đáp án đúng, giải thích, độ khó,
  language scope.
- Import câu hỏi qua 3 kênh: upload DOCX, dán khối text, nhập thủ công — dùng chung một
  pipeline parser (không có 2 bộ logic nhận diện câu hỏi trùng lặp).
- Preview/dry-run trước khi import thật; xử lý trùng lặp qua `content_hash` với 3 chiến lược
  SKIP/UPDATE/CREATE_COPY.
- Nguồn chỉ có câu hỏi + đáp án đúng (DOCX narrative, hoặc `CATEGORY/QUESTION/ANSWER`) tự
  động sinh 3 đáp án sai và luôn ở trạng thái **cần review** (`needs_review=True,
  active=False`) cho tới khi admin duyệt. Nguồn có sẵn đủ 4 đáp án (A/B/C/D hoặc
  OPTION×4/CORRECT_OPTION) được kích hoạt ngay nếu hợp lệ.
- Backend xáo trộn thứ tự đáp án và giữ ổn định trong cùng phiên luyện tập (không random bằng
  JavaScript).
- Chấm điểm trắc nghiệm: so khớp `selected_option_id` với `correct_option_id` lấy từ database
  — không tin dữ liệu `is_correct` gửi từ client.
- Luyện tập ngẫu nhiên / theo chủ đề / ôn câu sai (weighted review scheduler ưu tiên câu sai
  gần đây, câu quá hạn ôn tập, câu ít được luyện).
- Lịch sử luyện tập (đáp án đã chọn/đáp án đúng theo đúng thứ tự lúc làm), dashboard: tổng số
  câu đúng/sai, tỷ lệ chính xác, chuỗi đúng hiện tại/cao nhất, câu hay sai nhất, đáp án sai
  hay bị chọn nhất, tiến độ theo độ khó.
- Đề xuất concept/keyword tự động cho câu hỏi tự luận (legacy) + đề xuất/tạo lại 3 đáp án sai
  cho câu trắc nghiệm (`RuleBasedDistractorGenerator`, không cần LLM).
- Giao diện web Jinja2 + vanilla JS: radio option, phím tắt 1-4 chọn đáp án + Enter xác
  nhận/sang câu tiếp theo, responsive cơ bản (desktop & mobile).
- Giữ nguyên evaluator tự luận cũ (`KeywordAnswerEvaluator`) cho câu `FREE_TEXT`, không dùng
  trong luồng học mặc định.

## 2. Kiến trúc

```
API routes (HTTP only) -> Services (business logic) -> Repositories (SQLAlchemy)
                                                      -> Evaluation (pure) -- FREE_TEXT only
                                                      -> Importers  (pure DTO, no DB)
                                                      -> Scheduling (pure, review priority)
```

Chi tiết đầy đủ: [`docs/architecture.md`](docs/architecture.md) (kiến trúc gốc),
[`docs/implementation-plan.md`](docs/implementation-plan.md) (tiến độ MVP tự luận ban đầu),
[`docs/multiple-choice-migration-plan.md`](docs/multiple-choice-migration-plan.md) (kế hoạch
và các quyết định khi chuyển từ tự luận sang trắc nghiệm — bảng/API nào thay đổi, code cũ nào
được giữ, chiến lược migrate dữ liệu).

## 3. Cấu trúc thư mục

```
app/
  api/routes/       # FastAPI routers (HTTP only)
  core/             # config, logging, exceptions, hashing
  db/models/        # SQLAlchemy models + enums (question_option, question_delivery mới)
  schemas/          # Pydantic request/response DTOs
  repositories/     # SQLAlchemy query layer
  services/         # business logic (question_option_service, option_order_service mới)
  evaluation/        # normalizer, matcher, keyword evaluator (FREE_TEXT), mc_grader (MC)
  importers/        # extractors, parsers, validator, concept_suggester, distractor_generator
  scheduling/       # weighted_scheduler (legacy), mc_scheduler (mặc định)
  resources/        # technical_aliases.yml
  templates/, static/ # Jinja2 + vanilla JS/CSS web UI
alembic/            # migrations
docs/               # architecture.md, implementation-plan.md, multiple-choice-migration-plan.md
tests/unit/, tests/integration/
scripts/            # seed.py, import_docx.py, import_text.py, convert_free_text_questions.py
```

## 4. Yêu cầu môi trường

- Python 3.12+ (khuyến nghị dùng đúng bản trong `.venv`)
- SQLite cho local dev (mặc định) — Postgres qua biến môi trường `DATABASE_URL`
- Docker + Docker Compose (tùy chọn, cho triển khai)

## 5. Chạy bằng Docker

```bash
docker compose up --build
```

Ứng dụng chạy migration tự động khi container khởi động rồi phục vụ tại `http://localhost:8000`.
Dữ liệu SQLite được lưu ở volume `./data`. Để chuyển sang Postgres, bỏ comment service `db`
trong `docker-compose.yml` và đổi `DATABASE_URL`.

## 6. Chạy local

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
alembic upgrade head
python scripts/seed.py
uvicorn app.main:app --reload
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
alembic upgrade head
python scripts\seed.py
uvicorn app.main:app --reload
```

Mở `http://127.0.0.1:8000`.

## 7. Migrate database

```bash
alembic upgrade head                          # apply
alembic revision --autogenerate -m "message"   # tạo migration mới sau khi sửa model
```

SQLite không hỗ trợ `ALTER TABLE` đầy đủ nên `alembic/env.py` bật sẵn `render_as_batch=True`
— khi tự viết migration thêm cột/FK, luôn đặt tên rõ ràng cho constraint trong batch mode
(không truyền `None` cho `create_foreign_key`/`drop_constraint`, sẽ lỗi trên SQLite).

## 8. Seed dữ liệu mẫu

```bash
python scripts/seed.py
```

Script idempotent (dựa trên `content_hash`) — chạy lại không tạo trùng. Tạo:

- ~12 câu **trắc nghiệm** (`question_format=MULTIPLE_CHOICE`, active ngay) phủ Java Core,
  OOP, Python Core, Spring, SQL, REST API, Git, Testing, Python Backend.
- 20 câu **tự luận legacy** (`question_format=FREE_TEXT`, concept/keyword/contradiction) —
  dùng để minh họa `scripts/convert_free_text_questions.py`.

## 9. Chuyển đổi câu hỏi tự luận cũ sang trắc nghiệm

```bash
python scripts/convert_free_text_questions.py --dry-run             # chỉ xem báo cáo
python scripts/convert_free_text_questions.py                       # placeholder distractor
python scripts/convert_free_text_questions.py --generate-distractors # thử sinh distractor thật
```

Không xóa `reference_answer`/concepts/keywords — chỉ thêm 4 option + đổi
`question_format=MULTIPLE_CHOICE`, luôn đặt `needs_review=True, active=False`. Xem báo cáo
tổng số câu / chuyển đổi được / cần review / lỗi. `--dry-run` không ghi database.

## 10. Import DOCX

Qua UI: vào `/import` → tab "Upload DOCX" → chọn file → "Phân tích dữ liệu" (preview) →
"Xác nhận import". Nếu DOCX chỉ có câu hỏi + đáp án đúng, hệ thống tự sinh 3 đáp án sai và
đặt câu hỏi ở trạng thái cần review — vào `/admin/questions` để chỉnh sửa/duyệt rồi kích hoạt.

Qua CLI:

```bash
python scripts/import_docx.py path/to/questions.docx --dry-run
python scripts/import_docx.py path/to/questions.docx --duplicate-strategy update
```

## 11. Import text (dán)

Qua UI: `/import` → tab "Dán text" (xem nút "Xem định dạng mẫu" để có cả 3 định dạng bên dưới).

Qua CLI:

```bash
python scripts/import_text.py path/to/questions.txt --dry-run
cat questions.txt | python scripts/import_text.py -
```

## 12. Các định dạng text được hỗ trợ

**Định dạng 1 — tường thuật, chỉ có câu hỏi + đáp án đúng** (cần review, dùng cho DOCX lẫn
paste):

```
PHẦN I – NỀN TẢNG LẬP TRÌNH VÀ OOP

Câu 1. Compiler và interpreter khác nhau thế nào?

Trả lời: Compiler dịch toàn bộ mã nguồn...
```

**Định dạng 2 — block đơn giản, chỉ có câu hỏi + đáp án đúng** (cần review):

```
CATEGORY: Java Core
QUESTION: JVM là gì?
ANSWER: JVM là máy ảo thực thi Java bytecode.
---
```

**Định dạng 3 — đầy đủ 4 đáp án A/B/C/D** (active ngay nếu hợp lệ):

```
CATEGORY: Java Core
QUESTION: JVM là gì?
A: Một công cụ chỉ dùng để biên dịch source code Java.
B: Máy ảo thực thi Java bytecode.
C: Một thư viện giao diện người dùng của Java.
D: Một hệ quản trị cơ sở dữ liệu viết bằng Java.
CORRECT: B
EXPLANATION: JVM nạp và thực thi Java bytecode.
---
```

**Định dạng 4 — đầy đủ 4 đáp án qua field `OPTION` lặp lại** (active ngay nếu hợp lệ):

```
CATEGORY: Java Core
QUESTION: JVM là gì?
OPTION: Một công cụ chỉ dùng để biên dịch source code Java.
OPTION: Máy ảo thực thi Java bytecode.
OPTION: Một thư viện giao diện người dùng của Java.
OPTION: Một hệ quản trị cơ sở dữ liệu viết bằng Java.
CORRECT_OPTION: 2
EXPLANATION: JVM thực thi Java bytecode.
---
```

Mỗi câu cách nhau bằng dòng `---`. Field name không phân biệt hoa/thường. Cả 4 định dạng đi
qua chung một pipeline (`QuestionTextParser` → `ImportValidationService` →
`QuestionImportService`), không có logic nhận diện câu hỏi trùng lặp/tách rời cho từng định
dạng. `CATEGORY/QUESTION/ANSWER/KEYWORDS/...` (định dạng tự luận gốc) vẫn được hỗ trợ khi
import với `question_format=FREE_TEXT` (form/CLI có tham số riêng).

## 13. Cách review câu hỏi tự sinh đáp án sai (auto-generated)

1. Vào `/admin/questions`, lọc theo trạng thái — câu `needs_review=true` hiển thị badge
   "Cần review" và không xuất hiện trong `/study`.
2. Mở trang sửa (`/admin/questions/{id}/edit`), kiểm tra 4 đáp án (đáp án tự sinh có badge
   "Tự động sinh"), sửa nội dung nếu cần.
3. Có thể bấm "Tạo lại 3 đáp án sai" để sinh lại (gọi
   `POST /api/admin/questions/generate-distractors`), hoặc gõ tay trực tiếp.
4. Bấm "Lưu câu hỏi" với `active=true, needs_review=false` để kích hoạt.
5. Gọi `POST /api/admin/questions/{id}/validate` (hoặc dùng nút tương ứng trong UI nếu có)
   để xác nhận trạng thái `VALID` trước khi tin tưởng đưa vào luyện tập diện rộng.

## 14. Cách luyện tập

`/study` → chọn chủ đề/chế độ (Ngẫu nhiên, Theo chủ đề, Ôn câu sai) → chọn 1 trong 4 đáp án
(chuột hoặc phím `1`-`4`) → nút "Trả lời" (hoặc `Enter`) → xem đúng/sai + giải thích ngay →
"Câu tiếp theo" (hoặc `Enter` lần nữa). Không thể đổi đáp án sau khi đã trả lời, không thể
trả lời lại một câu đã trả lời trong cùng phiên (double-submit bị từ chối).

## 15. Cách thi thử

Enum `StudyMode.EXAM` và cột liên quan đã có sẵn trong model/API để mở rộng, nhưng luồng
API/UI "trả lời hết rồi mới chấm" **chưa được implement** trong MVP này — ưu tiên hoàn thiện
chế độ luyện tập (practice) trước theo đúng yêu cầu. Xem mục Giới hạn/Hướng mở rộng bên dưới.

## 16. Chạy test

```bash
pytest
pytest --cov=app --cov-report=term-missing   # có coverage
```

## 17. Chạy lint

```bash
ruff check .
ruff format .        # hoặc `ruff format --check .` để chỉ kiểm tra
```

## 18. Chạy mypy

```bash
mypy app
```

## 19. API documentation

Sau khi chạy server: Swagger UI tại `/docs`, ReDoc tại `/redoc`, OpenAPI JSON tại
`/openapi.json`.

Nhóm endpoint chính:
- `/api/questions*` (study, trả `StudyQuestionResponse` — không lộ đáp án đúng).
- `POST /api/study-sessions/{id}/next` — cấp câu hỏi kèm option đã xáo trộn, ổn định trong
  phiên.
- `POST /api/study-sessions/{id}/questions/{question_id}/answer` — nộp đáp án trắc nghiệm,
  trả về đúng/sai + đáp án đúng + giải thích (chỉ sau khi nộp).
- `/api/admin/questions*` — CRUD đầy đủ rubric/option,
  `POST .../suggest-rubric` (FREE_TEXT), `POST .../generate-distractors`,
  `POST .../{id}/regenerate-distractors`, `POST .../{id}/validate`,
  `POST .../{id}/duplicate`.
- `/api/admin/import/*` (DOCX/text/jobs).
- `/api/progress/*`, `/api/history*` — dashboard, lịch sử có kèm option đã chọn/đáp án đúng.
- `POST /api/study-sessions/{id}/attempts` và `POST /api/questions/{id}/evaluate` —
  **deprecated**, chỉ dùng cho câu `FREE_TEXT` (đánh dấu `deprecated=True` trong OpenAPI).

## 20. Giới hạn hiện tại

- Chưa có authentication/multi-user thật (cột `user_id` tồn tại nhưng luôn `NULL`).
- Chưa chạy/chấm code hoặc SQL người dùng nhập.
- `RuleBasedDistractorGenerator` chỉ có 2 chiến lược an toàn (hoán đổi thuật ngữ dễ nhầm +
  mượn đáp án đúng của câu khác cùng category), phần còn thiếu dùng placeholder — vì vậy
  MỌI câu tự sinh distractor đều bắt buộc `needs_review=True` cho tới khi admin duyệt.
- Chế độ thi thử (`EXAM`) mới có enum/DB, UI/API "chấm sau khi nộp hết" chưa hoàn thiện.
- Review scheduler MC dùng công thức/ladder đơn giản, chưa phải SM-2/FSRS thật.
- FREE_TEXT evaluator (giữ lại cho dữ liệu cũ) vẫn có giới hạn cũ: contradiction detection
  dựa trên phrase/fuzzy matching, không phải NLU thật.
- Rate limiting chưa bật.

## 21. Hướng mở rộng

- Hoàn thiện chế độ thi thử (EXAM): API nộp hàng loạt + chấm/hiển thị kết quả sau khi kết thúc.
- `LlmDistractorGenerator` (sinh đáp án sai bằng LLM) implement thêm cho `DistractorGenerator`
  Protocol, chọn qua `DISTRACTOR_GENERATOR_MODE`.
- Sentence embedding / LLM evaluator cho FREE_TEXT (đã có Protocol sẵn từ MVP gốc).
- Multi-user + authentication (đã chừa cột `user_id` nullable).
- Spaced repetition thật (SM-2/FSRS) thay cho `MultipleChoiceReviewScheduler` hiện tại.
- Chấm code/SQL tự động qua sandbox riêng (không chạy trong tiến trình API).
- Import thêm PDF/Excel/Markdown/JSON qua parser mới implement `QuestionDocumentParser`.

## 22. Lưu ý bảo mật khi triển khai production

- Đặt `DEBUG=false`, cấu hình `DATABASE_URL` trỏ tới Postgres có mật khẩu mạnh, không commit
  `.env` thật (chỉ commit `.env.example`).
- Giới hạn kích thước upload (`MAX_DOCX_UPLOAD_SIZE_MB`) và độ dài text import phù hợp hạ
  tầng thực tế; xem xét bật rate limiting trước khi expose public.
- `LOG_ANSWERS=false` nếu câu trả lời tự luận của người dùng có thể chứa dữ liệu nhạy cảm.
- Đặt reverse proxy (nginx/Caddy) trước Uvicorn, bật HTTPS, và cấu hình CORS phù hợp nếu
  frontend tách domain trong tương lai.
