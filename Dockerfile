# Use official Python image
FROM python:3.12-slim

# Environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install PostgreSQL client for pg_isready
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Set working directory to the root of the Django project
WORKDIR /app/app

# copy in app
COPY requirements.txt /app/app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Copy project files
COPY . .

# Expose port that Gunicorn will serve
EXPOSE 8000

# Default command: wait for DB, migrate, collectstatic, run Gunicorn
CMD ["sh", "-c", "\
until pg_isready -h $DB_HOST -p 5432; do echo waiting for db; sleep 2; done && \
echo 'DB is ready' && \
python manage.py migrate && \
echo 'MIGRATIONS DONE' && \
python manage.py collectstatic --noinput && \
echo 'STATIC DONE' && \
echo 'RUN ONLY AT ADDRESS WITHOUT PORT NOW DJANGO MODE - DEVELOPMENT!' && \
echo 'RUN ONLY http://127.0.0.1/login/' && \
gunicorn app.wsgi:application --bind 0.0.0.0:8000 \
"]