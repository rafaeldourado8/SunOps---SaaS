from sqlalchemy.orm import Session
from shared.infrastructure.database import SessionLocal
from premissas.infrastructure.models import PremissaModel, ConfiguracaoModel
import uuid

def seed_premissas():
    db = SessionLocal()
    
    premissas = [
        {"categoria": "KIT", "item": "Valor do Kit", "custo_unitario": 7160.00},
        {"categoria": "KIT", "item": "Painel", "custo_unitario": 0.00},
        {"categoria": "KIT", "item": "Inversor", "custo_unitario": 0.00},
        {"categoria": "SERVICO", "item": "Projeto", "custo_unitario": 400.00},
        {"categoria": "SERVICO", "item": "Montagem Painel", "custo_unitario": 60.00},
        {"categoria": "CUSTO", "item": "Materiais Elétricos", "custo_unitario": 600.00},
        {"categoria": "CUSTO", "item": "Hospedagem", "custo_unitario": 0.00},
        {"categoria": "CUSTO", "item": "Estrutura Solo", "custo_unitario": 0.00},
        {"categoria": "CUSTO", "item": "Frete", "custo_unitario": 0.00},
        {"categoria": "CUSTO", "item": "Locomoção", "custo_unitario": 0.00},
        {"categoria": "CUSTO", "item": "Indicação", "custo_unitario": 0.00},
        {"categoria": "CUSTO", "item": "Padrão", "custo_unitario": 0.00},
        {"categoria": "CUSTO", "item": "Deslocamento", "custo_unitario": 0.00},
        {"categoria": "CUSTO", "item": "Arredondamento", "custo_unitario": 0.00},
    ]
    
    for p in premissas:
        existing = db.query(PremissaModel).filter(PremissaModel.item == p["item"]).first()
        if not existing:
            model = PremissaModel(
                id=uuid.uuid4(),
                categoria=p["categoria"],
                item=p["item"],
                custo_unitario=p["custo_unitario"],
                margem_lucro=0.18,
                comissao=0.05,
                imposto=0.0
            )
            db.add(model)
    
    config = db.query(ConfiguracaoModel).first()
    if not config:
        config = ConfiguracaoModel(
            id=uuid.uuid4(),
            montagem_por_painel=60.0,
            custo_projeto=400.0,
            margem_lucro_padrao=0.18,
            comissao_padrao=0.05,
            imposto_padrao=0.0
        )
        db.add(config)
    
    db.commit()
    db.close()
    print("Premissas iniciais criadas!")

if __name__ == "__main__":
    seed_premissas()
