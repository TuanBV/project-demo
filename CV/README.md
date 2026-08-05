# CV Platform

A modular-monolith platform for candidates to store, manage, and share their
CVs through a stable public link - either an uploaded PDF or a
responsive, structured web CV - instead of forcing recruiters to download a
file. Not a job board: no recruiter accounts, no job applications, no
payments. See [docs/roadmap.md](docs/roadmap.md) for what's explicitly out
of scope.

**Current status: Phases 1-5 complete** (Foundation, Resume & PDF,
Publish & public link, Structured CV, Hardening). Accounts/login/sessions,
resume CRUD with PDF upload/versioning/rollback, publish/visibility/
download-policy/view tracking, structured (web) CVs with a section editor
and a responsive public template, and hardening (rate limiting, security
headers, request correlation ids, cross-owner authorization tests, a real-
browser E2E suite) all work end-to-end. There is no Phase 6 in
[docs/roadmap.md](docs/roadmap.md) - see it for a few small explicitly
deferred follow-ups (e.g. a shared rate-limit store if this ever scales to
multiple instances).

## Tech stack

- **Backend**: Java 21, Spring Boot 3.5, Spring Security, Spring Data JPA,
  PostgreSQL, Flyway, springdoc-openapi, JJWT, MinIO SDK, JUnit 5 +
  Mockito + Testcontainers. (Spring Boot is pinned to the 3.5 line rather
  than the newer 4.x because springdoc/JJWT don't yet support Spring
  Framework 7 - see [docs/architecture.md](docs/architecture.md).)
- **Frontend**: Vue 3 + TypeScript, Vite, Quasar, Pinia, Vue Router, Axios,
  Vitest, `@vue/test-utils`.
- **Infra**: Docker Compose (PostgreSQL, MinIO, backend, frontend) for
  local development.

## Repository layout

```
CV/
├── backend/    Spring Boot app (Maven) - see backend/src/main/java/com/cvplatform
├── frontend/   Vue 3 + Quasar SPA
├── docs/       architecture.md, security.md, api.md, roadmap.md
├── docker-compose.yml
└── .env.example
```

## Prerequisites

- Docker Desktop (or another Docker Engine) with Compose v2
- For running outside Docker: JDK 21 and Node.js 20+ / npm

## Quick start (Docker Compose)

```bash
cd CV
cp .env.example .env      # adjust values if needed, especially before deploying anywhere real
docker compose up -d --build
```

This starts:

| Service | URL | Notes |
|---|---|---|
| `frontend` | http://localhost:5174 | Vite dev server, hot reload |
| `backend` | http://localhost:8082 | Swagger UI at `/swagger-ui.html` |
| `postgres` | localhost:5433 | user/db from `.env` |
| `minio` | http://localhost:9012 (API), http://localhost:9013 (console) | backs PDF storage; bucket is created automatically on backend startup |

Tear down with `docker compose down` (add `-v` to also drop the named
volumes / start from a clean database).

### Verify the auth flow is working

Open http://localhost:5174, register an account, and you should land on
`/dashboard/cvs` showing your display name. Or from the command line:

```bash
curl -c cookies.txt -X POST http://localhost:8082/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"demo-password-1","displayName":"Demo User"}'
# -> { "accessToken": "...", "user": { ... } } and a cv_refresh_token cookie in cookies.txt

curl http://localhost:8082/api/v1/me -H "Authorization: Bearer <accessToken from above>"
# -> current user

curl -b cookies.txt -X POST http://localhost:8082/api/v1/auth/refresh
# -> a new accessToken; replaying the same cookie again afterwards now returns 401
```

### Verify the resume/PDF upload flow

From the dashboard UI: create a CV (type "PDF"), open it, choose a `.pdf`
file and click Upload - it becomes version 1 and "Đang dùng" (active).
Upload a second file and it becomes the new active version; the first is
still listed and can be restored via "Đặt làm active" (rollback), or
deleted once it's no longer active.

From the command line (note: on Windows/Git Bash, curl needs a native
Windows path for `-F @path`, e.g. via `cygpath -w`):

