// Admin question editor: MULTIPLE_CHOICE (4 options + 1 correct) is the default format;
// FREE_TEXT keeps the legacy concept/keyword/contradiction editor for old questions.

const OPTION_COUNT = 4;

function renderOptionRows(options = []) {
    const container = document.getElementById("options-container");
    container.innerHTML = "";
    for (let i = 0; i < OPTION_COUNT; i++) {
        const opt = options[i] || {};
        const row = document.createElement("div");
        row.className = "card option-edit-row";
        row.style.background = "#fafbfc";
        row.innerHTML = `
            <div class="flex-row">
                <label style="display:flex;align-items:center;gap:6px;width:auto;">
                    <input type="radio" name="correct-option" class="c-correct" ${opt.is_correct ? "checked" : ""} style="width:auto;" />
                    Đáp án đúng
                </label>
                ${opt.auto_generated ? '<span class="badge mostly">Tự động sinh</span>' : ""}
            </div>
            <textarea class="c-option-content" rows="2" placeholder="Nội dung đáp án ${i + 1}">${escapeHtml(opt.content || "")}</textarea>
        `;
        container.appendChild(row);
    }
    if (!options.some((o) => o.is_correct) && container.firstElementChild) {
        container.firstElementChild.querySelector(".c-correct").checked = true;
    }
}

function collectOptions() {
    return Array.from(document.querySelectorAll("#options-container .option-edit-row")).map((row) => ({
        content: row.querySelector(".c-option-content").value.trim(),
        is_correct: row.querySelector(".c-correct").checked,
    }));
}

function addConceptBlock(concept = {}) {
    const container = document.getElementById("concepts-container");
    const div = document.createElement("div");
    div.className = "card concept-block";
    const keywordsStr = (concept.keywords || [])
        .map((k) => (typeof k === "string" ? k : k.keyword))
        .join(", ");
    div.innerHTML = `
        <div class="flex-row">
            <input type="text" class="c-name" placeholder="Tên concept" value="${escapeHtml(concept.name || "")}" style="flex:2;" />
            <input type="number" class="c-weight" placeholder="Trọng số" value="${concept.weight ?? 0}" style="flex:1;" />
            <label style="display:flex;align-items:center;gap:4px;width:auto;"><input type="checkbox" class="c-required" ${concept.required ? "checked" : ""} style="width:auto;" /> Bắt buộc</label>
            <button class="btn danger remove-block" type="button">Xóa</button>
        </div>
        <label>Mô tả</label>
        <input type="text" class="c-description" value="${escapeHtml(concept.description || "")}" />
        <label>Keywords (phân cách bằng dấu phẩy)</label>
        <input type="text" class="c-keywords" value="${escapeHtml(keywordsStr)}" />
    `;
    div.querySelector(".remove-block").addEventListener("click", () => div.remove());
    container.appendChild(div);
}

function addContradictionBlock(rule = {}) {
    const container = document.getElementById("contradictions-container");
    const div = document.createElement("div");
    div.className = "card contradiction-block";
    div.innerHTML = `
        <div class="flex-row">
            <input type="text" class="r-pattern" placeholder="Phát biểu sai" value="${escapeHtml(rule.pattern || "")}" style="flex:2;" />
            <input type="number" class="r-penalty" placeholder="Penalty" value="${rule.penalty ?? 20}" style="flex:1;" />
            <input type="number" class="r-max" placeholder="Điểm tối đa" value="${rule.maximum_score ?? ""}" style="flex:1;" />
            <button class="btn danger remove-block" type="button">Xóa</button>
        </div>
        <label>Mô tả</label>
        <input type="text" class="r-description" value="${escapeHtml(rule.description || "")}" />
    `;
    div.querySelector(".remove-block").addEventListener("click", () => div.remove());
    container.appendChild(div);
}

