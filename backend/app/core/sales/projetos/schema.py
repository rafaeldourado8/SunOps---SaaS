from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from typing import Optional
from .models import ProjetoStatus
from app.core.users.schema import ShowUser
from app.core.clientes.schema import ShowCliente # Assumindo o caminho

class ProjetoBase(BaseModel):
    nome: str
    valor_total: Decimal
    potencia_kwp: Optional[float] = None
    cliente_id: int
    responsavel_id: int
    status: ProjetoStatus = ProjetoStatus.EM_NEGOCIACAO

class ProjetoCreate(ProjetoBase):
    pass

class ShowProjeto(ProjetoBase):
    id: int
    cliente: ShowCliente
    gestor_responsavel: ShowUser # Lembre-se que o nome deve bater com o do model

    model_config = ConfigDict(from_attributes=True)