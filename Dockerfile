# Use an official Python runtime as a parent image
FROM python:3.10-slim   

# Set the working directory in the container
WORKDIR /app

# Install system packages required for building psycopg2 and other deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Default runtime configuration (override via --build-arg or docker run -e)
ARG POSTGRES_USER=lodyne
ARG POSTGRES_PASSWORD
ARG POSTGRES_HOST=localhost
ARG POSTGRES_PORT=5432
ARG POSTGRES_DB=expense_tracker
ARG POSTGRES_SERVICE_HOST=postgres

ENV PYTHONUNBUFFERED=1 \
    POSTGRES_USER=${POSTGRES_USER} \
    POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
    POSTGRES_HOST=${POSTGRES_HOST} \
    POSTGRES_PORT=${POSTGRES_PORT} \
    POSTGRES_DB=${POSTGRES_DB} \
    POSTGRES_SERVICE_HOST=${POSTGRES_SERVICE_HOST} \
    DOCKERIZED=1

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
