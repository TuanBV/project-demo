// Small fetch wrapper shared by every page. No framework -- plain JS per spec.
async function apiRequest(method, url, body) {
    const options = { method, headers: {} };
    if (body !== undefined && !(body instanceof FormData)) {
        options.headers["Content-Type"] = "application/json";
        options.body = JSON.stringify(body);
    } else if (body instanceof FormData) {
        options.body = body;
    }
    const response = await fetch(url, options);
    const text = await response.text();
    const data = text ? JSON.parse(text) : null;
    if (!response.ok) {
        const message = (data && (data.message || JSON.stringify(data))) || response.statusText;
        throw new Error(message);
    }
    return data;
}

const api = {
    get: (url) => apiRequest("GET", url),
    post: (url, body) => apiRequest("POST", url, body),
    put: (url, body) => apiRequest("PUT", url, body),
    del: (url) => apiRequest("DELETE", url),
};

function escapeHtml(value) {
    if (value === null || value === undefined) return "";
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;");
}

function classificationBadge(classification) {
    const map = {
        CORRECT: "correct",
        MOSTLY_CORRECT: "mostly",
        PARTIALLY_CORRECT: "partial",
        INCORRECT: "incorrect",
    };
    const cls = map[classification] || "incorrect";
    const label = {
        CORRECT: "Chính xác",
        MOSTLY_CORRECT: "Đa phần đúng",
        PARTIALLY_CORRECT: "Đúng một phần",
        INCORRECT: "Chưa chính xác",
    }[classification] || classification;
    return `<span class="badge ${cls}">${escapeHtml(label)}</span>`;
}
