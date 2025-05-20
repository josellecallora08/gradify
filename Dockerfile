# Start from a slim, minimal Python base image
FROM python:3.10-slim

# Avoid Python stdout buffering (helpful for logging in Docker)
ENV PYTHONUNBUFFERED=1

# Disable pip cache to reduce image size
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DEFAULT_TIMEOUT=100
ENV PIP_RETRIES=10

# Set the working directory inside the container
WORKDIR /app

# Install required system libraries
# ⚠️ Double-check if all these are necessary — each adds size.
# - ffmpeg: For audio/video processing
# - libsndfile1: Needed for soundfile or similar libraries
# - libsoxr-dev: Optional, for audio resampling
# - libasound2: ALSA audio support
# - libgl1: Required for OpenCV or anything needing OpenGL
# - build-essential: Needed for pip installs requiring compilation (purged later)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    libsoxr-dev \
    libasound2 \
    libgl1 \
    build-essential \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
# ⚠️ Any large deps? Consider pre-built wheels or multi-stage builds.
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apt-get purge -y build-essential && \
    apt-get autoremove -y

# Copy the rest of your app into the image
COPY . .

# Expose port 8080 (update if your app uses a different one)
EXPOSE 8080

# Run your Python app (change `main.py` if needed)
CMD ["python", "main.py"]
