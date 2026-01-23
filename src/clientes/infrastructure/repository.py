from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime

from ..domain.entities import Cliente, StatusCliente, TipoPessoa, TipoRede, DadosEnergeticos
from ..domain.repository import IClienteRepository
from .models import ClienteModel
from shared.domain.value_objects import CPF, CNPJ, Email, Telefone, Endereco, Money


class SQLAlchemyClienteRepository(IClienteRepository):
    
    def __init__(self, db: Session):
        self.db = db
    
    def save(self, entity: Cliente) -> Cliente:
        model = self.db.query(ClienteModel).filter(ClienteModel.id == entity.id).first()
        
        if model:
            self._update_model(model, entity)
        else:
            model = self._to_model(entity)
            self.db.add(model)
        
        self.db.commit()
        self.db.refresh(model)
        return entity
    
    def find_by_id(self, id: UUID) -> Optional[Cliente]:
        model = self.db.query(ClienteModel).filter(ClienteModel.id == id).first()
        return self._to_entity(model) if model else None
    
    def find_by_cpf(self, cpf: str) -> Optional[Cliente]:
        model = self.db.query(ClienteModel).filter(ClienteModel.cpf == cpf).first()
        return self._to_entity(model) if model else None
    
    def find_by_cnpj(self, cnpj: str) -> Optional[Cliente]:
        model = self.db.query(ClienteModel).filter(ClienteModel.cnpj == cnpj).first()
        return self._to_entity(model) if model else None
    
    def find_by_vendedor(self, vendedor_id: UUID) -> List[Cliente]:
        models = self.db.query(ClienteModel).filter(ClienteModel.vendedor_id == vendedor_id).all()
        return [self._to_entity(m) for m in models]
    
    def find_by_status(self, status: StatusCliente) -> List[Cliente]:
        models = self.db.query(ClienteModel).filter(ClienteModel.status == status.value).all()
        return [self._to_entity(m) for m in models]
    
    def find_all(self) -> List[Cliente]:
        models = self.db.query(ClienteModel).all()
        return [self._to_entity(m) for m in models]
    
    def list_all(self) -> List[Cliente]:
        return self.find_all()
    
    def delete(self, id: UUID) -> None:
        self.db.query(ClienteModel).filter(ClienteModel.id == id).delete()
        self.db.commit()
    
    def _to_model(self, entity: Cliente) -> ClienteModel:
        return ClienteModel(
            id=entity.id,
            nome=entity.nome,
            tipo_pessoa=entity.tipo_pessoa.value,
            cpf=entity.cpf.value if entity.cpf else None,
            cnpj=entity.cnpj.value if entity.cnpj else None,
            rg=entity.rg,
            email=entity.email.value if entity.email else None,
            telefone=entity.telefone.value,
            logradouro=entity.endereco.logradouro if entity.endereco else None,
            numero=entity.endereco.numero if entity.endereco else None,
            complemento=entity.endereco.complemento if entity.endereco else None,
            bairro=entity.endereco.bairro if entity.endereco else None,
            cidade=entity.endereco.cidade if entity.endereco else None,
            estado=entity.endereco.estado if entity.endereco else None,
            cep=entity.endereco.cep if entity.endereco else None,
            consumo_mensal_kwh=entity.dados_energeticos.consumo_mensal_kwh if entity.dados_energeticos else 0,
            valor_conta_luz=entity.dados_energeticos.valor_conta_luz.value if entity.dados_energeticos else 0,
            tipo_rede=entity.dados_energeticos.tipo_rede.value if entity.dados_energeticos else "BIFASICO",
            status=entity.status.value,
            vendedor_id=entity.vendedor_id,
            notas_internas=entity.notas_internas
        )
    
    def _update_model(self, model: ClienteModel, entity: Cliente):
        # Campos básicos
        model.nome = entity.nome
        model.status = entity.status.value
        model.tipo_pessoa = entity.tipo_pessoa.value
        model.notas_internas = entity.notas_internas
        
        # Value Objects (Extrair valores para o banco)
        if entity.telefone:
            model.telefone = entity.telefone.value
        if entity.email:
            model.email = entity.email.value
        
        # Documentos
        model.cpf = entity.cpf.value if entity.cpf else None
        model.cnpj = entity.cnpj.value if entity.cnpj else None
        model.rg = entity.rg
        
        # Endereço
        if entity.endereco:
            model.logradouro = entity.endereco.logradouro
            model.numero = entity.endereco.numero
            model.complemento = entity.endereco.complemento
            model.bairro = entity.endereco.bairro
            model.cidade = entity.endereco.cidade
            model.estado = entity.endereco.estado
            model.cep = entity.endereco.cep
            
        # Dados Energéticos
        if entity.dados_energeticos:
            model.consumo_mensal_kwh = entity.dados_energeticos.consumo_mensal_kwh
            model.valor_conta_luz = entity.dados_energeticos.valor_conta_luz.value
            model.tipo_rede = entity.dados_energeticos.tipo_rede.value
            
        model.updated_at = datetime.now()
    
    def _to_entity(self, model: ClienteModel) -> Cliente:
        return Cliente(
            id=model.id,
            nome=model.nome,
            tipo_pessoa=TipoPessoa(model.tipo_pessoa),
            telefone=Telefone(model.telefone),
            endereco=Endereco(
                logradouro=model.logradouro or "",
                numero=model.numero or "S/N",
                cidade=model.cidade or "",
                estado=model.estado or "",
                cep=model.cep or "",
                complemento=model.complemento,
                bairro=model.bairro
            ),
            dados_energeticos=DadosEnergeticos(
                consumo_mensal_kwh=model.consumo_mensal_kwh,
                valor_conta_luz=Money(model.valor_conta_luz),
                tipo_rede=TipoRede(model.tipo_rede)
            ),
            vendedor_id=model.vendedor_id,
            status=StatusCliente(model.status),
            email=Email(model.email) if model.email else None,
            cpf=CPF(model.cpf) if model.cpf else None,
            cnpj=CNPJ(model.cnpj) if model.cnpj else None,
            rg=model.rg,
            notas_internas=model.notas_internas,
            created_at=model.created_at,
            updated_at=model.updated_at
        )