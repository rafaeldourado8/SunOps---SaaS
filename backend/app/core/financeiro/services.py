from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, or_, delete, update
from sqlalchemy.orm import selectinload
from datetime import date, datetime, timedelta
from typing import List, Optional, Tuple
from decimal import Decimal

from fastapi import HTTPException, status

from . import models, schema
from app.core.sales.propostas.models import Proposta # Para calcular comissão
# Importação necessária para o novo código
from app.core.users.models import User 

async def get_configuracoes(db: AsyncSession) -> models.ConfiguracaoFinanceira:
    '''Busca as configurações financeiras (ou cria se não existirem)'''
    query = select(models.ConfiguracaoFinanceira).where(models.ConfiguracaoFinanceira.id == 1)
    result = await db.execute(query)
    config = result.scalars().first()
    
    # Se for o primeiro acesso, cria a linha de configuração padrão
    if not config:
        config = models.ConfiguracaoFinanceira()
        db.add(config)
        await db.commit()
        await db.refresh(config)
    return config

async def update_configuracoes(
    db: AsyncSession, 
    config_update: schema.UpdateConfiguracaoFinanceira
) -> models.ConfiguracaoFinanceira:
    '''Atualiza as configurações financeiras'''
    config = await get_configuracoes(db)
    
    config.margem_lucro_padrao = config_update.margem_lucro_padrao
    config.percentual_comissao_padrao = config_update.percentual_comissao_padrao
    
    await db.commit()
    await db.refresh(config)
    return config

async def get_transacoes_vencidas_pendentes(db: AsyncSession) -> List[models.Transacao]:
    '''Busca transações para o alerta do dashboard'''
    query = (
        select(models.Transacao)
        .where(
            models.Transacao.status == models.StatusTransacao.PENDENTE,
            models.Transacao.data_vencimento < date.today()
        )
    )
    result = await db.execute(query)
    transacoes = result.scalars().all()
    
    # Opcional: Atualiza o status para "ATRASADA"
    for t in transacoes:
        t.status = models.StatusTransacao.ATRASADA
    if transacoes:
        await db.commit()
        
    return transacoes

async def get_all_transacoes(db: AsyncSession) -> List[models.Transacao]:
    '''Lista todas as transações'''
    query = select(models.Transacao).order_by(models.Transacao.data_vencimento.desc())
    result = await db.execute(query)
    return result.scalars().all()

async def get_transacao_by_id(db: AsyncSession, transacao_id: int) -> Optional[models.Transacao]:
    query = select(models.Transacao).where(models.Transacao.id == transacao_id)
    result = await db.execute(query)
    return result.scalars().first()

async def marcar_transacao_paga(db: AsyncSession, transacao: models.Transacao) -> models.Transacao:
    '''Marca uma transação como paga'''
    transacao.status = models.StatusTransacao.PAGA
    transacao.data_pagamento = datetime.utcnow()
    await db.commit()
    await db.refresh(transacao)
    return transacao

# --- Lógica de Negócio (chamada por outros módulos) ---

async def criar_transacao_entrada_projeto(db: AsyncSession, proposta_ganha: Proposta):
    '''Chamado pelo módulo 'sales' quando uma proposta é 'GANHA' '''
    
    # Regra de negócio: A entrada é 30% do valor total?
    # IMPORTANTE: A proposta_ganha.valor_total precisa ser Decimal
    valor_entrada = proposta_ganha.valor_total * Decimal("0.30")
    
    nova_transacao = models.Transacao(
        descricao=f"Pagamento da entrada do Projeto {proposta_ganha.cliente.nome_razao_social}",
        valor=valor_entrada,
        tipo=models.TipoTransacao.ENTRADA_PROJETO,
        status=models.StatusTransacao.PENDENTE,
        # Corrigindo: Faltava 'from datetime import timedelta' no original
        data_vencimento=date.today() + timedelta(days=5), # Vence em 5 dias
        projeto_id=proposta_ganha.projeto.id, # Assumindo que o projeto é criado junto
    )
    db.add(nova_transacao)
    # O commit será feito pelo serviço chamador


# --- INÍCIO DO NOVO CÓDIGO DA FEATURE DE PREMISSAS ---

# --- Helpers de Validação ---

def _validar_datas_premissa(data_inicio: date, data_fim: date):
    """Valida se a data de início é anterior à data de fim."""
    if data_fim < data_inicio:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="A data final da vigência não pode ser anterior à data inicial."
        )

