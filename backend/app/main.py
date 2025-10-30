import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.future import select

# --- Imports para o script de startup ---
from app.db import async_session
from app.core.users.models import User, UserRole
from app.core.users.hashing import get_password_hash
from app.core.equipamentos import router as equipamentos_router
# ----------------------------------------

# --- Importação dos módulos de rotas (routers) ---
from app.core.auth import router as auth_router
from app.core.users import router as users_router
from app.core.clientes import router as clientes_router
from app.core.sales.propostas import router as propostas_router
from app.core.sales.projetos import router as projetos_router
from app.core.financeiro import router as financeiro_router
from app.core.dashboards import router as dashboards_router

# Inicializa a aplicação FastAPI principal
app = FastAPI(
    title="SunOps", 
    version="0.0.1",
    description="API central para o sistema de gerenciamento SunOps SaaS."
)

# --- FUNÇÃO DE STARTUP ---
@app.on_event("startup")
async def on_startup():
    """
    Executa na inicialização da API para garantir que o usuário Gestor
    padrão exista no banco de dados.
    """
    print("--- Executando evento de startup: Verificando Gestor Padrão ---")
    
    # 1. Ler credenciais do ambiente (passadas pelo docker-compose.yml)
    ADMIN_EMAIL = os.getenv("FIRST_ADMIN_EMAIL")
    ADMIN_PASSWORD = os.getenv("FIRST_ADMIN_PASSWORD")
    ADMIN_NAME = os.getenv("FIRST_ADMIN_NAME", "Gestor Padrão")

    if not ADMIN_EMAIL or not ADMIN_PASSWORD:
        print("AVISO: Variáveis FIRST_ADMIN_EMAIL ou FIRST_ADMIN_PASSWORD não definidas.")
        print("--- Startup concluído (sem verificação de gestor) ---")
        return

    # 2. Criar uma sessão de banco de dados
    async with async_session() as session:
        try:
            # 3. Verificar se o usuário já existe
            query = select(User).where(User.email == ADMIN_EMAIL)
            result = await session.execute(query)
            existing_user = result.scalars().first()
            
            if existing_user:
                print(f"Usuário Gestor '{ADMIN_EMAIL}' já existe. Pulando.")
            else:
                # 4. Se não existe, criar
                print(f"Criando usuário Gestor '{ADMIN_EMAIL}'...")
                hashed_password = get_password_hash(ADMIN_PASSWORD)
                
                admin_user = User(
                    name=ADMIN_NAME,
                    email=ADMIN_EMAIL,
                    password_hash=hashed_password,
                    role=UserRole.GESTOR # Garante que ele é Gestor
                )
                
                session.add(admin_user)
                await session.commit()
                print("Usuário Gestor criado com sucesso.")
        
        except Exception as e:
            print(f"ERRO no evento de startup ao verificar/criar gestor: {e}")
            await session.rollback()
        
    print("--- Evento de startup concluído ---")
# --- FIM DA FUNÇÃO DE STARTUP ---


# Isso é essencial para permitir que seu frontend (ex: React, Vue)
# acesse a API a partir de um domínio diferente.
app.add_middleware(
    CORSMiddleware,
    # Em produção, mude "*" para a URL do seu frontend (ex: "http://app.sunops.com.br")
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], # Permite todos os métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"], # Permite todos os cabeçalhos
)

@app.get("/", tags=["Health Check"])
async def read_root():
    """
    Endpoint raiz usado para verificar se a API está online 
    e respondendo (Health Check).
    """
    return {"status": "SunOps API is running!"}

# --- Inclusão dos Routers ---
app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(clientes_router.router)
app.include_router(propostas_router.router)
app.include_router(projetos_router.router)
app.include_router(financeiro_router.router)
app.include_router(dashboards_router.router)
app.include_router(equipamentos_router.router)