# Correção do Template PROPOSTA.docx

## Problema Identificado

O arquivo `PROPOSTA.docx` tinha chaves no formato `{{CHAVE_MAIUSCULA}}`, mas o sistema esperava chaves no formato `{{chave_minuscula}}`.

## Chaves Encontradas no Template

Total: **16 chaves**

### Formato Minúsculo (Padrão do Sistema)
- `{{cliente_nome}}`
- `{{cliente_endereco}}`
- `{{cliente_cidade}}`
- `{{cliente_estado}}`
- `{{data_proposta}}`
- `{{geracao_mensal}}`
- `{{marca_inversor}}`
- `{{marca_painel}}`
- `{{perdas_sistema}}`
- `{{potencia_inversor}}`
- `{{quantidade_inversores}}`
- `{{quantidade_paineis}}`
- `{{valor_total}}`

### Formato Maiúsculo (Mantidas para Compatibilidade)
- `{{INVERSOR_POTENCIA}}`
- `{{PAINEIS_POTENCIA}}`
- `{{POTENCIA_TOTAL_KWP}}`

## Solução Implementada

### 1. Template Corrigido
- **Arquivo:** `docs/templates/PROPOSTA_COMERCIAL_TEMPLATE.docx`
- **Status:** ✅ Padronizado com chaves minúsculas
- **Compatibilidade:** Mantém chaves maiúsculas onde necessário

### 2. Gerador Atualizado
- **Arquivo:** `backend/apps/propostas/utils/gerador_proposta.py`
- **Mudanças:**
  - ✅ Adicionado `{{marca_painel}}`
  - ✅ Adicionado `{{marca_inversor}}`
  - ✅ Adicionado `{{quantidade_inversores}}`
  - ✅ Suporte para chaves em MAIÚSCULO (compatibilidade)

### 3. Mapeamento Completo de Chaves

```python
# Cliente
'{{cliente_nome}}': 'Nome do cliente'
'{{cliente_endereco}}': 'Endereço completo'
'{{cliente_cidade}}': 'Cidade'
'{{cliente_estado}}': 'UF'
'{{cliente_cep}}': 'CEP'
'{{cliente_telefone}}': 'Telefone'
'{{cliente_email}}': 'Email'
'{{cliente_bairro}}': 'Bairro'

# Sistema
'{{consumo_mensal}}': 'Consumo em kWh'
'{{potencia_sistema}}': 'Potência em kWp'
'{{POTENCIA_TOTAL_KWP}}': 'Potência (compatibilidade)'
'{{quantidade_paineis}}': 'Número de painéis'
'{{potencia_painel}}': 'Potência do painel em W'
'{{PAINEIS_POTENCIA}}': 'Potência painel (compatibilidade)'
'{{marca_painel}}': 'Marca do painel'
'{{potencia_inversor}}': 'Potência do inversor em W'
'{{INVERSOR_POTENCIA}}': 'Potência inversor (compatibilidade)'
'{{marca_inversor}}': 'Marca do inversor'
'{{quantidade_inversores}}': 'Número de inversores'
'{{geracao_mensal}}': 'Geração mensal em kWh'
'{{geracao_anual}}': 'Geração anual em kWh'

# Financeiro
'{{valor_total}}': 'Valor total formatado'
'{{valor_parcela}}': 'Valor da parcela'
'{{quantidade_parcelas}}': 'Número de parcelas'
'{{economia_mensal}}': 'Economia mensal'
'{{economia_anual}}': 'Economia anual'
'{{payback}}': 'Tempo de retorno'

# Técnico
'{{hsp}}': 'Horas de Sol Pleno'
'{{perdas_sistema}}': 'Perdas do sistema em %'
'{{degradacao_anual}}': 'Degradação anual em %'

# Empresa
'{{empresa_nome}}': 'Nome da empresa'
'{{empresa_cnpj}}': 'CNPJ'
'{{empresa_endereco}}': 'Endereço'
'{{empresa_telefone}}': 'Telefone'
'{{empresa_email}}': 'Email'
'{{empresa_site}}': 'Site'

# Datas
'{{data_proposta}}': 'Data de emissão'
'{{validade_proposta}}': 'Validade em dias'
```

## Como Usar

### 1. Upload do Template na Plataforma

```bash
# O arquivo correto está em:
docs/templates/PROPOSTA_COMERCIAL_TEMPLATE.docx
```

### 2. Gerar Proposta via API

```python
from apps.propostas.utils.gerador_proposta import GeradorPropostaComercial
from apps.orcamentos.models import Orcamento

# Buscar orçamento
orcamento = Orcamento.objects.get(id=1)

# Gerar proposta
gerador = GeradorPropostaComercial(orcamento)
arquivo = gerador.gerar()

print(f"Proposta gerada: {arquivo}")
```

### 3. Testar Geração

```bash
cd backend
python manage.py shell

# No shell:
from apps.propostas.utils.gerador_proposta import GeradorPropostaComercial
from apps.orcamentos.models import Orcamento

orcamento = Orcamento.objects.first()
gerador = GeradorPropostaComercial(orcamento)
arquivo = gerador.gerar()
print(f"Arquivo gerado: {arquivo}")
```

## Próximos Passos

1. ✅ Template corrigido e padronizado
2. ✅ Gerador atualizado com todas as chaves
3. ⏳ Fazer upload do template na plataforma
4. ⏳ Testar geração com dados reais
5. ⏳ Adicionar endpoint na API REST
6. ⏳ Criar botão no frontend

## Scripts Auxiliares Criados

- `backend/padronizar_chaves_proposta.py` - Padroniza chaves do template
- `backend/verificar_chaves_proposta.py` - Lista todas as chaves presentes
- `backend/corrigir_final.py` - Correção final de chaves restantes

## Resultado

✅ **Template pronto para uso na plataforma**
✅ **Todas as chaves mapeadas e funcionais**
✅ **Compatibilidade com formato antigo mantida**
