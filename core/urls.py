from django.contrib import admin
from django.urls import path
from blog.views import post_list, post_detail, about, projects, api_create_post

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', post_list, name='post_list'),
    path('about/', about, name='about'),
    path('projects/', projects, name='projects'),
    path('api/v1/create-post/', api_create_post, name='api_create_post'), # Yeni kapı
    path('<slug:post>/', post_detail, name='post_detail'),
]