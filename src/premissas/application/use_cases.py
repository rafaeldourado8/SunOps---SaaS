from dataclasses import dataclass
from uuid import UUID

from ..domain.entities import Premissa, CategoriaProduto, ConfiguracaoGlobal
from ..domain.repository import IPremissaRepository, IConfiguracaoRepository
from shared.domain.value_objects import Money


@dataclass
class CriarPremissaDTO:
    categoria: str
    item: str
    custo_unitario: float
    margem_lucro: float = 0.18
    comissao: float = 0.05
    imposto: float = 0.0


class CriarPremissaUseCase:
    def __init__(self, repository: IPremissaRepository):
        self._repository = repository
    
    def execute(self, dto: CriarPremissaDTO) -> Premissa:
        premissa = Premissa(
            categoria=CategoriaProduto(dto.categoria),
            item=dto.item,
            custo_unitario=Money(dto.custo_unitario),
            margem_lucro=dto.margem_lucro,
            comissao=dto.comissao,
            imposto=dto.imposto
        )
        return self._repository.save(premissa)


class ObterPrecoPorItemUseCase:
    def __init__(self, premissa_repo: IPremissaRepository, config_repo: IConfiguracaoRepository):
        self._premissa_repo = premissa_repo
        self._config_repo = config_repo
    
    def execute(self, item: str, quantidade: int) -> dict:
        premissa = self._premissa_repo.find_by_item(item)
        
        if not premissa:
            raise ValueError(f"Item '{item}' não encontrado nas premissas")
        
        preco_unitario = premissa.calcular_preco_venda()
        custo_unitario = premissa.custo_unitario
        
        config = self._config_repo.get_configuracao_atual()
        
        custo_adicional = Money(0)
        if "painel" in item.lower() or "módulo" in item.lower():
            custo_adicional = config.montagem_por_painel * quantidade
        
        return {
            "item": item,
            "quantidade": quantidade,
            "preco_unitario": preco_unitario.value,
            "custo_unitario": custo_unitario.value,
            "preco_total": preco_unitario.value * quantidade,
            "custo_total": (custo_unitario.value * quantidade) + custo_adicional.value,
            "custo_adicional": custo_adicional.value
        }


class AtualizarConfiguracaoUseCase:
    def __init__(self, repository: IConfiguracaoRepository):
        self._repository = repository
    
    def execute(self, montagem_por_painel: float, custo_projeto: float, margem_lucro: float, comissao: float, imposto: float) -> ConfiguracaoGlobal:
        config = ConfiguracaoGlobal(
            montagem_por_painel=Money(montagem_por_painel),
            custo_projeto=Money(custo_projeto),
            margem_lucro_padrao=margem_lucro,
            comissao_padrao=comissao,
            imposto_padrao=imposto
        )
        return self._repository.save(config)
