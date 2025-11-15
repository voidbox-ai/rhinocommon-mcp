# Multi-stage build for scraper and server

FROM python:3.11-slim as base

WORKDIR /app

# Install common dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ============================================
# Scraper stage
# ============================================
FROM base as scraper

WORKDIR /app

# Copy scraper files and install dependencies
COPY scraper/requirements.txt ./scraper/
RUN pip install --no-cache-dir -r scraper/requirements.txt

# Copy all scraper files
COPY scraper/ ./scraper/

# Create docs directory
RUN mkdir -p /app/docs

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app/scraper

CMD ["/bin/bash"]

# ============================================
# Server stage
# ============================================
FROM base as server

WORKDIR /app

# Copy server files and install dependencies
COPY server/requirements.txt ./server/
RUN pip install --no-cache-dir -r server/requirements.txt

# Copy all server files
COPY server/ ./server/

# Create docs directory
RUN mkdir -p /app/docs

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app/server

CMD ["/bin/bash"]