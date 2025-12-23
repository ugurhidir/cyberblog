from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Post, Profile, Skill, Certificate, Project

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