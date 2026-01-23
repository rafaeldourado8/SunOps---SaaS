from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from shared.infrastructure.database import Base


class PremissaModel(Base):
    __tablename__ = "premissas"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    categoria = Column(String(20), nullable=False)
    item = Column(String(255), nullable=False, unique=True)
    custo_unitario = Column(Float, nullable=False)
    margem_lucro = Column(Float, default=0.18)
    comissao = Column(Float, default=0.05)
    imposto = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class ConfiguracaoModel(Base):
    __tablename__ = "configuracoes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    montagem_por_painel = Column(Float, default=60.0)
    custo_projeto = Column(Float, default=400.0)
    margem_lucro_padrao = Column(Float, default=0.18)
    comissao_padrao = Column(Float, default=0.05)
    imposto_padrao = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
