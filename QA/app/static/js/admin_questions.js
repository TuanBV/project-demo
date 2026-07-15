// Admin question list: search/filter/paginate/disable/delete.
let currentPage = 1;
const pageSize = 20;

async function loadQuestions() {
    const params = new URLSearchParams();
    const search = document.getElementById("search-input").value.trim();
    const categoryId = document.getElementById("filter-category").value;
    const type = document.getElementById("filter-type").value;
    const active = document.getElementById("filter-active").value;
    if (search) params.set("search", search);
    if (categoryId) params.set("category_id", categoryId);
    if (type) params.set("question_type", type);
    if (active) params.set("active", active);
    params.set("page", currentPage);
    params.set("page_size", pageSize);

    const questions = await api.get(`/api/admin/questions?${params.toString()}`);
    const body = document.getElementById("question-body");
    body.innerHTML = "";
    for (const q of questions) {
        const tr = document.createElement("tr");
        const statusLabel = q.needs_review
            ? '<span class="badge mostly">Cần review</span>'
            : q.active
              ? '<span class="badge correct">Hoạt động</span>'
              : '<span class="badge incorrect">Đã tắt</span>';
        tr.innerHTML = `
            <td>${q.id}</td>
            <td>${escapeHtml((q.content || "").slice(0, 100))}</td>
            <td>${escapeHtml(q.question_format || q.question_type)}</td>
            <td>${escapeHtml(q.difficulty)}</td>
            <td>${statusLabel}</td>
            <td>
                <a class="btn secondary" href="/admin/questions/${q.id}/edit">Sửa</a>
                <button class="btn danger" data-id="${q.id}">Xóa</button>
            </td>`;
        body.appendChild(tr);
    }
    document.querySelectorAll("button.danger").forEach((btn) => {
        btn.addEventListener("click", async () => {
            if (!confirm("Xóa câu hỏi này?")) return;
            await api.del(`/api/admin/questions/${btn.dataset.id}`);
            loadQuestions();
        });
    });
    document.getElementById("page-label").textContent = `Trang ${currentPage}`;
}

document.getElementById("filter-btn").addEventListener("click", () => { currentPage = 1; loadQuestions(); });
document.getElementById("prev-page-btn").addEventListener("click", () => {
    if (currentPage > 1) { currentPage -= 1; loadQuestions(); }
});
document.getElementById("next-page-btn").addEventListener("click", () => { currentPage += 1; loadQuestions(); });

loadQuestions();
