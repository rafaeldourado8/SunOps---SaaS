"""
DTOs para Marca
"""
from dataclasses import dataclass


@dataclass
class CriarMarcaDTO:
    nome: str


@dataclass
class AtualizarMarcaDTO:
    id: int
    nome: str
    ativo: bool = True
