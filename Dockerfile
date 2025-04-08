# Use a slim Python base image
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

# Copy all your code
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Optional: set Tesseract data path
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/

# Expose the port your app runs on (default FastAPI port)
EXPOSE 8000

# ✅ Run your FastAPI app from ocr_api.py
CMD ["uvicorn", "ocr_api:app", "--host", "0.0.0.0", "--port", "8000"]
