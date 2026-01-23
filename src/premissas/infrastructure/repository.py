from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from ..domain.entities import Premissa, CategoriaProduto, ConfiguracaoGlobal
from ..domain.repository import IPremissaRepository, IConfiguracaoRepository
from .models import PremissaModel, ConfiguracaoModel
from shared.domain.value_objects import Money


class SQLAlchemyPremissaRepository(IPremissaRepository):
    
    def __init__(self, db: Session):
        self.db = db
    
    def save(self, entity: Premissa) -> Premissa:
        model = self.db.query(PremissaModel).filter(PremissaModel.id == entity.id).first()
        
        if model:
            model.custo_unitario = entity.custo_unitario.value
            model.margem_lucro = entity.margem_lucro
            model.comissao = entity.comissao
            model.imposto = entity.imposto
        else:
            model = PremissaModel(
                id=entity.id,
                categoria=entity.categoria.value,
                item=entity.item,
                custo_unitario=entity.custo_unitario.value,
                margem_lucro=entity.margem_lucro,
                comissao=entity.comissao,
                imposto=entity.imposto
            )
            self.db.add(model)
        
        self.db.commit()
        self.db.refresh(model)
        return entity
    
    def find_by_id(self, id: UUID) -> Optional[Premissa]:
        model = self.db.query(PremissaModel).filter(PremissaModel.id == id).first()
        return self._to_entity(model) if model else None
    
    def find_by_item(self, item: str) -> Optional[Premissa]:
        model = self.db.query(PremissaModel).filter(PremissaModel.item == item).first()
        return self._to_entity(model) if model else None
    
    def find_by_categoria(self, categoria: CategoriaProduto) -> List[Premissa]:
        models = self.db.query(PremissaModel).filter(PremissaModel.categoria == categoria.value).all()
        return [self._to_entity(m) for m in models]
    
    def find_all(self) -> List[Premissa]:
        models = self.db.query(PremissaModel).all()
        return [self._to_entity(m) for m in models]
    
    def delete(self, id: UUID) -> None:
        self.db.query(PremissaModel).filter(PremissaModel.id == id).delete()
        self.db.commit()
    
    def _to_entity(self, model: PremissaModel) -> Premissa:
        return Premissa(
            id=model.id,
            categoria=CategoriaProduto(model.categoria),
            item=model.item,
            custo_unitario=Money(model.custo_unitario),
            margem_lucro=model.margem_lucro,
            comissao=model.comissao,
            imposto=model.imposto,
            created_at=model.created_at,
            updated_at=model.updated_at
        )


class SQLAlchemyConfiguracaoRepository(IConfiguracaoRepository):
    
    def __init__(self, db: Session):
        self.db = db
    
    def save(self, entity: ConfiguracaoGlobal) -> ConfiguracaoGlobal:
        model = self.db.query(ConfiguracaoModel).first()
        
        if model:
            model.montagem_por_painel = entity.montagem_por_painel.value
            model.custo_projeto = entity.custo_projeto.value
            model.margem_lucro_padrao = entity.margem_lucro_padrao
            model.comissao_padrao = entity.comissao_padrao
            model.imposto_padrao = entity.imposto_padrao
        else:
            model = ConfiguracaoModel(
                montagem_por_painel=entity.montagem_por_painel.value,
                custo_projeto=entity.custo_projeto.value,
                margem_lucro_padrao=entity.margem_lucro_padrao,
                comissao_padrao=entity.comissao_padrao,
                imposto_padrao=entity.imposto_padrao
            )
            self.db.add(model)
        
        self.db.commit()
        self.db.refresh(model)
        return entity
    
    def get_configuracao_atual(self) -> ConfiguracaoGlobal:
        model = self.db.query(ConfiguracaoModel).first()
        
        if not model:
            config = ConfiguracaoGlobal()
            return self.save(config)
        
        return ConfiguracaoGlobal(
            id=model.id,
            montagem_por_painel=Money(model.montagem_por_painel),
            custo_projeto=Money(model.custo_projeto),
            margem_lucro_padrao=model.margem_lucro_padrao,
            comissao_padrao=model.comissao_padrao,
            imposto_padrao=model.imposto_padrao,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def find_by_id(self, id: UUID) -> Optional[ConfiguracaoGlobal]:
        return self.get_configuracao_atual()
    
    def find_all(self) -> List[ConfiguracaoGlobal]:
        return [self.get_configuracao_atual()]
    
    def delete(self, id: UUID) -> None:
        pass
