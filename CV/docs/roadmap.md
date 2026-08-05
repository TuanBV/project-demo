# Roadmap

## Phases

| Phase | Scope | Status |
|---|---|---|
| 0 - Discovery | Repo analysis, architecture, ERD, API contract, risk list | ✅ Done |
| 1 - Foundation | Project structure, Postgres migration, auth, global error handling, OpenAPI, Docker Compose, test foundation | ✅ Done |
| 2 - Resume & PDF | Resume CRUD, storage abstraction, MinIO, PDF upload, versioning, private preview | ✅ Done |
| 3 - Publish & public link | Visibility, publish/unpublish, public endpoint, PDF viewer, download policy, QR code, view tracking | ✅ Done |
| 4 - Structured CV | Section CRUD, editor, preview, responsive public template, print stylesheet | ✅ Done |
| 5 - Hardening | Authorization tests, rate limiting, security headers, file security, E2E, logging/metrics, production docs | ✅ Done |

A phase doesn't start until the previous one builds and tests green - see
each phase's summary in the PR/commit history for what actually shipped
vs. what moved to the next phase.

## Concrete follow-ups already identified while building Phase 1

- **Rate limiting** (login, register, forgot-password) - shipped in Phase 5
  per the "don't add Redis until needed" guidance; Bucket4j in-memory is
  enough at MVP scale, revisit only if the app needs to scale horizontally
  (see the Phase 5 follow-ups below).
- **Testcontainers IT execution in this dev sandbox** - blocked by a local
  Docker Desktop named-pipe API quirk (documented in
  [security.md](security.md#known-limitation-in-this-environment)). Not a
  code issue; re-run `./mvnw test` in CI or a normal dev machine.
- **Version-activation race condition** (two concurrent "activate version"
  or "upload" requests) - resolved in Phase 2 via `Resume.version`
  optimistic locking (concurrent writers get `409 CONCURRENT_MODIFICATION`)
  plus a `DataIntegrityViolationException` handler for the rarer case of two
  concurrent uploads racing on the `(resume_id, version_number)` unique
  constraint.
- **Duplicate() and file bytes**: duplicating a PDF resume does not re-upload
  or re-store file bytes - the new resume's version 1 points at the same
  `stored_files` row as the source's active version. Correct today because
  files are immutable once stored; would need revisiting if per-owner file
  encryption or storage-key-derived access control is added later.
- **Caught via manual end-to-end verification, not by a unit test**: mapping
  `resume_versions.snapshot_json` (a `jsonb` column) as a plain `String`
  field broke *every* version insert - including ones that leave it `NULL` -
  because PostgreSQL's JDBC driver binds a `String`-typed parameter as
  `varchar`, and Postgres refuses that against a `jsonb` column even for
  `NULL`. Fixed with `@JdbcTypeCode(SqlTypes.JSON)` on the field. This only
  surfaced when uploading a real PDF through the full Docker Compose stack
  (Mockito-based `ResumeServiceTest` mocks the repository, so it never
  touches real SQL) - a good reminder that mocked-repository tests can't
  catch schema/ORM mapping mismatches; only an integration test against a
  real database can.
- **OG/link-preview metadata for Facebook/LinkedIn/Zalo** (Phase 3 product
  brief item) - only partially done. `PublicResumePage.vue` sets
  `document.title` client-side, which helps JS-executing crawlers but not
  the non-JS link-unfurling bots most of those platforms actually use.
  Properly closing this gap needs SSR/prerendering (or a bot-user-agent
  server-rendered fallback) for the `/cv/:publicId/:slug` route - real
  infrastructure work, not a Phase 3-sized task. See
  [architecture.md](architecture.md#known-gap-oglink-preview-metadata-needs-server-side-rendering).
  Candidate for its own follow-up phase once Phase 4/5 land.
- **Public page content was intentionally thin in Phase 3** (no headline,
  bio, skills, or experience) because structured sections didn't exist
  yet. Phase 4 closes most of that gap for `STRUCTURED` resumes (headline,
  summary, skills, experience, education, etc. all now render on the
  public page). One piece is still missing: **no avatar** - the `profile`
  module (which already has a `user_profiles.avatar_storage_key` column
  sitting unused since Phase 1) still hasn't been built, and avatar upload
  needs its own image-file validation path (distinct from the PDF
  validator). Tracked here rather than partially implemented now.
- **Phase 4 field-config pattern is a genuine simplification, not a
  shortcut**: adding an 11th section type is one config entry
  (`sectionFields.ts`) + one backend content record + one render branch in
  `StructuredResumeView.vue` - not a new form component. Revisit only if a
  future section type needs interaction the generic object/list forms
  can't express (e.g. nested repeatable groups, file attachments within a
  section).

## Concrete follow-ups identified while building Phase 5

- **`RateLimiter`'s bucket map is unbounded** (`ConcurrentHashMap<String,
  Bucket>`, one entry per distinct IP+category ever seen) - fine at MVP
  traffic and a single-instance deployment, but a long-lived process
  facing many distinct IPs would grow this map forever. Revisit with a
  bounded/evicting cache (e.g. Caffeine with a TTL) only if that actually
  becomes a memory concern in production - not a problem at current scale.
- **Rate limits are per-process, not shared** - correct for today's single
  backend instance; if the backend is ever scaled to multiple instances
  behind a load balancer, each instance would enforce its own limit
  independently (effectively multiplying the real limit by instance
  count). Would need a shared store (Redis) at that point, not before.
- **No audit trail yet** for publish/unpublish/regenerate-link/delete
  actions (see [security.md](security.md#auditing-phase-5)) - deferred
  since there's no admin/support surface that would consume it yet.
- **CSP for public pages** still needs to be added at the frontend/nginx
  layer, not this backend - see
  [architecture.md](architecture.md#security-headers-phase-5). Not started;
  candidate for whoever picks up the production nginx config.
- **E2E coverage is one flow, not a suite** - `main-flow.spec.ts` covers the
  single most important path (register → PDF upload → publish → anonymous
  view) end-to-end in a real browser. It does not cover the structured-CV
  flow, unlisted links, download-policy toggling, or rollback - those
  remain covered at the unit/manual-verification level only. Worth
  expanding if regressions in those areas start showing up.

## Explicitly out of scope for the initial product

Recorded so it doesn't get accidentally re-scoped into an early phase:

- Job marketplace / recruiter accounts / job applications
- Payment or subscription billing
- AI resume scoring or AI PDF→structured-CV parsing
- Custom domains for public CVs
- Real-time multi-user co-editing of a resume
- Comments/reviews on a CV
- Advanced email analytics
- Full-text search across public CVs
- Native mobile app

## Also deferred (mentioned in the product brief, not MVP)

- CV password protection, link expiry dates
- Additional resume templates
- AI-assisted review/suggestions
- Rich text formatting in section text fields (summary, descriptions) -
  currently plain text only; see
  [architecture.md](architecture.md#known-limitation-no-rich-text-only-plain-text)
  for why this was the deliberate Phase 4 choice, and what adding it later
  would require (mandatory server-side HTML sanitization).
- Avatar upload for the `profile` module (see the Phase 4 follow-up above).
