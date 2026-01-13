from ..ports.user_repository import IUserRepository
from ..dtos.auth_dtos import LoginDTO, TokenDTO

class LoginUserUseCase:
    """Use Case: Autenticar usuário"""
    def __init__(self, repository: IUserRepository, password_hasher, token_generator):
        self._repository = repository
        self._hasher = password_hasher
        self._token_gen = token_generator
    
    async def execute(self, dto: LoginDTO) -> TokenDTO:
        user = await self._repository.find_by_email(dto.email)
        if not user:
            raise ValueError("Credenciais inválidas")
        
        if not self._hasher.verify(dto.password, user["hashed_password"]):
            raise ValueError("Credenciais inválidas")
        
        if not user["is_active"]:
            raise ValueError("Usuário inativo")
        
        access = self._token_gen.create_access_token(str(user["id"]))
        refresh = self._token_gen.create_refresh_token(str(user["id"]))
        
        return TokenDTO(access_token=access, refresh_token=refresh)
