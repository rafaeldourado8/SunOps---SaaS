"""Models para configurações financeiras."""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class ConfiguracaoFinanceira(models.Model):
    """Configurações financeiras - ADMIN ONLY."""
    
    comissao_percentual = models.DecimalField(
        max_digits=5, decimal_places=4, default=0.05,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Comissão (ex: 0.05 = 5%)"
    )
    imposto_percentual = models.DecimalField(
        max_digits=5, decimal_places=4, default=0.06,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Impostos (ex: 0.06 = 6%)"
    )
    margem_lucro_minima = models.DecimalField(
        max_digits=5, decimal_places=4, default=0.20,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Margem mínima (ex: 0.20 = 20%)"
    )
    custo_montagem_por_painel = models.DecimalField(
        max_digits=10, decimal_places=2, default=70.00,
        validators=[MinValueValidator(0)],
        help_text="Custo montagem/painel (R$)"
    )
    custo_operacional_fixo = models.DecimalField(
        max_digits=10, decimal_places=2, default=500.00,
        validators=[MinValueValidator(0)],
        help_text="Custo operacional fixo (R$)"
    )
    arredondamento_multiplo = models.IntegerField(
        default=100, validators=[MinValueValidator(1)],
        help_text="Múltiplo arredondamento"
    )
    ativo = models.BooleanField(default=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    atualizado_por = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = 'configuracao_financeira'
        verbose_name = 'Configuração Financeira'
        verbose_name_plural = 'Configurações Financeiras'
    
    def save(self, *args, **kwargs):
        if self.ativo:
            ConfiguracaoFinanceira.objects.filter(ativo=True).update(ativo=False)
        super().save(*args, **kwargs)


class AuditoriaFinanceira(models.Model):
    """Log de alterações financeiras."""
    
    admin_nome = models.CharField(max_length=200)
    acao = models.CharField(max_length=100)
    campo_alterado = models.CharField(max_length=100)
    valor_anterior = models.CharField(max_length=100)
    valor_novo = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'auditoria_financeira'
        ordering = ['-timestamp']
