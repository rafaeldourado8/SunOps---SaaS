# Template de Proposta Comercial - Chaves Disponíveis

## 📄 Arquivo
`docs/templates/PROPOSTA_COMERCIAL_TEMPLATE.docx`

## 🔑 Chaves de Template

### Dados do Cliente
| Chave | Descrição | Exemplo |
|-------|-----------|---------|
| `{{cliente_nome}}` | Nome completo do cliente | João Silva |
| `{{cliente_endereco}}` | Endereço completo | Rua das Flores, 123 |
| `{{cliente_bairro}}` | Bairro | Centro |
| `{{cliente_cidade}}` | Cidade | São Paulo |
| `{{cliente_estado}}` | Estado (UF) | SP |
| `{{cliente_cep}}` | CEP | 01234-567 |
| `{{cliente_telefone}}` | Telefone | (11) 98765-4321 |
| `{{cliente_email}}` | E-mail | joao@email.com |

### Dados do Sistema Fotovoltaico
| Chave | Descrição | Exemplo |
|-------|-----------|---------|
| `{{consumo_mensal}}` | Consumo mensal em kWh | 850 |
| `{{potencia_sistema}}` | Potência total do sistema | 10,50 |
| `{{quantidade_paineis}}` | Número de painéis | 20 |
| `{{potencia_painel}}` | Potência unitária do painel | 550 |
| `{{potencia_inversor}}` | Potência do inversor | 10 |
| `{{geracao_mensal}}` | Geração mensal estimada | 1.200 |
| `{{geracao_anual}}` | Geração anual estimada | 14.400 |

### Dados Financeiros
| Chave | Descrição | Exemplo |
|-------|-----------|---------|
| `{{valor_total}}` | Valor total do investimento | R$ 52.500,00 |
| `{{valor_parcela}}` | Valor da parcela | R$ 4.375,00 |
| `{{quantidade_parcelas}}` | Número de parcelas | 12 |
| `{{vida_util_sistema}}` | Vida útil do sistema | 25 |
| `{{economia_mensal}}` | Economia mensal estimada | R$ 1.200,00 |
| `{{economia_anual}}` | Economia anual estimada | R$ 14.400,00 |
| `{{payback}}` | Tempo de retorno do investimento | 3,6 |

### Dados Técnicos
| Chave | Descrição | Exemplo |
|-------|-----------|---------|
| `{{hsp}}` | Horas de Sol Pleno | 5,5 |
| `{{perdas_sistema}}` | Perdas do sistema (%) | 20 |
| `{{degradacao_anual}}` | Degradação anual (%) | 0,8 |

### Dados da Empresa
| Chave | Descrição | Exemplo |
|-------|-----------|---------|
| `{{empresa_nome}}` | Nome da empresa | SunOps Energia Solar |
| `{{empresa_cnpj}}` | CNPJ | 12.345.678/0001-90 |
| `{{empresa_endereco}}` | Endereço da empresa | Av. Paulista, 1000 |
| `{{empresa_telefone}}` | Telefone da empresa | (11) 3000-0000 |
| `{{empresa_email}}` | E-mail da empresa | contato@sunops.com.br |
| `{{empresa_site}}` | Site da empresa | www.sunops.com.br |

### Datas e Validade
| Chave | Descrição | Exemplo |
|-------|-----------|---------|
| `{{data_proposta}}` | Data de emissão da proposta | 15/02/2024 |
| `{{validade_proposta}}` | Validade da proposta em dias | 30 |

## 💡 Como Usar

### No Backend Django

