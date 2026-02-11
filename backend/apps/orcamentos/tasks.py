from celery import shared_task
from django.core.cache import cache
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def gerar_pdf_orcamento_async(self, orcamento_id):
    from apps.orcamentos.models import Orcamento
    from apps.premissas.models import Premissa
    from apps.orcamentos.services.template_processor import TemplateProcessorService
    from apps.templates.models import Template
    import tempfile
    import os
    import subprocess
    
    try:
        orcamento = Orcamento.objects.get(id=orcamento_id)
        premissa = Premissa.get_ativa()
        cliente = orcamento.cliente
        template = Template.objects.filter(tipo='orcamento', ativo=True).first()
        
        if not template:
            raise Exception('Template não encontrado')
        
        buffer_docx = TemplateProcessorService.processar_template(
            template.arquivo.path, orcamento, premissa, cliente
        )
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_docx:
            tmp_docx.write(buffer_docx.getvalue())
            tmp_docx_path = tmp_docx.name
        
        tmp_dir = os.path.dirname(tmp_docx_path)
        subprocess.run([
            'libreoffice', '--headless', '--convert-to', 'pdf',
            '--outdir', tmp_dir, tmp_docx_path
        ], check=True, capture_output=True, timeout=30)
        
        pdf_path = tmp_docx_path.replace('.docx', '.pdf')
        
        with open(pdf_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()
        
        os.unlink(tmp_docx_path)
        os.unlink(pdf_path)
        
        cache.set(f'pdf_orcamento_{orcamento_id}', pdf_content, timeout=3600)
        return {'status': 'success', 'orcamento_id': orcamento_id}
        
    except Exception as e:
        logger.error(f'Erro ao gerar PDF: {str(e)}')
        raise self.retry(exc=e, countdown=60)

@shared_task
def calcular_dashboard_metrics():
    from apps.clientes.models import Cliente
    from apps.orcamentos.models import Orcamento
    from django.utils import timezone
    from datetime import timedelta
    
    data_limite = timezone.now() - timedelta(days=30)
    
    metrics = {
        'total_clientes': Cliente.objects.count(),
        'novos_leads': Cliente.objects.filter(created_at__gte=data_limite, status='orcamento').count(),
        'orcamentos_ativos': Orcamento.objects.filter(convertido_proposta=False).count(),
        'valor_total_orcamentos': float(Orcamento.objects.aggregate(total=models.Sum('valor_final'))['total'] or 0)
    }
    
    cache.set('dashboard_metrics', metrics, timeout=300)
    return metrics

@shared_task
def processar_orcamento_async(data):
    from apps.orcamentos.models import Orcamento
    from apps.premissas.models import Premissa
    from apps.clientes.models import Cliente
    from apps.orcamentos.services.deslocamento_service import DeslocamentoService
    from decimal import Decimal, ROUND_UP, ROUND_HALF_UP
    
    premissa = Premissa.get_ativa()
    cliente = Cliente.objects.get(id=data['cliente_id'])
    vendedor_id = data.get('vendedor_id') or (cliente.vendedor.id if cliente.vendedor else None)
    
    deslocamento = DeslocamentoService.calcular_custo_deslocamento(cliente.cidade, premissa)
    valor_deslocamento = Decimal(str(deslocamento.get('custo_combustivel', 0)))
    
    valor_kit = Decimal(str(data['valor_kit']))
    valor_projeto = premissa.valor_projeto
    valor_montagem = premissa.montagem_por_painel * data['quantidade_paineis']
    valor_estrutura = Decimal(str(data.get('valor_estrutura', 0)))
    valor_material_eletrico = Decimal(str(data['valor_material_eletrico']))
    valor_adicionais = sum(Decimal(str(item.get('valor_total', 0))) for item in data.get('itens_adicionais', []))
    
    subtotal = valor_kit + valor_projeto + valor_montagem + valor_estrutura + valor_material_eletrico + valor_adicionais + valor_deslocamento
    
    percentual_total = (premissa.comissao_percentual + premissa.imposto_percentual + premissa.margem_lucro_percentual) / Decimal('100')
    valor_base = subtotal / (Decimal('1') - percentual_total)
    valor_base_arredondado = (valor_base / 100).quantize(Decimal('1'), rounding=ROUND_UP) * 100
    
    margem_desconto = valor_base_arredondado * (premissa.margem_desconto_avista_percentual / 100)
    valor_com_margem = valor_base_arredondado + margem_desconto
    valor_final = (valor_com_margem / 100).quantize(Decimal('1'), rounding=ROUND_UP) * 100
    
    forma_pagamento = data.get('forma_pagamento', 'avista')
    taxa_juros = Decimal('0')
    valor_parcela = None
    valor_final_com_juros = valor_final
    
    if forma_pagamento != 'avista':
        taxas = premissa.taxas_maquininha
        taxa_juros = Decimal(str(taxas.get(forma_pagamento, 0)))
        valor_final_com_juros = valor_final * (1 + taxa_juros / 100)
        valor_final_com_juros = valor_final_com_juros.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        valor_parcela = (valor_final_com_juros / int(forma_pagamento)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    ultimo = Orcamento.objects.order_by('-id').first()
    numero = f"ORC-{(ultimo.id + 1) if ultimo else 1:04d}"
    
    orcamento = Orcamento.objects.create(
        numero=numero,
        nome_kit=data['nome_kit'],
        cliente_id=data['cliente_id'],
        vendedor_id=vendedor_id,
        valor_kit=valor_kit,
        marca_painel=data['marca_painel'],
        potencia_painel=data['potencia_painel'],
        quantidade_paineis=data['quantidade_paineis'],
        marca_inversor=data['marca_inversor'],
        potencia_inversor=data['potencia_inversor'],
        quantidade_inversores=data['quantidade_inversores'],
        tipo_estrutura=data['tipo_estrutura'],
        valor_estrutura=valor_estrutura,
        valor_material_eletrico=valor_material_eletrico,
        itens_adicionais=data.get('itens_adicionais', []),
        valor_total=subtotal,
        forma_pagamento=forma_pagamento,
        taxa_juros=taxa_juros,
        valor_final=valor_final_com_juros if forma_pagamento != 'avista' else valor_final,
        valor_parcela=valor_parcela
    )
    
    return orcamento.id
