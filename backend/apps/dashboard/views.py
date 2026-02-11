from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from apps.clientes.models import Cliente
from apps.orcamentos.models import Orcamento
from apps.orcamentos.tasks import calcular_dashboard_metrics
from django.utils import timezone
from datetime import timedelta

class DashboardResumoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        cache_key = f'dashboard_{user.id}'
        
        # Tentar cache primeiro
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        if user.is_staff or user.is_superuser:
            clientes = Cliente.objects.all()
            orcamentos = Orcamento.objects.all()
        else:
            clientes = Cliente.objects.filter(criado_por=user)
            orcamentos = Orcamento.objects.filter(cliente__criado_por=user)
        
        data_limite = timezone.now() - timedelta(days=30)
        
        data = {
            'total_clientes': clientes.count(),
            'novos_leads': clientes.filter(created_at__gte=data_limite, status='orcamento').count(),
            'propostas_ativas': orcamentos.filter(convertido_proposta=False).count(),
            'ultimos_clientes': list(clientes[:5].values('id', 'nome', 'telefone', 'status', 'created_at'))
        }
        
        # Cache por 5 minutos
        cache.set(cache_key, data, timeout=300)
        
        # Atualizar métricas globais em background
        if user.is_staff or user.is_superuser:
            calcular_dashboard_metrics.delay()
        
        return Response(data)
