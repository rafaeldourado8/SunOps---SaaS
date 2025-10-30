# Em app/core/sales/propostas/services.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload # Adicionar selectinload
from typing import List, Optional
from decimal import Decimal # Adicionar Decimal

from . import models, schema
from app.core.users.models import User
# Importar o modelo do Kit para buscar o custo
from app.core.equipamentos.models import Kit 

async def create_proposta(
    db: AsyncSession, 
    proposta: schema.PropostaCreate, 
    vendedor_id: int
) -> models.Proposta:
    '''Cria uma nova proposta no banco'''
    
    # Extrai os 'itens' do dump
    proposta_data = proposta.model_dump()
    itens_data = proposta_data.pop('itens', [])
    
    db_proposta = models.Proposta(
        **proposta_data,
        vendedor_id=vendedor_id # Associa ao vendedor logado
    )
    
    # Se houver itens na criação, eles são adicionados
    # (Usado pela nossa nova lógica)
    if itens_data:
        for item_dto in itens_data:
            db_proposta.itens.append(models.PropostaItem(**item_dto))
            
    db.add(db_proposta)
    await db.commit()
    await db.refresh(db_proposta)
    # Recarrega com os dados do vendedor e cliente para retornar ao frontend
    return await get_proposta_by_id(db, db_proposta.id)

async def get_proposta_by_id(db: AsyncSession, proposta_id: int) -> Optional[models.Proposta]:
    '''Busca uma proposta específica, com dados do cliente, vendedor e ITENS'''
    query = (
        select(models.Proposta)
        .where(models.Proposta.id == proposta_id)
        .options(
            joinedload(models.Proposta.vendedor_responsavel), # Carrega o User
            joinedload(models.Proposta.cliente),            # Carrega o Cliente
            selectinload(models.Proposta.itens)             # Carrega a lista de Itens
        )
    )
    result = await db.execute(query)
    return result.scalars().first()

async def get_all_propostas(db: AsyncSession) -> List[models.Proposta]:
    '''Lista todas as propostas (para Gestores)'''
    query = (
        select(models.Proposta)
        .options(
            joinedload(models.Proposta.vendedor_responsavel),
            joinedload(models.Proposta.cliente),
            selectinload(models.Proposta.itens) # Também carregar itens na lista
        )
        .order_by(models.Proposta.id.desc())
    )
    result = await db.execute(query)
    return result.scalars().all()

async def get_propostas_por_vendedor(db: AsyncSession, vendedor_id: int) -> List[models.Proposta]:
    '''Lista propostas de um vendedor específico'''
    query = (
        select(models.Proposta)
        .where(models.Proposta.vendedor_id == vendedor_id) # O filtro de permissão
        .options(
            joinedload(models.Proposta.vendedor_responsavel),
            joinedload(models.Proposta.cliente),
            selectinload(models.Proposta.itens) # Também carregar itens na lista
        )
        .order_by(models.Proposta.id.desc())
    )
    result = await db.execute(query)
    return result.scalars().all()

# --- NOVO SERVIÇO 1 ---
async def save_dimensionamento_e_gerar_custos(
    db: AsyncSession, 
    proposta: models.Proposta, 
    data: schema.PropostaUpdateDimensionamento
) -> models.Proposta:
    '''
    Atualiza a proposta com os dados do dimensionamento e 
    gera a lista de custos inicial (baseada na image_692024.png)
    '''
    
    # 1. Atualiza os dados da proposta (Etapa 1)
    proposta.premissas = data.premissas
    proposta.potencia_kwp = data.potencia_kwp

    # 2. Limpa itens de custo antigos (se houver)
    # (Ou podemos adicionar uma lógica para preservar edições manuais)
    proposta.itens = [] 
    
    # 3. Adiciona o Kit selecionado (se houver)
    if data.kit_id:
        kit = await db.get(Kit, data.kit_id)
        if kit:
            proposta.itens.append(models.PropostaItem(
                categoria="Kit",
                descricao=f"{kit.nome_kit} (Cód: {kit.codigo_kit})",
                quantidade=1,
                custo_unitario=kit.custo_total_kit,
                valor_venda=kit.custo_total_kit # Inicialmente, valor de venda = custo
            ))

    # 4. Adiciona os placeholders de custo (baseado na sua imagem)
    placeholders = [
        ("Custos", "TRT OBRA / SERVIÇO", 85.00),
        ("Custos", "MONTAGEM", 220.00),
        ("Custos", "HOSPEDAGEM E ALIMENTAÇÃO", 0.00),
        ("Custos", "MATERIAIS ELÉTRICOS", 600.00),
        ("Custos", "ESTRUTURA / SOLO 1 LINHA", 0.00),
        ("Custos", "IMPOSTO", 647.54),
        ("Custos", "COMISSÃO", 462.96),
        ("Custos", "LUCRO", 2199.91),
        ("Custos", "ARREDONDAMENTO", 0.00),
        ("Custos", "ENG 1 %", 0.00),
        ("Custos", "LOCOMOÇÃO", 0.00),
        ("Outros", "INDICAÇÃO", 300.00)
    ]
    
    total_venda_calculado = Decimal(0)

    for cat, desc, valor in placeholders:
        item = models.PropostaItem(
            categoria=cat,
            descricao=desc,
            quantidade=1,
            custo_unitario=0, # Ajustar se você tiver o custo
            valor_venda=Decimal(valor)
        )
        proposta.itens.append(item)
        total_venda_calculado += item.valor_venda

    # 5. Atualiza o valor_total da proposta
    # (Idealmente, o valor_total seria a soma de todos os itens)
    proposta.valor_total = total_venda_calculado # Atualiza o total
    
    await db.commit()
    await db.refresh(proposta)
    return proposta

# --- NOVO SERVIÇO 2 ---
async def update_proposta_itens(
    db: AsyncSession, 
    proposta: models.Proposta, 
    data: schema.PropostaUpdateItens
) -> models.Proposta:
    '''
    Recebe a lista completa de itens da Etapa 2 (Custos) e 
    substitui os itens existentes.
    '''
    
    # 1. Limpa os itens antigos
    proposta.itens = []
    
    # 2. Adiciona os novos itens
    for item_dto in data.itens:
        novo_item = models.PropostaItem(**item_dto.model_dump())
        proposta.itens.append(novo_item)
        
    # 3. Atualiza o valor total da proposta
    proposta.valor_total = data.valor_total
    
    await db.commit()
    await db.refresh(proposta)
    # Recarrega os itens para garantir que a resposta esteja completa
    return await get_proposta_by_id(db, proposta.id)