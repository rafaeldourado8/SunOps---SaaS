from django.contrib import admin
from django.urls import path
from core.views import login, me

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/login', login),
    path('api/v1/auth/me', me),
]
