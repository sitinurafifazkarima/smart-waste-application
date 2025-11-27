# 🐳 DOCKERFILE FOR DEPLOYMENT
# ==============================
# Build Docker image for deployment

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements_deploy.txt .
RUN pip install --no-cache-dir -r requirements_deploy.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p backend/uploads_temp backend/dataset_private/raw backend/dataset_private/processed backend/model backend/training_logs

# Expose port
EXPOSE 5000

# Environment variables
ENV FLASK_ENV=production
ENV PORT=5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Run the application
CMD ["gunicorn", "--chdir", "backend", "app:app", "--bind", "0.0.0.0:5000", "--timeout", "120", "--workers", "2"]
