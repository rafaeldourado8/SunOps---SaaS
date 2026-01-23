from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session
from uuid import UUID
from pydantic import BaseModel
from typing import Optional, List

from shared.infrastructure.database import get_db
from shared.infrastructure.message_broker import broker
from clientes.application.use_cases import CriarClienteUseCase, CriarClienteDTO, PromoverClienteUseCase
from clientes.infrastructure.repository import SQLAlchemyClienteRepository
from clientes.domain.entities import StatusCliente, TipoPessoa, Cliente
from shared.domain.value_objects import CPF, CNPJ, Email, Telefone, Endereco

router = APIRouter(prefix="/clientes", tags=["clientes"])


class ClienteRequest(BaseModel):
    nome: str
    email: str = None
    telefone: str = None
    cpf_cnpj: str = None
    endereco: str = None
    cidade: str = None
    estado: str = None
    cep: str = None


@router.post("/")
async def criar_cliente(request: ClienteRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    from usuarios.infrastructure.models import UsuarioModel
    from clientes.infrastructure.models import ClienteModel
    import uuid
    
    # Pegar primeiro vendedor disponível
    vendedor = db.query(UsuarioModel).first()
    if not vendedor:
        raise HTTPException(status_code=400, detail="Nenhum vendedor disponível")
    
    # Criar cliente diretamente no banco
    cliente = ClienteModel(
        id=uuid.uuid4(),
        nome=request.nome,
        tipo_pessoa="PF",
        telefone=request.telefone or "",
        email=request.email,
        cpf=request.cpf_cnpj,
        logradouro=request.endereco or "",
        numero="",
        cidade=request.cidade or "",
        estado=request.estado or "",
        cep=request.cep or "",
        consumo_mensal_kwh=0,
        valor_conta_luz=0,
        # CORREÇÃO: Usar Enum válido para evitar erro 500
        tipo_rede="MONOFASICO",
        status="LEAD",
        vendedor_id=vendedor.id
    )
    
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    
    return {"id": str(cliente.id), "nome": cliente.nome, "status": cliente.status}


@router.put("/{cliente_id}")
async def atualizar_cliente(cliente_id: UUID, request: ClienteRequest, db: Session = Depends(get_db)):
    repository = SQLAlchemyClienteRepository(db)
    cliente = repository.find_by_id(cliente_id)
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    try:
        # Atualiza campos simples
        cliente.nome = request.nome
        
        # Atualiza Value Objects (com validação)
        if request.email:
            cliente.email = Email(request.email)
            
        if request.telefone:
            cliente.telefone = Telefone(request.telefone)
            
        # Atualiza Endereço (Mantém dados antigos se não vierem novos)
        current_endereco = cliente.endereco
        logradouro = request.endereco if request.endereco is not None else (current_endereco.logradouro if current_endereco else "")
        cidade = request.cidade if request.cidade is not None else (current_endereco.cidade if current_endereco else "")
        estado = request.estado if request.estado is not None else (current_endereco.estado if current_endereco else "")
        cep = request.cep if request.cep is not None else (current_endereco.cep if current_endereco else "")
        
        cliente.endereco = Endereco(
            logradouro=logradouro,
            numero=current_endereco.numero if current_endereco else "S/N",
            cidade=cidade,
            estado=estado,
            cep=cep,
            complemento=current_endereco.complemento if current_endereco else None,
            bairro=current_endereco.bairro if current_endereco else None
        )

        # Atualiza CPF/CNPJ e Tipo Pessoa logicamente
        if request.cpf_cnpj:
            clean_doc = request.cpf_cnpj.replace(".", "").replace("-", "").replace("/", "")
            if len(clean_doc) > 11:
                cliente.cnpj = CNPJ(clean_doc)
                cliente.cpf = None
                cliente.tipo_pessoa = TipoPessoa.JURIDICA
            else:
                cliente.cpf = CPF(clean_doc)
                cliente.cnpj = None
                cliente.tipo_pessoa = TipoPessoa.FISICA

        repository.save(cliente)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    return {"id": cliente.id, "nome": cliente.nome, "status": cliente.status.value}


@router.post("/{cliente_id}/promover")
async def promover_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    repository = SQLAlchemyClienteRepository(db)
    use_case = PromoverClienteUseCase(repository)
    cliente = use_case.execute(cliente_id)
    return {"id": cliente.id, "status": cliente.status.value}


@router.get("/")
async def listar_clientes(
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    repository = SQLAlchemyClienteRepository(db)
    
    if status:
        try:
            status_enum = StatusCliente(status.upper())
            clientes = repository.find_by_status(status_enum)
        except ValueError:
            opcoes = [e.value for e in StatusCliente]
            raise HTTPException(
                status_code=400, 
                detail=f"Status inválido. Opções permitidas: {opcoes}"
            )
    else:
        clientes = repository.list_all()
        
    return [{"id": c.id, "nome": c.nome, "status": c.status.value, "email": c.email, "telefone": c.telefone} for c in clientes]


@router.get("/{cliente_id}")
async def obter_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    repository = SQLAlchemyClienteRepository(db)
    cliente = repository.find_by_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"id": cliente.id, "nome": cliente.nome, "status": cliente.status.value}


@router.delete("/{cliente_id}", status_code=204)
async def excluir_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    repository = SQLAlchemyClienteRepository(db)
    cliente = repository.find_by_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    repository.delete(cliente_id)
    return