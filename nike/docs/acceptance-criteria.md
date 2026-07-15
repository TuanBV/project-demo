# MVP Acceptance Criteria

## Security
- No plaintext credential or private token is tracked.
- Public requests cannot create/administer admin accounts.
- Every admin mutation returns 401/403 when unauthenticated/unauthorized.
- File uploads validate MIME type, extension, decoded size, destination path, and filename collision.

## Authentication
- User and admin can sign in with distinct role checks.
- Session survives navigation and expires correctly.
- Logout removes the cookie.
- Change-password and reset-password flows invalidate old credentials/tokens.

## Catalog
- Public product list/detail, category, kind, active sale, and published post endpoints work.
- Admin CRUD supports validation, soft delete/reactivation, pagination, search, and deterministic ordering.

## Commerce
- Cart is persisted server-side and tied to the authenticated user.
- Quantity cannot exceed available stock or drop below one.
- Checkout is transactional and idempotent.
- Order totals are calculated on the server from trusted product data.
- Users only see their own orders; admins can see and update all orders.

## Quality
- Frontend production build passes.
- Frontend lint has zero errors and no uncontrolled warning flood.
- Backend compile/import checks pass.
- Critical backend and frontend tests pass.
- Docker Compose configuration validates from a clean checkout.
- README contains setup, environment, run, test, demo-data, troubleshooting, and security sections.
