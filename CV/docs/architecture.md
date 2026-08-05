# Architecture

## Overview

CV Platform is a **modular monolith**: one Spring Boot deployable, one Vue 3
SPA, organized so business modules stay decoupled enough to later peel off
into services if the product grows into a multi-tenant SaaS. Phase 1 shipped
`identity`; Phase 2 shipped `resume` CRUD/versioning and `storage`; Phase 3
shipped `sharing` (public link resolution) and `analytics` (view tracking);
Phase 4 shipped structured (web) CV sections; Phase 5 hardened the whole
stack (rate limiting, security headers, request correlation ids,
cross-owner authorization tests, a real-browser E2E suite). See
[roadmap.md](roadmap.md) for what's next.

## Why modular monolith

A single deployable keeps local dev and MVP operations simple (one DB, one
process, one deploy). Package-by-module with a strict dependency direction
means a future extraction (e.g. `analytics` becoming its own service) is a
matter of drawing an API boundary that already exists in code, not a rewrite.

## Layering

Every module follows the same call direction:

```
Controller (api)  ->  Application Service  ->  Domain / Entity  ->  Repository (infrastructure)
```

- Controllers never touch a `Repository` directly.
- DTOs (`api/dto`) are separate types from JPA entities (`domain`) - entities
  never cross the REST boundary, so adding a persistence-only field can't
  accidentally leak into a response.
- Cross-module calls go through a module's `application` service, never
  reaching into another module's `domain`/`infrastructure` packages.

## Module map

| Module | Owns | Status |
|---|---|---|
| `common` | Error handling (`ApiError`, `GlobalExceptionHandler`), `BaseEntity` (auditing + optimistic lock), env config (`AppProperties`), shared security utils (`TokenHasher`, `Checksums`) | Phase 1 |
| `identity` | User accounts, password hashing, JWT access tokens, refresh token rotation, forgot/reset password | Phase 1 |
| `profile` | Avatar, headline, bio, contact info | Not started - `user_profiles` table exists (Phase 1) but unused; see roadmap |
| `resume` | Resume CRUD, soft-delete/restore, duplicate, default flag, `ResumeVersion` + PDF upload/rollback, publish/unpublish, visibility + unlisted-token lifecycle, `ResumeSection` CRUD + publish-time snapshotting | Phase 2-4 done |
| `storage` | `FileStorage` abstraction + `MinioFileStorage` | Phase 2 done; S3 implementation not yet needed |
| `sharing` | Public link resolution (`PublicResumeController`/`PublicResumeService`): visibility/status gating, download policy enforcement, view-record delegation | Phase 3 done |
| `analytics` | Resume view tracking + dedup + summary aggregates | Phase 3 done |

## Authentication design

- **Access token**: short-lived JWT (default 15 min), HS256, returned in the
  JSON response body only. The frontend keeps it in a Pinia store
  (in-memory) - never in `localStorage`, so it isn't reachable by a
  same-origin XSS payload reading storage APIs after the fact (defense in
  depth; XSS itself must still be prevented separately).
- **Refresh token**: opaque random value, sent as an `HttpOnly` /
  `SameSite=Strict` cookie scoped to `/api/v1/auth`. Only its SHA-256 hash is
  persisted (`refresh_tokens.token_hash`) - the raw value exists only in the
  cookie. Every refresh **rotates** the token: the presented one is revoked
  and a new one issued in the same request, so a replayed/stolen-but-used
  token cannot succeed twice.
- **Session bootstrap**: on app load, the frontend calls `POST
  /api/v1/auth/refresh` once (cookie sent automatically) before mounting, so
  a page reload doesn't force a re-login as long as the refresh cookie is
  still valid.
- Full detail in [security.md](security.md).

## Public resume URL design & access gating (Phase 3)

Public CVs share one path shape regardless of visibility:
`/cv/{publicId}/{slugOrToken}`, backed by `GET /api/v1/public/resumes/{publicId}/{slugOrToken}`.

- `publicId` is a random UUID - never a sequential DB id - so it can't be
  enumerated.
- For `PUBLIC` resumes, the last segment is a human-friendly SEO slug; it is
  **not** treated as secret and isn't even validated - `PublicResumeService`
  serves the resume for *any* slug value once the `publicId` matches, matching
  the "slug is cosmetic, `publicId` is the real key" design.
- For `UNLISTED` resumes, the last segment **is** the unlisted share token
  itself (opaque, unguessable, `TokenHasher.generateOpaqueToken(24)`). The
  backend compares its SHA-256 against `resumes.unlisted_token_hash`.
