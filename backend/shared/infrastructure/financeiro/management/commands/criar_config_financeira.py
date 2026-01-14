"""Cria configuração financeira inicial."""
from django.core.management.base import BaseCommand
from shared.infrastructure.financeiro.models import ConfiguracaoFinanceira


class Command(BaseCommand):
    help = 'Cria configuração financeira inicial'
    
    def handle(self, *args, **options):
        if not ConfiguracaoFinanceira.objects.exists():
            config = ConfiguracaoFinanceira.objects.create(
                comissao_percentual=0.05,
                imposto_percentual=0.06,
                margem_lucro_minima=0.20,
                custo_montagem_por_painel=70.00,
                custo_operacional_fixo=500.00,
                arredondamento_multiplo=100,
                ativo=True,
                atualizado_por='system'
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Configuração criada: {config}'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  Configuração já existe'))
