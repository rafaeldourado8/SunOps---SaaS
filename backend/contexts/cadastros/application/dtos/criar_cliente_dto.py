"""
DTO (Data Transfer Object) para criar Cliente

SOLID: Single Responsibility - apenas transferir dados
Complexidade: 0 (apenas dados)
"""
from dataclasses import dataclass


@dataclass
class CriarClienteDTO:
    """
    DTO para entrada do Use Case CriarCliente.
    
    Attributes:
        nome: Nome completo
        documento: CPF ou CNPJ (string)
        email: Email (string)
        telefone: Telefone (string)
        endereco: Endereço completo
    """
    nome: str
    documento: str
    email: str
    telefone: str
    endereco: str
