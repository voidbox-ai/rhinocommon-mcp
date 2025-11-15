# Multi-stage build for scraper and server

FROM python:3.11-slim as base

WORKDIR /app

# Install common dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project structure
COPY . .

# ============================================
# Scraper stage
# ============================================
FROM base as scraper

WORKDIR /app/scraper

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "scraper.py"]

# ============================================
# Server stage
# ============================================
FROM base as server

WORKDIR /app/server

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "mcp_server.py"]