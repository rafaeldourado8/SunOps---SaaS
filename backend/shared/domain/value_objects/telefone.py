"""
Value Object: Telefone
Complexidade Ciclomática: 2
"""


class Telefone:
    def __init__(self, valor: str):
        limpo = self._limpar(valor)
        self._validar(limpo)
        self._valor = limpo
    
    def _limpar(self, valor: str) -> str:
        return ''.join(c for c in valor if c.isdigit())
    
    def _validar(self, telefone: str) -> None:
        if len(telefone) < 10 or len(telefone) > 11:
            raise ValueError("Telefone deve ter 10 ou 11 dígitos")
        
        if telefone == telefone[0] * len(telefone):
            raise ValueError("Telefone inválido")
    
    @property
    def valor(self) -> str:
        return self._valor
    
    @property
    def formatado(self) -> str:
        if len(self._valor) == 11:
            return f"({self._valor[:2]}) {self._valor[2:7]}-{self._valor[7:]}"
        return f"({self._valor[:2]}) {self._valor[2:6]}-{self._valor[6:]}"
    
    def __str__(self) -> str:
        return self.formatado
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Telefone) and self._valor == other._valor
    
    def __hash__(self) -> int:
        return hash(self._valor)
