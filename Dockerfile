# Use a Python base image
FROM python:3.11-slim

# Install system packages including tesseract and OpenCV dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    ffmpeg \
    build-essential \
    poppler-utils \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy your app code
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Set environment variable if needed
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/

# Expose port (optional if your app runs on 10000 for example)
EXPOSE 10000

# Start your FastAPI app with uvicorn
CMD ["uvicorn", "ocr_api:app", "--host", "0.0.0.0", "--port", "10000"]
