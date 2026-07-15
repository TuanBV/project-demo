# API Contract Gap Checklist

## Existing frontend calls missing backend routes
- [ ] `GET /user/{user_id}`
- [ ] `PUT /user/{user_id}`
- [ ] `DELETE /user/{user_id}` or documented soft-deactivate equivalent
- [ ] `PUT /user/password`
- [ ] `POST /user/forgot-password`
- [ ] `GET /user/forgot-password/{token}`
- [ ] `PUT /user/reset-password/{token}`
- [ ] `PUT /post/{post_id}`
- [ ] `PUT /post/{post_id}/active`

## Missing domain contracts
- [ ] Cart CRUD and totals
- [ ] Checkout/idempotency
- [ ] User order history
- [ ] Admin order search/detail/status
- [ ] Slide/banner CRUD or removal from UI
- [ ] Comment APIs or removal from MVP

## Contract rules
- Request and response schemas are explicit and versioned.
- HTTP status codes represent transport outcomes; domain error codes may supplement them.
- Pagination uses one shared shape.
- Date/time values use ISO 8601 and a documented timezone policy.
- Money uses decimal/fixed precision, not binary float.
