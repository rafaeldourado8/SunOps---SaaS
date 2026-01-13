const amqp = require('amqplib');
const config = require('../config');

class RabbitMQService {
  constructor() {
    this.connection = null;
    this.channel = null;
  }

  async connect() {
    try {
      this.connection = await amqp.connect(config.rabbitmq.url);
      this.channel = await this.connection.createChannel();
      await this.channel.assertQueue(config.rabbitmq.queue, { durable: true });
      console.log('✅ RabbitMQ conectado');
    } catch (error) {
      console.error('❌ Erro ao conectar RabbitMQ:', error.message);
      setTimeout(() => this.connect(), 5000);
    }
  }

  async publishMessage(message) {
    if (!this.channel) {
      console.error('❌ Canal RabbitMQ não disponível');
      return false;
    }

    try {
      const payload = JSON.stringify(message);
      this.channel.sendToQueue(config.rabbitmq.queue, Buffer.from(payload), {
        persistent: true
      });
      return true;
    } catch (error) {
      console.error('❌ Erro ao publicar mensagem:', error.message);
      return false;
    }
  }

  async close() {
    await this.channel?.close();
    await this.connection?.close();
  }
}

module.exports = new RabbitMQService();
