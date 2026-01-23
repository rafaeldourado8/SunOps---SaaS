from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime

from shared.infrastructure.database import Base


class PropostaModel(Base):
    __tablename__ = "propostas"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vendedor_id = Column(UUID(as_uuid=True), nullable=False)
    cliente_id = Column(UUID(as_uuid=True), nullable=False)
    potencia_sistema_kwp = Column(Float, nullable=False)
    status = Column(String(20), default="RASCUNHO")
    payback_anos = Column(Float, nullable=True)
    
    # Armazena itens como lista de objetos JSON: [{nome, qtd, preco, custo}, ...]
    itens = Column(JSONB, default=[])
    
    # Armazena desconto como objeto JSON: {valor, motivo, solicitante_id, ...}
    desconto = Column(JSONB, nullable=True)
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)