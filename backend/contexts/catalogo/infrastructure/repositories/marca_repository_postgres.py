"""
Repository PostgreSQL para Marca
"""
from typing import List, Optional
from contexts.catalogo.domain.entities.marca import Marca
from contexts.catalogo.domain.repositories.marca_repository import MarcaRepository
from contexts.catalogo.infrastructure.django_models.marca_model import MarcaModel


class MarcaRepositoryPostgreSQL(MarcaRepository):
    """Implementação PostgreSQL"""
    
    def criar(self, marca: Marca) -> Marca:
        model = MarcaModel.objects.create(nome=marca.nome, ativo=marca.ativo)
        marca.id = model.id
        return marca
    
    def buscar_por_id(self, marca_id: int) -> Optional[Marca]:
        try:
            model = MarcaModel.objects.get(id=marca_id)
            return Marca(id=model.id, nome=model.nome, ativo=model.ativo)
        except MarcaModel.DoesNotExist:
            return None
    
    def listar_todos(self) -> List[Marca]:
        models = MarcaModel.objects.all()
        return [Marca(id=m.id, nome=m.nome, ativo=m.ativo) for m in models]
    
    def atualizar(self, marca: Marca) -> Marca:
        MarcaModel.objects.filter(id=marca.id).update(nome=marca.nome, ativo=marca.ativo)
        return marca
    
    def deletar(self, marca_id: int) -> bool:
        deleted, _ = MarcaModel.objects.filter(id=marca_id).delete()
        return deleted > 0
