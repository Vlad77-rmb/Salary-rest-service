# Salary Service

- Python 3.9+
- Docker

## Установка

1. Клонируйте репозиторий:

git clone ... .git
cd Salary


2. Установите зависимости:

poetry install


3. Настройте окружение:

cp .env.example .env

4. Запустите сервер:

poetry run uvicorn app.main:app --reload

# Docker-развертывание

docker-compose up --build

# API Endpoints
- `POST /token` - Получение JWT токена
- `GET /salary` - Получение зарплаты (требует токен)

# Тестирование
poetry run pytest