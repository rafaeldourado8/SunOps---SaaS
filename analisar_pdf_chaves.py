import re

# Ler o PDF como texto (manualmente copie o conteúdo do PDF aqui)
# Ou use uma ferramenta online para extrair o texto

# Lista de chaves esperadas no template
chaves_esperadas = [
    'NUMERO_ORCAMENTO', 'DATA_ORCAMENTO', 'DATA_CRIACAO', 'DATA_VALIDADE',
    'NOME_CLIENTE', 'CLIENTE_NOME', 'CPF_CNPJ', 'TELEFONE', 'EMAIL',
    'ENDERECO', 'CLIENTE_ENDERECO', 'CIDADE', 'CLIENTE_CIDADE',
    'ESTADO', 'CLIENTE_ESTADO', 'POTENCIA_KWP', 'POTENCIA_TOTAL_KWP',
    'GERACAO_MENSAL', 'GERACAO_ANUAL', 'MARCA_PAINEL', 'PAINEIS_MARCA',
    'POTENCIA_PAINEL', 'PAINEIS_POTENCIA', 'QUANTIDADE_PAINEIS', 'PAINEIS_QTD',
    'MARCA_INVERSOR', 'INVERSOR_MARCA', 'POTENCIA_INVERSOR', 'INVERSOR_POTENCIA',
    'POTENCIA_INVERSOR_KW', 'QUANTIDADE_INVERSORES', 'INVERSOR_QTD',
    'TIPO_ESTRUTURA', 'VALOR_KIT', 'VALOR_ESTRUTURA', 'VALOR_MATERIAL_ELETRICO',
    'VALOR_PROJETO', 'VALOR_MONTAGEM', 'VALOR_TOTAL', 'VALOR_FINAL',
    'FORMA_PAGAMENTO', 'TAXA_JUROS', 'NOME_VENDEDOR', 'TELEFONE_VENDEDOR',
    'EMAIL_VENDEDOR', 'HSP', 'PERDA_SISTEMA'
]

# Simular texto do PDF (substitua pelo texto real extraído)
texto_pdf = """
Cole aqui o texto extraído do PDF Orcamento_ORC-0001.pdf
"""

# Encontrar chaves não substituídas (ainda com {{CHAVE}})
chaves_nao_substituidas = re.findall(r'\{\{([A-Z_]+)\}\}', texto_pdf)

if chaves_nao_substituidas:
    print("🔴 CHAVES NÃO SUBSTITUÍDAS NO PDF:")
    for chave in set(chaves_nao_substituidas):
        print(f"  - {{{{chave}}}}")
    print(f"\nTotal: {len(set(chaves_nao_substituidas))} chaves não substituídas")
else:
    print("✅ Todas as chaves foram substituídas corretamente!")

print("\n" + "="*60)
print("CHAVES ESPERADAS NO SISTEMA:")
for chave in chaves_esperadas:
    print(f"  - {chave}")
