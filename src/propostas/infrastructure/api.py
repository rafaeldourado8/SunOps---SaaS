from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from uuid import UUID
from pydantic import BaseModel
import os

from shared.infrastructure.database import get_db
from shared.infrastructure.message_broker import broker
from shared.infrastructure.pdf_generator import PDFDocument

from propostas.application.use_cases import (
    CriarPropostaUseCase, CriarPropostaDTO, 
    AdicionarItemPropostaUseCase, AdicionarItemDTO, 
    SolicitarDescontoUseCase, GerarPDFPropostaUseCase,
    ExcluirPropostaUseCase, AtualizarPropostaUseCase, AtualizarPropostaDTO
)
from propostas.infrastructure.repository import SQLAlchemyPropostaRepository
from propostas.infrastructure.pdf_proposta_generator import PropostaPDFGenerator

from premissas.application.use_cases import ObterPrecoPorItemUseCase
from premissas.infrastructure.repository import SQLAlchemyPremissaRepository, SQLAlchemyConfiguracaoRepository
from clientes.infrastructure.repository import SQLAlchemyClienteRepository

router = APIRouter(prefix="/propostas", tags=["propostas"])

# --- Requests ---
class PropostaRequest(BaseModel):
    cliente_id: str

class ItemRequest(BaseModel):
    nome: str
    quantidade: int

class DescontoRequest(BaseModel):
    valor: float
    motivo: str
    solicitante_id: UUID

class AtualizarPropostaRequest(BaseModel):
    status: str

# --- Rotas ---

@router.post("/")
async def criar_proposta(request: PropostaRequest, db: Session = Depends(get_db)):
    from usuarios.infrastructure.models import UsuarioModel
    import uuid
    
    # Busca um vendedor padrão (idealmente viria do token de auth)
    vendedor = db.query(UsuarioModel).first()
    if not vendedor:
        raise HTTPException(status_code=400, detail="Nenhum vendedor disponível no sistema")
    
    repository = SQLAlchemyPropostaRepository(db)
    use_case = CriarPropostaUseCase(repository)
    
    try:
        dto = CriarPropostaDTO(
            vendedor_id=vendedor.id,
            cliente_id=UUID(request.cliente_id),
            potencia_sistema_kwp=0.0 
        )
        proposta = use_case.execute(dto)
        return {"id": str(proposta.id), "status": proposta.status.value}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{proposta_id}")
async def atualizar_proposta(proposta_id: UUID, request: AtualizarPropostaRequest, db: Session = Depends(get_db)):
    repository = SQLAlchemyPropostaRepository(db)
    use_case = AtualizarPropostaUseCase(repository)
    
    try:
        dto = AtualizarPropostaDTO(
            id=proposta_id,
            status=request.status
        )
        proposta = use_case.execute(dto)
        return {"id": proposta.id, "status": proposta.status.value}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{proposta_id}/itens")
async def adicionar_item(proposta_id: UUID, request: ItemRequest, db: Session = Depends(get_db)):
    # 1. Calcular preço com base nas premissas
    premissa_repo = SQLAlchemyPremissaRepository(db)
    config_repo = SQLAlchemyConfiguracaoRepository(db)
    preco_use_case = ObterPrecoPorItemUseCase(premissa_repo, config_repo)
    
    try:
        preco_info = preco_use_case.execute(request.nome, request.quantidade)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao calcular preço: {str(e)}")
    
    # 2. Adicionar item à proposta
    repository = SQLAlchemyPropostaRepository(db)
    use_case = AdicionarItemPropostaUseCase(repository)
    
    dto = AdicionarItemDTO(
        proposta_id=proposta_id,
        nome=request.nome,
        quantidade=request.quantidade,
        preco_unitario=preco_info['preco_unitario'],
        custo_unitario=preco_info['custo_unitario']
    )
    
    proposta = use_case.execute(dto)
    
    return {
        "id": proposta.id,
        "total_itens": len(proposta.itens),
        "valor_total": proposta.calcular_valor_total().value,
        "item_adicionado": request.nome
    }


