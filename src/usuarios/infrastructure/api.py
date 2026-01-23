from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel

from shared.infrastructure.database import get_db
from usuarios.infrastructure.models import UsuarioModel

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "sunops-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 240

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict


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
