from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address
from ...infrastructure.database.config import get_session
from ...infrastructure.repositories.user_repository import UserRepository
from ....core.application.use_cases.register_user import RegisterUserUseCase
from ....core.application.use_cases.login_user import LoginUserUseCase
from ....core.application.dtos.auth_dtos import RegisterDTO, LoginDTO, TokenDTO, UserDTO
from ..security import PasswordHasher, TokenGenerator
import os

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
security = HTTPBearer()
limiter = Limiter(key_func=get_remote_address)

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
hasher = PasswordHasher()
token_gen = TokenGenerator(SECRET_KEY)

@router.post("/register", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register(
    request: Request,
    dto: RegisterDTO,
    session: AsyncSession = Depends(get_session)
):
    repo = UserRepository(session)
    use_case = RegisterUserUseCase(repo, hasher)
    try:
        return await use_case.execute(dto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenDTO)
@limiter.limit("10/minute")
async def login(
    request: Request,
    dto: LoginDTO,
    session: AsyncSession = Depends(get_session)
):
    repo = UserRepository(session)
    use_case = LoginUserUseCase(repo, hasher, token_gen)
    try:
        return await use_case.execute(dto)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> dict:
    try:
        payload = token_gen.decode(credentials.credentials)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        repo = UserRepository(session)
        from uuid import UUID
        user = await repo.find_by_id(UUID(user_id))
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        
        return user
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro no get_current_user: {e}")
        raise HTTPException(status_code=401, detail=f"Token inválido: {str(e)}")

@router.get("/me", response_model=UserDTO)
async def get_me(user: dict = Depends(get_current_user)):
    return UserDTO(**user)
