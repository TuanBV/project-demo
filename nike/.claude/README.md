# Claude Code Kit

Thư mục này được tổ chức theo ba nhóm chính: **agents**, **skills** và **rules**.
Tên thư mục được giữ ở dạng chữ thường và số nhiều vì đây là đường dẫn mà Claude Code tự động nhận diện.

```text
.claude/
├── agents/
│   ├── architecture/
│   │   └── project-architect/
│   │       └── AGENT.md
│   ├── backend/
│   │   └── fastapi-backend/
│   │       └── AGENT.md
│   ├── frontend/
│   │   └── vue-frontend/
│   │       └── AGENT.md
│   └── ...
├── skills/
│   ├── audit-project/
│   │   └── SKILL.md
│   ├── fix-build/
│   │   └── SKILL.md
│   └── ...
├── rules/
│   ├── backend/
│   │   ├── fastapi/
│   │   │   └── RULE.md
│   │   └── sqlalchemy/
│   │       └── RULE.md
│   ├── frontend/
│   ├── security/
│   └── ...
├── hooks/
│   └── protect-files.mjs
├── settings.json
└── settings.local.example.json
```

## Quy ước entrypoint

- `AGENT.md`: định nghĩa một Claude Code subagent, có YAML frontmatter như `name`, `description`, `tools`, `model`.
- `SKILL.md`: entrypoint bắt buộc của một skill, có thể gọi bằng `/skill-name`.
- `RULE.md`: một rule được Claude Code nạp tự động; rules được tìm đệ quy trong `.claude/rules/`.

Không đổi ba thư mục gốc thành `Agent`, `SKILL` hoặc `Rule`, vì trên Linux/WSL đường dẫn phân biệt hoa thường và Claude Code chỉ tự động nhận diện các vị trí chuẩn `.claude/agents`, `.claude/skills`, `.claude/rules`.

## Phiên làm việc đầu tiên

1. Mở Claude Code tại thư mục gốc của project.
2. Chạy `/doctor` và `/memory` để kiểm tra discovery.
3. Chạy `/audit-project`.
4. Làm việc theo `CLAUDE.md`, `PROJECT-AUDIT.md` và `docs/completion-roadmap.md` — các file này đã chứa toàn bộ chỉ dẫn thường trực, không cần dán prompt khởi động riêng nữa.
5. Làm từng milestone và kết thúc bằng `/quality-gate full`.

Kit không tự bật plugin hoặc MCP bên thứ ba.
