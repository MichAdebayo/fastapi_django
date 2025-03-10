# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies for Azure SQL, ODBC drivers, and wget
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    apt-transport-https \
    software-properties-common \
    curl \
    gnupg2 \
    build-essential \
    unixodbc-dev \
    libcurl4 \
    libssl3 && \
    apt-get remove --purge -y libodbc* libodbccr* unixodbc* && \
    apt-get autoremove -y

# Copy and run the script to install SQL Server drivers
COPY install_sql_driver.sh install_sql_driver.sh
RUN chmod +x ./install_sql_driver.sh && ./install_sql_driver.sh

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Download wait-for-it.sh and make it executable (before switching to appuser)
RUN wget -O /wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x /wait-for-it.sh

# Create the staticfiles directory and set correct ownership/permissions
RUN mkdir -p /app/staticfiles && \
    chmod -R 777 /app/staticfiles && \
    chown -R 10001:10001 /app/staticfiles  # Ensures appuser can write

# Switch to the non-privileged user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Set ownership for all necessary directories
RUN chown -R appuser:appuser /app

# Copy the source code AFTER setting permissions
COPY . .

# Ensure static files are collected before switching users
RUN python manage.py collectstatic --noinput || { echo "❌ Collectstatic failed"; exit 1; }

# Set executable permissions for start.sh
RUN chmod +x /app/start.sh && chown appuser:appuser /app/start.sh

# Switch to non-root user AFTER setting permissions
USER appuser

# Expose the application port
EXPOSE 8000

# Run the start script
CMD ["/app/start.sh"]