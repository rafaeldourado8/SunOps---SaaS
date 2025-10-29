from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from .models import PropostaStatus
from app.core.users.schema import ShowUser
from app.core.clientes.schema import ShowCliente # Assumindo o caminho

# Schema base com campos comuns
class PropostaBase(BaseModel):
    valor_total: Decimal
    cliente_id: int
    status: PropostaStatus = PropostaStatus.NOVA

# Schema para criar uma proposta (o que a API recebe)
class PropostaCreate(PropostaBase):
    pass

# Schema para atualizar o status
class PropostaUpdateStatus(BaseModel):
    status: PropostaStatus

# Schema para exibir uma proposta (o que a API envia)
class ShowProposta(PropostaBase):
    id: int
    vendedor_responsavel: ShowUser # Objeto aninhado
    cliente: ShowCliente          # Objeto aninhado

    model_config = ConfigDict(from_attributes=True)