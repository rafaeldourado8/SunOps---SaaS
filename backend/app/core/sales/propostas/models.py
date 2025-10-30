import enum
# Imports atualizados
from sqlalchemy import Column, Integer, String, Enum as SAEnum, ForeignKey, Numeric, DateTime, JSON, Float
from sqlalchemy.sql import func 
from sqlalchemy.orm import relationship
from app.db import Base
from app.core.users.models import User 

class PropostaStatus(str, enum.Enum):
    NOVA = "nova"
    ENVIADA = "enviada"
    EM_NEGOCIACAO = "em_negociacao"
    GANHA = "ganha"
    PERDIDA = "perdida"

# NOVO MODELO (para a tabela de custos)
class PropostaItem(Base):
    __tablename__ = "proposta_itens"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Relação com a proposta principal
    proposta_id = Column(Integer, ForeignKey("propostas.id"), nullable=False)

    # Colunas baseadas nas imagens image_5c5e62.png e image_5c5e80.png
    categoria = Column(String(100), nullable=False, default="Custos") # Ex: KIT, Custos, Outros
    descricao = Column(String(255), nullable=False) # Ex: MONTAGEM, LUCRO, MATERIAIS ELETRICOS
    quantidade = Column(Integer, nullable=False, default=1)
    
    # Valores
    custo_unitario = Column(Numeric(10, 2), nullable=False, default=0.0)
    # Se você quiser seguir a tabela exata (image_5c5e80.png)
    impostos = Column(Numeric(10, 2), nullable=False, default=0.0)
    margem = Column(Numeric(10, 2), nullable=False, default=0.0)
    valor_venda = Column(Numeric(10, 2), nullable=False, default=0.0) # O valor final do item

    def __repr__(self) -> str:
        return f"<PropostaItem(id={self.id!r}, desc={self.descricao!r}, valor={self.valor_venda!r})>"


class Proposta(Base):
    __tablename__ = "propostas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # --- NOVOS CAMPOS ADICIONADOS ---
    nome = Column(String(255), nullable=True) # "Nome da Proposta"
    descricao = Column(String(1000), nullable=True) # "Descrição (Opcional)"
    
    # Dados técnicos
    potencia_kwp = Column(Float, nullable=True) # Ex: 2,80 kWp
    
    # Campo JSON para armazenar dados complexos da "Etapa 2"
    premissas = Column(JSON, nullable=True) 
    # Ex: {"sistema": "On grid", "topologia": "Tradicional", "inclinacao": 20, "desvio": 0}
    
    # O valor_total agora deve ser a SOMA dos 'PropostaItem'
    # Você pode manter ou remover, mas a fonte da verdade agora são os itens.
    valor_total = Column(Numeric(10, 2), nullable=False) 
    
    status = Column(
        SAEnum(PropostaStatus), 
        nullable=False, 
        default=PropostaStatus.NOVA
    )
    
    data_atualizacao = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(),
        nullable=False
    )
    
    # Relações (Foreign Keys)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    vendedor_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relações SQLAlchemy
    cliente = relationship("Cliente", back_populates="propostas")
    vendedor_responsavel = relationship("User", back_populates="propostas")
    
    # --- RELACIONAMENTO ADICIONADO ---
    # Uma proposta agora tem UMA LISTA de itens
    itens = relationship("PropostaItem", back_populates="proposta", cascade="all, delete-orphan")
    # Adicione este "proposta" no PropostaItem
    PropostaItem.proposta = relationship("Proposta", back_populates="itens")

    def __repr__(self) -> str:
        return f"<Proposta(id={self.id!r}, status={self.status!r}, valor={self.valor_total!r})>"