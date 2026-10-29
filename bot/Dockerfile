# ============================================
# Stage 1: Builder
# ============================================
FROM python:3.13.7-slim-bookworm AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.10.8 /uv /uvx /bin/

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=0 \
    UV_PROJECT_ENVIRONMENT=/opt/venv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


# ============================================
# Stage 2: Runtime
# ============================================
FROM python:3.13.7-slim-bookworm

# Runtime-зависимости:
# ca-certificates — для HTTPS
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 botuser

WORKDIR /app

# venv из builder-стадии
COPY --from=builder /opt/venv /opt/venv

# Код
COPY --chown=botuser:botuser . .

RUN mkdir -p /app/logs && chown -R botuser:botuser /app

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1

USER botuser

EXPOSE 8080

CMD ["python", "-m", "app.aiogram_run"]