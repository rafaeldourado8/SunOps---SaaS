from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from ..domain.template import Template, TipoTemplate
from .models import TemplateModel


class SQLAlchemyTemplateRepository:
    
    def __init__(self, db: Session):
        self.db = db
    
    def save(self, entity: Template) -> Template:
        model = self.db.query(TemplateModel).filter(TemplateModel.id == entity.id).first()
        
        if model:
            model.nome = entity.nome
            model.ativo = entity.ativo
            model.tipo = entity.tipo.value
            model.arquivo_path = entity.arquivo_path
        else:
            model = TemplateModel(
                id=entity.id,
                tipo=entity.tipo.value,
                nome=entity.nome,
                arquivo_path=entity.arquivo_path,
                vendedor_id=entity.vendedor_id,
                ativo=entity.ativo
            )
            self.db.add(model)
        
        self.db.commit()
        self.db.refresh(model)
        return entity
    
    def find_by_id(self, id: UUID) -> Optional[Template]:
        model = self.db.query(TemplateModel).filter(TemplateModel.id == id).first()
        return self._to_entity(model) if model else None
    
    def find_by_vendedor(self, vendedor_id: UUID) -> List[Template]:
        models = self.db.query(TemplateModel).filter(TemplateModel.vendedor_id == vendedor_id, TemplateModel.ativo == True).all()
        return [self._to_entity(m) for m in models]
    
    def find_all(self) -> List[Template]:
        models = self.db.query(TemplateModel).filter(TemplateModel.ativo == True).all()
        return [self._to_entity(m) for m in models]
    
    def delete(self, id: UUID) -> None:
        model = self.db.query(TemplateModel).filter(TemplateModel.id == id).first()
        if model:
            model.ativo = False
            self.db.commit()
    
    def _to_entity(self, model: TemplateModel) -> Template:
        return Template(
            id=model.id,
            tipo=TipoTemplate(model.tipo),
            nome=model.nome,
            arquivo_path=model.arquivo_path,
            vendedor_id=str(model.vendedor_id),
            ativo=model.ativo,
            created_at=model.created_at,
            updated_at=model.updated_at
        )