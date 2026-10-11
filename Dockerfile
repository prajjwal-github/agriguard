# Multi-stage Dockerfile for AgriGuard AI
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and models
COPY pyproject.toml .
COPY src/ src/
COPY configs/ configs/
COPY datasets/ datasets/
COPY models/exported/ models/exported/
COPY data/reports/ data/reports/

RUN pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["uvicorn", "agriguard.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
