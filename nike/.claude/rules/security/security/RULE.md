# Security Rules
- Never read, print, copy, commit, or invent real credentials.
- Public registration must never accept a privileged role.
- Authorize every resource and mutation server-side; UI hiding is not authorization.
- Hash passwords with a maintained password hasher and constant-time verification.
- Validate uploads by decoded content, size, MIME, extension, path, and authorization.
- Avoid logging passwords, tokens, cookies, reset links, raw request bodies, or PII.
- Return generic authentication/reset responses that do not enable account enumeration.
