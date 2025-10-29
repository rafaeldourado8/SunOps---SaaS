import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum as SAEnum, ForeignKey, Numeric, Float, DateTime, Date
from sqlalchemy.orm import relationship
from app.db import Base

# 1. Tabela de Configurações (para a tela de "Configurações Financeiras")
# Esta tabela terá apenas UMA linha (o Padrão Singleton)
class ConfiguracaoFinanceira(Base):
    __tablename__ = "configuracoes_financeiras"

    id = Column(Integer, primary_key=True, default=1) # Sempre ID 1
    
    # "Defina margens de lucro..."
    margem_lucro_padrao = Column(Float, nullable=False, default=0.20) # 20%
    
    # "Defina... comissões"
    percentual_comissao_padrao = Column(Float, nullable=False, default=0.05) # 5%


# 2. Enums para a tabela de Transações
class TipoTransacao(str, enum.Enum):
    ENTRADA_PROJETO = "entrada_projeto" # "Pagamento da entrada..."
    CUSTO_EQUIPAMENTO = "custo_equipamento"
    COMISSAO_A_PAGAR = "comissao_a_pagar"
    OUTRA_RECEITA = "outra_receita"
    OUTRA_DESPESA = "outra_despesa"

class StatusTransacao(str, enum.Enum):
    PENDENTE = "pendente"
    PAGA = "paga"
    ATRASADA = "atrasada" # Para o alerta
    CANCELADA = "cancelada"

# 3. Tabela de Transações (para o alerta de pagamento)
class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(255), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    
    tipo = Column(SAEnum(TipoTransacao), nullable=False)
    status = Column(SAEnum(StatusTransacao), nullable=False, default=StatusTransacao.PENDENTE)

    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_vencimento = Column(Date, nullable=True) # Para o alerta de "atrasado"
    data_pagamento = Column(DateTime, nullable=True) # Quando foi paga

    # Relações
    projeto_id = Column(Integer, ForeignKey("projetos.id"), nullable=True)
    vendedor_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Para comissões

    projeto = relationship("Projeto")
    vendedor = relationship("User")