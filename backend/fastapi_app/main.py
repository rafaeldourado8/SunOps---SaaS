from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import django

# Setup Django antes de importar models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shared.infrastructure.tenant.middleware import TenantMiddleware
from fastapi_app.routers import auth, clientes, fornecedores, marcas, dashboard, chat, orcamentos, financeiro

app = FastAPI(
    title="OPS CRM API",
    version="1.0.0",
    description="API multi-tenant para CRM de energia solar"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tenant Resolution
app.add_middleware(TenantMiddleware)

# Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(clientes.router, prefix="/api/v1/clientes", tags=["Clientes"])
app.include_router(fornecedores.router, prefix="/api/v1/fornecedores", tags=["Fornecedores"])
app.include_router(marcas.router, prefix="/api/v1/marcas", tags=["Marcas"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])
app.include_router(financeiro.router, tags=["Financeiro"])
app.include_router(orcamentos.router, tags=["Orçamentos"])
app.include_router(chat.router, tags=["Chat"])

# Static files
app.mount("/static", StaticFiles(directory="fastapi_app/static"), name="static")


@app.get("/")
async def root():
    return {"message": "OPS CRM API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "ok"}
