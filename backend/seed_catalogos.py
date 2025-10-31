# backend/seed_catalogos.py
import json
import asyncio
import logging
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession  # <--- CORREÇÃO AQUI

# Importa a configuração da sessão assíncrona e a Base do seu app
from app.db import async_session, Base, engine

# Importa os modelos que vamos popular
from app.core.equipamentos.models import Equipamento, CategoriaEquipamento

# Configura um logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define os arquivos e suas respectivas categorias
CATALOGOS = {
    "Módulos": "catalogo_modulos.json",
    "Inversores": "catalogo_inversores.json"
}

async def init_db():
    """
    Cria todas as tabelas no banco de dados com base nos modelos.
    """
    async with engine.begin() as conn:
        logger.info("Inicializando o banco de dados e criando tabelas (se não existirem)...")
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Tabelas criadas com sucesso.")

async def get_or_create_categoria(session: AsyncSession, nome_categoria: str) -> CategoriaEquipamento:
    """
    Busca uma categoria pelo nome. Se não existir, cria, salva e a retorna.
    """
    # Tenta encontrar a categoria
    result = await session.execute(
        select(CategoriaEquipamento).where(CategoriaEquipamento.nome == nome_categoria)
    )
    categoria = result.scalar_one_or_none()
    
    # Se não encontrar, cria uma nova
    if not categoria:
        logger.info(f"Categoria '{nome_categoria}' não encontrada. Criando...")
        categoria = CategoriaEquipamento(nome=nome_categoria)
        session.add(categoria)
        try:
            await session.flush()
            await session.refresh(categoria)
            logger.info(f"Categoria '{nome_categoria}' criada com ID: {categoria.id}.")
        except IntegrityError:
            await session.rollback()
            result = await session.execute(
                select(CategoriaEquipamento).where(CategoriaEquipamento.nome == nome_categoria)
            )
            categoria = result.scalar_one()
    
    return categoria

async def seed_data():
    """
    Função principal para ler os JSONs e popular o banco de dados.
    """
    logger.info("Iniciando o processo de seeding dos catálogos...")
    
    async with async_session() as session:
        result = await session.execute(select(Equipamento.nome_modelo))
        modelos_existentes = {row[0] for row in result}
        logger.info(f"Encontrados {len(modelos_existentes)} equipamentos existentes no DB.")

    async with async_session() as session:
        try:
            total_adicionados = 0
            
            for nome_categoria, nome_arquivo in CATALOGOS.items():
                logger.info(f"Processando arquivo: {nome_arquivo} para Categoria: {nome_categoria}")
                
                # 1. Garante que a categoria existe
                categoria = await get_or_create_categoria(session, nome_categoria)
                
                # 2. Carrega os dados do JSON
                try:
                    # O script é executado de /app/ dentro do container
                    with open(nome_arquivo, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except FileNotFoundError:
                    logger.error(f"ERRO: Arquivo '{nome_arquivo}' não encontrado. Pulando...")
                    continue
                except json.JSONDecodeError:
                    logger.error(f"ERRO: Arquivo '{nome_arquivo}' não é um JSON válido. Pulando...")
                    continue

                # 3. Itera e adiciona os equipamentos
                adicionados_neste_arquivo = 0
                for item in data:
                    nome_modelo = item.get("nome_modelo")
                    
                    if not nome_modelo:
                        logger.warning(f"Item sem 'nome_modelo' encontrado em {nome_arquivo}. Pulando.")
                        continue
                        
                    # 4. Verifica se o equipamento já existe
                    if nome_modelo not in modelos_existentes:
                        novo_equipamento = Equipamento(
                            categoria_id=categoria.id,
                            nome_modelo=nome_modelo,
                            fabricante=item.get("fabricante"),
                            potencia_w=item.get("potencia_w") 
                        )
                        session.add(novo_equipamento)
                        modelos_existentes.add(nome_modelo) 
                        adicionados_neste_arquivo += 1
                
                logger.info(f"Adicionados {adicionados_neste_arquivo} novos equipamentos de {nome_arquivo}.")
                total_adicionados += adicionados_neste_arquivo

            # 5. Comita a transação
            if total_adicionados > 0:
                await session.commit()
                logger.info(f"Sucesso! {total_adicionados} novos equipamentos foram salvos no banco de dados.")
            else:
                logger.info("Nenhum equipamento novo para adicionar. O banco de dados já está atualizado.")

        except IntegrityError as e:
            logger.error(f"Erro de integridade ao salvar dados (possível duplicata não detectada): {e}")
            await session.rollback()
        except Exception as e:
            logger.error(f"Ocorreu um erro inesperado: {e}")
            await session.rollback()

async def main():
    await init_db()
    await seed_data()

if __name__ == "__main__":
    logger.info("Iniciando script de seeding dentro do container...")
    asyncio.run(main())