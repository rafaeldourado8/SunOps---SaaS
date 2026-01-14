"""
Repository PostgreSQL para Cliente (Adapter)

SOLID: Dependency Inversion - implementa ClienteRepository (Port)
Complexidade: Mantida baixa
"""
from typing import List, Optional
from uuid import UUID

import sys
sys.path.append('../../../..')

from contexts.cadastros.domain.entities import Cliente
from contexts.cadastros.domain.repositories import ClienteRepository
from contexts.cadastros.infrastructure.django_models.cliente_model import ClienteModel
from shared.domain.value_objects import CPF, CNPJ, Email, Telefone


class ClienteRepositoryPostgreSQL(ClienteRepository):
    """
    Adapter que implementa ClienteRepository usando Django ORM.
    
    Responsabilidades:
    - Converter Entity ↔ Model
    - Persistir no PostgreSQL
    """
    
    def salvar(self, cliente: Cliente) -> Cliente:
        """Salva ou atualiza cliente. Complexidade: 2"""
        model = ClienteModel.objects.filter(id=cliente.id).first()
        
        if model:
            # Atualizar
            model.nome = cliente.nome
            model.documento = cliente.documento.valor
            model.email = cliente.email.valor
            model.telefone = cliente.telefone.valor
            model.endereco = cliente.endereco
            model.ativo = cliente.ativo
        else:
            # Criar
            model = ClienteModel(
                id=cliente.id,
                nome=cliente.nome,
                documento=cliente.documento.valor,
                email=cliente.email.valor,
                telefone=cliente.telefone.valor,
                endereco=cliente.endereco,
                ativo=cliente.ativo
            )
        
        model.save()
        return self._to_entity(model)
    
    def buscar_por_id(self, id: UUID) -> Optional[Cliente]:
        """Busca por ID. Complexidade: 2"""
        model = ClienteModel.objects.filter(id=id).first()
        return self._to_entity(model) if model else None
    
    def buscar_por_documento(self, documento: str) -> Optional[Cliente]:
        """Busca por documento. Complexidade: 2"""
        limpo = ''.join(c for c in documento if c.isdigit())
        model = ClienteModel.objects.filter(documento=limpo).first()
        return self._to_entity(model) if model else None
    
    def listar_todos(self, apenas_ativos: bool = True) -> List[Cliente]:
        """Lista todos. Complexidade: 2"""
        queryset = ClienteModel.objects.all()
        if apenas_ativos:
            queryset = queryset.filter(ativo=True)
        return [self._to_entity(m) for m in queryset]
    
    def deletar(self, id: UUID) -> bool:
        """Deleta por ID. Complexidade: 2"""
        deleted, _ = ClienteModel.objects.filter(id=id).delete()
        return deleted > 0
    
    def _to_entity(self, model: ClienteModel) -> Cliente:
        """
        Converte Model → Entity.
        Complexidade: 2
        """
        # Detectar CPF ou CNPJ
        if len(model.documento) == 11:
            documento = CPF(model.documento)
        else:
            documento = CNPJ(model.documento)
        
        return Cliente(
            id=model.id,
            nome=model.nome,
            documento=documento,
            email=Email(model.email),
            telefone=Telefone(model.telefone),
            endereco=model.endereco,
            ativo=model.ativo,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
