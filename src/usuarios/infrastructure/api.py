from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Dict, Any

from shared.infrastructure.database import get_db
from usuarios.infrastructure.models import UsuarioModel
from usuarios.infrastructure.estado_repository import UsuarioEstadoRepository
from usuarios.application.estado_use_cases import GerenciarEstadoUsuario

router = APIRouter(prefix="/auth", tags=["auth"])
router_estado = APIRouter(prefix="/usuarios/estado", tags=["usuario-estado"])

SECRET_KEY = "sunops-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 240

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict


class EstadoRequest(BaseModel):
    chave: str
    valor: Any


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UsuarioModel).filter(UsuarioModel.email == form_data.username).first()
    
    if not user or not pwd_context.verify(form_data.password, user.senha_hash):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    if not user.ativo:
        raise HTTPException(status_code=403, detail="Usuário inativo")
    
    access_token = create_access_token(data={"sub": user.email, "id": str(user.id), "tipo": user.tipo})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "name": user.nome,
            "email": user.email,
            "tipo": user.tipo
        }
    }


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    user = db.query(UsuarioModel).filter(UsuarioModel.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    
    return user


@router.get("/me")
async def get_me(current_user: UsuarioModel = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "name": current_user.nome,
        "email": current_user.email,
        "tipo": current_user.tipo
    }


# Endpoints de Estado do Usuário
@router_estado.post("/preferencia")
async def salvar_preferencia(
    request: EstadoRequest,
    current_user: UsuarioModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repo = UsuarioEstadoRepository(db)
    use_case = GerenciarEstadoUsuario(repo)
    use_case.salvar_preferencia(str(current_user.id), request.chave, request.valor)
    return {"message": "Preferência salva"}


@router_estado.get("/preferencia/{chave}")
async def obter_preferencia(
    chave: str,
    current_user: UsuarioModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repo = UsuarioEstadoRepository(db)
    use_case = GerenciarEstadoUsuario(repo)
    valor = use_case.obter_preferencia(str(current_user.id), chave)
    return {"chave": chave, "valor": valor}


@router_estado.post("/filtro/{tela}")
async def salvar_filtro(
    tela: str,
    filtros: Dict[str, Any],
    current_user: UsuarioModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repo = UsuarioEstadoRepository(db)
    use_case = GerenciarEstadoUsuario(repo)
    use_case.salvar_filtro(str(current_user.id), tela, filtros)
    return {"message": "Filtros salvos"}


@router_estado.get("/filtro/{tela}")
async def obter_filtro(
    tela: str,
    current_user: UsuarioModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repo = UsuarioEstadoRepository(db)
    use_case = GerenciarEstadoUsuario(repo)
    filtros = use_case.obter_filtro(str(current_user.id), tela)
    return {"tela": tela, "filtros": filtros}


@router_estado.post("/dashboard")
async def salvar_dashboard(
    config: Dict[str, Any],
    current_user: UsuarioModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repo = UsuarioEstadoRepository(db)
    use_case = GerenciarEstadoUsuario(repo)
    use_case.salvar_dashboard(str(current_user.id), config)
    return {"message": "Dashboard salvo"}


@router_estado.get("/dashboard")
async def obter_dashboard(
    current_user: UsuarioModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repo = UsuarioEstadoRepository(db)
    use_case = GerenciarEstadoUsuario(repo)
    config = use_case.obter_dashboard(str(current_user.id))
    return {"config": config}


@router_estado.get("/todos")
async def obter_todos_estados(
    current_user: UsuarioModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repo = UsuarioEstadoRepository(db)
    use_case = GerenciarEstadoUsuario(repo)
    estados = use_case.obter_todos_estados(str(current_user.id))
    return estados


@router_estado.delete("/limpar")
async def limpar_estados(
    current_user: UsuarioModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repo = UsuarioEstadoRepository(db)
    use_case = GerenciarEstadoUsuario(repo)
    count = use_case.limpar_estados(str(current_user.id))
    return {"message": f"{count} estados removidos"}
