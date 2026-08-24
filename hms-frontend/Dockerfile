#Stage 1: Build dependencies
FROM python:3.13-slim AS builder

WORKDIR /app 

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONBUFFERED=1

# Insall buld dependencies if needed, then buld wheels 

COPY py-env/requirements.txt . 
RUN pip install --no-cache-dir --prefix=/py-root -r requirements.txt 

# Stage 2: Final runtime image

FROM python:3.13-slim AS runner 

WORKDIR /app 

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONBUFFERED=1 \
    PORT=9001

# Copy installed Python dependencies from builder
COPY --from=builder /py-root /usr/local

# Copy application source code and configuration
COPY hms-frontend/app.py . 
COPY hms-frontend/templates .

# Run application 
CMD ["python","app.py"]