@router.post("/{proposta_id}/desconto")
async def solicitar_desconto(proposta_id: UUID, request: DescontoRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    repository = SQLAlchemyPropostaRepository(db)
    use_case = SolicitarDescontoUseCase(repository)
    
    try:
        proposta = use_case.execute(
            proposta_id=proposta_id, 
            valor=request.valor, 
            motivo=request.motivo, 
            solicitante_id=request.solicitante_id
        )
        # Notificar via Broker (se configurado)
        background_tasks.add_task(broker.publish, "desconto_solicitado", {"proposta_id": str(proposta.id), "valor": request.valor})
        
        return {"id": proposta.id, "status": proposta.status.value}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
async def listar_propostas(db: Session = Depends(get_db)):
    repository = SQLAlchemyPropostaRepository(db)
    cliente_repo = SQLAlchemyClienteRepository(db)
    
    propostas = repository.find_all()
    
    # Enriquecer com nome do cliente
    resultado = []
    for p in propostas:
        cliente = cliente_repo.find_by_id(p.cliente_id)
        cliente_nome = cliente.nome if cliente else "Desconhecido"
        
        resultado.append({
            "id": p.id,
            "cliente_nome": cliente_nome,
            "status": p.status.value,
            "valor_total": p.calcular_valor_total().value,
            "potencia": p.potencia_sistema_kwp,
            "data": p.created_at
        })
        
    return resultado


@router.get("/{proposta_id}")
async def obter_proposta(proposta_id: UUID, db: Session = Depends(get_db)):
    repository = SQLAlchemyPropostaRepository(db)
    cliente_repo = SQLAlchemyClienteRepository(db)
    
    proposta = repository.find_by_id(proposta_id)
    if not proposta:
        raise HTTPException(status_code=404, detail="Proposta não encontrada")
        
    cliente = cliente_repo.find_by_id(proposta.cliente_id)
    
    return {
        "id": proposta.id,
        "cliente_id": proposta.cliente_id,
        "cliente_nome": cliente.nome if cliente else "Desconhecido",
        "status": proposta.status.value,
        "potencia": proposta.potencia_sistema_kwp,
        "valor_total": proposta.calcular_valor_total().value,
        "itens": [
            {
                "nome": i.nome,
                "quantidade": i.quantidade,
                "preco_unitario": i.preco_unitario.value,
                "total": i.calcular_total_preco().value
            } for i in proposta.itens
        ],
        "desconto": {
            "valor": proposta.desconto.valor.value,
            "motivo": proposta.desconto.motivo
        } if proposta.desconto else None
    }


@router.get("/{proposta_id}/pdf")
async def gerar_pdf_proposta(proposta_id: UUID, db: Session = Depends(get_db)):
    # Repositórios necessários
    proposta_repo = SQLAlchemyPropostaRepository(db)
    cliente_repo = SQLAlchemyClienteRepository(db)
    
    # Buscar dados
    proposta = proposta_repo.find_by_id(proposta_id)
    if not proposta:
        raise HTTPException(status_code=404, detail="Proposta não encontrada")
        
    cliente = cliente_repo.find_by_id(proposta.cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente associado não encontrado")
    
    # Gerar PDF
    generator = PropostaPDFGenerator()
    use_case = GerarPDFPropostaUseCase(generator)
    
    output_path = f"uploads/propostas/proposta_{proposta.id}.pdf"
    os.makedirs("uploads/propostas", exist_ok=True)
    
    path = use_case.execute(proposta, cliente.nome, output_path)
    
    return FileResponse(path, media_type='application/pdf', filename=f"Proposta_{cliente.nome}.pdf")


@router.delete("/{proposta_id}", status_code=204)
async def excluir_proposta(proposta_id: UUID, db: Session = Depends(get_db)):
    repository = SQLAlchemyPropostaRepository(db)
    use_case = ExcluirPropostaUseCase(repository)
    try:
        use_case.execute(proposta_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return