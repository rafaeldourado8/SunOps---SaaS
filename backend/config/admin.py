from django.contrib import admin
from django.contrib.admin import AdminSite


class SuperAdminSite(AdminSite):
    site_header = 'OPS CRM - Super Admin'
    site_title = 'OPS CRM Admin'
    index_title = 'Gerenciamento Multi-Tenant'
    
    def has_permission(self, request):
        """Apenas superusers podem acessar"""
        return request.user.is_active and request.user.is_superuser


superadmin_site = SuperAdminSite(name='superadmin')
