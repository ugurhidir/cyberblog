import json
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from django.contrib.auth.models import User
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
    return render(request, 'blog/about.html', {'profile': profile, 'skills': skills, 'certificates': certificates, 'template_base': template_base})

def projects(request):
    projects_list = Project.objects.all()
    template_base = "base.html"
    if request.headers.get('HX-Request'):
        template_base = "blog/partial.html"
    return render(request, 'blog/projects.html', {'projects': projects_list, 'template_base': template_base})

# --- AKILLI OTOMASYON API ---
@csrf_exempt
def api_create_post(request):
    BLOG_API_KEY = "sloan_automation_secret_key_987"
    
    # 1. Güvenlik Kontrolü
    api_key = request.headers.get('X-Api-Key')
    if api_key != BLOG_API_KEY:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    # 2. Kontrol Modu (n8n Gemini'ye gitmeden önce buraya soracak)
    if request.method == 'GET':
        check_url = request.GET.get('check_url')
        if check_url and Post.objects.filter(source_url=check_url).exists():
            return JsonResponse({'exists': True})
        return JsonResponse({'exists': False})

    # 3. Yazı Oluşturma Modu (POST)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            source_url = data.get('source_url')
            title = data.get('title')
            content = data.get('content')

            if Post.objects.filter(source_url=source_url).exists():
                return JsonResponse({'message': 'Already exists'}, status=200)

            author = User.objects.filter(is_superuser=True).first() or User.objects.first()
            new_post = Post.objects.create(
                title=title,
                slug=slugify(title),
                body=content,
                source_url=source_url,
                author=author,
                status='published'
            )
            return JsonResponse({'message': 'Success', 'id': new_post.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)