def _validar_sobreposicao_faixas(faixas: List[schema.PremissaFaixaCreate]) -> bool:
    """
    Valida se existe alguma sobreposição (overlap) nas faixas de potência.
    Ex: [0-4, 3-6] -> Inválido.
    """
    if not faixas:
        return True # Nenhuma faixa, nada a validar
        
    faixas_ordenadas = sorted(faixas, key=lambda f: f.potencia_min)
    
    for i in range(len(faixas_ordenadas) - 1):
        faixa_atual = faixas_ordenadas[i]
        proxima_faixa = faixas_ordenadas[i+1]
        
        # Se o máximo da faixa atual for maior que o mínimo da próxima, há sobreposição
        if faixa_atual.potencia_max > proxima_faixa.potencia_min:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Sobreposição detectada nas faixas: '{faixa_atual.nome_faixa}' ({faixa_atual.potencia_min}-{faixa_atual.potencia_max}kW) e '{proxima_faixa.nome_faixa}' ({proxima_faixa.potencia_min}-{proxima_faixa.potencia_max}kW)."
            )
    return True

# --- Helpers de Busca (CRUD) ---

async def get_premissa_by_id(db: AsyncSession, premissa_id: int, user: User) -> models.Premissa:
    """Busca uma premissa pelo ID, garantindo que pertença ao usuário (empresa)."""
    query = (
        select(models.Premissa)
        .where(
            models.Premissa.id == premissa_id,
            models.Premissa.empresa_id == user.id
        )
        # options(selectinload(models.Premissa.faixas), selectinload(models.Premissa.regioes)) # lazy="joined" já faz isso
    )
    result = await db.execute(query)
    premissa = result.scalars().first()
    
    if not premissa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Premissa não encontrada.")
    return premissa

async def get_faixa_by_id(db: AsyncSession, premissa_id: int, faixa_id: int, user: User) -> models.PremissaFaixa:
    """Busca uma faixa de premissa pelo ID, garantindo que pertença à premissa e ao usuário."""
    # Garante que a premissa pai pertence ao usuário
    premissa = await get_premissa_by_id(db, premissa_id, user)
    
    query = select(models.PremissaFaixa).where(
        models.PremissaFaixa.id == faixa_id,
        models.PremissaFaixa.premissa_id == premissa.id # Garante que a faixa é da premissa
    )
    result = await db.execute(query)
    faixa = result.scalars().first()
    
    if not faixa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Faixa da premissa não encontrada.")
    return faixa

async def get_regiao_by_id(db: AsyncSession, premissa_id: int, regiao_id: int, user: User) -> models.PremissaPorRegiao:
    """Busca uma região de premissa pelo ID, garantindo que pertença à premissa e ao usuário."""
    premissa = await get_premissa_by_id(db, premissa_id, user)
    
    query = select(models.PremissaPorRegiao).where(
        models.PremissaPorRegiao.id == regiao_id,
        models.PremissaPorRegiao.premissa_id == premissa.id
    )
    result = await db.execute(query)
    regiao = result.scalars().first()
    
    if not regiao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Região da premissa não encontrada.")
    return regiao

async def get_regiao_by_nome_e_premissa(db: AsyncSession, premissa_id: int, regiao_nome: str) -> Optional[models.PremissaPorRegiao]:
    """Busca uma configuração de região pelo nome (ex: 'SP') dentro de uma premissa."""
    query = select(models.PremissaPorRegiao).where(
        models.PremissaPorRegiao.premissa_id == premissa_id,
        models.PremissaPorRegiao.regiao.ilike(regiao_nome) # Case-insensitive
    )
    result = await db.execute(query)
    return result.scalars().first()


# --- Serviços de Premissa (CRUD) ---

async def listar_premissas(
    db: AsyncSession, 
    user: User, 
    ativa_apenas: bool = False, 
    data: Optional[date] = None
) -> List[models.Premissa]:
    """
    Lista todas as premissas de uma empresa, com filtros opcionais.
    - Filtra por vigência se 'data' for fornecida.
    - Filtra por 'ativa' se 'ativa_apenas' for True.
    - Ordena por data de vigência final (mais recentes primeiro).
    """
    query = select(models.Premissa).where(models.Premissa.empresa_id == user.id)
    
    if ativa_apenas:
        query = query.where(models.Premissa.ativa == True)
        
    if data:
        # Busca premissas cuja vigência (inicio E fim) engloba a data fornecida
        query = query.where(
            models.Premissa.data_vigencia_inicio <= data,
            models.Premissa.data_vigencia_fim >= data
        )
        
    query = query.order_by(models.Premissa.data_vigencia_fim.desc())
    
    result = await db.execute(query)
    return result.scalars().all()


