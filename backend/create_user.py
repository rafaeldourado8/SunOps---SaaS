import asyncio
from src.adapters.infrastructure.database.config import AsyncSessionLocal
from src.adapters.infrastructure.database.models import UserModel
from src.adapters.fastapi_app.security import PasswordHasher

async def create_user():
    async with AsyncSessionLocal() as session:
        hasher = PasswordHasher()
        user = UserModel(
            email='admin@sunops.com',
            hashed_password=hasher.hash('admin123'),
            full_name='Admin User',
            is_active=True,
            is_superuser=True
        )
        session.add(user)
        await session.commit()
        print('✅ Usuário criado com sucesso!')
        print('Email: admin@sunops.com')
        print('Senha: admin123')

if __name__ == '__main__':
    asyncio.run(create_user())
