"""
Celery Task: Alerta de Cotação Segunda-feira
"""
from celery_app.celeryconfig import app
from datetime import datetime


@app.task
def alerta_cotacao_segunda():
    """
    Task executada toda segunda-feira para alertar sobre cotações expiradas
    """
    hoje = datetime.now()
    
    # Verifica se é segunda-feira (0 = segunda)
    if hoje.weekday() != 0:
        return "Não é segunda-feira"
    
    # TODO: Buscar cotações expiradas e enviar alertas
    print(f"[ALERTA] Verificando cotações expiradas em {hoje}")
    
    return f"Alerta enviado em {hoje}"
