"""
URL Configuration
"""
from django.contrib import admin
from django.urls import path
from config.admin import superadmin_site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('superadmin/', superadmin_site.urls),
]
