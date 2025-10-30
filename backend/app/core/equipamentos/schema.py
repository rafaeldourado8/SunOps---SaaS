from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Any
from decimal import Decimal

# --- Distribuidor Schemas ---
class DistribuidorBase(BaseModel):
    nome: str = Field(..., max_length=255)

class DistribuidorCreate(DistribuidorBase):
    pass

class ShowDistribuidor(DistribuidorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- CategoriaEquipamento Schemas ---
class CategoriaEquipamentoBase(BaseModel):
    nome: str = Field(..., max_length=100)
    parent_id: Optional[int] = None

class CategoriaEquipamentoCreate(CategoriaEquipamentoBase):
    pass

class ShowCategoriaEquipamento(CategoriaEquipamentoBase):
    id: int
    # Para mostrar subcategorias aninhadas, se necessário no futuro
    # subcategorias: List['ShowCategoriaEquipamento'] = []
    model_config = ConfigDict(from_attributes=True)

# --- Equipamento Schemas ---
# Removido o Enum TipoEquipamento, pois agora usamos CategoriaEquipamento
class EquipamentoBase(BaseModel):
    categoria_id: int
    nome_modelo: str = Field(..., max_length=255)
    fabricante: Optional[str] = Field(None, max_length=100)
    potencia_w: Optional[float] = None
    dados_tecnicos: Optional[dict[str, Any]] = None

class EquipamentoCreate(EquipamentoBase):
    pass

class ShowEquipamento(EquipamentoBase):
    id: int
    # Poderíamos incluir a categoria aqui se necessário
    # categoria: ShowCategoriaEquipamento
    model_config = ConfigDict(from_attributes=True)

# --- CatalogoItem Schemas ---
class CatalogoItemBase(BaseModel):
    equipamento_id: int
    distribuidor_id: int
    codigo_distribuidor: Optional[str] = Field(None, max_length=100)
    preco_custo: Decimal
    disponivel: bool = True

class CatalogoItemCreate(CatalogoItemBase):
    pass

class ShowCatalogoItem(CatalogoItemBase):
    id: int
    equipamento: ShowEquipamento # Mostrar detalhes do equipamento
    distribuidor: ShowDistribuidor # Mostrar detalhes do distribuidor
    data_atualizacao_preco: Optional[Any] = None # Ou use datetime
    model_config = ConfigDict(from_attributes=True)

# --- Kit Schemas ---
# Schema para representar um item dentro do kit (na criação/exibição)
class KitItemAssociationSchema(BaseModel):
    catalogo_item_id: int
    quantidade: int = 1

class KitBase(BaseModel):
    distribuidor_id: int
    nome_kit: str = Field(..., max_length=255)
    codigo_kit: Optional[str] = Field(None, max_length=100)
    custo_total_kit: Decimal

class KitCreate(KitBase):
    # Ao criar um kit, esperamos a lista de IDs e quantidades
    itens: List[KitItemAssociationSchema] = []

class ShowKitItemDetail(BaseModel): # Schema específico para exibir o item DENTRO do kit
    quantidade: int
    item: ShowCatalogoItem # Mostra os detalhes completos do CatalogoItem
    model_config = ConfigDict(from_attributes=True)


class ShowKit(KitBase):
    id: int
    distribuidor: ShowDistribuidor # Mostrar detalhes do distribuidor
    # Ao exibir um kit, mostramos os detalhes dos itens
    itens: List[ShowKitItemDetail] = [] # Ajustado para mostrar mais detalhes
    model_config = ConfigDict(from_attributes=True)