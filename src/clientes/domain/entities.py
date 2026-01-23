from dataclasses import dataclass
from enum import Enum
from typing import Optional
from uuid import UUID

from shared.domain.entity import Entity
from shared.domain.value_objects import CPF, CNPJ, Email, Telefone, Endereco, Money


class TipoPessoa(Enum):
    FISICA = "PF"
    JURIDICA = "PJ"


class StatusCliente(Enum):
    LEAD = "LEAD"
    PROSPECT = "PROSPECT"
    CLIENTE = "CLIENTE"
    PERDIDO = "PERDIDO"


class TipoRede(Enum):
    MONOFASICO = "MONOFASICO"
    BIFASICO = "BIFASICO"
    TRIFASICO = "TRIFASICO"


@dataclass
class DadosEnergeticos:
    consumo_mensal_kwh: float
    valor_conta_luz: Money
    tipo_rede: TipoRede
    
    def calcular_tarifa_media(self) -> float:
        if self.consumo_mensal_kwh == 0:
            return 0
        return self.valor_conta_luz.value / self.consumo_mensal_kwh


@dataclass
class Cliente(Entity):
    nome: str = ""
    tipo_pessoa: TipoPessoa = TipoPessoa.FISICA
    telefone: Telefone = None
    endereco: Endereco = None
    dados_energeticos: DadosEnergeticos = None
    vendedor_id: UUID = None
    status: StatusCliente = StatusCliente.LEAD
    email: Optional[Email] = None
    cpf: Optional[CPF] = None
    cnpj: Optional[CNPJ] = None
    rg: Optional[str] = None
    notas_internas: str = ""
    
    def __post_init__(self):
        pass
    
    def validar_para_contrato(self):
        """Valida se o cliente tem os dados necessários para criar um contrato"""
        if self.tipo_pessoa == TipoPessoa.FISICA and not self.cpf:
            raise ValueError("CPF obrigatório para criar contrato de pessoa física")
        if self.tipo_pessoa == TipoPessoa.JURIDICA and not self.cnpj:
            raise ValueError("CNPJ obrigatório para criar contrato de pessoa jurídica")
    
    def promover_para_prospect(self):
        if self.status != StatusCliente.LEAD:
            raise ValueError("Apenas LEADs podem ser promovidos a PROSPECT")
        self.status = StatusCliente.PROSPECT
    
    def converter_em_cliente(self):
        if self.status not in [StatusCliente.LEAD, StatusCliente.PROSPECT]:
            raise ValueError("Status inválido para conversão")
        self.status = StatusCliente.CLIENTE
    
    def marcar_como_perdido(self):
        self.status = StatusCliente.PERDIDO