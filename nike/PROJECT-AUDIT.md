# Project Audit — Nike E-commerce

Audit date: 2026-07-15

## Executive assessment
The repository is a partially implemented learning/demo e-commerce application. Product/category/kind/sale/post/image/settings CRUD has a recognizable layered structure, but the project is not yet a runnable or secure MVP. The highest risks are committed credentials, broken authentication/cookie behavior, missing API contracts, a failing frontend build, little meaningful test coverage, and placeholder admin/user screens.

## Verified baseline
- Stack: Vue 3, Vite, Pinia, AJV, Tailwind; FastAPI, SQLAlchemy, MySQL, Redis, Celery; Docker Compose.
- Backend exposes 42 routes.
- `python -m compileall -q api worker queue storage`: passes.
- Backend tests: none found.
- Frontend install audit: 36 vulnerabilities total (4 critical); production dependency audit: 15 total (2 critical).
- Frontend build: fails on missing `src/components/admin/modal/RichTextCustom.vue`.
- Frontend tests: 3 files pass, 1 suite fails; 6 tests pass, but `NavBar.test.js` imports a nonexistent component path.
- Frontend lint: 15 errors and 12,419 warnings; most warnings are CRLF/Prettier noise, while the errors are unused variables and invalid props.

## P0 — security and run blockers
1. Real credentials were committed in `api/.env`, `api/env.example`, and note files. Rotate the Gmail app password, Facebook tokens, JWT secret, and database password. Purge them from Git history before publishing.
2. `UserRequest.role` lets public registration submit an admin role. Public registration must always create a normal user; admin user creation must be a separate protected endpoint.
3. `/user/all` and `/user/{user_id}/{status}` lack authentication and admin authorization.
4. `make_cookie()` always sets `secure=True`, ignoring the environment-aware cookie setting. On plain HTTP localhost, authentication cookies may not work.
5. CORS origins, API base URL, database host, and credentials are hard-coded.
6. `api/main.py` registers `post_router` twice.
7. Frontend cannot build due to a case/name mismatch: `RichTextCustom.vue` vs `RichTextCusTom.vue`.
8. The project has no health endpoint or reliable startup verification.

## P0 — data correctness defects
1. SQLAlchemy `CartProduct.cart_id` is `Integer`, while `Cart.cart_id` and SQL schema use `VARCHAR(20)`.
2. `Image.folder` is non-null in the model, but `ImageRepository.add()` does not set it.
3. Product joins use inconsistent keys around `product_kind_id`, `ProductKind.id`, and `ProductKind.kind_id`; verify every query against the schema.
4. Docker Compose passes `MYSQL_DATABASE`/`MYSQL_HOST`, while application settings expect `MYSQL_DB`, `MYSQL_HOST_WRITE`, and `MYSQL_HOST_READ`; the database class then ignores those hosts and hard-codes `database:3306`.
5. The SQLAlchemy URL uses `pymysql`, but it is installed ad hoc in the Dockerfile rather than declared and pinned in `requirements.txt`.
6. Error handling often converts domain errors to HTTP 200 and may reference local variables in `finally` before assignment.

## P1 — API contract gaps
The frontend user repository calls endpoints that do not exist in the backend:
- `GET /user/{user_id}`
- `PUT /user/{user_id}`
- `DELETE /user/{user_id}`
- `PUT /user/password`
- `POST /user/forgot-password`
- `GET /user/forgot-password/{token}`
- `PUT /user/reset-password/{token}`

The frontend post repository also calls missing update/activate routes:
- `PUT /post/{post_id}`
- `PUT /post/{post_id}/active`

There are UI routes or models without complete backend features:
- cart persistence and quantity management;
- checkout and orders;
- profile update/address management;
- slide/banner management;
- comments/blog interactions;
- admin email/chat/social publishing integrations.

## P1 — frontend quality gaps
- `frontend/src/views/admin/order/OrderView.vue` and slide screens reuse product/category placeholder logic and do not implement their named domains.
- Profile links are inert (`href="#"`).
- Several service methods return `null` on errors, swallowing useful error state.
- Router guards call `/user/me` on every navigation and mix admin-role decisions with truthiness rather than explicit role checks.
- API base URL is hard-coded to localhost.
- Playground tests outweigh real feature tests.
- `fe-quasar/` appears to be a second scaffold and should be explicitly removed, archived, or adopted; do not maintain two frontends accidentally.

## P2 — maintainability and delivery gaps
- Dependencies are mostly unpinned on the Python side.
- No Alembic migrations.
- No CI pipeline.
- No end-to-end or backend integration tests.
- README only contains destructive Docker commands and lacks setup, architecture, credentials, demo accounts, troubleshooting, and test instructions.
- Logging code exists but request/response logging is commented out.
- No pagination/filter/sort contract standardization.
- No accessibility or responsive acceptance tests.

## Recommended completion order
1. Rotate/purge secrets and make configuration reproducible.
2. Fix build, lint baseline, unit test imports, Docker config, health checks, and authentication cookies.
3. Lock down authorization and repair model/schema/repository defects.
4. Reconcile API contracts for user/profile and post.
5. Implement cart → checkout → order as one vertical slice.
6. Finish admin product/image/sale/post/settings workflows.
7. Decide and implement or remove slide/chat/email/social placeholders.
8. Add migrations, backend tests, frontend component tests, one e2e critical path, CI, and operational documentation.
