import enum
from sqlalchemy import Column, Integer, String, Enum as SAEnum, ForeignKey, Numeric, Float
from sqlalchemy.orm import relationship
from app.db import Base

# 1. Define os status dos projetos
class ProjetoStatus(str, enum.Enum):
    EM_NEGOCIACAO = "Em Negociação"
    APROVADO = "Aprovado"
    EM_ANALISE = "Em Análise"
    INSTALADO = "Instalado"
    CANCELADO = "Cancelado"

# 2. Define a tabela "projetos"
class Projeto(Base):
    __tablename__ = "projetos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False) # Ex: "João Silva Residencial"
    valor_total = Column(Numeric(10, 2), nullable=False) # Ex: 45600.00
    potencia_kwp = Column(Float, nullable=True) # Ex: 8.4
    
    status = Column(
        SAEnum(ProjetoStatus), 
        nullable=False, 
        default=ProjetoStatus.EM_NEGOCIACAO
    )
    
    # Relações (Foreign Keys)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    
    # 'Responsável' (pode ser Gestor ou Vendedor)
    responsavel_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relações SQLAlchemy
    cliente = relationship("Cliente", back_populates="projetos")
    
    # Linka ao 'User' (usando o 'projetos' do user.models.py)
    # Lembre-se que no seu user.models.py você chamou o back_populates de "gestor_responsavel"
    # O ideal seria renomear lá para "projetos_responsaveis"
    # Mas, seguindo seu código:
    gestor_responsavel = relationship("User", back_populates="projetos")