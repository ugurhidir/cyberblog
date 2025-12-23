from django.shortcuts import render, get_object_or_404
from .models import Post
from django.db.models import Q

def post_list(request):
    query = request.GET.get('q')
    
    if query:
        # Hem başlıkta (title) HEM DE içerikte (body) arama yapar
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query),
            status='published'
        )
    else:
        posts = Post.objects.filter(status='published')
    
    template_base = "base.html"
    if request.headers.get('HX-Request'):
        template_base = "blog/partial.html"

    return render(request, 'blog/post_list.html', {
        'posts': posts, 
        'template_base': template_base,
        'query': query # Aranan kelimeyi şablona geri gönderiyoruz
    })

def post_detail(request, post):
    post = get_object_or_404(Post, slug=post, status='published')
    
    # Aynı mantık burada da geçerli
    template_base = "base.html"
    if request.headers.get('HX-Request'):
        template_base = "blog/partial.html"

    return render(request, 'blog/post_detail.html', {
        'post': post, 
        'template_base': template_base
    })
    
def about(request):
    template_base = "base.html"
    if request.headers.get('HX-Request'):
        template_base = "blog/partial.html"
    return render(request, 'blog/about.html', {'template_base': template_base})

def projects(request):
    template_base = "base.html"
    if request.headers.get('HX-Request'):
        template_base = "blog/partial.html"
    return render(request, 'blog/projects.html', {'template_base': template_base})