- `PRIVATE` resumes never resolve through the public endpoint regardless of
  what's in the URL.

**404 vs. 410, deliberately different:**
- **Unknown `publicId`, or an `UNLISTED` resume with a wrong/missing
  token** → `404 RESUME_LINK_NOT_FOUND`. These two cases are made to look
  identical on purpose: if a wrong-token request instead returned 410
  ("exists, just gone"), that would confirm to an attacker that a given
  `publicId` is real and has content, which weakens the token's whole
  purpose. Both "never existed" and "exists but you guessed the token
  wrong" must be indistinguishable.
- **Real `publicId`, but the resume is deleted, unpublished (`status !=
  PUBLISHED`), or `PRIVATE`** → `410 RESUME_LINK_GONE`. This is the owner's
  own resume becoming intentionally unreachable, not a guessing attack, so
  there's no symmetry constraint to preserve - a clear "no longer
  available" message is better UX than a bare 404.
- Enforced in one place, `PublicResumeService.resolvePublic()`, so every
  public endpoint (data, file, view) shares exactly the same gate - a new
  endpoint can't accidentally skip a check.

**Publish is independent of visibility.** `POST /resumes/{id}/publish` only
requires an active version to exist; it does not require (or change)
visibility. A `PUBLISHED` + `PRIVATE` resume is a valid, intentional state
("ready to share, just not yet") - the public endpoint's gate checks
`status == PUBLISHED AND visibility != PRIVATE` together, so publishing
alone never makes anything publicly reachable.

**Switching visibility to/from `UNLISTED` always touches the token:**
entering `UNLISTED` mints a brand-new token (never reuses one from a
previous unlisted period that might have leaked); leaving `UNLISTED`
clears the stored hash so an old leaked link can't work again even if
visibility is switched back later without an explicit regenerate. The raw
token is returned in the API response **only** for the mutation that just
generated it (visibility→UNLISTED, or `POST .../regenerate-link`) - see
`ResumeMutationResult`/`ResumeResponse.unlistedShareToken`. It is never
persisted or re-derivable, so the frontend must capture and show it
immediately (`ResumeEditPage`'s "reveal" dialog) or the user has to
regenerate to see it again.

## View tracking & privacy (Phase 3)

- `AnalyticsService.recordView` de-duplicates by `(resumeId, visitorHash)`
  within `app.analytics.view-dedup-window` (default 30 min) - repeated
  requests from the same visitor (page reloads, asset fetches) collapse
  into one page view instead of inflating the count.
- `VisitorHasher` computes a SHA-256 of `ip|userAgent` on the fly; the raw
  IP is never persisted anywhere, only the hash - satisfies "don't retain
  raw IPs" without needing a separate purge job.
- The owner's own visits never count: `PublicResumeController`'s view
  endpoint stays public/unauthenticated, but still optionally reads the
  bearer token via `CurrentUserProvider.optionalUserId()` and skips
  recording when the resolved user id matches the resume's `ownerId`.
  Verified against the real stack: an owner's authenticated view leaves
  `viewCount` at 0, an anonymous view increments it to 1.
- `ReferrerNormalizer` keeps only the referring **host** (e.g.
  `linkedin.com`), never the full URL - avoids storing query-string
  tracking parameters. `UserAgentClassifier` is a small heuristic bucket
  (desktop/mobile/tablet/bot), not a full UA-parsing dependency.

## Known gap: OG/link-preview metadata needs server-side rendering

The product brief wants rich link previews when a public CV is shared on
Facebook/LinkedIn/Zalo. `PublicResumePage.vue` does set `document.title`
client-side, which works for crawlers that execute JavaScript, but most
link-unfurling bots **do not** run JS - they read `<meta property="og:*">`
tags from the initial HTML response, which this SPA can't provide (the
served `index.html` is static and identical for every route). Properly
fixing this needs either SSR/prerendering for the `/cv/:publicId/:slug`
route or a bot-user-agent-triggered server-rendered fallback from the
backend. Neither fits Phase 3's scope - tracked as a follow-up in
[roadmap.md](roadmap.md) rather than silently claimed as done.

## Storage abstraction & PDF versioning (Phase 2)

- **`FileStorage` interface** (`storage/FileStorage.java`): `store`,
  `loadPrivate`, `createTemporaryReadUrl`, `delete`. `MinioFileStorage` is
  the only implementation today; an S3-native implementation can be added
  later behind the same interface without touching `ResumeService`.
