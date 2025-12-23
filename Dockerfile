# Python 3.11 Slim versiyonunu kullan (Hafif)
FROM python:3.11-slim

# Python loglarını anlık görmek için
ENV PYTHONUNBUFFERED=1

# Çalışma dizini oluştur
WORKDIR /app

# Gereksinimleri kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Statik dosyaları (CSS/JS) topla
RUN python manage.py collectstatic --noinput

# Portu aç (Gunicorn için)
EXPOSE 8000

# Uygulamayı başlat
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]