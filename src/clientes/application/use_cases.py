from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from ..domain.entities import Cliente, TipoPessoa, StatusCliente, TipoRede, DadosEnergeticos
from ..domain.repository import IClienteRepository
from shared.domain.value_objects import CPF, CNPJ, Email, Telefone, Endereco, Money


@dataclass
class CriarClienteDTO:
    nome: str
    tipo_pessoa: str
    telefone: str
    logradouro: str
    numero: str
    cidade: str
    estado: str
    cep: str
    consumo_mensal_kwh: float
    valor_conta_luz: float
    tipo_rede: str
    vendedor_id: UUID
    email: Optional[str] = None
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    rg: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None


@dataclass
class AtualizarClienteDTO:
    id: UUID
    nome: str
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    cpf_cnpj: Optional[str] = None


class CriarClienteUseCase:
    def __init__(self, repository: IClienteRepository):
        self._repository = repository
    
    def execute(self, dto: CriarClienteDTO) -> Cliente:
        if dto.cpf:
            existing = self._repository.find_by_cpf(dto.cpf)
            if existing:
                raise ValueError("CPF já cadastrado")
        
        if dto.cnpj:
            existing = self._repository.find_by_cnpj(dto.cnpj)
            if existing:
                raise ValueError("CNPJ já cadastrado")
        
        endereco = Endereco(
            logradouro=dto.logradouro,
            numero=dto.numero,
            cidade=dto.cidade,
            estado=dto.estado,
            cep=dto.cep,
            complemento=dto.complemento,
            bairro=dto.bairro
        )
        
        dados_energeticos = DadosEnergeticos(
            consumo_mensal_kwh=dto.consumo_mensal_kwh,
            valor_conta_luz=Money(dto.valor_conta_luz),
            tipo_rede=TipoRede(dto.tipo_rede)
        )
        
        cliente = Cliente(
            nome=dto.nome,
            tipo_pessoa=TipoPessoa(dto.tipo_pessoa),
            telefone=Telefone(dto.telefone),
            endereco=endereco,
            dados_energeticos=dados_energeticos,
            vendedor_id=dto.vendedor_id,
            email=Email(dto.email) if dto.email else None,
            cpf=CPF(dto.cpf) if dto.cpf else None,
            cnpj=CNPJ(dto.cnpj) if dto.cnpj else None,
            rg=dto.rg
        )
        
        return self._repository.save(cliente)


class AtualizarClienteUseCase:
    def __init__(self, repository: IClienteRepository):
        self._repository = repository
    
    def execute(self, dto: AtualizarClienteDTO) -> Cliente:
        cliente = self._repository.find_by_id(dto.id)
        if not cliente:
            raise ValueError("Cliente não encontrado")
            
        cliente.nome = dto.nome
        
        if dto.email:
            cliente.email = Email(dto.email)
        
        if dto.telefone:
            cliente.telefone = Telefone(dto.telefone)
            
        # Lógica de atualização de endereço e documentos simplificada
        # Idealmente, o DTO deveria vir estruturado, mas mantendo compatibilidade:
        if any([dto.endereco, dto.cidade, dto.estado, dto.cep]):
            current = cliente.endereco
            cliente.endereco = Endereco(
                logradouro=dto.endereco or (current.logradouro if current else ""),
                numero=current.numero if current else "S/N",
                cidade=dto.cidade or (current.cidade if current else ""),
                estado=dto.estado or (current.estado if current else ""),
                cep=dto.cep or (current.cep if current else ""),
                complemento=current.complemento if current else None,
                bairro=current.bairro if current else None
            )

        if dto.cpf_cnpj:
            clean_doc = dto.cpf_cnpj.replace(".", "").replace("-", "").replace("/", "")
            if len(clean_doc) > 11:
                cliente.cnpj = CNPJ(clean_doc)
                cliente.cpf = None
                cliente.tipo_pessoa = TipoPessoa.JURIDICA
            else:
                cliente.cpf = CPF(clean_doc)
                cliente.cnpj = None
                cliente.tipo_pessoa = TipoPessoa.FISICA
        
        return self._repository.save(cliente)


class PromoverClienteUseCase:
    def __init__(self, repository: IClienteRepository):
        self._repository = repository
    
    def execute(self, cliente_id: UUID) -> Cliente:
        cliente = self._repository.find_by_id(cliente_id)
        if not cliente:
            raise ValueError("Cliente não encontrado")
        
        cliente.promover_para_prospect()
        return self._repository.save(cliente)


class ExcluirClienteUseCase:
    def __init__(self, repository: IClienteRepository):
        self._repository = repository
    
    def execute(self, cliente_id: UUID) -> None:
        cliente = self._repository.find_by_id(cliente_id)
        if not cliente:
            raise ValueError("Cliente não encontrado")
        
        self._repository.delete(cliente_id)