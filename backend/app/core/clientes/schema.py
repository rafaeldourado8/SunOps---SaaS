from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, Annotated
from .models import TipoCliente

# Schema base com todos os campos que podem ser criados ou atualizados
class ClienteBase(BaseModel):
    nome_razao_social: Annotated[str, Field(min_length=3, max_length=255)]
    tipo: TipoCliente
    documento: Annotated[str, Field(min_length=11, max_length=18)] # Para CPF/CNPJ
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None

# Schema para criar um cliente (usado no "+ Novo Cliente")
class ClienteCreate(ClienteBase):
    pass

# Schema para exibir um cliente (o que a API retorna)
class ShowCliente(ClienteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# Schema para exibir o cliente com detalhes (para a tela "Ver detalhes")
# Apenas um exemplo de como você pode expandir
class ShowClienteDetalhado(ShowCliente):
    # Aqui você poderia adicionar listas de propostas e projetos
    # propostas: List[ShowProposta] = []
    # projetos: List[ShowProjeto] = []
    pass