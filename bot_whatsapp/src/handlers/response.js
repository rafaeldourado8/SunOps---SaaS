const amqp = require('amqplib');
const config = require('../config');
const whatsappService = require('../services/whatsapp');

class ResponseHandler {
  constructor() {
    this.connection = null;
    this.channel = null;
    this.responseQueue = 'whatsapp_responses';
  }

  async start() {
    try {
      this.connection = await amqp.connect(config.rabbitmq.url);
      this.channel = await this.connection.createChannel();
      await this.channel.assertQueue(this.responseQueue, { durable: true });
      
      console.log('✅ ResponseHandler aguardando respostas...');

      this.channel.consume(this.responseQueue, async (msg) => {
        if (msg) {
          await this.handleResponse(msg);
          this.channel.ack(msg);
        }
      });
    } catch (error) {
      console.error('❌ Erro no ResponseHandler:', error.message);
      setTimeout(() => this.start(), 5000);
    }
  }

  async handleResponse(msg) {
    try {
      const response = JSON.parse(msg.content.toString());
      const { to, text, typing } = response;

      // Simular digitação
      if (typing) {
        await whatsappService.sendTyping(to, typing);
        await this.sleep(typing);
      }

      // Enviar mensagem
      await whatsappService.sendMessage(to, text);
      console.log(`📤 Resposta enviada para ${to}`);

    } catch (error) {
      console.error('❌ Erro ao processar resposta:', error.message);
    }
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

module.exports = new ResponseHandler();
