"""
URL configuration for News project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from home.views import post, home, post_detail, esewa_request, esewa_verify, post_by_category, add_post, post_delete, post_edit
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path('post/<str:url>', post_detail, name='post'),
    path('category/<str:cat_name>/', post_by_category, name = "post_by_category"),
    path('accounts/', include('allauth.urls')),
    path('addPost/', add_post, name = "add_post"),
    path('editPost/<int:pid>/',post_edit, name = "post_edit"),
    path('deletePost/<int:pid>/', post_delete, name = 'post_delete'),
    path('subscribe/', esewa_request, name='subscribe'),
    path('esewa_verify/', esewa_verify, name='esewa_verify'),

]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
