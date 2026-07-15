#!/usr/bin/env python
"""Seed the database with demo questions across the required topics (spec section 24).

Reuses QuestionService/CategoryService directly -- no separate seeding logic. Safe to
re-run: each question's content_hash is checked first and existing rows are skipped.
"""

from __future__ import annotations

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.hashing import compute_content_hash  # noqa: E402
from app.db.models.enums import QuestionFormat  # noqa: E402
from app.db.session import SessionLocal  # noqa: E402
from app.repositories.category_repository import CategoryRepository  # noqa: E402
from app.repositories.question_repository import QuestionRepository  # noqa: E402
from app.schemas.question import (  # noqa: E402
    AdminQuestionCreate,
    AnswerConceptCreate,
    ConceptKeywordCreate,
    ContradictionRuleCreate,
)
from app.services.category_service import CategoryService  # noqa: E402
from app.services.question_service import QuestionService  # noqa: E402


def kw(
    keyword: str, match_type: str = "CONTAINS", similarity: float = 80.0
) -> ConceptKeywordCreate:
    return ConceptKeywordCreate(
        keyword=keyword, match_type=match_type, minimum_similarity=similarity
    )


def concept(
    name: str, description: str, weight: float, required: bool, keywords: list[ConceptKeywordCreate]
) -> AnswerConceptCreate:
    return AnswerConceptCreate(
        name=name, description=description, weight=weight, required=required, keywords=keywords
    )


