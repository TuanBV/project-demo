# Completion Roadmap

## Milestone 0 — secure, reproducible baseline
- Rotate and purge secrets.
- Normalize environment variables and Docker Compose.
- Add `/health/live` and `/health/ready`.
- Fix frontend build and test import blockers.
- Isolate CRLF formatting into one mechanical commit.
- Pin/upgrade dependencies after reviewing breaking changes.

Exit: clean install works, compose config validates, frontend builds, Python imports compile, and no known credential is tracked.

## Milestone 1 — authentication and authorization
- Public registration always creates `ROLE.USER`.
- Protect all admin routes with `authorized_user` plus explicit admin permission.
- Correct cookie settings for local HTTP and production HTTPS.
- Implement user detail/update/deactivate and password change/reset contracts.
- Add unique email constraint, password policy, token expiry/revocation strategy, and rate limiting plan.

Exit: user/admin login, logout, session restore, profile update, and password flows pass integration tests.

## Milestone 2 — catalog and content
- Repair product/product-kind/image relationships and queries.
- Complete admin CRUD for category, kind, product, image, sale, post, setting.
- Add pagination, filtering, sorting, validation, and consistent response/error semantics.
- Implement missing post update/reactivation.

Exit: admin can manage content and users can browse/filter/view product details.

## Milestone 3 — commerce vertical slice
- Persist carts per user.
- Add/update/remove cart lines with stock checks.
- Create order, order items, totals, status history, shipping data, and idempotent checkout.
- Decrement/reserve stock transactionally.
- Implement user order history and admin order management.

Exit: sign in → add product → update cart → checkout → see order → admin updates status.

## Milestone 4 — optional product features
For slide/banner, comments, chat, email, and social publishing, choose one of two explicit outcomes per feature: implement a tested vertical slice, or remove the route/menu/component and document it as out of MVP scope. Do not leave deceptive placeholder screens.

## Milestone 5 — delivery
- Alembic migrations and seed strategy.
- Backend unit/integration tests and frontend component tests.
- One browser e2e critical path.
- CI for secret scan, lint, tests, build, and Docker config.
- README, API docs, deployment notes, backup/restore, and observability.