async def criar_premissa(
    db: AsyncSession, 
    user: User, 
    premissa_create: schema.PremissaCreate
) -> models.Premissa:
    """Cria uma nova premissa com suas faixas e regiões aninhadas."""
    
    # 1. Validar dados da premissa
    _validar_datas_premissa(premissa_create.data_vigencia_inicio, premissa_create.data_vigencia_fim)
    
    # 2. Validar faixas aninhadas
    _validar_sobreposicao_faixas(premissa_create.faixas)
    
    # 3. Criar Premissa
    premissa_data = premissa_create.model_dump(exclude={"faixas", "regioes"})
    db_premissa = models.Premissa(**premissa_data, empresa_id=user.id)
    db.add(db_premissa)
    
    # 4. Criar Faixas e Regiões
    # Usamos o db_premissa (objeto ORM) para o relacionamento
    db_premissa.faixas = [
        models.PremissaFaixa(**faixa.model_dump()) for faixa in premissa_create.faixas
    ]
    db_premissa.regioes = [
        models.PremissaPorRegiao(**regiao.model_dump()) for regiao in premissa_create.regioes
    ]

    try:
        await db.commit()
        await db.refresh(db_premissa)
        return db_premissa
    except Exception as e:
        await db.rollback()
        # Captura erros de constraint (ex: FK)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar premissa: {e}"
        )

async def atualizar_premissa(
    db: AsyncSession, 
    premissa_id: int, 
    user: User, 
    premissa_update: schema.PremissaUpdate
) -> models.Premissa:
    """Atualiza os dados principais de uma premissa (não atualiza faixas/regiões)."""
    db_premissa = await get_premissa_by_id(db, premissa_id, user)
    
    update_data = premissa_update.model_dump(exclude_unset=True)

    # Validar datas se elas foram alteradas
    data_inicio = update_data.get("data_vigencia_inicio", db_premissa.data_vigencia_inicio)
    data_fim = update_data.get("data_vigencia_fim", db_premissa.data_vigencia_fim)
    _validar_datas_premissa(data_inicio, data_fim)

    for key, value in update_data.items():
        setattr(db_premissa, key, value)
        
    db_premissa.atualizada_em = datetime.utcnow() # Força atualização
    
    try:
        await db.commit()
        await db.refresh(db_premissa)
        return db_premissa
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar premissa: {e}"
        )

async def deletar_premissa(db: AsyncSession, premissa_id: int, user: User) -> bool:
    """Deleta uma premissa (e suas faixas/regiões via cascade)."""
    db_premissa = await get_premissa_by_id(db, premissa_id, user)
    
    await db.delete(db_premissa)
    await db.commit()
    return True


# --- Serviços de Faixas (Sub-CRUD) ---

async def adicionar_faixa(
    db: AsyncSession, 
    premissa_id: int, 
    user: User, 
    faixa_create: schema.PremissaFaixaCreate
) -> models.PremissaFaixa:
    """Adiciona uma nova faixa a uma premissa existente."""
    db_premissa = await get_premissa_by_id(db, premissa_id, user)
    
    # Validar sobreposição com faixas existentes
    faixas_atuais_schemas = [
        schema.PremissaFaixaCreate.model_validate(f) for f in db_premissa.faixas
    ]
    _validar_sobreposicao_faixas(faixas_atuais_schemas + [faixa_create])
    
    db_faixa = models.PremissaFaixa(
        **faixa_create.model_dump(),
        premissa_id=db_premissa.id
    )
    
    db.add(db_faixa)
    await db.commit()
    await db.refresh(db_faixa)
    return db_faixa

async def atualizar_faixa(
    db: AsyncSession, 
    premissa_id: int, 
    faixa_id: int, 
    user: User, 
    faixa_update: schema.PremissaFaixaCreate # Reusa o Create schema
) -> models.PremissaFaixa:
    """Atualiza uma faixa existente."""
    db_faixa = await get_faixa_by_id(db, premissa_id, faixa_id, user)
    
    # Validar sobreposição (excluindo a própria faixa da validação)
    outras_faixas = [
        schema.PremissaFaixaCreate.model_validate(f) 
        for f in db_faixa.premissa.faixas if f.id != faixa_id
    ]
    _validar_sobreposicao_faixas(outras_faixas + [faixa_update])

    update_data = faixa_update.model_dump()
    for key, value in update_data.items():
        setattr(db_faixa, key, value)

    await db.commit()
    await db.refresh(db_faixa)
    return db_faixa
    
