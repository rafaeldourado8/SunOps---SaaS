from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from ..domain.entities import Proposta, StatusProposta, ItemProposta, Desconto
from ..domain.repository import IPropostaRepository
from .models import PropostaModel
from shared.domain.value_objects import Money


class SQLAlchemyPropostaRepository(IPropostaRepository):
    
    def __init__(self, db: Session):
        self.db = db
    
    def save(self, entity: Proposta) -> Proposta:
        model = self.db.query(PropostaModel).filter(PropostaModel.id == entity.id).first()
        
        if model:
            self._update_model(model, entity)
        else:
            model = self._to_model(entity)
            self.db.add(model)
        
        self.db.commit()
        self.db.refresh(model)
        return entity
    
    def find_by_id(self, id: UUID) -> Optional[Proposta]:
        model = self.db.query(PropostaModel).filter(PropostaModel.id == id).first()
        return self._to_entity(model) if model else None
    
    def find_by_vendedor(self, vendedor_id: UUID) -> List[Proposta]:
        models = self.db.query(PropostaModel).filter(PropostaModel.vendedor_id == vendedor_id).all()
        return [self._to_entity(m) for m in models]
    
    def find_by_cliente(self, cliente_id: UUID) -> List[Proposta]:
        models = self.db.query(PropostaModel).filter(PropostaModel.cliente_id == cliente_id).all()
        return [self._to_entity(m) for m in models]
    
    def find_by_status(self, status: StatusProposta) -> List[Proposta]:
        models = self.db.query(PropostaModel).filter(PropostaModel.status == status.value).all()
        return [self._to_entity(m) for m in models]
    
    def find_all(self) -> List[Proposta]:
        models = self.db.query(PropostaModel).all()
        return [self._to_entity(m) for m in models]
    
    def delete(self, id: UUID) -> None:
        self.db.query(PropostaModel).filter(PropostaModel.id == id).delete()
        self.db.commit()
    
    def _to_model(self, entity: Proposta) -> PropostaModel:
        # Serializa lista de itens
        itens_json = [
            {
                'nome': i.nome, 
                'quantidade': i.quantidade, 
                'preco_unitario': i.preco_unitario.value, 
                'custo_unitario': i.custo_unitario.value
            } for i in entity.itens
        ]
        
        # Serializa desconto
        desconto_json = None
        if entity.desconto:
            desconto_json = {
                'valor': entity.desconto.valor.value, 
                'motivo': entity.desconto.motivo, 
                'solicitante_id': str(entity.desconto.solicitante_id),
                'aprovador_id': str(entity.desconto.aprovador_id) if entity.desconto.aprovador_id else None,
                'feedback': entity.desconto.feedback
            }
        
        return PropostaModel(
            id=entity.id, 
            vendedor_id=entity.vendedor_id, 
            cliente_id=entity.cliente_id, 
            potencia_sistema_kwp=entity.potencia_sistema_kwp, 
            status=entity.status.value, 
            payback_anos=entity.payback_anos, 
            itens=itens_json, 
            desconto=desconto_json
        )
    
    def _update_model(self, model: PropostaModel, entity: Proposta):
        model.status = entity.status.value
        model.potencia_sistema_kwp = entity.potencia_sistema_kwp
        model.payback_anos = entity.payback_anos
        
        model.itens = [
            {
                'nome': i.nome, 
                'quantidade': i.quantidade, 
                'preco_unitario': i.preco_unitario.value, 
                'custo_unitario': i.custo_unitario.value
            } for i in entity.itens
        ]
        
        if entity.desconto:
            model.desconto = {
                'valor': entity.desconto.valor.value, 
                'motivo': entity.desconto.motivo, 
                'solicitante_id': str(entity.desconto.solicitante_id),
                'aprovador_id': str(entity.desconto.aprovador_id) if entity.desconto.aprovador_id else None,
                'feedback': entity.desconto.feedback
            }
        else:
            model.desconto = None
    
    def _to_entity(self, model: PropostaModel) -> Proposta:
        # Deserializa itens
        itens = [
            ItemProposta(
                nome=i['nome'], 
                quantidade=i['quantidade'], 
                preco_unitario=Money(i['preco_unitario']), 
                custo_unitario=Money(i['custo_unitario'])
            ) for i in model.itens
        ]
        
        # Deserializa desconto
        desconto = None
        if model.desconto:
            desconto = Desconto(
                valor=Money(model.desconto['valor']), 
                motivo=model.desconto['motivo'], 
                solicitante_id=UUID(model.desconto['solicitante_id']),
                aprovador_id=UUID(model.desconto['aprovador_id']) if model.desconto.get('aprovador_id') else None,
                feedback=model.desconto.get('feedback')
            )
        
        return Proposta(
            id=model.id, 
            vendedor_id=model.vendedor_id, 
            cliente_id=model.cliente_id, 
            potencia_sistema_kwp=model.potencia_sistema_kwp, 
            itens=itens, 
            status=StatusProposta(model.status), 
            desconto=desconto, 
            payback_anos=model.payback_anos, 
            created_at=model.created_at, 
            updated_at=model.updated_at
        )