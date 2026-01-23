from sqlalchemy import Column, String, Float, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from shared.infrastructure.database import Base


class ClienteModel(Base):
    __tablename__ = "clientes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(255), nullable=False)
    tipo_pessoa = Column(String(2), nullable=False)
    cpf = Column(String(14), unique=True, nullable=True)
    cnpj = Column(String(18), unique=True, nullable=True)
    rg = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    telefone = Column(String(20), nullable=False)
    
    logradouro = Column(String(255), nullable=True)
    numero = Column(String(20), nullable=True)
    complemento = Column(String(100), nullable=True)
    bairro = Column(String(100), nullable=True)
    cidade = Column(String(100), nullable=False)
    estado = Column(String(2), nullable=False)
    cep = Column(String(9), nullable=True)
    
    consumo_mensal_kwh = Column(Float, default=0)
    valor_conta_luz = Column(Float, default=0)
    
    # CORREÇÃO: Valor padrão deve corresponder a um Enum válido
    tipo_rede = Column(String(20), default="BIFASICO")
    
    status = Column(String(20), default="LEAD")
    vendedor_id = Column(UUID(as_uuid=True), nullable=False)
    notas_internas = Column(Text, default="")
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)