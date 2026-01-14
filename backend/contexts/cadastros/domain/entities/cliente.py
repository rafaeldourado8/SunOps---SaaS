"""
Entity: Cliente

Usa Value Objects para garantir validação.
Complexidade Ciclomática: Mantida baixa (< 5 por método)
SOLID: Single Responsibility + Dependency Inversion (usa abstrações)
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Union
from uuid import UUID, uuid4

import sys
sys.path.append('../../..')
from shared.domain.value_objects import CPF, CNPJ, Email, Telefone


@dataclass
class Cliente:
    """
    Entity Cliente - Agregado raiz do contexto Cadastros.
    
    Attributes:
        id: Identificador único
        nome: Nome completo
        documento: CPF ou CNPJ (Value Object)
        email: Email (Value Object)
        telefone: Telefone (Value Object)
        endereco: Endereço completo
        ativo: Se cliente está ativo
        created_at: Data de criação
        updated_at: Data de atualização
    """
    
    nome: str
    documento: Union[CPF, CNPJ]
    email: Email
    telefone: Telefone
    endereco: str
    id: UUID = None
    ativo: bool = True
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        """Inicializa valores padrão. Complexidade: 2"""
        if self.id is None:
            self.id = uuid4()
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        
        self.validate()
    
    def validate(self) -> None:
        """
        Valida regras de negócio do Cliente.
        Complexidade: 2 (Value Objects já validam)
        """
        if not self.nome or len(self.nome) < 3:
            raise ValueError("Nome deve ter no mínimo 3 caracteres")
        
        if not self.endereco:
            raise ValueError("Endereço é obrigatório")
    
    def atualizar(self, **kwargs) -> None:
        """
        Atualiza dados do cliente.
        Complexidade: 1
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        self.updated_at = datetime.now()
        self.validate()
    
    def desativar(self) -> None:
        """Desativa cliente. Complexidade: 1"""
        self.ativo = False
        self.updated_at = datetime.now()
    
    def ativar(self) -> None:
        """Ativa cliente. Complexidade: 1"""
        self.ativo = True
        self.updated_at = datetime.now()
    
    def __str__(self) -> str:
        return f"Cliente({self.nome}, {self.documento})"
    
    def __repr__(self) -> str:
        return f"Cliente(id={self.id}, nome='{self.nome}')"
