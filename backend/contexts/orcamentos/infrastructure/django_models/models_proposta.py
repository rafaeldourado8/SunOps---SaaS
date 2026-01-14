"""Models para templates de propostas."""
from django.db import models
from django.core.validators import MinValueValidator


class TemplateProposta(models.Model):
    """Template de proposta comercial."""
    
    TIPO_CHOICES = [
        ('RESIDENCIAL', 'Residencial'),
        ('COMERCIAL', 'Comercial'),
        ('INDUSTRIAL', 'Industrial'),
    ]
    
    STATUS_CHOICES = [
        ('RASCUNHO', 'Rascunho'),
        ('MAPEAMENTO', 'Em Mapeamento'),
        ('VALIDADO', 'Validado'),
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo'),
    ]
    
    nome = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    versao = models.CharField(max_length=20, default='1.0')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RASCUNHO')
    
    # Template HTML
    conteudo_html = models.TextField(help_text="HTML do template")
    
    # Mapeamento validado
    mapeamento_confirmado = models.BooleanField(default=False)
    mapeamento_json = models.JSONField(null=True, blank=True, help_text="Bindings validados")
    
    # Controle
    criado_por = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)
    validado_por = models.CharField(max_length=100, blank=True)
    validado_em = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'template_proposta'
        ordering = ['-criado_em']
        unique_together = ['nome', 'versao']
    
    def __str__(self):
        return f"{self.nome} v{self.versao} ({self.status})"


class CampoSistema(models.Model):
    """Campos disponíveis do sistema para mapeamento."""
    
    TIPO_CHOICES = [
        ('TEXTO', 'Texto'),
        ('NUMERO', 'Número'),
        ('MOEDA', 'Moeda'),
        ('PERCENTUAL', 'Percentual'),
        ('DATA', 'Data'),
    ]
    
    nome_interno = models.CharField(max_length=100, unique=True)
    nome_exibicao = models.CharField(max_length=200)
    descricao = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=50)
    exemplo = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'campo_sistema'
        ordering = ['categoria', 'nome_exibicao']
    
    def __str__(self):
        return f"{self.nome_exibicao} ({{{{self.nome_interno}}}})"


class MapeamentoCampo(models.Model):
    """Mapeamento entre label do template e campo do sistema."""
    
    template = models.ForeignKey(TemplateProposta, on_delete=models.CASCADE, related_name='mapeamentos')
    label_template = models.CharField(max_length=200, help_text="Label detectado no template")
    campo_sistema = models.ForeignKey(CampoSistema, on_delete=models.PROTECT)
    
    # IA
    sugerido_por_ia = models.BooleanField(default=False)
    confianca_ia = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Validação
    validado = models.BooleanField(default=False)
    validado_por = models.CharField(max_length=100, blank=True)
    validado_em = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'mapeamento_campo'
        unique_together = ['template', 'label_template']
    
    def __str__(self):
        return f"{self.label_template} → {self.campo_sistema.nome_interno}"


class PropostaGerada(models.Model):
    """Proposta gerada para um cliente."""
    
    STATUS_CHOICES = [
        ('GERADA', 'Gerada'),
        ('ENVIADA', 'Enviada'),
        ('VISUALIZADA', 'Visualizada'),
        ('APROVADA', 'Aprovada'),
        ('REJEITADA', 'Rejeitada'),
    ]
    
    uuid = models.UUIDField(unique=True)
    template = models.ForeignKey(TemplateProposta, on_delete=models.PROTECT)
    
    # Cliente
    cliente_nome = models.CharField(max_length=200)
    cliente_email = models.EmailField(blank=True)
    
    # Snapshot dos dados
    dados_orcamento = models.JSONField(help_text="Snapshot completo do orçamento")
    template_snapshot = models.TextField(help_text="HTML renderizado")
    
    # Controle
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='GERADA')
    gerado_por = models.CharField(max_length=100)
    gerado_em = models.DateTimeField(auto_now_add=True)
    
    # Rastreamento
    visualizacoes = models.IntegerField(default=0)
    ultima_visualizacao = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'proposta_gerada'
        ordering = ['-gerado_em']
    
    def __str__(self):
        return f"Proposta {self.uuid} - {self.cliente_nome}"
