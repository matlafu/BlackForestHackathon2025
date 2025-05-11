FROM python:3.11-slim

LABEL maintainer="UnQuack Team"
LABEL description="BalkonSolar - Optimizing Small-Scale Storage and Plug-In Solar"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt ./
COPY balkonsolar/requirements.txt ./balkonsolar/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install -r balkonsolar/requirements.txt && \
    pip install appdaemon

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/data /app/logs

# Create volume mount points
VOLUME ["/app/data", "/app/logs", "/app/config"]

# Set environment variables
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Expose AppDaemon port
EXPOSE 5050

# Create entrypoint script
RUN echo '#!/bin/bash\n\
if [ -f /app/config/.env ]; then\n\
  export $(grep -v "^#" /app/config/.env | xargs)\n\
fi\n\
# Run AppDaemon\n\
exec appdaemon -c /app/balkonsolar/appdaemon\n\
' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Usage instructions in comments:
# Build with: docker build -t balkonsolar .
# Run with: docker run -d --name balkonsolar \
#   -v /path/to/config:/app/config \
#   -v /path/to/data:/app/data \
#   -v /path/to/logs:/app/logs \
#   -p 5050:5050 \
#   balkonsolar 