```python
from docx import Document
from docx2pdf import convert
import os

def gerar_proposta_comercial(orcamento_id):
    # Buscar dados do orçamento
    orcamento = Orcamento.objects.get(id=orcamento_id)
    cliente = orcamento.cliente
    
    # Abrir template
    template_path = 'docs/templates/PROPOSTA_COMERCIAL_TEMPLATE.docx'
    doc = Document(template_path)
    
    # Dados para substituição
    dados = {
        # Cliente
        '{{cliente_nome}}': cliente.nome,
        '{{cliente_endereco}}': cliente.endereco,
        '{{cliente_bairro}}': cliente.bairro,
        '{{cliente_cidade}}': cliente.cidade,
        '{{cliente_estado}}': cliente.estado,
        '{{cliente_cep}}': cliente.cep,
        '{{cliente_telefone}}': cliente.telefone,
        '{{cliente_email}}': cliente.email,
        
        # Sistema
        '{{consumo_mensal}}': f"{orcamento.consumo_mensal:.0f}",
        '{{potencia_sistema}}': f"{orcamento.potencia_sistema:.2f}",
        '{{quantidade_paineis}}': str(orcamento.quantidade_paineis),
        '{{potencia_painel}}': f"{orcamento.painel.potencia:.0f}",
        '{{potencia_inversor}}': f"{orcamento.inversor.potencia:.0f}",
        '{{geracao_mensal}}': f"{orcamento.geracao_mensal:.0f}",
        '{{geracao_anual}}': f"{orcamento.geracao_anual:.0f}",
        
        # Financeiro
        '{{valor_total}}': f"R$ {orcamento.valor_total:,.2f}",
        '{{valor_parcela}}': f"R$ {orcamento.valor_parcela:,.2f}",
        '{{quantidade_parcelas}}': str(orcamento.parcelas),
        '{{vida_util_sistema}}': "25",
        '{{economia_mensal}}': f"R$ {orcamento.economia_mensal:,.2f}",
        '{{economia_anual}}': f"R$ {orcamento.economia_anual:,.2f}",
        '{{payback}}': f"{orcamento.payback:.1f}",
        
        # Técnico
        '{{hsp}}': f"{orcamento.hsp:.1f}",
        '{{perdas_sistema}}': f"{orcamento.perdas * 100:.0f}",
        '{{degradacao_anual}}': "0,8",
        
        # Empresa
        '{{empresa_nome}}': "SunOps Energia Solar",
        '{{empresa_cnpj}}': "12.345.678/0001-90",
        '{{empresa_endereco}}': "Av. Paulista, 1000",
        '{{empresa_telefone}}': "(11) 3000-0000",
        '{{empresa_email}}': "contato@sunops.com.br",
        '{{empresa_site}}': "www.sunops.com.br",
        
        # Datas
        '{{data_proposta}}': datetime.now().strftime('%d/%m/%Y'),
        '{{validade_proposta}}': "30",
    }
    
    # Substituir em parágrafos
    for paragraph in doc.paragraphs:
        for key, value in dados.items():
            if key in paragraph.text:
                for run in paragraph.runs:
                    if key in run.text:
                        run.text = run.text.replace(key, value)
    
    # Substituir em tabelas
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for key, value in dados.items():
                        if key in paragraph.text:
                            for run in paragraph.runs:
                                if key in run.text:
                                    run.text = run.text.replace(key, value)
    
    # Salvar DOCX
    output_docx = f'media/propostas/proposta_{orcamento_id}.docx'
    os.makedirs(os.path.dirname(output_docx), exist_ok=True)
    doc.save(output_docx)
    
    # Converter para PDF (opcional)
    output_pdf = output_docx.replace('.docx', '.pdf')
    convert(output_docx, output_pdf)
    
    return output_pdf
```

## 📋 Checklist de Implementação

- [x] Converter PDF para DOCX
- [x] Adicionar chaves de template
- [x] Preservar formatação original
- [x] Documentar todas as chaves
- [ ] Integrar com backend Django
- [ ] Criar endpoint de geração
- [ ] Adicionar testes
- [ ] Implementar preview no frontend

## 🎨 Formatação Preservada

O template mantém toda a formatação original do PDF:
- ✅ Cores e fontes
- ✅ Logotipos e imagens
- ✅ Tabelas e layouts
- ✅ Espaçamentos e margens
- ✅ Cabeçalhos e rodapés

## 🔄 Próximos Passos

1. **Backend**: Criar view para gerar proposta
2. **Frontend**: Adicionar botão "Gerar Proposta Comercial"
3. **Testes**: Validar geração com dados reais
4. **Deploy**: Adicionar template ao repositório
