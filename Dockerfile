# ===============================
# Stage 1: Build frontend
# ===============================
FROM node:20-alpine AS frontend-builder

WORKDIR /app

# Copy package files first to leverage Docker cache
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install --silent

# Copy the rest of the frontend code
COPY public ./public
COPY src ./src

# Build the frontend
RUN npm run build

# ===============================
# Stage 2: Build backend dependencies
# ===============================
FROM python:3.14-slim AS backend-builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build tools for Python packages, if needed
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ===============================
# Stage 3: Final production image
# ===============================
FROM python:3.14-slim

# Create non-root user
RUN addgroup --system app && adduser --system --ingroup app app

WORKDIR /app

# Copy backend packages from builder
COPY --from=backend-builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Copy backend application code
COPY --chown=app:app app ./app

# Copy built frontend from the frontend-builder stage
COPY --from=frontend-builder /app/build ./public

# Switch to non-root user
USER app

# Expose port for the application
EXPOSE 7070

# Healthcheck to ensure the application is running
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python3 - <<EOF
import urllib.request, sys
try:
    urllib.request.urlopen("http://localhost:7070/health")
except:
    sys.exit(1)
EOF

# Run Gunicorn with Uvicorn workers for production
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "app.main:app", "-b", "0.0.0.0:7070", "--log-level", "info"]
