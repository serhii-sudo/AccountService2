# Use the official Python image as the base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app

# Collecting staticfiles
RUN cd app && python manage.py collectstatic --noinput || true

# Expose the port that Gunicorn will run on
EXPOSE 8000

# Run Gunicorn to serve the Django app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--chdir", "app", "app.wsgi:application"]
