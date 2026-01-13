const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const config = require('../config');
const websocketService = require('./websocket');
const messageHandler = require('../handlers/message');

class WhatsAppService {
  constructor() {
    this.client = new Client({
      authStrategy: new LocalAuth({ clientId: config.whatsapp.sessionName }),
      puppeteer: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
      }
    });

    this.setupEventHandlers();
  }

  setupEventHandlers() {
    this.client.on('qr', (qr) => {
      console.log('📱 QR Code gerado:');
      qrcode.generate(qr, { small: true });
      websocketService.broadcast('qr', qr);
    });

    this.client.on('ready', () => {
      console.log('✅ WhatsApp conectado e pronto!');
      websocketService.broadcast('ready', { status: 'connected' });
    });

    this.client.on('authenticated', () => {
      console.log('🔐 WhatsApp autenticado');
      websocketService.broadcast('authenticated', { status: 'authenticated' });
    });

    this.client.on('auth_failure', (msg) => {
      console.error('❌ Falha na autenticação:', msg);
      websocketService.broadcast('auth_failure', { error: msg });
    });

    this.client.on('disconnected', (reason) => {
      console.log('🔌 WhatsApp desconectado:', reason);
      websocketService.broadcast('disconnected', { reason });
    });

    this.client.on('message', async (msg) => {
      await messageHandler.handleIncoming(msg, this.client);
    });
  }

  async initialize() {
    await this.client.initialize();
  }

  async sendMessage(to, text) {
    try {
      await this.client.sendMessage(to, text);
      return true;
    } catch (error) {
      console.error('❌ Erro ao enviar mensagem:', error.message);
      return false;
    }
  }

  async sendTyping(to, duration = 3000) {
    try {
      const chat = await this.client.getChatById(to);
      await chat.sendStateTyping();
      setTimeout(async () => {
        await chat.clearState();
      }, duration);
    } catch (error) {
      console.error('❌ Erro ao enviar typing:', error.message);
    }
  }
}

module.exports = new WhatsAppService();
