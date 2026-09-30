# MoviSabio Enterprise Platform
FROM python:3.11-slim

# Install system dependencies (SUMO, OpenCV reqs, PostGIS clients)
RUN apt-get update && apt-get install -y \
    sumo \
    sumo-tools \
    sumo-doc \
    libgl1-mesa-glx \
    libglib2.0-0 \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set up non-root user for security
RUN useradd -m -s /bin/bash movisabio
USER movisabio
WORKDIR /home/movisabio/app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY --chown=movisabio:movisabio . .

# Set Python path
ENV PYTHONPATH=/home/movisabio/app
ENV SUMO_HOME=/usr/share/sumo

# Expose API and Dashboard ports
EXPOSE 8000 8501

# Default command (can be overridden by docker-compose)
CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
