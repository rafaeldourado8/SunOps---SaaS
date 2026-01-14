"""
Value Object: CPF
Complexidade Ciclomática: 3
"""


class CPF:
    def __init__(self, valor: str):
        limpo = self._limpar(valor)
        self._validar(limpo)
        self._valor = limpo
    
    def _limpar(self, valor: str) -> str:
        return ''.join(c for c in valor if c.isdigit())
    
    def _validar(self, cpf: str) -> None:
        if len(cpf) != 11:
            raise ValueError("CPF deve ter 11 dígitos")
        
        if cpf == cpf[0] * 11:
            raise ValueError("CPF inválido")
        
        if not self._validar_digitos(cpf):
            raise ValueError("CPF inválido")
    
    def _validar_digitos(self, cpf: str) -> bool:
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digito1 = (soma * 10 % 11) % 10
        
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digito2 = (soma * 10 % 11) % 10
        
        return cpf[-2:] == f"{digito1}{digito2}"
    
    @property
    def valor(self) -> str:
        return self._valor
    
    @property
    def formatado(self) -> str:
        return f"{self._valor[:3]}.{self._valor[3:6]}.{self._valor[6:9]}-{self._valor[9:]}"
    
    def __str__(self) -> str:
        return self.formatado
    
    def __eq__(self, other) -> bool:
        return isinstance(other, CPF) and self._valor == other._valor
    
    def __hash__(self) -> int:
        return hash(self._valor)
