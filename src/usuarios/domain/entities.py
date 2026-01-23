from dataclasses import dataclass
from enum import Enum
from typing import Optional

from shared.domain.entity import Entity
from shared.domain.value_objects import Email


class TipoUsuario(Enum):
    VENDEDOR = "VENDEDOR"
    GESTOR = "GESTOR"
    ADMIN = "ADMIN"


@dataclass
class Usuario(Entity):
    nome: str = ""
    email: Email = None
    senha_hash: str = ""
    tipo: TipoUsuario = TipoUsuario.VENDEDOR
    ativo: bool = True
    
    def is_admin(self) -> bool:
        return self.tipo == TipoUsuario.ADMIN
    
    def is_gestor(self) -> bool:
        return self.tipo in [TipoUsuario.GESTOR, TipoUsuario.ADMIN]
