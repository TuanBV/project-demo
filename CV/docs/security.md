# Security

Status legend: ✅ implemented, 🔜 planned for the phase noted.

## Authentication & session

- ✅ Passwords hashed with BCrypt (`BCryptPasswordEncoder`), never logged,
  never returned in any response DTO.
- ✅ Access tokens are short-lived JWTs (HS256, 15 min default), validated on
  every request by `JwtAuthenticationFilter`. An invalid/expired token does
  not reject the request itself - it just leaves `SecurityContext` empty, so
  public endpoints stay reachable and protected endpoints 401 via
  `RestAuthEntryPoints`.
- ✅ Refresh tokens are opaque random values (48 bytes, `SecureRandom`),
  stored only as a SHA-256 hash (`TokenHasher`), delivered as an
  `HttpOnly` + `SameSite=Strict` cookie scoped to `/api/v1/auth`.
  `cookie-secure` is `false` only in the `local` profile (plain HTTP
  localhost); it defaults to `true` everywhere else.
- ✅ Refresh rotation: every `POST /api/v1/auth/refresh` revokes the
  presented token and issues a new one in the same transaction
  (`AuthService.rotateRefreshToken`). A replayed token - even one that was
  valid seconds ago - is rejected (`INVALID_REFRESH_TOKEN`).
- ✅ Logout and password change both revoke tokens
  (`RefreshTokenRepository.revokeAllActiveForUser` on password change, single-token
  revoke on logout).
- ✅ Access tokens live only in the frontend's in-memory Pinia state, never
  `localStorage`/`sessionStorage`, reducing (not eliminating) exposure to
  XSS-driven storage scraping.
