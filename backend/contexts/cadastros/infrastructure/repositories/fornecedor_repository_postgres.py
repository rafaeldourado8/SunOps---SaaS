"""
Repository PostgreSQL para Fornecedor (Adapter)
"""
from typing import List, Optional
from contexts.cadastros.domain.entities.fornecedor import Fornecedor
from contexts.cadastros.domain.repositories.fornecedor_repository import FornecedorRepository
from contexts.cadastros.infrastructure.django_models.fornecedor_model import FornecedorModel
from shared.domain.value_objects.cnpj import CNPJ
from shared.domain.value_objects.email import Email
from shared.domain.value_objects.telefone import Telefone


class FornecedorRepositoryPostgreSQL(FornecedorRepository):
    """Implementação PostgreSQL do repositório"""
    
    def criar(self, fornecedor: Fornecedor) -> Fornecedor:
        model = FornecedorModel.objects.create(
            nome=fornecedor.nome,
            cnpj=fornecedor.cnpj.numero,
            email=fornecedor.email.endereco,
            telefone=fornecedor.telefone.numero,
            endereco=fornecedor.endereco,
            ativo=fornecedor.ativo
        )
        fornecedor.id = model.id
        return fornecedor
    
    def buscar_por_id(self, fornecedor_id: int) -> Optional[Fornecedor]:
        try:
            model = FornecedorModel.objects.get(id=fornecedor_id)
            return self._to_entity(model)
        except FornecedorModel.DoesNotExist:
            return None
    
    def listar_todos(self) -> List[Fornecedor]:
        models = FornecedorModel.objects.all()
        return [self._to_entity(m) for m in models]
    
    def atualizar(self, fornecedor: Fornecedor) -> Fornecedor:
        FornecedorModel.objects.filter(id=fornecedor.id).update(
            nome=fornecedor.nome,
            email=fornecedor.email.endereco,
            telefone=fornecedor.telefone.numero,
            endereco=fornecedor.endereco,
            ativo=fornecedor.ativo
        )
        return fornecedor
    
    def deletar(self, fornecedor_id: int) -> bool:
        deleted, _ = FornecedorModel.objects.filter(id=fornecedor_id).delete()
        return deleted > 0
    
    def _to_entity(self, model: FornecedorModel) -> Fornecedor:
        return Fornecedor(
            id=model.id,
            nome=model.nome,
            cnpj=CNPJ(model.cnpj),
            email=Email(model.email),
            telefone=Telefone(model.telefone),
            endereco=model.endereco,
            ativo=model.ativo
        )
