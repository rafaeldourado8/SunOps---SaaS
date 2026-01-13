from sqlalchemy import Column, String, Boolean, Integer, Numeric, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class KitModel(Base):
    __tablename__ = "kits"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(200), nullable=False)
    is_template = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    data = Column(JSONB)
    
    itens = relationship("ItemKitModel", back_populates="kit", cascade="all, delete-orphan")

class ItemKitModel(Base):
    __tablename__ = "itens_kit"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kit_id = Column(UUID(as_uuid=True), ForeignKey("kits.id"), nullable=False)
    categoria = Column(String(50), nullable=False)
    nome = Column(String(200), nullable=False)
    marca = Column(String(100))
    potencia_watts = Column(Integer)
    preco = Column(Numeric(10, 2), nullable=False)
    quantidade = Column(Integer, nullable=False)
    descricao = Column(Text)
    
    kit = relationship("KitModel", back_populates="itens")

class OrcamentoModel(Base):
    __tablename__ = "orcamentos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kit_id = Column(UUID(as_uuid=True), ForeignKey("kits.id"), nullable=False)
    cliente_nome = Column(String(200), nullable=False)
    cliente_contato = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    validade_dias = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    aprovado_por = Column(String(200))
    enviado_em = Column(DateTime)
    data = Column(JSONB)
    
    kit = relationship("KitModel")

class DomainEventModel(Base):
    __tablename__ = "domain_events"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    aggregate_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    aggregate_type = Column(String(100), nullable=False)
    event_type = Column(String(100), nullable=False)
    event_data = Column(JSONB, nullable=False)
    occurred_at = Column(DateTime, default=datetime.now)
    version = Column(Integer, nullable=False)

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class ConversationModel(Base):
    __tablename__ = "conversations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone = Column(String(20), nullable=False, index=True)
    agent_type = Column(String(50), nullable=False)
    context_json = Column(JSONB, default={})
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    messages = relationship("MessageModel", back_populates="conversation", cascade="all, delete-orphan")

class MessageModel(Base):
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    conversation = relationship("ConversationModel", back_populates="messages")

class TicketModel(Base):
    __tablename__ = "tickets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_number = Column(String(20), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    status = Column(String(50), nullable=False, default="open")
    priority = Column(String(20), default="normal")
    subject = Column(String(200))
    description = Column(Text)
    inverter_serial = Column(String(100))
    warranty_status = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    resolved_at = Column(DateTime)
    data = Column(JSONB, default={})
