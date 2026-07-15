.PHONY: install run migrate seed test lint format typecheck check docker-up docker-down

install:
	pip install -e ".[dev]"

run:
	uvicorn app.main:app --reload

migrate:
	alembic upgrade head

seed:
	python scripts/seed.py

test:
	pytest --cov=app --cov-report=term-missing

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy app

check: format lint typecheck test

docker-up:
	docker compose up --build

docker-down:
	docker compose down
