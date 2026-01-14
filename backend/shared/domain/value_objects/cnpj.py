"""
Value Object: CNPJ
Complexidade Ciclomática: 3
"""


class CNPJ:
    def __init__(self, valor: str):
        limpo = self._limpar(valor)
        self._validar(limpo)
        self._valor = limpo
    
    def _limpar(self, valor: str) -> str:
        return ''.join(c for c in valor if c.isdigit())
    
    def _validar(self, cnpj: str) -> None:
        if len(cnpj) != 14:
            raise ValueError("CNPJ deve ter 14 dígitos")
        
        if cnpj == cnpj[0] * 14:
            raise ValueError("CNPJ inválido")
        
        if not self._validar_digitos(cnpj):
            raise ValueError("CNPJ inválido")
    
    def _validar_digitos(self, cnpj: str) -> bool:
        # Primeiro dígito
        pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * pesos[i] for i in range(12))
        digito1 = 0 if soma % 11 < 2 else 11 - (soma % 11)
        
        # Segundo dígito
        pesos = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * pesos[i] for i in range(13))
        digito2 = 0 if soma % 11 < 2 else 11 - (soma % 11)
        
        return cnpj[-2:] == f"{digito1}{digito2}"
    
    @property
    def valor(self) -> str:
        return self._valor
    
    @property
    def formatado(self) -> str:
        return f"{self._valor[:2]}.{self._valor[2:5]}.{self._valor[5:8]}/{self._valor[8:12]}-{self._valor[12:]}"
    
    def __str__(self) -> str:
        return self.formatado
    
    def __eq__(self, other) -> bool:
        return isinstance(other, CNPJ) and self._valor == other._valor
    
    def __hash__(self) -> int:
        return hash(self._valor)
