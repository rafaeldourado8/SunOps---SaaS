const rabbitmqService = require('../services/rabbitmq');

class MessageHandler {
  async handleIncoming(msg, client) {
    try {
      const messageData = {
        id: msg.id._serialized,
        from: msg.from,
        to: msg.to,
        body: msg.body,
        timestamp: msg.timestamp,
        hasMedia: msg.hasMedia,
        type: msg.type,
        isForwarded: msg.isForwarded,
        author: msg.author,
        contact: {
          name: msg._data.notifyName || 'Desconhecido',
          number: msg.from.replace('@c.us', '')
        }
      };

      // Processar áudio
      if (msg.hasMedia && msg.type === 'ptt') {
        const media = await msg.downloadMedia();
        messageData.audio = {
          mimetype: media.mimetype,
          data: media.data
        };
      }

      console.log(`📩 Mensagem recebida de ${messageData.contact.name}: ${msg.body}`);

      // Publicar no RabbitMQ
      const published = await rabbitmqService.publishMessage(messageData);
      
      if (!published) {
        console.error('❌ Falha ao publicar mensagem no RabbitMQ');
      }

    } catch (error) {
      console.error('❌ Erro ao processar mensagem:', error.message);
    }
  }
}

module.exports = new MessageHandler();
