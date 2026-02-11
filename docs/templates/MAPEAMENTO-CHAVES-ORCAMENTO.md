# MAPEAMENTO DE CHAVES - TEMPLATE DE ORÇAMENTO

## Como usar:
No seu template DOCX, use as chaves entre chaves duplas: {{CHAVE}}
Exemplo: {{NOME_CLIENTE}} será substituído pelo nome do cliente

---

## 📋 DADOS DO ORÇAMENTO

{{NUMERO_ORCAMENTO}}          - Número do orçamento (ex: ORC-0001)
{{DATA_ORCAMENTO}}             - Data de criação (ex: 11/02/2026)
{{DATA_CRIACAO}}               - Alias para DATA_ORCAMENTO
{{DATA_VALIDADE}}              - Data de validade do orçamento

---

## 👤 DADOS DO CLIENTE

{{NOME_CLIENTE}}               - Nome completo do cliente
{{CLIENTE_NOME}}               - Alias para NOME_CLIENTE
{{CPF_CNPJ}}                   - CPF ou CNPJ
{{TELEFONE}}                   - Telefone do cliente
{{EMAIL}}                      - E-mail do cliente
{{ENDERECO}}                   - Endereço completo
{{CLIENTE_ENDERECO}}           - Alias para ENDERECO
{{CIDADE}}                     - Cidade
{{CLIENTE_CIDADE}}             - Alias para CIDADE
{{ESTADO}}                     - Estado (UF)
{{CLIENTE_ESTADO}}             - Alias para ESTADO

---

## ⚡ SISTEMA FOTOVOLTAICO

{{POTENCIA_KWP}}               - Potência total em kWp (ex: 8.40)
{{POTENCIA_TOTAL_KWP}}         - Alias para POTENCIA_KWP
{{GERACAO_MENSAL}}             - Geração mensal estimada em kWh
{{GERACAO_ANUAL}}              - Geração anual estimada em kWh

---

## 🔆 PAINÉIS SOLARES

{{MARCA_PAINEL}}               - Marca do painel (ex: Canadian Solar)
{{PAINEIS_MARCA}}              - Alias para MARCA_PAINEL
{{POTENCIA_PAINEL}}            - Potência unitária em W (ex: 550)
{{PAINEIS_POTENCIA}}           - Alias para POTENCIA_PAINEL
{{QUANTIDADE_PAINEIS}}         - Quantidade de painéis (ex: 16)
{{PAINEIS_QTD}}                - Alias para QUANTIDADE_PAINEIS

---

## 🔌 INVERSORES

{{MARCA_INVERSOR}}             - Marca do inversor (ex: Growatt)
{{INVERSOR_MARCA}}             - Alias para MARCA_INVERSOR
{{POTENCIA_INVERSOR}}          - Potência em W (ex: 8000)
{{INVERSOR_POTENCIA}}          - Alias para POTENCIA_INVERSOR
{{POTENCIA_INVERSOR_KW}}       - Potência em kW (ex: 8.0)
{{QUANTIDADE_INVERSORES}}      - Quantidade de inversores (ex: 1)
{{INVERSOR_QTD}}               - Alias para QUANTIDADE_INVERSORES

---

## 🏗️ ESTRUTURA

{{TIPO_ESTRUTURA}}             - Tipo de estrutura (ex: Fibrocimento, Metálica, Solo)

---

## 💰 VALORES

{{VALOR_KIT}}                  - Valor do kit (painéis + inversor)
{{VALOR_ESTRUTURA}}            - Valor da estrutura de fixação
{{VALOR_MATERIAL_ELETRICO}}    - Valor dos materiais elétricos
{{VALOR_PROJETO}}              - Valor do projeto
{{VALOR_MONTAGEM}}             - Valor da montagem
{{VALOR_TOTAL}}                - Valor total (custo)
{{VALOR_FINAL}}                - Valor final de venda

---

## 💳 PAGAMENTO

{{FORMA_PAGAMENTO}}            - Forma de pagamento (ex: À vista, 12x de R$ 1.200,00)
{{TAXA_JUROS}}                 - Taxa de juros aplicada (ex: 2.5%)

---

## 👨‍💼 VENDEDOR

{{NOME_VENDEDOR}}              - Nome do vendedor
{{TELEFONE_VENDEDOR}}          - Telefone do vendedor
{{EMAIL_VENDEDOR}}             - E-mail do vendedor

---

## 📊 PREMISSAS TÉCNICAS

{{HSP}}                        - Horas de Sol Pico (ex: 4.50)
{{PERDA_SISTEMA}}              - Perda do sistema (ex: 20.0%)

---

## 💡 EXEMPLO DE USO NO TEMPLATE:

```
PROPOSTA COMERCIAL Nº {{NUMERO_ORCAMENTO}}

Cliente: {{NOME_CLIENTE}}
Cidade: {{CIDADE}} - {{ESTADO}}
Data: {{DATA_ORCAMENTO}}

SISTEMA PROPOSTO:
- Potência: {{POTENCIA_KWP}} kWp
- Painéis: {{QUANTIDADE_PAINEIS}}x {{MARCA_PAINEL}} {{POTENCIA_PAINEL}}W
- Inversor: {{QUANTIDADE_INVERSORES}}x {{MARCA_INVERSOR}} {{POTENCIA_INVERSOR_KW}}kW
- Estrutura: {{TIPO_ESTRUTURA}}

GERAÇÃO ESTIMADA:
- Mensal: {{GERACAO_MENSAL}} kWh
- Anual: {{GERACAO_ANUAL}} kWh

INVESTIMENTO:
Valor Total: {{VALOR_FINAL}}
Forma de Pagamento: {{FORMA_PAGAMENTO}}

Vendedor: {{NOME_VENDEDOR}}
Contato: {{TELEFONE_VENDEDOR}}
```

---

## 📝 NOTAS IMPORTANTES:

1. Use SEMPRE chaves duplas: {{CHAVE}}
2. As chaves são case-sensitive (maiúsculas/minúsculas importam)
3. Valores monetários já vêm formatados (R$ 1.234,56)
4. Datas já vêm formatadas (DD/MM/AAAA)
5. Percentuais já vêm com o símbolo %
6. Você pode usar os aliases (nomes alternativos) das chaves

---

## 🎨 DICAS DE FORMATAÇÃO:

- Mantenha a formatação do Word (negrito, cores, tamanhos)
- A substituição preserva a formatação original
- Use tabelas para organizar informações
- Adicione imagens e logotipos normalmente
- O template será convertido para PDF automaticamente

---

Criado em: 11/02/2026
Versão: 1.0
