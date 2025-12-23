from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Taslak'),
        ('published', 'Yayında'),
    )

    title = models.CharField(max_length=250, verbose_name="Başlık")
    slug = models.SlugField(max_length=250, unique_for_date='publish', verbose_name="URL Yolu")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name="Yazar")
    body = models.TextField(verbose_name="İçerik")
    publish = models.DateTimeField(default=timezone.now, verbose_name="Yayınlanma Tarihi")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="Durum")

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Yazı'
        verbose_name_plural = 'Yazılar'

    def __str__(self):
        return self.title