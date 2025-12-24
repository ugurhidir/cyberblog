FROM python:3.11

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Gereksinimleri yükle
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Projeyi kopyala
COPY . .

# Persistence klasörünü oluştur
RUN mkdir -p /app/persistent_data

# Statik dosyaları topla (Build aşamasında)
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# OTOMASYON: Önce veritabanını güncelle, sonra uygulamayı başlat
CMD sh -c "python manage.py migrate --noinput && gunicorn core.wsgi:application --bind 0.0.0.0:8000"