function collectConcepts() {
    return Array.from(document.querySelectorAll("#concepts-container .concept-block")).map((div) => {
        const keywords = div
            .querySelector(".c-keywords")
            .value.split(",")
            .map((s) => s.trim())
            .filter(Boolean)
            .map((k) => ({ keyword: k, match_type: "CONTAINS" }));
        return {
            name: div.querySelector(".c-name").value || "concept",
            description: div.querySelector(".c-description").value,
            weight: Number(div.querySelector(".c-weight").value) || 0,
            required: div.querySelector(".c-required").checked,
            keywords,
        };
    });
}

function collectContradictions() {
    return Array.from(document.querySelectorAll("#contradictions-container .contradiction-block"))
        .map((div) => ({
            pattern: div.querySelector(".r-pattern").value,
            description: div.querySelector(".r-description").value,
            penalty: Number(div.querySelector(".r-penalty").value) || 20,
            maximum_score: div.querySelector(".r-max").value ? Number(div.querySelector(".r-max").value) : null,
            match_type: "CONTAINS",
        }))
        .filter((r) => r.pattern);
}

function applyFormatVisibility() {
    const isMc = document.getElementById("f-format").value === "MULTIPLE_CHOICE";
    document.getElementById("mc-section").classList.toggle("hidden", !isMc);
    document.getElementById("free-text-section").classList.toggle("hidden", isMc);
    document.getElementById("free-text-test-section").classList.toggle("hidden", isMc);
}

async function loadExisting(id) {
    const q = await api.get(`/api/admin/questions/${id}`);
    document.getElementById("f-category").value = q.category_id;
    document.getElementById("f-format").value = q.question_format;
    document.getElementById("f-type").value = q.question_type;
    document.getElementById("f-language").value = q.language_scope;
    document.getElementById("f-difficulty").value = q.difficulty;
    document.getElementById("f-active").value = String(q.active);
    document.getElementById("f-content").value = q.content;
    document.getElementById("f-explanation").value = q.explanation || "";
    document.getElementById("f-answer").value = q.reference_answer || "";
    document.getElementById("f-java").value = q.java_answer || "";
    document.getElementById("f-python").value = q.python_answer || "";
    document.getElementById("f-sql").value = q.sql_answer || "";

    renderOptionRows(q.options || []);
    document.getElementById("concepts-container").innerHTML = "";
    (q.concepts || []).forEach((c) => addConceptBlock(c));
    document.getElementById("contradictions-container").innerHTML = "";
    (q.contradiction_rules || []).forEach((r) => addContradictionBlock(r));

    document.getElementById("needs-review-banner").style.display = q.needs_review ? "block" : "none";
    applyFormatVisibility();

    if (q.question_format === "FREE_TEXT") {
        document.getElementById("test-btn").disabled = false;
        document.getElementById("test-hint").textContent = "";
    }
}

function gatherPayload() {
    const format = document.getElementById("f-format").value;
    const payload = {
        category_id: Number(document.getElementById("f-category").value),
        question_format: format,
        question_type: document.getElementById("f-type").value,
        language_scope: document.getElementById("f-language").value,
        difficulty: document.getElementById("f-difficulty").value,
        active: document.getElementById("f-active").value === "true",
        needs_review: false,
        content: document.getElementById("f-content").value,
        explanation: document.getElementById("f-explanation").value || null,
    };
    if (format === "MULTIPLE_CHOICE") {
        payload.options = collectOptions();
    } else {
        payload.reference_answer = document.getElementById("f-answer").value || null;
        payload.java_answer = document.getElementById("f-java").value || null;
        payload.python_answer = document.getElementById("f-python").value || null;
        payload.sql_answer = document.getElementById("f-sql").value || null;
        payload.concepts = collectConcepts();
        payload.contradiction_rules = collectContradictions();
    }
    return payload;
}

document.getElementById("f-format").addEventListener("change", applyFormatVisibility);
document.getElementById("add-concept-btn").addEventListener("click", () => addConceptBlock());
document.getElementById("add-contradiction-btn").addEventListener("click", () => addContradictionBlock());

