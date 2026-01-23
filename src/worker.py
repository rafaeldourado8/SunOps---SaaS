from shared.infrastructure.message_broker import broker
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def processar_cliente_criado(message: dict):
    logger.info(f"Cliente criado: {message}")


def processar_desconto_solicitado(message: dict):
    logger.info(f"Desconto solicitado: {message}")


def main():
    logger.info("Worker iniciado...")
    broker.consume("cliente_criado", processar_cliente_criado)
    broker.consume("desconto_solicitado", processar_desconto_solicitado)


if __name__ == "__main__":
    main()
