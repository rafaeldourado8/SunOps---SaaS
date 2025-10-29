from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.core.users.models import User, UserRole
# Importa a dependência de login base
from app.core.auth.dependencies import get_current_user 
from . import services, schema

router = APIRouter(tags=['Dashboards'], prefix='/dashboard')

@router.get(
    '/', 
    # O tipo de resposta pode ser um ou outro
    response_model=schema.DashboardGestor | schema.DashboardVendedor
)
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
    # Pega o usuário logado, seja ele Gestor ou Vendedor
    current_user: User = Depends(get_current_user)
):
    '''
    Retorna o dashboard apropriado para o "role" do usuário logado.
    - Gestor: Vê o dashboard global.
    - Vendedor: Vê o dashboard pessoal.
    '''
    
    # AQUI ESTÁ A LÓGICA DE PERMISSÃO (RBAC)
    if current_user.role == UserRole.GESTOR:
        return await services.build_gestor_dashboard(db)
    
    elif current_user.role == UserRole.VENDEDOR:
        return await services.build_vendedor_dashboard(db, current_user)
    
    else:
        # Ex: "Suporte" ou outros roles não têm dashboard
        raise HTTPException(
            status_code=403, 
            detail="Seu perfil não possui um dashboard."
        )