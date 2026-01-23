from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from shared.infrastructure.database import Base

class TemplateModel(Base):
    __tablename__ = "templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tipo = Column(String(50), nullable=False)
    nome = Column(String(255), nullable=False)
    arquivo_path = Column(String(255), nullable=False)
    vendedor_id = Column(UUID(as_uuid=True), nullable=False)
    ativo = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)