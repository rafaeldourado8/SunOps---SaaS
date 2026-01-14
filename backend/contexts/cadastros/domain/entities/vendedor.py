"""
Entity: Vendedor

Representa um vendedor no domínio de Cadastros.
Contém apenas regras de negócio.

Complexidade Ciclomática: Mantida baixa (< 5 por método)
SOLID: Single Responsibility
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Vendedor:
    """
    Entity Vendedor.
    
    Attributes:
        id: Identificador único
        nome: Nome completo
        email: Email corporativo
        telefone: Telefone
        comissao_percentual: Percentual de comissão (0-100)
        ativo: Se vendedor está ativo
        created_at: Data de criação
        updated_at: Data de atualização
    """
    
    nome: str
    email: str
    telefone: str
    comissao_percentual: float = 5.0
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
        Valida regras de negócio do Vendedor.
        Complexidade: 4
        """
        if not self.nome or len(self.nome) < 3:
            raise ValueError("Nome deve ter no mínimo 3 caracteres")
        
        if not self.email:
            raise ValueError("Email é obrigatório")
        
        if not self.telefone:
            raise ValueError("Telefone é obrigatório")
        
        if not (0 <= self.comissao_percentual <= 100):
            raise ValueError("Comissão deve estar entre 0 e 100")
    
    def atualizar_comissao(self, novo_percentual: float) -> None:
        """
        Atualiza percentual de comissão.
        Complexidade: 2
        """
        if not (0 <= novo_percentual <= 100):
            raise ValueError("Comissão deve estar entre 0 e 100")
        
        self.comissao_percentual = novo_percentual
        self.updated_at = datetime.now()
    
    def calcular_comissao(self, valor_venda: float) -> float:
        """
        Calcula valor da comissão.
        Complexidade: 1
        """
        return valor_venda * (self.comissao_percentual / 100)
    
    def desativar(self) -> None:
        """Desativa vendedor. Complexidade: 1"""
        self.ativo = False
        self.updated_at = datetime.now()
    
    def ativar(self) -> None:
        """Ativa vendedor. Complexidade: 1"""
        self.ativo = True
        self.updated_at = datetime.now()
    
    def __str__(self) -> str:
        return f"Vendedor({self.nome}, {self.comissao_percentual}%)"
    
    def __repr__(self) -> str:
        return f"Vendedor(id={self.id}, nome='{self.nome}')"
