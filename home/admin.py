from django.contrib import admin
from .models import Category, Post, subscriber
# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(subscriber)