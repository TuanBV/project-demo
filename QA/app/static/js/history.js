async function loadHistory() {
    const items = await api.get("/api/history?page=1&page_size=50");
    const body = document.getElementById("history-body");
    body.innerHTML = "";
    for (const item of items) {
        const time = new Date(item.created_at).toLocaleString("vi-VN");
        const tr = document.createElement("tr");
        tr.className = "history-row";
        tr.style.cursor = item.options ? "pointer" : "default";
        tr.innerHTML = `
            <td>${time}</td>
            <td>${escapeHtml((item.question_content || "").slice(0, 80))}</td>
            <td>${escapeHtml(item.category_name)}</td>
            <td>${item.score}</td>
            <td>${classificationBadge(item.classification)}</td>
            <td>${item.response_time_seconds ? item.response_time_seconds.toFixed(1) + "s" : "-"}</td>
        `;
        body.appendChild(tr);

        if (item.options && item.options.length) {
            const detailRow = document.createElement("tr");
            detailRow.className = "history-detail hidden";
            const optionsHtml = item.options
                .map((o) => {
                    let label = "";
                    if (o.is_correct) label = ' <span class="badge correct">Đúng</span>';
                    if (o.is_selected && !o.is_correct) label += ' <span class="badge incorrect">Đã chọn</span>';
                    else if (o.is_selected) label += " (đã chọn)";
                    return `<li>${escapeHtml(o.content)}${label}</li>`;
                })
                .join("");
            detailRow.innerHTML = `
                <td colspan="6">
                    <ul style="margin:4px 0;">${optionsHtml}</ul>
                    ${item.explanation ? `<p class="muted">${escapeHtml(item.explanation)}</p>` : ""}
                </td>
            `;
            body.appendChild(detailRow);
            tr.addEventListener("click", () => detailRow.classList.toggle("hidden"));
        }
    }
}

loadHistory();
