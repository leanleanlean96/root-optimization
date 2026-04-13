# ========== STAGE 1: Builder ==========
FROM python:3.13-slim AS builder

WORKDIR /app

# Системные зависимости для сборки
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    gdal-bin \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем Poetry и production-зависимости
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root --only main

# ========== STAGE 2: Final ==========
FROM python:3.13-slim

# Runtime-зависимости (без gcc)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gdal-bin \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем установленные пакеты из builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Копируем код приложения
COPY app/ ./app/

ENV PYTHONPATH=/app

# Команда по умолчанию (в docker-compose переопределяется)