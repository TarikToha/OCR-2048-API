# Use a lightweight Python base image
FROM python:3.11-slim

# Install dependencies: Tesseract and build tools
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy your code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for FastAPI
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "ocr_api:app", "--host", "0.0.0.0", "--port", "8000"]
