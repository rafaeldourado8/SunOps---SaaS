from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from uuid import UUID
import os
import shutil

from shared.infrastructure.database import get_db
from contratos.infrastructure.repository import SQLAlchemyTemplateRepository
from contratos.application.use_cases import SalvarTemplateUseCase, SalvarTemplateDTO, ListarTemplatesUseCase

router = APIRouter(prefix="/templates", tags=["templates"])

UPLOAD_DIR = "uploads/templates"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/")
async def upload_template(
    file: UploadFile = File(...),
    tipo: str = Form(...),
    nome: str = Form(...),
    vendedor_id: str = Form(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são permitidos")
    
    # Nome seguro para o arquivo
    safe_filename = f"{vendedor_id}_{file.filename.replace(' ', '_')}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    repository = SQLAlchemyTemplateRepository(db)
    use_case = SalvarTemplateUseCase(repository)
    
    try:
        vendedor_uuid = UUID(vendedor_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID do vendedor inválido")
    
    dto = SalvarTemplateDTO(
        tipo=tipo,
        nome=nome,
        arquivo_path=file_path,
        vendedor_id=vendedor_uuid
    )
    
    template = use_case.execute(dto)
    
    return {
        "id": template.id,
        "tipo": template.tipo.value,
        "nome": template.nome,
        "arquivo_path": template.arquivo_path
    }


@router.get("/")
async def listar_templates(vendedor_id: str = None, db: Session = Depends(get_db)):
    repository = SQLAlchemyTemplateRepository(db)
    use_case = ListarTemplatesUseCase(repository)
    
    v_id = None
    if vendedor_id:
        try:
            v_id = UUID(vendedor_id)
        except ValueError:
            pass 

    templates = use_case.execute(v_id)
    
    return [
        {
            "id": t.id,
            "tipo": t.tipo.value,
            "nome": t.nome,
            "ativo": t.ativo
        }
        for t in templates
    ]


@router.get("/{template_id}")
async def obter_template(template_id: UUID, db: Session = Depends(get_db)):
    repository = SQLAlchemyTemplateRepository(db)
    template = repository.find_by_id(template_id)
    
    if not template:
        raise HTTPException(status_code=404, detail="Template não encontrado")
    
    return {
        "id": template.id,
        "tipo": template.tipo.value,
        "nome": template.nome,
        "arquivo_path": template.arquivo_path,
        "ativo": template.ativo
    }


@router.get("/{template_id}/arquivo")
async def baixar_template_arquivo(template_id: UUID, db: Session = Depends(get_db)):
    repository = SQLAlchemyTemplateRepository(db)
    template = repository.find_by_id(template_id)
    
    if not template:
        raise HTTPException(status_code=404, detail="Template não encontrado")
        
    if not os.path.exists(template.arquivo_path):
        raise HTTPException(status_code=404, detail="Arquivo físico não encontrado no servidor")
        
    return FileResponse(template.arquivo_path, media_type='application/pdf', filename=f"{template.nome}.pdf")


@router.delete("/{template_id}", status_code=204)
async def excluir_template(template_id: UUID, db: Session = Depends(get_db)):
    repository = SQLAlchemyTemplateRepository(db)
    template = repository.find_by_id(template_id)
    
    if not template:
        raise HTTPException(status_code=404, detail="Template não encontrado")
    
    repository.delete(template_id)
    return