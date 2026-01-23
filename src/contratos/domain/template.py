from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from typing import Optional

from shared.domain.entity import Entity


class TipoTemplate(Enum):
    PROPOSTA = "PROPOSTA"
    CONTRATO = "CONTRATO"


@dataclass
class Template(Entity):
    tipo: TipoTemplate = TipoTemplate.PROPOSTA
    nome: str = ""
    arquivo_path: str = ""
    vendedor_id: str = ""
    ativo: bool = True
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()