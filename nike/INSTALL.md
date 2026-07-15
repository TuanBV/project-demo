# Cài Claude Kit

Sao chép toàn bộ file và thư mục ẩn trong package này vào thư mục gốc của project, giữ nguyên đường dẫn.

Cấu trúc chính:

```text
.claude/
├── agents/<nhóm>/<agent-name>/AGENT.md
├── skills/<skill-name>/SKILL.md
├── rules/<nhóm>/<rule-name>/RULE.md
├── hooks/
└── settings.json
```

Lưu ý: dùng đúng các thư mục chuẩn chữ thường `agents`, `skills`, `rules`. Chỉ skill dùng entrypoint bắt buộc `SKILL.md`; agent dùng `AGENT.md`, rule dùng `RULE.md` để dễ phân biệt, và Claude Code vẫn tìm chúng đệ quy.

Sau khi chép:

1. chạy `node scripts/quality-gate.mjs --quick`;
2. mở Claude Code tại cùng thư mục;
3. chạy `/doctor`, `/memory`, `/audit-project`;
4. làm việc theo `CLAUDE.md`, `PROJECT-AUDIT.md` và `docs/completion-roadmap.md` (đã chứa toàn bộ chỉ dẫn thường trực);
5. chạy `/quality-gate full` trước khi release.

Kit không chứa plugin hoặc MCP bên thứ ba.
