from dataclasses import dataclass
from typing import Optional
import re


@dataclass(frozen=True)
class CPF:
    value: str
    
    def __post_init__(self):
        if not self._is_valid():
            raise ValueError(f"CPF inválido: {self.value}")
    
    def _is_valid(self) -> bool:
        cpf = re.sub(r'\D', '', self.value)
        return len(cpf) == 11 and cpf != cpf[0] * 11


@dataclass(frozen=True)
class CNPJ:
    value: str
    
    def __post_init__(self):
        if not self._is_valid():
            raise ValueError(f"CNPJ inválido: {self.value}")
    
    def _is_valid(self) -> bool:
        cnpj = re.sub(r'\D', '', self.value)
        return len(cnpj) == 14 and cnpj != cnpj[0] * 14


@dataclass(frozen=True)
class Email:
    value: str
    
    def __post_init__(self):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', self.value):
            raise ValueError(f"Email inválido: {self.value}")


@dataclass(frozen=True)
class Telefone:
    value: str
    
    def __post_init__(self):
        digits = re.sub(r'\D', '', self.value)
        if len(digits) < 10 or len(digits) > 11:
            raise ValueError(f"Telefone inválido: {self.value}")


@dataclass(frozen=True)
class Endereco:
    logradouro: str
    numero: str
    cidade: str
    estado: str
    cep: str
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    
    def __post_init__(self):
        if len(self.estado) != 2:
            raise ValueError("Estado deve ter 2 caracteres")


@dataclass(frozen=True)
class Money:
    value: float
    
    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Valor monetário não pode ser negativo")
    
    def __add__(self, other: 'Money') -> 'Money':
        return Money(self.value + other.value)
    
    def __sub__(self, other: 'Money') -> 'Money':
        return Money(self.value - other.value)
    
    def __mul__(self, multiplier: float) -> 'Money':
        return Money(self.value * multiplier)