- The whole upload is loaded into memory as `byte[]` (`StoreFileCommand`)
  rather than streamed - simpler checksum computation, and fine at the
  10MB PDF cap. Revisit only if the max upload size grows substantially.
- **Every PDF upload becomes the active version immediately** - there is no
  separate "publish this version" step for PDFs; the explicit `activate`
  endpoint exists for *rollback* to an older version, not for promoting a
  new one. This matches the product flow: "upload v2 → the link now shows
  v2 → I can roll back to v1 if v2 was a mistake."
- **`duplicate()` does not re-upload file bytes.** It copies the resume's
  metadata and creates a version 1 for the new resume that points at the
  *same* `stored_files` row as the source's active version - safe because
  stored files are immutable once written, and it avoids doubling object
  storage usage for what is otherwise identical content.
- **Optimistic locking already covers the version-activation race**
  identified in Phase 1's risk list: `activateVersion`/`uploadPdfVersion`
  both load-then-save the `Resume` row inside one `@Transactional` method,
  so `Resume.version` catches two concurrent writers (`409
  CONCURRENT_MODIFICATION`). A rarer race - two concurrent uploads to the
  same resume both computing the same next `version_number` - is caught by
  the DB's `(resume_id, version_number)` unique constraint and mapped from
  `DataIntegrityViolationException` to the same error code.

## Resume content storage: JSONB vs. relational (Phase 4)

`resume_sections.content_json` is `JSONB`, not one child table per section
type. Trade-off:

- **JSONB (chosen)**: one table handles 10 heterogeneous section shapes
  (skills vs. work experience vs. education) without a join explosion when
  rendering/reordering a CV. Validation moves to the application layer -
  `SectionContentValidator` deserializes each `section_type` into its own
  typed Java record (`SkillsContent`, `ExperienceContent`, ... registered in
  `SectionContentType`) via Jackson before persisting, then re-serializes
  the typed object back to JSON. That round-trip both validates the shape
  *and* normalizes the stored JSON (drops unknown fields, applies record
  defaults) - so `resume_sections.content_json` never contains anything
  that doesn't match its type's schema, without a DB constraint doing it.
- **Fully relational (rejected for MVP)**: stronger DB-level integrity, but
  8-10 extra tables and multi-way joins just to render one CV page. Revisit
  if a section type needs to be queried/filtered independently of its
  parent resume (not a current requirement).
- `resume_sections` has a **unique `(resume_id, section_type)`** constraint
  - a resume gets at most one section per type (e.g. one "Experience"
    section holding a list of jobs), not several standalone ones. This
    matches the fixed section list from the product brief and keeps the
    frontend's "add section" UI simple (offer only the types not yet
    present).

## Per-field visibility & the publish snapshot (Phase 2-4)

`resume_versions.snapshot_json` stores an immutable snapshot taken at
publish time - for `STRUCTURED` resumes, that's the current sections
(visible-only, in position order); for `PDF` resumes it's unused (the
version instead points at a `stored_files` row). The public page always
serves the last published snapshot, never live draft data - verified
end-to-end: editing a section's content after publishing does **not**
change what the public page shows until the owner explicitly publishes
again, at which point a fresh snapshot is taken and the old one is
superseded (same `active_version_id` mechanism PDF rollback already used).

