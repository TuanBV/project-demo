// Practical Review ("Ôn lý thuyết thực chiến") frontend. Entirely separate from study.js --
// never calls /api/questions, /api/study-sessions, or any multiple-choice endpoint. Progress
// is stored client-side only, under the "practicalReview.*" localStorage namespace. Relies
// on the shared, generic api.js helpers (api.get, escapeHtml) already loaded by base.html.
(function () {
    "use strict";

    const API_BASE = "/api/practical-review";

    // ---------------------------------------------------------------------
    // ProgressStore -- localStorage-backed, versioned, never stores question content.
    // ---------------------------------------------------------------------
    const ProgressStore = (function () {
        const STORAGE_KEY = "practicalReview.progress.v1";
        const LAST_TOPIC_KEY = "practicalReview.lastTopic.v1";
        const SCHEMA_VERSION = 1;
        const VALID_STATUSES = ["unseen", "learning", "review", "mastered"];

        function _emptyState() {
            return { version: SCHEMA_VERSION, items: {} };
        }

        function _read() {
            let raw;
            try {
                raw = localStorage.getItem(STORAGE_KEY);
            } catch (err) {
                return _emptyState();
            }
            if (!raw) return _emptyState();
            try {
                const parsed = JSON.parse(raw);
                if (
                    !parsed ||
                    typeof parsed !== "object" ||
                    parsed.version !== SCHEMA_VERSION ||
                    typeof parsed.items !== "object" ||
                    parsed.items === null
                ) {
                    return _emptyState();
                }
                return parsed;
            } catch (err) {
                return _emptyState();
            }
        }

        function _write(data) {
            try {
                localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
            } catch (err) {
                // localStorage full/unavailable (e.g. private browsing) -- fail silently,
                // progress just won't persist across reloads.
            }
        }

        function _defaultEntry(questionNumber) {
            return {
                question_number: questionNumber,
                status: "unseen",
                view_count: 0,
                last_viewed_at: null,
            };
        }

        function getEntry(questionNumber) {
            const data = _read();
            const entry = data.items[String(questionNumber)];
            return entry ? { ...entry } : _defaultEntry(questionNumber);
        }

        function getStatus(questionNumber) {
            return getEntry(questionNumber).status;
        }

        function recordView(questionNumber) {
            const data = _read();
            const key = String(questionNumber);
            const entry = data.items[key] || _defaultEntry(questionNumber);
            entry.view_count += 1;
            entry.last_viewed_at = new Date().toISOString();
            if (entry.status === "unseen") entry.status = "learning";
            data.items[key] = entry;
            _write(data);
            return entry;
        }

        function setStatus(questionNumber, status) {
            if (!VALID_STATUSES.includes(status)) return getEntry(questionNumber);
            const data = _read();
            const key = String(questionNumber);
            const entry = data.items[key] || _defaultEntry(questionNumber);
            entry.status = status;
            entry.last_viewed_at = new Date().toISOString();
            data.items[key] = entry;
            _write(data);
            return entry;
        }

        function getStatsFor(questionNumbers) {
            const stats = { unseen: 0, learning: 0, review: 0, mastered: 0, total: questionNumbers.length };
            for (const num of questionNumbers) {
                const status = getStatus(num);
                stats[status] = (stats[status] || 0) + 1;
            }
            return stats;
        }

        function reset() {
            try {
                localStorage.removeItem(STORAGE_KEY);
            } catch (err) {
                /* ignore */
            }
        }

        function getLastTopicSlug() {
            try {
                return localStorage.getItem(LAST_TOPIC_KEY);
            } catch (err) {
                return null;
            }
        }

        function setLastTopicSlug(slug) {
            try {
                localStorage.setItem(LAST_TOPIC_KEY, slug);
            } catch (err) {
                /* ignore */
            }
        }

        return {
            getEntry,
            getStatus,
            recordView,
            setStatus,
            getStatsFor,
            reset,
            getLastTopicSlug,
            setLastTopicSlug,
            STORAGE_KEY,
        };
    })();

    // ---------------------------------------------------------------------
    // Shared status-label helpers
    // ---------------------------------------------------------------------
    const STATUS_LABELS = {
        unseen: "Chưa học",
        learning: "Đang học",
        review: "Cần xem lại",
        mastered: "Đã nắm",
    };

    function statusBadgeHtml(status) {
        const label = STATUS_LABELS[status] || status;
        return `<span class="pr-badge pr-badge-${status}">${escapeHtml(label)}</span>`;
    }

    function escapeRegExp(value) {
        return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    }

    // ---------------------------------------------------------------------
    // TopicFilter -- pure filtering helper shared by the topic question list page.
    // ---------------------------------------------------------------------
    const TopicFilter = {
        apply(questionsWithStatus, filterKey) {
            if (filterKey === "all") return questionsWithStatus;
            return questionsWithStatus.filter((item) => item.status === filterKey);
        },
    };

    // ---------------------------------------------------------------------
    // Search -- text normalization + safe highlight (always escapes before inserting HTML).
    // ---------------------------------------------------------------------
    const Search = (function () {
        function stripDiacritics(value) {
            return value
                .normalize("NFD")
                .replace(/[̀-ͯ]/g, "") // combining diacritical marks (U+0300-U+036F)
                .replace(/đ/g, "d")
                .replace(/Đ/g, "D");
        }

        function normalize(value) {
            return stripDiacritics(value || "").toLowerCase();
        }

        function matches(haystackParts, query) {
            const normalizedQuery = normalize(query).trim();
            if (!normalizedQuery) return false;
            const haystack = normalize(haystackParts.join(" "));
            return haystack.includes(normalizedQuery);
        }

        function highlight(text, query) {
            const escapedText = escapeHtml(text);
            const trimmedQuery = (query || "").trim();
            if (!trimmedQuery) return escapedText;
            const escapedQuery = escapeRegExp(escapeHtml(trimmedQuery));
            if (!escapedQuery) return escapedText;
            try {
                const pattern = new RegExp(escapedQuery, "gi");
                return escapedText.replace(pattern, (m) => `<mark class="pr-highlight">${m}</mark>`);
            } catch (err) {
                return escapedText;
            }
        }

        function debounce(fn, delay) {
            let timer = null;
            return function (...args) {
                clearTimeout(timer);
                timer = setTimeout(() => fn.apply(null, args), delay);
            };
        }

        return { normalize, matches, highlight, debounce };
    })();

    // ---------------------------------------------------------------------
    // Glossary -- surfaces recognized technical jargon as an always-visible list beneath a
    // question, instead of a hover tooltip (tooltips don't work well on touch/smartphone).
    // Supplementary UI metadata only (see app/practical_review/glossary.py); never treated
    // as DOCX content. Fetched once and cached for the lifetime of the page.
    // ---------------------------------------------------------------------
    const Glossary = (function () {
        let terms = [];
        let pattern = null;
        let loadPromise = null;

        function fetchTerms() {
            if (!loadPromise) {
                loadPromise = api
                    .get(`${API_BASE}/glossary`)
                    .then((data) => {
                        terms = Array.isArray(data) ? data : [];
                        if (terms.length) {
                            const sorted = [...terms].sort((a, b) => b.term.length - a.term.length);
                            const alternation = sorted.map((t) => escapeRegExp(t.term)).join("|");
                            pattern = new RegExp(`\\b(${alternation})\\b`, "gi");
                        }
                    })
                    .catch(() => {
                        terms = [];
                        pattern = null;
                    });
            }
            return loadPromise;
        }

        function definitionFor(matchedText) {
            const found = terms.find((t) => t.term.toLowerCase() === matchedText.toLowerCase());
            return found ? found.definition : "";
        }

        // Scans RAW (unescaped) text for recognized jargon and returns the distinct terms
        // found, each with its definition, in first-seen order.
        function findIn(...rawTexts) {
            if (!pattern) return [];
            const seen = new Set();
            const found = [];
            const re = new RegExp(pattern.source, pattern.flags);
            for (const text of rawTexts) {
                if (!text) continue;
                re.lastIndex = 0;
                let m;
                while ((m = re.exec(text)) !== null) {
                    const key = m[1].toLowerCase();
                    if (seen.has(key)) continue;
                    const definition = definitionFor(m[1]);
                    if (!definition) continue;
                    seen.add(key);
                    found.push({ term: m[1], definition });
                }
            }
            return found;
        }

        // Renders an always-visible "Thuật ngữ" box listing every jargon term recognized in
        // the given raw texts, or "" when none are found.
        function renderBox(...rawTexts) {
            const found = findIn(...rawTexts);
            if (!found.length) return "";
            const items = found
                .map(
                    (t) =>
                        `<li><span class="pr-term-name">${escapeHtml(t.term)}</span>: ` +
                        `<span class="pr-term-def">${escapeHtml(t.definition)}</span></li>`,
                )
                .join("");
            return `
                <div class="pr-terms-box">
                    <span class="pr-qa-label">Thuật ngữ</span>
                    <ul class="pr-terms-list">${items}</ul>
                </div>
            `;
        }

        return { fetchTerms, renderBox };
    })();

    // ---------------------------------------------------------------------
    // Page: overview
    // ---------------------------------------------------------------------
    function renderOverviewStats(cards, overviewCache) {
        let totalSeen = 0;
        let totalMastered = 0;
        let totalReview = 0;
        let bestReviewSlug = null;

        for (const card of cards) {
            const slug = card.dataset.topicSlug;
            const count = parseInt(card.dataset.questionCount, 10) || 0;
            const learnedEl = card.querySelector('[data-role="learned-count"]');
            const fillEl = card.querySelector('[data-role="progress-fill"]');
            const cached = overviewCache[slug];
            if (!cached) continue;
            learnedEl.textContent = String(cached.learned);
            fillEl.style.width = `${count ? (cached.learned / count) * 100 : 0}%`;
            totalSeen += cached.learned;
            totalMastered += cached.mastered;
            totalReview += cached.review;
            if (cached.review > 0 && bestReviewSlug === null) bestReviewSlug = slug;
        }

        document.getElementById("pr-stat-seen").textContent = String(totalSeen);
        document.getElementById("pr-stat-mastered").textContent = String(totalMastered);
        document.getElementById("pr-stat-review").textContent = String(totalReview);
        return { bestReviewSlug };
    }

    function bindOverviewEvents(cards, getBestReviewSlug) {
        const continueBtn = document.getElementById("pr-continue-btn");
        continueBtn.addEventListener("click", () => {
            const lastSlug = ProgressStore.getLastTopicSlug();
            const targetSlug =
                lastSlug && cards.some((c) => c.dataset.topicSlug === lastSlug)
                    ? lastSlug
                    : cards.length
                        ? cards[0].dataset.topicSlug
                        : null;
            if (targetSlug) window.location.href = `/practical-review/topics/${targetSlug}/study`;
        });

        const reviewBtn = document.getElementById("pr-review-btn");
        reviewBtn.addEventListener("click", () => {
            const bestReviewSlug = getBestReviewSlug();
            if (bestReviewSlug) {
                window.location.href = `/practical-review/topics/${bestReviewSlug}/study?order=review`;
            }
        });

        const searchInput = document.getElementById("pr-overview-search-input");
        searchInput.addEventListener("keydown", (event) => {
            if (event.key === "Enter" && searchInput.value.trim()) {
                window.location.href = `/practical-review/search?q=${encodeURIComponent(searchInput.value.trim())}`;
            }
        });
    }

    async function initOverviewPage() {
        const cards = Array.from(document.querySelectorAll(".pr-topic-card"));
        const overviewCache = {};
        let bestReviewSlug = null;

        bindOverviewEvents(cards, () => bestReviewSlug);

        const reviewBtn = document.getElementById("pr-review-btn");
        reviewBtn.disabled = true;
        reviewBtn.title = "Chưa có câu nào cần xem lại";

        // One request per topic to compute real per-question progress -- the server has no
        // notion of per-user progress, so this is the simplest way to get accurate totals.
        await Promise.all(
            cards.map(async (card) => {
                const slug = card.dataset.topicSlug;
                try {
                    const detail = await api.get(`${API_BASE}/topics/${slug}`);
                    let learned = 0;
                    let mastered = 0;
                    let review = 0;
                    for (const question of detail.questions) {
                        const status = ProgressStore.getStatus(question.number);
                        if (status !== "unseen") learned += 1;
                        if (status === "mastered") mastered += 1;
                        if (status === "review") review += 1;
                    }
                    overviewCache[slug] = { learned, mastered, review };
                } catch (err) {
                    overviewCache[slug] = { learned: 0, mastered: 0, review: 0 };
                }
            })
        );

        const result = renderOverviewStats(cards, overviewCache);
        bestReviewSlug = result.bestReviewSlug;
        if (bestReviewSlug) {
            reviewBtn.disabled = false;
            reviewBtn.title = "";
        }
    }

    // ---------------------------------------------------------------------
    // Page: topic question list (accordion)
    // ---------------------------------------------------------------------
    async function initTopicPage() {
        const root = document.querySelector('.pr-app[data-pr-page="topic"]');
        const slug = root.dataset.topicSlug;
        const listEl = document.getElementById("pr-qa-list");
        const emptyEl = document.getElementById("pr-topic-empty-state");
        const searchInput = document.getElementById("pr-topic-search-input");
        const filterBtns = Array.from(document.querySelectorAll(".pr-filter-btn"));

        let questions = [];
        try {
            const [detail] = await Promise.all([
                api.get(`${API_BASE}/topics/${slug}`),
                Glossary.fetchTerms(),
            ]);
            questions = detail.questions;
        } catch (err) {
            listEl.innerHTML = `<p class="muted">Không tải được câu hỏi: ${escapeHtml(err.message)}</p>`;
            return;
        }

        let activeFilter = "all";
        let searchQuery = "";

        function computeAndRenderProgress() {
            const numbers = questions.map((q) => q.number);
            const stats = ProgressStore.getStatsFor(numbers);
            const learned = stats.learning + stats.review + stats.mastered;
            document.getElementById("pr-topic-progress-text").textContent = `${learned} đã học`;
            document.getElementById("pr-topic-progress-fill").style.width =
                `${questions.length ? (learned / questions.length) * 100 : 0}%`;
        }

        function render() {
            let withStatus = questions.map((q) => ({ ...q, status: ProgressStore.getStatus(q.number) }));
            withStatus = TopicFilter.apply(withStatus, activeFilter);
            if (searchQuery.trim()) {
                withStatus = withStatus.filter((q) =>
                    Search.matches([q.question, q.answer, q.explanation], searchQuery)
                );
            }

            listEl.innerHTML = "";
            emptyEl.classList.toggle("hidden", withStatus.length > 0);

            for (const question of withStatus) {
                listEl.appendChild(renderAccordionItem(question, searchQuery));
            }
            computeAndRenderProgress();
        }

        function renderAccordionItem(question, query) {
            const item = document.createElement("div");
            item.className = "pr-qa-item";
            item.dataset.questionNumber = String(question.number);
            item.dataset.open = "false";
            const bodyId = `pr-qa-body-${question.number}`;

            const header = document.createElement("button");
            header.type = "button";
            header.className = "pr-qa-item-header";
            header.setAttribute("aria-expanded", "false");
            header.setAttribute("aria-controls", bodyId);
            header.innerHTML = `
                <span class="pr-qa-number">Câu ${question.number}</span>
                <span class="pr-qa-question-text">${Search.highlight(question.question, query)}</span>
                ${statusBadgeHtml(question.status)}
                <span class="pr-qa-chevron" aria-hidden="true">&rsaquo;</span>
            `;

            const body = document.createElement("div");
            body.className = "pr-qa-item-body";
            body.id = bodyId;
            body.innerHTML = `
                <div class="pr-qa-answer-block">
                    <span class="pr-qa-label">Đáp án</span>
                    <p>${Search.highlight(question.answer, query)}</p>
                </div>
                <div class="pr-qa-explanation-block">
                    <span class="pr-qa-label">Giải thích</span>
                    <p>${Search.highlight(question.explanation, query)}</p>
                </div>
                ${Glossary.renderBox(question.question, question.answer, question.explanation)}
                <div class="pr-status-actions">
                    <button class="pr-btn pr-btn-outline pr-rate-btn pr-rate-mastered" data-rate="mastered" type="button">Đã nắm</button>
                    <button class="pr-btn pr-btn-outline pr-rate-btn pr-rate-review" data-rate="review" type="button">Cần xem lại</button>
                    <button class="pr-btn pr-btn-outline pr-rate-btn pr-rate-unseen" data-rate="unseen" type="button">Chưa học</button>
                </div>
            `;

            header.addEventListener("click", () => {
                const isOpen = item.dataset.open === "true";
                item.dataset.open = isOpen ? "false" : "true";
                header.setAttribute("aria-expanded", isOpen ? "false" : "true");
                if (!isOpen) {
                    ProgressStore.recordView(question.number);
                    const badge = header.querySelector(".pr-badge");
                    badge.outerHTML = statusBadgeHtml(ProgressStore.getStatus(question.number));
                }
            });

            for (const btn of body.querySelectorAll(".pr-rate-btn")) {
                btn.addEventListener("click", () => {
                    ProgressStore.setStatus(question.number, btn.dataset.rate);
                    const badge = header.querySelector(".pr-badge");
                    badge.outerHTML = statusBadgeHtml(ProgressStore.getStatus(question.number));
                    computeAndRenderProgress();
                });
            }

            item.appendChild(header);
            item.appendChild(body);
            return item;
        }

        for (const btn of filterBtns) {
            btn.addEventListener("click", () => {
                for (const other of filterBtns) other.setAttribute("aria-pressed", "false");
                btn.setAttribute("aria-pressed", "true");
                activeFilter = btn.dataset.filter;
                render();
            });
        }

        searchInput.addEventListener(
            "input",
            Search.debounce(() => {
                searchQuery = searchInput.value;
                render();
            }, 200)
        );

        ProgressStore.setLastTopicSlug(slug);
        render();
    }

    // ---------------------------------------------------------------------
    // FlashcardController -- study page (one question at a time).
    // ---------------------------------------------------------------------
    const FlashcardController = (function () {
        let questions = [];
        let order = [];
        let position = 0;

        function shuffle(array) {
            const copy = array.slice();
            for (let i = copy.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [copy[i], copy[j]] = [copy[j], copy[i]];
            }
            return copy;
        }

        function buildOrder(mode) {
            const indices = questions.map((_, i) => i);
            if (mode === "random") return shuffle(indices);
            if (mode === "review") {
                return indices.filter((i) => ProgressStore.getStatus(questions[i].number) === "review");
            }
            return indices;
        }

        function firstUnmasteredPosition() {
            for (let i = 0; i < order.length; i++) {
                if (ProgressStore.getStatus(questions[order[i]].number) !== "mastered") return i;
            }
            return 0;
        }

        // Answer/explanation are shown immediately alongside the question (no separate
        // reveal step), so a view is recorded as soon as a card becomes current.
        function _recordViewForCurrent() {
            const question = current();
            if (question) ProgressStore.recordView(question.number);
        }

        function init(loadedQuestions, mode, startAt) {
            questions = loadedQuestions;
            order = buildOrder(mode);
            if (typeof startAt === "number") {
                position = Math.min(Math.max(startAt, 0), Math.max(order.length - 1, 0));
            } else {
                position = firstUnmasteredPosition();
            }
            _recordViewForCurrent();
        }

        function isEmpty() {
            return order.length === 0;
        }

        function current() {
            if (isEmpty()) return null;
            return questions[order[position]];
        }

        function rate(status) {
            const question = current();
            if (!question) return;
            ProgressStore.setStatus(question.number, status);
        }

        function next() {
            if (isEmpty()) return;
            position = Math.min(position + 1, order.length - 1);
            _recordViewForCurrent();
        }

        function prev() {
            if (isEmpty()) return;
            position = Math.max(position - 1, 0);
            _recordViewForCurrent();
        }

        function progress() {
            return { position, total: order.length };
        }

        return { init, isEmpty, current, rate, next, prev, progress };
    })();

    // ---------------------------------------------------------------------
    // KeyboardController -- study page shortcuts only; scoped, removed if page unmounts.
    // ---------------------------------------------------------------------
    const KeyboardController = {
        bind(handlers) {
            function onKeydown(event) {
                if (event.target && ["INPUT", "SELECT", "TEXTAREA"].includes(event.target.tagName)) {
                    return;
                }
                switch (event.key) {
                    case " ":
                    case "Enter":
                        event.preventDefault();
                        handlers.onReveal();
                        break;
                    case "1":
                        handlers.onRate("learning");
                        break;
                    case "2":
                        handlers.onRate("review");
                        break;
                    case "3":
                        handlers.onRate("mastered");
                        break;
                    case "ArrowLeft":
                        handlers.onPrev();
                        break;
                    case "ArrowRight":
                        handlers.onNext();
                        break;
                    default:
                        break;
                }
            }
            document.addEventListener("keydown", onKeydown);
            return () => document.removeEventListener("keydown", onKeydown);
        },
    };

    // ---------------------------------------------------------------------
    // Page: study (flashcard)
    // ---------------------------------------------------------------------
    async function initStudyPage() {
        const root = document.querySelector('.pr-app[data-pr-page="study"]');
        const slug = root.dataset.topicSlug;
        const params = new URLSearchParams(window.location.search);
        const orderSelect = document.getElementById("pr-order-mode");
        const questionEl = document.getElementById("pr-flashcard-question");
        const answerEl = document.getElementById("pr-flashcard-answer");
        const explanationEl = document.getElementById("pr-flashcard-explanation");
        const termsEl = document.getElementById("pr-flashcard-terms");
        const positionEl = document.getElementById("pr-flashcard-position");
        const progressFillEl = document.getElementById("pr-flashcard-progress-fill");
        const emptyEl = document.getElementById("pr-flashcard-empty-state");
        const shellEl = document.querySelector(".pr-flashcard-shell");
        const prevBtn = document.getElementById("pr-prev-btn");
        const nextBtn = document.getElementById("pr-next-btn");

        let questions = [];
        try {
            const [detail] = await Promise.all([
                api.get(`${API_BASE}/topics/${slug}`),
                Glossary.fetchTerms(),
            ]);
            questions = detail.questions;
        } catch (err) {
            questionEl.textContent = `Không tải được câu hỏi: ${err.message}`;
            return;
        }

        const initialMode = params.get("order") === "review" || params.get("order") === "random"
            ? params.get("order")
            : "sequential";
        orderSelect.value = initialMode;
        const startAt = params.has("start") ? parseInt(params.get("start"), 10) : undefined;
        FlashcardController.init(questions, initialMode, startAt);

        function renderCard() {
            if (FlashcardController.isEmpty()) {
                shellEl.classList.add("hidden");
                emptyEl.classList.remove("hidden");
                return;
            }
            shellEl.classList.remove("hidden");
            emptyEl.classList.add("hidden");

            const question = FlashcardController.current();
            const { position, total } = FlashcardController.progress();
            positionEl.textContent = `Câu ${position + 1} / ${total}`;
            progressFillEl.style.width = `${total ? ((position + 1) / total) * 100 : 0}%`;
            questionEl.textContent = question.question;
            answerEl.textContent = question.answer;
            explanationEl.textContent = question.explanation;
            termsEl.innerHTML = Glossary.renderBox(
                question.question,
                question.answer,
                question.explanation,
            );
            prevBtn.disabled = position <= 0;
            nextBtn.disabled = position >= total - 1;
        }

        function doRate(status) {
            FlashcardController.rate(status);
            renderCard();
        }

        function doNext() {
            FlashcardController.next();
            renderCard();
        }

        function doPrev() {
            FlashcardController.prev();
            renderCard();
        }

        prevBtn.addEventListener("click", doPrev);
        nextBtn.addEventListener("click", doNext);
        for (const btn of document.querySelectorAll(".pr-flashcard-rate-actions .pr-rate-btn")) {
            btn.addEventListener("click", () => doRate(btn.dataset.rate));
        }
        orderSelect.addEventListener("change", () => {
            FlashcardController.init(questions, orderSelect.value);
            renderCard();
        });

        KeyboardController.bind({
            onReveal: doNext,
            onRate: doRate,
            onNext: doNext,
            onPrev: doPrev,
        });

        ProgressStore.setLastTopicSlug(slug);
        renderCard();
    }

    // ---------------------------------------------------------------------
    // Page: search
    // ---------------------------------------------------------------------
    function initSearchPage() {
        const input = document.getElementById("pr-search-input");
        const topicFilter = document.getElementById("pr-search-topic-filter");
        const resultsEl = document.getElementById("pr-search-results");
        const countEl = document.getElementById("pr-search-result-count");
        const emptyEl = document.getElementById("pr-search-empty-state");

        const params = new URLSearchParams(window.location.search);
        if (params.get("q")) input.value = params.get("q");
        if (params.get("topic_slug")) topicFilter.value = params.get("topic_slug");

        async function runSearch() {
            const query = input.value.trim();
            resultsEl.innerHTML = "";
            if (!query) {
                countEl.textContent = "";
                emptyEl.classList.remove("hidden");
                emptyEl.querySelector("p").textContent =
                    "Nhập từ khóa để tìm trong 240 câu hỏi, đáp án và giải thích.";
                return;
            }

            const url = new URL(`${API_BASE}/search`, window.location.origin);
            url.searchParams.set("q", query);
            if (topicFilter.value) url.searchParams.set("topic_slug", topicFilter.value);

            let result;
            try {
                result = await api.get(url.pathname + "?" + url.searchParams.toString());
            } catch (err) {
                countEl.textContent = "";
                emptyEl.classList.remove("hidden");
                emptyEl.querySelector("p").textContent = `Lỗi tìm kiếm: ${err.message}`;
                return;
            }

            countEl.textContent = `${result.total} kết quả`;
            emptyEl.classList.toggle("hidden", result.items.length > 0);
            if (result.items.length === 0) {
                emptyEl.querySelector("p").textContent = "Không tìm thấy kết quả phù hợp.";
                return;
            }

            for (const item of result.items) {
                const card = document.createElement("a");
                card.className = "pr-qa-item";
                card.style.display = "block";
                card.style.padding = "14px 16px";
                card.style.textDecoration = "none";
                card.style.color = "inherit";
                card.href = `/practical-review/topics/${item.topic_slug}#question-${item.number}`;
                card.innerHTML = `
                    <div class="muted">${escapeHtml(item.topic_name)}</div>
                    <div><strong>Câu ${item.number}.</strong> ${Search.highlight(item.question, query)}</div>
                `;
                resultsEl.appendChild(card);
            }
        }

        input.addEventListener("input", Search.debounce(runSearch, 250));
        topicFilter.addEventListener("change", runSearch);

        if (input.value.trim()) runSearch();
    }

    // ---------------------------------------------------------------------
    // Entry point
    // ---------------------------------------------------------------------
    function init() {
        const page = document.querySelector(".pr-app")?.dataset.prPage;
        if (page === "overview") {
            initOverviewPage();
        } else if (page === "topic") {
            initTopicPage();
        } else if (page === "study") {
            initStudyPage();
        } else if (page === "search") {
            initSearchPage();
        }
    }

    init();
})();
