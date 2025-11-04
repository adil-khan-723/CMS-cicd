from django.contrib import admin
from .models import UserProfile, Category, Post, Comment, Tag, BlogPost

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(BlogPost)