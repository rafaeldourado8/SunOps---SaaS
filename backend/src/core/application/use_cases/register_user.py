from ..ports.user_repository import IUserRepository
from ..dtos.auth_dtos import RegisterDTO, UserDTO

class RegisterUserUseCase:
    """Use Case: Registrar novo usuário"""
    def __init__(self, repository: IUserRepository, password_hasher):
        self._repository = repository
        self._hasher = password_hasher
    
    async def execute(self, dto: RegisterDTO) -> UserDTO:
        existing = await self._repository.find_by_email(dto.email)
        if existing:
            raise ValueError("Email já cadastrado")
        
        hashed = self._hasher.hash(dto.password)
        user = await self._repository.create(dto.email, hashed, dto.full_name)
        return UserDTO(**user)