QUESTIONS: list[dict] = [
    dict(
        category="OOP",
        content="Encapsulation (đóng gói) trong OOP là gì?",
        answer=(
            "Encapsulation là che giấu trạng thái nội bộ của object và chỉ cho phép truy cập "
            "thông qua các phương thức public như getter/setter, giúp bảo vệ dữ liệu và giảm sự "
            "phụ thuộc giữa các thành phần."
        ),
        concepts=[
            concept(
                "hide_state",
                "Che giấu trạng thái nội bộ của object",
                60,
                True,
                [
                    kw("che giấu"),
                    kw("hide"),
                    kw("trạng thái nội bộ"),
                    kw("internal state"),
                    kw("private"),
                ],
            ),
            concept(
                "access_via_methods",
                "Truy cập qua getter/setter public",
                40,
                False,
                [kw("getter"), kw("setter"), kw("public")],
            ),
        ],
    ),
    dict(
        category="OOP",
        content="Kế thừa (inheritance) và Đa hình (polymorphism) khác nhau như thế nào?",
        answer=(
            "Kế thừa cho phép một lớp con tái sử dụng thuộc tính và phương thức của lớp cha. "
            "Đa hình cho phép một phương thức có nhiều cách hiện thực khác nhau tùy theo lớp con "
            "gọi nó, thường thông qua override hoặc interface."
        ),
        concepts=[
            concept(
                "inheritance_def",
                "Kế thừa tái sử dụng thuộc tính/phương thức của lớp cha",
                50,
                True,
                [kw("kế thừa"), kw("inheritance"), kw("lớp cha"), kw("tái sử dụng")],
            ),
            concept(
                "polymorphism_def",
                "Đa hình cho phép nhiều cách hiện thực của cùng một phương thức",
                50,
                True,
                [kw("đa hình"), kw("polymorphism"), kw("override"), kw("interface")],
            ),
        ],
    ),
    dict(
        category="Java Core",
        content="JVM là gì?",
        answer=(
            "JVM (Java Virtual Machine) là máy ảo thực thi Java bytecode, giúp chương trình "
            "Java chạy độc lập với hệ điều hành."
        ),
        concepts=[
            concept(
                "jvm_def",
                "JVM thực thi bytecode, độc lập hệ điều hành",
                100,
                True,
                [
                    kw("jvm"),
                    kw("bytecode"),
                    kw("máy ảo"),
                    kw("virtual machine"),
                    kw("độc lập hệ điều hành"),
                ],
            ),
        ],
    ),
    dict(
        category="Java Core",
        content="== và equals() trong Java khác nhau thế nào?",
        answer=(
            "Với kiểu primitive, == so sánh giá trị. Với object, == so sánh reference (địa chỉ), "
            "còn equals() so sánh nội dung/logical equality nếu class override đúng."
        ),
        concepts=[
            concept(
                "reference_compare",
                "== so sánh reference của object",
                50,
                True,
                [kw("=="), kw("reference"), kw("tham chiếu"), kw("địa chỉ")],
            ),
            concept(
                "equals_compare",
                "equals() so sánh nội dung/logical equality",
                50,
                True,
                [kw("equals"), kw("logical equality"), kw("nội dung"), kw("override")],
            ),
        ],
        contradictions=[
            ContradictionRuleCreate(
                pattern="== so sánh nội dung",
                description=(
                    "== luôn so sánh nội dung object (sai với object, chỉ đúng với primitive)"
                ),
                penalty=30,
                maximum_score=50,
                match_type="CONTAINS",
            )
        ],
    ),
    dict(
        category="Java Core",
        content="volatile trong Java có đảm bảo tính atomic không?",
        answer=(
            "volatile chỉ đảm bảo visibility (thay đổi giá trị được thấy ngay bởi các thread khác) "
            "nhưng không đảm bảo atomicity cho các thao tác ghép như count++."
        ),
        concepts=[
            concept(
                "visibility",
                "volatile đảm bảo visibility",
                50,
                True,
                [kw("visibility"), kw("hiển thị")],
            ),
            concept(
                "no_atomicity",
                "volatile không đảm bảo atomicity cho count++",
                50,
                True,
                [kw("atomicity"), kw("atomic"), kw("count++")],
            ),
        ],
        contradictions=[
            ContradictionRuleCreate(
                pattern="đảm bảo atomic",
                description="volatile không đảm bảo count++ là atomic",
                penalty=30,
                maximum_score=50,
                match_type="CONTAINS",
            )
        ],
    ),
    dict(
        category="Spring",
        content="Dependency Injection trong Spring là gì?",
        answer=(
            "Dependency Injection là kỹ thuật Spring container tự động khởi tạo và truyền các "
            "dependency (bean) vào một class thay vì class tự new đối tượng, giúp giảm coupling."
        ),
        concepts=[
            concept(
                "di_def",
                "Spring container tự động inject dependency/bean",
                70,
                True,
                [kw("dependency injection"), kw("bean"), kw("container"), kw("inject")],
            ),
            concept(
                "loose_coupling",
                "Giảm sự phụ thuộc (coupling) giữa các class",
                30,
                False,
                [kw("coupling"), kw("phụ thuộc")],
            ),
        ],
    ),
    dict(
        category="Spring",
        content="@Transactional trong Spring dùng để làm gì?",
        answer=(
            "@Transactional đánh dấu một phương thức chạy trong một transaction; nếu có exception "
            "runtime xảy ra, Spring sẽ tự động rollback toàn bộ thay đổi trong transaction đó."
        ),
        concepts=[
            concept(
                "transaction_boundary",
                "@Transactional định nghĩa ranh giới transaction",
                50,
                True,
                [kw("@transactional"), kw("transaction")],
            ),
            concept(
                "rollback",
                "Tự động rollback khi có exception",
                50,
                True,
                [kw("rollback"), kw("exception")],
            ),
        ],
    ),
    dict(
        category="Python Core",
        content="Mutable và immutable trong Python là gì?",
        answer=(
            "Mutable là kiểu dữ liệu có thể thay đổi giá trị sau khi tạo, ví dụ list, dict. "
            "Immutable là kiểu không thể thay đổi sau khi tạo, ví dụ tuple, str, int."
        ),
        concepts=[
            concept(
                "mutable_def",
                "Mutable có thể thay đổi sau khi tạo (list, dict)",
                50,
                True,
                [kw("mutable"), kw("khả biến"), kw("list"), kw("dict")],
            ),
            concept(
                "immutable_def",
                "Immutable không thể thay đổi sau khi tạo (tuple, str, int)",
                50,
                True,
                [kw("immutable"), kw("bất biến"), kw("tuple"), kw("str")],
            ),
        ],
        contradictions=[
            ContradictionRuleCreate(
                pattern="list là immutable",
                description="list là mutable, không phải immutable",
                penalty=40,
                maximum_score=40,
                match_type="CONTAINS",
            )
        ],
    ),
    dict(
        category="Python Core",
        content="Generator trong Python là gì?",
        answer=(
            "Generator là một loại iterator sinh dữ liệu lazy (theo yêu cầu) bằng từ khóa "
            "yield, giúp tiết kiệm bộ nhớ khi xử lý dữ liệu lớn."
        ),
        concepts=[
            concept(
                "iterator_lazy",
                "Generator là iterator sinh dữ liệu lazy",
                60,
                True,
                [kw("iterator"), kw("lazy"), kw("generator")],
            ),
            concept("yield_keyword", "Sử dụng từ khóa yield", 40, True, [kw("yield")]),
        ],
    ),
    dict(
        category="Python Backend",
        content="WSGI là gì và vai trò của nó trong ứng dụng Python web?",
        answer=(
            "WSGI (Web Server Gateway Interface) là chuẩn giao tiếp giữa web server và ứng dụng "
            "Python, cho phép các framework như Django, Flask chạy trên nhiều server khác nhau."
        ),
        concepts=[
            concept(
                "wsgi_def",
                "WSGI là chuẩn giao tiếp giữa server và ứng dụng Python",
                70,
                True,
                [kw("wsgi"), kw("gateway interface"), kw("giao tiếp")],
            ),
            concept(
                "framework_portability",
                "Cho phép framework chạy trên nhiều server",
                30,
                False,
                [kw("framework"), kw("server")],
            ),
        ],
    ),
    dict(
        category="SQL",
        content="Primary key và Foreign key khác nhau thế nào?",
        answer=(
            "Primary key là khóa định danh duy nhất cho mỗi dòng trong một bảng. Foreign key là "
            "khóa tham chiếu đến primary key của bảng khác để thiết lập quan hệ giữa các bảng."
        ),
        concepts=[
            concept(
                "primary_key_def",
                "Primary key định danh duy nhất mỗi dòng",
                50,
                True,
                [kw("primary key"), kw("khóa chính"), kw("duy nhất")],
            ),
            concept(
                "foreign_key_def",
                "Foreign key tham chiếu đến bảng khác",
                50,
                True,
                [kw("foreign key"), kw("khóa ngoại"), kw("tham chiếu")],
            ),
        ],
    ),
    dict(
        category="REST API",
        content="REST API là gì? Nêu các phương thức HTTP thường dùng.",
        answer=(
            "REST API là kiểu kiến trúc API dựa trên HTTP, thao tác trên resource thông qua các "
            "phương thức như GET (đọc), POST (tạo mới), PUT (cập nhật toàn bộ), PATCH (cập nhật "
            "một phần), DELETE (xóa)."
        ),
        concepts=[
            concept(
                "resource_based",
                "REST thao tác trên resource qua HTTP",
                40,
                True,
                [kw("resource"), kw("http")],
            ),
            concept(
                "http_methods",
                "Các phương thức GET/POST/PUT/DELETE",
                60,
                True,
                [kw("get"), kw("post"), kw("put"), kw("delete")],
            ),
        ],
    ),
    dict(
        category="Git",
        content="git merge và git rebase khác nhau như thế nào?",
        answer=(
            "git merge tạo một commit hợp nhất giữ nguyên lịch sử của cả hai nhánh. git rebase "
            "viết lại lịch sử bằng cách di chuyển các commit của nhánh hiện tại lên đầu "
            "nhánh đích, tạo lịch sử tuyến tính hơn."
        ),
        concepts=[
            concept(
                "merge_def",
                "merge tạo commit hợp nhất, giữ lịch sử",
                50,
                True,
                [kw("merge"), kw("hợp nhất"), kw("merge commit")],
            ),
            concept(
                "rebase_def",
                "rebase viết lại lịch sử tuyến tính",
                50,
                True,
                [kw("rebase"), kw("lịch sử tuyến tính")],
            ),
        ],
    ),
    dict(
        category="Testing",
        content="Unit test và Integration test khác nhau như thế nào?",
        answer=(
            "Unit test kiểm thử một đơn vị code nhỏ (hàm/class) một cách độc lập, thường "
            "dùng mock. Integration test kiểm thử sự tương tác giữa nhiều thành phần thực "
            "tế với nhau như database, API."
        ),
        concepts=[
            concept(
                "unit_test_def",
                "Unit test kiểm thử độc lập một đơn vị code",
                50,
                True,
                [kw("unit test"), kw("độc lập"), kw("mock")],
            ),
            concept(
                "integration_test_def",
                "Integration test kiểm thử tương tác giữa nhiều thành phần",
                50,
                True,
                [kw("integration test"), kw("tương tác")],
            ),
        ],
    ),
    dict(
        category="Tình huống kỹ thuật",
        question_type="SCENARIO",
        content=(
            "Hệ thống của bạn bị chậm khi truy vấn database ở một API cụ thể. Bạn sẽ debug "
            "và xử lý như thế nào?"
        ),
        answer=(
            "Trước tiên xem execution plan/EXPLAIN của query để tìm bottleneck, kiểm tra xem có "
            "thiếu index phù hợp không, kiểm tra N+1 query, sau đó cân nhắc thêm cache hoặc tối ưu "
            "lại câu query."
        ),
        concepts=[
            concept(
                "explain_plan",
                "Xem execution plan/EXPLAIN để tìm bottleneck",
                40,
                True,
                [kw("execution plan"), kw("explain")],
            ),
            concept("index_check", "Kiểm tra thiếu index", 30, True, [kw("index")]),
            concept("n_plus_one", "Kiểm tra N+1 query", 15, False, [kw("n+1")]),
            concept(
                "cache_optimize",
                "Thêm cache hoặc tối ưu query",
                15,
                False,
                [kw("cache"), kw("tối ưu")],
            ),
        ],
    ),
    dict(
        category="Tình huống kỹ thuật",
        question_type="SCENARIO",
        content=(
            "Một API trả về lỗi 500 ngẫu nhiên trong production. Bạn sẽ xử lý sự cố này "
            "như thế nào?"
        ),
        answer=(
            "Kiểm tra log và stack trace để xác định nguyên nhân, dùng correlation/request id để "
            "trace request cụ thể, kiểm tra tài nguyên hệ thống (memory, connection pool), sau đó "
            "rollback hoặc hotfix nếu cần và bổ sung monitoring/alerting."
        ),
        concepts=[
            concept(
                "check_logs",
                "Kiểm tra log/stack trace để tìm nguyên nhân",
                40,
                True,
                [kw("log"), kw("stack trace")],
            ),
            concept(
                "correlation_id",
                "Dùng correlation/request id để trace",
                20,
                False,
                [kw("correlation"), kw("request id")],
            ),
            concept(
                "resource_check",
                "Kiểm tra tài nguyên hệ thống",
                20,
                False,
                [kw("memory"), kw("connection pool")],
            ),
            concept(
                "rollback_hotfix",
                "Rollback hoặc hotfix và bổ sung monitoring",
                20,
                False,
                [kw("rollback"), kw("monitoring")],
            ),
        ],
    ),
    dict(
        category="SQL",
        question_type="SQL",
        content=(
            "Viết câu SQL lấy danh sách nhân viên (employees) có lương (salary) lớn hơn lương "
            "trung bình của toàn bộ công ty."
        ),
        answer="Dùng subquery tính AVG(salary) rồi so sánh salary từng nhân viên với giá trị đó.",
        sql_answer=("SELECT * FROM employees\nWHERE salary > (SELECT AVG(salary) FROM employees);"),
        concepts=[
            concept(
                "subquery_avg",
                "Dùng subquery AVG(salary) để so sánh",
                100,
                True,
                [kw("avg"), kw("subquery")],
            ),
        ],
    ),
    dict(
        category="SQL",
        question_type="SQL",
        content="Viết câu SQL đếm số đơn hàng (orders) theo từng khách hàng (customer_id).",
        answer="Dùng GROUP BY customer_id kết hợp COUNT(*).",
        sql_answer=(
            "SELECT customer_id, COUNT(*) AS total_orders\nFROM orders\nGROUP BY customer_id;"
        ),
        concepts=[
            concept(
                "group_by_count",
                "Dùng GROUP BY + COUNT theo customer_id",
                100,
                True,
                [kw("group by"), kw("count")],
            ),
        ],
    ),
    dict(
        category="OOP",
        question_type="CODE",
        content=(
            "Viết hàm tìm phần tử lớn thứ hai phân biệt trong danh sách số nguyên.\n"
            "Input: [5, 1, 9, 7, 9]\nOutput: 7"
        ),
        answer=(
            "Loại bỏ trùng lặp, sắp xếp giảm dần và lấy phần tử thứ hai; hoặc duyệt một lần "
            "O(n) giữ hai biến max1/max2."
        ),
        java_answer=(
            "public int secondMax(int[] nums) {\n"
            "    int max1 = Integer.MIN_VALUE, max2 = Integer.MIN_VALUE;\n"
            "    for (int n : nums) {\n"
            "        if (n > max1) { max2 = max1; max1 = n; }\n"
            "        else if (n > max2 && n < max1) { max2 = n; }\n"
            "    }\n"
            "    return max2;\n"
            "}"
        ),
        python_answer=(
            "def second_max(nums):\n    uniq = sorted(set(nums), reverse=True)\n    return uniq[1]"
        ),
        explanation="O(n) thời gian, O(1) bộ nhớ nếu dùng cách duyệt một lần.",
        concepts=[
            concept(
                "distinct_second_max",
                "Xác định đúng phần tử lớn thứ hai phân biệt",
                100,
                True,
                [kw("second max"), kw("phân biệt")],
            ),
        ],
    ),
    dict(
        category="Python Core",
        question_type="CODE",
        content=(
            "Viết hàm kiểm tra một chuỗi có phải là palindrome hay không (bỏ qua khoảng "
            "trắng và hoa/thường)."
        ),
        answer=(
            "Chuẩn hóa chuỗi (bỏ khoảng trắng, lowercase) rồi so sánh chuỗi với chuỗi đảo "
            "ngược của nó."
        ),
        java_answer=(
            "public boolean isPalindrome(String s) {\n"
            '    String clean = s.replaceAll("\\\\s+", "").toLowerCase();\n'
            "    return clean.equals(new StringBuilder(clean).reverse().toString());\n"
            "}"
        ),
        python_answer=(
            "def is_palindrome(s):\n"
            "    clean = ''.join(s.split()).lower()\n"
            "    return clean == clean[::-1]"
        ),
        concepts=[
            concept(
                "normalize_compare_reverse",
                "Chuẩn hóa chuỗi rồi so sánh với chuỗi đảo ngược",
                100,
                True,
                [kw("palindrome"), kw("đảo ngược"), kw("reverse")],
            ),
        ],
    ),
]


