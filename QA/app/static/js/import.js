// Import page: tab switching + preview/import for DOCX and pasted text.
document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
        document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
        document.querySelectorAll(".tab-panel").forEach((p) => p.classList.remove("active"));
        btn.classList.add("active");
        document.getElementById(`tab-${btn.dataset.tab}`).classList.add("active");
    });
});

function renderPreview(result) {
    const section = document.getElementById("preview-section");
    section.classList.remove("hidden");
    const s = result.summary;
    document.getElementById("preview-summary").textContent =
        `Category: ${s.categories_detected} | Câu hỏi: ${s.questions_detected} | Hợp lệ: ${s.valid_questions} | ` +
        `Cảnh báo: ${s.warning_count} | Lỗi: ${s.error_count}` +
        (result.dry_run
            ? ""
            : ` | Tạo mới: ${s.questions_created} | Cập nhật: ${s.questions_updated} | ` +
              `Bỏ qua: ${s.questions_skipped} | Cần review: ${s.questions_needs_review}`);

    const body = document.getElementById("preview-body");
    body.innerHTML = "";
    for (const item of result.items) {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${item.source_order}</td>
            <td>${escapeHtml(item.category)}</td>
            <td>${escapeHtml(item.question_type)}</td>
            <td>${escapeHtml(item.question)}</td>
            <td>${escapeHtml((item.answer || "").slice(0, 80))}</td>
            <td>${escapeHtml(item.status)}</td>
            <td>${escapeHtml((item.warnings || []).join("; "))}</td>
        `;
        body.appendChild(tr);
    }
}

async function runDocx(dryRun) {
    const fileInput = document.getElementById("docx-file");
    if (!fileInput.files.length) {
        alert("Vui lòng chọn file .docx");
        return;
    }
    const form = new FormData();
    form.append("file", fileInput.files[0]);
    form.append("dry_run", String(dryRun));
    form.append("duplicate_strategy", document.getElementById("docx-duplicate").value);
    form.append("generate_concepts", String(document.getElementById("docx-generate-concepts").checked));
    try {
        const result = await api.post("/api/admin/import/docx", form);
        renderPreview(result);
    } catch (err) {
        alert("Lỗi import: " + err.message);
    }
}

async function runPaste(dryRun) {
    const content = document.getElementById("paste-content").value;
    if (!content.trim()) {
        alert("Vui lòng dán nội dung câu hỏi");
        return;
    }
    try {
        const result = await api.post("/api/admin/import/text", {
            content,
            dry_run: dryRun,
            duplicate_strategy: document.getElementById("paste-duplicate").value,
            generate_concepts: document.getElementById("paste-generate-concepts").checked,
        });
        renderPreview(result);
    } catch (err) {
        alert("Lỗi import: " + err.message);
    }
}

document.getElementById("docx-preview-btn").addEventListener("click", () => runDocx(true));
document.getElementById("docx-import-btn").addEventListener("click", () => runDocx(false));
document.getElementById("paste-preview-btn").addEventListener("click", () => runPaste(true));
document.getElementById("paste-import-btn").addEventListener("click", () => runPaste(false));
document.getElementById("paste-sample-btn").addEventListener("click", () => {
    alert(
        "Định dạng 1 (câu hỏi + đáp án đúng, hệ thống tự đề xuất 3 đáp án sai, cần review):\n" +
        "CATEGORY: Java Core\nTYPE: TEXT\nQUESTION: JVM la gi?\nANSWER: JVM la may ao thuc thi bytecode.\n---\n\n" +
        "Định dạng 2 (tường thuật, cũng cần review):\n" +
        "PHAN I - JAVA CORE\n\nCau 1. JVM la gi?\n\nTra loi: JVM thuc thi Java bytecode...\n\n" +
        "Định dạng 3 (đầy đủ 4 đáp án A/B/C/D, active ngay nếu hợp lệ):\n" +
        "CATEGORY: Java Core\nQUESTION: JVM la gi?\nA: Cong cu bien dich.\nB: May ao thuc thi Java bytecode.\n" +
        "C: Thu vien giao dien.\nD: He quan tri CSDL.\nCORRECT: B\nEXPLANATION: JVM thuc thi bytecode.\n---"
    );
});

function renderManualOptions() {
    const container = document.getElementById("manual-options");
    container.innerHTML = "";
    for (let i = 0; i < 4; i++) {
        const row = document.createElement("div");
        row.className = "flex-row manual-option-row";
        row.innerHTML = `
            <label style="display:flex;align-items:center;gap:6px;width:auto;">
                <input type="radio" name="manual-correct" class="manual-correct" ${i === 0 ? "checked" : ""} style="width:auto;" /> Đúng
            </label>
            <input type="text" class="manual-option-content" placeholder="Đáp án ${i + 1}" style="flex:1;" />
        `;
        container.appendChild(row);
    }
}
renderManualOptions();

document.getElementById("manual-submit-btn").addEventListener("click", async () => {
    const rows = Array.from(document.querySelectorAll(".manual-option-row"));
    const options = rows.map((row) => ({
        content: row.querySelector(".manual-option-content").value.trim(),
        is_correct: row.querySelector(".manual-correct").checked,
    }));
    if (options.some((o) => !o.content)) {
        alert("Vui lòng nhập đủ 4 đáp án.");
        return;
    }
    const payload = {
        category_id: Number(document.getElementById("manual-category").value),
        question_format: "MULTIPLE_CHOICE",
        content: document.getElementById("manual-question").value,
        explanation: document.getElementById("manual-explanation").value || null,
        options,
    };
    try {
        await api.post("/api/admin/questions", payload);
        alert("Đã tạo câu hỏi thành công.");
        document.getElementById("manual-question").value = "";
        document.getElementById("manual-explanation").value = "";
        renderManualOptions();
    } catch (err) {
        alert("Lỗi tạo câu hỏi: " + err.message);
    }
});
