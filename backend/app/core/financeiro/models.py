import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum as SAEnum, ForeignKey, Numeric, Float, DateTime, Date, Text, Boolean, Index
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


# --- INÍCIO DO NOVO CÓDIGO DA FEATURE DE PREMISSAS ---

class Premissa(Base):
    """
    Tabela principal de Premissas de Preço.
    Contém a vigência, nome e status de uma tabela de preços.
    """
    __tablename__ = "premissas"

    id = Column(Integer, primary_key=True, index=True)
    # Assumindo que o "gestor" (User) é o dono da premissa (multi-tenancy)
    empresa_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True) 
    
    nome = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=True)
    
    data_vigencia_inicio = Column(Date, nullable=False)
    data_vigencia_fim = Column(Date, nullable=False)
    ativa = Column(Boolean, default=True, nullable=False)

    criada_em = Column(DateTime, default=datetime.utcnow)
    atualizada_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    faixas = relationship(
        "PremissaFaixa", 
        back_populates="premissa", 
        cascade="all, delete-orphan",
        lazy="joined" # Sempre carrega as faixas
    )
    regioes = relationship(
        "PremissaPorRegiao", 
        back_populates="premissa", 
        cascade="all, delete-orphan",
        lazy="joined" # Sempre carrega as regiões
    )
    
    __table_args__ = (
        Index("ix_premissas_vigencia_ativa", "data_vigencia_inicio", "data_vigencia_fim", "ativa"),
    )


class PremissaFaixa(Base):
    """
    Tabela de Faixas de Potência (ex: 0-4kW, 4-8kW)
    Define o preço por Watt (Wp) para cada faixa.
    """
    __tablename__ = "premissas_faixas"

    id = Column(Integer, primary_key=True)
    premissa_id = Column(Integer, ForeignKey("premissas.id"), nullable=False, index=True)

    nome_faixa = Column(String(100), nullable=True, default="Faixa Padrão")
    potencia_min = Column(Float, nullable=False) # Em kW
    potencia_max = Column(Float, nullable=False) # Em kW
    
    # Usar Numeric para valores monetários
    preco_unitario = Column(Numeric(10, 4), nullable=False) # Ex: 0.2300 (R$/Wp)

    ordem = Column(Integer, default=0)
    criada_em = Column(DateTime, default=datetime.utcnow)

    # Relacionamento
    premissa = relationship("Premissa", back_populates="faixas")


class PremissaPorRegiao(Base):
    """
    Tabela de Alíquotas de Imposto por Região (UF).
    Define o percentual de imposto para uma premissa específica em uma região.
    """
    __tablename__ = "premissas_por_regiao"

    id = Column(Integer, primary_key=True)
    premissa_id = Column(Integer, ForeignKey("premissas.id"), nullable=False, index=True)
    
    regiao = Column(String(10), nullable=False) # Ex: "SP", "RJ", "MG"
    aliquota_imposto = Column(Float, nullable=False) # Ex: 0.16 (16%)
    
    observacoes = Column(Text, nullable=True)
    criada_em = Column(DateTime, default=datetime.utcnow)

    # Relacionamento
    premissa = relationship("Premissa", back_populates="regioes")

    __table_args__ = (
        Index("ix_premissas_regiao_lookup", "premissa_id", "regiao"),
    )

# --- FIM DO NOVO CÓDIGO DA FEATURE DE PREMISSAS ---