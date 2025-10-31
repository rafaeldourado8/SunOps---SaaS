from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from typing import Optional, List

# --- Categoria (Para Módulos, Inversores, etc.) ---

class CategoriaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    categoria_pai_id: Optional[int] = None

class CategoriaCreate(CategoriaBase):
    pass

class ShowCategoria(CategoriaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Equipamento (O item técnico da ANEEL, sem preço) ---

class EquipamentoBase(BaseModel):
    nome_modelo: str
    fabricante: Optional[str] = None
    potencia_w: Optional[float] = None
    dados_tecnicos: Optional[dict] = None
    categoria_id: int

class EquipamentoCreate(EquipamentoBase):
    pass

class ShowEquipamento(EquipamentoBase):
    id: int
    categoria: ShowCategoria
    model_config = ConfigDict(from_attributes=True)

# --- Distribuidor (Aldo, Belenus, etc. - MANTIDO) ---

class DistribuidorBase(BaseModel):
    nome: str
    website: Optional[str] = None
    contato: Optional[str] = None

class DistribuidorCreate(DistribuidorBase):
    pass

class ShowDistribuidor(DistribuidorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# --- CatalogoItem (O "SKU" com preço - MANTIDO) ---

class CatalogoItemBase(BaseModel):
    equipamento_id: int
    distribuidor_id: int
    codigo_distribuidor: str
    preco_custo: Decimal
    disponivel: bool = True

class CatalogoItemCreate(CatalogoItemBase):
    pass

class ShowCatalogoItem(BaseModel):
    id: int
    equipamento: ShowEquipamento
    distribuidor: ShowDistribuidor
    codigo_distribuidor: str
    preco_custo: Decimal
    disponivel: bool
    model_config = ConfigDict(from_attributes=True)


# --- Kits (Pacotes de itens - MANTIDO) ---

class KitBase(BaseModel):
    nome_kit: str
    distribuidor_id: int
    codigo_kit: str
    custo_total_kit: Decimal
    itens_kit: List[int] # Lista de IDs de CatalogoItem

class KitCreate(KitBase):
    pass

class ShowKit(KitBase):
    id: int
    distribuidor: ShowDistribuidor
    itens: List[ShowCatalogoItem] # Mostra os itens completos
    model_config = ConfigDict(from_attributes=True)