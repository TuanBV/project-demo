FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY pyproject.toml ./
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./
COPY scripts ./scripts

RUN pip install --no-cache-dir . && mkdir -p /app/data

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && python scripts/seed_java_python_mc.py && python scripts/seed_extended_topics.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