```bash
TOKEN=$(curl -s -X POST http://localhost:8082/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"demo-password-1","displayName":"Demo User"}' \
  | node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>console.log(JSON.parse(d).accessToken))")

RESUME=$(curl -s -X POST http://localhost:8082/api/v1/resumes \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"My CV","resumeType":"PDF"}')
# -> note the "id" and "publicId" in the response

curl -X POST http://localhost:8082/api/v1/resumes/<id>/versions/pdf \
  -H "Authorization: Bearer $TOKEN" -F "file=@/path/to/resume.pdf;type=application/pdf"
# -> versionNumber 1, active: true

curl http://localhost:8082/api/v1/resumes/<id> -H "Authorization: Bearer $TOKEN"
# -> same "publicId" as before - uploading a new version never changes it
```

### Verify publishing & the public link

From the dashboard UI: open a CV that already has an uploaded PDF, go to
"Chia sẻ & Xuất bản", set visibility to `PUBLIC`, click "Xuất bản". A
public link + QR code appear immediately; open the link in an incognito
window to see the same page an unauthenticated visitor would - PDF inline
viewer, no download button (until you also toggle "Cho phép tải PDF"),
and a "Lượt xem" counter on the edit page that increments for that
incognito visit but never for your own logged-in visits.

To try `UNLISTED` instead: switching visibility to `UNLISTED` shows the
share link + QR **once**, in a dialog - copy it then, because the backend
never stores or re-shows the raw token (only its hash). "Tạo lại link"
invalidates the old one immediately.

From the command line, continuing from the resume created above:

```bash
curl -X PATCH http://localhost:8082/api/v1/resumes/<id> \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"visibility":"PUBLIC"}'

curl -X POST http://localhost:8082/api/v1/resumes/<id>/publish -H "Authorization: Bearer $TOKEN"
# -> "status": "PUBLISHED"

curl http://localhost:8082/api/v1/public/resumes/<publicId>/<slug>
# -> works with no Authorization header at all

curl -X POST http://localhost:8082/api/v1/resumes/<id>/unpublish -H "Authorization: Bearer $TOKEN"
curl -o /dev/null -w "%{http_code}\n" http://localhost:8082/api/v1/public/resumes/<publicId>/<slug>
# -> 410, not 404 - the link existed, it's just not public anymore
```

### Verify structured (web) CVs

From the dashboard UI: create a CV with type "STRUCTURED", open it, and
use "Thêm mục" to add sections (Personal info, Summary, Skills,
Experience, ...) - one of each type. Each section expands to a form; edit
it and click "Lưu" to save (nothing is sent until you do, so a failed
save never loses your draft). Use the up/down arrows to reorder, the
toggle to hide a section, and "Xem trước" to see exactly what publishing
would produce - including a hidden phone/email/location showing as
blank, if you've checked those boxes in "Thông tin cá nhân". Publish and
visit the public link the same way as a PDF resume; the public page now
renders your sections responsively (and prints cleanly via the browser's
print dialog).

```bash
RESUME=$(curl -s -X POST http://localhost:8082/api/v1/resumes \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"Web CV","resumeType":"STRUCTURED"}')
# -> note the "id"

curl -X POST http://localhost:8082/api/v1/resumes/<id>/sections \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"sectionType":"SUMMARY","title":"Summary","content":{"text":"Backend engineer."}}'

curl http://localhost:8082/api/v1/resumes/<id>/sections/preview -H "Authorization: Bearer $TOKEN"
# -> exactly what publishing would produce right now, without publishing anything

curl -X POST http://localhost:8082/api/v1/resumes/<id>/publish -H "Authorization: Bearer $TOKEN"
curl http://localhost:8082/api/v1/public/resumes/<publicId>/<slug>
# -> includes a "sections" array now

# Edit the section, then check the public page BEFORE republishing:
curl -X PATCH http://localhost:8082/api/v1/resumes/<id>/sections/<sectionId> \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"content":{"text":"Updated text"}}'
curl http://localhost:8082/api/v1/public/resumes/<publicId>/<slug>
# -> still shows the OLD text - editing never touches an already-published snapshot

curl -X POST http://localhost:8082/api/v1/resumes/<id>/publish -H "Authorization: Bearer $TOKEN"
curl http://localhost:8082/api/v1/public/resumes/<publicId>/<slug>
# -> now shows "Updated text"
```

