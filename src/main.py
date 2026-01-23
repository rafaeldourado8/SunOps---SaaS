from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from clientes.infrastructure.api import router as clientes_router
from propostas.infrastructure.api import router as propostas_router
from premissas.infrastructure.api import router as premissas_router
from contratos.infrastructure.api import router as templates_router
from usuarios.infrastructure.api import router as auth_router
from shared.infrastructure.database import engine, Base

app = FastAPI(title="SunOPS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https?://.*",  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(clientes_router)
app.include_router(propostas_router)
app.include_router(premissas_router)
app.include_router(templates_router)


@app.get("/")
async def root():
    return {"message": "SunOPS API - DDD Architecture"}


@app.get("/health")
async def health():
    return {"status": "healthy"}