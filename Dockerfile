# ===============================
# Stage 1: Build frontend
# ===============================
FROM node:24.12.0-alpine AS frontend-builder

WORKDIR /app

# Copy package files first to leverage Docker cache
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install --quiet 

# Copy the rest of the frontend code
COPY index.html ./
COPY public ./public
COPY src ./src
COPY vite.config.js ./

# Build the frontend
RUN npm run build

# ===============================
# Stage 2: Build backend dependencies
# ==============================
FROM python:3.13-slim AS backend-builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build tools for Python packages, if needed
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ===============================
# Stage 3: Final production image
# ===============================
FROM python:3.13-slim

# Install curl for healthcheck
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -g 1003 saudi && \ 
    useradd -u 1003 -g saudi -s /usr/sbin/nologin saudi

WORKDIR /app

# Copy Python packages from builder (use correct Python version path)
COPY --from=backend-builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Copy backend application code
COPY --chown=saudi:saudi app ./app

# Copy built frontend from the frontend-builder stage (use 'build' not 'dist')
COPY --from=frontend-builder /app/build ./public

# Switch to non-root user
USER saudi

# Expose port for the application
EXPOSE 7070

# Healthcheck to ensure the application is running
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:7070/health || exit 1

# Fixed CMD - use correct module path
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7070", "--log-level", "info"]