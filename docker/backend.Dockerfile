FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    sumo \
    sumo-tools \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ /app/backend/
COPY aitcs/ /app/aitcs/
COPY scripts/ /app/scripts/

ENV PYTHONPATH=/app
ENV ENVIRONMENT=production
ENV SUMO_HOME=/usr/share/sumo
ENV CONTROLLER_MODE=mock

RUN useradd --create-home --shell /usr/sbin/nologin movisabio \
    && chown -R movisabio:movisabio /app
USER movisabio

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
