"""Curated glossary of technical jargon that actually appears across the 240 practical-review
questions (verified by frequency-scanning the parsed DOCX content before writing this list).
This is supplementary annotation metadata for the UI -- it is NOT part of the DOCX source
content and must never be treated as if it were a question/answer/explanation from the DOCX.
Self-contained: no dependency on the quiz feature or the JSON seed data.
"""

from __future__ import annotations

from dataclasses import dataclass

# (term, definition) -- ordered roughly by topic area for maintainability. Matching in the
# frontend is case-insensitive and longest-term-first, so multi-word terms here are safe.
_ENTRIES: list[tuple[str, str]] = [
    (
        "encapsulation",
        "Che giấu trạng thái nội bộ của đối tượng, chỉ cho truy cập qua phương thức public.",
    ),
    (
        "polymorphism",
        "Đa hình: một phương thức có nhiều cách hiện thực khác nhau tùy theo lớp con gọi nó.",
    ),
    # OOP / design
    ("inheritance", "Kế thừa: lớp con tái sử dụng thuộc tính/phương thức của lớp cha."),
    ("coupling", "Mức độ phụ thuộc lẫn nhau giữa các module/class; nên giữ thấp (low coupling)."),
    (
        "cohesion",
        "Mức độ các phần bên trong một module/class liên quan chặt chẽ với nhau; nên giữ cao (high "
        "cohesion).",
    ),
    (
        "dependency injection",
        "Kỹ thuật truyền dependency từ bên ngoài vào một class thay vì để class tự khởi tạo (new).",
    ),
    ("constructor", "Phương thức khởi tạo được gọi khi tạo một đối tượng mới."),
    ("override", "Lớp con định nghĩa lại (ghi đè) một phương thức đã có ở lớp cha."),
    ("immutable", "Bất biến: không thể thay đổi trạng thái sau khi được tạo ra."),
    ("mutable", "Khả biến: có thể thay đổi trạng thái sau khi được tạo ra."),
    (
        "interface",
        "Hợp đồng hành vi (tập phương thức) mà một class cam kết hiện thực, không chứa trạng thái.",
    ),
    (
        "abstract class",
        "Lớp trừu tượng: có thể chứa cả trạng thái/implementation dùng chung lẫn phương thức chưa "
        "hiện thực.",
    ),
    (
        "JVM",
        "Java Virtual Machine — máy ảo thực thi Java bytecode, giúp chương trình chạy độc lập hệ "
        "điều hành.",
    ),
    (
        "GC",
        "Garbage Collector — cơ chế tự động thu hồi bộ nhớ của các object không còn được tham "
        "chiếu.",
    ),
    (
        "garbage collector",
        "Cơ chế tự động thu hồi bộ nhớ của các object không còn được tham chiếu tới.",
    ),
    (
        "thread",
        "Một luồng thực thi độc lập trong cùng một process, chia sẻ bộ nhớ heap với các thread "
        "khác.",
    ),
    (
        "race condition",
        "Lỗi xảy ra khi nhiều thread truy cập/sửa cùng dữ liệu đồng thời mà không đồng bộ hóa, cho "
        "kết quả không xác định.",
    ),
    (
        "deadlock",
        "Tình trạng các thread chờ khóa (lock) của nhau theo vòng tròn khép kín, không thread nào "
        "tiến hành tiếp được.",
    ),
    (
        "synchronized",
        "Từ khóa Java tạo mutual exclusion (chỉ một thread vào khối code tại một thời điểm) và đảm "
        "bảo visibility.",
    ),
    (
        "volatile",
        "Từ khóa Java chỉ đảm bảo visibility (thay đổi được thread khác thấy ngay), không đảm bảo "
        "atomic cho thao tác ghép.",
    ),
    (
        "ConcurrentHashMap",
        "HashMap an toàn cho truy cập đồng thời từ nhiều thread, dùng CAS/khóa hạt mịn thay vì "
        "khóa toàn bộ map.",
    ),
    (
        "ExecutorService",
        "API quản lý thread pool trong Java: nhận task, phân phối cho các thread, kiểm soát vòng "
        "đời.",
    ),
    (
        "Stream API",
        "API xử lý dữ liệu dạng pipeline (filter, map, reduce...) trong Java, thường lazy cho tới "
        "terminal operation.",
    ),
    (
        "Optional",
        "Kiểu dùng để biểu diễn giá trị có thể thiếu, tránh dùng null trực tiếp và "
        "NullPointerException.",
    ),
    (
        "generic",
        "Cơ chế viết code/class hoạt động với nhiều kiểu dữ liệu mà vẫn kiểm tra kiểu tại "
        "compile-time.",
    ),
    (
        "wildcard",
        "Ký hiệu `?` trong generic Java (`? extends T`, `? super T`) biểu diễn một kiểu chưa xác "
        "định, theo quy tắc PECS.",
    ),
    (
        "JIT",
        "Just-In-Time compiler — biên dịch bytecode thành mã máy native lúc chạy để tăng tốc các "
        "đoạn code chạy nhiều lần.",
    ),
    (
        "hashCode",
        "Phương thức trả về mã băm của object, dùng để định vị bucket trong các cấu trúc dựa trên "
        "hash (HashMap, HashSet).",
    ),
    (
        "equals",
        "Phương thức so sánh hai object có bằng nhau về mặt logic hay không (khác với so sánh địa "
        "chỉ bằng ==).",
    ),
    # Java Core
    ("heap", "Vùng bộ nhớ chứa các object có vòng đời linh hoạt, được garbage collector quản lý."),
    (
        "stack",
        "Vùng bộ nhớ chứa frame của các lời gọi hàm và biến cục bộ, cấp phát/thu hồi theo LIFO.",
    ),
    # Spring
    ("bean", "Một object được Spring IoC container khởi tạo, cấu hình và quản lý vòng đời."),
    (
        "AOP",
        "Aspect-Oriented Programming — kỹ thuật tách các mối quan tâm xuyên suốt (logging, "
        "transaction...) ra khỏi logic nghiệp vụ chính.",
    ),
    (
        "proxy",
        "Object bao bọc object gốc để chèn thêm hành vi (ví dụ transaction, cache) mà không sửa "
        "code gốc — Spring AOP dùng cơ chế này.",
    ),
    (
        "Transactional",
        "Annotation Spring đánh dấu một phương thức chạy trong một transaction, tự rollback khi có "
        "lỗi runtime.",
    ),
    (
        "autoconfiguration",
        "Cơ chế Spring Boot tự tạo bean dựa trên những gì có sẵn trên classpath, giảm cấu hình thủ "
        "công.",
    ),
    (
        "bucket",
        "Một ô/nhóm chứa các entry trong cấu trúc dữ liệu dựa trên hash (ví dụ HashMap), được xác "
        "định bởi hashCode.",
    ),
    (
        "GIL",
        "Global Interpreter Lock — cơ chế của CPython chỉ cho một thread thực thi bytecode Python "
        "tại một thời điểm.",
    ),
    (
        "CPython",
        "Bản hiện thực (implementation) phổ biến nhất của Python, biên dịch source sang bytecode "
        "rồi chạy trên interpreter.",
    ),
    (
        "decorator",
        "Hàm/class bao bọc một hàm khác để thêm hành vi (logging, cache, kiểm tra quyền...) mà "
        "không sửa hàm gốc.",
    ),
    (
        "generator",
        "Hàm dùng `yield` để tạo ra một iterator sinh giá trị lazy (theo yêu cầu), tiết kiệm bộ "
        "nhớ.",
    ),
    (
        "context manager",
        "Đối tượng quản lý setup/cleanup tài nguyên qua `__enter__`/`__exit__`, dùng với câu lệnh "
        "`with`.",
    ),
    (
        "descriptor",
        "Cơ chế Python cho phép một class kiểm soát việc get/set thuộc tính của class khác (nền "
        "tảng của `property`).",
    ),
    # Python Core
    ("metaclass", '"Class của class" trong Python — kiểm soát quá trình một class được tạo ra.'),
    (
        "dataclass",
        "Decorator Python tự sinh `__init__`, `__repr__`, `__eq__`... cho một class chủ yếu chứa "
        "dữ liệu.",
    ),
    (
        "async",
        "Từ khóa khai báo một coroutine (hàm bất đồng bộ) trong Python, chạy phối hợp qua event "
        "loop.",
    ),
    (
        "await",
        "Từ khóa tạm nhường quyền điều khiển cho event loop trong khi chờ một tác vụ bất đồng bộ "
        "hoàn thành.",
    ),
    (
        "event loop",
        "Vòng lặp trung tâm điều phối các coroutine bất đồng bộ (asyncio) trên một luồng đơn.",
    ),
    ("CPU-bound", "Tác vụ bị giới hạn bởi tốc độ xử lý của CPU (tính toán nặng) thay vì chờ I/O."),
    (
        "ORM",
        "Object-Relational Mapping — thư viện ánh xạ bảng dữ liệu quan hệ thành object trong code "
        "(ví dụ SQLAlchemy, Hibernate).",
    ),
    (
        "N+1 query",
        "Vấn đề hiệu năng: 1 câu query lấy danh sách cha, cộng thêm N câu query riêng để lấy quan "
        "hệ của từng phần tử.",
    ),
    (
        "connection pool",
        "Tập hợp các kết nối database được tái sử dụng, tránh chi phí mở/đóng kết nối mới cho mỗi "
        "request.",
    ),
    (
        "cache-aside",
        "Chiến lược cache: đọc thì kiểm tra cache trước, miss mới query DB rồi ghi lại cache; ghi "
        "thì chỉ cập nhật DB.",
    ),
    (
        "session",
        "Trạng thái làm việc được duy trì giữa các request (ví dụ SQLAlchemy Session, hoặc phiên "
        "đăng nhập người dùng).",
    ),
    (
        "JWT",
        "JSON Web Token — định dạng token gồm header.payload.signature, dùng để xác thực mà không "
        "cần lưu session server-side.",
    ),
    (
        "OAuth2",
        "Chuẩn giao thức ủy quyền (authorization) phổ biến, cho phép ứng dụng truy cập tài nguyên "
        "thay mặt người dùng.",
    ),
    (
        "PKCE",
        "Proof Key for Code Exchange — cơ chế bảo vệ Authorization Code Flow của OAuth2 cho public "
        "client (SPA, mobile).",
    ),
    (
        "rate limiting",
        "Giới hạn số lượng request một client được phép gửi trong một khoảng thời gian.",
    ),
    (
        "idempotent",
        "Gọi cùng một request nhiều lần cho ra cùng trạng thái cuối như gọi một lần (ví dụ GET, "
        "PUT, DELETE).",
    ),
    (
        "WSGI",
        "Web Server Gateway Interface — chuẩn giao tiếp đồng bộ giữa web server và ứng dụng "
        "Python.",
    ),
    (
        "ASGI",
        "Asynchronous Server Gateway Interface — chuẩn giao tiếp bất đồng bộ, hỗ trợ async/await "
        "và WebSocket.",
    ),
    (
        "worker",
        "Tiến trình/luồng xử lý task (ví dụ worker của Celery, hoặc worker process của "
        "Gunicorn/Uvicorn).",
    ),
    # Backend / Python backend
    ("queue", "Hàng đợi lưu tạm các task/message chờ được xử lý."),
    (
        "broker",
        "Thành phần trung gian định tuyến/lưu tạm message giữa producer và consumer (ví dụ Redis, "
        "RabbitMQ trong Celery).",
    ),
    ("retry", "Việc tự động thử lại một thao tác thất bại, thường kèm giới hạn số lần và backoff."),
    (
        "webhook",
        "Cơ chế một hệ thống gọi ngược (HTTP callback) tới hệ thống khác khi có sự kiện xảy ra.",
    ),
    (
        "FastAPI",
        "Framework Python hiện đại để xây REST API, dựa trên Starlette (ASGI) và Pydantic.",
    ),
    (
        "Pydantic",
        "Thư viện Python validate/serialize dữ liệu dựa trên type hint, được FastAPI dùng cho "
        "request/response schema.",
    ),
    (
        "index",
        "Cấu trúc dữ liệu (thường B-tree) giúp tăng tốc tìm kiếm/join/sắp xếp, đánh đổi bằng chi "
        "phí ghi và dung lượng.",
    ),
    (
        "transaction",
        "Một nhóm thao tác được thực thi như một đơn vị: hoặc tất cả thành công (commit), hoặc "
        "không gì được áp dụng (rollback).",
    ),
    (
        "ACID",
        "Atomicity, Consistency, Isolation, Durability — bốn tính chất đảm bảo của transaction "
        "trong CSDL quan hệ.",
    ),
    (
        "isolation level",
        "Mức độ một transaction bị ảnh hưởng bởi các transaction khác chạy đồng thời (READ "
        "COMMITTED, REPEATABLE READ...).",
    ),
    # SQL / Database
    ("JOIN", "Thao tác kết hợp dữ liệu từ hai hay nhiều bảng dựa trên điều kiện liên kết."),
    (
        "composite index",
        "Chỉ mục được tạo trên nhiều cột cùng lúc; thứ tự cột ảnh hưởng tới việc truy vấn có tận "
        "dụng được index hay không.",
    ),
    (
        "covering index",
        "Chỉ mục chứa đủ mọi cột truy vấn cần, cho phép trả kết quả trực tiếp từ index mà không "
        "cần đọc bảng gốc.",
    ),
    (
        "CTE",
        "Common Table Expression (`WITH ... AS`) — kết quả truy vấn tạm đặt tên, dùng trong phạm "
        "vi một câu lệnh SQL.",
    ),
    (
        "replication",
        "Cơ chế sao chép dữ liệu từ một database (master/primary) sang một hoặc nhiều bản sao "
        "(replica).",
    ),
    (
        "normalization",
        "Quá trình tổ chức schema để giảm dữ liệu trùng lặp, tuân theo các dạng chuẩn (1NF, 2NF, "
        "3NF...).",
    ),
    # REST API
    ("endpoint", "Một địa chỉ URL cụ thể mà client có thể gọi tới để tương tác với API."),
    ("payload", "Phần nội dung dữ liệu chính của một request/response (thường là JSON body)."),
    (
        "status code",
        "Mã số HTTP cho biết kết quả xử lý request (200 OK, 404 Not Found, 500 Internal Server "
        "Error...).",
    ),
    ("pagination", "Kỹ thuật chia một danh sách kết quả lớn thành nhiều trang nhỏ để trả về dần."),
    (
        "HATEOAS",
        "Hypermedia as the Engine of Application State — nhúng link điều hướng ngay trong response "
        "API.",
    ),
    (
        "versioning",
        "Chiến lược quản lý các phiên bản khác nhau của một API theo thời gian (qua URL, "
        "header...).",
    ),
    (
        "CORS",
        "Cross-Origin Resource Sharing — cơ chế trình duyệt kiểm soát việc một trang web gọi API ở "
        "domain khác.",
    ),
    # Git
    ("commit", "Một snapshot các thay đổi được lưu vào lịch sử của repository."),
    ("merge", "Gộp lịch sử của hai nhánh lại với nhau, thường tạo thêm một merge commit."),
    (
        "rebase",
        "Viết lại lịch sử bằng cách di chuyển các commit lên trên một base mới, tạo lịch sử tuyến "
        "tính hơn.",
    ),
    ("branch", "Một nhánh phát triển độc lập trong lịch sử Git."),
    (
        "stash",
        "Tạm cất các thay đổi chưa commit sang một chỗ khác để quay lại làm việc khác, có thể lấy "
        "lại sau.",
    ),
    (
        "cherry-pick",
        "Áp dụng một commit cụ thể từ nhánh này sang nhánh khác mà không cần merge toàn bộ nhánh "
        "nguồn.",
    ),
    ("bisect", "Công cụ Git tìm commit gây lỗi bằng cách tìm kiếm nhị phân trên lịch sử commit."),
    (
        "reflog",
        "Nhật ký nội bộ ghi lại mọi lần di chuyển của HEAD/nhánh, dùng để khôi phục commit tưởng "
        "đã mất.",
    ),
    ("HEAD", "Con trỏ chỉ tới commit/nhánh hiện tại đang được checkout trong working directory."),
    (
        "hook",
        "Script Git tự động chạy khi có một sự kiện nhất định xảy ra (ví dụ pre-commit, pre-push).",
    ),
    (
        "mock",
        "Đối tượng giả lập dùng để kiểm tra một tương tác (lời gọi, tham số) thực sự xảy ra như kỳ "
        "vọng.",
    ),
    (
        "stub",
        "Đối tượng giả lập chỉ trả về giá trị đã định trước, không quan tâm cách nó được gọi.",
    ),
    (
        "unit test",
        "Bài test kiểm tra một đơn vị code nhỏ (hàm/class) một cách độc lập, thường cô lập "
        "dependency.",
    ),
    (
        "integration test",
        "Bài test kiểm tra sự tương tác thực tế giữa nhiều thành phần (DB, API, service khác).",
    ),
    (
        "coverage",
        "Chỉ số đo tỷ lệ code được thực thi khi chạy test (line coverage, branch coverage...).",
    ),
    (
        "flaky test",
        "Bài test cho kết quả không nhất quán giữa các lần chạy dù code không đổi, thường do "
        "race condition/shared state.",
    ),
    (
        "TDD",
        "Test-Driven Development — quy trình viết test thất bại trước, viết code tối thiểu để "
        "pass, rồi refactor.",
    ),
    (
        "fixture",
        "Dữ liệu/trạng thái được chuẩn bị sẵn (setup) để dùng chung cho nhiều test case, ví dụ "
        "pytest fixture.",
    ),
    # Testing
    # Vibe coding / AI
    ("prompt", "Nội dung mô tả yêu cầu được gửi cho một mô hình AI để nó sinh ra phản hồi/code."),
    (
        "hallucination",
        "Hiện tượng AI sinh ra thông tin/API nghe có vẻ hợp lý nhưng thực chất không tồn tại hoặc "
        "sai.",
    ),
    (
        "prompt injection",
        "Kiểu tấn công chèn chỉ dẫn độc hại vào nội dung mà AI đọc được, khiến AI thực hiện hành "
        "động ngoài ý muốn.",
    ),
    (
        "agent",
        "Công cụ AI có khả năng tự đọc file, chạy lệnh và thực hiện nhiều bước để hoàn thành một "
        "tác vụ.",
    ),
    (
        "context window",
        'Giới hạn lượng văn bản (token) mà một mô hình AI có thể "nhìn thấy" cùng lúc trong một '
        "lượt xử lý.",
    ),
    (
        "LLM",
        "Large Language Model — mô hình ngôn ngữ lớn (như GPT, Claude) được huấn luyện để hiểu và "
        "sinh văn bản/code.",
    ),
]


@dataclass(frozen=True)
class GlossaryTerm:
    term: str
    definition: str


GLOSSARY: list[GlossaryTerm] = [GlossaryTerm(term=t, definition=d) for t, d in _ENTRIES]
