# API

Base path: `/api/v1`. Interactive docs (OpenAPI/Swagger, springdoc) are
served by the running backend at:

- `GET /swagger-ui.html` - Swagger UI
- `GET /v3/api-docs` - raw OpenAPI JSON

This file tracks what's implemented per phase; the live Swagger UI is the
source of truth for exact request/response shapes.

## Implemented (Phase 1 - identity)

| Method & path | Auth | Notes |
|---|---|---|
| `POST /api/v1/auth/register` | public | Creates the account and immediately logs in (returns access token + sets refresh cookie) |
| `POST /api/v1/auth/login` | public | Rate-limited, see [Rate limiting](#rate-limiting-phase-5) below |
| `POST /api/v1/auth/refresh` | refresh cookie | Rotates the refresh token; old one is revoked in the same call |
| `POST /api/v1/auth/logout` | refresh cookie | Revokes the presented refresh token, clears the cookie |
| `POST /api/v1/auth/forgot-password` | public | Always `202`, never reveals whether the email exists |
| `POST /api/v1/auth/reset-password` | public (token) | Single-use, 1h-expiry token; revokes all sessions on success |
| `GET /api/v1/me` | bearer | Current user |
| `PATCH /api/v1/me` | bearer | Update display name |
| `POST /api/v1/me/change-password` | bearer | Not in the original endpoint sketch - added to cover the "change password" MVP requirement (§6.1); revokes other sessions on success |

## Implemented (Phase 2 - resume CRUD, PDF upload & versioning)

| Method & path | Auth | Notes |
|---|---|---|
| `GET /api/v1/resumes` | bearer | Own resumes only. `?includeDeleted=true` also returns soft-deleted ones (trash view) |
| `POST /api/v1/resumes` | bearer | `{ name, resumeType: "PDF"\|"STRUCTURED" }` |
| `GET /api/v1/resumes/{resumeId}` | bearer, owner-only | 404 (not 403) if not found or not yours |
| `PATCH /api/v1/resumes/{resumeId}` | bearer, owner-only | `{ name?, isDefault?, visibility?, allowDownload?, searchEngineIndexable? }` - PATCH semantics, `null`/omitted = unchanged. Setting `isDefault: true` atomically unsets the previous default. Setting `visibility: "UNLISTED"` mints a fresh share token, returned once as `unlistedShareToken` in this response only |
| `DELETE /api/v1/resumes/{resumeId}` | bearer, owner-only | Soft delete (`deleted_at`), clears the default flag |
| `POST /api/v1/resumes/{resumeId}/restore` | bearer, owner-only | Not in the original endpoint sketch - added for the "restore within retention window" MVP requirement (§6.2). `409 RESTORE_WINDOW_EXPIRED` past `app.resume.trash-retention` (default 30d) |
| `POST /api/v1/resumes/{resumeId}/duplicate` | bearer, owner-only | Copies metadata + a version-1 reference to the source's active file (no re-upload of bytes) |
| `POST /api/v1/resumes/{resumeId}/versions/pdf` | bearer, owner-only, multipart | Field name `file`. Validates extension + declared MIME + magic bytes + size; becomes the active version immediately |
| `GET /api/v1/resumes/{resumeId}/versions` | bearer, owner-only | Newest first, each with `active: boolean` |
| `POST /api/v1/resumes/{resumeId}/versions/{versionId}/activate` | bearer, owner-only | Rollback to an older version |
| `DELETE /api/v1/resumes/{resumeId}/versions/{versionId}` | bearer, owner-only | `409 CANNOT_DELETE_ACTIVE_VERSION` if it's the active one |
| `GET /api/v1/resumes/{resumeId}/preview/file` | bearer, owner-only | Not in the original endpoint sketch - the owner-only private equivalent of the Phase 3 public file endpoint, needed so the dashboard can preview a PDF before it's ever published |

## Implemented (Phase 3 - publish, public link, analytics)

| Method & path | Auth | Notes |
|---|---|---|
| `POST /api/v1/resumes/{resumeId}/publish` | bearer, owner-only | Requires an active version to exist (`409 CANNOT_PUBLISH` otherwise). Independent of visibility - see [architecture.md](architecture.md#public-resume-url-design--access-gating-phase-3) |
| `POST /api/v1/resumes/{resumeId}/unpublish` | bearer, owner-only | Reverts status to `DRAFT` |
| `POST /api/v1/resumes/{resumeId}/regenerate-link` | bearer, owner-only | Mints a new unlisted token and invalidates the old one immediately, regardless of current visibility. Raw token returned once as `unlistedShareToken` |
| `GET /api/v1/public/resumes/{publicId}/{slugOrToken}` | public | `404` for an unknown `publicId` or a wrong unlisted token; `410` for a real resume that's deleted/unpublished/private. Response is an explicitly whitelisted `PublicResumeResponse`, never the raw entity |
| `GET /api/v1/public/resumes/{publicId}/{slugOrToken}/file` | public | `?download=true` streams `Content-Disposition: attachment` and is rejected with `403 DOWNLOAD_NOT_ALLOWED` unless the owner set `allowDownload=true`; without it, always streams inline regardless of that setting |
| `POST /api/v1/public/resumes/{publicId}/{slugOrToken}/view` | public (optional bearer) | Records a de-duplicated page view; skipped if the optionally-present bearer token identifies the resume's own owner |
| `GET /api/v1/resumes/{resumeId}/analytics/summary` | bearer, owner-only | `{ totalViews, views7d, views30d, lastViewedAt }` |

`{slugOrToken}`: a friendly SEO slug for `PUBLIC` resumes, or the unlisted
share token itself for `UNLISTED` resumes - see
[architecture.md](architecture.md#public-resume-url-design--access-gating-phase-3).

### Error shape (all endpoints)

```json
{
  "code": "RESUME_NOT_FOUND",
  "message": "Resume was not found",
  "fieldErrors": [],
  "traceId": "5b1f...",
  "timestamp": "2026-08-05T03:10:00Z"
}
```

`fieldErrors` is populated only for validation failures (`VALIDATION_FAILED`),
each entry `{ "field": "...", "message": "..." }`.

`traceId` matches the `X-Trace-Id` response header sent on **every**
response (success or error) - see
[architecture.md](architecture.md#request-correlation-ids-phase-5).

### Rate limiting (Phase 5)

`POST /api/v1/auth/{login,register,forgot-password}` (default 10/min/IP)
and every `GET/POST /api/v1/public/**` endpoint (default 60/min/IP) are
rate-limited. Exceeding the limit returns:

```json
{
  "code": "RATE_LIMIT_EXCEEDED",
  "message": "Too many requests, please try again later",
  "fieldErrors": [],
  "traceId": "5b1f...",
  "timestamp": "2026-08-05T03:10:00Z"
}
```

with HTTP status `429`. See
[architecture.md](architecture.md#rate-limiting-phase-5) for the keying
and refill behavior.

## Implemented (Phase 4 - structured sections)

All section endpoints require `resumeType == STRUCTURED`
(`400 NOT_A_STRUCTURED_RESUME` otherwise) and owner auth.

| Method & path | Notes |
|---|---|
| `GET /api/v1/resumes/{resumeId}/sections` | Newest-position-first list, each with its typed `content` |
| `POST /api/v1/resumes/{resumeId}/sections` | `{ sectionType, title, content }`. `409 DUPLICATE_SECTION_TYPE` if one of that type already exists; `400 INVALID_SECTION_CONTENT` if `content` doesn't match the shape for `sectionType` (see `SectionContentType` for the registry) |
| `PATCH /api/v1/resumes/{resumeId}/sections/{sectionId}` | `{ title?, content?, visible? }` - PATCH semantics |
| `DELETE /api/v1/resumes/{resumeId}/sections/{sectionId}` | Hard delete (sections aren't versioned individually - the resume's published snapshot is) |
| `PUT /api/v1/resumes/{resumeId}/sections/order` | `{ sectionIds: [...] }` - must contain exactly the resume's current section ids, each once; `400 INVALID_SECTION_ORDER` otherwise |
| `GET /api/v1/resumes/{resumeId}/sections/preview` | Not in the original endpoint sketch - returns exactly what publishing would produce right now (visible-only, contact fields masked), without publishing anything |

`POST /resumes/{resumeId}/publish` (Phase 3) now also handles
`STRUCTURED` resumes: it builds a snapshot from the current sections and
stores it as a new `ResumeVersion` (`sourceType: STRUCTURED_SNAPSHOT`),
same as a PDF upload becomes a version. `409 CANNOT_PUBLISH` if there are
no visible sections yet. The Phase 3 public endpoints
(`GET /public/resumes/{publicId}/{slugOrToken}`) now include a `sections`
array (masked/visible-only, taken from the published snapshot) when
`resumeType == STRUCTURED`; it's omitted/empty for `PDF` resumes.
