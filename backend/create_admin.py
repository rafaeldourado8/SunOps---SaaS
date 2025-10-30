import asyncio
import os
import sys
from sqlalchemy.future import select
from dotenv import load_dotenv # Para carregar o .env

# Importe os componentes necessários da sua aplicação
from app.db import async_session
from app.core.users.models import User, UserRole
from app.core.users.hashing import get_password_hash

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- Lê os dados das variáveis de ambiente ---
ADMIN_EMAIL = os.getenv("FIRST_ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("FIRST_ADMIN_PASSWORD")
ADMIN_NAME = os.getenv("FIRST_ADMIN_NAME", "Gestor Padrão") # Usa "Gestor Padrão" se a variável de nome não existir
# ----------------------------------------------------

async def create_seed_admin():
    """
    Script para criar o primeiro usuário Gestor (Admin) lendo de variáveis de ambiente.
    """
    print("Iniciando script para criar usuário Gestor...")

    # --- Validação ---
    if not ADMIN_EMAIL or not ADMIN_PASSWORD:
        print("\nErro Crítico: As variáveis de ambiente 'FIRST_ADMIN_EMAIL' e 'FIRST_ADMIN_PASSWORD' não foram definidas.")
        print("Por favor, adicione-as ao seu arquivo .env e tente novamente.\n")
        return
    # -----------------

    # Inicia uma nova sessão assíncrona com o banco
    async with async_session() as session:
        
        # 1. Verifica se o usuário já existe
        query = select(User).where(User.email == ADMIN_EMAIL)
        result = await session.execute(query)
        existing_user = result.scalars().first()
        
        if existing_user:
            print(f"Erro: Usuário com e-mail '{ADMIN_EMAIL}' já existe.")
            return

        # 2. Se não existe, cria o novo usuário
        print(f"Criando novo usuário '{ADMIN_NAME}' com e-mail '{ADMIN_EMAIL}'...")
        
        # Hash da senha
        hashed_password = get_password_hash(ADMIN_PASSWORD)
        
        admin_user = User(
            name=ADMIN_NAME,
            email=ADMIN_EMAIL,
            password_hash=hashed_password,
            role=UserRole.GESTOR  # Define a permissão de Gestor
        )
        
        # Adiciona ao banco e commita
        session.add(admin_user)
        await session.commit()
        
        print("\n---")
        print("Usuário Gestor criado com sucesso!")
        print(f"E-mail: {ADMIN_EMAIL}")
        print(f"(Senha foi lida do .env e hasheada)")
        print("---\n")

if __name__ == "__main__":
    # Roda a função assíncrona
    asyncio.run(create_seed_admin())