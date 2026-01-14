"""Models Django para chat."""
from django.db import models
from django.utils import timezone


class Conversa(models.Model):
    """Conversa entre admin e vendedor."""
    
    class Status(models.TextChoices):
        ABERTA = 'ABERTA', 'Aberta'
        EM_ATENDIMENTO = 'EM_ATENDIMENTO', 'Em Atendimento'
        RESOLVIDA = 'RESOLVIDA', 'Resolvida'
        FECHADA = 'FECHADA', 'Fechada'
    
    id = models.UUIDField(primary_key=True)
    vendedor_id = models.CharField(max_length=100)
    admin_id = models.CharField(max_length=100, null=True, blank=True)
    assunto = models.CharField(max_length=255, default='Solicitação de orçamento')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ABERTA)
    criada_em = models.DateTimeField(default=timezone.now)
    atualizada_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'chat_conversas'
        ordering = ['-atualizada_em']


class Mensagem(models.Model):
    """Mensagem do chat."""
    
    class TipoRemetente(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        VENDEDOR = 'VENDEDOR', 'Vendedor'
        IA = 'IA', 'IA'
    
    class Status(models.TextChoices):
        ENVIADA = 'ENVIADA', 'Enviada'
        ENTREGUE = 'ENTREGUE', 'Entregue'
        LIDA = 'LIDA', 'Lida'
    
    id = models.UUIDField(primary_key=True)
    conversa = models.ForeignKey(Conversa, on_delete=models.CASCADE, related_name='mensagens')
    remetente_id = models.CharField(max_length=100)
    tipo_remetente = models.CharField(max_length=10, choices=TipoRemetente.choices)
    conteudo = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ENVIADA)
    metadata = models.JSONField(null=True, blank=True)
    
    class Meta:
        db_table = 'chat_mensagens'
        ordering = ['timestamp']
