# Stage 1: Build dependencies
FROM python:3.14-slim AS ksa

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# System dependencies for building some python packages, and clean up
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final application image
FROM python:3.14-slim

# Create a non-root user
RUN addgroup --system app && \ 
    adduser --system --ingroup app app

# Set working directory
WORKDIR /

# Copy virtual environment from ksa
COPY --from=ksa /opt/venv /opt/venv

# Copy application code
COPY app /app
COPY public /public
COPY src /src

# Set ownership to non-root user
RUN chown -R app:app /app /public /src

# Set user
USER app

# Activate virtual environment by adding it to the path
ENV PATH="/opt/venv/bin:$PATH"

# Expose port and run application

EXPOSE 7070

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \ 
     CMD [ "curl", "-f", "http://localhost:7070/health"] || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7070"]
