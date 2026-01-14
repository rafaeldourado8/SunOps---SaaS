from celery_app.celeryconfig import app


@app.task
def exemplo_task(x, y):
    """Task exemplo para testar Celery"""
    return x + y


@app.task
def enviar_email_task(destinatario: str, assunto: str, corpo: str):
    """Task para enviar emails (placeholder)"""
    print(f"Enviando email para {destinatario}: {assunto}")
    return True