async def deletar_faixa(db: AsyncSession, premissa_id: int, faixa_id: int, user: User) -> bool:
    """Deleta uma faixa de uma premissa."""
    db_faixa = await get_faixa_by_id(db, premissa_id, faixa_id, user)
    await db.delete(db_faixa)
    await db.commit()
    return True

# --- Serviços de Regiões (Sub-CRUD) ---

async def adicionar_regiao(
    db: AsyncSession, 
    premissa_id: int, 
    user: User, 
    regiao_create: schema.PremissaPorRegiaoCreate
) -> models.PremissaPorRegiao:
    """Adiciona uma nova região (alíquota) a uma premissa."""
    db_premissa = await get_premissa_by_id(db, premissa_id, user)
    
    # Validar se a região já existe para esta premissa
    regiao_existente = await get_regiao_by_nome_e_premissa(db, premissa_id, regiao_create.regiao)
    if regiao_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A região '{regiao_create.regiao}' já está cadastrada nesta premissa."
        )

    db_regiao = models.PremissaPorRegiao(
        **regiao_create.model_dump(),
        premissa_id=db_premissa.id
    )
    
    db.add(db_regiao)
    await db.commit()
    await db.refresh(db_regiao)
    return db_regiao

async def atualizar_regiao(
    db: AsyncSession, 
    premissa_id: int, 
    regiao_id: int, 
    user: User, 
    regiao_update: schema.PremissaPorRegiaoCreate # Reusa o Create
) -> models.PremissaPorRegiao:
    """Atualiza uma configuração de região."""
    db_regiao = await get_regiao_by_id(db, premissa_id, regiao_id, user)

    # Se o nome da região mudou, verificar se o novo nome já existe
    if regiao_update.regiao.upper() != db_regiao.regiao.upper():
        regiao_existente = await get_regiao_by_nome_e_premissa(db, premissa_id, regiao_update.regiao)
        if regiao_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A região '{regiao_update.regiao}' já está cadastrada nesta premissa."
            )

    update_data = regiao_update.model_dump()
    for key, value in update_data.items():
        setattr(db_regiao, key, value)

    await db.commit()
    await db.refresh(db_regiao)
    return db_regiao

async def deletar_regiao(db: AsyncSession, premissa_id: int, regiao_id: int, user: User) -> bool:
    """Deleta uma configuração de região."""
    db_regiao = await get_regiao_by_id(db, premissa_id, regiao_id, user)
    await db.delete(db_regiao)
    await db.commit()
    return True


# --- Serviço Principal: Cálculo de Preço ---

async def encontrar_faixa(
    db: AsyncSession, 
    premissa_id: int, 
    potencia: float
) -> Optional[models.PremissaFaixa]:
    """Encontra a faixa de preço aplicável para uma dada potência."""
    query = select(models.PremissaFaixa).where(
        models.PremissaFaixa.premissa_id == premissa_id,
        models.PremissaFaixa.potencia_min <= potencia,
        models.PremissaFaixa.potencia_max >= potencia
    )
    result = await db.execute(query)
    return result.scalars().first()

async def get_premissa_ativa_recente(
    db: AsyncSession, 
    user: User, 
    data_calculo: date
) -> Optional[models.Premissa]:
    """Busca a premissa ativa mais recente baseada na data de cálculo."""
    query = (
        select(models.Premissa)
        .where(
            models.Premissa.empresa_id == user.id,
            models.Premissa.ativa == True,
            models.Premissa.data_vigencia_inicio <= data_calculo,
            models.Premissa.data_vigencia_fim >= data_calculo
        )
        .order_by(models.Premissa.data_vigencia_fim.desc()) # A mais recente
        .limit(1)
    )
    result = await db.execute(query)
    return result.scalars().first()


