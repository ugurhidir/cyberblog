# Slim yerine tam sürüm kullanalım (Derleme hatalarını önler)
FROM python:3.11

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Sistem bağımlılıklarını güncelle (Gerekirse diye)
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Upgrade pip ve paketleri yükle
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]