#!/bin/bash
# UniCore Provisioning Script
# Creates a new isolated institution instance

set -e

echo "=== UniCore Instance Provisioning ==="
echo ""

# Configuration
read -p "Institution Slug (e.g., unilag): " SLUG
read -p "Domain (e.g., unilag.edu.ng): " DOMAIN
read -p "Admin Email: " ADMIN_EMAIL
read -p "Admin Password (leave empty to generate): " ADMIN_PASSWORD

SLUG=${SLUG:-$(echo $DOMAIN | cut -d. -f1)}
INSTANCE_DIR="/var/unicore/instances/${SLUG}"
DB_NAME="unicore_${SLUG}"

# Generate password if not provided
if [ -z "$ADMIN_PASSWORD" ]; then
  ADMIN_PASSWORD=$(openssl rand -base64 12)
  echo "Generated password: $ADMIN_PASSWORD"
fi

# Generate secrets
DB_PASSWORD=$(openssl rand -base64 16)
DJANGO_SECRET=$(openssl rand -base64 32)

echo ""
echo "Creating instance at $INSTANCE_DIR..."

# Create directory
mkdir -p "$INSTANCE_DIR"

# Create .env file
cat > "$INSTANCE_DIR/.env" << EOF
SECRET_KEY=${DJANGO_SECRET}
DEBUG=False
ALLOWED_HOSTS=${DOMAIN},localhost

DB_NAME=${DB_NAME}
DB_USER=postgres
DB_PASSWORD=${DB_PASSWORD}
DB_HOST=localhost
DB_PORT=5432

REDIS_HOST=localhost
REDIS_PORT=6379

CORS_ORIGINS=https://${DOMAIN}
AWS_S3_KEY=
AWS_S3_SECRET=
S3_BUCKET=unicore-${SLUG}

PAYSTACK_SECRET_KEY=
FLUTTERWAVE_SECRET_KEY=

 EMAIL_USER=
EMAIL_PASSWORD=
EOF

# Create docker-compose.yml
cat > "$INSTANCE_DIR/docker-compose.yml" << EOF
version: '3.8'

services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELLELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

  web:
    build: ../backend
    command: gunicorn unicore.wsgi --bind 0.0.0.0:8000
    environment:
      - DJANGO_SETTINGS_MODULE=unicore.settings
    env_file:
      - .env
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - static_volume:/app/static:ro
      - media_volume:/app/media:ro
    depends_on:
      - web

volumes:
  db_data:
  redis_data:
  static_volume:
  media_volume:
EOF

echo ""
echo "Instance created! Next steps:"
echo "1. Create database: createdb -h localhost -U postgres $DB_NAME"
echo "2. Run: cd $INSTANCE_DIR && docker compose up -d"
echo "3. Create admin: docker exec web python manage.py createsuperuser --email $ADMIN_EMAIL"
echo ""
echo "Login URL: https://${DOMAIN}/admin"