# syntax=docker/dockerfile:1

FROM python:3.12-slim

# Не создавать .pyc-файлы и буферизацию
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Установка системных зависимостей (для psycopg2, компиляции и ожидания БД)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Установка Python-зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Открываем порт для сервера Django
EXPOSE 8000

# Команда по умолчанию — миграции и запуск сервера
CMD sh -c "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"