**Section-level `visible` vs. field-level hiding are two different
mechanisms, both applied when the snapshot is built, never at read time:**
- `StructuredSnapshotBuilder.buildVisibleSections()` first drops any
  section with `visible = false` entirely (e.g. a hidden "Additional
  info" section never appears in the snapshot at all).
- `StructuredContentMasker` then blanks out individual `PERSONAL_INFO`
  contact fields the owner marked hidden (`hidePhone`/`hideEmail`/
  `hideLocation`) - the field name still appears in the JSON with a `null`
  value (so the frontend's rendering logic doesn't need to special-case a
  missing key), but the actual value never leaves the backend.
- Both the **preview** endpoint (`GET .../sections/preview`, owner-only,
  pre-publish) and the **real publish snapshot** call the exact same
  builder - preview can never show something different from what
  publishing would actually produce, because they're not two
  implementations of the same rule, they're one.

The `snapshot_json`/`content_json` entity fields are annotated
`@JdbcTypeCode(SqlTypes.JSON)` (Hibernate 6) rather than a plain
`@Column` - without it, PostgreSQL's JDBC driver binds the parameter as
`varchar` and Postgres rejects that against a `jsonb` column *even when
the value is `NULL`*. This broke every Phase 2 PDF upload until caught by
manual end-to-end testing against the real Docker Compose stack (see
[roadmap.md](roadmap.md)) - the fix was applied proactively to
`ResumeSection.contentJson` from the start in Phase 4, rather than
waiting to hit the same bug twice.

## Frontend: one generic form pattern for ten section types (Phase 4)

Rather than ten bespoke Vue components, every section type is described
declaratively in `src/config/sectionFields.ts` as either:
- an **object** shape (`PERSONAL_INFO`, `SUMMARY`, `ADDITIONAL`) - rendered
  by `SectionObjectForm.vue`, one input per field; or
- a **list** shape (`EXPERIENCE`, `EDUCATION`, `PROJECTS`, `SKILLS`,
  `LANGUAGES`, `CERTIFICATIONS`, `LINKS`) - a repeatable array of items
  under one key (e.g. `{ items: [...] }` or `{ skills: [...] }`) - rendered
  by `RepeatableItemList.vue`, one card per item with add/remove.

Both the editor (`StructuredSectionManager.vue`) and the read-only
template (`StructuredResumeView.vue`, shared by the owner's preview dialog
and the real public page) key off the same `SECTION_FIELD_CONFIG`/
`SECTION_LABELS` maps, so adding an eleventh section type only means
adding one config entry plus one render branch in the view component -
not a whole new form component.

Sections are saved via an explicit **"Lưu" (Save) button per section**,
not autosave/debounce - simpler to reason about, and nothing is sent to
the server (so nothing can be lost) until the user deliberately clicks
it; a failed save leaves the in-memory draft untouched.

## Known limitation: no rich text, only plain text

Section text fields (summary, descriptions, additional info) are plain
strings rendered with Vue's default `{{ }}` interpolation (auto-escaped) -
there is no WYSIWYG/rich-text editor and no HTML is ever accepted or
rendered from user content. This is a deliberate simplification: it
satisfies "sanitize rich text / never render unsanitized HTML" by the
simplest possible means (there is no HTML to sanitize), at the cost of no
bold/italic/bullet formatting in these fields. If rich text is added
later, server-side HTML sanitization before persisting becomes mandatory.

## Frontend architecture

- Vue 3 + `<script setup>` + TypeScript, Vite, Quasar for components, Pinia
  for state, Vue Router for navigation.
- `src/api/client.ts` is the single Axios instance: attaches the in-memory
  access token, and on a 401 attempts exactly one silent refresh before
  giving up (see `src/api/client.ts`'s response interceptor).
- `src/stores/auth.ts` owns session state; no other store or component talks
  to `authApi` directly.
- Route guards (`src/router/index.ts`) redirect unauthenticated users away
  from `requiresAuth` routes and authenticated users away from
  `guestOnly` routes (login/register).

## Rate limiting (Phase 5)

- `RateLimiter` (`common/web`) wraps [Bucket4j](https://github.com/bucket4j/bucket4j)
  (`bucket4j_jdk17-core`), one in-memory `Bucket` per key in a
  `ConcurrentHashMap`. No Redis: this is a single-instance monolith, so a
  process-local bucket is enough - revisit only if the backend ever runs as
  more than one instance behind a load balancer, since buckets don't sync
  across processes.
- Buckets use Bucket4j's **greedy refill** (`Bandwidth.builder().capacity(n)
  .refillGreedy(n, window).build()`): tokens trickle back continuously
  across the window rather than resetting all-at-once at a window boundary.
  Verified against the real stack: after exhausting the login bucket,
  single follow-up requests succeed intermittently (~1 token every ~6s for
  a 10/60s bucket) while a genuine burst is still capped at 10 - this is
  correct Bucket4j behavior, not a bug (see the greedy-refill note this
  caused during testing).
- `RateLimitFilter` (a plain `OncePerRequestFilter`, not part of the
  authorization chain) buckets requests into two categories by path/method:
  `"auth"` for `POST /api/v1/auth/{login,register,forgot-password}`
  (default 10/min), `"public"` for anything under `/api/v1/public/**`
  (default 60/min). Everything else is unthrottled. Limits are keyed by
  `ClientIpResolver.resolve(request)` (first `X-Forwarded-For` hop, else
  `getRemoteAddr()`) combined with the category, so one visitor exhausting
  the public-view bucket doesn't affect another visitor or another
  endpoint. Exceeding the limit returns `429` with the standard `ApiError`
  shape (`RATE_LIMIT_EXCEEDED`).
- Registered via `.addFilterBefore(new RateLimitFilter(...),
  JwtAuthenticationFilter.class)` in `SecurityConfig` - explicitly anchored
  before the JWT filter (not just "added in registration order") so the
  chain order (`RateLimitFilter` → `JwtAuthenticationFilter` →
  `UsernamePasswordAuthenticationFilter`) is unambiguous from the code
  itself.
- `app.rate-limit.enabled=false` in `application-test.yml` - integration
  tests fire many requests per test class against the same IP/category and
  would otherwise trip the limiter; the feature itself is covered in
  isolation by `RateLimiterTest` (pure unit test, no Spring context).

## Security headers (Phase 5)

- Added via Spring Security's `headers()` DSL in `SecurityConfig`:
  `frameOptions().deny()` (no framing at all - this API serves JSON, not
  pages meant to be embedded) and `referrerPolicy(STRICT_ORIGIN_WHEN_CROSS_ORIGIN)`.
  `X-Content-Type-Options: nosniff` and a baseline `X-Frame-Options` are
  already Spring Security defaults, not something added here.
- **Deliberately no `Content-Security-Policy` here.** A strict CSP is only
  meaningful on the layer that serves HTML - this backend returns JSON
  (`application/json`) for every endpoint except the raw PDF file stream, so
  there's no inline script/style surface for a backend-issued CSP to
  restrict. The real CSP belongs on the frontend's nginx layer
  (`frontend/nginx.conf`, production image) where actual HTML is served -
  tracked as a frontend/infra concern, not silently skipped.

## Request correlation ids (Phase 5)

- `RequestCorrelationFilter` (a `FilterRegistrationBean` with
  `Ordered.HIGHEST_PRECEDENCE`, registered outside the Spring Security
  filter chain entirely) generates one UUID per request, puts it in SLF4J's
  MDC under `traceId`, and echoes it back as an `X-Trace-Id` response
  header - on every request, including ones Spring Security itself
  rejects (401/403 before the JWT filter runs), since it sits ahead of the
  whole chain.
- `GlobalExceptionHandler.newTraceId()` reads the same MDC value for
  `ApiError.traceId` instead of minting a fresh, disconnected UUID - so the
  id a client sees in an error response is the *exact* id that appears
  against the corresponding server log line
  (`logging.pattern.level: "%5p [traceId=%X{traceId:-}]"`), letting a
  user-reported trace id be grepped straight out of the logs.

## End-to-end test suite (Phase 5)

- `frontend/e2e/main-flow.spec.ts` runs a real Chromium browser (Playwright)
  against the live Docker Compose stack: register → create a PDF resume →
  upload a real PDF → switch visibility to `PUBLIC` → publish → open the
  resulting public link in a **fresh, cookie-less browser context**
  (`browser.newContext()`, standing in for an anonymous recruiter who never
  logged in) → assert the CV name and PDF viewer render. This exercises the
  full stack (frontend build, backend API, MinIO, Postgres) in a way curl
  scripts and unit tests can't - it's the only test that actually drives
  the Quasar UI.
- Kept in a separate `e2e/` directory with its own `playwright.config.ts`
  and its own `test`/`expect` import, deliberately excluded from Vitest's
  glob (`vite.config.ts`'s `test.exclude: [..., 'e2e/**']`) since the two
  runners' `test()` APIs aren't interchangeable.
- Run with `npm run test:e2e` (see README.md) - requires the Compose stack
  already up, since this hits the real running frontend/backend rather than
  a mocked environment.

## Local infrastructure

`docker-compose.yml` (repo root of this project, `CV/`) runs:

- `postgres` (16-alpine) - port `5433` on the host to avoid colliding with
  sibling projects in this monorepo (`QA` uses 8000, `nike` uses
  8001/3307/6379/5000).
- `minio` - S3-compatible storage backing the `storage` module since
  Phase 2, ports `9012` (S3 API) / `9013` (web console) on the host - `9002`
  collided with an unrelated project already running on this machine, so
  don't assume `9002` even though that's MinIO's usual default.
- `backend` - built from `backend/Dockerfile`, port `8082`.
- `frontend` - runs the Vite dev server directly (bind-mounted source, hot
  reload) rather than a built image, since this compose file targets local
  development. `frontend/Dockerfile` is the production image (multi-stage
  build → nginx) used for prod builds, not by `docker-compose.yml`.
