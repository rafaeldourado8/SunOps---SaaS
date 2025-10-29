import enum
from sqlalchemy import Column, Integer, String, Enum as SAEnum, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db import Base
from app.core.users.models import User # Importa o modelo User
# Importe também seu modelo Cliente (vou assumir o caminho)
# from app.core.clientes.models import Cliente 

# 1. Define os status do funil de propostas
class PropostaStatus(str, enum.Enum):
    NOVA = "nova"
    ENVIADA = "enviada"
    EM_NEGOCIACAO = "em_negociacao"
    GANHA = "ganha"
    PERDIDA = "perdida"

# 2. Define a tabela "propostas"
class Proposta(Base):
    __tablename__ = "propostas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Ex: 847300.00 (Valor em Negociação)
    valor_total = Column(Numeric(10, 2), nullable=False) 
    
    # 3. Coluna de Status (linkada ao Enum)
    status = Column(
        SAEnum(PropostaStatus), 
        nullable=False, 
        default=PropostaStatus.NOVA
    )
    
    # 4. Relações (Foreign Keys)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    vendedor_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # 5. Relações SQLAlchemy (para acessar os objetos)
    cliente = relationship("Cliente", back_populates="propostas")
    
    # Linka ao 'User' e usa o 'propostas' que definimos no models.py do usuário
    vendedor_responsavel = relationship("User", back_populates="propostas")

    def __repr__(self) -> str:
        return f"<Proposta(id={self.id!r}, status={self.status!r}, valor={self.valor_total!r})>"