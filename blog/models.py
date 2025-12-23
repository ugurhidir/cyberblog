from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    STATUS_CHOICES = (('draft', 'Taslak'), ('published', 'Yayında'))
    title = models.CharField(max_length=250, verbose_name="Başlık")
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)
    def __str__(self):
        return self.title

class Profile(models.Model):
    name = models.CharField(max_length=100, default='Uğur "Sloan" Hıdır')
    title = models.CharField(max_length=100, default='Mid-Level Python Dev')
    bio_summary = models.TextField(verbose_name="Kısa Biyografi")
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    email = models.EmailField(default="ugurhidir34@gmail.com")
    education_uni = models.CharField(max_length=200, default="Eskişehir Osmangazi Uni.")
    education_dept = models.CharField(max_length=200, default="Computer Programming")
    education_year = models.CharField(max_length=50, default="2017 - 2020")

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=50)
    percentage = models.IntegerField(default=80)
    def __str__(self):
        return f"{self.name} (%{self.percentage})"

class Certificate(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, help_text="Örn: OWN PROJECT, SECURITY")
    technologies = models.CharField(max_length=200, help_text="Örn: Python, Django, HTMX")
    repo_url = models.URLField(blank=True)
    year = models.CharField(max_length=4, default="2025")
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.title