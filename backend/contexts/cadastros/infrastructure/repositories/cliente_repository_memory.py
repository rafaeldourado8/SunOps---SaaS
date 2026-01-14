"""
Repository In-Memory para Cliente (Adapter para testes)

SOLID: Dependency Inversion - implementa ClienteRepository (Port)
Complexidade: Mantida baixa
"""
from typing import List, Optional, Dict
from uuid import UUID

import sys
sys.path.append('../../../..')
from contexts.cadastros.domain.entities import Cliente
from contexts.cadastros.domain.repositories import ClienteRepository


class ClienteRepositoryInMemory(ClienteRepository):
    """
    Implementação em memória do ClienteRepository.
    Usado para testes (não precisa de banco real).
    """
    
    def __init__(self):
        """Inicializa storage em memória. Complexidade: 1"""
        self._clientes: Dict[UUID, Cliente] = {}
    
    def salvar(self, cliente: Cliente) -> Cliente:
        """Salva cliente em memória. Complexidade: 1"""
        self._clientes[cliente.id] = cliente
        return cliente
    
    def buscar_por_id(self, id: UUID) -> Optional[Cliente]:
        """Busca por ID. Complexidade: 1"""
        return self._clientes.get(id)
    
    def buscar_por_documento(self, documento: str) -> Optional[Cliente]:
        """Busca por documento. Complexidade: 2"""
        limpo = ''.join(c for c in documento if c.isdigit())
        for cliente in self._clientes.values():
            if cliente.documento.valor == limpo:
                return cliente
        return None
    
    def listar_todos(self, apenas_ativos: bool = True) -> List[Cliente]:
        """Lista todos. Complexidade: 2"""
        clientes = list(self._clientes.values())
        if apenas_ativos:
            return [c for c in clientes if c.ativo]
        return clientes
    
    def deletar(self, id: UUID) -> bool:
        """Deleta por ID. Complexidade: 2"""
        if id in self._clientes:
            del self._clientes[id]
            return True
        return False
    
    def limpar(self):
        """Limpa todos os dados (útil para testes). Complexidade: 1"""
        self._clientes.clear()
