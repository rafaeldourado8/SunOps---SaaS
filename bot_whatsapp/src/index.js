const rabbitmqService = require('./services/rabbitmq');
const websocketService = require('./services/websocket');
const whatsappService = require('./services/whatsapp');
const responseHandler = require('./handlers/response');

async function main() {
  console.log('🚀 Iniciando SunOps WhatsApp Gateway...\n');

  try {
    // Inicializar RabbitMQ
    await rabbitmqService.connect();

    // Inicializar WebSocket
    websocketService.start();

    // Inicializar WhatsApp
    await whatsappService.initialize();

    // Inicializar ResponseHandler
    await responseHandler.start();

    console.log('\n✅ Gateway inicializado com sucesso!\n');

  } catch (error) {
    console.error('❌ Erro ao inicializar gateway:', error.message);
    process.exit(1);
  }
}

// Graceful shutdown
process.on('SIGINT', async () => {
  console.log('\n🛑 Encerrando gateway...');
  await rabbitmqService.close();
  process.exit(0);
});

main();
