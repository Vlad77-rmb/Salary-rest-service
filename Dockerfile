# Установка зависимостей
FROM python:3.9-slim as builder

# Установка системных зависимостей для компиляции
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копирование файлов зависимостей
COPY pyproject.toml poetry.lock ./

# Установка poetry
RUN pip install --no-cache-dir poetry==1.8.2

# Установка зависимости (создаем .venv)
RUN poetry config virtualenvs.in-project true && \
    poetry install --without dev --no-root --no-interaction --no-ansi

# Финальный образ
FROM python:3.9-slim

# Установка runtime-зависимостей для bcrypt
RUN apt-get update && apt-get install -y \
    libffi8 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копирование виртуального окружение из builder-этапа
COPY --from=builder /app/.venv /app/.venv

# Добавление .venv в PATH
ENV PATH="/app/.venv/bin:$PATH"

# Копируем исходный код
COPY . .

# Проверяем установку bcrypt
RUN python -c "import bcrypt; print(f'bcrypt version: {bcrypt.__version__}')"

CMD ["uvicorn", "salary_service.main:app", "--host", "0.0.0.0", "--port", "8000"]