### Verify rate limiting & security headers

```bash
# Security headers are present on every response, success or error:
curl -i http://localhost:8082/api/v1/me
# -> X-Content-Type-Options: nosniff
# -> X-Frame-Options: DENY
# -> Referrer-Policy: strict-origin-when-cross-origin
# -> X-Trace-Id: <uuid>  (matches "traceId" in any ApiError body)

# Login is rate-limited to 10/min/IP - fire a quick burst:
for i in $(seq 1 15); do
  curl -s -o /dev/null -w "%{http_code} " http://localhost:8082/api/v1/auth/login \
    -H "Content-Type: application/json" -d '{"email":"nobody@example.com","password":"wrong"}'
done; echo
# -> mostly "401 ..." for the first ~10, then "429 ..." for the rest.
# Bucket4j's refill is continuous ("greedy"), not a hard per-minute reset -
# a single request sent right after a burst may occasionally succeed again
# (401, not 429) if enough time passed for one token to trickle back; a
# tight burst like this one reliably shows the 429s. See
# docs/architecture.md#rate-limiting-phase-5.

# /actuator/metrics requires auth like any other protected endpoint:
curl -o /dev/null -w "%{http_code}\n" http://localhost:8082/actuator/metrics
# -> 401
```

### Running the E2E tests

The E2E suite drives a real Chromium browser against the live stack (not
mocked), so `docker compose` must already be up (Quick Start above) before
running it:

```bash
cd frontend
npm install
npx playwright install chromium   # one-time browser download
npm run test:e2e
```

