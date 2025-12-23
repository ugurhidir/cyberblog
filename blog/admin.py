from django.contrib import admin
from .models import Post, Profile, Skill, Certificate, Project

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')

admin.site.register(Skill)
admin.site.register(Certificate)
admin.site.register(Project)