import enum
# --- IMPORTS ATUALIZADOS ---
from sqlalchemy import Column, Integer, String, Enum as SAEnum, DateTime
from sqlalchemy.sql import func # Para func.now()
# ---------------------------
from sqlalchemy.orm import relationship
from app.db import Base

# 1. Define o tipo de cliente (Pessoa Física ou Jurídica)
class TipoCliente(str, enum.Enum):
    PESSOA_FISICA = "pessoa_fisica"
    PESSOA_JURIDICA = "pessoa_juridica"

# 2. Define a tabela "clientes"
class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # "João Silva" ou "Empresa Solar Tech"
    nome_razao_social = Column(String(255), nullable=False)
    
    tipo = Column(SAEnum(TipoCliente), nullable=False)
    
    # "Doc: 123.456.789-00"
    documento = Column(String(20), nullable=False, unique=True)
    
    email = Column(String(255), nullable=True)
    telefone = Column(String(20), nullable=True)
    endereco = Column(String(255), nullable=True) # "São Paulo, SP"

    # --- CORREÇÃO ADICIONADA AQUI ---
    # Esta coluna registrará quando o cliente foi criado
    data_criacao = Column(
        DateTime(timezone=True), 
        server_default=func.now(), # Define o padrão no BD
        nullable=False
    )
    # --- FIM DA CORREÇÃO ---

    # 3. Relações (back-populates)
    #    Isso linka de volta aos módulos 'Proposta' e 'Projeto' que criámos antes.
    propostas = relationship("Proposta", back_populates="cliente")
    projetos = relationship("Projeto", back_populates="cliente")

    def __repr__(self) -> str:
        return f"<Cliente(id={self.id!r}, nome={self.nome_razao_social!r})>"