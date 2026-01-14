from django.core.management.base import BaseCommand
from contexts.catalogo.infrastructure.django_models.marca_model import MarcaModel
from contexts.cadastros.infrastructure.django_models.fornecedor_model import FornecedorModel
from contexts.catalogo.infrastructure.django_models.inversor_model import InversorModel
from decimal import Decimal


class Command(BaseCommand):
    help = 'Cadastra inversores monofásicos Solis'

    def handle(self, *args, **options):
        marca_solis, _ = MarcaModel.objects.get_or_create(
            nome="Solis",
            defaults={'ativo': True}
        )
        self.stdout.write(f"✅ Marca Solis: {marca_solis.id}")

        fornecedor, _ = FornecedorModel.objects.get_or_create(
            cnpj="11.222.333/0001-81",
            defaults={
                'nome': "Fornecedor Solar Ltda",
                'email': "contato@fornecedor.com",
                'telefone': "11999999999",
                'ativo': True
            }
        )
        self.stdout.write(f"✅ Fornecedor: {fornecedor.id}")

        inversores = [
            {"nome": "Solis 1P 0.7K-4G", "potencia": "0.7", "preco": "1200.00"},
            {"nome": "Solis 1P 1.0K-4G", "potencia": "1.0", "preco": "1400.00"},
            {"nome": "Solis 1P 1.5K-4G", "potencia": "1.5", "preco": "1600.00"},
            {"nome": "Solis 1P 2.0K-4G", "potencia": "2.0", "preco": "1800.00"},
            {"nome": "Solis 1P 2.5K-4G", "potencia": "2.5", "preco": "2000.00"},
            {"nome": "Solis 1P 3.0K-4G", "potencia": "3.0", "preco": "2200.00"},
            {"nome": "Solis 1P 3.6K-4G", "potencia": "3.6", "preco": "2400.00"},
            {"nome": "Solis 1P 4.0K-4G", "potencia": "4.0", "preco": "2600.00"},
            {"nome": "Solis 1P 4.6K-4G", "potencia": "4.6", "preco": "2800.00"},
            {"nome": "Solis 1P 5.0K-4G", "potencia": "5.0", "preco": "3000.00"},
            {"nome": "Solis 1P 6.0K-4G", "potencia": "6.0", "preco": "3200.00"},
        ]

        count = 0
        for inv in inversores:
            _, created = InversorModel.objects.get_or_create(
                nome=inv["nome"],
                defaults={
                    'marca_id': marca_solis.id,
                    'fornecedor_id': fornecedor.id,
                    'preco': Decimal(inv["preco"]),
                    'potencia': Decimal(inv["potencia"]),
                    'tipo': 'STRING',
                    'fases': 1,
                    'ativo': True
                }
            )
            if created:
                count += 1
                self.stdout.write(f"✅ {inv['nome']} - {inv['potencia']}kW - R$ {inv['preco']}")

        self.stdout.write(self.style.SUCCESS(f"\n🎉 {count} inversores cadastrados!"))
