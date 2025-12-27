FROM python:3.11-slim

WORKDIR /app

# deps système (souvent nécessaires pour numpy/scipy/sklearn sur slim)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
EXPOSE 8080

CMD sh -c "gunicorn colors_images:app --workers 2 --threads 4 --timeout 120 --bind 0.0.0.0:${PORT:-8080}"