By default it targets `http://localhost:5174`; override with
`E2E_BASE_URL` if the frontend is running somewhere else. See
[docs/architecture.md](docs/architecture.md#end-to-end-test-suite-phase-5)
for what the one flow covers.

## Running without Docker

### Backend

```bash
cd backend
cp .env.example .env 2>/dev/null || true   # or export the vars from the root .env.example manually
./mvnw spring-boot:run
# Needs a Postgres reachable at DB_HOST:DB_PORT (default localhost:5432) -
# either `docker compose up -d postgres` from the repo root, or your own instance.
```

Runs on `:8080` by default (`SERVER_PORT` to override). Active profile
defaults to none; pass `-Dspring-boot.run.profiles=local` to relax the
refresh-cookie `Secure` flag for plain-HTTP localhost testing.

### Frontend

```bash
cd frontend
cp .env.example .env   # VITE_API_BASE_URL
npm install
npm run dev
```

Runs on `:5174` (configured in `vite.config.ts`).

## Environment variables

See [`.env.example`](.env.example) (Docker Compose / shared) and
[`frontend/.env.example`](frontend/.env.example) (frontend-only, when
running outside Compose). Key backend variables (all have safe local
defaults - see `backend/src/main/resources/application.yml`):

| Variable | Purpose |
|---|---|
| `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USERNAME`, `DB_PASSWORD` | PostgreSQL connection |
| `JWT_SECRET` | HMAC signing key for access tokens - **must** be a real random secret outside local dev |
| `JWT_COOKIE_SECURE` | Set to `false` only for plain-HTTP local dev |
| `CORS_ALLOWED_ORIGINS` | Comma-separated allow-list, no wildcard |
| `PUBLIC_SITE_BASE_URL` | Used to build links (e.g. the password reset link logged by `LoggingNotificationMailer`) |
| `UPLOAD_MAX_FILE_SIZE` | Container-level multipart size cap (default `10MB`) |
| `UPLOAD_MAX_PDF_SIZE_BYTES` | Service-level PDF size cap in bytes (default `10485760`) - keep in sync with `UPLOAD_MAX_FILE_SIZE` |
| `RESUME_TRASH_RETENTION` | How long a soft-deleted resume can be restored (default `30d`) |
| `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`, `MINIO_BUCKET` | Object storage connection (defaults match `docker-compose.yml`'s `minio` service) |
| `ANALYTICS_VIEW_DEDUP_WINDOW` | Repeated views from the same visitor within this window count as one page view (default `30m`) |
| `RATE_LIMIT_ENABLED` | Master on/off switch for rate limiting (default `true`; disabled in the test profile) |
| `RATE_LIMIT_AUTH_CAPACITY`, `RATE_LIMIT_AUTH_WINDOW` | Login/register/forgot-password limit (default `10` per `1m`) |
| `RATE_LIMIT_PUBLIC_CAPACITY`, `RATE_LIMIT_PUBLIC_WINDOW` | Public resume/view/file endpoints limit (default `60` per `1m`) |

Never commit a real `.env`. It's already covered by `.gitignore` at the
monorepo root.

## MinIO bucket setup

The backend creates its bucket (`MINIO_BUCKET`, default `cv-platform-local`)
automatically on startup if it doesn't exist yet (`MinioStorageConfig`) - no
manual step needed for local dev. To inspect stored files or create the
bucket by hand instead:

1. Open the console at http://localhost:9013 and log in with
   `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD` from your `.env`.
2. Keep the bucket's access policy **private** - the app proxies file
   access through the backend (`GET /api/v1/resumes/{id}/preview/file`),
   never exposing a public bucket URL (see [docs/security.md](docs/security.md)).
3. Or via the `mc` CLI: `mc alias set local http://localhost:9012 <user> <password> && mc mb local/cv-platform-local`.

## Tests

### Backend

```bash
cd backend
./mvnw test
```

- Unit tests (`AuthServiceTest`, `JwtServiceTest`, `ResumeServiceTest`,
  `PdfFileValidatorTest`, `AnalyticsServiceTest`, `PublicResumeServiceTest`,
  `ResumeSectionServiceTest`, `SectionContentValidatorTest`,
  `StructuredContentMaskerTest`, `StructuredSnapshotBuilderTest`,
  `RateLimiterTest`) run everywhere, no Docker required.
  `PublicResumeServiceTest` covers all the public-link gating rules (404
  vs. 410, wrong unlisted token, download policy, owner-view exclusion);
  `StructuredSnapshotBuilderTest` and `StructuredContentMaskerTest` cover
  the section-visibility and contact-field-masking rules;
  `ResumeSectionServiceTest` also covers cross-owner authorization
  (listing/creating/deleting a section on another user's resume all 404);
  `RateLimiterTest` covers the token-bucket behavior in isolation, without
  a Spring context - all at the Mockito/pure-unit level.
- `AuthControllerIT`, `ResumeControllerIT`, `PublicResumeControllerIT`,
  `ResumeSectionControllerIT`, and `CvPlatformBackendApplicationTests` use
  Testcontainers (real PostgreSQL +, for the resume/sharing ITs, a real
  MinIO container) and need a working
  Docker Engine API. **Known caveat**: in the sandbox this project was
  built in, Docker Desktop's named-pipe API rejected Testcontainers'
  client with an HTTP 400 even though the `docker` CLI itself worked fine
  against the same pipe - see
  [docs/security.md](docs/security.md#known-limitation-in-this-environment).
  If `./mvnw test` fails only on those classes with a
  "Could not find a valid Docker environment" error, it's this
  environment-specific issue, not a code defect; every flow they cover has
  been run and verified by hand against the real containers via
  `docker compose` (see the Quick Start / upload-flow / publish-flow
  sections above), and they should pass as-is on a standard CI runner or
  dev machine.

### Frontend

```bash
cd frontend
npm test          # vitest run - component/unit tests, no browser
npm run build      # type-checks (vue-tsc) + production build
npm run test:e2e   # Playwright, real Chromium - needs docker compose up first, see above
```

## Production build

- **Backend**: `backend/Dockerfile` is a multi-stage build producing a
  runnable jar image. Build with
  `docker build -t cv-platform-backend ./backend` and run with real
  secrets injected via environment variables (never bake `JWT_SECRET` or
  DB credentials into the image).
- **Frontend**: `frontend/Dockerfile` builds the static assets and serves
  them via nginx (`frontend/nginx.conf` has the SPA fallback route needed
  for client-side routing). Build with
  `docker build -t cv-platform-frontend --build-arg VITE_API_BASE_URL=https://api.example.com ./frontend`.
- `docker-compose.yml` at the repo root is for **local development only**
  (it runs the frontend via the Vite dev server, not the production
  image) - see [docs/architecture.md](docs/architecture.md#local-infrastructure).

### Secrets

- `JWT_SECRET`, `DB_PASSWORD`, `MINIO_ROOT_PASSWORD`/`MINIO_SECRET_KEY` must
  all be freshly generated, real random values outside local dev - the
  `.env.example` defaults are for Docker Compose on localhost only and are
  not safe anywhere reachable from the internet.
- Inject secrets via your platform's secret store (e.g. environment
  variables from a secrets manager, Docker/Kubernetes secrets) - never
  commit a real `.env`, and never bake a secret into a built image layer.
- Rotating `JWT_SECRET` invalidates every access token in circulation
  immediately (refresh tokens are unaffected, since they're validated
  against the DB, not the JWT signature) - plan for a brief re-login wave
  if you ever need to rotate it.

### HTTPS / reverse proxy

- Neither `backend/Dockerfile` nor `frontend/Dockerfile` terminate TLS -
  put a reverse proxy (nginx, Caddy, or your cloud LB) in front of both
  and terminate HTTPS there.
- Set `JWT_COOKIE_SECURE=true` (the non-`local`-profile default) once
  running behind HTTPS, so the refresh-token cookie is only ever sent over
  an encrypted connection.
- Route the frontend's `VITE_API_BASE_URL` and the backend's
  `CORS_ALLOWED_ORIGINS` to the real public hostnames - not `localhost` -
  and keep `CORS_ALLOWED_ORIGINS` an exact allow-list (no wildcard), since
  `allowCredentials(true)` is required for the refresh cookie to work.

### Backups

- The only stateful services are `postgres` (all relational data) and
  `minio` (uploaded PDFs, keyed as `resumes/{ownerId}/{uuid}.pdf` -
  content-addressed by random key, not by anything derivable from the DB
  row alone). Back up both; a Postgres-only backup loses every uploaded
  PDF's bytes even though the DB rows referencing them survive.
- Flyway migrations (`backend/src/main/resources/db/migration`) are
  forward-only and already applied automatically on backend startup -
  don't hand-edit a past migration; add a new one instead, same as any
  other environment.

### Pre-deploy environment checklist

- [ ] `JWT_SECRET` is a fresh random value, not the `.env.example` default
- [ ] `JWT_COOKIE_SECURE=true`
- [ ] `CORS_ALLOWED_ORIGINS` lists only real production origin(s)
- [ ] `DB_PASSWORD`, `MINIO_ROOT_PASSWORD`/`MINIO_SECRET_KEY` are fresh,
      not defaults
- [ ] TLS terminates in front of both `frontend` and `backend`
- [ ] `PUBLIC_SITE_BASE_URL` points at the real public hostname (used to
      build links such as the password-reset link)
- [ ] Postgres and MinIO have a backup/restore plan in place
- [ ] Rate-limit defaults (`RATE_LIMIT_*`, see
      [docs/architecture.md](docs/architecture.md#rate-limiting-phase-5))
      reviewed for expected real-world traffic, not just local testing

## Documentation

- [docs/architecture.md](docs/architecture.md) - module layout, auth
  design, public-URL and content-storage decisions
- [docs/security.md](docs/security.md) - security checklist, what's done
  vs. planned per phase
- [docs/api.md](docs/api.md) - endpoint reference (implemented + planned)
- [docs/roadmap.md](docs/roadmap.md) - phase plan and explicit
  out-of-scope list
