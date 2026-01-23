from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from shared.infrastructure.database import Base


class UsuarioModel(Base):
    __tablename__ = "usuarios"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    tipo = Column(String(20), default="VENDEDOR")
    ativo = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    estados = relationship("UsuarioEstadoModel", back_populates="usuario", cascade="all, delete-orphan")


class UsuarioEstadoModel(Base):
    __tablename__ = "usuario_estado"
    __table_args__ = (UniqueConstraint('usuario_id', 'chave', name='uq_usuario_chave'),)
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    chave = Column(String(100), nullable=False)
    valor = Column(JSONB, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    usuario = relationship("UsuarioModel", back_populates="estados")
