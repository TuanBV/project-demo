# Architecture Map

## Runtime components
- `frontend/`: Vue 3 SPA, Vite, Pinia, Vue Router, AJV validation, Tailwind.
- `api/`: FastAPI HTTP API with dependency injection and SQLAlchemy repositories.
- `mysql`: transactional persistence.
- `redis`: Celery broker/result backend.
- `worker/`: Celery worker and beat schedule.
- `storage/` and `queue/`: experimental services; either integrate with documented contracts or remove from the production compose profile.

## Intended request flow
Vue component → domain service → REST repository/client → FastAPI router → service → repository → SQLAlchemy/MySQL.

## Boundary rules
- Routers do not contain SQL queries.
- Repositories do not construct HTTP responses.
- Services own business invariants and transactions.
- Frontend components do not build raw API URLs.
- Stores do not silently swallow API failures.
- External integrations are adapters behind interfaces and are disabled by default in local development.
