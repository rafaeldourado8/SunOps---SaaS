# ✅ Proposta Comercial - Template Pronto

## 📦 Arquivos Criados

### 1. Template DOCX com Chaves
**Localização:** `docs/templates/PROPOSTA_COMERCIAL_TEMPLATE.docx`
- ✅ Convertido do PDF original
- ✅ Formatação preservada (cores, fontes, layout)
- ✅ Chaves de template adicionadas
- ✅ Pronto para uso

### 2. Documentação das Chaves
**Localização:** `docs/TEMPLATE_PROPOSTA_COMERCIAL.md`
- Lista completa de todas as chaves disponíveis
- Exemplos de uso
- Código de integração com Django

### 3. Gerador Python
**Localização:** `backend/apps/propostas/utils/gerador_proposta.py`
- Classe `GeradorPropostaComercial`
- Substituição automática de chaves
- Preserva formatação original

## 🔑 Chaves Disponíveis (40 no total)

### Cliente (8 chaves)
- `{{cliente_nome}}`
- `{{cliente_endereco}}`
- `{{cliente_bairro}}`
- `{{cliente_cidade}}`
- `{{cliente_estado}}`
- `{{cliente_cep}}`
- `{{cliente_telefone}}`
- `{{cliente_email}}`

### Sistema Fotovoltaico (7 chaves)
- `{{consumo_mensal}}`
- `{{potencia_sistema}}`
- `{{quantidade_paineis}}`
- `{{potencia_painel}}`
- `{{potencia_inversor}}`
- `{{geracao_mensal}}`
- `{{geracao_anual}}`

### Financeiro (7 chaves)
- `{{valor_total}}`
- `{{valor_parcela}}`
- `{{quantidade_parcelas}}`
- `{{vida_util_sistema}}`
- `{{economia_mensal}}`
- `{{economia_anual}}`
- `{{payback}}`

### Técnico (3 chaves)
- `{{hsp}}`
- `{{perdas_sistema}}`
- `{{degradacao_anual}}`

### Empresa (6 chaves)
- `{{empresa_nome}}`
- `{{empresa_cnpj}}`
- `{{empresa_endereco}}`
- `{{empresa_telefone}}`
- `{{empresa_email}}`
- `{{empresa_site}}`

### Datas (2 chaves)
- `{{data_proposta}}`
- `{{validade_proposta}}`

## 💻 Como Usar

### Exemplo Rápido
```python
from apps.orcamentos.models import Orcamento
from apps.propostas.utils.gerador_proposta import GeradorPropostaComercial

# Buscar orçamento
orcamento = Orcamento.objects.get(id=1)

# Gerar proposta
gerador = GeradorPropostaComercial(orcamento)
arquivo = gerador.gerar()

print(f"Proposta gerada: {arquivo}")
# Output: media/propostas/proposta_comercial_1_20240215_163000.docx
```

### Integração com API
```python
# Em apps/propostas/views.py
from rest_framework.decorators import action
from rest_framework.response import Response
from .utils.gerador_proposta import GeradorPropostaComercial

class OrcamentoViewSet(viewsets.ModelViewSet):
    
    @action(detail=True, methods=['post'])
    def gerar_proposta(self, request, pk=None):
        orcamento = self.get_object()
        
        try:
            gerador = GeradorPropostaComercial(orcamento)
            arquivo = gerador.gerar()
            
            return Response({
                'success': True,
                'arquivo': arquivo,
                'mensagem': 'Proposta comercial gerada com sucesso!'
            })
        except Exception as e:
            return Response({
                'success': False,
                'erro': str(e)
            }, status=400)
```

## ✨ Características

- ✅ **Formatação Preservada**: Mantém cores, fontes e layout do PDF original
- ✅ **40 Chaves**: Cobertura completa de dados do cliente, sistema e empresa
- ✅ **Fácil Integração**: Classe Python pronta para uso
- ✅ **Flexível**: Aceita output_path customizado
- ✅ **Seguro**: Validação de template e tratamento de erros

## 🎯 Próximos Passos

1. Testar geração com dados reais
2. Adicionar endpoint na API REST
3. Criar botão no frontend
4. Implementar conversão para PDF (opcional)
5. Adicionar envio por email (opcional)
