const WebSocket = require('ws');
const config = require('../config');

class WebSocketService {
  constructor() {
    this.wss = null;
    this.clients = new Set();
  }

  start() {
    this.wss = new WebSocket.Server({ port: config.websocket.port });

    this.wss.on('connection', (ws) => {
      this.clients.add(ws);
      console.log('🔌 Cliente WebSocket conectado');

      ws.on('close', () => {
        this.clients.delete(ws);
        console.log('🔌 Cliente WebSocket desconectado');
      });
    });

    console.log(`✅ WebSocket rodando na porta ${config.websocket.port}`);
  }

  broadcast(event, data) {
    const message = JSON.stringify({ event, data });
    this.clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(message);
      }
    });
  }
}

module.exports = new WebSocketService();
