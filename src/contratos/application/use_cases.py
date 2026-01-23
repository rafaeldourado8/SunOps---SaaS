from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID

from ..domain.template import Template, TipoTemplate
from ..infrastructure.repository import SQLAlchemyTemplateRepository


@dataclass
class SalvarTemplateDTO:
    tipo: str
    nome: str
    arquivo_path: str
    vendedor_id: UUID


class SalvarTemplateUseCase:
    def __init__(self, repository: SQLAlchemyTemplateRepository):
        self._repository = repository
    
    def execute(self, dto: SalvarTemplateDTO) -> Template:
        template = Template(
            tipo=TipoTemplate(dto.tipo),
            nome=dto.nome,
            arquivo_path=dto.arquivo_path,
            vendedor_id=str(dto.vendedor_id)
        )
        return self._repository.save(template)


class ListarTemplatesUseCase:
    def __init__(self, repository: SQLAlchemyTemplateRepository):
        self._repository = repository
    
    def execute(self, vendedor_id: Optional[UUID] = None) -> List[Template]:
        if vendedor_id:
            return self._repository.find_by_vendedor(vendedor_id)
        return self._repository.find_all()