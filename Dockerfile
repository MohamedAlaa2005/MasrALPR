# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- CRITICAL CHANGES BELOW ---
# 1. Copy the Python logic
COPY ./app ./app

# 2. Copy the Frontend folder (which includes index.html and /static)
COPY ./frontend ./frontend

# 3. Copy any existing database or static uploads if needed
COPY ./static ./static 
# ------------------------------

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]