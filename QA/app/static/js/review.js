// Read-only knowledge review page: browse questions + correct answers + explanations.
// No session, no grading -- pure study-guide list backed by /api/knowledge-review.
const PAGE_SIZE = 20;
let currentPage = 1;
let currentTotal = 0;

const categorySelect = document.getElementById("review-category-select");
const listEl = document.getElementById("review-list");
const countEl = document.getElementById("review-count");
const emptyCard = document.getElementById("review-empty-card");
const paginationEl = document.getElementById("review-pagination");
const pageIndicatorEl = document.getElementById("review-page-indicator");
const prevBtn = document.getElementById("review-prev-btn");
const nextBtn = document.getElementById("review-next-btn");

function difficultyLabel(value) {
    return { EASY: "Dễ", MEDIUM: "Trung bình", HARD: "Khó" }[value] || value;
}

function renderItem(item) {
    const card = document.createElement("div");
    card.className = "card review-item";

    const optionsHtml = item.options
        ? `<ul class="review-options">${item.options
              .map((opt) => {
                  const isCorrect = opt === item.correct_answer;
                  return `<li class="${isCorrect ? "review-correct-option" : ""}">${escapeHtml(opt)}</li>`;
              })
              .join("")}</ul>`
        : "";

    card.innerHTML = `
        <div class="flex-row muted">
            <span>${escapeHtml(item.category.name)}</span> ·
            <span>${difficultyLabel(item.difficulty)}</span>
        </div>
        <h3 style="white-space:pre-wrap;">${escapeHtml(item.content)}</h3>
        <button class="btn secondary review-toggle-btn">Hiện đáp án</button>
        <div class="review-answer hidden">
            ${optionsHtml}
            <p><strong>Đáp án đúng:</strong> ${escapeHtml(item.correct_answer)}</p>
            ${item.explanation ? `<p class="muted">${escapeHtml(item.explanation)}</p>` : ""}
        </div>
    `;

    const toggleBtn = card.querySelector(".review-toggle-btn");
    const answerEl = card.querySelector(".review-answer");
    toggleBtn.addEventListener("click", () => {
        const nowHidden = answerEl.classList.toggle("hidden");
        toggleBtn.textContent = nowHidden ? "Hiện đáp án" : "Ẩn đáp án";
    });

    return card;
}

async function loadReview() {
    const categoryId = categorySelect.value;
    const params = new URLSearchParams({ page: String(currentPage), page_size: String(PAGE_SIZE) });
    if (categoryId) params.set("category_id", categoryId);

    const result = await api.get(`/api/knowledge-review?${params.toString()}`);
    currentTotal = result.total;

    listEl.innerHTML = "";
    if (result.items.length === 0) {
        emptyCard.classList.remove("hidden");
        paginationEl.classList.add("hidden");
        countEl.textContent = "";
        return;
    }
    emptyCard.classList.add("hidden");
    paginationEl.classList.remove("hidden");

    for (const item of result.items) {
        listEl.appendChild(renderItem(item));
    }

    const totalPages = Math.max(1, Math.ceil(currentTotal / PAGE_SIZE));
    countEl.textContent = `${currentTotal} câu hỏi`;
    pageIndicatorEl.textContent = `Trang ${currentPage} / ${totalPages}`;
    prevBtn.disabled = currentPage <= 1;
    nextBtn.disabled = currentPage >= totalPages;
}

categorySelect.addEventListener("change", () => {
    currentPage = 1;
    loadReview();
});
prevBtn.addEventListener("click", () => {
    if (currentPage > 1) {
        currentPage -= 1;
        loadReview();
    }
});
nextBtn.addEventListener("click", () => {
    const totalPages = Math.max(1, Math.ceil(currentTotal / PAGE_SIZE));
    if (currentPage < totalPages) {
        currentPage += 1;
        loadReview();
    }
});

loadReview();
