from django.contrib import admin
from django.urls import path
from blog.views import post_list, post_detail, about, projects  # about ve projects eklendi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', post_list, name='post_list'),
    path('about/', about, name='about'),       # Yeni
    path('projects/', projects, name='projects'), # Yeni
    path('<slug:post>/', post_detail, name='post_detail'),
]