# Use Python base image
FROM python:3.11-slim

# Install system dependencies (Tesseract, OCR language data, and image libraries)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1 \
    build-essential \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "ocr_api:app", "--host", "0.0.0.0", "--port", "8000"]