document.getElementById("regenerate-distractors-btn").addEventListener("click", async () => {
    const question = document.getElementById("f-content").value;
    const options = collectOptions();
    const correct = options.find((o) => o.is_correct);
    if (!question || !correct || !correct.content) {
        alert("Vui lòng nhập câu hỏi và nội dung đáp án đúng trước khi tạo đáp án sai.");
        return;
    }
    try {
        const result = await api.post("/api/admin/questions/generate-distractors", {
            question,
            correct_answer: correct.content,
            count: 3,
        });
        if (result.has_placeholder) {
            document.getElementById("options-warning").textContent =
                "Hệ thống không tạo được đủ đáp án sai chất lượng, vui lòng tự nhập.";
        } else {
            document.getElementById("options-warning").textContent = "";
        }
        const rows = Array.from(document.querySelectorAll("#options-container .option-edit-row"));
        const wrongRows = rows.filter((row) => !row.querySelector(".c-correct").checked);
        wrongRows.forEach((row, i) => {
            if (result.distractors[i] !== undefined) {
                row.querySelector(".c-option-content").value = result.distractors[i];
            }
        });
    } catch (err) {
        alert("Lỗi tạo đáp án sai: " + err.message);
    }
});

document.getElementById("suggest-btn").addEventListener("click", async () => {
    const question = document.getElementById("f-content").value;
    const referenceAnswer = document.getElementById("f-answer").value;
    if (!question || !referenceAnswer) {
        alert("Vui lòng nhập câu hỏi và đáp án tham khảo trước khi đề xuất.");
        return;
    }
    try {
        const result = await api.post("/api/admin/questions/suggest-rubric", {
            question,
            reference_answer: referenceAnswer,
            language_scope: document.getElementById("f-language").value,
        });
        if (
            document.querySelectorAll("#concepts-container .concept-block").length &&
            !confirm("Thay thế danh sách concept hiện tại bằng đề xuất?")
        ) {
            return;
        }
        document.getElementById("concepts-container").innerHTML = "";
        result.concepts.forEach((c) => addConceptBlock(c));
    } catch (err) {
        alert("Lỗi đề xuất rubric: " + err.message);
    }
});

let currentQuestionId = document.getElementById("question-id").value || null;

document.getElementById("save-btn").addEventListener("click", async () => {
    const payload = gatherPayload();
    if (payload.question_format === "MULTIPLE_CHOICE") {
        const correctCount = payload.options.filter((o) => o.is_correct).length;
        const emptyCount = payload.options.filter((o) => !o.content).length;
        if (payload.options.length !== 4 || correctCount !== 1 || emptyCount > 0) {
            alert("Cần nhập đủ 4 đáp án và chọn đúng 1 đáp án đúng.");
            return;
        }
    }
    try {
        if (currentQuestionId) {
            await api.put(`/api/admin/questions/${currentQuestionId}`, payload);
            alert("Đã cập nhật câu hỏi.");
            loadExisting(currentQuestionId);
        } else {
            const created = await api.post("/api/admin/questions", payload);
            window.location.href = `/admin/questions/${created.id}/edit`;
        }
    } catch (err) {
        alert("Lỗi lưu câu hỏi: " + err.message);
    }
});

document.getElementById("test-btn").addEventListener("click", async () => {
    if (!currentQuestionId) return;
    try {
        const result = await api.post(`/api/admin/questions/${currentQuestionId}/test-evaluation`, {
            submitted_answer: document.getElementById("test-answer").value,
        });
        document.getElementById("test-result").textContent = JSON.stringify(result, null, 2);
    } catch (err) {
        alert("Lỗi test: " + err.message);
    }
});

applyFormatVisibility();
if (!currentQuestionId) {
    renderOptionRows([]);
}
if (currentQuestionId) {
    loadExisting(currentQuestionId);
}
