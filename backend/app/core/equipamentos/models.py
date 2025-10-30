import enum
from sqlalchemy import (
    Column, Integer, String, Enum as SAEnum, Float, JSON, ForeignKey, 
    Numeric, DateTime, Boolean, Table
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from app.db import Base

# --- MODELO 1: O VENDEDOR (DISTRIBUIDOR) ---
# Quem vende o produto. Ex: Aldo, Belenus, Ecori.
class Distribuidor(Base):
    __tablename__ = "distribuidores"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False, unique=True, index=True)
    
    # Relações
    catalogo_itens = relationship("CatalogoItem", back_populates="distribuidor")
    kits = relationship("Kit", back_populates="distribuidor")

    def __repr__(self) -> str:
        return f"<Distribuidor(id={self.id!r}, nome={self.nome!r})>"

# --- MODELO 2: A CATEGORIA (COM ANINHAMENTO) ---
# Permite aninhar categorias, como você pediu:
# Estruturas (Pai) -> Solo (Filho)
# Estruturas (Pai) -> Fibrometal (Filho)
class CategoriaEquipamento(Base):
    __tablename__ = "categorias_equipamentos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    
    # Auto-relacionamento para aninhamento (Ex: 'Solo' aponta para 'Estruturas')
    parent_id = Column(Integer, ForeignKey("categorias_equipamentos.id"), nullable=True)
    
    # Relações
    parent = relationship("CategoriaEquipamento", remote_side=[id], back_populates="subcategorias")
    subcategorias = relationship("CategoriaEquipamento", back_populates="parent")
    equipamentos = relationship("Equipamento", back_populates="categoria")

    def __repr__(self) -> str:
        return f"<CategoriaEquipamento(id={self.id!r}, nome={self.nome!r})>"

# --- MODELO 3: O PRODUTO BASE ---
# A definição "pura" do equipamento, sem preço ou distribuidor.
# Ex: "Módulo HELIUS HYPERION HMB13..."
class Equipamento(Base):
    __tablename__ = "equipamentos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Relação com Categoria (Substitui o Enum 'TipoEquipamento')
    categoria_id = Column(Integer, ForeignKey("categorias_equipamentos.id"), nullable=False)
    
    nome_modelo = Column(String(255), nullable=False, unique=True, index=True)
    fabricante = Column(String(100), nullable=True)
    potencia_w = Column(Float, nullable=True) # Potência em Watts
    dados_tecnicos = Column(JSON, nullable=True) # Para Vmp, Imp, Dimensões, etc.
    
    # Relações
    categoria = relationship("CategoriaEquipamento", back_populates="equipamentos")
    catalogo_itens = relationship("CatalogoItem", back_populates="equipamento")

    def __repr__(self) -> str:
        return f"<Equipamento(id={self.id!r}, nome={self.nome_modelo!r})>"

# --- MODELO 4: O ITEM DE CATÁLOGO (SKU) ---
# Esta é a "cola" que liga o PRODUTO (Equipamento) ao VENDEDOR (Distribuidor)
# e adiciona o PREÇO.
class CatalogoItem(Base):
    __tablename__ = "catalogo_itens"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # O que é? (Ex: Módulo Helius)
    equipamento_id = Column(Integer, ForeignKey("equipamentos.id"), nullable=False)
    
    # Quem vende? (Ex: Belenus)
    distribuidor_id = Column(Integer, ForeignKey("distribuidores.id"), nullable=False)
    
    # Código do produto NO distribuidor (Ex: "08092023")
    codigo_distribuidor = Column(String(100), nullable=True, index=True)
    
    # Quanto custa para MIM (SaaS user) comprar
    preco_custo = Column(Numeric(10, 2), nullable=False)
    
    disponivel = Column(Boolean, default=True)
    data_atualizacao_preco = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relações
    equipamento = relationship("Equipamento", back_populates="catalogo_itens")
    distribuidor = relationship("Distribuidor", back_populates="catalogo_itens")

    def __repr__(self) -> str:
        return f"<CatalogoItem(id={self.id!r}, cod={self.codigo_distribuidor!r}, preco={self.preco_custo!r})>"

# --- Tabela de Associação: Kit <-> CatalogoItem ---
# Define a relação N-para-N (Muitos-para-Muitos) entre um Kit e seus Itens.
# Um Kit é composto por vários Itens, e um Item pode estar em vários Kits.
kit_items_association = Table(
    'kit_items_association',
    Base.metadata,
    Column('kit_id', Integer, ForeignKey('kits.id'), primary_key=True),
    Column('catalogo_item_id', Integer, ForeignKey('catalogo_itens.id'), primary_key=True),
    Column('quantidade', Integer, nullable=False, default=1) # Quantos desse item vão no kit
)

# --- MODELO 5: O KIT (BUNDLE) ---
# Representa o "Kit Fechado Manual"
# É um "pacote" de Itens de Catálogo de UM distribuidor.
class Kit(Base):
    __tablename__ = "kits"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # De qual distribuidor é este kit?
    distribuidor_id = Column(Integer, ForeignKey("distribuidores.id"), nullable=False)
    
    nome_kit = Column(String(255), nullable=False) # Ex: "KIT SOLAR"
    codigo_kit = Column(String(100), nullable=True, index=True) # Ex: "08092023"
    
    # Custo total do Kit (pode ser a soma dos itens ou um valor fixo)
    custo_total_kit = Column(Numeric(10, 2), nullable=False) # Ex: "R$ 5.354,14"
    
    # Relações
    distribuidor = relationship("Distribuidor", back_populates="kits")
    
    # Relação N-para-N (Muitos-para-Muitos)
    # "itens" é a lista de 'CatalogoItem' que compõem este kit.
    itens = relationship(
        "CatalogoItem",
        secondary=kit_items_association,
        backref=backref("kits_onde_aparece") # Um item pode aparecer em N kits
    )