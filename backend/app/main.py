from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

