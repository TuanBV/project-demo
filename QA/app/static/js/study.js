// Multiple-choice study screen: session, radio options, submit, next, keyboard shortcuts.
let sessionId = null;
let currentQuestionId = null;
let currentOptions = [];
let selectedOptionId = null;
let questionShownAt = null;
let submitting = false;
let answered = false;
let answeredCount = 0;

const categorySelect = document.getElementById("category-select");
const modeSelect = document.getElementById("mode-select");
const questionCard = document.getElementById("question-card");
const optionsList = document.getElementById("options-list");
const submitBtn = document.getElementById("submit-btn");
const nextBtn = document.getElementById("next-btn");
const resultBanner = document.getElementById("result-banner");
const resultTitle = document.getElementById("result-title");
const resultExplanation = document.getElementById("result-explanation");
const loadingCard = document.getElementById("loading-card");
const errorCard = document.getElementById("error-card");
const errorMessage = document.getElementById("error-message");
const emptyCard = document.getElementById("empty-card");

function hideAllStatusCards() {
    resultBanner.classList.add("hidden");
    errorCard.classList.add("hidden");
    emptyCard.classList.add("hidden");
}

function applyQueryDefaults() {
    const params = new URLSearchParams(window.location.search);
    const mode = params.get("mode");
    const categoryId = params.get("category_id");
    if (mode && mode !== "EXAM") modeSelect.value = mode;
    if (categoryId) categorySelect.value = categoryId;
}

async function startSession() {
    hideAllStatusCards();
    answeredCount = 0;
    const body = {
        mode: modeSelect.value,
        category_id: categorySelect.value ? Number(categorySelect.value) : null,
    };
    const session = await api.post("/api/study-sessions", body);
    sessionId = session.id;
    await loadNextQuestion();
}

function renderOptions(options) {
    optionsList.innerHTML = "";
    optionsList.className = "option-list";
    options.forEach((option, index) => {
        const item = document.createElement("div");
        item.className = "option-item";
        item.dataset.optionId = String(option.id);
        item.setAttribute("role", "radio");
        item.setAttribute("aria-checked", "false");
        item.tabIndex = 0;
        item.innerHTML = `
            <span class="option-key">${index + 1}</span>
            <span class="option-content">${escapeHtml(option.content)}</span>
        `;
        item.addEventListener("click", () => selectOption(option.id));
        optionsList.appendChild(item);
    });
}

function selectOption(optionId) {
    if (answered) return;
    selectedOptionId = optionId;
    document.querySelectorAll(".option-item").forEach((el) => {
        const isSelected = Number(el.dataset.optionId) === optionId;
        el.classList.toggle("selected", isSelected);
        el.setAttribute("aria-checked", isSelected ? "true" : "false");
    });
    submitBtn.disabled = false;
}

async function loadNextQuestion() {
    hideAllStatusCards();
    questionCard.classList.add("hidden");
    loadingCard.classList.remove("hidden");
    nextBtn.classList.add("hidden");
    submitBtn.classList.remove("hidden");
    submitBtn.disabled = true;
    answered = false;
    selectedOptionId = null;

    try {
        const question = await api.post(`/api/study-sessions/${sessionId}/next`);
        currentQuestionId = question.id;
        currentOptions = question.options;
        questionShownAt = Date.now();
        answeredCount += 1;
        document.getElementById("q-category").textContent = question.category.name;
        document.getElementById("q-type").textContent = question.question_type;
        document.getElementById("q-difficulty").textContent = question.difficulty;
        document.getElementById("q-counter").textContent = `Câu ${answeredCount}`;
        document.getElementById("q-content").textContent = question.content;
        renderOptions(question.options);
        loadingCard.classList.add("hidden");
        questionCard.classList.remove("hidden");
    } catch (err) {
        loadingCard.classList.add("hidden");
        emptyCard.classList.remove("hidden");
    }
}

async function submitAnswer() {
    if (submitting || answered || selectedOptionId === null) return;
    submitting = true;
    submitBtn.disabled = true;
    try {
        const responseTimeSeconds = (Date.now() - questionShownAt) / 1000;
        const result = await api.post(
            `/api/study-sessions/${sessionId}/questions/${currentQuestionId}/answer`,
            { selected_option_id: selectedOptionId, response_time_seconds: responseTimeSeconds }
        );
        answered = true;
        document.querySelectorAll(".option-item").forEach((el) => {
            const optionId = Number(el.dataset.optionId);
            el.classList.add("disabled");
            if (optionId === result.correct_option_id) {
                el.classList.add("reveal-correct");
            } else if (optionId === selectedOptionId) {
                el.classList.add("reveal-incorrect");
            }
        });
        resultTitle.textContent = result.is_correct ? "✓ Chính xác" : "✗ Chưa chính xác";
        resultTitle.style.color = result.is_correct ? "var(--color-success)" : "var(--color-danger)";
        resultExplanation.textContent = result.explanation || "(không có giải thích)";
        resultBanner.classList.remove("hidden");
        submitBtn.classList.add("hidden");
        nextBtn.classList.remove("hidden");
    } catch (err) {
        errorMessage.textContent = "Lỗi khi nộp câu trả lời: " + err.message;
        errorCard.classList.remove("hidden");
        submitBtn.disabled = false;
    } finally {
        submitting = false;
    }
}

document.getElementById("restart-btn").addEventListener("click", startSession);
submitBtn.addEventListener("click", submitAnswer);
nextBtn.addEventListener("click", loadNextQuestion);

document.addEventListener("keydown", (event) => {
    if (questionCard.classList.contains("hidden")) return;
    if (["1", "2", "3", "4"].includes(event.key)) {
        const index = Number(event.key) - 1;
        if (currentOptions[index]) selectOption(currentOptions[index].id);
        return;
    }
    if (event.key === "Enter") {
        if (!answered && selectedOptionId !== null) {
            submitAnswer();
        } else if (answered && !nextBtn.classList.contains("hidden")) {
            loadNextQuestion();
        }
    }
});

applyQueryDefaults();
startSession();
