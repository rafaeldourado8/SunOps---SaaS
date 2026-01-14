"""
DTOs para Fornecedor (Application Layer)
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class CriarFornecedorDTO:
    """DTO para criar fornecedor"""
    nome: str
    cnpj: str
    email: str
    telefone: str
    endereco: Optional[str] = None


@dataclass
class AtualizarFornecedorDTO:
    """DTO para atualizar fornecedor"""
    id: int
    nome: str
    email: str
    telefone: str
    endereco: Optional[str] = None
    ativo: bool = True
