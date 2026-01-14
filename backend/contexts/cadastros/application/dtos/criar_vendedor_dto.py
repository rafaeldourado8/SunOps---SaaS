"""
DTO para criar Vendedor

SOLID: Single Responsibility
Complexidade: 0
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class CriarVendedorDTO:
    """
    DTO para entrada do Use Case CriarVendedor.
    
    Attributes:
        nome: Nome completo
        email: Email (string)
        telefone: Telefone (string)
        comissao_percentual: Percentual de comissão (opcional, padrão 5%)
    """
    nome: str
    email: str
    telefone: str
    comissao_percentual: Optional[float] = 5.0