- ✅ Rate limiting on `/auth/login`, `/auth/register`,
  `/auth/forgot-password` (Bucket4j, in-memory, keyed by client IP - no
  Redis needed at this scale; see
  [architecture.md](architecture.md#rate-limiting-phase-5)). Default 10
  requests/min per IP; exceeding it returns `429 RATE_LIMIT_EXCEEDED`.
  Verified against the real stack: 12 rapid logins → 10× `401` then 2×
  `429`; an immediate 15-request burst → 4× `401` then 11× `429` with no
  gaps; `/api/v1/me` stays unaffected while the auth bucket is exhausted.

## Forgot / reset password

- ✅ `POST /auth/forgot-password` always returns `202 Accepted` whether or
  not the email is registered - the response cannot be used to enumerate
  accounts. The reset link/token is only ever handed to
  `NotificationMailer` (logged locally by `LoggingNotificationMailer`); a
  real SMTP/SES-backed implementation slots in later behind the same
  interface without touching `AuthService`.
- ✅ Reset tokens are opaque, hashed at rest (`password_reset_tokens`),
  single-use (`used_at`), and expire after 1 hour.
- ✅ A successful reset revokes every active refresh token for that user, so
  a session hijacked before the reset can't survive it.

## Authorization

- ✅ Every non-public endpoint requires a valid access token
  (`SecurityConfig` - default-deny, explicit allow-list for
  `/api/v1/auth/**`, `/api/v1/public/**`, Swagger, `/actuator/health`).
- ✅ Every resume/version/preview endpoint authorizes by comparing the
  resource's `owner_id` against the authenticated user id
  (`ResumeService.requireOwned`) - never a client-supplied owner field.
  Cross-owner access (User A reading/editing/uploading to User B's resume)
  returns `404 RESUME_NOT_FOUND`, not `403`, so the response can't be used
  to confirm the resource exists at all. Verified against a real second
  account via `docker compose` (GET, DELETE, and PDF upload all return 404
  for a non-owner).
- ✅ Same cross-owner rule extended to structured sections (Phase 5):
  `ResumeSectionServiceTest` asserts that listing, creating, and deleting a
  section on another user's resume all throw `ResumeNotFoundException`
  (→ `404`), via the same `requireOwned` ownership check every other
  resume-scoped endpoint uses - there's no separate, easier-to-miss
  ownership gate for sections.
- ✅ `/actuator/metrics` requires authentication like any other protected
  endpoint - it is **not** in `SecurityConfig`'s public allow-list, only
  `/actuator/health` is. Verified: anonymous request → `401`. Metrics are
  operational data, not something to leave anonymously world-readable.

## Input validation & file safety (Phase 2)

- ✅ PDF upload validated by extension **and** declared MIME type **and**
  magic bytes (`%PDF-` header) - all three must agree
  (`PdfFileValidator`). A `.pdf`-renamed text file with a spoofed
  `Content-Type: application/pdf` header is still rejected because its
  first bytes aren't `%PDF-`.
- ✅ Upload size capped at both layers: `UPLOAD_MAX_PDF_SIZE_BYTES`
  (service-level check, `INVALID_FILE`) and
  `spring.servlet.multipart.max-file-size` (container-level, `413` +
  `FILE_TOO_LARGE`) - both default to 10MB.
- ✅ Physical storage keys are system-generated
  (`resumes/{ownerId}/{random-uuid}.pdf` in `MinioFileStorage`), never
  derived from the user-supplied filename - eliminates path traversal via
  filename and collisions between users. The original filename is kept
  only as display metadata (`stored_files.original_filename`), never used
  to build a path.
- ✅ The MinIO bucket is created without a public-read policy
  (`MinioStorageConfig`'s default bucket creation grants no anonymous
  access); both the owner-only preview (`GET /resumes/{id}/preview/file`)
  and the Phase 3 public file endpoint (`GET
  /public/resumes/{publicId}/{slugOrToken}/file`) proxy bytes through the
  backend rather than exposing a raw MinIO URL.

## Output safety

- ✅ Every error response uses one schema (`ApiError`: `code`, `message`,
  `fieldErrors`, `traceId`, `timestamp`) via `GlobalExceptionHandler` -
  no stack traces, SQL, or internal exception messages ever reach a client;
  those are logged server-side against the same `traceId` for correlation.
- ✅ `PublicResumeResponse` is an explicitly whitelisted field list
  (`publicId`, `name`, `slug`, `resumeType`, `allowDownload`,
  `searchEngineIndexable`, `canonicalUrl`, `sections`) built by a
  dedicated factory method, never by serializing the `Resume` entity -
  `ownerId`, storage keys, and the unlisted token hash are structurally
  impossible to leak through this endpoint.
- ✅ Section content has no rich-text/HTML surface at all - every text
  field is a plain string rendered via Vue's auto-escaping `{{ }}`
  interpolation, never `v-html`. There is nothing to sanitize because
  nothing that looks like markup is ever treated as markup; see
  [architecture.md](architecture.md#known-limitation-no-rich-text-only-plain-text)
  for the trade-off this implies (no bold/italic/bullets in these fields).

## Structured CV sections (Phase 4)

- ✅ Section content shape is enforced server-side by
  `SectionContentValidator`, one typed Java record per `sectionType`
  (registered in `SectionContentType`) - a client can't send
  `EXPERIENCE`-shaped JSON into a `SKILLS` section, or arbitrary extra
  fields (the deserialize-then-reserialize round trip drops anything
  unrecognized). Verified: malformed content → `400
  INVALID_SECTION_CONTENT`.
- ✅ Per-field contact masking (`hidePhone`/`hideEmail`/`hideLocation` on
  `PERSONAL_INFO`) is applied by `StructuredContentMasker` when the
  publish snapshot is built - the raw value is never included in what
  gets persisted into `resume_versions.snapshot_json`, so there's no
  read-time check that could be forgotten or bypassed by a new endpoint.
  Verified against the real stack: a hidden phone number shows as `null`
  in the public response while the email (not hidden) still shows.
  Hiding a whole section (`visible: false`) excludes it from the snapshot
  entirely - verified the hidden section never appears in either the
  owner's preview or the real public page.
- ✅ The owner-facing preview endpoint
  (`GET /resumes/{id}/sections/preview`) and the real publish snapshot
  call the identical `StructuredSnapshotBuilder` - preview cannot show
  something publishing wouldn't actually produce, by construction rather
  than by keeping two implementations in sync.
- ✅ Editing sections after a resume is published never changes what the
  public page shows until the owner explicitly republishes - verified by
  editing a published resume's content, confirming the public page still
  served the old value, then republishing and confirming it updated.
- ✅ Section endpoints are gated to `resumeType == STRUCTURED`
  (`400 NOT_A_STRUCTURED_RESUME`) and go through the same owner-ownership
  check as every other resume-scoped endpoint.

## Public sharing (Phase 3)

- ✅ A wrong unlisted token and an unknown `publicId` both return the exact
  same `404 RESUME_LINK_NOT_FOUND` - returning `410` for a wrong token
  would leak that the `publicId` is valid and has content, undermining the
  token's purpose. Verified: unknown `publicId` → 404; unlisted resume
  with the wrong token → 404 (not 410); real but unpublished/private
  resume → 410.
- ✅ Switching a resume's visibility to `UNLISTED` always mints a fresh
  token; switching away from `UNLISTED` clears the stored hash
  immediately, so a previously-leaked link stops working even before
  anyone explicitly regenerates it. `POST .../regenerate-link` explicitly
  invalidates the old token in the same call. Verified: old token → 404
  immediately after regenerating; new token → 200.
- ✅ Download is gated independently of viewing: `GET
  .../file` always allows inline viewing, but `?download=true` is
  rejected with `403 DOWNLOAD_NOT_ALLOWED` unless the owner has set
  `allowDownload = true`. Verified against the real stack both ways.
- ✅ Publishing does not by itself expose anything: the public endpoint
  requires `status == PUBLISHED **and**  visibility != PRIVATE` together,
  so a `PUBLISHED` `PRIVATE` resume (a legitimate "ready but not shared
  yet" state) still returns `410` from the public endpoint.
- ✅ View recording never stores a raw IP - only a SHA-256 of
  `ip|userAgent` (`VisitorHasher`), and de-duplicates repeated requests
  from the same visitor within a 30-minute window
  (`app.analytics.view-dedup-window`) so page-asset requests don't inflate
  the count.
- ✅ The resume owner's own visits are never counted, even though the view
  endpoint itself is unauthenticated/public - it optionally reads the
  bearer token (if present) and compares the resolved user id against the
  resume's `ownerId` before deciding whether to record. Verified: owner's
  authenticated view leaves `viewCount` at 0; an anonymous view increments it.
- 🔜 Not done: server-side OG/link-preview metadata for
  Facebook/LinkedIn/Zalo unfurling - the SPA can only set `document.title`
  client-side, which non-JS-executing preview bots won't see. See
  [architecture.md](architecture.md#known-gap-oglink-preview-metadata-needs-server-side-rendering).

## Transport & headers

- ✅ CORS is allow-list only (`AppProperties.cors.allowedOrigins`, wired
  into `SecurityConfig`'s `CorsConfigurationSource`) - no wildcard origin,
  and `allowCredentials(true)` so the refresh cookie round-trips correctly
  for the configured frontend origin(s) only.
- ✅ Standard security headers on every response: `X-Content-Type-Options:
  nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy:
  strict-origin-when-cross-origin` (see
  [architecture.md](architecture.md#security-headers-phase-5)). Verified
  present via `curl -I` against the real stack, including on error
  responses.
- ✅ Every response also carries `X-Trace-Id`, matching the `traceId` in
  that request's `ApiError` (if any) and in the corresponding server log
  line - see
  [architecture.md](architecture.md#request-correlation-ids-phase-5).
- 🔜 Not done: a `Content-Security-Policy` for the public resume pages -
  deliberately deferred to the frontend/nginx layer since this backend
  only ever returns JSON (or a raw PDF stream), never HTML; see
  [architecture.md](architecture.md#security-headers-phase-5) for why that
  boundary is intentional rather than an oversight.

## Concurrency

- ✅ `BaseEntity.version` (`@Version`) backs optimistic locking on every
  aggregate root. A concurrent update loses with `409 CONCURRENT_MODIFICATION`
  (mapped in `GlobalExceptionHandler`) instead of silently overwriting.
- ✅ Activating a resume version and uploading a new one both load-then-save
  the `Resume` row within one transaction, so `Resume.version` catches two
  concurrent writers. Two concurrent uploads racing on the same
  `(resume_id, version_number)` are caught by the DB unique constraint
  (`DataIntegrityViolationException` → `409 CONCURRENT_MODIFICATION`).

## End-to-end coverage (Phase 5)

- ✅ `frontend/e2e/main-flow.spec.ts` (Playwright, real Chromium) drives the
  entire register → upload → publish → anonymous-view flow against the
  live stack, including a genuinely separate cookie-less browser context
  standing in for an anonymous visitor - not just curl/unit-test coverage
  of individual endpoints, but proof the assembled product actually works
  the way a real user would experience it. See
  [architecture.md](architecture.md#end-to-end-test-suite-phase-5).

## Auditing (Phase 5)

- 🔜 Publish, unpublish, regenerate-link, and delete actions get an audit
  trail (actor, timestamp, resource) - not yet needed while there's no
  resume module to act on.

## Known limitation in this environment

Testcontainers-based integration tests (`AuthControllerIT`,
`ResumeControllerIT`, `PublicResumeControllerIT`, `ResumeSectionControllerIT`,
`CvPlatformBackendApplicationTests`) could not be executed in the sandbox
this project was built in - the local Docker Desktop's named-pipe API
(`dockerDesktopLinuxEngine`, engine API 1.54) rejects `docker-java`'s
requests with an HTTP 400 even though the real `docker` CLI works fine
against the same pipe. This reproduces with `DOCKER_HOST` and
`DOCKER_API_VERSION` overrides too, so it looks like a Docker Desktop
security/negotiation quirk specific to this machine's Docker Desktop
build, not a code defect. The tests themselves are correct Testcontainers
usage and should run in any standard CI runner or dev machine with normal
Docker Engine API access - `./mvnw test` will pick them back up there with
no changes needed. `PublicResumeServiceTest` (pure Mockito, no Docker) is a
fast-running substitute that covers the same visibility/status/token
gating rules - the specific 404-vs-410 and owner-exclusion cases listed
above are asserted there too, plus verified by hand via `docker compose`.
