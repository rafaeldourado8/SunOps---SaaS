import json
import re

def extrair_dados(linha):
    """Extrai fabricante, modelo e potência de uma linha"""
    partes = linha.strip().split()
    if len(partes) < 2:
        return None
    
    # Busca números que podem ser potência
    potencia = None
    for parte in partes:
        nums = re.findall(r'\d+', parte)
        if nums:
            n = int(nums[0])
            if 50 < n < 10000:
                potencia = n
                break
    
    return {
        "fabricante": partes[0],
        "nome_modelo": ' '.join(partes[1:]),
        "potencia_w": potencia
    }

def converter(arquivo_txt):
    """Converte TXT para JSON"""
    with open(arquivo_txt, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    dados = []
    for linha in linhas:
        if linha.strip():
            item = extrair_dados(linha)
            if item:
                dados.append(item)
    
    arquivo_json = arquivo_txt.replace('.txt', '.json')
    with open(arquivo_json, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
    
    print(f"✓ {len(dados)} itens → {arquivo_json}")
    return dados

# Uso
if __name__ == "__main__":
    converter('dados.txt')