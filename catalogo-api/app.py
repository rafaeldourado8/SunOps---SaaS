from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_caching import Cache  # 1. Importar
import json
import os

app = Flask(__name__)
CORS(app)  # Permite requisições do frontend

# 2. Configuração do Cache
#    (Usando variáveis de ambiente. 'redis' é o host padrão do Docker Compose)
app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_HOST"] = os.environ.get('REDIS_HOST', 'localhost')
app.config["CACHE_REDIS_PORT"] = os.environ.get('REDIS_PORT', 6379)
app.config["CACHE_REDIS_DB"] = 0
app.config["CACHE_DEFAULT_TIMEOUT"] = 3600  # Cache de 1 hora (em segundos)

cache = Cache(app)  # 3. Inicializar o cache

# Carrega os JSONs na inicialização (1x só)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def load_json(filename):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

# Carrega os dados em memória
try:
    MODULOS = load_json('catalogo_modulos.json')
    INVERSORES = load_json('catalogo_inversores.json')
    print(f"✓ Carregados {len(MODULOS)} módulos e {len(INVERSORES)} inversores")
except Exception as e:
    print(f"✗ Erro ao carregar catálogos: {e}")
    MODULOS = []
    INVERSORES = []

# ============= ROTAS =============

@app.route('/health', methods=['GET'])
@cache.cached(timeout=60)  # 4. Adicionar decorator de cache
def health():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'modulos': len(MODULOS),
        'inversores': len(INVERSORES)
    })

@app.route('/modulos', methods=['GET'])
@cache.cached(query_string=True)  # 4. Cachear baseado na query (fabricante, limit, etc)
def get_modulos():
    """Retorna lista de módulos com filtros opcionais"""
    fabricante = request.args.get('fabricante', '').upper()
    potencia_min = request.args.get('potencia_min', type=int)
    potencia_max = request.args.get('potencia_max', type=int)
    limit = request.args.get('limit', default=100, type=int)
    search = request.args.get('search', '').upper()
    
    resultado = MODULOS
    
    if fabricante:
        resultado = [m for m in resultado if fabricante in m.get('fabricante', '').upper()]
    
    if potencia_min:
        resultado = [m for m in resultado if m.get('potencia_w', 0) >= potencia_min]
    
    if potencia_max:
        resultado = [m for m in resultado if m.get('potencia_w', 0) <= potencia_max]
    
    if search:
        resultado = [m for m in resultado 
                    if search in m.get('nome_modelo', '').upper() 
                    or search in m.get('fabricante', '').upper()]
    
    resultado = resultado[:limit]
    
    return jsonify({
        'total': len(resultado),
        'data': resultado
    })

@app.route('/inversores', methods=['GET'])
@cache.cached(query_string=True)  # 4. Cachear baseado na query
def get_inversores():
    """Retorna lista de inversores com filtros opcionais"""
    fabricante = request.args.get('fabricante', '').upper()
    potencia_min = request.args.get('potencia_min', type=int)
    potencia_max = request.args.get('potencia_max', type=int)
    limit = request.args.get('limit', default=100, type=int)
    search = request.args.get('search', '').upper()
    
    resultado = INVERSORES
    
    if fabricante:
        resultado = [i for i in resultado if fabricante in i.get('fabricante', '').upper()]
    
    if potencia_min:
        resultado = [i for i in resultado if i.get('potencia_w', 0) >= potencia_min]
    
    if potencia_max:
        resultado = [i for i in resultado if i.get('potencia_w', 0) <= potencia_max]
    
    if search:
        resultado = [i for i in resultado 
                    if search in i.get('nome_modelo', '').upper() 
                    or search in i.get('fabricante', '').upper()]
    
    resultado = resultado[:limit]
    
    return jsonify({
        'total': len(resultado),
        'data': resultado
    })

@app.route('/fabricantes', methods=['GET'])
@cache.cached(query_string=True)  # 4. Cachear baseado na query
def get_fabricantes():
    """Retorna lista de fabricantes únicos"""
    tipo = request.args.get('tipo', 'modulos')
    
    dados = MODULOS if tipo == 'modulos' else INVERSORES
    fabricantes = sorted(set(item.get('fabricante', '') for item in dados))
    
    return jsonify({
        'total': len(fabricantes),
        'data': fabricantes
    })

@app.route('/search', methods=['GET'])
@cache.cached(query_string=True)  # 4. Cachear baseado na query
def search():
    """Busca em todos os catálogos"""
    query = request.args.get('q', '').upper()
    limit = request.args.get('limit', default=50, type=int)
    
    if not query or len(query) < 2:
        return jsonify({'error': 'Query deve ter pelo menos 2 caracteres'}), 400
    
    modulos_result = [m for m in MODULOS 
                      if query in m.get('nome_modelo', '').upper() 
                      or query in m.get('fabricante', '').upper()][:limit]
    
    inversores_result = [i for i in INVERSORES 
                        if query in i.get('nome_modelo', '').upper() 
                        or query in i.get('fabricante', '').upper()][:limit]
    
    return jsonify({
        'query': query,
        'modulos': {'total': len(modulos_result), 'data': modulos_result},
        'inversores': {'total': len(inversores_result), 'data': inversores_result}
    })

# Rota bônus para limpar o cache se você atualizar os JSONs
@app.route('/clear-cache', methods=['POST'])
def clear_cache_route():
    cache.clear()
    print("✓ Cache limpo manualmente.")
    return jsonify({"message": "Cache limpo com sucesso!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)