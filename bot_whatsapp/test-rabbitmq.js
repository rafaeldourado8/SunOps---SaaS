const amqp = require('amqplib');

async function testRabbitMQ() {
  try {
    console.log('🧪 Testando conexão RabbitMQ...');
    
    const connection = await amqp.connect('amqp://guest:guest@localhost:5672');
    const channel = await connection.createChannel();
    
    await channel.assertQueue('whatsapp_messages', { durable: true });
    await channel.assertQueue('whatsapp_responses', { durable: true });
    
    console.log('✅ Filas criadas com sucesso!');
    console.log('   - whatsapp_messages (entrada)');
    console.log('   - whatsapp_responses (saída)');
    
    await channel.close();
    await connection.close();
    
    console.log('✅ Teste concluído!');
    process.exit(0);
    
  } catch (error) {
    console.error('❌ Erro:', error.message);
    console.log('\n💡 Certifique-se de que o RabbitMQ está rodando:');
    console.log('   docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management');
    process.exit(1);
  }
}

testRabbitMQ();
