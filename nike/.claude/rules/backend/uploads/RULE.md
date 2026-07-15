---
paths:
  - "api/image/**/*.py"
  - "api/sale/**/*.py"
  - "api/router/image.py"
  - "upload/**/*"
---
# Upload Rules
- Reject untrusted base64/extension combinations and enforce decoded size limits.
- Generate collision-resistant names and create directories safely.
- Store public URL/path separately from filesystem path.
- Delete or orphan-clean files transactionally when database writes fail.
- Uploaded runtime files are not source-controlled test fixtures.
