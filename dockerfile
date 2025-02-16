FROM python:3.12-slim-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev

# Download and install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Install Python dependencies
RUN pip install fastapi uvicorn Pillow

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin:$PATH"

# Set up the application directory
WORKDIR /app

# Copy the entire project directory
COPY . /app

# Copy application files
COPY app.py /app

# Expose the application port
EXPOSE 8000

# Run the application
CMD ["/root/.local/bin/uv", "run", "app.py"]