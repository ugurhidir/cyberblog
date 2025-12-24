import json
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.conf import settings
from .models import Post, Profile, Skill, Certificate, Project

# --- NORMAL GÖRÜNÜMLER ---
def post_list(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(status='published')
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(body__icontains=query))
    template_base = "base.html"
    if request.headers.get('HX-Request'):
        template_base = "blog/partial.html"
    return render(request, 'blog/post_list.html', {'posts': posts, 'template_base': template_base})

def post_detail(request, post):
    post = get_object_or_404(Post, slug=post, status='published')
    template_base = "base.html"
    if request.headers.get('HX-Request'):
        template_base = "blog/partial.html"
    return render(request, 'blog/post_detail.html', {'post': post, 'template_base': template_base})

def about(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    certificates = Certificate.objects.all()
    template_base = "base.html"
    if request.headers.get('HX-Request'):
        template_base = "blog/partial.html"
    return render(request, 'blog/about.html', {
        'profile': profile, 'skills': skills, 'certificates': certificates, 'template_base': template_base
    })

def projects(request):
    projects_list = Project.objects.all()
    template_base = "base.html"
    if request.headers.get('HX-Request'):
        template_base = "blog/partial.html"
    return render(request, 'blog/projects.html', {'projects': projects_list, 'template_base': template_base})

# --- OTOMASYON API (n8n İÇİN) ---
@csrf_exempt
def api_create_post(request):
    # Bu key settings.py içinde tanımlanmalı (bir sonraki adımda yapacağız)
    BLOG_API_KEY = "sloan_automation_secret_key_987"
    
    if request.method == 'POST':
        api_key = request.headers.get('X-Api-Key')
        if api_key != BLOG_API_KEY:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        try:
            data = json.loads(request.body)
            # Aynı başlıkta yazı varsa tekrar oluşturma (Spam kontrolü)
            slug = slugify(data['title'])
            if Post.objects.filter(slug=slug).exists():
                return JsonResponse({'message': 'Post already exists'}, status=200)

            new_post = Post.objects.create(
                title=data['title'],
                slug=slug,
                body=data['content'],
                author=User.objects.first(), # İlk admini yazar yapar
                status='published'
            )
            return JsonResponse({'message': 'Success', 'id': new_post.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only POST allowed'}, status=405)