def opt(content: str, is_correct: bool = False) -> dict:
    return {"content": content, "is_correct": is_correct}


# Hand-authored MULTIPLE_CHOICE questions -- the default study flow. Kept separate from
# QUESTIONS (legacy FREE_TEXT demo data, still seeded so scripts/convert_free_text_questions.py
# has real data to demonstrate on) so the app has ready-to-study MC content out of the box.
MC_QUESTIONS: list[dict] = [
    dict(
        category="Java Core",
        content="JVM là gì?",
        explanation="JVM (Java Virtual Machine) nạp và thực thi Java bytecode.",
        options=[
            opt("Máy ảo thực thi Java bytecode.", True),
            opt("Trình biên dịch source code Java thành bytecode."),
            opt("Một framework phát triển giao diện Java."),
            opt("Một hệ quản trị cơ sở dữ liệu."),
        ],
    ),
    dict(
        category="Java Core",
        content="== và equals() trong Java khác nhau thế nào?",
        explanation=(
            "Với object, == so sánh reference. equals() so sánh nội dung nếu override đúng."
        ),
        options=[
            opt(
                "== so sánh reference với object, equals() dùng để so sánh bình đẳng "
                "logic khi được override phù hợp.",
                True,
            ),
            opt("== và equals() luôn có hành vi giống nhau."),
            opt("equals() chỉ dùng cho primitive còn == chỉ dùng cho object."),
            opt("== luôn so sánh nội dung của object."),
        ],
    ),
    dict(
        category="OOP",
        content="Kế thừa (inheritance) trong OOP là gì?",
        explanation="Kế thừa cho phép lớp con tái sử dụng thuộc tính/phương thức của lớp cha.",
        options=[
            opt("Cho phép một lớp con tái sử dụng thuộc tính và phương thức của lớp cha.", True),
            opt("Cho phép một đối tượng có nhiều hình dạng khác nhau."),
            opt("Che giấu trạng thái nội bộ của đối tượng."),
            opt("Chuyển đổi kiểu dữ liệu tự động giữa các lớp."),
        ],
    ),
    dict(
        category="OOP",
        content="Encapsulation (đóng gói) trong OOP là gì?",
        explanation="Encapsulation che giấu trạng thái nội bộ, chỉ truy cập qua getter/setter.",
        options=[
            opt("Che giấu trạng thái nội bộ, chỉ cho truy cập qua các phương thức public.", True),
            opt("Cho phép ghi đè phương thức của lớp cha."),
            opt("Cho phép một lớp kế thừa từ nhiều lớp khác nhau."),
            opt("Tự động giải phóng bộ nhớ không dùng đến."),
        ],
    ),
    dict(
        category="Python Core",
        content="Mutable và immutable trong Python khác nhau thế nào?",
        explanation="Mutable (list, dict) có thể đổi giá trị; immutable (tuple, str) thì không.",
        options=[
            opt(
                "Mutable có thể thay đổi sau khi tạo (list, dict); "
                "immutable thì không (tuple, str).",
                True,
            ),
            opt("Mutable chỉ dùng cho số nguyên, immutable chỉ dùng cho chuỗi."),
            opt("Cả hai đều không thể thay đổi sau khi khởi tạo."),
            opt("Immutable có thể thay đổi nếu dùng vòng lặp for."),
        ],
    ),
    dict(
        category="Python Core",
        content="Generator trong Python là gì?",
        explanation="Generator là iterator sinh dữ liệu lazy bằng từ khóa yield.",
        options=[
            opt("Một loại iterator sinh dữ liệu lazy bằng từ khóa yield.", True),
            opt("Một hàm luôn trả về danh sách đầy đủ ngay lập tức."),
            opt("Một cấu trúc dữ liệu chỉ lưu được một phần tử."),
            opt("Một loại vòng lặp chỉ chạy được một lần duy nhất."),
        ],
    ),
    dict(
        category="Spring",
        content="Dependency Injection trong Spring là gì?",
        explanation="Spring container tự động khởi tạo và inject dependency, giảm coupling.",
        options=[
            opt("Kỹ thuật Spring container tự động khởi tạo và truyền dependency vào class.", True),
            opt("Kỹ thuật nén dữ liệu trước khi lưu vào database."),
            opt("Cách Spring quản lý phiên đăng nhập của người dùng."),
            opt("Cơ chế cache tự động cho các REST API."),
        ],
    ),
    dict(
        category="SQL",
        content="Primary key và Foreign key khác nhau thế nào?",
        explanation="Primary key định danh duy nhất; foreign key tham chiếu bảng khác.",
        options=[
            opt(
                "Primary key định danh duy nhất một dòng; foreign key tham chiếu đến bảng khác.",
                True,
            ),
            opt("Primary key và foreign key luôn là cùng một cột trong một bảng."),
            opt("Foreign key chỉ dùng để tăng tốc độ truy vấn."),
            opt("Primary key có thể trùng lặp giữa các dòng trong bảng."),
        ],
    ),
    dict(
        category="REST API",
        content="Phương thức HTTP nào thường dùng để cập nhật toàn bộ một resource?",
        explanation="PUT thường dùng để cập nhật/thay thế toàn bộ resource.",
        options=[
            opt("PUT", True),
            opt("GET"),
            opt("DELETE"),
            opt("OPTIONS"),
        ],
    ),
    dict(
        category="Git",
        content="git rebase khác git merge như thế nào?",
        explanation=(
            "rebase viết lại lịch sử tuyến tính; merge tạo một merge commit giữ nguyên lịch sử."
        ),
        options=[
            opt(
                "rebase viết lại lịch sử để tuyến tính hơn; "
                "merge tạo commit hợp nhất giữ nguyên lịch sử.",
                True,
            ),
            opt("rebase và merge luôn cho kết quả lịch sử giống hệt nhau."),
            opt("merge xóa toàn bộ lịch sử commit cũ."),
            opt("rebase chỉ dùng được trên nhánh main."),
        ],
    ),
    dict(
        category="Testing",
        content="Unit test khác Integration test ở điểm nào?",
        explanation=(
            "Unit test kiểm thử độc lập một đơn vị code; "
            "integration test kiểm thử tương tác nhiều thành phần."
        ),
        options=[
            opt(
                "Unit test kiểm thử độc lập một đơn vị code; "
                "integration test kiểm thử nhiều thành phần cùng lúc.",
                True,
            ),
            opt("Unit test luôn chậm hơn integration test."),
            opt("Integration test không cần database hay API thật."),
            opt("Unit test chỉ áp dụng được cho ngôn ngữ Python."),
        ],
    ),
    dict(
        category="Python Backend",
        content="WSGI là gì?",
        explanation="WSGI là chuẩn giao tiếp giữa web server và ứng dụng Python.",
        options=[
            opt("Chuẩn giao tiếp giữa web server và ứng dụng Python (vd Django, Flask).", True),
            opt("Một thư viện xử lý ảnh trong Python."),
            opt("Một công cụ quản lý phiên bản Python."),
            opt("Một framework testing dành riêng cho Python."),
        ],
    ),
]


