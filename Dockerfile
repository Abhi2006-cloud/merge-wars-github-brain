# Multi-stage lightweight Dockerfile for GitHub AI Brain
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies first for build caching
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

# Copy dependencies from builder stage
COPY --from=builder /install /usr/local

# Copy application source code
COPY . .

# Run as non-root unprivileged user for container security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Default command launches interactive CLI mode
ENTRYPOINT ["python3", "main.py"]
