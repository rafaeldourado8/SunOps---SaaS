require('dotenv').config();

module.exports = {
  rabbitmq: {
    url: process.env.RABBITMQ_URL || 'amqp://guest:guest@localhost:5672',
    queue: process.env.RABBITMQ_QUEUE || 'whatsapp_messages'
  },
  websocket: {
    port: parseInt(process.env.WS_PORT) || 3001
  },
  whatsapp: {
    sessionName: process.env.WHATSAPP_SESSION_NAME || 'sunops-session'
  }
};
