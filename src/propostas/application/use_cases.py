from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from ..domain.entities import Proposta, ItemProposta, StatusProposta
from ..domain.repository import IPropostaRepository
from ..domain.services import CalculadoraPayback
from shared.domain.value_objects import Money
from shared.infrastructure.pdf_generator import IPDFGenerator, PDFDocument


@dataclass
class CriarPropostaDTO:
    vendedor_id: UUID
    cliente_id: UUID
    potencia_sistema_kwp: float


@dataclass
class AdicionarItemDTO:
    proposta_id: UUID
    nome: str
    quantidade: int
    preco_unitario: float
    custo_unitario: float


@dataclass
class AtualizarPropostaDTO:
    id: UUID
    status: str


class CriarPropostaUseCase:
    def __init__(self, repository: IPropostaRepository):
        self._repository = repository
    
    def execute(self, dto: CriarPropostaDTO) -> Proposta:
        proposta = Proposta(
            vendedor_id=dto.vendedor_id,
            cliente_id=dto.cliente_id,
            potencia_sistema_kwp=dto.potencia_sistema_kwp
        )
        return self._repository.save(proposta)


class AtualizarPropostaUseCase:
    def __init__(self, repository: IPropostaRepository):
        self._repository = repository
        
    def execute(self, dto: AtualizarPropostaDTO) -> Proposta:
        proposta = self._repository.find_by_id(dto.id)
        if not proposta:
            raise ValueError("Proposta não encontrada")
        
        try:
            proposta.status = StatusProposta(dto.status)
        except ValueError:
            raise ValueError(f"Status inválido: {dto.status}")
            
        return self._repository.save(proposta)


class AdicionarItemPropostaUseCase:
    def __init__(self, repository: IPropostaRepository):
        self._repository = repository
    
    def execute(self, dto: AdicionarItemDTO) -> Proposta:
        proposta = self._repository.find_by_id(dto.proposta_id)
        if not proposta:
            raise ValueError("Proposta não encontrada")
        
        item = ItemProposta(
            nome=dto.nome,
            quantidade=dto.quantidade,
            preco_unitario=Money(dto.preco_unitario),
            custo_unitario=Money(dto.custo_unitario)
        )
        
        proposta.adicionar_item(item)
        return self._repository.save(proposta)


class SolicitarDescontoUseCase:
    def __init__(self, repository: IPropostaRepository):
        self._repository = repository
    
    def execute(self, proposta_id: UUID, valor: float, motivo: str, solicitante_id: UUID) -> Proposta:
        proposta = self._repository.find_by_id(proposta_id)
        if not proposta:
            raise ValueError("Proposta não encontrada")
        
        proposta.solicitar_desconto(Money(valor), motivo, solicitante_id)
        return self._repository.save(proposta)


class CalcularPaybackUseCase:
    def __init__(self, repository: IPropostaRepository, calculadora: CalculadoraPayback):
        self._repository = repository
        self._calculadora = calculadora
    
    def execute(self, proposta_id: UUID, economia_mensal: float) -> Proposta:
        proposta = self._repository.find_by_id(proposta_id)
        if not proposta:
            raise ValueError("Proposta não encontrada")
        
        proposta.payback_anos = self._calculadora.calcular(proposta, economia_mensal)
        return self._repository.save(proposta)


class GerarPDFPropostaUseCase:
    def __init__(self, generator: IPDFGenerator):
        self._generator = generator
        
    def execute(self, proposta: Proposta, cliente_nome: str, output_path: str) -> str:
        document = PDFDocument(
            content={'proposta': proposta, 'cliente_nome': cliente_nome},
            output_path=output_path
        )
        return self._generator.generate(document)


class ExcluirPropostaUseCase:
    def __init__(self, repository: IPropostaRepository):
        self._repository = repository
        
    def execute(self, proposta_id: UUID):
        proposta = self._repository.find_by_id(proposta_id)
        if not proposta:
            raise ValueError("Proposta não encontrada")
        self._repository.delete(proposta_id)