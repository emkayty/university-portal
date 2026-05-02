# Build stage
FROM python:3.12-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -t /wheels

# Final stage
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /wheels /app
COPY . /app

RUN pip install --no-cache-dir gunicorn

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=unicore.settings

EXPOSE 8000

CMD ["gunicorn", "unicore.wsgi", "--bind", "0.0.0.0:8000"]