def main() -> None:
    db = SessionLocal()
    try:
        category_service = CategoryService(CategoryRepository(db))
        question_service = QuestionService(QuestionRepository(db), CategoryRepository(db))
        question_repo = QuestionRepository(db)

        created = 0
        skipped = 0
        for item in QUESTIONS:
            category = category_service.get_or_create_by_name(item["category"])
            question_type = item.get("question_type", "TEXT")
            content_hash = compute_content_hash(category.name, item["content"], question_type)
            if question_repo.get_by_content_hash(content_hash) is not None:
                skipped += 1
                continue

            data = AdminQuestionCreate(
                category_id=category.id,
                question_format=QuestionFormat.FREE_TEXT,
                question_type=question_type,
                content=item["content"],
                reference_answer=item.get("answer"),
                explanation=item.get("explanation"),
                java_answer=item.get("java_answer"),
                python_answer=item.get("python_answer"),
                sql_answer=item.get("sql_answer"),
                concepts=item.get("concepts", []),
                contradiction_rules=item.get("contradictions", []),
            )
            question_service.create(data, source_type="SEED")
            created += 1

        mc_created = 0
        mc_skipped = 0
        for item in MC_QUESTIONS:
            category = category_service.get_or_create_by_name(item["category"])
            content_hash = compute_content_hash(category.name, item["content"], "TEXT")
            if question_repo.get_by_content_hash(content_hash) is not None:
                mc_skipped += 1
                continue

            data = AdminQuestionCreate(
                category_id=category.id,
                question_format=QuestionFormat.MULTIPLE_CHOICE,
                content=item["content"],
                explanation=item.get("explanation"),
                options=item["options"],
            )
            question_service.create(data, source_type="SEED")
            mc_created += 1

        print(
            f"Seed hoàn tất: {created} câu FREE_TEXT được tạo, {skipped} câu đã tồn tại; "
            f"{mc_created} câu MULTIPLE_CHOICE được tạo, {mc_skipped} câu đã tồn tại."
        )
    finally:
        db.close()


if __name__ == "__main__":
    main()
