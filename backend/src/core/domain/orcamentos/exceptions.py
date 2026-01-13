class DomainException(Exception):
    """Base para exceções de domínio"""
    pass

class KitInvalidoException(DomainException):
    """Kit não atende requisitos mínimos"""
    pass

class OrcamentoInvalidoException(DomainException):
    """Orçamento em estado inválido"""
    pass

class OrcamentoExpiradoException(DomainException):
    """Orçamento fora da validade"""
    pass

class StatusInvalidoException(DomainException):
    """Transição de status inválida"""
    pass

class ValorInvalidoException(DomainException):
    """Valor monetário inválido"""
    pass

class QuantidadeInvalidaException(DomainException):
    """Quantidade inválida"""
    pass
