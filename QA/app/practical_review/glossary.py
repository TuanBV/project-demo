"""Glossary of technical jargon for the practical-review area, sourced verbatim from the
"PHỤ LỤC A — TỪ ĐIỂN THUẬT NGỮ" appendix of
scripts/data/so_tay_on_tap_sap_xep_theo_chu_de_uu_tien.docx (the same handbook the 207
questions come from). This is supplementary annotation metadata for the UI -- it is NOT part
of the DOCX question/answer/explanation content and must never be treated as such.
Self-contained: no dependency on the quiz feature or the JSON seed data.
"""

from __future__ import annotations

from dataclasses import dataclass

# (term, definition) -- verbatim from the DOCX appendix table, alphabetically ordered as in
# the source. Matching in the frontend is case-insensitive and longest-term-first, so
# multi-word terms here are safe.
_ENTRIES: list[tuple[str, str]] = [
    ("Abstraction", "Trừu tượng: che giấu chi tiết triển khai, chỉ lộ giao diện cần dùng."),
    (
        "Atomicity",
        "Tính nguyên tử: thao tác hoặc transaction hoàn tất trọn vẹn, không ở trạng thái nửa "
        "chừng.",
    ),
    ("Authentication", "Xác thực danh tính: người dùng là ai."),
    ("Authorization", "Phân quyền: người dùng được phép làm gì."),
    ("Backpressure", "Cơ chế làm chậm nguồn gửi khi phía nhận đang quá tải."),
    ("Batch", "Nhóm dữ liệu nhỏ được xử lý cùng lúc."),
    ("Broker", "Thành phần trung gian chuyển message/task từ producer tới consumer/worker."),
    ("Bucket", "Vùng trong hash table chứa các entry có vị trí hash tương ứng."),
    ("Cache aside", "Ứng dụng tự đọc cache trước, miss mới đọc DB và tự invalidate khi ghi."),
    ("CAS", "Compare-And-Set: chỉ cập nhật nếu giá trị hiện tại vẫn đúng như kỳ vọng."),
    ("Circuit breaker", "Tạm ngắt lời gọi tới dependency đang lỗi để tránh lỗi lan rộng."),
    ("Cohesion", "Mức độ các trách nhiệm trong một module liên quan chặt chẽ với nhau."),
    ("Collision", "Hai hoặc nhiều key hash vào cùng bucket."),
    ("Compile time", "Thời điểm code được biên dịch và kiểm tra trước khi chạy."),
    ("Concurrency", "Nhiều công việc tiến triển chồng lấn theo thời gian."),
    ("Consistency", "Tính nhất quán: dữ liệu tuân thủ các quy tắc đã định."),
    ("Context manager", "Cơ chế Python quản lý setup/cleanup bằng with."),
    ("Correlation ID", "ID theo dõi một request xuyên qua log và service."),
    ("Coupling", "Mức độ một module phụ thuộc vào module khác."),
    ("Cursor pagination", "Phân trang dựa trên khóa tiếp tục thay vì offset."),
    ("Deadlock", "Các thread/transaction chờ lock của nhau vô hạn."),
    ("Decorator", "Pattern bọc object để thêm hành vi mà không sửa class gốc."),
    ("Dependency Injection", "Truyền dependency từ bên ngoài vào object thay vì object tự tạo."),
    ("DTO", "Data Transfer Object: object dùng trao đổi dữ liệu qua boundary/API."),
    ("Durability", "Đã commit thì dữ liệu được giữ bền vững sau sự cố."),
    ("Dynamic dispatch", "Chọn method override theo kiểu object thực tế tại runtime."),
    ("Eager loading", "Tải quan hệ ngay cùng hoặc ngay sau entity chính."),
    ("Encapsulation", "Đóng gói: bảo vệ dữ liệu và kiểm soát truy cập trạng thái."),
    ("Event loop", "Vòng lặp điều phối coroutine/task bất đồng bộ."),
    ("Eventual consistency", "Dữ liệu có thể lệch tạm thời nhưng sẽ hội tụ về đúng."),
    ("Factory", "Pattern che giấu logic tạo object hoặc chọn implementation."),
    ("Feature flag", "Cờ cấu hình bật/tắt chức năng mà không cần deploy lại."),
    ("Flaky test", "Test lúc pass lúc fail dù code không đổi."),
    ("GC", "Garbage Collector: bộ thu gom object không còn reachable."),
    ("Generator", "Iterator lazy sinh từng giá trị bằng yield."),
    ("GIL", "Global Interpreter Lock của CPython truyền thống."),
    ("Hallucination", "AI tạo thông tin/code có vẻ hợp lý nhưng sai hoặc không tồn tại."),
    ("HMAC", "Chữ ký xác thực message bằng hash và shared secret."),
    ("Idempotency", "Gọi lặp lại cho cùng trạng thái cuối hoặc side effect không bị nhân đôi."),
    ("Identity map", "Session ORM giữ một instance object cho mỗi row identity đã load."),
    ("Immutable", "Không thay đổi trạng thái sau khi tạo."),
    ("Index", "Cấu trúc phụ giúp DB tìm/sort nhanh hơn, đổi lại tăng chi phí ghi."),
    ("Invariant", "Điều kiện luôn phải đúng của object/domain."),
    ("Isolation", "Mức độ transaction đồng thời nhìn thấy hoặc ảnh hưởng lẫn nhau."),
    ("Jitter", "Độ trễ ngẫu nhiên thêm vào retry để tránh đồng loạt."),
    ("JWT", "JSON Web Token có header, payload và signature."),
    ("Latency", "Thời gian hoàn thành một request hoặc thao tác."),
    ("Lazy loading", "Chỉ tải dữ liệu khi code thực sự truy cập."),
    ("Least privilege", "Chỉ cấp quyền tối thiểu cần thiết."),
    ("Lock contention", "Nhiều thread cạnh tranh cùng lock làm giảm throughput."),
    ("LRU", "Least Recently Used: loại phần tử ít được sử dụng gần đây nhất."),
    ("N+1 query", "Một query cha cộng N query con khi duyệt quan hệ."),
    ("Observability", "Khả năng hiểu trạng thái hệ thống qua log, metric và trace."),
    ("OOP", "Object-Oriented Programming: lập trình hướng đối tượng."),
    ("ORM", "Object-Relational Mapping: ánh xạ object với bảng database."),
    ("p95 / p99", "Phân vị latency; 95% hoặc 99% request không vượt quá giá trị này."),
    ("PECS", "Producer Extends, Consumer Super trong Java generic."),
    ("Polymorphism", "Đa hình: cùng interface/lời gọi nhưng implementation khác nhau."),
    ("Postmortem", "Tài liệu phân tích sự cố, nguyên nhân và hành động phòng ngừa."),
    ("Race condition", "Kết quả sai hoặc không ổn định do thứ tự concurrent không kiểm soát."),
    ("Rate limiting", "Giới hạn số request theo user/key/thời gian."),
    ("Regression", "Chức năng cũ bị hỏng sau thay đổi mới."),
    ("Replication lag", "Độ trễ replica áp dụng thay đổi từ primary."),
    ("Runtime", "Thời điểm chương trình đang thực thi."),
    ("Sandbox", "Môi trường cô lập giới hạn quyền và ảnh hưởng."),
    ("Serialization", "Chuyển object thành định dạng truyền/lưu như JSON hoặc binary."),
    ("Shallow copy", "Copy container nhưng vẫn dùng chung object con."),
    ("SOLID", "Năm nguyên tắc thiết kế hướng đối tượng."),
    ("Strategy", "Pattern đóng gói các thuật toán có thể thay thế."),
    ("Structured logging", "Log theo field có cấu trúc, thường ở dạng JSON."),
    ("Technical debt", "Chi phí bảo trì tương lai do giải pháp hiện tại chưa bền vững."),
    ("Terminal operation", "Operation kết thúc và kích hoạt Stream pipeline."),
    ("Thread-safe", "Hoạt động đúng khi nhiều thread truy cập đồng thời."),
    ("Throughput", "Số lượng công việc xử lý trong một đơn vị thời gian."),
    ("Trace", "Dữ liệu mô tả hành trình request qua các component."),
    ("Transaction", "Nhóm thao tác dữ liệu được xử lý như một đơn vị."),
    ("Type erasure", "Java loại bỏ phần lớn thông tin generic khi runtime."),
    ("Validation", "Kiểm tra dữ liệu thỏa schema và quy tắc nghiệp vụ."),
    ("Visibility", "Mức bảo đảm thread khác nhìn thấy giá trị cập nhật."),
    ("Volatile", "Từ khóa Java tăng visibility và ordering nhưng không bảo đảm atomicity."),
    ("Webhook", "HTTP callback được hệ thống ngoài gửi khi event xảy ra."),
    ("Window function", "SQL function tính theo nhóm/cửa sổ nhưng vẫn giữ từng dòng."),
]


@dataclass(frozen=True)
class GlossaryTerm:
    term: str
    definition: str


GLOSSARY: list[GlossaryTerm] = [GlossaryTerm(term=t, definition=d) for t, d in _ENTRIES]
