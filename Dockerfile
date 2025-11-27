FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements_hf.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_hf.txt

# Copy application code
COPY app_hf.py .
COPY modules/ ./modules/
COPY frontend/ ./frontend/
COPY model/ ./model/

# Create necessary directories
RUN mkdir -p dataset_private/raw \
    dataset_private/processed \
    training_logs \
    uploads_temp

# Expose port (Hugging Face uses 7860)
EXPOSE 7860

# Set environment variables
ENV PORT=7860
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "app_hf.py"]
