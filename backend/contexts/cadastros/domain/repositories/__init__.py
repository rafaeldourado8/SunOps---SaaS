"""
Repository Interfaces (Ports) do contexto Cadastros
"""
from .cliente_repository import ClienteRepository
from .vendedor_repository import VendedorRepository

__all__ = ['ClienteRepository', 'VendedorRepository']
