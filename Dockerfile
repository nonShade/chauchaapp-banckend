# Dockerfile for chauchaapp-backend
# Multi-stage build for development and production

# Base stage for common dependencies
FROM python:3.12-slim AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install uv and dependencies
RUN pip install --no-cache-dir uv && \
    uv pip install --system --no-cache-dir -r pyproject.toml

# Copy application code
COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app
USER appuser

# Development stage
FROM base AS development
# Install development dependencies
USER root
RUN uv pip install --system --no-cache-dir pytest pytest-asyncio pytest-cov
USER appuser

# Set development-specific environment variables
ENV DEBUG=true \
    RELOAD=true

# Expose port
EXPOSE 8000

# Command for development (hot reload)
# Using reflex run for development with hot reload
CMD ["reflex", "run", "--backend-host", "0.0.0.0", "--backend-port", "8000"]

# Production stage
FROM base AS production
# Copy only necessary files from base stage
COPY --from=base /app /app

# Set production environment variables
ENV DEBUG=false \
    RELOAD=false

# Expose port
EXPOSE 8000

# Command for production
# Using reflex prod for production build and serve
CMD ["reflex", "prod", "--backend-host", "0.0.0.0", "--backend-port", "8000"]