async def calcular_preco(
    db: AsyncSession, 
    user: User, 
    calculo_request: schema.CalculoPrecosRequest
) -> schema.CalculoPrecosResponse:
    """
    Serviço principal para calcular o preço final de um sistema
    baseado nas premissas e overrides.
    """
    
    # 1. Obter Configurações Globais (Margem/Comissão Padrão)
    config_global = await get_configuracoes(db)
    
    # 2. Obter Premissa
    premissa = None
    if calculo_request.premissa_id:
        # Busca por ID (ignora data e status 'ativa')
        premissa = await get_premissa_by_id(db, calculo_request.premissa_id, user)
    else:
        # Busca automática (ativa e vigente na data)
        premissa = await get_premissa_ativa_recente(db, user, calculo_request.data)
        if not premissa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nenhuma premissa de preço ativa encontrada para a data {calculo_request.data}."
            )
            
    # 3. Obter Faixa de Preço (baseado na potência)
    # Convertemos kW (ex: 5.5) para Wp (ex: 5500) para o cálculo base
    potencia_wp = Decimal(str(calculo_request.potencia_kw * 1000))
    
    faixa = await encontrar_faixa(db, premissa.id, calculo_request.potencia_kw)
    if not faixa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nenhuma faixa de preço encontrada na premissa '{premissa.nome}' para a potência de {calculo_request.potencia_kw}kW."
        )
        
    # 4. Obter Configuração de Região (Imposto)
    regiao_config = await get_regiao_by_nome_e_premissa(db, premissa.id, calculo_request.regiao)
    if not regiao_config and not calculo_request.imposto_override:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Configuração de imposto para a região '{calculo_request.regiao}' não encontrada na premissa '{premissa.nome}'. Use 'imposto_override' se desejar."
        )

    # 5. Definir Parâmetros de Cálculo (Padrão vs Override)
    detalhes = {}
    
    preco_unitario_wp = faixa.preco_unitario # Decimal
    
    custos_adicionais = calculo_request.custos_adicionais # Decimal

    margem_pct = calculo_request.margem_lucro_override
    if margem_pct is None:
        margem_pct = config_global.margem_lucro_padrao
        detalhes["margem_pct_origem"] = "Configuração Global"
    else:
        detalhes["margem_pct_origem"] = "Override"

    comissao_pct = calculo_request.comissao_override
    if comissao_pct is None:
        comissao_pct = config_global.percentual_comissao_padrao
        detalhes["comissao_pct_origem"] = "Configuração Global"
    else:
        detalhes["comissao_pct_origem"] = "Override"

    imposto_pct = calculo_request.imposto_override
    if imposto_pct is None:
        imposto_pct = regiao_config.aliquota_imposto
        detalhes["imposto_pct_origem"] = f"Premissa (Região: {regiao_config.regiao})"
    else:
        detalhes["imposto_pct_origem"] = "Override"

    # 6. Executar Cálculo (usando Decimal para precisão monetária)
    
    # preco_base = potencia × preco_unitario
    # Ex: 5500 Wp * R$ 0.23/Wp
    preco_base = (potencia_wp * preco_unitario_wp).quantize(Decimal("0.01"))
    
    # subtotal_custos = preco_base + custos_adicionais
    subtotal_custos = (preco_base + custos_adicionais).quantize(Decimal("0.01"))
    
    # margem_lucro_valor = subtotal_custos × %margem
    margem_valor = (subtotal_custos * Decimal(str(margem_pct))).quantize(Decimal("0.01"))
    
    # comissao_valor = subtotal_custos × %comissao
    comissao_valor = (subtotal_custos * Decimal(str(comissao_pct))).quantize(Decimal("0.01"))
    
    # subtotal_sem_imposto = subtotal_custos + margem_lucro_valor + comissao_valor
    subtotal_sem_imposto = (subtotal_custos + margem_valor + comissao_valor).quantize(Decimal("0.01"))
    
    # imposto_valor = subtotal_sem_imposto × %imposto
    imposto_valor = (subtotal_sem_imposto * Decimal(str(imposto_pct))).quantize(Decimal("0.01"))
    
    # preco_final = subtotal_sem_imposto + imposto_valor
    preco_final = (subtotal_sem_imposto + imposto_valor).quantize(Decimal("0.01"))

    # 7. Montar Resposta
    return schema.CalculoPrecosResponse(
        potencia_solicitada_kw=calculo_request.potencia_kw,
        regiao=calculo_request.regiao.upper(),
        data_calculo=calculo_request.data,
        premissa_usada_id=premissa.id,
        premissa_usada_nome=premissa.nome,
        faixa_aplicada_nome=faixa.nome_faixa,
        preco_unitario_wp=preco_unitario_wp,
        preco_base=preco_base,
        custos_adicionais=custos_adicionais,
        subtotal_custos=subtotal_custos,
        margem_lucro_percentual=margem_pct,
        margem_lucro_valor=margem_valor,
        comissao_percentual=comissao_pct,
        comissao_valor=comissao_valor,
        subtotal_sem_imposto=subtotal_sem_imposto,
        imposto_percentual=imposto_pct,
        imposto_valor=imposto_valor,
        preco_final=preco_final,
        detalhes=detalhes
    )

# --- FIM DO NOVO CÓDIGO DA FEATURE DE PREMISSAS ---